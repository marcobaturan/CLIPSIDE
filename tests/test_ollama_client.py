"""Tests for OllamaClient — mocked so no real Ollama instance is needed."""

import pytest
from unittest.mock import MagicMock, patch

from src.core import ollama_client as oc


@pytest.fixture(autouse=True)
def temp_sessions(tmp_path, monkeypatch):
    """Redirect session storage."""
    from src.core import session_history as sh
    monkeypatch.setattr(sh, "SESSION_DIR", tmp_path / "sessions")


def _make_chunk(text: str) -> dict:
    return {"message": {"content": text}}


class TestChatStream:
    def test_tokens_delivered_to_callback(self) -> None:
        tokens: list[str] = []
        chunks = [_make_chunk("Hello"), _make_chunk(" world")]
        with patch("ollama.chat", return_value=iter(chunks)):
            result = oc.chat_stream("hi", "sess-001", on_token=tokens.append)
        assert tokens == ["Hello", " world"]
        assert result == "Hello world"

    def test_exchange_saved_to_session(self) -> None:
        from src.core import session_history as sh
        chunks = [_make_chunk("answer")]
        with patch("ollama.chat", return_value=iter(chunks)):
            oc.chat_stream("question", "sess-002", on_token=lambda t: None)
        history = sh.load_history("sess-002")
        assert any(m["content"] == "question" for m in history)
        assert any(m["content"] == "answer" for m in history)

    def test_ollama_error_returns_error_message(self) -> None:
        tokens: list[str] = []
        with patch("ollama.chat", side_effect=ConnectionError("refused")):
            result = oc.chat_stream("hi", "sess-003", on_token=tokens.append)
        assert "Error" in result

    def test_system_prompt_injected(self) -> None:
        captured_messages: list = []
        def fake_chat(model, messages, stream):
            captured_messages.extend(messages)
            return iter([_make_chunk("ok")])
        with patch("ollama.chat", side_effect=fake_chat):
            oc.chat_stream("test", "sess-004", on_token=lambda t: None)
        assert captured_messages[0]["role"] == "system"
        assert "CLIPS" in captured_messages[0]["content"]


class TestGenerateSnippet:
    def test_returns_clips_code(self) -> None:
        fake_response = {"message": {"content": "(defrule test () => )"}}
        with patch("ollama.chat", return_value=fake_response):
            result = oc.generate_snippet("a simple rule")
        assert "(defrule" in result

    def test_error_returns_comment(self) -> None:
        with patch("ollama.chat", side_effect=Exception("boom")):
            result = oc.generate_snippet("anything")
        assert result.startswith("; Error")


class TestAvailabilityCheck:
    def test_available_when_model_listed(self) -> None:
        fake_list = {"models": [{"model": oc.MODEL}]}
        with patch("ollama.list", return_value=fake_list):
            assert oc.check_ollama_available() is True

    def test_unavailable_when_exception(self) -> None:
        with patch("ollama.list", side_effect=Exception("no server")):
            assert oc.check_ollama_available() is False
