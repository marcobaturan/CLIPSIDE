# CLIPSIDE — User Manual (v0.3.0)

## Starting the IDE

```bash
cd /home/marco/PycharmProjects/CLIPSIDE
./start.sh
```

A splash screen appears while modules load, then the main window opens.

> **First run may be slow** (~2 minutes) while the RAG index is built from the CLIPS 6.4 documentation PDFs. Subsequent launches are instant.

---

## Interface Overview

```
┌──────────┬─────────────────────────────┬─────────────────────┐
│ Explorer │    Editor (tabs)            │  Facts | Agenda | … │
│          │                             │                     │
│          │                             │  AI Assistant Chat  │
│ 🤖 AI    │                             │     [🔍 RAG]        │
├──────────┴─────────────────────────────┴─────────────────────┤
│                    CLIPS Console (REPL)                      │
└──────────────────────────────────────────────────────────────┘
```

| Panel | Description |
|---|---|
| **Explorer** | Browse your filesystem; double-click a `.clp` file to open it. Right-click → "🗑 Delete" to remove files/folders. |
| **AI Assistant** | Chat with the local model; optional RAG augmentation over CLIPS documentation. |
| **Editor** | Multi-tab editor with syntax highlighting and close buttons (✖). |
| **Inspector** | Live tabs for Facts, Agenda, and Instances. |
| **Console** | Interactive CLIPS REPL with context directory indicator `[carpeta]`. |

---

## Collapsible Panels

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

### RAG Mode (🔍 RAG)

The AI Assistant can optionally augment its responses with relevant excerpts from the official CLIPS 6.4 documentation (Basic Programming Guide, Advanced Programming Guide, User's Guide, Installation Guide).

- **Toggle**: Click the **🔍 RAG** button in the chat input row.
  - **Blue** = enabled (default).
  - **Grey** = disabled (the model answers from its training only).
- **Indicator**: When RAG context is found for your question, a `📖 +docs` line appears in the chat.
- **First use**: On first launch, the IDE indexes all 4 PDFs (~4400 chunks). This takes 1-2 minutes and happens in the background.
- **How it works**: Your question is used to retrieve the 3 most relevant documentation excerpts. These are injected into the system prompt. The model decides whether to use them — if the excerpts are irrelevant, it ignores them.
- **When to disable RAG**: For creative or open-ended questions (e.g., "design an expert system for X"), the documentation context may not help and can constrain the model. Disable RAG for maximum creativity.

### Working Directory Context

When you open a file from the Explorer or switch tabs, the REPL console shows the active directory in brackets: `[subfolder]` next to the `CLIPS>` prompt. All `(load "...")` commands resolve relative to that directory.

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
