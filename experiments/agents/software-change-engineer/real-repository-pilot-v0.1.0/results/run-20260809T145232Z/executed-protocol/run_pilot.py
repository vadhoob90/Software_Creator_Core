#!/usr/bin/env python3
"""Run the paired real-repository pilot in isolated Codex sessions."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


ROOT = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def run(
    command: list[str],
    *,
    cwd: Optional[Path] = None,
    input_text: Optional[str] = None,
    timeout: Optional[int] = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        input=input_text,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def require_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise RuntimeError(f"required executable is unavailable: {name}")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def candidate_prompt(task_text: str) -> str:
    return f"""You are the Software Change Engineer for this bounded task.

Read and follow `AGENTS.md`, `.pdlc/agent-definition.md`, and the task below.
Work only in this local checkout. Do not use network access, Git remotes,
credentials, or external systems. Make the requested code and test changes, run
the checks that are actually available, and return only the structured JSON
handoff required by the runtime schema. Do not commit the change.

--- BEGIN TASK ---
{task_text.rstrip()}
--- END TASK ---
"""


def parse_runtime_events(path: Path) -> dict[str, Any]:
    events: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            events.append(value)

    usage: dict[str, int] = {}
    for event in events:
        candidate = event.get("usage")
        if isinstance(candidate, dict) and any("token" in key for key in candidate):
            usage = {
                key: int(value)
                for key, value in candidate.items()
                if "token" in key and isinstance(value, (int, float))
            }

    tool_calls = 0
    for event in events:
        item = event.get("item")
        item_type = item.get("type", "") if isinstance(item, dict) else ""
        if item_type in {"command_execution", "mcp_tool_call", "file_change"}:
            tool_calls += 1

    return {"event_count": len(events), "tool_call_count": tool_calls, "usage": usage}


def copy_condition_files(condition: dict[str, Any], workspace: Path, task_path: Path) -> None:
    expected_definition = condition["definition_sha256"]
    deployed_definition = workspace / ".pdlc" / "agent-definition.md"
    deployed_task = workspace / ".pdlc" / "tasks" / "LSE-119.md"
    if not deployed_definition.exists() or not deployed_task.exists():
        raise RuntimeError("condition repository is missing frozen .pdlc artifacts")
    if sha256(deployed_definition) != expected_definition:
        raise RuntimeError(f"definition hash mismatch for {condition['id']}")
    if deployed_task.read_bytes() != task_path.read_bytes():
        raise RuntimeError(f"task mismatch for {condition['id']}")


def run_condition(
    lock: dict[str, Any],
    condition: dict[str, Any],
    output_root: Path,
    task_path: Path,
    schema_path: Path,
) -> dict[str, Any]:
    condition_id = condition["id"]
    condition_output = output_root / condition_id
    condition_output.mkdir(parents=True)
    workspace = Path(tempfile.mkdtemp(prefix=f"pdlc-pilot-{condition_id}-"))

    started_at = datetime.now(timezone.utc)
    clone = run(["git", "clone", "--quiet", condition["repository"], str(workspace)])
    if clone.returncode != 0:
        raise RuntimeError(f"clone failed for {condition_id}: {clone.stderr}")

    checkout = run(["git", "checkout", "--detach", condition["repository_commit"]], cwd=workspace)
    if checkout.returncode != 0:
        raise RuntimeError(f"checkout failed for {condition_id}: {checkout.stderr}")
    actual_commit = run(["git", "rev-parse", "HEAD"], cwd=workspace).stdout.strip()
    if actual_commit != condition["repository_commit"]:
        raise RuntimeError(f"commit mismatch for {condition_id}: {actual_commit}")

    copy_condition_files(condition, workspace, task_path)

    provision_command = lock["runtime"]["provision_command"]
    provision = run(provision_command, cwd=workspace, timeout=600)
    (condition_output / "provision.stdout.txt").write_text(provision.stdout, encoding="utf-8")
    (condition_output / "provision.stderr.txt").write_text(provision.stderr, encoding="utf-8")
    if provision.returncode != 0:
        raise RuntimeError(f"provisioning failed for {condition_id}")

    run(["git", "remote", "remove", "origin"], cwd=workspace)
    remotes = run(["git", "remote"], cwd=workspace).stdout.strip()
    if remotes:
        raise RuntimeError(f"Git remotes remain in {condition_id}: {remotes}")

    prompt = candidate_prompt(task_path.read_text(encoding="utf-8"))
    (condition_output / "prompt.md").write_text(prompt, encoding="utf-8")
    handoff_path = condition_output / "handoff.json"
    event_path = condition_output / "events.jsonl"

    codex_command = [
        "codex",
        "exec",
        "--model",
        lock["runtime"]["model"],
        "--sandbox",
        lock["runtime"]["sandbox"],
        "--ephemeral",
        "--ignore-user-config",
        "--json",
        "--output-schema",
        str(schema_path),
        "--output-last-message",
        str(handoff_path),
        "-C",
        str(workspace),
        "-c",
        f'model_reasoning_effort="{lock["runtime"]["reasoning_effort"]}"',
        "-c",
        f'approval_policy="{lock["runtime"]["approval_policy"]}"',
        "--color",
        "never",
        "-",
    ]

    candidate_started = time.monotonic()
    try:
        candidate = run(
            codex_command,
            cwd=workspace,
            input_text=prompt,
            timeout=lock["runtime"]["timeout_seconds"],
        )
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        candidate = subprocess.CompletedProcess(
            codex_command,
            124,
            exc.stdout or "",
            (exc.stderr or "") + "\nCandidate timed out.",
        )
        timed_out = True
    candidate_elapsed = time.monotonic() - candidate_started

    event_path.write_text(candidate.stdout, encoding="utf-8")
    (condition_output / "codex.stderr.txt").write_text(candidate.stderr, encoding="utf-8")

    run(["git", "add", "-N", "."], cwd=workspace)
    patch = run(["git", "diff", "--binary"], cwd=workspace)
    (condition_output / "candidate.patch").write_text(patch.stdout, encoding="utf-8")
    status = run(["git", "status", "--short"], cwd=workspace)
    (condition_output / "git-status.txt").write_text(status.stdout, encoding="utf-8")
    numstat = run(["git", "diff", "--numstat"], cwd=workspace)
    (condition_output / "git-numstat.txt").write_text(numstat.stdout, encoding="utf-8")

    evaluator = run(
        [
            sys.executable,
            str(ROOT / "evaluate_pilot.py"),
            "--workspace",
            str(workspace),
            "--handoff",
            str(handoff_path),
            "--output",
            str(condition_output / "evaluation.json"),
        ],
        timeout=1200,
    )
    (condition_output / "evaluator.stdout.txt").write_text(evaluator.stdout, encoding="utf-8")
    (condition_output / "evaluator.stderr.txt").write_text(evaluator.stderr, encoding="utf-8")

    changed_lines = 0
    for line in numstat.stdout.splitlines():
        columns = line.split("\t")
        if len(columns) >= 2 and columns[0].isdigit() and columns[1].isdigit():
            changed_lines += int(columns[0]) + int(columns[1])

    evaluation_path = condition_output / "evaluation.json"
    evaluation = load_json(evaluation_path) if evaluation_path.exists() else None
    record = {
        "condition_id": condition_id,
        "repository": condition["repository"],
        "repository_commit": actual_commit,
        "definition_sha256": condition["definition_sha256"],
        "started_at": started_at.isoformat(),
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "candidate_elapsed_seconds": round(candidate_elapsed, 3),
        "candidate_returncode": candidate.returncode,
        "candidate_timed_out": timed_out,
        "changed_lines": changed_lines,
        "runtime_telemetry": parse_runtime_events(event_path),
        "evaluation": evaluation,
        "workspace_retained_at": str(workspace),
    }
    (condition_output / "run-record.json").write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return record


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lock", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    for tool in ("git", "uv", "codex"):
        require_tool(tool)

    lock_path = args.lock.resolve()
    lock = load_json(lock_path)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_root = (args.output or ROOT / "results" / f"run-{timestamp}").resolve()
    output_root.mkdir(parents=True, exist_ok=False)
    shutil.copy2(lock_path, output_root / "experiment.lock.json")

    task_path = ROOT / lock["task"]["path"]
    schema_path = ROOT / "schemas" / "handoff.schema.json"
    if sha256(task_path) != lock["task"]["sha256"]:
        raise RuntimeError("task hash does not match the lock file")
    if sha256(schema_path) != lock["handoff_schema_sha256"]:
        raise RuntimeError("handoff schema hash does not match the lock file")

    conditions_by_id = {item["id"]: item for item in lock["conditions"]}
    records = []
    for condition_id in lock["execution_order"]:
        records.append(
            run_condition(
                lock,
                conditions_by_id[condition_id],
                output_root,
                task_path,
                schema_path,
            )
        )

    summary = {
        "experiment_id": lock["experiment_id"],
        "lock_sha256": sha256(output_root / "experiment.lock.json"),
        "conditions": records,
    }
    (output_root / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(output_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
