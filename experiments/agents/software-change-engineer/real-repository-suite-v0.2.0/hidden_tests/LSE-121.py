from __future__ import annotations

import pytest

from requests.hooks import dispatch_hook


def test_invalid_hook_collection_is_validated_before_execution() -> None:
    calls: list[str] = []

    def first(value: str) -> str:
        calls.append(value)
        return value + "-changed"

    with pytest.raises(TypeError, match=r"response.*1"):
        dispatch_hook("response", {"response": [first, object()]}, "original")

    assert calls == []


def test_generator_hooks_remain_ordered_and_none_preserves_value() -> None:
    def hooks():
        yield lambda value: value + "-first"
        yield lambda value: None
        yield lambda value: value + "-last"

    assert (
        dispatch_hook("response", {"response": hooks()}, "original")
        == "original-first-last"
    )


def test_single_callable_remains_supported() -> None:
    assert dispatch_hook("response", {"response": lambda value: value.upper()}, "ok") == "OK"
