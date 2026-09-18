"""Versioned, strict input and evidence contracts; no I/O or host dependencies."""

from enum import StrEnum
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

Text = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=8000)]
Identifier = Annotated[str, StringConstraints(pattern=r"^[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}$")]
Digest = Annotated[str, StringConstraints(pattern=r"^[a-f0-9]{64}$")]


class Contract(BaseModel):
    """Reject unknown fields so future/incorrect contracts never silently downgrade."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)


class Role(StrEnum):
    PRODUCT = "product-manager"
    ARCHITECT = "software-architect"
    ENGINEER = "software-engineer"
    QUALITY = "quality-engineer"
    REVIEWER = "code-reviewer"


class Stage(StrEnum):
    COMMITMENT = "awaiting-commitment"
    IMPLEMENT = "implementation"
    VERIFY = "verification"
    REVIEW = "review"
    ACCEPT = "awaiting-acceptance"
    COMPLETE = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Brief(Contract):
    schema_version: Literal["1"] = "1"
    request: Text
    owner: Identifier
    problem: Text
    desired_outcome: Text
    acceptance: Annotated[tuple[Text, ...], Field(min_length=1, max_length=30)]
    constraints: Annotated[tuple[Text, ...], Field(min_length=1, max_length=30)]
    non_goals: Annotated[tuple[Text, ...], Field(min_length=1, max_length=30)]
    evidence: Annotated[tuple[Text, ...], Field(min_length=1, max_length=30)]
    stopping_conditions: Annotated[tuple[Text, ...], Field(min_length=1, max_length=30)]
    risk: Literal["standard", "elevated", "critical"] = "standard"
    needs_discovery: bool = False
    needs_architecture: bool = False


class Source(Contract):
    """Explicitly selected context; references are relative to a caller-owned workspace."""

    kind: Literal["profile", "specialisation", "learning", "task"]
    path: Text
    sha256: Digest
    role: Role
    version: Text
    approved_by: Identifier


class JobSpec(Contract):
    schema_version: Literal["1"] = "1"
    job_id: Identifier
    brief: Brief
    sources: tuple[Source, ...] = ()
    artifact_paths: Annotated[tuple[Text, ...], Field(min_length=1, max_length=100)]
    max_submissions: Annotated[int, Field(ge=3, le=30)] = 8


class Artifact(Contract):
    path: Text
    sha256: Digest


class Evidence(Contract):
    """A cited observation; executable logs remain caller-owned artifacts."""

    criterion: Text
    result: Literal["pass", "fail"]
    artifact: Artifact


class Contribution(Contract):
    schema_version: Literal["1"]
    job_id: Identifier
    revision: Annotated[int, Field(ge=0)]
    context_digest: Digest
    role: Role
    actor: Identifier
    host: Literal["codex", "claude-code", "human", "replay"]
    model: Text
    outcome: Literal["success", "partial", "degraded", "failure", "cancelled"]
    summary: Text
    artifacts: Annotated[tuple[Artifact, ...], Field(max_length=100)]
    evidence: Annotated[tuple[Evidence, ...], Field(max_length=100)]

    @model_validator(mode="after")
    def require_success_artifacts(self) -> "Contribution":
        if self.outcome == "success" and not self.artifacts:
            raise ValueError("Success requires at least one inspectable artifact")
        return self


class Approval(Contract):
    actor: Identifier
    digest: Digest


class Job(Contract):
    """One atomic persisted snapshot, with a bounded append-only contribution history."""

    schema_version: Literal["1"] = "1"
    spec: JobSpec
    workspace_digest: Digest
    stage: Stage = Stage.COMMITMENT
    revision: Annotated[int, Field(ge=0)] = 0
    contributions: tuple[Contribution, ...] = ()
    approvals: tuple[Approval, ...] = ()
    artifacts: tuple[Artifact, ...] = ()
    manifests: tuple[dict[str, Any], ...] = ()
