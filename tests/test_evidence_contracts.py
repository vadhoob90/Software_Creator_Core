"""Independently specified wire-format and journal invariants, not only happy-path coverage."""

import hashlib
import json
import sqlite3

import pytest

from software_creator_core import __version__
from software_creator_core.context import packet, resolve
from software_creator_core.contracts import Approval, Role, Source, Stage
from software_creator_core.errors import CoreError
from software_creator_core.files import digest, file_digest, read_artifact
from software_creator_core.roles import BASELINE, STANDARDS, role_definition
from software_creator_core.service import Workflow, _serialize
from software_creator_core.storage import job_digest

from .conftest import contribution


def canonical(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    return hashlib.sha256(data).hexdigest()


def test_canonical_digest_contract():
    value = {"z": ["é", 1], "a": {"x": False}}
    assert digest(value) == canonical(value)


def test_full_composition_manifest_and_private_packet(workflow, active):
    role = Role.ENGINEER
    expected = {
        "schema_version": "1",
        "workspace_digest": canonical(str(workflow.workspace)),
        "core_version": __version__,
        "job_id": "addition",
        "revision": 1,
        "role": "software-engineer",
        "brief_sha256": canonical(active.spec.brief.model_dump(mode="json")),
        "artifacts": [],
        "layers": [
            {"kind": "core-harness", "status": "loaded", "sha256": canonical(BASELINE)},
            {"kind": "standards", "status": "loaded", "sha256": canonical(STANDARDS)},
            {"kind": "role", "status": "loaded", "sha256": canonical(role_definition(role))},
            *[
                {"kind": kind, "status": "skipped", "reason": "not-selected-for-role"}
                for kind in ("profile", "specialisation", "learning", "task")
            ],
        ],
        "authority": {"host_mode": "handoff", "publish": False, "paid_api": False},
        "limits": {"max_submissions": 8},
    }
    resolved = resolve(active, workflow.workspace, role)
    assert resolved == {"manifest": expected, "digest": canonical(expected)}
    assert packet(active, workflow.workspace, role) == {
        **resolved,
        "baseline": BASELINE,
        "standards": STANDARDS,
        "definition": role_definition(role),
        "brief": active.spec.brief.model_dump(mode="json"),
        "context_data": [],
        "artifact_paths": ["result.py", "checks.txt", "review.md"],
    }


def test_loaded_layers_and_private_payload_contract(workflow, spec):
    (workflow.workspace / "profile.md").write_text("Selected private evidence é")
    selected = Source(
        kind="profile",
        path="profile.md",
        sha256=file_digest(workflow.workspace, "profile.md"),
        role=Role.ENGINEER,
        version="reviewed-1",
        approved_by="owner",
    )
    job = workflow.create(spec.model_copy(update={"sources": (selected,)}))
    resolved = packet(job, workflow.workspace, Role.ENGINEER)
    assert resolved["manifest"]["layers"][3] == {
        **selected.model_dump(mode="json"),
        "status": "loaded",
    }
    assert resolved["context_data"] == [
        {"source": "profile.md", "text": "Selected private evidence é"}
    ]
    assert len(resolved["manifest"]["layers"]) == 7
    reviewer = resolve(job, workflow.workspace, Role.REVIEWER)
    assert all(layer["status"] == "skipped" for layer in reviewer["manifest"]["layers"][3:])


def test_conflicting_verification_cannot_pass(workflow, active):
    job = workflow.submit(contribution(workflow, active))
    result = contribution(workflow, job)
    conflicting = result.evidence + (result.evidence[0].model_copy(update={"result": "fail"}),)
    assert (
        workflow.submit(result.model_copy(update={"evidence": conflicting})).stage == Stage.FAILED
    )


def test_file_reads_are_bounded(tmp_path, monkeypatch):
    from contextlib import contextmanager
    from pathlib import Path

    target = tmp_path / "input"
    target.write_bytes(b"small input")
    original = Path.open

    @contextmanager
    def bounded_open(path, *args, **kwargs):
        with original(path, *args, **kwargs) as stream:

            class BoundedStream:
                def read(self, size):
                    assert isinstance(size, int) and 0 < size <= 256002
                    return stream.read(size)

            yield BoundedStream()

    monkeypatch.setattr(Path, "open", bounded_open)
    assert read_artifact(tmp_path, "input") == b"small input"


def test_approvals_contributions_and_manifests_are_retained(workflow, active):
    assert len(active.approvals) == 1
    with sqlite3.connect(workflow.store.path) as db:
        original = json.loads(
            db.execute("SELECT payload FROM snapshots WHERE revision=0").fetchone()[0]
        )
    assert active.approvals == (Approval(actor="owner", digest=canonical(original)),)
    initial = active
    for _ in range(3):
        result = contribution(workflow, active)
        manifest = resolve(active, workflow.workspace, result.role)["manifest"]
        updated = workflow.submit(result)
        assert updated.contributions == (*active.contributions, result)
        assert updated.manifests == (*active.manifests, manifest)
        assert updated.approvals == initial.approvals
        active = updated
    accepted = workflow.approve(active.spec.job_id, "owner", job_digest(active))
    assert accepted.approvals == (
        *initial.approvals,
        Approval(actor="owner", digest=job_digest(active)),
    )
    assert accepted.stage == Stage.COMPLETE
    with pytest.raises(CoreError):
        workflow.cancel(accepted.spec.job_id, "owner")
    with sqlite3.connect(workflow.store.path) as db:
        rows = db.execute(
            "SELECT revision,payload,digest FROM snapshots ORDER BY revision"
        ).fetchall()
    assert [row[0] for row in rows] == list(range(6))
    assert all(canonical(json.loads(row[1])) == row[2] for row in rows)


def test_exact_file_size_boundary(tmp_path):
    path = tmp_path / "limit.bin"
    path.write_bytes(b"a" * 256000)
    assert read_artifact(tmp_path, "limit.bin") == b"a" * 256000


def test_workflow_requires_real_workspace(workflow):
    with pytest.raises(FileNotFoundError):
        Workflow(workflow.store, workflow.workspace / "missing")


def test_serialization_contract():
    approval = Approval(actor="human", digest="0" * 64)
    assert _serialize(approval) == {"actor": "human", "digest": "0" * 64}
    with pytest.raises(TypeError, match="^Unsupported state value$"):
        _serialize("not a contract")


def test_budget_boundary(workflow, active):
    result = contribution(workflow, active)
    below = active.model_copy(
        update={"contributions": (result,) * (active.spec.max_submissions - 1)}
    )
    assert workflow._validate_submission(below, result) is None
    above = active.model_copy(
        update={"contributions": (result,) * (active.spec.max_submissions + 1)}
    )
    with pytest.raises(CoreError) as caught:
        workflow._validate_submission(above, result)
    assert caught.value.as_dict() == {
        "outcome": "failure",
        "code": "submission-limit",
        "message": "The job submission budget is exhausted.",
        "remedy": "Stop and review the job before authorising further work.",
    }
