"""File manager — handles new/open/save/.clp operations via tkinter dialogs."""

import os
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import Optional

# Default starting directory for file dialogs
DEFAULT_DIR = str(Path.home() / "Documents" / "CLIPS")
CLP_FILETYPES = [("CLIPS Files", "*.clp"), ("All Files", "*.*")]


def ensure_default_dir() -> None:
    """Create the default CLIPS documents directory if it doesn't exist."""
    os.makedirs(DEFAULT_DIR, exist_ok=True)


def open_file() -> Optional[tuple[str, str]]:
    """
    Open a file dialog and return (path, content) or None if cancelled.
    """
    path = filedialog.askopenfilename(
        title="Open CLIPS File",
        initialdir=DEFAULT_DIR,
        filetypes=CLP_FILETYPES,
    )
    if not path:
        return None
    return path, read_file(path)


def open_directory() -> Optional[str]:
    """
    Open a directory dialog and return the selected path or None.
    """
    path = filedialog.askdirectory(
        title="Open Project Folder",
        initialdir=DEFAULT_DIR,
    )
    return path if path else None


def read_file(path: str) -> str:
    """Read and return the content of a file."""
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def save_file(path: str, content: str) -> bool:
    """Save content to an existing path. Returns True on success."""
    try:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        return True
    except OSError as exc:
        messagebox.showerror("Save Error", str(exc))
        return False


def save_file_as(content: str) -> Optional[str]:
    """
    Open a save-as dialog and write content. Returns the saved path or None.
    """
    path = filedialog.asksaveasfilename(
        title="Save CLIPS File",
        initialdir=DEFAULT_DIR,
        defaultextension=".clp",
        filetypes=CLP_FILETYPES,
    )
    if not path:
        return None
    save_file(path, content)
    return path


def new_file_content() -> str:
    """Return default content for a blank new file."""
    return "; New CLIPS file\n; Author: \n; Date: \n\n"


def confirm_discard(parent=None) -> bool:
    """Ask the user to confirm discarding unsaved changes. Returns True if confirmed."""
    return messagebox.askyesno(
        "Unsaved Changes",
        "You have unsaved changes. Discard them?",
        parent=parent,
    )


def delete_path(path: str, parent=None) -> bool:
    """Delete a file or directory. Returns True on success."""
    try:
        if os.path.isdir(path):
            import shutil
            shutil.rmtree(path)
        else:
            os.remove(path)
        return True
    except Exception as exc:
        messagebox.showerror("Delete Error", str(exc), parent=parent)
        return False
