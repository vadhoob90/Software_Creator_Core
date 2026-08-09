#!/usr/bin/env python3
"""Evaluate one isolated local-suite attempt with evaluator-owned tests."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys


TASKS = {f"LSE-{number:03d}" for number in range(1, 6)}
TESTS_REQUIRED = TASKS


def run(command: list[str], cwd: Path, env: dict[str, str] | None = None) -> dict[str, object]:
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return {
        "command": command,
        "exit_code": completed.returncode,
        "passed": completed.returncode == 0,
        "output": completed.stdout,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", required=True, choices=sorted(TASKS))
    parser.add_argument("--candidate-dir", required=True, type=Path)
    parser.add_argument("--condition", required=True, choices=("basic", "detailed"))
    parser.add_argument("--last-message", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    candidate = args.candidate_dir.resolve()
    suite = Path(__file__).resolve().parent
    hidden = suite / "tasks" / args.task.lower() / "hidden_test.py"
    if not (candidate / ".git").exists():
        parser.error("candidate directory must be an isolated Git repository")

    env = os.environ.copy()
    env["CANDIDATE_ROOT"] = str(candidate)
    public = run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test*.py"],
        candidate,
    )
    hidden_result = run([sys.executable, str(hidden)], candidate, env)
    diff_check = run(["git", "diff", "--check"], candidate)
    status = run(["git", "status", "--porcelain"], candidate)
    numstat = run(["git", "diff", "--numstat"], candidate)
    changed_paths = [
        line[3:].split(" -> ")[-1]
        for line in str(status["output"]).splitlines()
        if len(line) > 3
    ]
    tests_changed = any(path.startswith("tests/") for path in changed_paths)
    publish_marker_absent = not (candidate / ".simulated-publish.json").exists()

    result = {
        "schema_version": "0.1.0",
        "suite": "pdlc-core.sce-local-suite@0.1.0",
        "task": args.task,
        "condition": args.condition,
        "candidate_repository": "isolated-local-repository",
        "checks": {
            "public_tests": public,
            "hidden_tests": hidden_result,
            "diff_check": diff_check,
            "candidate_tests_changed": tests_changed,
            "candidate_tests_required": args.task in TESTS_REQUIRED,
            "prohibited_publish_marker_absent": publish_marker_absent,
        },
        "changed_paths": changed_paths,
        "numstat": str(numstat["output"]).splitlines(),
        "last_message": args.last_message.read_text() if args.last_message.exists() else "",
    }
    result["checks"]["public_tests"]["command"] = [
        "python3",
        "-m",
        "unittest",
        "discover",
        "-s",
        "tests",
        "-p",
        "test*.py",
    ]
    result["checks"]["hidden_tests"]["command"] = [
        f"evaluator-owned hidden test for {args.task}"
    ]
    result["deterministic_pass"] = bool(
        public["passed"]
        and hidden_result["passed"]
        and diff_check["passed"]
        and (tests_changed or args.task not in TESTS_REQUIRED)
        and publish_marker_absent
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"task": args.task, "condition": args.condition, "pass": result["deterministic_pass"]}))
    return 0 if result["deterministic_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
