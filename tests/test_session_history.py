"""Tests for session_history — TDD-first."""

import json
import pytest
from pathlib import Path
from unittest.mock import patch

from src.core import session_history as sh


@pytest.fixture(autouse=True)
def temp_session_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Redirect session storage to a temporary directory for each test."""
    monkeypatch.setattr(sh, "SESSION_DIR", tmp_path / "sessions")


class TestSaveAndLoad:
    def test_save_and_load_single_message(self) -> None:
        sid = "test-session-001"
        sh.save_message(sid, "user", "Hello CLIPS")
        history = sh.load_history(sid)
        assert len(history) == 1
        assert history[0] == {"role": "user", "content": "Hello CLIPS"}

    def test_load_nonexistent_session_returns_empty(self) -> None:
        result = sh.load_history("nonexistent-session")
        assert result == []

    def test_multiple_messages_preserved_in_order(self) -> None:
        sid = "test-session-002"
        sh.save_message(sid, "user", "first")
        sh.save_message(sid, "assistant", "second")
        sh.save_message(sid, "user", "third")
        history = sh.load_history(sid)
        assert [m["content"] for m in history] == ["first", "second", "third"]


class TestContextWindow:
    def test_context_window_returns_last_n(self) -> None:
        sid = "test-window-001"
        for i in range(15):
            sh.save_message(sid, "user", f"msg-{i}")
        context = sh.get_context_window(sid, n=5)
        assert len(context) == 5
        assert context[-1]["content"] == "msg-14"

    def test_context_window_smaller_than_history(self) -> None:
        sid = "test-window-002"
        sh.save_message(sid, "user", "only one")
        context = sh.get_context_window(sid, n=10)
        assert len(context) == 1


class TestSessionManagement:
    def test_list_sessions_returns_created_sessions(self) -> None:
        sh.save_message("alpha", "user", "a")
        sh.save_message("beta", "user", "b")
        sessions = sh.list_sessions()
        assert "alpha" in sessions
        assert "beta" in sessions

    def test_delete_session_removes_file(self) -> None:
        sh.save_message("to-delete", "user", "bye")
        sh.delete_session("to-delete")
        assert sh.load_history("to-delete") == []

    def test_new_session_id_is_string(self) -> None:
        sid = sh.new_session_id()
        assert isinstance(sid, str)
        assert len(sid) > 0


class TestMaxMessages:
    def test_trim_to_max_messages(self) -> None:
        sid = "test-trim"
        sh.MAX_SESSION_MESSAGES = 5
        for i in range(10):
            sh.save_message(sid, "user", f"msg-{i}")
        history = sh.load_history(sid)
        # Should be trimmed to last 5
        assert len(history) <= 5
        assert history[-1]["content"] == "msg-9"
