"""Menu bar — full application menu for CLIPSIDE."""

import webbrowser
import customtkinter as ctk
import tkinter as tk
from typing import Callable

CLIPS_DOCS_URL = "https://www.clipsrules.net/"


class MenuBar(tk.Menu):
    """
    Full application menu bar.
    Callbacks are injected from MainWindow to keep this module stateless.
    """

    def __init__(
        self,
        parent,
        callbacks: dict[str, Callable],
    ) -> None:
        super().__init__(parent, bg="#161B22", fg="#EEFFFF",
                         activebackground="#1F6FEB", activeforeground="#FFFFFF",
                         relief="flat", bd=0)
        self._cb = callbacks
        self._build()

    def _build(self) -> None:
        self._add_file_menu()
        self._add_edit_menu()
        self._add_environment_menu()
        self._add_debug_menu()
        self._add_tools_menu()
        self._add_help_menu()

    def _menu(self, label: str) -> tk.Menu:
        """Create and add a top-level menu cascade."""
        m = tk.Menu(self, tearoff=False,
                    bg="#161B22", fg="#EEFFFF",
                    activebackground="#1F6FEB", activeforeground="#FFFFFF")
        self.add_cascade(label=label, menu=m)
        return m

    def _add_file_menu(self) -> None:
        m = self._menu("File")
        m.add_command(label="New File",    accelerator="Ctrl+N", command=self._cb.get("new"))
        m.add_command(label="New Folder",  accelerator="Ctrl+Shift+N", command=self._cb.get("new_folder"))
        m.add_separator()
        m.add_command(label="Open File…", accelerator="Ctrl+O", command=self._cb.get("open"))
        m.add_command(label="Open Folder…", command=self._cb.get("open_folder"))
        m.add_separator()
        m.add_command(label="Save",       accelerator="Ctrl+S", command=self._cb.get("save"))
        m.add_command(label="Save As…",   accelerator="Ctrl+Shift+S", command=self._cb.get("save_as"))
        m.add_command(label="Close File", accelerator="Ctrl+W", command=self._cb.get("close"))
        m.add_separator()

        m.add_command(label="Exit",       accelerator="Alt+F4", command=self._cb.get("exit"))

    def _add_edit_menu(self) -> None:
        m = self._menu("Edit")
        m.add_command(label="Undo",       accelerator="Ctrl+Z", command=self._cb.get("undo"))
        m.add_command(label="Redo",       accelerator="Ctrl+Y", command=self._cb.get("redo"))
        m.add_separator()
        m.add_command(label="Cut",        accelerator="Ctrl+X", command=self._cb.get("cut"))
        m.add_command(label="Copy",       accelerator="Ctrl+C", command=self._cb.get("copy"))
        m.add_command(label="Paste",      accelerator="Ctrl+V", command=self._cb.get("paste"))

    def _add_environment_menu(self) -> None:
        m = self._menu("Environment")
        m.add_command(label="Build Buffer", accelerator="Ctrl+B", command=self._cb.get("build"))
        m.add_separator()
        m.add_command(label="Reset",     accelerator="F5",  command=self._cb.get("reset"))
        m.add_command(label="Run",       accelerator="F6",  command=self._cb.get("run"))
        m.add_command(label="Step",      accelerator="F7",  command=self._cb.get("step"))
        m.add_separator()
        m.add_command(label="Clear All",                    command=self._cb.get("clear"))
        m.add_separator()
        m.add_command(label="Clear",     command=self._cb.get("clear"))

    def _add_debug_menu(self) -> None:
        m = self._menu("Debug")
        m.add_command(label="Facts Window",    command=self._cb.get("show_facts"))
        m.add_command(label="Agenda Window",   command=self._cb.get("show_agenda"))
        m.add_command(label="Instances Window",command=self._cb.get("show_instances"))

    def _add_tools_menu(self) -> None:
        m = self._menu("Tools")
        m.add_command(label="Pull AI Model",       command=self._cb.get("pull_model"))
        m.add_command(label="AI Session History",  command=self._cb.get("session_history"))


    def _add_help_menu(self) -> None:
        m = self._menu("Help")
        m.add_command(label="User Manual",          command=self._cb.get("manual"))
        m.add_command(label="About CLIPSIDE",       command=self._cb.get("about"))
        m.add_separator()
        m.add_command(
            label="CLIPS Rules Documentation ↗",
            command=lambda: webbrowser.open(CLIPS_DOCS_URL),
        )
