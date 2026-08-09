from __future__ import annotations

import pytest

from rich.measure import Measurement


@pytest.mark.parametrize("method", ["with_minimum", "with_maximum"])
def test_negative_bound_is_rejected_without_mutation(method: str) -> None:
    measurement = Measurement(20, 100)
    bound = method.removeprefix("with_")

    with pytest.raises(
        ValueError,
        match=rf"(?i)({bound}.*(width|negative)|width.*{bound})",
    ):
        getattr(measurement, method)(-1)

    assert measurement == Measurement(20, 100)


def test_contradictory_clamp_is_rejected_without_mutation() -> None:
    measurement = Measurement(20, 100)

    with pytest.raises(ValueError, match=r"80.*50|minimum.*maximum"):
        measurement.clamp(80, 50)

    assert measurement == Measurement(20, 100)


def test_valid_and_none_bounds_remain_compatible() -> None:
    measurement = Measurement(20, 100)

    assert measurement.clamp(30, 50) == Measurement(30, 50)
    assert measurement.clamp(None, 50) == Measurement(20, 50)
    assert measurement.clamp(30, None) == Measurement(30, 100)
    assert measurement.clamp(None, None) == measurement
