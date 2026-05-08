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

---

## 🛠️ Tech Stack

| Component | Technology | Version |
|---|---|---|
| Language | Python | 3.11+ |
| GUI Framework | CustomTkinter | 5.2.2 |
| CLIPS Engine | CLIPSpy | ≥ 1.0.6 |
| Syntax Highlight | Pygments | ≥ 2.17 |
| AI Assistant | Ollama Python SDK | ≥ 0.4.0 |
| Image | Pillow | ≥ 10.0.0 |
| Testing | pytest + pytest-mock | ≥ 8.0.0 |

---

## 🚀 Version: v0.1.0

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
git clone <your-repo-url> CLIPSIDE
cd CLIPSIDE
bash scripts/setup_env.sh
```

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

---

## 📄 License

MIT © 2026 Marco Baturan
