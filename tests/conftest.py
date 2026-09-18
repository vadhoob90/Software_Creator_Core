"""Synthetic local workspaces; never read production repositories or credentials."""

import json

import pytest

from software_creator_core.context import resolve
from software_creator_core.contracts import Artifact, Brief, Contribution, Evidence, JobSpec
from software_creator_core.files import file_digest
from software_creator_core.roles import STAGE_ROLES
from software_creator_core.service import Workflow
from software_creator_core.storage import Store, job_digest


@pytest.fixture
def spec():
    return JobSpec(
        job_id="addition",
        brief=Brief(
            request="Implement integer addition",
            owner="owner",
            problem="Missing addition",
            desired_outcome="Correct integer addition",
            acceptance=("adds integers",),
            constraints=("No network",),
            non_goals=("No deployment",),
            evidence=("Human request",),
            stopping_conditions=("Unresolved ambiguity",),
        ),
        artifact_paths=("result.py", "checks.txt", "review.md"),
    )


@pytest.fixture
def workflow(tmp_path):
    (tmp_path / "result.py").write_text("def add(a, b):\n    return a + b\n")
    (tmp_path / "checks.txt").write_text("Independent test run: pass\n")
    (tmp_path / "review.md").write_text("Independent review: pass\n")
    return Workflow(Store(tmp_path / "jobs.sqlite3"), tmp_path)


@pytest.fixture
def active(workflow, spec):
    job = workflow.create(spec)
    return workflow.approve(spec.job_id, "owner", job_digest(job))


def contribution(workflow, job, **changes):
    role = STAGE_ROLES[job.stage]
    path = {
        "software-engineer": "result.py",
        "quality-engineer": "checks.txt",
        "code-reviewer": "review.md",
    }[role.value]
    artifact = Artifact(path=path, sha256=file_digest(workflow.workspace, path))
    result = Contribution(
        schema_version="1",
        job_id=job.spec.job_id,
        revision=job.revision,
        context_digest=resolve(job, workflow.workspace, role)["digest"],
        role=role,
        actor=role.value,
        host="replay",
        model="deterministic-test-v1",
        outcome="success",
        summary="Synthetic evidence",
        artifacts=(artifact,),
        evidence=(Evidence(criterion="adds integers", result="pass", artifact=artifact),),
    )
    data = result.model_dump(mode="json")
    data.update(changes)
    return Contribution.model_validate_json(json.dumps(data))
