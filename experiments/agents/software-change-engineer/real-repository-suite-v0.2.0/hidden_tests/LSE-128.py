from __future__ import annotations

import pytest

from _pytest.stash import Stash, StashKey


def test_pop_returns_and_removes_typed_value() -> None:
    stash = Stash()
    key = StashKey[str]()
    stash[key] = "value"

    assert stash.pop(key) == "value"
    assert key not in stash
    assert len(stash) == 0


def test_pop_missing_without_default_raises_key_error() -> None:
    stash = Stash()
    key = StashKey[int]()

    with pytest.raises(KeyError):
        stash.pop(key)


def test_pop_missing_distinguishes_explicit_none_default() -> None:
    stash = Stash()
    key = StashKey[int]()

    assert stash.pop(key, None) is None
    assert len(stash) == 0


def test_pop_default_does_not_change_other_values() -> None:
    stash = Stash()
    present = StashKey[int]()
    missing = StashKey[int]()
    stash[present] = 7

    assert stash.pop(missing, "fallback") == "fallback"
    assert stash[present] == 7
