"""CLIPSIDE entry point — shows splash screen and launches the main window."""

import sys
import os

# Ensure src/ is on the path when running as `python src/main.py`
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import customtkinter as ctk

from src.ui.splash_screen import SplashScreen
from src.ui.main_window import MainWindow


def _load_modules(splash: SplashScreen) -> None:
    """Pre-import heavy modules while showing splash progress."""
    splash.set_progress(0.2, "Loading CLIPS engine…")
    import src.core.clips_engine  # noqa: F401

    splash.set_progress(0.45, "Loading AI client…")
    import src.core.ollama_client  # noqa: F401

    splash.set_progress(0.65, "Loading editor…")
    import src.ui.editor_panel    # noqa: F401

    splash.set_progress(0.85, "Initialising UI…")
    import src.ui.main_window     # noqa: F401

    splash.set_progress(1.0, "Ready!")
    splash.after(400, splash.close)


def main() -> None:
    """Application entry point."""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    root = ctk.CTk()
    root.withdraw()  # Hide root until ready

    splash = SplashScreen(root)
    root.after(100, lambda: _load_modules(splash))
    root.after(2200, lambda: _reveal(root))
    root.mainloop()


def _reveal(root: ctk.CTk) -> None:
    """Destroy root stub and open the real main window."""
    root.destroy()
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
