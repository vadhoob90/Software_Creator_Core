"""Exhaustive transition and approval checks, including exact failure contracts."""

import pytest

from software_creator_core.contracts import Stage
from software_creator_core.errors import CoreError
from software_creator_core.policy import NEXT_STAGE, approve_stage, contribution_stage


@pytest.mark.parametrize(
    "stage,next_stage",
    [
        (Stage.COMMITMENT, Stage.IMPLEMENT),
        (Stage.ACCEPT, Stage.COMPLETE),
    ],
)
def test_owner_approval(stage, next_stage):
    assert approve_stage(stage, "owner", "owner", "digest", "digest") == next_stage


@pytest.mark.parametrize(
    "actor,supplied", [("other", "digest"), ("owner", "old"), ("other", "old")]
)
def test_denied_approval(actor, supplied):
    with pytest.raises(CoreError) as caught:
        approve_stage(Stage.COMMITMENT, "owner", actor, "digest", supplied)
    assert caught.value.as_dict() == {
        "outcome": "failure",
        "code": "approval-denied",
        "message": "Approval does not match owner and snapshot.",
        "remedy": "Inspect the job and approve its current digest as its owner.",
    }


@pytest.mark.parametrize("stage", list(set(Stage) - {Stage.COMMITMENT, Stage.ACCEPT}))
def test_wrong_approval_stage(stage):
    with pytest.raises(CoreError) as caught:
        approve_stage(stage, "owner", "owner", "digest", "digest")
    assert caught.value.as_dict() == {
        "outcome": "failure",
        "code": "invalid-transition",
        "message": "This stage cannot be approved.",
        "remedy": "Inspect the job stage.",
    }


def test_transition_inventory():
    assert NEXT_STAGE == {
        Stage.IMPLEMENT: Stage.VERIFY,
        Stage.VERIFY: Stage.REVIEW,
        Stage.REVIEW: Stage.ACCEPT,
    }


@pytest.mark.parametrize("stage,expected", list(NEXT_STAGE.items()))
@pytest.mark.parametrize("outcome", ["success", "partial", "degraded", "failure", "cancelled"])
@pytest.mark.parametrize("passed", [True, False])
def test_contribution_outcomes(stage, expected, outcome, passed):
    if outcome == "cancelled":
        expected = Stage.CANCELLED
    elif outcome != "success" or not passed:
        expected = Stage.FAILED
    assert contribution_stage(stage, outcome, True, passed) == expected


@pytest.mark.parametrize("stage", list(set(Stage) - set(NEXT_STAGE)))
def test_illegal_contribution(stage):
    with pytest.raises(CoreError) as caught:
        contribution_stage(stage, "success", True, True)
    assert caught.value.as_dict() == {
        "outcome": "failure",
        "code": "invalid-transition",
        "message": "No contribution is due at this stage.",
        "remedy": "Inspect the job and follow its next action.",
    }


def test_self_approval_is_never_allowed():
    with pytest.raises(CoreError) as caught:
        contribution_stage(Stage.REVIEW, "success", False, True)
    assert caught.value.as_dict() == {
        "outcome": "failure",
        "code": "independence-denied",
        "message": "A contributor cannot approve their own work.",
        "remedy": "Use a distinct reviewer or verifier identity.",
    }
