# CLIPSIDE — Modern CLIPS IDE for Python/Linux

<p align="center">
  <img src="../src/assets/icon.png" width="120" alt="CLIPSIDE Snake Icon"/>
  <br/>
  <strong>A modern, AI-assisted IDE for the CLIPS rule-based expert system language — built in Python for Linux.</strong>
</p>

---

## 🎯 Project Vision

CLIPSIDE replicates (and surpasses) the classic Windows/Mac CLIPS IDE, offering:
- 🖤 Native dark-mode GUI via **CustomTkinter**
- 🐍 Python-first architecture with **CLIPSpy** bindings
- 🤖 Local AI assistant powered by **Ollama** (`marcobaturan/clips-architect-final`)
- 📋 Live **Fact**, **Agenda** and **Instance** inspection panels
- 🔁 Interactive **CLIPS REPL** console
- 🌲 File explorer, multi-tab editor, full menu bar

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

## 📁 Project Structure

```
CLIPSIDE/
├── src/
│   ├── main.py                 # Entry point + splash screen
│   ├── core/
│   │   ├── clips_engine.py     # CLIPSpy wrapper (thread-safe)
│   │   ├── ollama_client.py    # Ollama streaming chat + snippet gen
│   │   ├── file_manager.py     # Open / save .clp files
│   │   └── session_history.py  # Cross-session AI context persistence
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
│   ├── README.md               # This file
│   └── USER_MANUAL.md          # End-user guide
├── tests/                      # Full TDD test suite
├── requirements.txt
└── start.sh
```

---

## 🚀 Automated Installation

```bash
git clone <your-repo-url> CLIPSIDE
cd CLIPSIDE
bash scripts/setup_env.sh
```

This script will:
1. Check for `gcc`, `make`, `curl`, `unzip`, `python3`
2. Build and install `libclips.so` from CLIPS 6.41 source
3. Create/activate `.venv` and install Python deps
4. Pull the Ollama AI model (`4.7 GB`)
5. Install the `.desktop` launcher to `~/.local/share/applications/`

### System prerequisites (Debian 12)

```bash
sudo apt-get install -y build-essential curl unzip python3-pip
# Ollama: https://ollama.com/download
curl -fsSL https://ollama.com/install.sh | sh
```

---

## 🔧 Manual Installation

```bash
# 1. Clone and enter
cd /home/marco/PycharmProjects/CLIPSIDE

# 2. Activate venv
python3 -m venv .venv && source .venv/bin/activate

# 3. Install Python deps
pip install -r requirements.txt

# 4. Build libclips.so (requires gcc/make)
curl -L -o /tmp/clips.zip "https://sourceforge.net/projects/clipsrules/files/CLIPS/6.41/clips_core_source_6_41.zip/download"
unzip /tmp/clips.zip -d /tmp/clips_src
cd /tmp/clips_src/clips_core_source_641/
gcc -std=c99 -O2 -fPIC -shared -o /tmp/libclips.so *.c -lm
sudo cp /tmp/libclips.so /usr/local/lib/ && sudo ldconfig

# 5. Pull Ollama model
ollama pull marcobaturan/clips-architect-final

# 6. Run
cd /home/marco/PycharmProjects/CLIPSIDE && ./start.sh
```

---

## 🧪 Test Battery

### Running tests

```bash
source .venv/bin/activate
python -m pytest tests/ -v --tb=short
```

> Note: `test_clips_engine.py` requires `clipspy` and `libclips.so` to be installed.

### Test results log

| Date | Suite | Passed | Failed | Skipped |
|---|---|---|---|---|
| 2026-05-08 | session_history, file_manager, syntax_highlighter, ollama_client | 41 | 0 | 0 |

---

## 🤖 AI Model

- **Model:** `marcobaturan/clips-architect-final`
- **Source:** [ollama.com/marcobaturan/clips-architect-final](https://ollama.com/marcobaturan/clips-architect-final)
- **Size:** 4.7 GB · 32K context window
- **Fine-tuned on:** Official CLIPS 6.4 manuals by Gary Riley
- **System prompt:** Injected automatically with CLIPS syntax rules to prevent hallucination

Session history is stored in `~/.clipside/sessions/` as JSON files, enabling context to persist across IDE restarts and model switches.

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl+N` | New file tab |
| `Ctrl+O` | Open file |
| `Ctrl+S` | Save |
| `Ctrl+Shift+S` | Save as |
| `F5` | Reset environment |
| `F6` | Run inference engine |
| `F7` | Step (one rule) |
| `Ctrl+Enter` | Send AI chat message |

---

## 🖥️ Desktop Launcher

After running `setup_env.sh`, CLIPSIDE appears in your application menu.
Manual installation:
```bash
cp src/assets/clipside.desktop ~/.local/share/applications/
# Edit the file to update PROJECT_DIR to your install path
```

---

## 📚 References

- [CLIPS Rules](https://www.clipsrules.net/) — Gary Riley
- [CLIPSpy Documentation](https://clipspy.readthedocs.io/en/latest/)
- [CustomTkinter](https://customtkinter.tomschimansky.com/)
- [Ollama](https://ollama.com/)
- [Fine-tuning article](https://getdevworks.hashnode.dev/from-generalist-to-specialist-taming-a-local-llm-for-niche-languages)

---

## 📄 License

MIT © 2026 Marco Baturan
