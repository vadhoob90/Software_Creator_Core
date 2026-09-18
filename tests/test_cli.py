import json

import pytest

from software_creator_core.cli import main, read_input
from software_creator_core.errors import CoreError
from software_creator_core.storage import job_digest

from .conftest import contribution


@pytest.mark.parametrize(
    "args",
    [
        ["doctor"],
        ["schema", "job"],
        ["schema", "contribution"],
        ["role", "product-manager"],
        ["role", "software-architect"],
    ],
)
def test_read_only_commands(args, capsys):
    assert main(args) == 0
    assert json.loads(capsys.readouterr().out)


def test_create_show_approve_context_handoff_and_submit(workflow, spec, capsys):
    path = workflow.workspace / "job.json"
    path.write_text(spec.model_dump_json())
    base = ["--store", str(workflow.store.path), "--workspace", str(workflow.workspace)]
    assert main([*base, "create", str(path)]) == 0
    created = json.loads(capsys.readouterr().out)
    assert created["workflow_outcome"] == "partial"
    assert main([*base, "show", spec.job_id]) == 0
    assert json.loads(capsys.readouterr().out) == created
    assert (
        main([*base, "approve", spec.job_id, "--actor", "owner", "--digest", created["digest"]])
        == 0
    )
    capsys.readouterr()
    assert main([*base, "context", spec.job_id, "--role", "software-engineer"]) == 0
    context = json.loads(capsys.readouterr().out)
    assert context["manifest"]["revision"] == 1
    assert (
        main([*base, "handoff", spec.job_id, "--role", "software-engineer", "--host", "codex"]) == 0
    )
    handoff = json.loads(capsys.readouterr().out)
    assert handoff["packet"]["digest"] == context["digest"]
    result = contribution(workflow, workflow.store.load(spec.job_id))
    response = workflow.workspace / "response.json"
    response.write_text(result.model_dump_json())
    assert main([*base, "submit", str(response)]) == 0
    assert json.loads(capsys.readouterr().out)["stage"] == "verification"
    assert main([*base, "cancel", spec.job_id, "--actor", "owner"]) == 3
    assert json.loads(capsys.readouterr().out)["workflow_outcome"] == "cancelled"


def test_cli_error_has_no_private_input(tmp_path, capsys):
    path = tmp_path / "bad.json"
    path.write_text('{"private": "do-not-print-this-secret"}')
    assert main(["create", str(path)]) == 2
    result = capsys.readouterr()
    assert not result.out
    assert "do-not-print" not in result.err
    assert json.loads(result.err)["code"] == "invalid-input"


def test_cli_reports_domain_errors(workflow, active, capsys):
    base = ["--store", str(workflow.store.path), "--workspace", str(workflow.workspace)]
    assert (
        main(
            [
                *base,
                "approve",
                active.spec.job_id,
                "--actor",
                "other",
                "--digest",
                job_digest(active),
            ]
        )
        == 1
    )
    assert json.loads(capsys.readouterr().err)["code"] == "approval-denied"


def test_cli_input_limit(tmp_path):
    path = tmp_path / "huge.json"
    path.write_bytes(b"x" * 256001)
    with pytest.raises(CoreError):
        read_input(path)


def test_help_is_discoverable(capsys):
    with pytest.raises(SystemExit) as caught:
        main(["--help"])
    assert caught.value.code == 0
    assert "handoff" in capsys.readouterr().out
