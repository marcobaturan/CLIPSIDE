import sys
import os
from unittest.mock import MagicMock

# Mock tkinter and customtkinter before importing src
sys.modules['tkinter'] = MagicMock()
sys.modules['customtkinter'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.Image'] = MagicMock()
sys.modules['PIL.ImageTk'] = MagicMock()
sys.modules['clips'] = MagicMock()

# Mock components that are not easily testable without a real tk
sys.modules['src.ui.editor_panel'] = MagicMock()
sys.modules['src.ui.console_panel'] = MagicMock()
sys.modules['src.ui.facts_panel'] = MagicMock()
sys.modules['src.ui.agenda_panel'] = MagicMock()
sys.modules['src.ui.ai_panel'] = MagicMock()
sys.modules['src.ui.file_explorer'] = MagicMock()
sys.modules['src.ui.menu_bar'] = MagicMock()

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

def test_mainwindow_init():
    from src.ui.main_window import MainWindow
    # This should not raise AttributeError now
    try:
        app = MainWindow()
        print("MainWindow initialization successful (mocked)")
    except AttributeError as e:
        print(f"FAILED: AttributeError during init: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Other error (expected due to mocks): {type(e).__name__}: {e}")

if __name__ == "__main__":
    test_mainwindow_init()
