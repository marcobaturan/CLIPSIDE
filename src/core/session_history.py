"""Session history manager — persists conversation context across sessions."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


# Directory where session files are stored
SESSION_DIR = Path.home() / ".clipside" / "sessions"

# Maximum messages kept in a single session file
MAX_SESSION_MESSAGES = 200


def _session_dir() -> Path:
    """Return the session directory, creating it if needed."""
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    return SESSION_DIR


def _session_path(session_id: str) -> Path:
    """Return the file path for a given session ID."""
    return _session_dir() / f"{session_id}.json"


def new_session_id() -> str:
    """Generate a timestamp-based session ID."""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def save_message(session_id: str, role: str, content: str) -> None:
    """Append a message to the session history file."""
    path = _session_path(session_id)
    history = load_history(session_id)
    history.append({"role": role, "content": content})
    # Trim to max to avoid unbounded growth
    if len(history) > MAX_SESSION_MESSAGES:
        history = history[-MAX_SESSION_MESSAGES:]
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(history, fh, indent=2, ensure_ascii=False)


def load_history(session_id: str) -> list[dict]:
    """Load full message history for a session. Returns empty list if not found."""
    path = _session_path(session_id)
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def get_context_window(session_id: str, n: int = 10) -> list[dict]:
    """Return the last n messages for use as context in API calls."""
    history = load_history(session_id)
    return history[-n:]


def list_sessions() -> list[str]:
    """Return all available session IDs, sorted newest first."""
    dir_ = _session_dir()
    files = sorted(dir_.glob("*.json"), reverse=True)
    return [f.stem for f in files]


def delete_session(session_id: str) -> None:
    """Delete a session file permanently."""
    path = _session_path(session_id)
    if path.exists():
        path.unlink()
