from __future__ import annotations

import pytest

import httpx


@pytest.mark.parametrize("name", ["X-API-Key", "x-api-key", "API-Key", "api-key"])
def test_api_key_header_repr_is_redacted_without_mutating_value(name: str) -> None:
    headers = httpx.Headers([(name, "first-secret"), (name, "second-secret")])

    rendered = repr(headers)

    assert "first-secret" not in rendered
    assert "second-secret" not in rendered
    assert rendered.count("[secure]") == 2
    assert headers.get_list(name) == ["first-secret", "second-secret"]


def test_byte_api_key_header_is_redacted_without_mutating_raw() -> None:
    headers = httpx.Headers([(b"X-API-Key", b"byte-secret")])

    assert "byte-secret" not in repr(headers)
    assert headers.raw == [(b"X-API-Key", b"byte-secret")]


def test_non_sensitive_header_remains_visible() -> None:
    assert "public-value" in repr(httpx.Headers({"X-Trace": "public-value"}))
