"""Agenda panel — displays pending rule activations."""

import customtkinter as ctk
import tkinter as tk


class AgendaPanel(ctk.CTkFrame):
    """Live list of CLIPS agenda activations."""

    def __init__(self, parent, show_header: bool = False, **kwargs) -> None:
        super().__init__(parent, fg_color="#0D1117", **kwargs)
        self._show_header = show_header
        self._build()

    def _build(self) -> None:
        if self._show_header:
            header = ctk.CTkFrame(self, fg_color="#161B22", height=28)
            header.pack(fill="x")
            ctk.CTkLabel(
                header, text="  ⚡ Agenda",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="#C792EA",
            ).pack(side="left", padx=4)

        self._listbox = tk.Listbox(
            self, bg="#0D1117", fg="#C792EA",
            selectbackground="#1F6FEB",
            font=("Courier New", 10),
            relief="flat", borderwidth=0,
        )
        scrollbar = ctk.CTkScrollbar(self, command=self._listbox.yview)
        self._listbox.configure(yscrollcommand=scrollbar.set)
        self._listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def update_agenda(self, activations: list[str]) -> None:
        """Replace the activation list."""
        self._listbox.delete(0, "end")
        for item in activations:
            self._listbox.insert("end", item)


class InstancePanel(ctk.CTkFrame):
    """Live list of COOL class instances."""

    def __init__(self, parent, show_header: bool = False, **kwargs) -> None:
        super().__init__(parent, fg_color="#0D1117", **kwargs)
        self._show_header = show_header
        self._build()

    def _build(self) -> None:
        if self._show_header:
            header = ctk.CTkFrame(self, fg_color="#161B22", height=28)
            header.pack(fill="x")
            ctk.CTkLabel(
                header, text="  🔷 Instances",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="#89DDFF",
            ).pack(side="left", padx=4)

        self._listbox = tk.Listbox(
            self, bg="#0D1117", fg="#89DDFF",
            selectbackground="#1F6FEB",
            font=("Courier New", 10),
            relief="flat", borderwidth=0,
        )
        scrollbar = ctk.CTkScrollbar(self, command=self._listbox.yview)
        self._listbox.configure(yscrollcommand=scrollbar.set)
        self._listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def update_instances(self, instances: list[str]) -> None:
        """Replace the instance list."""
        self._listbox.delete(0, "end")
        for item in instances:
            self._listbox.insert("end", item)
