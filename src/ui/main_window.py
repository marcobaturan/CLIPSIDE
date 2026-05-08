"""Main window — assembles all panels with clear column layout and visual identity."""

import os
import subprocess
import tkinter as tk
from pathlib import Path
from typing import Optional, Callable
import customtkinter as ctk
from tkinter import messagebox

from src.core.clips_engine import ClipsEngine
from src.core import file_manager as fm
import src.core.config_manager as cfg
from src.ui.editor_panel import EditorPanel
from src.ui.console_panel import ConsolePanel
from src.ui.facts_panel import FactsPanel
from src.ui.agenda_panel import AgendaPanel, InstancePanel
from src.ui.ai_panel import AiPanel
from src.ui.file_explorer import FileExplorer
from src.ui.menu_bar import MenuBar

# --- Project State ---
_PROJECT_ROOT = cfg.get_last_root()

# Colours
_BG_DARK  = "#0A0E1A"
_BG_MID   = "#0D1117"
_BG_PANEL = "#111827"
_BORDER   = "#1F2937"
_ACCENT   = "#1F6FEB"
_GREEN    = "#00FF88"
_AMBER    = "#FFCB6B"
_PURPLE   = "#C792EA"
_CYAN     = "#89DDFF"
_GREY     = "#546E7A"


def _panel_header(parent, icon: str, label: str, colour: str, actions: list = None) -> ctk.CTkFrame:
    """Create a styled column/panel header bar with optional action buttons."""
    bar = ctk.CTkFrame(parent, fg_color=_BORDER, height=32, corner_radius=0)
    bar.pack(fill="x")
    bar.pack_propagate(False)
    
    ctk.CTkLabel(
        bar,
        text=f"  {icon}  {label}",
        font=ctk.CTkFont(family="Courier New", size=12, weight="bold"),
        text_color=colour,
    ).pack(side="left", padx=6, pady=4)

    if actions:
        for btn_icon, btn_cmd in reversed(actions):
            ctk.CTkButton(
                bar, text=btn_icon, width=24, height=22,
                fg_color="transparent", hover_color=_BG_DARK,
                font=ctk.CTkFont(size=14),
                command=btn_cmd,
            ).pack(side="right", padx=2, pady=4)
            
    return bar


def _column_wrapper(parent, title: str, icon: str, colour: str, **kwargs) -> ctk.CTkFrame:
    """Create a labelled column frame with a top header."""
    outer = ctk.CTkFrame(parent, fg_color=_BORDER, corner_radius=6, **kwargs)
    inner = ctk.CTkFrame(outer, fg_color=_BG_MID, corner_radius=0)
    _panel_header(inner, icon, title, colour)
    inner.pack(fill="both", expand=True, padx=1, pady=(0, 1))
    return outer, inner


class MainWindow(ctk.CTk):
    """Root application window: 3 columns with visible panel labels."""

    def __init__(self) -> None:
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.title("CLIPSIDE — Modern CLIPS IDE")
        self.geometry("1440x880")
        self.minsize(960, 620)
        self.configure(fg_color=_BG_DARK)

        self._set_icon()
        self._engine = ClipsEngine(output_callback=self._on_engine_output)

        self._build_menu()
        self._build_layout()
        self._bind_shortcuts()

        self._editor.new_tab()

    # ------------------------------------------------------------------
    # Icon
    # ------------------------------------------------------------------

    def _set_icon(self) -> None:
        icon_path = Path(__file__).parent.parent / "assets" / "icon.png"
        if icon_path.exists():
            from PIL import Image, ImageTk
            img = Image.open(icon_path).resize((64, 64))
            self._icon = ImageTk.PhotoImage(img)
            self.iconphoto(True, self._icon)

    # ------------------------------------------------------------------
    # Menu
    # ------------------------------------------------------------------

    def _build_menu(self) -> None:
        callbacks = {
            "new":             self._cmd_new,
            "open":            self._cmd_open,
            "open_folder":     self._cmd_open_folder,
            "new_folder":      self._cmd_new_folder,
            "build":           self._cmd_build_buffer,
            "run":             self._cmd_run,
            "save":            self._cmd_save,
            "save_as":         self._cmd_save_as,
            "close":           self._cmd_close,
            "exit":            self.destroy,

            "undo":            lambda: self.focus_get() and self.focus_get().event_generate("<<Undo>>"),
            "redo":            lambda: self.focus_get() and self.focus_get().event_generate("<<Redo>>"),
            "cut":             lambda: self.focus_get() and self.focus_get().event_generate("<<Cut>>"),
            "copy":            lambda: self.focus_get() and self.focus_get().event_generate("<<Copy>>"),
            "paste":           lambda: self.focus_get() and self.focus_get().event_generate("<<Paste>>"),
            "load_constructs": self._cmd_load_constructs,
            "reset":           self._cmd_reset,
            "run":             self._cmd_run,
            "step":            self._cmd_step,
            "clear":           self._cmd_clear,
            "show_facts":      lambda: self._inspect_tabs.set("📋 Facts"),
            "show_agenda":     lambda: self._inspect_tabs.set("⚡ Agenda"),
            "show_instances":  lambda: self._inspect_tabs.set("🔷 Instances"),
            "pull_model":      self._cmd_pull_model,
            "session_history": lambda: None,
            "manual":          self._cmd_manual,

            "about":           self._cmd_about,
        }
        self._menubar = MenuBar(self, callbacks)
        self.config(menu=self._menubar)

    # ------------------------------------------------------------------
    # Layout — 3 columns with panel headers
    # ------------------------------------------------------------------

    def _build_layout(self) -> None:
        # Status bar at the very bottom
        self._status_bar = self._build_status_bar()

        # === 1. TOP-LEVEL CONTAINERS ===
        h_pane = tk.PanedWindow(
            self, orient="horizontal",
            bg=_BG_DARK, sashwidth=5, sashrelief="flat",
            sashpad=0,
        )
        h_pane.pack(fill="both", expand=True, padx=4, pady=(4, 0))

        # Column containers (Outer)
        left_outer = ctk.CTkFrame(h_pane, fg_color=_BORDER, corner_radius=6)
        centre_outer = ctk.CTkFrame(h_pane, fg_color=_BORDER, corner_radius=6)
        right_outer = ctk.CTkFrame(h_pane, fg_color=_BORDER, corner_radius=6)

        h_pane.add(left_outer, minsize=240, width=320)
        h_pane.add(centre_outer, minsize=400)
        h_pane.add(right_outer, minsize=240, width=300)

        # Column containers (Inner)
        left_inner = ctk.CTkFrame(left_outer, fg_color=_BG_MID, corner_radius=0)
        left_inner.pack(fill="both", expand=True, padx=1, pady=(0, 1))
        
        centre_inner = ctk.CTkFrame(centre_outer, fg_color=_BG_MID, corner_radius=0)
        centre_inner.pack(fill="both", expand=True, padx=1, pady=(0, 1))
        
        right_inner = ctk.CTkFrame(right_outer, fg_color=_BG_MID, corner_radius=0)
        right_inner.pack(fill="both", expand=True, padx=1, pady=(0, 1))

        # === 2. CENTRE COLUMN (Editor) ===
        editor_header_container = ctk.CTkFrame(centre_inner, fg_color=_BG_MID, corner_radius=0)
        _panel_header(
            editor_header_container, "✏️", "Editor", _GREEN,
            actions=[
                ("✖",  self._cmd_close),
                ("🔨", self._cmd_build_buffer),
                ("▶",  self._cmd_run),
                ("💾", self._cmd_save),
            ]
        )

        editor_header_container.pack(fill="x")
        
        v_pane = tk.PanedWindow(centre_inner, orient="vertical", bg=_BG_DARK, sashwidth=5, sashrelief="flat")
        v_pane.pack(fill="both", expand=True)

        editor_frame = ctk.CTkFrame(v_pane, fg_color=_BG_MID, corner_radius=0)
        self._editor = EditorPanel(editor_frame, on_tab_change=self._on_editor_tab_change)
        self._editor.pack(fill="both", expand=True)
        v_pane.add(editor_frame, minsize=200)

        console_frame = ctk.CTkFrame(v_pane, fg_color=_BG_MID, corner_radius=0)
        _panel_header(console_frame, "◉", "CLIPS Console", _GREEN)
        self._console = ConsolePanel(console_frame, on_command=self._handle_console_command, show_header=False)
        self._console.pack(fill="both", expand=True)
        v_pane.add(console_frame, minsize=120, height=180)

        # === 3. LEFT COLUMN (Explorer + AI) ===
        left_v_pane = tk.PanedWindow(left_inner, orient="vertical", bg=_BG_DARK, sashwidth=5, sashrelief="flat")
        left_v_pane.pack(fill="both", expand=True)

        explorer_frame = ctk.CTkFrame(left_v_pane, fg_color=_BG_MID, corner_radius=0)
        _panel_header(
            explorer_frame, "📁", "Explorer", _AMBER,
            actions=[
                ("⟳", self._refresh_explorer),
                ("＋", self._cmd_new_folder),
                ("📄", self._cmd_new_file_in_context),
            ]
        )
        self._explorer = FileExplorer(explorer_frame, root_dir=_PROJECT_ROOT, on_open_file=self._open_file_from_explorer, on_folder_double_click=self._cmd_new_folder, show_header=False, folders_only=False)
        self._explorer.pack(fill="both", expand=True)
        left_v_pane.add(explorer_frame, minsize=200, height=350)

        ai_frame = ctk.CTkFrame(left_v_pane, fg_color=_BG_MID, corner_radius=0)
        _panel_header(ai_frame, "🤖", "AI Assistant", _CYAN)
        self._ai_panel = AiPanel(ai_frame, on_insert_snippet=self._editor.insert_at_cursor, show_header=False)
        self._ai_panel.pack(fill="both", expand=True)
        left_v_pane.add(ai_frame, minsize=200)

        # === 4. RIGHT COLUMN (Inspector) ===
        inspect_frame = ctk.CTkFrame(right_inner, fg_color=_BG_MID, corner_radius=0)
        _panel_header(inspect_frame, "🔍", "Inspector", _AMBER)
        self._inspect_tabs = ctk.CTkTabview(inspect_frame, fg_color=_BG_MID, segmented_button_fg_color=_BORDER, segmented_button_selected_color=_ACCENT, segmented_button_selected_hover_color="#388BFD", segmented_button_unselected_color=_BORDER, segmented_button_unselected_hover_color="#1F2937", border_color=_BORDER, border_width=1)
        self._inspect_tabs.pack(fill="both", expand=True)
        self._facts_panel    = FactsPanel(self._inspect_tabs.add("📋 Facts"))
        self._agenda_panel   = AgendaPanel(self._inspect_tabs.add("⚡ Agenda"))
        self._instance_panel = InstancePanel(self._inspect_tabs.add("🔷 Instances"))
        for p in (self._facts_panel, self._agenda_panel, self._instance_panel): p.pack(fill="both", expand=True)
        inspect_frame.pack(fill="both", expand=True)

    def _build_status_bar(self) -> ctk.CTkFrame:
        """Thin status bar at the bottom of the window."""
        bar = ctk.CTkFrame(self, fg_color=_BORDER, height=22, corner_radius=0)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)
        self._status_text = ctk.CTkLabel(
            bar, text="  Ready",
            font=ctk.CTkFont(size=10), text_color=_GREY,
        )
        self._status_text.pack(side="left", padx=6)
        ctk.CTkLabel(
            bar, text="CLIPS 6.41  │  Ollama marcobaturan/clips-architect-final  ",
            font=ctk.CTkFont(size=10), text_color=_GREY,
        ).pack(side="right", padx=6)
        return bar

    def _set_status(self, text: str) -> None:
        self._status_text.configure(text=f"  {text}")

    # ------------------------------------------------------------------
    # Keyboard shortcuts
    # ------------------------------------------------------------------

    def _bind_shortcuts(self) -> None:
        self.bind("<Control-n>", lambda _: self._cmd_new())
        self.bind("<Control-o>", lambda _: self._cmd_open())
        self.bind("<Control-b>", lambda _: self._cmd_build_buffer())
        self.bind("<Control-Shift-N>", lambda _: self._cmd_new_folder())
        self.bind("<Control-s>", lambda _: self._cmd_save())
        self.bind("<Control-S>", lambda _: self._cmd_save_as())
        self.bind("<Control-w>", lambda _: self._cmd_close())
        self.bind("<F5>",        lambda _: self._cmd_reset())

        self.bind("<F6>",        lambda _: self._cmd_run())
        self.bind("<F7>",        lambda _: self._cmd_step())

    # ------------------------------------------------------------------
    # Engine commands
    # ------------------------------------------------------------------

    def _cmd_reset(self) -> None:
        self._engine.reset()
        self._console.append("=== Reset ===\n", "info")
        self._set_status("Environment reset")
        self._refresh_inspectors()

    def _cmd_run(self) -> None:
        fired = self._engine.run()
        self._console.append(f"=== Run: {fired} rules fired ===\n", "info")
        self._set_status(f"Run complete — {fired} rules fired")
        self._refresh_inspectors()

    def _cmd_step(self) -> None:
        fired = self._engine.step()
        self._console.append(f"=== Step: {fired} rule(s) ===\n", "info")
        self._set_status(f"Step — {fired} rule(s) fired")
        self._refresh_inspectors()

    def _cmd_clear(self) -> None:
        self._engine.clear()
        self._console.append("=== Cleared ===\n", "info")
        self._set_status("Environment cleared")
        self._refresh_inspectors()

    def _cmd_load_constructs(self) -> None:
        result = fm.open_file()
        if result:
            path, content = result
            self._editor.new_tab(title=Path(path).name, content=content, path=path)
            try:
                self._engine.load_file(path)
                self._console.append(f"Loaded: {path}\n", "info")
                self._set_status(f"Loaded {Path(path).name}")
                self._refresh_inspectors()
            except Exception as exc:
                self._console.append(f"[ERROR] {exc}\n", "error")

    def _cmd_build_buffer(self) -> None:
        """Build current editor content into CLIPS environment."""
        content = self._editor.get_active_content()
        if not content.strip():
            return
            
        try:
            # Save to a temporary file to load multiple constructs safely
            import tempfile
            with tempfile.NamedTemporaryFile(suffix=".clp", mode="w", delete=False) as f:
                f.write(content)
                temp_path = f.name
            
            self._engine.load_file(temp_path)
            os.unlink(temp_path)
            
            self._refresh_inspectors()
            self._set_status("Code built successfully.")
        except Exception as exc:
            self._console.append(f"\n[BUILD ERROR] {exc}\n", "error")
            messagebox.showerror("Build Error", f"Failed to build constructs: {exc}")

    def _cmd_run(self) -> None:
        """Run the CLIPS engine."""
        try:
            count = self._engine.run()
            self._console.append(f"[ENGINE] Fired {count} rules.\n", "info")
            self._refresh_inspectors()
        except Exception as exc:
            self._console.append(f"[RUN ERROR] {exc}\n", "error")

    def _handle_console_command(self, cmd: str) -> None:
        try:
            result = self._engine.eval(cmd)
            if result is not None:
                self._console.append(f"{result}\n")
        except Exception as exc:
            self._console.append(f"[ERROR] {exc}\n", "error")
        self._refresh_inspectors()

    def _on_engine_output(self, message: str) -> None:
        self._console.append(message)

    def _refresh_inspectors(self) -> None:
        self._facts_panel.update_facts(self._engine.get_facts())
        self._agenda_panel.update_agenda(self._engine.get_agenda())
        self._instance_panel.update_instances(self._engine.get_instances())

    def _on_editor_tab_change(self, path: Optional[str]) -> None:
        """Sync process working directory with the active tab's file location."""
        if path:
            target_dir = os.path.dirname(path)
            if os.path.isdir(target_dir):
                os.chdir(target_dir)
                self._set_status(f"Context: {os.path.basename(target_dir)}")
        else:
            os.chdir(_PROJECT_ROOT)
            self._set_status("Context: Project Root")

    # ------------------------------------------------------------------
    # File commands
    # ------------------------------------------------------------------

    def _cmd_new(self) -> None:
        self._editor.new_tab(content=fm.new_file_content())
        self._set_status("New file")

    def _refresh_explorer(self) -> None:
        self._explorer.refresh()
        self._set_status("Explorer refreshed")

    def _cmd_new_folder(self, path: Optional[str] = None) -> None:
        """Create a new subfolder. If path is provided, use it as parent."""
        selected = path or self._explorer.get_selected_path()
        base_path = Path(selected) if selected and os.path.isdir(selected) else Path(_PROJECT_ROOT)
        
        dialog = ctk.CTkInputDialog(text=f"New folder in {base_path.name}:", title="New Folder")
        name = dialog.get_input()
        if name:
            new_path = base_path / name
            try:
                new_path.mkdir(parents=True, exist_ok=True)
                self._explorer.refresh()
                self._set_status(f"Created folder: {name}")
            except Exception as exc:
                messagebox.showerror("Error", f"Could not create folder: {exc}")

    def _cmd_new_file_in_context(self) -> None:
        """Create a new file in the selected directory."""
        selected = self._explorer.get_selected_path()
        base_path = Path(selected) if selected and os.path.isdir(selected) else Path(_PROJECT_ROOT)
        
        dialog = ctk.CTkInputDialog(text=f"New .clp file in {base_path.name}:", title="New File")
        name = dialog.get_input()
        if name:
            if not name.endswith(".clp"):
                name += ".clp"
            new_path = base_path / name
            try:
                new_path.write_text(fm.new_file_content(), encoding="utf-8")
                self._explorer.refresh()
                self._open_file_from_explorer(str(new_path))
                self._set_status(f"Created file: {name}")
            except Exception as exc:
                messagebox.showerror("Error", f"Could not create file: {exc}")


    def _cmd_open(self) -> None:
        result = fm.open_file()
        if result:
            path, content = result
            self._editor.new_tab(title=Path(path).name, content=content, path=path)
            self._set_status(f"Opened {Path(path).name}")

    def _cmd_open_folder(self) -> None:
        """Open a directory and set it as the new project root."""
        path = fm.open_directory()
        if path:
            global _PROJECT_ROOT
            _PROJECT_ROOT = path
            cfg.set_last_root(path)
            os.chdir(path)
            self._explorer.update_root(path)
            self._refresh_explorer()
            self._set_status(f"Project root: {path}")


    def _open_file_from_explorer(self, path: str) -> None:
        content = fm.read_file(path)
        self._editor.new_tab(title=Path(path).name, content=content, path=path)
        self._set_status(f"Opened {Path(path).name}")

    def _cmd_save(self) -> None:
        if self._editor.save_active():
            self._set_status("Saved")

    def _cmd_save_as(self) -> None:
        tab = self._editor.get_active_tab()
        if tab:
            path = fm.save_file_as(tab.get_content())
            if path:
                tab.path = path
                tab.dirty = False
                self._set_status(f"Saved as {Path(path).name}")

    def _cmd_close(self) -> None:
        """Close the active editor tab."""
        self._editor.close_active()
        self._set_status("File closed")


    # ------------------------------------------------------------------
    # Help / meta
    # ------------------------------------------------------------------

    def _cmd_pull_model(self) -> None:
        subprocess.Popen(
            ["x-terminal-emulator", "-e",
             "ollama pull marcobaturan/clips-architect-final"],
            stderr=subprocess.DEVNULL,
        )

    def _cmd_manual(self) -> None:
        manual = Path(__file__).parent.parent.parent / "docs" / "USER_MANUAL.md"
        if manual.exists():
            subprocess.Popen(["xdg-open", str(manual)])

    def _cmd_about(self) -> None:
        messagebox.showinfo(
            "About CLIPSIDE",
            "CLIPSIDE — Modern CLIPS IDE\n"
            "Version 0.1.0 (Beta)\n\n"
            "Developed by Marco Baturan\n"
            "GitHub: https://github.com/marcobaturan/CLIPSIDE\n\n"
            "License: MIT (Open Source & Free)\n\n"
            "Acknowledgements:\n"
            "• Gary Riley (Creator of CLIPS)\n"
            "• Matteo Cafasso (Creator of CLIPSPy)\n"
            "• Tom Schimansky (Creator of CustomTkinter)\n\n"
            "Powered by:\n"
            "• CLIPSpy (CLIPS 6.41)\n"
            "• CustomTkinter\n"
            "• Ollama (clips-architect-final)\n\n"
            "© 2026 Marco Baturan",
        )



