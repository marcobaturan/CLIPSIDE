"""Config manager — handles persistent IDE settings (e.g. last opened folder)."""

import json
import os
from pathlib import Path

CONFIG_FILE = Path.home() / ".clipside_config.json"

DEFAULT_CONFIG = {
    "last_project_root": str(Path.cwd()),
    "theme": "dark-blue",
}

def load_config() -> dict:
    """Load configuration from disk or return defaults."""
    if not CONFIG_FILE.exists():
        return DEFAULT_CONFIG
    
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            # Ensure all default keys exist
            for k, v in DEFAULT_CONFIG.items():
                if k not in config:
                    config[k] = v
            return config
    except Exception:
        return DEFAULT_CONFIG

def save_config(config: dict) -> None:
    """Save configuration to disk."""
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(f"Failed to save config: {e}")

def get_last_root() -> str:
    """Get the last project root, ensuring it still exists."""
    config = load_config()
    path = config.get("last_project_root")
    if path and os.path.isdir(path):
        return path
    return str(Path.cwd())

def set_last_root(path: str) -> None:
    """Save the last project root."""
    config = load_config()
    config["last_project_root"] = str(path)
    save_config(config)
