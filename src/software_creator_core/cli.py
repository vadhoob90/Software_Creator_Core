"""Human-readable commands with a stable JSON result and error envelope."""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from . import __version__
from .context import resolve
from .contracts import Contribution, Job, JobSpec, Role
from .errors import CoreError
from .files import MAX_FILE_BYTES
from .hosts import availability, handoff
from .roles import role_definition
from .service import Workflow
from .storage import Store, job_digest


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(
        description="Run a bounded, evidence-led software change workflow."
    )
    cli.add_argument("--version", action="version", version=__version__)
    cli.add_argument(
        "--store", type=Path, default=Path("core-jobs.sqlite3"), help="Local job journal"
    )
    cli.add_argument(
        "--workspace", type=Path, default=Path.cwd(), help="Root for declared artifacts"
    )
    commands = cli.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor", help="Report host installation; no network or model calls")
    schema = commands.add_parser("schema", help="Print a versioned JSON Schema")
    schema.add_argument("kind", choices=("job", "contribution"))
    role = commands.add_parser(
        "role", help="Inspect an experimental role without using the harness"
    )
    role.add_argument("role", choices=[r.value for r in Role])
    create = commands.add_parser("create", help="Create a job awaiting human commitment")
    create.add_argument("input", type=Path)
    submit = commands.add_parser(
        "submit", help="Validate a contribution and advance one checkpoint"
    )
    submit.add_argument("input", type=Path)
    for name in ("show", "approve", "cancel", "context", "handoff"):
        command = commands.add_parser(name, help=f"{name.capitalize()} an existing job")
        command.add_argument("job_id")
        _command_options(command, name)
    return cli


def _command_options(command: argparse.ArgumentParser, name: str) -> None:
    if name in ("approve", "cancel"):
        command.add_argument("--actor", required=True)
    if name == "approve":
        command.add_argument("--digest", required=True, help="Digest from the latest show result")
    if name in ("context", "handoff"):
        command.add_argument("--role", choices=[r.value for r in Role], required=True)
    if name == "handoff":
        command.add_argument("--host", choices=("codex", "claude-code"), required=True)


def read_input(path: Path) -> str:
    with path.open("rb") as stream:
        content = stream.read(MAX_FILE_BYTES + 1)
    if len(content) > MAX_FILE_BYTES:
        raise CoreError(
            "input-limit", "Input exceeds 256 KB.", "Use a smaller job or contribution."
        )
    return content.decode("utf-8")


def summary(job: Job) -> dict[str, Any]:
    return {
        "operation_outcome": "success",
        "workflow_outcome": {
            "completed": "success",
            "failed": "failure",
            "cancelled": "cancelled",
        }.get(job.stage.value, "partial"),
        "stage": job.stage.value,
        "revision": job.revision,
        "digest": job_digest(job),
        "job": job.model_dump(mode="json"),
    }


def dispatch(args: argparse.Namespace) -> dict[str, Any]:
    if args.command == "doctor":
        return {
            "core_version": __version__,
            "api_calls": False,
            "hosts": [availability("codex"), availability("claude-code")],
        }
    if args.command == "schema":
        model = JobSpec if args.kind == "job" else Contribution
        return model.model_json_schema()
    if args.command == "role":
        return role_definition(Role(args.role))
    workflow = Workflow(Store(args.store), args.workspace)
    return _workflow_command(workflow, args)


def _workflow_command(workflow: Workflow, args: argparse.Namespace) -> dict[str, Any]:
    if args.command == "create":
        return summary(workflow.create(JobSpec.model_validate_json(read_input(args.input))))
    if args.command == "submit":
        return summary(workflow.submit(Contribution.model_validate_json(read_input(args.input))))
    if args.command == "approve":
        return summary(workflow.approve(args.job_id, args.actor, args.digest))
    if args.command == "cancel":
        return summary(workflow.cancel(args.job_id, args.actor))
    job = workflow.store.load(args.job_id)
    if args.command == "context":
        return resolve(job, workflow.workspace, Role(args.role))
    if args.command == "handoff":
        return handoff(job, workflow.workspace, Role(args.role), args.host)
    return summary(job)


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        result = dispatch(args)
    except CoreError as exc:
        print(json.dumps(exc.as_dict()), file=sys.stderr)
        return 1
    except (OSError, UnicodeError, ValidationError) as exc:
        # Do not echo source text, secrets, Pydantic input values or OS paths.
        error = CoreError(
            "invalid-input",
            f"Input could not be processed ({type(exc).__name__}).",
            "Check the file, workspace, permissions and published JSON Schema.",
        )
        print(json.dumps(error.as_dict()), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 3 if result.get("workflow_outcome") in ("failure", "cancelled") else 0


if __name__ == "__main__":
    raise SystemExit(main())
