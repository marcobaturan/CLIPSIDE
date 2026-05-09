"""Editor panel — multi-tab code editor with line numbers and syntax highlighting."""

import customtkinter as ctk
import tkinter as tk
from typing import Callable, Optional

from src.ui.syntax_highlighter import apply_highlighting
from src.core import file_manager as fm

# Debounce delay in ms before re-highlighting after typing
HIGHLIGHT_DEBOUNCE_MS = 300


class EditorTab:
    """Represents a single open file tab."""

    def __init__(
        self,
        notebook: ctk.CTkTabview,
        title: str,
        content: str = "",
        path: Optional[str] = None,
    ) -> None:
        self.path = path
        self.dirty = False
        self._title = title
        self._notebook = notebook
        self._highlight_job: Optional[str] = None

        # Add tab
        self._tab = notebook.add(title)
        self._build_editor(content)

    def _build_editor(self, content: str) -> None:
        """Build the text editor with a line-number gutter."""
        frame = ctk.CTkFrame(self._tab, fg_color="transparent")
        frame.pack(fill="both", expand=True)

        # Line numbers (Canvas)
        self._line_canvas = tk.Canvas(
            frame, width=40, bg="#0D1117", highlightthickness=0
        )
        self._line_canvas.pack(side="left", fill="y")

        # Scrollbar
        scrollbar = ctk.CTkScrollbar(frame, orientation="vertical")
        scrollbar.pack(side="right", fill="y")

        # Main text widget
        self._text = tk.Text(
            frame,
            bg="#0D1117", fg="#EEFFFF",
            insertbackground="#00FF88",
            selectbackground="#264F78",
            font=("Courier New", 12),
            yscrollcommand=scrollbar.set,
            wrap="none",
            undo=True,
            relief="flat",
            padx=6, pady=4,
        )
        self._text.pack(side="left", fill="both", expand=True)
        self._text.config(state="normal")
        scrollbar.configure(command=self._text.yview)


        # Bind events
        self._text.bind("<KeyRelease>", self._on_key_release)
        self._text.bind("<MouseWheel>", self._on_scroll)
        self._text.bind("<Button-4>", self._on_scroll)
        self._text.bind("<Button-5>", self._on_scroll)

        if content:
            self._text.insert("1.0", content)
            self._schedule_highlight()
            self._update_line_numbers()

    def _on_key_release(self, event=None) -> None:
        """Mark dirty and schedule a highlight refresh."""
        self.dirty = True
        self._schedule_highlight()
        self._update_line_numbers()

    def _on_scroll(self, event=None) -> None:
        """Sync line numbers on scroll."""
        self._update_line_numbers()

    def _schedule_highlight(self) -> None:
        """Debounce syntax highlighting to avoid re-running on every keystroke."""
        if self._highlight_job:
            self._text.after_cancel(self._highlight_job)
        self._highlight_job = self._text.after(
            HIGHLIGHT_DEBOUNCE_MS, self._run_highlight
        )

    def _run_highlight(self) -> None:
        """Apply syntax highlighting to the current content."""
        code = self.get_content()
        apply_highlighting(self._text, code)

    def _update_line_numbers(self) -> None:
        """Redraw line numbers in the gutter canvas."""
        self._line_canvas.delete("all")
        first_line = int(self._text.index("@0,0").split(".")[0])
        last_line = int(self._text.index(f"@0,{self._text.winfo_height()}").split(".")[0])
        for line_no in range(first_line, last_line + 1):
            y = self._text.dlineinfo(f"{line_no}.0")
            if y is None:
                continue
            self._line_canvas.create_text(
                36, y[1] + y[3] // 2,
                text=str(line_no),
                fill="#546E7A",
                font=("Courier New", 10),
                anchor="e",
            )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_content(self) -> str:
        """Return the full text content of this tab."""
        return self._text.get("1.0", "end-1c")

    def set_content(self, content: str) -> None:
        """Replace the editor content."""
        self._text.delete("1.0", "end")
        self._text.insert("1.0", content)
        self._schedule_highlight()
        self._update_line_numbers()
        self.dirty = False

    def insert_at_cursor(self, text: str) -> None:
        """Insert text at the current cursor position."""
        self._text.insert("insert", text)
        self._schedule_highlight()

    def destroy(self) -> None:
        """Cleanup pending jobs."""
        if self._highlight_job:
            self._text.after_cancel(self._highlight_job)
            self._highlight_job = None



class EditorPanel(ctk.CTkFrame):
    """Multi-tab editor panel hosting multiple EditorTab instances."""

    def __init__(self, parent, on_tab_change: Optional[Callable[[Optional[str]], None]] = None, **kwargs) -> None:
        super().__init__(parent, fg_color="#0D1117", **kwargs)
        self._tabs: dict[str, EditorTab] = {}
        self._counter = 0
        self._on_tab_change = on_tab_change
        self._build()

    def _build(self) -> None:
        self._notebook = ctk.CTkTabview(
            self, fg_color="#0D1117",
            segmented_button_fg_color="#161B22",
            segmented_button_selected_color="#1F6FEB",
            segmented_button_unselected_color="#161B22",
            command=self._handle_tab_change,
        )
        self._notebook.pack(fill="both", expand=True)

    def _handle_tab_change(self) -> None:
        if self._on_tab_change:
            tab = self.get_active_tab()
            if tab:
                tab._text.focus_set()
                self._on_tab_change(tab.path)
            else:
                self._on_tab_change(None)


    def new_tab(self, title: str = "Untitled", content: str = "", path: Optional[str] = None) -> str:
        """Open a new tab and return its key. If it exists, switch to it."""
        if not title or title == "Untitled":
            self._counter += 1
            title = f"Untitled-{self._counter}"
            
        if title in self._tabs:
            self._notebook.set(title)
            self._handle_tab_change()
            return title

        tab = EditorTab(self._notebook, title, content, path)
        self._tabs[title] = tab
        self._notebook.set(title)
        tab._text.focus_set()
        self._handle_tab_change()
        return title


    def get_active_tab(self) -> Optional[EditorTab]:
        """Return the currently visible EditorTab."""
        name = self._notebook.get()
        return self._tabs.get(name)

    def get_active_content(self) -> str:
        tab = self.get_active_tab()
        return tab.get_content() if tab else ""

    def insert_at_cursor(self, text: str) -> None:
        tab = self.get_active_tab()
        if tab:
            tab.insert_at_cursor(text)

    def save_active(self) -> bool:
        """Save the active tab. Returns True if saved."""
        tab = self.get_active_tab()
        if not tab:
            return False
        if tab.path:
            success = fm.save_file(tab.path, tab.get_content())
            if success:
                tab.dirty = False
            return success
        # No path — prompt save-as
        path = fm.save_file_as(tab.get_content())
        if path:
            tab.path = path
            tab.dirty = False
            return True
        return False

    def close_active(self) -> None:
        """Close the currently active tab."""
        name = self._notebook.get()
        if name in self._tabs:
            tab = self._tabs.pop(name)
            tab.destroy()
            self._notebook.delete(name)
            self._handle_tab_change()


