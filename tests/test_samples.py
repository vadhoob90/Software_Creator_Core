"""Public examples use disposable local data and execute real, known synthetic code."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

from scripts.demo import demonstrate, submit
from software_creator_core.contracts import JobSpec, Stage
from software_creator_core.service import Workflow
from software_creator_core.storage import Store, job_digest


def test_documented_example_completes(tmp_path):
    spec = JobSpec.model_validate_json(Path("examples/job.json").read_text())
    completed = demonstrate(tmp_path, spec)
    assert completed.stage == Stage.COMPLETE
    assert completed.revision == 5
    assert len(completed.artifacts) == 3
    assert "PASS" in (tmp_path / "verification.txt").read_text()


def test_unrelated_workspace_uses_same_contract_and_harness(tmp_path, spec):
    (tmp_path / "docs").mkdir()
    (tmp_path / "lib").mkdir()
    (tmp_path / "docs" / "existing.md").write_text("Product-owned guidance: retain me.")
    data = spec.model_dump(mode="json")
    data["job_id"] = "normalise-labels"
    data["artifact_paths"] = ["lib/labels.py", "checks.log", "docs/review.txt"]
    data["brief"].update(
        request="Normalise a label",
        problem="Inconsistent labels",
        desired_outcome="Trim and lowercase labels",
        acceptance=["normalises labels"],
    )
    selected = JobSpec.model_validate_json(json.dumps(data))
    workflow = Workflow(Store(tmp_path / "journal.sqlite3"), tmp_path)
    job = workflow.create(selected)
    job = workflow.approve(selected.job_id, selected.brief.owner, job_digest(job))
    (tmp_path / "lib" / "labels.py").write_text(
        "def normalise(text):\n    return text.strip().lower()\n"
    )
    job = submit(workflow, job, "lib/labels.py")
    run = subprocess.run(
        [
            sys.executable,
            "-I",
            "-c",
            "exec(open('lib/labels.py').read()); "
            "assert normalise(' Hello ') == 'hello'; assert normalise('') == ''; print('PASS')",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
        timeout=5,
    )
    (tmp_path / "checks.log").write_text(run.stdout)
    job = submit(workflow, job, "checks.log")
    (tmp_path / "docs" / "review.txt").write_text("Synthetic independent review: PASS")
    job = submit(workflow, job, "docs/review.txt")
    assert (
        workflow.approve(job.spec.job_id, selected.brief.owner, job_digest(job)).stage
        == Stage.COMPLETE
    )
    assert (tmp_path / "docs" / "existing.md").read_text() == "Product-owned guidance: retain me."


def test_markdown_checker_ignores_generated_dependency_trees(tmp_path):
    specification = importlib.util.spec_from_file_location(
        "markdown_check", ".github/scripts/check_markdown_links.py"
    )
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    expected = tmp_path / "README.md"
    expected.write_text("Source")
    for directory in module.GENERATED_DIRECTORIES:
        (tmp_path / directory).mkdir()
        (tmp_path / directory / "dependency.md").write_text("Not repository documentation")
    assert module.markdown_files(tmp_path) == [expected]
