"""Deterministic context packets; manifests keep hashes instead of private source copies."""

from pathlib import Path
from typing import Any

from . import __version__
from .contracts import Job, Role
from .errors import CoreError
from .files import digest, file_digest, read_artifact
from .roles import BASELINE, STANDARDS, role_definition

SOURCE_ORDER = ("profile", "specialisation", "learning", "task")


def source_layers(job: Job, root: Path, role: Role) -> list[dict[str, Any]]:
    layers: list[dict[str, Any]] = []
    for kind in SOURCE_ORDER:
        selected = [s for s in job.spec.sources if s.kind == kind and s.role == role]
        if not selected:
            layers.append({"kind": kind, "status": "skipped", "reason": "not-selected-for-role"})
        for source in selected:
            if source.approved_by != job.spec.brief.owner:
                raise CoreError(
                    "context-denied",
                    "Context lacks owner approval.",
                    "Have the brief owner approve each selected source.",
                )
            if file_digest(root, source.path) != source.sha256:
                raise CoreError(
                    "stale-context",
                    "A pinned context source has changed.",
                    "Create a new job with the reviewed source digest.",
                )
            layers.append({**source.model_dump(mode="json"), "status": "loaded"})
    return layers


def resolve(job: Job, root: Path, role: Role) -> dict[str, Any]:
    """Preview role context without writing files or invoking a host."""
    if job.workspace_digest != digest(str(root.resolve())):
        raise CoreError(
            "workspace-denied",
            "The job belongs to a different workspace.",
            "Use the original workspace or create a separate job.",
        )
    definition = role_definition(role)
    layers = [
        {"kind": "core-harness", "status": "loaded", "sha256": digest(BASELINE)},
        {"kind": "standards", "status": "loaded", "sha256": digest(STANDARDS)},
        {"kind": "role", "status": "loaded", "sha256": digest(definition)},
        *source_layers(job, root, role),
    ]
    manifest = {
        "schema_version": "1",
        "workspace_digest": job.workspace_digest,
        "core_version": __version__,
        "job_id": job.spec.job_id,
        "revision": job.revision,
        "role": role.value,
        "brief_sha256": digest(job.spec.brief.model_dump(mode="json")),
        "artifacts": [a.model_dump(mode="json") for a in job.artifacts],
        "layers": layers,
        "authority": {"host_mode": "handoff", "publish": False, "paid_api": False},
        "limits": {"max_submissions": job.spec.max_submissions},
    }
    return {"manifest": manifest, "digest": digest(manifest)}


def packet(job: Job, root: Path, role: Role) -> dict[str, Any]:
    """Return private prompt material separately from the hash-only manifest."""
    resolved = resolve(job, root, role)
    selected = [s for s in job.spec.sources if s.role == role]
    return {
        **resolved,
        "baseline": BASELINE,
        "standards": STANDARDS,
        "definition": role_definition(role),
        "brief": job.spec.brief.model_dump(mode="json"),
        "context_data": [
            {"source": s.path, "text": read_artifact(root, s.path).decode("utf-8")}
            for s in selected
        ],
        "artifact_paths": list(job.spec.artifact_paths),
    }
