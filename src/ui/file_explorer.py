"""File explorer — left-panel tree view of the project filesystem."""

import os
import customtkinter as ctk
import tkinter as tk
from pathlib import Path
from typing import Callable, Optional


class FileExplorer(ctk.CTkFrame):
    """
    Minimal file tree explorer rooted at a given directory.
    Double-clicking a .clp file fires the on_open_file callback.
    """

    def __init__(
        self,
        parent,
        root_dir: str,
        on_open_file: Callable[[str], None],
        on_folder_double_click: Optional[Callable[[str], None]] = None,
        show_header: bool = True,
        folders_only: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(parent, fg_color="#0D1117", **kwargs)
        self._root_dir = root_dir
        self._on_open_file = on_open_file
        self._on_folder_double_click = on_folder_double_click
        self._show_header = show_header
        self._folders_only = folders_only
        self._build()
        self.refresh()

    def _build(self) -> None:
        if self._show_header:
            header = ctk.CTkFrame(self, fg_color="#161B22", height=28)
            header.pack(fill="x")
            ctk.CTkLabel(
                header, text="  📁 Explorer",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="#FFCB6B",
            ).pack(side="left", padx=4)
            ctk.CTkButton(
                header, text="⟳", width=28, height=22,
                fg_color="#1F2937", hover_color="#374151",
                command=self.refresh,
            ).pack(side="right", padx=4, pady=3)

        self._tree = tk.Listbox(
            self, bg="#0D1117", fg="#EEFFFF",
            selectbackground="#1F6FEB",
            font=("Courier New", 10),
            relief="flat", borderwidth=0,
        )
        scrollbar = ctk.CTkScrollbar(self, command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)
        self._tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._tree.bind("<Double-Button-1>", self._on_double_click)

        self._path_map: dict[int, str] = {}

    def update_root(self, new_root: str) -> None:
        """Update the root directory and refresh the view."""
        self._root_dir = new_root
        self.refresh()

    def refresh(self) -> None:
        """Rebuild the file list from the root directory."""
        self._tree.delete(0, "end")
        self._path_map.clear()
        self._populate(self._root_dir, prefix="")

    def _populate(self, directory: str, prefix: str) -> None:
        """Recursively add entries to the listbox."""
        try:
            entries = sorted(
                os.scandir(directory),
                key=lambda e: (not e.is_dir(), e.name.lower()),
            )
        except PermissionError:
            return
        _IGNORED = {".git", ".venv", "__pycache__", ".pytest_cache", ".idea"}
        for entry in entries:
            if entry.name.startswith(".") and entry.name not in {".clp"}:
                if entry.name in _IGNORED or entry.is_dir():
                    continue
            if entry.name in _IGNORED:
                continue
                
            if entry.is_dir():
                idx = self._tree.size()
                self._tree.insert("end", f"{prefix}📂 {entry.name}/")
                self._tree.itemconfig(idx, foreground="#FFCB6B")
                self._path_map[idx] = entry.path
                self._populate(entry.path, prefix + "  ")
            elif not self._folders_only and entry.name.endswith(".clp"):
                idx = self._tree.size()
                self._tree.insert("end", f"{prefix}📄 {entry.name}")
                self._tree.itemconfig(idx, foreground="#C3E88D")
                self._path_map[idx] = entry.path

    def get_selected_path(self) -> Optional[str]:
        """Return the absolute path of the currently selected item."""
        selection = self._tree.curselection()
        if not selection:
            return None
        return self._path_map.get(selection[0])

    def _on_double_click(self, _event) -> None:
        selection = self._tree.curselection()
        if not selection:
            return
        idx = selection[0]
        path = self._path_map.get(idx, "")
        if not path:
            return

        if os.path.isdir(path):
            if self._on_folder_double_click:
                self._on_folder_double_click(path)
        elif path.endswith(".clp"):
            self._on_open_file(path)
