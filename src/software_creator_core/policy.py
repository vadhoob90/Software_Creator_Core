"""Pure workflow decisions, independently mutation-tested; no agent can override them."""

from .contracts import Stage
from .errors import CoreError

NEXT_STAGE = {
    Stage.IMPLEMENT: Stage.VERIFY,
    Stage.VERIFY: Stage.REVIEW,
    Stage.REVIEW: Stage.ACCEPT,
}


def approve_stage(stage: Stage, owner: str, actor: str, expected: str, supplied: str) -> Stage:
    """Bind an owner decision to the exact current snapshot; never permit self-release."""
    if actor != owner or supplied != expected:
        raise CoreError(
            "approval-denied",
            "Approval does not match owner and snapshot.",
            "Inspect the job and approve its current digest as its owner.",
        )
    if stage == Stage.COMMITMENT:
        return Stage.IMPLEMENT
    if stage == Stage.ACCEPT:
        return Stage.COMPLETE
    raise CoreError(
        "invalid-transition", "This stage cannot be approved.", "Inspect the job stage."
    )


def contribution_stage(
    stage: Stage, outcome: str, independent: bool, evidence_passed: bool
) -> Stage:
    """Require distinct review actors and passing verification; non-success stays visible."""
    if stage not in NEXT_STAGE:
        raise CoreError(
            "invalid-transition",
            "No contribution is due at this stage.",
            "Inspect the job and follow its next action.",
        )
    if not independent:
        raise CoreError(
            "independence-denied",
            "A contributor cannot approve their own work.",
            "Use a distinct reviewer or verifier identity.",
        )
    if outcome == "cancelled":
        return Stage.CANCELLED
    if outcome != "success" or not evidence_passed:
        return Stage.FAILED
    return NEXT_STAGE[stage]
