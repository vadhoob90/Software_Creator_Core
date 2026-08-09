from __future__ import annotations

import pytest

from rich import filesize


@pytest.mark.parametrize(
    ("size", "expected"),
    [
        (0, "0 bytes"),
        (1, "1 byte"),
        (1023, "1,023 bytes"),
        (1024, "1.0 KiB"),
        (1536, "1.5 KiB"),
        (1024**2, "1.0 MiB"),
        (1024**8, "1.0 YiB"),
    ],
)
def test_binary_sizes(size: int, expected: str) -> None:
    assert filesize.binary(size) == expected


def test_binary_precision_and_separator() -> None:
    assert filesize.binary(1536, precision=2, separator="") == "1.50KiB"


@pytest.mark.parametrize("formatter", [filesize.decimal, lambda size: filesize.binary(size)])
def test_negative_sizes_are_explicit(formatter) -> None:
    with pytest.raises(ValueError, match=r"(?i)size.*non-negative"):
        formatter(-1)


def test_binary_is_exported() -> None:
    assert "binary" in filesize.__all__
