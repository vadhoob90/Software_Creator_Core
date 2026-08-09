from __future__ import annotations

import math

import pytest

from _pytest import timing


@pytest.mark.parametrize("duration", [-1, -0.5, math.nan, math.inf, -math.inf])
def test_invalid_sleep_is_rejected_without_clock_change(duration: float) -> None:
    clock = timing.MockTiming()
    before = clock.time()

    with pytest.raises(ValueError, match=r"(?i)(finite|non-negative|duration)"):
        clock.sleep(duration)

    assert clock.time() == before


@pytest.mark.parametrize("duration", [0, 1, 1.5])
def test_valid_sleep_remains_deterministic(duration: float) -> None:
    clock = timing.MockTiming()
    before = clock.time()

    clock.sleep(duration)

    assert clock.time() == before + duration


def test_rejected_sleep_cannot_make_elapsed_negative(monkeypatch) -> None:
    clock = timing.MockTiming()
    clock.patch(monkeypatch)
    start = timing.Instant()

    with pytest.raises(ValueError):
        clock.sleep(-5)

    assert start.elapsed().seconds >= 0
