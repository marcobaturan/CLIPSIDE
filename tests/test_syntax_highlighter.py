"""Tests for the CLIPS syntax highlighter — token generation only (no Tk)."""

import pytest
from pygments.token import Token

from src.ui.syntax_highlighter import tokenise, ClipsLexer


def _token_types(code: str) -> list:
    """Return only token types from tokenise(), excluding whitespace."""
    return [tt for tt, val in tokenise(code) if val.strip()]


def _has_token(code: str, expected_type, expected_value: str) -> bool:
    """Check that a given token type + value appears in the output."""
    return any(
        tt in expected_type and val == expected_value
        for tt, val in tokenise(code)
    )


class TestKeywords:
    def test_defrule_is_keyword(self) -> None:
        assert _has_token("defrule", Token.Keyword, "defrule")

    def test_deffacts_is_keyword(self) -> None:
        assert _has_token("deffacts", Token.Keyword, "deffacts")

    def test_deftemplate_is_keyword(self) -> None:
        assert _has_token("deftemplate", Token.Keyword, "deftemplate")

    def test_defglobal_is_keyword(self) -> None:
        assert _has_token("defglobal", Token.Keyword, "defglobal")


class TestBuiltins:
    def test_assert_is_builtin(self) -> None:
        assert _has_token("assert", Token.Name.Builtin, "assert")

    def test_retract_is_builtin(self) -> None:
        assert _has_token("retract", Token.Name.Builtin, "retract")

    def test_run_is_builtin(self) -> None:
        assert _has_token("run", Token.Name.Builtin, "run")

    def test_printout_is_builtin(self) -> None:
        assert _has_token("printout", Token.Name.Builtin, "printout")


class TestVariables:
    def test_simple_variable(self) -> None:
        assert _has_token("?x", Token.Name.Variable, "?x")

    def test_multifield_variable(self) -> None:
        assert _has_token("$?items", Token.Name.Variable, "$?items")


class TestLiterals:
    def test_string_literal(self) -> None:
        assert _has_token('"hello world"', Token.Literal.String, '"hello world"')

    def test_integer_literal(self) -> None:
        assert _has_token("42", Token.Literal.Number.Integer, "42")

    def test_float_literal(self) -> None:
        assert _has_token("3.14", Token.Literal.Number.Float, "3.14")


class TestComments:
    def test_semicolon_comment(self) -> None:
        assert _has_token("; this is a comment", Token.Comment, "; this is a comment")


class TestOperators:
    def test_arrow_operator(self) -> None:
        assert _has_token("=>", Token.Operator, "=>")


class TestFullRule:
    def test_complete_rule_tokenises_without_error(self) -> None:
        code = """
(defrule temperature-alert
    ; Fires when temperature exceeds threshold
    (temperature ?t&:(> ?t 100))
    =>
    (printout t "ALERT: " ?t crlf))
"""
        types = _token_types(code)
        # Must contain keywords, builtins, variables — no unexpected errors
        assert Token.Keyword in types or any(tt in Token.Keyword for tt in types)
        # No error tokens in valid code
        error_tokens = [val for tt, val in tokenise(code) if tt == Token.Error]
        assert error_tokens == []
