from __future__ import annotations

import httpx


def test_remove_value_removes_only_first_match_and_preserves_order() -> None:
    original = httpx.QueryParams([("a", 1), ("b", 2), ("a", 1), ("a", 3)])

    changed = original.remove_value("a", 1)

    assert changed.multi_items() == [("b", "2"), ("a", "1"), ("a", "3")]
    assert original.multi_items() == [
        ("a", "1"),
        ("b", "2"),
        ("a", "1"),
        ("a", "3"),
    ]


def test_remove_value_uses_existing_coercion_rules() -> None:
    assert httpx.QueryParams({"flag": True}).remove_value("flag", True) == httpx.QueryParams()
    assert httpx.QueryParams({"empty": None}).remove_value("empty", None) == httpx.QueryParams()


def test_missing_value_returns_independent_equal_object() -> None:
    original = httpx.QueryParams("a=1&b=2")

    changed = original.remove_value("a", "missing")

    assert changed == original
    assert changed is not original
