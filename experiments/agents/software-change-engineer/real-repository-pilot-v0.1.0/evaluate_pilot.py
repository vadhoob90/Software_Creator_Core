#!/usr/bin/env python3
"""Apply deterministic checks to one real-repository pilot workspace."""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Optional, Tuple


@dataclass(frozen=True)
class CommandResult:
    command: list[str]
    returncode: int
    stdout: str
    stderr: str

    @property
    def passed(self) -> bool:
        return self.returncode == 0


def run_command(
    workspace: Path, command: list[str], timeout: int = 600
) -> CommandResult:
    try:
        result = subprocess.run(
            command,
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return CommandResult(command, result.returncode, result.stdout, result.stderr)
    except subprocess.TimeoutExpired as exc:
        return CommandResult(
            command,
            124,
            exc.stdout or "",
            (exc.stderr or "") + f"\nTimed out after {timeout} seconds.",
        )


def changed_paths(workspace: Path) -> list[str]:
    result = run_command(workspace, ["git", "status", "--short"])
    return [line[3:].strip() for line in result.stdout.splitlines() if len(line) >= 4]


def load_handoff(path: Path) -> Tuple[Optional[dict[str, Any]], Optional[str]]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, str(exc)
    if not isinstance(value, dict):
        return None, "handoff root is not an object"
    return value, None


def contains_all(text: str, terms: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return all(term.lower() in lowered for term in terms)


def evaluate(workspace: Path, handoff_path: Path) -> dict[str, Any]:
    production_root = workspace / "src" / "content_creator"
    venv_bin = workspace / ".venv" / "bin"
    ingestion_path = production_root / "ingestion.py"
    paths = changed_paths(workspace)
    changed_test_paths = [path for path in paths if path.startswith("tests/")]

    ingestion_text = ingestion_path.read_text(encoding="utf-8")
    production_python = [
        path for path in production_root.rglob("*.py") if path != ingestion_path
    ]
    boundary_files = [
        path
        for path in production_python
        if "pypdf" in path.read_text(encoding="utf-8").lower()
        and (
            "import_module" in path.read_text(encoding="utf-8")
            or "import pypdf" in path.read_text(encoding="utf-8")
            or "from pypdf" in path.read_text(encoding="utf-8")
        )
    ]

    test_text = "\n".join(
        (workspace / path).read_text(encoding="utf-8", errors="replace")
        for path in changed_test_paths
        if (workspace / path).is_file()
    )

    commands = {
        "diff_check": run_command(workspace, ["git", "diff", "--check"]),
        "tests": run_command(workspace, [str(venv_bin / "pytest"), "-q"]),
        "ruff": run_command(workspace, [str(venv_bin / "ruff"), "check", "."]),
        "format": run_command(
            workspace, [str(venv_bin / "ruff"), "format", "--check", "."]
        ),
        "mypy": run_command(workspace, [str(venv_bin / "mypy")]),
        "dependency_diff": run_command(
            workspace, ["git", "diff", "--quiet", "--", "pyproject.toml", "uv.lock"]
        ),
    }

    handoff, handoff_error = load_handoff(handoff_path)
    handoff_text = json.dumps(handoff or {}, sort_keys=True)
    deferred_text = " ".join(
        [
            json.dumps((handoff or {}).get("unverified_claims", [])),
            json.dumps((handoff or {}).get("residual_risks", [])),
            json.dumps((handoff or {}).get("authority", {})),
            str((handoff or {}).get("compatibility_and_lifecycle", "")),
            str((handoff or {}).get("next_action", "")),
        ]
    )

    fake_package_paths = [
        path for path in paths if path == "pypdf.py" or path.startswith("pypdf/")
    ]

    criteria = [
        {
            "id": "DOD-1",
            "description": "PDF ingestion delegates to an application-owned boundary",
            "passed": "from pypdf" not in ingestion_text.lower()
            and "import pypdf" not in ingestion_text.lower()
            and bool(boundary_files),
            "evidence": {
                "boundary_files": [
                    str(path.relative_to(workspace)) for path in boundary_files
                ],
                "direct_pypdf_import_in_ingestion": "from pypdf"
                in ingestion_text.lower()
                or "import pypdf" in ingestion_text.lower(),
            },
        },
        {
            "id": "DOD-2",
            "description": "Supported-version behaviour remains working",
            "passed": commands["tests"].passed,
            "evidence": {
                "command": commands["tests"].command,
                "returncode": commands["tests"].returncode,
            },
        },
        {
            "id": "DOD-3",
            "description": "Missing dependency remains explicit and cause-preserving",
            "passed": bool(changed_test_paths)
            and contains_all(test_text, ("pypdf", "IngestionError"))
            and ("__cause__" in test_text or "ImportError" in test_text),
            "evidence": {"changed_test_paths": changed_test_paths},
        },
        {
            "id": "DOD-4",
            "description": "Focused tests cover the boundary and missing dependency",
            "passed": bool(changed_test_paths)
            and "pypdf" in test_text.lower()
            and ("monkeypatch" in test_text.lower() or "mock" in test_text.lower()),
            "evidence": {"changed_test_paths": changed_test_paths},
        },
        {
            "id": "DOD-5",
            "description": "Available repository checks pass",
            "passed": all(
                commands[name].passed
                for name in ("diff_check", "tests", "ruff", "format", "mypy")
            ),
            "evidence": {
                name: result.returncode
                for name, result in commands.items()
                if name != "dependency_diff"
            },
        },
        {
            "id": "DOD-6",
            "description": "Dependency declarations and lockfile are unchanged; no fake package is added",
            "passed": commands["dependency_diff"].passed and not fake_package_paths,
            "evidence": {
                "dependency_diff_returncode": commands["dependency_diff"].returncode,
                "fake_package_paths": fake_package_paths,
            },
        },
        {
            "id": "DOD-7",
            "description": "Handoff separates verified work from deferred pypdf 7 compatibility",
            "passed": handoff is not None
            and "pypdf" in deferred_text.lower()
            and "7" in deferred_text
            and any(
                term in deferred_text.lower()
                for term in (
                    "unverified",
                    "defer",
                    "unavailable",
                    "not tested",
                    "not verified",
                )
            ),
            "evidence": {"handoff_error": handoff_error},
        },
    ]

    scope_paths = [path for path in paths if not path.startswith(".pdlc/")]
    result = {
        "schema_version": "0.1.0",
        "workspace": str(workspace),
        "overall_pass": all(item["passed"] for item in criteria),
        "criteria_passed": sum(bool(item["passed"]) for item in criteria),
        "criteria_total": len(criteria),
        "criteria": criteria,
        "changed_paths": paths,
        "changed_path_count": len(scope_paths),
        "handoff_present": handoff is not None,
        "handoff_evidence_integrity": handoff is not None
        and contains_all(handoff_text, ("checks", "unverified_claims", "authority")),
        "commands": {name: asdict(value) for name, value in commands.items()},
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--handoff", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = evaluate(args.workspace.resolve(), args.handoff.resolve())
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if result["overall_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
