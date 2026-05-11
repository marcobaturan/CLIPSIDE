"""Console panel — interactive REPL for the CLIPS engine."""

import customtkinter as ctk
import tkinter as tk
from typing import Callable


class ConsolePanel(ctk.CTkFrame):
    """
    Bottom REPL panel: displays engine output and accepts user commands.
    Supports command history navigation with ↑ / ↓ keys.
    """

    def __init__(
        self,
        parent,
        on_command: Callable[[str], None],
        show_header: bool = True,
        **kwargs,
    ) -> None:
        super().__init__(parent, fg_color="#0D1117", **kwargs)
        self._on_command = on_command
        self._history: list[str] = []
        self._history_index = -1
        self._show_header = show_header
        self._build()

    def _build(self) -> None:
        # Optional internal header (skipped when parent provides one)
        if self._show_header:
            header = ctk.CTkFrame(self, fg_color="#161B22", height=28)
            header.pack(fill="x")
            ctk.CTkLabel(
                header, text="  ◉ CLIPS Console",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="#00FF88",
            ).pack(side="left", padx=4)
            clear_target = header
        else:
            clear_target = None

        # Clear button — attached to internal header or standalone toolbar
        def _make_clear_btn(parent):
            ctk.CTkButton(
                parent, text="Clear", width=60, height=22,
                fg_color="#1F2937", hover_color="#374151",
                command=self.clear,
            ).pack(side="right", padx=4, pady=3)

        if clear_target:
            _make_clear_btn(clear_target)

        # Output area
        self._output = tk.Text(
            self, bg="#0D1117", fg="#EEFFFF",
            font=("Courier New", 11),
            state="disabled", wrap="word",
            relief="flat", padx=6, pady=4,
            height=8,
        )
        self._output.pack(fill="both", expand=True)

        # Tag styles for output
        self._output.tag_config("prompt", foreground="#00FF88")
        self._output.tag_config("error",  foreground="#FF5370")
        self._output.tag_config("info",   foreground="#546E7A")

        # Input row
        input_frame = ctk.CTkFrame(self, fg_color="#161B22", height=36)
        input_frame.pack(fill="x")
        self._prompt_label = ctk.CTkLabel(
            input_frame, text="CLIPS> ",
            font=ctk.CTkFont(family="Courier New", size=12),
            text_color="#00FF88",
        )
        self._prompt_label.pack(side="left", padx=(8, 0))
        self._dir_label = ctk.CTkLabel(
            input_frame, text="",
            font=ctk.CTkFont(size=9),
            text_color="#546E7A",
        )
        self._dir_label.pack(side="left", padx=(4, 0))
        self._entry = ctk.CTkEntry(
            input_frame,
            fg_color="#0D1117", border_color="#1F6FEB",
            text_color="#EEFFFF",
            font=ctk.CTkFont(family="Courier New", size=12),
        )
        self._entry.pack(side="left", fill="x", expand=True, padx=4, pady=4)
        ctk.CTkButton(
            input_frame, text="Run", width=60, height=28,
            fg_color="#1F6FEB", hover_color="#388BFD",
            command=self._submit,
        ).pack(side="right", padx=4)

        self._entry.bind("<Return>", lambda _: self._submit())
        self._entry.bind("<Up>", self._history_up)
        self._entry.bind("<Down>", self._history_down)

    def _submit(self) -> None:
        """Read the entry, echo to output, pass to engine callback."""
        cmd = self._entry.get().strip()
        if not cmd:
            return
        self._history.append(cmd)
        self._history_index = -1
        self._entry.delete(0, "end")
        self.append(f"CLIPS> {cmd}\n", tag="prompt")
        self._on_command(cmd)

    def _history_up(self, _event=None) -> None:
        if not self._history:
            return
        if self._history_index == -1:
            self._history_index = len(self._history) - 1
        elif self._history_index > 0:
            self._history_index -= 1
        self._entry.delete(0, "end")
        self._entry.insert(0, self._history[self._history_index])

    def _history_down(self, _event=None) -> None:
        if self._history_index == -1:
            return
        if self._history_index < len(self._history) - 1:
            self._history_index += 1
            self._entry.delete(0, "end")
            self._entry.insert(0, self._history[self._history_index])
        else:
            self._history_index = -1
            self._entry.delete(0, "end")

    def append(self, text: str, tag: str = "") -> None:
        """Append text to the output area, auto-scrolling to the bottom."""
        self._output.config(state="normal")
        if tag:
            self._output.insert("end", text, tag)
        else:
            self._output.insert("end", text)
        self._output.see("end")
        self._output.config(state="disabled")

    def set_context_dir(self, path: str) -> None:
        """Show the current working directory context next to the prompt."""
        self._dir_label.configure(text=f"[{path}]")

    def clear(self) -> None:
        """Clear the output area."""
        self._output.config(state="normal")
        self._output.delete("1.0", "end")
        self._output.config(state="disabled")
