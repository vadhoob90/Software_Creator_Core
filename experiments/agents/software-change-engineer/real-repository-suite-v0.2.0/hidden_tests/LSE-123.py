from __future__ import annotations

import io

import pytest

from click._termui_impl import ProgressBar


@pytest.mark.parametrize("steps", [0, -1])
def test_update_threshold_must_be_positive(steps: int) -> None:
    with pytest.raises(ValueError, match=r"update_min_steps.*positive|at least 1"):
        ProgressBar(range(3), update_min_steps=steps, hidden=True)


def test_finish_flushes_partial_batch_once() -> None:
    bar = ProgressBar(
        range(10),
        update_min_steps=3,
        hidden=True,
        file=io.StringIO(),
    )
    bar.update(2)

    assert bar.pos == 0
    bar.finish()

    assert bar.pos == 2
    assert bar.finished is True
    assert bar._completed_intervals == 0

    bar.finish()
    assert bar.pos == 2


def test_threshold_update_is_not_reapplied_at_finish() -> None:
    bar = ProgressBar(range(10), update_min_steps=3, hidden=True, file=io.StringIO())
    bar.update(3)
    bar.finish()

    assert bar.pos == 3
