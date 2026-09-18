"""Exercise the whole Core workflow with synthetic contributors and real local checks."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from software_creator_core.context import resolve
from software_creator_core.contracts import Artifact, Contribution, Evidence, JobSpec
from software_creator_core.files import file_digest
from software_creator_core.roles import STAGE_ROLES
from software_creator_core.service import Workflow
from software_creator_core.storage import Store, job_digest


def submit(workflow, job, path):
    role = STAGE_ROLES[job.stage]
    artifact = Artifact(path=path, sha256=file_digest(workflow.workspace, path))
    result = Contribution(
        schema_version="1",
        job_id=job.spec.job_id,
        revision=job.revision,
        context_digest=resolve(job, workflow.workspace, role)["digest"],
        role=role,
        actor=role.value,
        host="replay",
        model="synthetic-example-v1",
        outcome="success",
        summary="Scripted demonstration contribution, not a model capability claim.",
        artifacts=(artifact,),
        evidence=(
            Evidence(criterion=job.spec.brief.acceptance[0], result="pass", artifact=artifact),
        ),
    )
    return workflow.submit(result)


def demonstrate(root, spec):
    workflow = Workflow(Store(root / "jobs.sqlite3"), root)
    job = workflow.create(spec)
    job = workflow.approve(spec.job_id, spec.brief.owner, job_digest(job))
    (root / "calculator.py").write_text("def add(a, b):\n    return a + b\n")
    job = submit(workflow, job, "calculator.py")
    test = subprocess.run(
        [
            sys.executable,
            "-I",
            "-c",
            "exec(open('calculator.py').read()); "
            "assert add(2, 3) == 5; assert add(-3, 1) == -2; print('PASS: adds integers')",
        ],
        cwd=root,
        capture_output=True,
        text=True,
        timeout=5,
        check=True,
    )
    (root / "verification.txt").write_text(test.stdout)
    job = submit(workflow, job, "verification.txt")
    (root / "review.md").write_text(
        "Synthetic reviewer fixture: narrow implementation; tests pass."
    )
    job = submit(workflow, job, "review.md")
    return workflow.approve(spec.job_id, spec.brief.owner, job_digest(job))


def main():
    spec = JobSpec.model_validate_json(Path("examples/job.json").read_text())
    with tempfile.TemporaryDirectory(prefix="software-core-demo-") as directory:
        job = demonstrate(Path(directory), spec)
        print(
            json.dumps(
                {
                    "stage": job.stage.value,
                    "revision": job.revision,
                    "contributors": "synthetic replay",
                    "local_checks": "executed",
                    "artifact_count": len(job.artifacts),
                    "api_calls": False,
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
