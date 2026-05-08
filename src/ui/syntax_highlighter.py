"""CLIPS syntax highlighter — Pygments lexer + tag applicator for CTkTextbox."""

import re
from typing import Iterator

from pygments.lexer import RegexLexer, bygroups
from pygments import token as T
from pygments.token import Token

# -----------------------------------------------------------------------
# Colour palette — optimised for dark backgrounds
# -----------------------------------------------------------------------
COLOUR_MAP: dict[T._TokenType, str] = {
    Token.Keyword:             "#C792EA",   # purple — defrule, deffacts …
    Token.Keyword.Declaration: "#C792EA",
    Token.Keyword.Type:        "#FFCB6B",   # yellow — slot types
    Token.Name.Builtin:        "#89DDFF",   # cyan — assert, retract, run …
    Token.Name.Variable:       "#F07178",   # red-pink — ?var, $?var
    Token.Literal.String:      "#C3E88D",   # green — "strings"
    Token.Literal.Number:      "#F78C6C",   # orange — numbers
    Token.Comment:             "#546E7A",   # dark grey — ; comments
    Token.Operator:            "#89DDFF",   # cyan — => , =, < …
    Token.Punctuation:         "#EEFFFF",   # white — () brackets
    Token.Name:                "#EEFFFF",   # default text
    Token.Text:                "#EEFFFF",
    Token.Error:               "#FF5370",
}


class ClipsLexer(RegexLexer):
    """Pygments lexer for the CLIPS 6.4 rule language."""

    name = "CLIPS"
    aliases = ["clips", "clp"]
    filenames = ["*.clp"]

    _KEYWORDS = (
        r"defrule|deffacts|deftemplate|defglobal|deffunction|defclass|"
        r"defmessage-handler|defmodule|defrule|definstances"
    )
    _BUILTINS = (
        r"assert|retract|modify|duplicate|reset|run|step|clear|load|save|"
        r"facts|agenda|instances|rules|templates|globals|printout|t|crlf|"
        r"bind|if|then|else|while|do-for-all-facts|do-for-fact|"
        r"not|and|or|test|exists|forall|logical|declare|salience|"
        r"find-fact|find-all-facts|slot|multislot|is-a|type|default|range|"
        r"message-handler|send|make-instance|delete-instance|"
        r"str-cat|str-length|sub-string|upcase|lowcase|sym-cat|"
        r"create\\$|nth\\$|length\\$|member\\$|delete\\$|insert\\$|"
        r"numberp|stringp|symbolp|listp|oddp|evenp|integerp|floatp"
    )

    tokens = {
        "root": [
            # Comments
            (r";.*$", T.Comment),
            # Strings
            (r'"[^"\\]*(?:\\.[^"\\]*)*"', T.Literal.String),
            # Variables  ?var  $?var
            (r"\$?\?[A-Za-z_][A-Za-z0-9_\-]*", T.Name.Variable),
            # Numbers
            (r"-?\d+\.\d+", T.Literal.Number.Float),
            (r"-?\d+", T.Literal.Number.Integer),
            # Keywords (constructs)
            (r"\b(" + _KEYWORDS + r")\b", T.Keyword),
            # Built-in functions / commands
            (r"\b(" + _BUILTINS + r")\b", T.Name.Builtin),
            # Arrow operator
            (r"=>", T.Operator),
            # Comparison / arithmetic / constraint operators
            (r"[<>=!+\-*/&|~:]", T.Operator),
            # Parentheses
            (r"[()]", T.Punctuation),
            # Identifiers
            (r"[A-Za-z_][A-Za-z0-9_\-]*", T.Name),
            # Whitespace
            (r"\s+", T.Text),
            # Anything else
            (r".", T.Error),
        ]
    }


def tokenise(code: str) -> Iterator[tuple[T._TokenType, str]]:
    """Yield (token_type, value) pairs for a CLIPS code string."""
    lexer = ClipsLexer()
    yield from lexer.get_tokens(code)


def apply_highlighting(text_widget, code: str) -> None:
    """
    Apply syntax highlighting tags to a Tkinter/CTk Text widget.

    Existing tags are cleared first. Tag names are derived from token types.
    """
    text_widget.config(state="normal")

    # Remove existing highlight tags
    for tag in text_widget.tag_names():
        if tag.startswith("hl_"):
            text_widget.tag_remove(tag, "1.0", "end")

    # Configure colour tags (idempotent — safe to call every time)
    for token_type, colour in COLOUR_MAP.items():
        tag_name = _tag_name(token_type)
        text_widget.tag_config(tag_name, foreground=colour)

    # Apply tokens
    pos = "1.0"
    for token_type, value in tokenise(code):
        end_pos = _advance_pos(text_widget, pos, value)
        tag = _tag_name(token_type)
        if tag in text_widget.tag_names():
            text_widget.tag_add(tag, pos, end_pos)
        pos = end_pos


def _tag_name(token_type: T._TokenType) -> str:
    """Convert a Pygments token type to a safe Tk tag name."""
    return "hl_" + str(token_type).replace(".", "_").replace(" ", "_")


def _advance_pos(widget, start: str, value: str) -> str:
    """Compute the end position after inserting a value at start."""
    lines = value.split("\n")
    if len(lines) == 1:
        row, col = map(int, start.split("."))
        return f"{row}.{col + len(value)}"
    row = int(start.split(".")[0]) + len(lines) - 1
    return f"{row}.{len(lines[-1])}"
