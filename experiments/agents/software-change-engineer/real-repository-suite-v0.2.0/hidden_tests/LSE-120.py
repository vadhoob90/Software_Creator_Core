from __future__ import annotations

import pytest

from requests.structures import CaseInsensitiveDict


def test_direct_invalid_key_is_explicit_and_non_mutating() -> None:
    headers = CaseInsensitiveDict({"Accept": "application/json"})

    with pytest.raises(TypeError, match=r"(?i)key.*string.*int"):
        headers[7] = "invalid"  # type: ignore[index]

    assert list(headers.items()) == [("Accept", "application/json")]


@pytest.mark.parametrize(
    "incoming",
    [
        {"Cache-Control": "no-cache", 7: "invalid"},
        [("Cache-Control", "no-cache"), (7, "invalid")],
    ],
)
def test_update_prevalidates_all_keys_atomically(incoming: object) -> None:
    headers = CaseInsensitiveDict({"Accept": "application/json"})

    with pytest.raises(TypeError, match=r"(?i)key.*string.*int"):
        headers.update(incoming)  # type: ignore[arg-type]

    assert list(headers.items()) == [("Accept", "application/json")]


def test_valid_update_keeps_last_casing() -> None:
    headers = CaseInsensitiveDict({"Accept": "application/json"})
    headers.update([("ACCEPT", "text/plain"), ("X-Test", "yes")])

    assert list(headers.items()) == [("ACCEPT", "text/plain"), ("X-Test", "yes")]
