"""Ollama client — wraps the Ollama Python SDK with CLIPS system prompt and streaming."""

from typing import Callable, Generator, Optional

import ollama

from src.core import session_history as sh

# Model identifier
MODEL = "marcobaturan/clips-architect-final"

# CLIPS system prompt injected in every request to guide the model
CLIPS_SYSTEM_PROMPT = """You are CLIPS Architect, a specialized expert in the CLIPS (C Language Integrated Production System) rule-based programming language.

Key CLIPS syntax rules you MUST follow:
- Rules: (defrule name (pattern) => (action))
- Facts: (assert (fact-name slot-value))
- Templates: (deftemplate name (slot field (type TYPE)))
- Globals: (defglobal ?*name* = value)
- Functions: (deffunction name (?arg) body)
- Classes (COOL): (defclass Name (is-a USER) (slot field))
- Comments start with semicolons: ; this is a comment
- Strings use double quotes: "hello"
- Variables start with ?: ?variable
- Multifield variables: $?variable
- Salience: (declare (salience 100)) inside defrule

Do NOT invent functions that do not exist in CLIPS 6.4. Only use documented constructs.
Always return complete, runnable CLIPS code."""


def _build_messages(
    history: list[dict], user_message: str
) -> list[dict]:
    """Assemble the full message list: system prompt + history + new message."""
    messages = [{"role": "system", "content": CLIPS_SYSTEM_PROMPT}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_message})
    return messages


def chat_stream(
    user_message: str,
    session_id: str,
    on_token: Callable[[str], None],
    context_window: int = 10,
) -> str:
    """
    Stream a chat response token-by-token via a callback.

    Saves the exchange to the session history and returns the full response.
    """
    history = sh.get_context_window(session_id, n=context_window)
    messages = _build_messages(history, user_message)

    full_response_parts: list[str] = []
    try:
        stream = ollama.chat(
            model=MODEL,
            messages=messages,
            stream=True,
        )
        for chunk in stream:
            token = chunk["message"]["content"]
            full_response_parts.append(token)
            on_token(token)
    except Exception as exc:
        error_msg = f"\n[Error connecting to Ollama: {exc}]\nMake sure Ollama is running: ollama serve"
        on_token(error_msg)
        return error_msg

    full_response = "".join(full_response_parts)
    sh.save_message(session_id, "user", user_message)
    sh.save_message(session_id, "assistant", full_response)
    return full_response


def generate_snippet(description: str) -> str:
    """
    Generate a CLIPS code snippet from a natural language description.

    Returns the raw text response (no streaming).
    """
    prompt = (
        f"Generate a complete CLIPS rule or construct for the following requirement:\n\n"
        f"{description}\n\n"
        f"Return ONLY valid CLIPS code, no explanation."
    )
    messages = _build_messages([], prompt)
    try:
        response = ollama.chat(model=MODEL, messages=messages, stream=False)
        return response["message"]["content"]
    except Exception as exc:
        return f"; Error: {exc}"


def check_ollama_available() -> bool:
    """Return True if Ollama is running and the model is available."""
    try:
        models = ollama.list()
        names = [m["model"] for m in models.get("models", [])]
        return any(MODEL in name for name in names)
    except Exception:
        return False
