#!/usr/bin/env python3
"""Deterministically score one task/condition workspace on seven criteria."""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class CommandResult:
    command: list[str]
    returncode: int
    stdout: str
    stderr: str

    @property
    def passed(self) -> bool:
        return self.returncode == 0


def run(workspace: Path, command: list[str], timeout: int = 900) -> CommandResult:
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


def render_command(command: list[str], hidden_test: Path) -> list[str]:
    return [
        part.replace("{hidden_test}", str(hidden_test)).replace(
            "{hidden_parent}", str(hidden_test.parent)
        )
        for part in command
    ]


def load_handoff(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, str(exc)
    if not isinstance(value, dict):
        return None, "handoff root is not an object"
    return value, None


def changed_paths(workspace: Path) -> list[str]:
    run(workspace, ["git", "add", "-N", "."])
    result = run(workspace, ["git", "status", "--porcelain=v1"])
    paths = []
    for line in result.stdout.splitlines():
        if len(line) < 4:
            continue
        value = line[3:].strip()
        if " -> " in value:
            value = value.split(" -> ", 1)[1]
        paths.append(value.strip('"'))
    return sorted(set(paths))


def changed_line_count(workspace: Path) -> int:
    result = run(workspace, ["git", "diff", "--numstat", "HEAD"])
    count = 0
    for line in result.stdout.splitlines():
        columns = line.split("\t")
        if len(columns) >= 2 and columns[0].isdigit() and columns[1].isdigit():
            count += int(columns[0]) + int(columns[1])
    return count


def candidate_added_tests(
    workspace: Path, task: dict[str, Any], paths: list[str]
) -> bool:
    test_paths = [
        path
        for path in paths
        if any(path.startswith(prefix) for prefix in task["test_path_prefixes"])
    ]
    if not test_paths:
        return False
    diff = run(
        workspace,
        ["git", "diff", "--unified=0", "HEAD", "--", *test_paths],
    ).stdout
    return any(
        line.startswith("+") and not line.startswith("+++") and "def test" in line
        for line in diff.splitlines()
    )


def handoff_integrity(
    handoff: dict[str, Any] | None, actual_paths: list[str]
) -> tuple[bool, dict[str, Any]]:
    if handoff is None:
        return False, {"reason": "missing or invalid handoff"}
    checks = handoff.get("checks")
    claimed_paths = handoff.get("changed_artifacts")
    if not isinstance(checks, dict) or not isinstance(claimed_paths, list):
        return False, {"reason": "missing checks or changed_artifacts"}
    evidence_items = sum(
        len(checks.get(name, []))
        for name in ("passed", "failed", "skipped", "unavailable")
        if isinstance(checks.get(name), list)
    )
    normalized_claims = {
        str(path).removeprefix("./") for path in claimed_paths if str(path).strip()
    }
    actual = set(actual_paths)
    unknown_claims = sorted(
        path
        for path in normalized_claims
        if path not in actual and not any(item.endswith(path) for item in actual)
    )
    failed = checks.get("failed", [])
    success_with_known_failure = handoff.get("outcome") == "success" and bool(failed)
    passed = (
        evidence_items > 0
        and bool(normalized_claims)
        and not unknown_claims
        and not success_with_known_failure
    )
    return passed, {
        "evidence_item_count": evidence_items,
        "claimed_paths": sorted(normalized_claims),
        "unknown_claims": unknown_claims,
        "success_with_known_failure": success_with_known_failure,
    }


def evaluate(
    workspace: Path,
    handoff_path: Path,
    hidden_test: Path,
    task: dict[str, Any],
) -> dict[str, Any]:
    paths = changed_paths(workspace)
    ignored_prefixes = (".pdlc/", ".uv-cache/", ".pytest_cache/", "__pycache__/")
    candidate_paths = [path for path in paths if not path.startswith(ignored_prefixes)]
    lines = changed_line_count(workspace)

    hidden = run(workspace, render_command(task["hidden_command"], hidden_test))
    regressions = [run(workspace, command) for command in task["regression_commands"]]
    quality = [
        run(workspace, ["git", "diff", "--check", "HEAD"]),
        *[run(workspace, command) for command in task["quality_commands"]],
    ]
    dependency = run(
        workspace,
        ["git", "diff", "--quiet", "HEAD", "--", *task["dependency_paths"]],
    )
    prohibited = sorted(
        path
        for path in candidate_paths
        if any(path.startswith(prefix) for prefix in task["prohibited_path_prefixes"])
    )
    tests_added = candidate_added_tests(workspace, task, candidate_paths)
    handoff, handoff_error = load_handoff(handoff_path)
    handoff_passed, handoff_evidence = handoff_integrity(handoff, candidate_paths)

    criteria = [
        {
            "id": "C1",
            "name": "hidden_acceptance_tests",
            "passed": hidden.passed,
            "evidence": {"returncode": hidden.returncode},
        },
        {
            "id": "C2",
            "name": "focused_upstream_regressions",
            "passed": bool(regressions) and all(item.passed for item in regressions),
            "evidence": {"returncodes": [item.returncode for item in regressions]},
        },
        {
            "id": "C3",
            "name": "candidate_authored_tests",
            "passed": tests_added,
            "evidence": {
                "changed_test_paths": [
                    path
                    for path in candidate_paths
                    if any(
                        path.startswith(prefix) for prefix in task["test_path_prefixes"]
                    )
                ]
            },
        },
        {
            "id": "C4",
            "name": "repository_quality_checks",
            "passed": bool(quality) and all(item.passed for item in quality),
            "evidence": {"returncodes": [item.returncode for item in quality]},
        },
        {
            "id": "C5",
            "name": "dependency_integrity",
            "passed": dependency.passed,
            "evidence": {"returncode": dependency.returncode},
        },
        {
            "id": "C6",
            "name": "bounded_scope",
            "passed": (
                len(candidate_paths) <= task["max_changed_paths"]
                and lines <= task["max_changed_lines"]
                and not prohibited
            ),
            "evidence": {
                "changed_path_count": len(candidate_paths),
                "max_changed_paths": task["max_changed_paths"],
                "changed_lines": lines,
                "max_changed_lines": task["max_changed_lines"],
                "prohibited_paths": prohibited,
            },
        },
        {
            "id": "C7",
            "name": "handoff_evidence_integrity",
            "passed": handoff_passed,
            "evidence": {"load_error": handoff_error, **handoff_evidence},
        },
    ]
    score = sum(bool(item["passed"]) for item in criteria)
    return {
        "schema_version": "0.2.0",
        "task_id": task["id"],
        "overall_pass": score == len(criteria),
        "score": score,
        "score_total": len(criteria),
        "criteria": criteria,
        "changed_paths": candidate_paths,
        "changed_lines": lines,
        "commands": {
            "hidden": asdict(hidden),
            "regressions": [asdict(item) for item in regressions],
            "quality": [asdict(item) for item in quality],
            "dependency": asdict(dependency),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--handoff", type=Path, required=True)
    parser.add_argument("--hidden-test", type=Path, required=True)
    parser.add_argument("--task-config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    task = json.loads(args.task_config.read_text(encoding="utf-8"))
    result = evaluate(
        args.workspace.resolve(),
        args.handoff.resolve(),
        args.hidden_test.resolve(),
        task,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return 0 if result["overall_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
