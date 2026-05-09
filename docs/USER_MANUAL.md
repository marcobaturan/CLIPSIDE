# CLIPSIDE — User Manual (v0.2.0)

## Starting the IDE

```bash
cd /home/marco/PycharmProjects/CLIPSIDE
./start.sh
```

A splash screen appears while modules load, then the main window opens.

---

## Interface Overview

```
┌──────────┬─────────────────────────────┬─────────────────────┐
│ Explorer │    Editor (tabs)            │  Facts | Agenda | … │
│          │                             │                     │
│          │                             │  AI Assistant Chat  │
│ 🤖 AI    │                             │                     │
├──────────┴─────────────────────────────┴─────────────────────┤
│                    CLIPS Console (REPL)                      │
└──────────────────────────────────────────────────────────────┘
```

| Panel | Description |
|---|---|
| **Explorer** | Browse your filesystem; double-click a `.clp` file to open it. |
| **AI Assistant** | Chat with the local model; generate code snippets. |
| **Editor** | Multi-tab editor with syntax highlighting and close buttons (✖). |
| **Inspector** | Live tabs for Facts, Agenda, and Instances. |
| **Console** | Interactive CLIPS REPL. |

---

## Collapsible Panels (v0.2.0)

You can hide/show the side panels to give more room to the editor and console:

| Method | Action |
|---|---|
| Click **📁** in the Editor header | Toggle **left** panel (Explorer + AI) |
| Click **🔍** in the Editor header | Toggle **right** panel (Inspector) |
| `Ctrl+L` | Keyboard shortcut for left panel |
| `Ctrl+R` | Keyboard shortcut for right panel |
| `Ctrl+M` | Toggle **all** panels — gives the editor full window width |

Each panel **remembers its width** when you collapse it. Drag the splitters between columns to resize freely.

> 💡 The window can shrink as small as **680×520 px** — ideal for placing the IDE on one half of a laptop screen with a browser or documentation on the other.

---

## Working with Files

- **New File**: `Ctrl+N`
- **Open File**: `Ctrl+O`
- **Save File**: `Ctrl+S`
- **Close Tab**: `Ctrl+W` or click the **✖** button in the editor header.
- **Persistent Folder**: The IDE automatically opens the last folder you worked in.

---

## Running CLIPS Code

### Build Buffer (🔨)
Use **Ctrl+B** or the 🔨 icon. This saves the current editor content to a temporary file and loads all constructs (rules, templates, etc.) into the CLIPS environment.

### Control the Engine
| Action | Keyboard |
|---|---|
| **Reset Environment** | `F5` |
| **Run (Inference)** | `F6` |
| **Step (One rule)** | `F7` |

---

## AI Assistant

- **Chat**: Type in the box and press `Ctrl+Enter`.
- **Insert**: Click **Insert ↗** to paste the last code block from the AI directly into your editor.
- **Streaming**: The AI responds in real-time.

---

## Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl+N` | New file tab |
| `Ctrl+O` | Open file |
| `Ctrl+S` | Save current file |
| `Ctrl+W` | Close current tab |
| `Ctrl+B` | Build Buffer (Load constructs) |
| `Ctrl+L` | Toggle **left** panel (Explorer/AI) |
| `Ctrl+R` | Toggle **right** panel (Inspector) |
| `Ctrl+M` | Toggle **all** panels (maximise editor) |
| `F5` | Reset engine |
| `F6` | Run engine |
| `F7` | Step engine |
| `Ctrl+Return` | Send AI message |

---

## Troubleshooting

- **Ollama Status**: If it shows "not running", ensure the Ollama service is active on your system.
- **Refresh Explorer**: Click the ⟳ icon in the explorer header if the filesystem changes externally.
