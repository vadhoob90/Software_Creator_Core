"""Application boundary: resolve, validate and persist one explicit workflow step."""

import json
from pathlib import Path

from .context import resolve
from .contracts import Approval, Contract, Contribution, Job, JobSpec, Role, Stage
from .errors import CoreError
from .evidence import check_contribution, merged_artifacts, validate_artifacts
from .files import digest
from .policy import approve_stage, contribution_stage
from .roles import STAGE_ROLES
from .storage import Store, job_digest


class Workflow:
    """A bounded delivery slice; discovery and architecture templates are available separately."""

    def __init__(self, store: Store, workspace: Path) -> None:
        self.store = store
        self.workspace = workspace.resolve(strict=True)

    def create(self, spec: JobSpec) -> Job:
        if spec.brief.needs_discovery or spec.brief.needs_architecture:
            raise CoreError(
                "brief-not-ready",
                "This delivery slice needs a resolved brief/design.",
                "Complete discovery/architecture with the candidate roles before delivery.",
            )
        job = Job(spec=spec, workspace_digest=digest(str(self.workspace)))
        for role in (Role.ENGINEER, Role.QUALITY, Role.REVIEWER):
            resolve(job, self.workspace, role)
        self.store.append(job, None)
        return job

    def approve(self, job_id: str, actor: str, supplied_digest: str) -> Job:
        job = self.store.load(job_id)
        for role in (Role.ENGINEER, Role.QUALITY, Role.REVIEWER):
            resolve(job, self.workspace, role)
        validate_artifacts(self.workspace, job.artifacts, job.spec.artifact_paths)
        stage = approve_stage(
            job.stage, job.spec.brief.owner, actor, job_digest(job), supplied_digest
        )
        approval = Approval(actor=actor, digest=supplied_digest)
        return self._save(job, stage=stage, approvals=(*job.approvals, approval))

    def submit(self, result: Contribution) -> Job:
        job = self.store.load(result.job_id)
        self._validate_submission(job, result)
        resolved = resolve(job, self.workspace, result.role)
        if result.context_digest != resolved["digest"]:
            raise CoreError(
                "stale-context",
                "Contribution used a different context snapshot.",
                "Export the current role packet before producing a contribution.",
            )
        validate_artifacts(self.workspace, job.artifacts, job.spec.artifact_paths)
        passed = check_contribution(job, result, self.workspace)
        previous = {entry.actor for entry in job.contributions}
        independent = result.actor not in previous and result.actor != job.spec.brief.owner
        stage = contribution_stage(job.stage, result.outcome, independent, passed)
        return self._save(
            job,
            stage=stage,
            contributions=(*job.contributions, result),
            artifacts=merged_artifacts(job, result),
            manifests=(*job.manifests, resolved["manifest"]),
        )

    def cancel(self, job_id: str, actor: str) -> Job:
        job = self.store.load(job_id)
        if job.workspace_digest != digest(str(self.workspace)):
            raise CoreError(
                "workspace-denied",
                "The job belongs to a different workspace.",
                "Use its original workspace.",
            )
        if actor != job.spec.brief.owner or job.stage in (Stage.COMPLETE, Stage.CANCELLED):
            raise CoreError(
                "cancellation-denied",
                "This actor or job state cannot cancel.",
                "Use the job owner on a non-terminal job.",
            )
        return self._save(job, stage=Stage.CANCELLED)

    def _validate_submission(self, job: Job, result: Contribution) -> None:
        if result.revision != job.revision or result.role != STAGE_ROLES.get(job.stage):
            raise CoreError(
                "stale-submission",
                "Role or revision does not match the current job.",
                "Inspect the current stage and export a fresh packet.",
            )
        if len(job.contributions) >= job.spec.max_submissions:
            raise CoreError(
                "submission-limit",
                "The job submission budget is exhausted.",
                "Stop and review the job before authorising further work.",
            )

    def _save(self, old: Job, **changes: object) -> Job:
        data = old.model_dump(mode="json")
        data.update(changes)
        data["revision"] = old.revision + 1
        # Revalidate changes, including enums and tuples, through the persisted JSON contract.
        updated = Job.model_validate_json(json.dumps(data, default=_serialize))
        self.store.append(updated, old.revision)
        return updated


def _serialize(value: object) -> object:
    if isinstance(value, Contract):
        return value.model_dump(mode="json")
    raise TypeError("Unsupported state value")
