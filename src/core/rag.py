"""RAG retriever — indexes CLIPS PDF docs and retrieves relevant chunks.

Architecture (simple, no overengineering):
  1. PDFs in src/assets/clips_docs/ are extracted with pdfplumber
  2. Text is split into ~500-char chunks with 100-char overlap
  3. Each chunk is embedded with all-MiniLM-L6-v2 (80 MB, runs on CPU)
  4. Embeddings + text stored in a persistent ChromaDB index (.rag_index/)
  5. At query time, the retriever returns top-3 chunks above a similarity threshold
  6. Chunks are injected as context into the LLM system prompt (model decides)

The index is built once (first call or explicit re-index) and persisted to disk.
Indexing takes ~30-60s on first run (downloading the embedding model + processing).
Retrieval takes ~40-80 ms per query.
"""

from __future__ import annotations

import os
import re
import threading
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Paths & tuning knobs
# ---------------------------------------------------------------------------

DOCS_DIR = Path(__file__).parent.parent / "assets" / "clips_docs"
CHROMA_DIR = DOCS_DIR / ".rag_index"
EMBED_MODEL = "all-MiniLM-L6-v2"

CHUNK_SIZE = 500          # characters per chunk
CHUNK_OVERLAP = 100       # overlap between consecutive chunks
MIN_CHUNK_LEN = 80        # discard tiny fragments
TOP_K = 3                 # chunks retrieved per query
SIMILARITY_THRESHOLD = 0.28  # cosine similarity minimum (Chroma returns distance)


# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------

def _extract_pdf_text(path: Path) -> str:
    """Return all text from a single PDF page by page (uses pymupdf — fast & robust)."""
    import fitz
    doc = fitz.open(str(path))
    pages: list[str] = []
    for page in doc:
        text = page.get_text()
        if text:
            pages.append(text)
    doc.close()
    return "\n".join(pages)


def _split_text(text: str) -> list[str]:
    """Split text into chunks on newline boundaries near CHUNK_SIZE."""
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + CHUNK_SIZE, len(text))
        if end < len(text):
            nl = text.rfind("\n", start, end)
            if nl > start + CHUNK_SIZE // 2:
                end = nl
        chunk = text[start:end].strip()
        if len(chunk) >= MIN_CHUNK_LEN:
            chunks.append(chunk)
        if end == len(text):
            break
        start = end - CHUNK_OVERLAP
    return chunks


# ---------------------------------------------------------------------------
# Embedding function (plain callable, no ChromaDB coupling)
# ---------------------------------------------------------------------------

class _EmbedFn:
    """Wraps sentence-transformers as a ChromaDB-compatible embedding function."""

    @staticmethod
    def name() -> str:
        return f"st_{EMBED_MODEL}"

    def __init__(self) -> None:
        from sentence_transformers import SentenceTransformer
        self._model = SentenceTransformer(EMBED_MODEL)

    def embed_query(self, input: str) -> list[float]:
        return self._model.encode(input).tolist()  # type: ignore[no-any-return]

    def embed_documents(self, input: list[str]) -> list[list[float]]:
        return self._model.encode(input).tolist()  # type: ignore[no-any-return]

    def __call__(self, input: list[str]) -> list[list[float]]:
        return self.embed_documents(input)


# ---------------------------------------------------------------------------
# Singleton retriever
# ---------------------------------------------------------------------------

_lock = threading.Lock()
_instance: Optional["ClipsRetriever"] = None


def get_retriever() -> "ClipsRetriever":
    """Return the shared singleton retriever (lazy-init, thread-safe)."""
    global _instance
    if _instance is None:
        with _lock:
            if _instance is None:
                _instance = ClipsRetriever()
    return _instance


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

class ClipsRetriever:
    """Lightweight RAG engine for CLIPS documentation.

    Usage:
        retriever = get_retriever()
        if not retriever.is_indexed():
            retriever.index_documents()
        chunks = retriever.retrieve("how to define a rule with salience")
    """

    def __init__(self) -> None:
        self._vectorstore: object = None   # ChromaDB collection
        self._embed_fn: _EmbedFn | None = None

    # ------------------------------------------------------------------
    # Indexing
    # ------------------------------------------------------------------

    def is_indexed(self) -> bool:
        """Return True if the vector index exists on disk."""
        return CHROMA_DIR.exists()

    def index_documents(self) -> None:
        """Extract, chunk, embed and store all PDFs in ChromaDB.

        Safe to call multiple times — re-creates the index from scratch.
        """
        import chromadb

        pdf_files = sorted(DOCS_DIR.glob("*.pdf"))
        if not pdf_files:
            raise RuntimeError(f"No PDFs found in {DOCS_DIR}")

        CHROMA_DIR.mkdir(parents=True, exist_ok=True)
        self._embed_fn = _EmbedFn()

        # Remove old index to start fresh
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        try:
            client.delete_collection("clips_docs")
        except Exception:
            pass

        collection = client.create_collection(
            name="clips_docs",
            embedding_function=self._embed_fn,  # type: ignore[arg-type]
        )

        all_chunks: list[str] = []
        all_ids: list[str] = []
        all_sources: list[str] = []

        for pdf_path in pdf_files:
            text = _extract_pdf_text(pdf_path)
            chunks = _split_text(text)
            source = pdf_path.name
            for i, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                all_ids.append(f"{source}_{i}")
                all_sources.append(source)

        # Add in batches of 200 to avoid huge memory spikes
        BATCH = 200
        for i in range(0, len(all_chunks), BATCH):
            batch_end = i + BATCH
            collection.add(
                documents=all_chunks[i:batch_end],
                ids=all_ids[i:batch_end],
                metadatas=[{"source": s} for s in all_sources[i:batch_end]],
            )

        self._vectorstore = collection

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    def _ensure_loaded(self) -> None:
        """Lazy-load the persistent collection from disk.

        If the index does not exist yet, builds it first.
        """
        if self._vectorstore is not None:
            return

        import chromadb

        if not self.is_indexed():
            self.index_documents()
            return

        if self._embed_fn is None:
            self._embed_fn = _EmbedFn()

        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        self._vectorstore = client.get_collection(
            name="clips_docs",
            embedding_function=self._embed_fn,  # type: ignore[arg-type]
        )

    def retrieve(self, query: str, top_k: int = TOP_K) -> list[dict]:
        """Retrieve relevant chunks for *query*.

        Returns a list of dicts with keys ``text``, ``score``, ``source``.
        Empty list when nothing passes the similarity threshold.
        """
        self._ensure_loaded()

        results = self._vectorstore.query(  # type: ignore[union-attr]
            query_texts=[query],
            n_results=top_k,
        )

        docs = results.get("documents", [[]])[0]
        dist = results.get("distances", [[]])[0]
        meta = results.get("metadatas", [[]])[0]

        items: list[dict] = []
        for text, distance, metadata in zip(docs, dist, meta):
            score = 1.0 - distance
            if score >= SIMILARITY_THRESHOLD:
                items.append({
                    "text": text,
                    "score": round(score, 3),
                    "source": metadata.get("source", ""),
                })
        return items

    def format_context(self, query: str) -> str:
        """Retrieve chunks and format them as a prose block for prompt injection.

        Returns an empty string if nothing relevant was found.
        """
        items = self.retrieve(query)
        if not items:
            return ""

        sections = []
        for item in items:
            sections.append(
                f"[From: {item['source']} | relevance: {item['score']}]\n{item['text']}"
            )
        return (
            "The following excerpts are from the official CLIPS 6.4 documentation. "
            "Use them if they are relevant to answer the user's question. "
            "If they are not relevant, ignore them.\n\n"
            + "\n\n---\n\n".join(sections)
        )
