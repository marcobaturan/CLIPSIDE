# Changelog — CLIPSIDE

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.1] - 2026-05-12

### Fixed
- **CLIPS download URL in setup script**: Fixed broken SourceForge URL — version directory was `6.41` instead of `6.4.1`, and zip suffix was `6_41` instead of `641`. The setup script now correctly resolves to `clips_core_source_641.zip`.

## [0.3.0] - 2026-05-11

### Added
- **Right-click delete in Explorer**: Context menu with "🗑 Delete" on files and folders in the file tree. Asks for confirmation before removing.
- **Context directory indicator**: REPL console now shows the active working directory `[carpeta]` next to the `CLIPS>` prompt.
- **RAG (Retrieval-Augmented Generation)**: AI Assistant can now retrieve relevant excerpts from the official CLIPS 6.4 documentation and inject them into the LLM prompt.
  - `src/core/rag.py` — new module: PDF extraction (PyMuPDF), chunking (500-char windows with 100-char overlap), embedding (sentence-transformers all-MiniLM-L6-v2), and vector retrieval (ChromaDB persistent index).
  - 4 official CLIPS 6.4 manuals indexed: Basic Programming Guide (432 pp.), Advanced Programming Guide (225 pp.), User's Guide (156 pp.), Installation Guide (104 pp.) → 4 424 chunks total.
  - Embedding model ~80 MB, runs on CPU, ~11 s initial load, ~40-80 ms per query.
  - Index built once and persisted to disk (`src/assets/clips_docs/.rag_index/`).
  - Toggle button 🔍 RAG in the AI panel header to enable/disable.
  - Retrieval threshold 0.28 similarity; top-3 chunks injected into the system prompt.
  - The model decides whether to use the context — no external classifier needed.

### Changed
- **REPL `chdir` before eval**: Console now calls `os.chdir()` to the active file's directory before each `(load ...)` command, fixing file resolution in subfolders.
- **Splash screen delay**: Extended from 400 ms → 3 seconds for screenshot capture.
- **Version bumped**: About dialog, splash screen, and README updated to v0.3.0.

### Fixed
- CLIPS `(load "...")` in REPL failing when the active editor tab was in a subfolder.

### Architecture & References

The RAG implementation follows established research on combining fine-tuning with retrieval augmentation for domain-specific code generation:

1. **RAG + Fine-tuning are complementary**, not competing — their combination consistently outperforms either alone, achieving higher accuracy ceilings than fine-tuning alone, with RAG providing better scalability as knowledge bases grow. *Tencent/WXG study on 160k+ industrial code files, arXiv:2505.15179 (May 2025)*.

2. **BM25 + dense embeddings (hybrid) achieve the best balance** of retrieval effectiveness and efficiency for code/documentation retrieval, with BM25 alone often matching or exceeding neural embedding models on technical documentation. *Same Tencent study; also confirmed by JetBrains' Long Code Arena benchmark.*

3. **Adaptive (implicit) routing** — using a similarity threshold to decide whether to inject context — matches the production recommendation of "use single-shot for easy questions, retrieval for hard ones", avoiding the 2-4× token/latency cost of always-on agentic RAG. *CallSphere agentic RAG cost analysis, 2026; LangGraph documentation on adaptive routing.*

4. **Sentence-transformers all-MiniLM-L6-v2** (80 MB, CPU, ~50 ms/query) is the recommended embedding model for local-first RAG systems, offering the best accuracy-to-latency ratio for single-user desktop applications. *Sentence-Transformers benchmark suite (SBERT.net).*

5. **Retrieval-augmented code generation on niche/domain-specific languages** (CLIPS qualifies) has been shown to substantially improve factual accuracy and reduce hallucination, especially for API usage, syntax details, and edge cases. *arXiv survey on RAG for code generation (2510.04905, Oct 2025).*

## [0.2.0] - 2026-05-09

### Added
- **Collapsible panels**: Left panel (Explorer/AI) and right panel (Inspector) can now be hidden/shown independently.
  - 📁 icon in the Editor header toggles the left panel.
  - 🔍 icon in the Editor header toggles the right panel.
  - `Ctrl+L` / `Ctrl+R` keyboard shortcuts for left/right panel toggle.
  - `Ctrl+M` toggles **all** panels at once for maximum editor space.
- **Half-screen support**: Minimum window size reduced to 680×520 px, letting the IDE sit comfortably on one side of a laptop screen while a browser or manual occupies the other.
- **Width memory**: Each panel remembers its last width when collapsed and restores it on re-open.

### Changed
- Panel `minsize` values lowered from 240→140 px (side panels) and 400→280 px (center editor) to allow more aggressive resizing.
- `_refresh_h_pane()` simplified for smoother dynamic layout recalculation.

## [0.1.0] - 2026-05-08

### Added
- **Persistent Project Root**: The IDE now remembers the last opened project directory across sessions (~/.clipside_config.json).
- **Build Buffer (Ctrl+B)**: New command to save the current editor content to a temporary file and load all constructs (rules, templates, facts) into the engine simultaneously.
- **Close File (Ctrl+W)**: Added a close button (✖) in the editor header and a keyboard shortcut to close the active tab.
- **Explorer Enhancements**: Implemented `update_root` to correctly refresh the file tree when opening a new folder.
- **Improved UI Column Layout**: Stabilized the 3-column architecture (Explorer/AI, Editor/Console, Inspector).
- **Inspector Refresh**: Centralized UI refresh logic for Facts, Agenda, and Instances.
- **Streaming AI Chat**: Local Ollama assistant with word-by-word streaming and code snippet insertion.
- **CLIPS Engine Integration**: Thread-safe wrapper for `clipspy` supporting reset, run, step, and eval.

### Changed
- **Menu Structure**: Unified "Build" and "Run" commands in the File and Environment menus.
- **Internal Engine Logic**: Switched from `agenda()` to `activations()` for better compatibility with modern `clipspy`.

### Fixed
- Fixed AttributeError when accessing agenda in CLIPS environment.
- Resolved issues with File Explorer not updating after project folder change.
- Suppressed non-fatal Tkinter lifecycle warnings.

---
*Created by Antigravity AI for Marco Baturan*
