"""Facts panel — live display of the CLIPS working memory."""

import customtkinter as ctk
import tkinter as tk


class FactsPanel(ctk.CTkFrame):
    """
    Scrollable list of current CLIPS facts.
    Refreshed by calling update_facts() after each engine operation.
    """

    def __init__(self, parent, show_header: bool = False, **kwargs) -> None:
        super().__init__(parent, fg_color="#0D1117", **kwargs)
        self._show_header = show_header
        self._build()

    def _build(self) -> None:
        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", lambda *_: self._apply_filter())

        if self._show_header:
            header = ctk.CTkFrame(self, fg_color="#161B22", height=28)
            header.pack(fill="x")
            ctk.CTkLabel(
                header, text="  📋 Facts",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="#FFCB6B",
            ).pack(side="left", padx=4)
            ctk.CTkEntry(
                header, textvariable=self._search_var,
                placeholder_text="Filter…", width=120, height=22,
                fg_color="#0D1117", border_color="#374151",
            ).pack(side="right", padx=4, pady=3)
        else:
            # Show just the filter row if no header
            filter_row = ctk.CTkFrame(self, fg_color="#161B22", height=26)
            filter_row.pack(fill="x")
            ctk.CTkEntry(
                filter_row, textvariable=self._search_var,
                placeholder_text="Filter facts…", width=180, height=20,
                fg_color="#0D1117", border_color="#374151",
            ).pack(side="left", padx=6, pady=2)

        # Listbox
        self._listbox = tk.Listbox(
            self, bg="#0D1117", fg="#C3E88D",
            selectbackground="#1F6FEB",
            font=("Courier New", 10),
            relief="flat", borderwidth=0,
        )
        scrollbar = ctk.CTkScrollbar(self, command=self._listbox.yview)
        self._listbox.configure(yscrollcommand=scrollbar.set)
        self._listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._all_facts: list[str] = []

    def update_facts(self, facts: list[str]) -> None:
        """Replace the current fact list."""
        self._all_facts = facts
        self._apply_filter()

    def _apply_filter(self) -> None:
        """Filter displayed facts by the search term."""
        query = self._search_var.get().lower()
        self._listbox.delete(0, "end")
        for fact in self._all_facts:
            if query in fact.lower():
                self._listbox.insert("end", fact)
