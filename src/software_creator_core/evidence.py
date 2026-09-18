"""Validate file evidence, scope and acceptance before a workflow can advance."""

from pathlib import Path

from .contracts import Artifact, Contribution, Job, Stage
from .errors import CoreError
from .files import file_digest


def validate_artifacts(
    root: Path, artifacts: tuple[Artifact, ...], allowed: tuple[str, ...]
) -> None:
    for artifact in artifacts:
        if artifact.path not in allowed:
            raise CoreError(
                "artifact-denied",
                "An artifact is outside the declared scope.",
                "Use only paths listed in the approved job.",
            )
        if file_digest(root, artifact.path) != artifact.sha256:
            raise CoreError(
                "stale-evidence",
                "An artifact no longer matches its evidence digest.",
                "Start a new job for changed inputs or restore the exact reviewed files.",
            )


def check_contribution(job: Job, result: Contribution, root: Path) -> bool:
    """A cited passing log is evidence, not a claim that Core executed that log's commands."""
    artifacts = result.artifacts + tuple(e.artifact for e in result.evidence)
    validate_artifacts(root, artifacts, job.spec.artifact_paths)
    if job.stage == Stage.IMPLEMENT:
        return True
    passed = {entry.criterion for entry in result.evidence if entry.result == "pass"}
    failed = any(entry.result == "fail" for entry in result.evidence)
    return set(job.spec.brief.acceptance) <= passed and not failed


def merged_artifacts(job: Job, result: Contribution) -> tuple[Artifact, ...]:
    records = {artifact.path: artifact for artifact in job.artifacts}
    for artifact in result.artifacts + tuple(e.artifact for e in result.evidence):
        records[artifact.path] = artifact
    return tuple(records[path] for path in sorted(records))
