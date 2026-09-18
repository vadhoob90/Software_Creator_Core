"""Stable error codes, explanations and remediation are part of the public contract."""

import sqlite3

import pytest

from software_creator_core.context import resolve
from software_creator_core.contracts import Role, Source
from software_creator_core.errors import CoreError
from software_creator_core.files import file_digest, read_artifact
from software_creator_core.service import Workflow
from software_creator_core.storage import Store, job_digest

from .conftest import contribution


def assert_failure(action, code, message, remedy):
    with pytest.raises(CoreError) as caught:
        action()
    assert caught.value.as_dict() == {
        "outcome": "failure",
        "code": code,
        "message": message,
        "remedy": remedy,
    }


@pytest.mark.parametrize(
    "path,code,message,remedy",
    [
        (
            "../escape",
            "unsafe-path",
            "Expected a workspace-relative file path.",
            "Use a regular file inside the declared workspace.",
        ),
        (
            "missing",
            "missing-artifact",
            "A declared artifact is not a regular file.",
            "Create the required artifact before submitting evidence.",
        ),
        (
            "link",
            "unsafe-path",
            "Symbolic links are not valid evidence sources.",
            "Select an ordinary workspace file.",
        ),
        (
            "large",
            "input-limit",
            "An artifact exceeds the size limit.",
            "Provide a focused artifact under 256 KB.",
        ),
    ],
)
def test_file_errors(tmp_path, path, code, message, remedy):
    (tmp_path / "link").symlink_to(tmp_path / "missing")
    (tmp_path / "large").write_bytes(b"x" * 256001)
    assert_failure(lambda: read_artifact(tmp_path, path), code, message, remedy)


def test_service_errors(workflow, active):
    result = contribution(workflow, active)
    assert_failure(
        lambda: workflow.submit(result.model_copy(update={"context_digest": "0" * 64})),
        "stale-context",
        "Contribution used a different context snapshot.",
        "Export the current role packet before producing a contribution.",
    )
    assert_failure(
        lambda: workflow.submit(result.model_copy(update={"revision": 0})),
        "stale-submission",
        "Role or revision does not match the current job.",
        "Inspect the current stage and export a fresh packet.",
    )
    assert_failure(
        lambda: workflow.cancel(active.spec.job_id, "wrong"),
        "cancellation-denied",
        "This actor or job state cannot cancel.",
        "Use the job owner on a non-terminal job.",
    )
    other = workflow.workspace / "other"
    other.mkdir()
    wrong = Workflow(workflow.store, other)
    assert_failure(
        lambda: wrong.cancel(active.spec.job_id, "owner"),
        "workspace-denied",
        "The job belongs to a different workspace.",
        "Use its original workspace.",
    )
    assert_failure(
        lambda: wrong.approve(active.spec.job_id, "owner", job_digest(active)),
        "workspace-denied",
        "The job belongs to a different workspace.",
        "Use the original workspace or create a separate job.",
    )


def test_creation_and_context_errors(workflow, spec):
    unready = spec.model_copy(
        update={"brief": spec.brief.model_copy(update={"needs_discovery": True})}
    )
    assert_failure(
        lambda: workflow.create(unready),
        "brief-not-ready",
        "This delivery slice needs a resolved brief/design.",
        "Complete discovery/architecture with the candidate roles before delivery.",
    )
    source = Source(
        kind="profile",
        path="checks.txt",
        sha256=file_digest(workflow.workspace, "checks.txt"),
        role=Role.ENGINEER,
        version="1",
        approved_by="wrong",
    )
    assert_failure(
        lambda: workflow.create(spec.model_copy(update={"sources": (source,)})),
        "context-denied",
        "Context lacks owner approval.",
        "Have the brief owner approve each selected source.",
    )
    job = workflow.create(
        spec.model_copy(update={"sources": (source.model_copy(update={"approved_by": "owner"}),)})
    )
    (workflow.workspace / "checks.txt").write_text("changed")
    assert_failure(
        lambda: resolve(job, workflow.workspace, Role.ENGINEER),
        "stale-context",
        "A pinned context source has changed.",
        "Create a new job with the reviewed source digest.",
    )


def test_evidence_errors(workflow, active):
    result = contribution(workflow, active)
    bad = result.artifacts[0].model_copy(update={"path": "other.txt"})
    assert_failure(
        lambda: workflow.submit(result.model_copy(update={"artifacts": (bad,)})),
        "artifact-denied",
        "An artifact is outside the declared scope.",
        "Use only paths listed in the approved job.",
    )
    bad = result.artifacts[0].model_copy(update={"sha256": "0" * 64})
    assert_failure(
        lambda: workflow.submit(result.model_copy(update={"artifacts": (bad,)})),
        "stale-evidence",
        "An artifact no longer matches its evidence digest.",
        "Start a new job for changed inputs or restore the exact reviewed files.",
    )


def test_storage_errors(workflow, spec):
    assert_failure(
        lambda: workflow.store.load("missing"),
        "missing-store",
        "The job store does not exist.",
        "Create a job first.",
    )
    workflow.create(spec)
    assert_failure(
        lambda: workflow.store.load("missing"),
        "missing-job",
        "The requested job does not exist.",
        "Check the job ID.",
    )
    assert_failure(
        lambda: workflow.create(spec),
        "revision-conflict",
        "The job changed or already exists.",
        "Reload the job; do not replay an old approval or contribution.",
    )
    (workflow.workspace / "link.sqlite3").symlink_to(workflow.store.path)
    assert_failure(
        lambda: Store(workflow.workspace / "link.sqlite3").load("missing"),
        "unsafe-store",
        "Store must not be a symbolic link.",
        "Select an ordinary local database file.",
    )


def test_corruption_errors(workflow, active):
    with sqlite3.connect(workflow.store.path) as db:
        db.execute("UPDATE snapshots SET digest='bad'")
    assert_failure(
        lambda: workflow.store.load(active.spec.job_id),
        "corrupt-state",
        "The stored job digest or identity is invalid.",
        "Restore a verified backup and retain the corrupt file for investigation.",
    )
    with sqlite3.connect(workflow.store.path) as db:
        db.execute("UPDATE snapshots SET payload='{}'")
    assert_failure(
        lambda: workflow.store.load(active.spec.job_id),
        "corrupt-state",
        "The stored job violates its contract.",
        "Restore a verified database backup; do not overwrite this record.",
    )


def test_database_failure_contract(workflow, active):
    def invalid_query():
        with workflow.store.connection() as db:
            db.execute("SELECT * FROM absent_table")

    assert_failure(
        invalid_query,
        "store-failure",
        "The job transaction could not be committed.",
        "Check the database and retry from the last durable revision.",
    )


def test_database_open_failure_is_redacted(tmp_path, spec):
    workflow = Workflow(Store(tmp_path / "private-missing-parent" / "jobs.sqlite3"), tmp_path)
    assert_failure(
        lambda: workflow.create(spec),
        "store-failure",
        "The job transaction could not be committed.",
        "Check the database and retry from the last durable revision.",
    )
