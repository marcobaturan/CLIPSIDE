# CLIPSIDE — Modern CLIPS IDE for Python/Linux

<p align="center">
  <img src="src/assets/icon.png" width="120" alt="CLIPSIDE Snake Icon"/>
  <br/>
  <strong>A modern, AI-assisted IDE for the CLIPS rule-based expert system language — built in Python for Linux.</strong>
</p>

---

## 📖 About CLIPSIDE

**CLIPSIDE** is a modern, high-performance integrated development environment (IDE) specifically designed for the **CLIPS** (C Language Integrated Production System) rule-based expert system language. 

Developed by **Marco Baturan**, this project aims to provide a professional, AI-augmented workflow for knowledge engineers and developers working on expert systems. It is completely **open-source**, **free**, and built with a focus on cross-platform compatibility and modern UX.

- **GitHub Repository**: [https://github.com/marcobaturan/CLIPSIDE](https://github.com/marcobaturan/CLIPSIDE)
- **Post**: [https://getdevworks.hashnode.dev/building-a-modern-clips-ide-in-python-ai-assisted-expert-system-development-on-linux]
- **License**: MIT (Open Source & Free)
- **Author**: Marco Baturan

---


CLIPSIDE replicates (and surpasses) the classic Windows/Mac CLIPS IDE, offering:
- 🖤 Native dark-mode GUI via **CustomTkinter**
- 🐍 Python-first architecture with **CLIPSpy** bindings
- 🤖 Local AI assistant powered by **Ollama** (`marcobaturan/clips-architect-final`)
- 📋 Live **Fact**, **Agenda** and **Instance** inspection panels
- 🔁 Interactive **CLIPS REPL** console
- 🌲 File explorer, multi-tab editor, full menu bar
- 💾 Persistence of project workspace and last folder
- 📐 **Collapsible panels** — hide/show Explorer and Inspector to maximise editor space
- ↔️ **Half-screen friendly** — window shrinks down to 680px for side-by-side workflow

---

## 🛠️ Tech Stack

| Component | Technology | Version |
|---|---|---|
| Language | Python | 3.10+ |
| GUI Framework | CustomTkinter | 5.2.2 |
| CLIPS Engine | CLIPSpy | ≥ 1.0.6 |
| Syntax Highlight | Pygments | ≥ 2.17 |
| AI Assistant | Ollama Python SDK | ≥ 0.4.0 |
| Image | Pillow | ≥ 10.0.0 |
| Testing | pytest + pytest-mock | ≥ 8.0.0 |

---

## 🚀 Version: v0.3.2

See [CHANGELOG.md](CHANGELOG.md) for full release details.

---

## 📁 Project Structure

```
CLIPSIDE/
├── src/
│   ├── main.py                 # Entry point + splash screen
│   ├── core/
│   │   ├── clips_engine.py     # CLIPSpy wrapper (thread-safe)
│   │   ├── ollama_client.py    # Ollama streaming chat + snippet gen
│   │   ├── file_manager.py     # Open / save .clp files
│   │   ├── session_history.py  # Cross-session AI context persistence
│   │   └── config_manager.py   # IDE settings and folder persistence
│   ├── ui/
│   │   ├── main_window.py      # Root window + layout
│   │   ├── editor_panel.py     # Multi-tab editor + line numbers
│   │   ├── syntax_highlighter.py # Pygments CLIPS lexer
│   │   ├── console_panel.py    # REPL console
│   │   ├── facts_panel.py      # Live facts inspector
│   │   ├── agenda_panel.py     # Live agenda + instances
│   │   ├── ai_panel.py         # AI chat + snippet panel
│   │   ├── file_explorer.py    # File tree (left)
│   │   ├── menu_bar.py         # Full application menu
│   │   └── splash_screen.py    # Animated splash
│   └── assets/
│       ├── icon.png            # Pixel-art cobra snake icon
│       └── clipside.desktop    # Linux desktop entry
├── scripts/
│   └── setup_env.sh            # Automated installer
├── docs/
│   └── USER_MANUAL.md          # End-user guide
├── tests/                      # Full TDD test suite
├── requirements.txt
├── CHANGELOG.md                # Version history
└── start.sh
```

---

## 🚀 Automated Installation

```bash
gh repo clone marcobaturan/CLIPSIDE
cd CLIPSIDE
bash scripts/setup_env.sh
```

---

## 🖥️ Desktop Integration

To add CLIPSIDE to your Applications menu (Development section) and your Desktop, run the following script:

```bash
bash scripts/install_launcher.sh
```

This will create a `CLIPSIDE` entry in your system's application launcher and a shortcut on your Desktop for easy access.


---

## 🧪 Test Battery

```bash
source .venv/bin/activate
python -m pytest tests/ -v --tb=short
```

---

## 🤖 AI Model

- **Model:** `marcobaturan/clips-architect-final`
- **Fine-tuned on:** Official CLIPS 6.4 manuals
- **System prompt:** Injected automatically with CLIPS syntax rules.

---

## 🔍 RAG — Retrieval-Augmented Generation (v0.3.1)

The AI Assistant can augment its responses with relevant excerpts from the **official CLIPS 6.4 documentation** (Basic Programming Guide, Advanced Programming Guide, User's Guide, Installation Guide — 917 pages total).

- **🔍 RAG button** toggles the feature on/off (blue = on, grey = off).
- On first launch, 4 PDFs are indexed into a local ChromaDB vector store (embedding: all-MiniLM-L6-v2, ~80 MB on CPU).
- Your question is used to retrieve the **top-3 most relevant chunks** (500-char windows, hybrid BM25 + dense retrieval) which are injected into the LLM's system prompt.
- The model decides whether the context is relevant — if not, it ignores it.
- RAG is particularly effective for syntax questions, edge cases, and API details. Disable for creative/open-ended tasks.

> 📖 When context is found, a `📖 +docs` indicator appears in the chat.

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl+N` | New file tab |
| `Ctrl+O` | Open file |
| `Ctrl+S` | Save |
| `Ctrl+W` | Close File |
| `Ctrl+B` | Build Buffer (Load into engine) |
| `F5` | Reset environment |
| `F6` | Run inference engine |
| `F7` | Step (one rule) |
| `Ctrl+Return` | Send AI chat message |
| Right-click on file | Delete from Explorer |

## 📐 Panel Collapse

Collapse the side panels with a single click to give the editor maximum space:

| Icon | Location | Action |
|---|---|---|
| 📁 | Editor header (leftmost) | Toggle **Explorer** / **AI Assistant** panel |
| 🔍 | Editor header (right side) | Toggle **Inspector** panel |
| `Ctrl+L` | Keyboard | Toggle left panel |
| `Ctrl+R` | Keyboard | Toggle right panel |
| `Ctrl+M` | Keyboard | Toggle **all** panels (maximise editor) |

> 💡 The IDE remembers each panel's width when collapsed. Drag the splitters to resize freely. Minimum window size is 680px — perfect for half a laptop screen. The REPL now shows the active directory `[carpeta]` context next to the prompt.

---

## 🖥️ Compatibility

### Tested and supported

| OS | Python | Status |
|---|---|---|
| Debian 12 | 3.11 | ✅ Confirmed working |
| CentOS Stream 9 | 3.11+ | ✅ Requires: `sudo dnf install unifont gnu-free-fonts-common` |
| Ubuntu 22.04 | 3.10+ | ✅ Requires: `sudo apt-get install python3-tk fonts-unifont` |
| Linux Mint 21+ | 3.10+ | ✅ Requires: `sudo apt-get install fonts-unifont fonts-symbola` |

### Not supported

| OS | Python | Reason |
|---|---|---|
| Linux Mint 20.3 | 3.8 | Python 3.8 is below the minimum requirement (3.10) |
| Ubuntu 20.04 | 3.8 | Python 3.8 is below the minimum requirement (3.10) |

### Python version matrix (Debian 12 — pyenv multi-version verified)

A complete Python version test matrix has been executed on the reference platform. Using `pyenv` and three independent virtual environments, CLIPSIDE was compiled and verified:
* **Python 3.10.20** (`.venv10`): All tests passing (54/54) ✅
* **Python 3.12.13** (`.venv12`): All tests passing (54/54), Editor launches successfully ✅
* **Python 3.13.13** (`.venv13`): All tests passing (54/54) ✅

---

## 🖥️ Testing Hardware Profile

The following system specs were used for compiling, testing, and validating CLIPSIDE v0.3.2 across the entire Python version matrix:
* **CPU**: AMD Ryzen 7 4700U with Radeon Graphics (8 cores / 8 threads)
* **RAM**: 14 GiB RAM
* **OS**: Debian GNU/Linux 12 (bookworm)
* **Windowing System**: X11 (Display `:0.0`)

---

## ⚠️ Known Issues

| Issue | Affected distros | Fix |
|---|---|---|
| **X11 BadLength / RenderAddGlyphs** crash on launch | CentOS Stream 9, Fedora, RHEL | `sudo dnf install unifont gnu-free-fonts-common` |
| **Segmentation fault** on launch | Ubuntu 22.04 | `sudo apt-get install python3-tk python3-dev libxcb1 libxcb-render0` |
| **`clips.h: No such file or directory`** during build | All distros (pre-fix) | Fixed in v0.3.2 — update `setup_env.sh` |
| Python 3.8 not supported | Linux Mint 20.3, Ubuntu 20.04 | Upgrade to Python 3.10+ or use a newer OS release |

> The X11 BadLength / RenderAddGlyphs error is a Tkinter/X11 font rendering issue,
> not a CLIPSIDE bug. Installing Unicode font packages resolves it.

---

## 📄 License

MIT © 2026 Marco Baturan
