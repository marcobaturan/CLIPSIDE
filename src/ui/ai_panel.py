"""AI assistant panel — Ollama chat with streaming and snippet insertion.

Optionally augmented with RAG (Retrieval-Augmented Generation) over
the official CLIPS 6.4 documentation stored in src/assets/clips_docs/.
"""

import threading
import customtkinter as ctk
import tkinter as tk
from typing import Callable, Optional

from src.core import ollama_client as ai
from src.core import session_history as sh
from src.core.rag import get_retriever


class AiPanel(ctk.CTkFrame):
    """
    Right-side AI assistant panel.

    Provides a streaming chat interface and a snippet generator
    that inserts code directly into the active editor tab.

    When RAG is enabled (toggle button), the user's question is
    first used to retrieve relevant excerpts from the CLIPS
    documentation. Those excerpts are injected into the system
    prompt so the model can ground its answer on official docs.
    """

    def __init__(
        self,
        parent,
        on_insert_snippet: Callable[[str], None],
        show_header: bool = True,
        **kwargs,
    ) -> None:
        super().__init__(parent, fg_color="#0D1117", **kwargs)
        self._on_insert = on_insert_snippet
        self._show_header = show_header
        self._session_id = sh.new_session_id()
        self._last_snippet = ""
        self._rag_enabled = True
        self._rag_ready = False
        self._build()
        self._check_ollama()
        self._init_rag()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build(self) -> None:
        # Title bar (optional — suppressed when parent draws its own header)
        if self._show_header:
            header = ctk.CTkFrame(self, fg_color="#161B22", height=32)
            header.pack(fill="x")
            ctk.CTkLabel(
                header, text="  🤖 AI Assistant",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#00FF88",
            ).pack(side="left", padx=6, pady=4)



        # Ollama status indicator
        self._status_label = ctk.CTkLabel(
            self, text="● Checking Ollama…",
            font=ctk.CTkFont(size=10), text_color="#546E7A",
        )
        self._status_label.pack(anchor="w", padx=8, pady=(4, 0))

        # Chat input section — pinned to bottom
        input_frame = ctk.CTkFrame(self, fg_color="#161B22")
        input_frame.pack(side="bottom", fill="x", padx=4, pady=4)
        
        self._chat_entry = ctk.CTkTextbox(
            input_frame, height=64, wrap="word",
            fg_color="#0D1117", border_color="#374151",
            font=ctk.CTkFont(family="Courier New", size=11),
        )
        self._chat_entry.pack(fill="x", padx=4, pady=(4, 2))
        
        btn_row = ctk.CTkFrame(input_frame, fg_color="transparent")
        btn_row.pack(fill="x", padx=4, pady=(0, 4))

        ctk.CTkButton(
            btn_row, text="Send", width=80, height=26,
            fg_color="#1F6FEB", hover_color="#388BFD",
            command=self._send_chat,
        ).pack(side="left", padx=(0, 4))
        
        ctk.CTkButton(
            btn_row, text="Insert ↗", width=80, height=26,
            fg_color="#238636", hover_color="#2EA043",
            command=self._insert_last_block,
        ).pack(side="left", padx=(0, 4))

        ctk.CTkButton(
            btn_row, text="Clear", width=80, height=26,
            fg_color="#454D59", hover_color="#546E7A",
            command=self._clear_chat,
        ).pack(side="left")

        self._rag_btn = ctk.CTkButton(
            btn_row, text="🔍 RAG", width=60, height=26,
            fg_color="#1F6FEB", hover_color="#388BFD",
            command=self._toggle_rag,
        )
        self._rag_btn.pack(side="right", padx=(4, 0))

        self._chat_entry.bind("<Control-Return>", lambda _: self._send_chat())

        # Chat display area — fills the rest
        self._chat_display = tk.Text(
            self, bg="#0D1117", fg="#EEFFFF",
            font=("Courier New", 11), state="disabled",
            wrap="word", relief="flat", padx=8, pady=4,
        )
        self._chat_display.tag_config("user",      foreground="#00FF88")
        self._chat_display.tag_config("assistant", foreground="#89DDFF")
        self._chat_display.tag_config("error",     foreground="#FF5370")
        self._chat_display.tag_config("system",    foreground="#546E7A")
        
        scroll = ctk.CTkScrollbar(self, command=self._chat_display.yview)
        self._chat_display.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self._chat_display.pack(fill="both", expand=True)

    # ------------------------------------------------------------------
    # RAG initialisation (background, non-blocking)
    # ------------------------------------------------------------------

    def _init_rag(self) -> None:
        """Ensure the vector index exists. Runs in a thread so the UI stays responsive."""
        def _work():
            try:
                retriever = get_retriever()
                if not retriever.is_indexed():
                    self._update_status("● Indexing CLIPS docs (first run)…", "#FFCB6B")
                    retriever.index_documents()
                self._rag_ready = True
                self._update_status("● Ollama ready" if ai.check_ollama_available() else "● Ollama not running", "#00FF88" if ai.check_ollama_available() else "#FF5370")
            except Exception as exc:
                self._rag_ready = False
                self._update_status(f"● RAG unavailable: {exc}", "#FF5370")
        threading.Thread(target=_work, daemon=True).start()

    def _update_status(self, text: str, colour: str) -> None:
        self._status_label.configure(text=text, text_color=colour)

    # ------------------------------------------------------------------
    # Ollama availability
    # ------------------------------------------------------------------

    def _check_ollama(self) -> None:
        """Check Ollama availability in a background thread."""
        def _check():
            available = ai.check_ollama_available()
            colour = "#00FF88" if available else "#FF5370"
            text = "● Ollama ready" if available else "● Ollama not running"
            self._status_label.configure(text_color=colour, text=text)
        threading.Thread(target=_check, daemon=True).start()

    # ------------------------------------------------------------------
    # Chat Logic
    # ------------------------------------------------------------------

    def _clear_chat(self) -> None:
        """Clear the chat display and reset history."""
        self._chat_display.config(state="normal")
        self._chat_display.delete("1.0", "end")
        self._chat_display.config(state="disabled")
        self._last_snippet = ""

    def _insert_last_block(self) -> None:
        """Insert the last block of text (ideally code) into the editor."""
        if self._last_snippet:
            self._on_insert(self._last_snippet)

    def _toggle_rag(self) -> None:
        """Enable / disable RAG context injection."""
        self._rag_enabled = not self._rag_enabled
        colour = "#1F6FEB" if self._rag_enabled else "#454D59"
        label = "🔍 RAG" if self._rag_enabled else "🔍 RAG"
        self._rag_btn.configure(fg_color=colour, hover_color=colour)
        status = "RAG enabled" if self._rag_enabled else "RAG disabled"
        self._append_chat(f"[{status}]\n", "system")

    def _send_chat(self) -> None:
        """Stream a chat response from the model."""
        message = self._chat_entry.get("1.0", "end-1c").strip()
        if not message:
            return
        self._chat_entry.delete("1.0", "end")
        self._append_chat(f"You: {message}\n", "user")
        self._append_chat("Assistant: ", "assistant")

        self._last_snippet = "" # Reset for current response

        # Retrieve RAG context if enabled and ready
        rag_context = ""
        if self._rag_enabled and self._rag_ready:
            try:
                retriever = get_retriever()
                rag_context = retriever.format_context(message)
                if rag_context:
                    self._append_chat("📖 +docs\n", "system")
            except Exception:
                pass  # Silently degrade if RAG fails

        def _on_token(tok: str):
            self._append_chat(tok, "assistant")
            self._last_snippet += tok # Collect full response

        def _stream():
            ai.chat_stream(
                user_message=message,
                session_id=self._session_id,
                on_token=_on_token,
                rag_context=rag_context,
            )
            self._append_chat("\n\n", "assistant")
            # After stream, try to extract code block if present
            self._last_snippet = self._extract_code(self._last_snippet)

        threading.Thread(target=_stream, daemon=True).start()

    def _extract_code(self, text: str) -> str:
        """Extract content between ``` marks if present, otherwise return full text."""
        import re
        matches = re.findall(r"```(?:\w+)?\n(.*?)\n```", text, re.DOTALL)
        if matches:
            return matches[-1].strip() # Take the last code block
        return text.strip()

    def _append_chat(self, text: str, tag: str = "") -> None:
        """Thread-safe append to the chat display."""
        def _do():
            self._chat_display.config(state="normal")
            self._chat_display.insert("end", text, tag)
            self._chat_display.see("end")
            self._chat_display.config(state="disabled")
        self._chat_display.after(0, _do)

    # ------------------------------------------------------------------
    # Session management
    # ------------------------------------------------------------------

    def _load_session(self, session_id: str) -> None:
        """Load a previous session's history into the chat display."""
        self._session_id = session_id
        history = sh.load_history(session_id)
        self._chat_display.config(state="normal")
        self._chat_display.delete("1.0", "end")
        for msg in history:
            tag = "user" if msg["role"] == "user" else "assistant"
            prefix = "You" if msg["role"] == "user" else "Assistant"
            self._chat_display.insert("end", f"{prefix}: {msg['content']}\n\n", tag)
        self._chat_display.see("end")
        self._chat_display.config(state="disabled")
