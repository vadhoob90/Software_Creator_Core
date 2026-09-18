import json
import subprocess
import sys

import pytest

from software_creator_core.contracts import JobSpec, Stage
from software_creator_core.errors import CoreError
from software_creator_core.service import Workflow, _serialize
from software_creator_core.storage import Store, job_digest

from .conftest import contribution


def test_complete_workflow_with_real_local_code_execution(workflow, active):
    job = workflow.submit(contribution(workflow, active))
    execution = subprocess.run(
        [
            sys.executable,
            "-I",
            "-c",
            "exec(open('result.py').read()); assert add(2, 3) == 5; "
            "assert add(-3, 3) == 0; print('adds integers: pass')",
        ],
        cwd=workflow.workspace,
        capture_output=True,
        text=True,
        timeout=5,
        check=True,
    )
    (workflow.workspace / "checks.txt").write_text(execution.stdout)
    job = workflow.submit(contribution(workflow, job))
    # Reopen from disk to prove resumption is independent of conversation/process memory.
    reopened = Workflow(Store(workflow.store.path), workflow.workspace)
    job = reopened.submit(contribution(reopened, job))
    assert job.stage == Stage.ACCEPT
    assert len(job.manifests) == 3
    assert len(job.artifacts) == 3
    assert "context_data" not in json.dumps(job.manifests)
    approved = reopened.approve(job.spec.job_id, "owner", job_digest(job))
    assert approved.stage == Stage.COMPLETE
    assert reopened.store.load(job.spec.job_id) == approved


@pytest.mark.parametrize("host", ["codex", "claude-code"])
def test_host_contributions_use_identical_contracts(workflow, active, host):
    job = active
    for _ in range(3):
        job = workflow.submit(contribution(workflow, job, host=host))
    assert job.stage == Stage.ACCEPT
    assert {c.host for c in job.contributions} == {host}


@pytest.mark.parametrize("field", ["needs_discovery", "needs_architecture"])
def test_incomplete_brief_stops_delivery(workflow, spec, field):
    data = spec.model_dump(mode="json")
    data["brief"][field] = True
    with pytest.raises(CoreError, match="resolved brief"):
        workflow.create(JobSpec.model_validate_json(json.dumps(data)))
    assert not workflow.store.path.exists()


@pytest.mark.parametrize(
    "changes",
    [
        {"revision": 0},
        {"role": "code-reviewer"},
        {"context_digest": "0" * 64},
        {"actor": "owner"},
    ],
)
def test_rejects_stale_or_unauthorised_contribution(workflow, active, changes):
    with pytest.raises(CoreError):
        workflow.submit(contribution(workflow, active, **changes))
    assert workflow.store.load(active.spec.job_id) == active


def test_duplicate_submission_is_not_replayed(workflow, active):
    result = contribution(workflow, active)
    committed = workflow.submit(result)
    with pytest.raises(CoreError):
        workflow.submit(result)
    assert workflow.store.load(active.spec.job_id) == committed


def test_distinct_verifier_required(workflow, active):
    job = workflow.submit(contribution(workflow, active))
    with pytest.raises(CoreError, match="own work"):
        workflow.submit(contribution(workflow, job, actor="software-engineer"))


def test_stale_artifact_invalidates_review(workflow, active):
    job = workflow.submit(contribution(workflow, active))
    (workflow.workspace / "result.py").write_text("def add(a, b): return 0\n")
    with pytest.raises(CoreError, match="digest"):
        workflow.submit(contribution(workflow, job))


@pytest.mark.parametrize(
    "evidence",
    [
        [],
        [
            {
                "criterion": "adds integers",
                "result": "fail",
                "artifact": {"path": "checks.txt", "sha256": "placeholder"},
            }
        ],
    ],
)
def test_incomplete_or_failed_verification_is_failure(workflow, active, evidence):
    from software_creator_core.files import file_digest

    job = workflow.submit(contribution(workflow, active))
    if evidence:
        evidence[0]["artifact"]["sha256"] = file_digest(workflow.workspace, "checks.txt")
    failed = workflow.submit(contribution(workflow, job, evidence=evidence))
    assert failed.stage == Stage.FAILED
    with pytest.raises(CoreError):
        workflow.approve(job.spec.job_id, "owner", job_digest(failed))


def test_out_of_scope_artifact_rejected(workflow, active):
    with pytest.raises(CoreError, match="outside"):
        workflow.submit(
            contribution(
                workflow,
                active,
                artifacts=[
                    {
                        "path": "undeclared.txt",
                        "sha256": "0" * 64,
                    }
                ],
            )
        )


def test_cancel_and_repeated_cancellation(workflow, active):
    with pytest.raises(CoreError):
        workflow.cancel(active.spec.job_id, "other")
    job = workflow.cancel(active.spec.job_id, "owner")
    assert job.stage == Stage.CANCELLED
    with pytest.raises(CoreError):
        workflow.cancel(job.spec.job_id, "owner")


def test_budget_is_enforced(workflow, active):
    # Exercise defensive validation on a restored state at the budget boundary.
    result = contribution(workflow, active)
    exhausted = active.model_copy(update={"contributions": (result,) * active.spec.max_submissions})
    with pytest.raises(CoreError, match="budget"):
        workflow._validate_submission(exhausted, result)


def test_unknown_state_value_rejected():
    with pytest.raises(TypeError):
        _serialize(object())
