import json
import sqlite3

import pytest
from hypothesis import given
from hypothesis import strategies as st
from pydantic import ValidationError

from software_creator_core.context import packet, resolve
from software_creator_core.contracts import JobSpec, Role, Source
from software_creator_core.errors import CoreError
from software_creator_core.files import digest, file_digest, read_artifact
from software_creator_core.hosts import availability, handoff
from software_creator_core.service import Workflow
from software_creator_core.storage import Store, job_digest

from .conftest import contribution


@pytest.mark.parametrize("path", ["../secret", "/etc/passwd", "a/../../secret", "a\\secret", ""])
def test_unsafe_paths(tmp_path, path):
    with pytest.raises(CoreError, match="relative"):
        read_artifact(tmp_path, path)


def test_symlinks_missing_and_limits(tmp_path):
    (tmp_path / "real").write_text("safe")
    (tmp_path / "link").symlink_to(tmp_path / "real")
    with pytest.raises(CoreError, match="Symbolic"):
        read_artifact(tmp_path, "link")
    with pytest.raises(CoreError, match="regular"):
        read_artifact(tmp_path, "absent")
    (tmp_path / "large").write_bytes(b"x" * 256001)
    with pytest.raises(CoreError, match="size"):
        read_artifact(tmp_path, "large")


@given(st.dictionaries(st.text(max_size=30), st.integers(), max_size=10))
def test_digest_does_not_depend_on_mapping_order(value):
    assert digest(value) == digest(dict(reversed(list(value.items()))))
    assert len(digest(value)) == 64


def test_contract_rejects_unknown_and_future_fields(spec):
    for changes in ({"schema_version": "2"}, {"paid_api": True}, {"job_id": "../escape"}):
        with pytest.raises(ValidationError):
            JobSpec.model_validate_json(json.dumps({**spec.model_dump(mode="json"), **changes}))


def test_success_cannot_have_no_artifacts(workflow, active):
    with pytest.raises(ValidationError, match="inspectable"):
        contribution(workflow, active, artifacts=[])
    assert contribution(workflow, active, outcome="failure", artifacts=[]).outcome == "failure"


def test_context_pins_selected_role_sources(workflow, spec):
    path = workflow.workspace / "profile.md"
    path.write_text("Private profile: never publish.")
    source = Source(
        kind="profile",
        path="profile.md",
        sha256=file_digest(workflow.workspace, path.name),
        role=Role.ENGINEER,
        version="1",
        approved_by="owner",
    )
    selected = spec.model_copy(update={"sources": (source,)})
    job = workflow.create(selected)
    resolved = resolve(job, workflow.workspace, Role.ENGINEER)
    assert "Private profile" not in json.dumps(resolved)
    assert packet(job, workflow.workspace, Role.ENGINEER)["context_data"][0]["text"].startswith(
        "Private"
    )
    assert packet(job, workflow.workspace, Role.REVIEWER)["context_data"] == []
    path.write_text("Changed profile")
    with pytest.raises(CoreError, match="changed"):
        resolve(job, workflow.workspace, Role.ENGINEER)


def test_unapproved_context_rejected(workflow, spec):
    source = Source(
        kind="learning",
        path="profile.md",
        sha256="0" * 64,
        role=Role.ENGINEER,
        version="1",
        approved_by="other",
    )
    with pytest.raises(CoreError, match="approval"):
        workflow.create(spec.model_copy(update={"sources": (source,)}))


def test_host_handoffs_are_equivalent_except_host_status(workflow, active, monkeypatch):
    monkeypatch.setattr("software_creator_core.hosts.shutil.which", lambda _: None)
    codex = handoff(active, workflow.workspace, Role.ENGINEER, "codex")
    claude = handoff(active, workflow.workspace, Role.ENGINEER, "claude-code")
    assert codex["packet"] == claude["packet"]
    assert codex["response_schema"] == claude["response_schema"]
    assert not claude["status"]["installed"]
    monkeypatch.setattr("software_creator_core.hosts.shutil.which", lambda _: "/bin/host")
    assert availability("codex")["installed"]
    assert availability("codex")["authentication"] == "not-checked"


def test_store_missing_duplicate_and_stale_writer(workflow, spec):
    with pytest.raises(CoreError, match="store"):
        workflow.store.load("unknown")
    job = workflow.create(spec)
    with pytest.raises(CoreError, match="already exists"):
        workflow.create(spec)
    with pytest.raises(CoreError, match="does not exist"):
        workflow.store.load("unknown")
    with pytest.raises(CoreError, match="already exists"):
        workflow.store.append(job.model_copy(update={"revision": 3}), 0)
    assert workflow.store.load(spec.job_id) == job


@pytest.mark.parametrize("corruption", ["digest", "payload", "identity"])
def test_corruption_is_not_silently_repaired(workflow, active, corruption):
    with sqlite3.connect(workflow.store.path) as db:
        if corruption == "digest":
            db.execute("UPDATE snapshots SET digest = 'bad'")
        elif corruption == "payload":
            db.execute("UPDATE snapshots SET payload = '{}'")
        else:
            db.execute("UPDATE snapshots SET job_id = 'wrong'")
    with pytest.raises(CoreError, match="invalid|contract"):
        workflow.store.load("wrong" if corruption == "identity" else active.spec.job_id)


def test_sql_errors_are_explicit_and_transactions_rollback(workflow, active):
    with pytest.raises(CoreError, match="transaction"), workflow.store.connection() as db:
        db.execute("UPDATE snapshots SET digest = 'bad'")
        db.execute("SELECT * FROM does_not_exist")
    assert workflow.store.load(active.spec.job_id) == active


def test_symlink_store_denied(tmp_path):
    target = tmp_path / "target"
    target.touch()
    link = tmp_path / "db"
    link.symlink_to(target)
    with pytest.raises(CoreError, match="symbolic"):
        Store(link).load("test")


def test_workspace_cannot_be_rebound(workflow, active, tmp_path):
    other = tmp_path / "other"
    other.mkdir()
    wrong = Workflow(workflow.store, other)
    with pytest.raises(CoreError, match="different workspace"):
        wrong.approve(active.spec.job_id, "owner", job_digest(active))
    with pytest.raises(CoreError, match="different workspace"):
        wrong.cancel(active.spec.job_id, "owner")


def test_concurrent_writers_cannot_both_commit(workflow, active):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier

    barrier = Barrier(2)

    def append():
        barrier.wait(timeout=3)
        try:
            workflow.store.append(active.model_copy(update={"revision": 2}), 1)
        except CoreError as exc:
            return exc.code
        return "committed"

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: append(), range(2)))
    assert sorted(results) == ["committed", "revision-conflict"]
