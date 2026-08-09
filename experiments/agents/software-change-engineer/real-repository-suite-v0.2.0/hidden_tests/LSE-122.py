from __future__ import annotations

from click._compat import strip_ansi, term_len
from click.utils import _make_default_short_help


RED = "\x1b[31m"
RESET = "\x1b[0m"


def test_styled_help_below_visible_limit_is_not_truncated() -> None:
    value = f"{RED}Deploy safely{RESET}"

    assert _make_default_short_help(value, 13) == value


def test_styled_help_uses_visible_width_at_truncation_boundary() -> None:
    value = f"{RED}Deploy{RESET} safely to production now"
    result = _make_default_short_help(value, 18)

    assert strip_ansi(result) == "Deploy safely..."
    assert RED in result and RESET in result
    assert term_len(result) <= 18


def test_sentence_ending_semantics_survive_styling() -> None:
    value = f"{RED}Deploy safely.{RESET} More detail follows"
    result = _make_default_short_help(value, 20)

    assert strip_ansi(result) == "Deploy safely."
    assert result.endswith(RESET)
