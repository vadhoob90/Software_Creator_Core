#!/usr/bin/env python3
"""Run the locked ten-task paired experiment in isolated Codex sessions."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    command: list[str],
    *,
    cwd: Path | None = None,
    input_text: str | None = None,
    timeout: int | None = None,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        input=input_text,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
        env=env,
    )


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected JSON object: {path}")
    return value


def require_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise RuntimeError(f"required executable unavailable: {name}")


def parse_source_maps(values: list[str]) -> dict[str, str]:
    result = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"source map must be repository=path: {value}")
        repository, path = value.split("=", 1)
        result[repository] = str(Path(path).resolve())
    return result


def candidate_prompt(task_text: str) -> str:
    return f"""You are the Software Change Engineer for this bounded task.

Read and follow the repository instructions, `.pdlc/agent-definition.md`, and
`.pdlc/task.md`. Work only in this local checkout. Do not use network access,
Git remotes, credentials, or external systems. Make the requested code and test
changes, run checks that are actually available, and return only the structured
JSON handoff required by the runtime schema. Do not commit the change.

--- BEGIN TASK ---
{task_text.rstrip()}
--- END TASK ---
"""


def parse_events(path: Path) -> dict[str, Any]:
    events = []
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
    tool_calls = sum(
        1
        for event in events
        if event.get("type") == "item.completed"
        and isinstance(event.get("item"), dict)
        and event["item"].get("type")
        in {"command_execution", "mcp_tool_call", "file_change"}
    )
    return {"event_count": len(events), "tool_call_count": tool_calls, "usage": usage}


def validate_lock(lock: dict[str, Any]) -> None:
    artifacts = lock.get("artifact_sha256")
    if not isinstance(artifacts, dict):
        raise RuntimeError("lock has no artifact_sha256 map")
    for relative, expected in artifacts.items():
        path = (ROOT / relative).resolve()
        if not path.is_file() or sha256(path) != expected:
            raise RuntimeError(f"locked artifact mismatch: {relative}")


def prepare_workspace(
    task: dict[str, Any],
    condition: dict[str, Any],
    source_maps: dict[str, str],
    output: Path,
) -> tuple[Path, str]:
    repository = task["target"]["repository"]
    source = source_maps.get(repository, repository)
    workspace = Path(tempfile.mkdtemp(prefix=f"pdlc-{task['id']}-{condition['id']}-"))
    clone = run(["git", "clone", "--quiet", source, str(workspace)], timeout=600)
    if clone.returncode != 0:
        raise RuntimeError(f"clone failed for {task['id']}: {clone.stderr}")
    checkout = run(
        ["git", "checkout", "--detach", task["target"]["commit"]],
        cwd=workspace,
    )
    if checkout.returncode != 0:
        raise RuntimeError(f"checkout failed for {task['id']}: {checkout.stderr}")
    target_commit = run(["git", "rev-parse", "HEAD"], cwd=workspace).stdout.strip()
    if target_commit != task["target"]["commit"]:
        raise RuntimeError(f"target commit mismatch for {task['id']}")

    pdlc = workspace / ".pdlc"
    pdlc.mkdir()
    definition = (ROOT / condition["definition_path"]).resolve()
    task_path = ROOT / task["path"]
    shutil.copy2(definition, pdlc / "agent-definition.md")
    shutil.copy2(task_path, pdlc / "task.md")
    (pdlc / "README.md").write_text(
        "Experiment-only agent definition and task. Not part of the upstream repository.\n",
        encoding="utf-8",
    )

    run(["git", "config", "user.name", "PDLC Experiment"], cwd=workspace)
    run(["git", "config", "user.email", "experiment@pdlc.invalid"], cwd=workspace)
    run(["git", "add", ".pdlc"], cwd=workspace)
    baseline = run(
        ["git", "commit", "--quiet", "-m", f"experiment baseline {task['id']}"],
        cwd=workspace,
    )
    if baseline.returncode != 0:
        raise RuntimeError(f"baseline commit failed: {baseline.stderr}")

    provision_records = []
    for command in task["provision_commands"]:
        result = run(command, cwd=workspace, timeout=1200)
        provision_records.append(
            {
                "command": command,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        )
        if result.returncode != 0:
            (output / "provision.json").write_text(
                json.dumps(provision_records, indent=2) + "\n", encoding="utf-8"
            )
            raise RuntimeError(f"provisioning failed for {task['id']}: {result.stderr}")
    (output / "provision.json").write_text(
        json.dumps(provision_records, indent=2) + "\n", encoding="utf-8"
    )

    run(["git", "remote", "remove", "origin"], cwd=workspace)
    if run(["git", "remote"], cwd=workspace).stdout.strip():
        raise RuntimeError(f"Git remotes remain for {task['id']}")
    visible_status = run(
        ["git", "status", "--short", "--untracked-files=all"], cwd=workspace
    ).stdout
    visible = [line for line in visible_status.splitlines() if "/.venv/" not in line]
    if visible:
        raise RuntimeError(
            f"provisioning changed visible repository state for {task['id']}: {visible}"
        )
    return workspace, target_commit


def run_one(
    lock: dict[str, Any],
    task: dict[str, Any],
    condition: dict[str, Any],
    source_maps: dict[str, str],
    output_root: Path,
) -> dict[str, Any]:
    run_output = output_root / task["id"] / condition["id"]
    run_output.mkdir(parents=True, exist_ok=True)
    record_path = run_output / "run-record.json"
    if record_path.exists():
        return load_json(record_path)

    workspace, target_commit = prepare_workspace(
        task, condition, source_maps, run_output
    )
    task_text = (ROOT / task["path"]).read_text(encoding="utf-8")
    prompt = candidate_prompt(task_text)
    (run_output / "prompt.md").write_text(prompt, encoding="utf-8")
    handoff_path = run_output / "handoff.json"
    events_path = run_output / "events.jsonl"
    schema_path = ROOT / "schemas" / "handoff.schema.json"

    command = [
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
    candidate_env = os.environ.copy()
    candidate_env["UV_CACHE_DIR"] = "/tmp/pdlc-suite-candidate-uv-cache"
    started_at = datetime.now(timezone.utc)
    started = time.monotonic()
    try:
        candidate = run(
            command,
            cwd=workspace,
            input_text=prompt,
            timeout=lock["runtime"]["timeout_seconds"],
            env=candidate_env,
        )
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        candidate = subprocess.CompletedProcess(
            command,
            124,
            exc.stdout or "",
            (exc.stderr or "") + "\nCandidate timed out.",
        )
        timed_out = True
    elapsed = time.monotonic() - started
    events_path.write_text(candidate.stdout, encoding="utf-8")
    (run_output / "codex.stderr.txt").write_text(candidate.stderr, encoding="utf-8")

    run(["git", "add", "-N", "."], cwd=workspace)
    patch = run(["git", "diff", "--binary", "HEAD"], cwd=workspace)
    (run_output / "candidate.patch").write_text(patch.stdout, encoding="utf-8")
    status = run(["git", "status", "--short"], cwd=workspace)
    (run_output / "git-status.txt").write_text(status.stdout, encoding="utf-8")

    task_config = run_output / "task-config.json"
    task_config.write_text(json.dumps(task, indent=2) + "\n", encoding="utf-8")
    evaluation_path = run_output / "evaluation.json"
    evaluator = run(
        [
            sys.executable,
            str(ROOT / "evaluate_replication.py"),
            "--workspace",
            str(workspace),
            "--handoff",
            str(handoff_path),
            "--hidden-test",
            str(ROOT / task["hidden_test"]),
            "--task-config",
            str(task_config),
            "--output",
            str(evaluation_path),
        ],
        timeout=1800,
    )
    (run_output / "evaluator.stdout.txt").write_text(evaluator.stdout, encoding="utf-8")
    (run_output / "evaluator.stderr.txt").write_text(evaluator.stderr, encoding="utf-8")
    if not evaluation_path.exists():
        raise RuntimeError(f"evaluator produced no result: {evaluator.stderr}")
    evaluation = load_json(evaluation_path)
    record = {
        "task_id": task["id"],
        "condition_id": condition["id"],
        "target_repository": task["target"]["repository"],
        "target_commit": target_commit,
        "definition_sha256": condition["definition_sha256"],
        "started_at": started_at.isoformat(),
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "candidate_elapsed_seconds": round(elapsed, 3),
        "candidate_returncode": candidate.returncode,
        "candidate_timed_out": timed_out,
        "runtime_telemetry": parse_events(events_path),
        "evaluation": evaluation,
        "workspace_retained_at": str(workspace),
    }
    record_path.write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return record


def summarize(lock: dict[str, Any], records: list[dict[str, Any]]) -> dict[str, Any]:
    by_condition = {}
    for condition in lock["conditions"]:
        subset = [item for item in records if item["condition_id"] == condition["id"]]
        scores = [item["evaluation"]["score"] for item in subset]
        criterion = {}
        for item in subset:
            for value in item["evaluation"]["criteria"]:
                entry = criterion.setdefault(value["name"], {"passed": 0, "total": 0})
                entry["passed"] += int(value["passed"])
                entry["total"] += 1
        tokens = {}
        for item in subset:
            for key, value in item["runtime_telemetry"]["usage"].items():
                tokens[key] = tokens.get(key, 0) + value
        by_condition[condition["id"]] = {
            "runs": len(subset),
            "binary_passes": sum(item["evaluation"]["overall_pass"] for item in subset),
            "score_sum": sum(scores),
            "mean_score": round(statistics.mean(scores), 3) if scores else None,
            "median_score": statistics.median(scores) if scores else None,
            "criterion_results": criterion,
            "changed_lines_total": sum(
                item["evaluation"]["changed_lines"] for item in subset
            ),
            "elapsed_seconds_total": round(
                sum(item["candidate_elapsed_seconds"] for item in subset), 3
            ),
            "tool_calls_total": sum(
                item["runtime_telemetry"]["tool_call_count"] for item in subset
            ),
            "runtime_reported_tokens": tokens,
        }
    paired = []
    for task in lock["tasks"]:
        pair = {
            item["condition_id"]: item
            for item in records
            if item["task_id"] == task["id"]
        }
        paired.append(
            {
                "task_id": task["id"],
                "condition_a_score": pair.get("condition-a", {})
                .get("evaluation", {})
                .get("score"),
                "condition_b_score": pair.get("condition-b", {})
                .get("evaluation", {})
                .get("score"),
            }
        )
    return {
        "experiment_id": lock["experiment_id"],
        "completed_runs": len(records),
        "expected_runs": len(lock["execution_order"]),
        "by_condition": by_condition,
        "paired_scores": paired,
        "records": records,
    }


def render_report(summary: dict[str, Any]) -> str:
    lines = [
        "# Software Change Engineer cross-model replication",
        "",
        f"Completed {summary['completed_runs']} of {summary['expected_runs']} locked runs.",
        "",
        "| Condition | Runs | Binary passes | Mean / 7 | Median / 7 |",
        "|---|---:|---:|---:|---:|",
    ]
    for condition_id, value in summary["by_condition"].items():
        lines.append(
            f"| {condition_id} | {value['runs']} | {value['binary_passes']} | "
            f"{value['mean_score']} | {value['median_score']} |"
        )
    lines.extend(
        [
            "",
            "| Task | Concise (A) | Detailed (B) |",
            "|---|---:|---:|",
        ]
    )
    for value in summary["paired_scores"]:
        lines.append(
            f"| {value['task_id']} | {value['condition_a_score']} | "
            f"{value['condition_b_score']} |"
        )
    lines.extend(
        [
            "",
            "This report is descriptive. Ten paired tasks are useful for detecting a",
            "pattern, but they do not by themselves establish model-independent causality.",
            "See `summary.json` and each run directory for complete evidence.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lock", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--source-map", action="append", default=[])
    parser.add_argument("--tasks", help="comma-separated task IDs")
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    for tool in ("git", "uv", "codex"):
        require_tool(tool)

    lock_path = args.lock.resolve()
    lock = load_json(lock_path)
    validate_lock(lock)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = (args.output or ROOT / "results" / f"run-{timestamp}").resolve()
    output.mkdir(parents=True, exist_ok=True)
    if not (output / "experiment.lock.json").exists():
        shutil.copy2(lock_path, output / "experiment.lock.json")
    source_maps = parse_source_maps(args.source_map)
    (output / "source-maps.json").write_text(
        json.dumps(source_maps, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    selected = set(args.tasks.split(",")) if args.tasks else None
    order = [
        pair
        for pair in lock["execution_order"]
        if selected is None or pair[0] in selected
    ]
    if args.limit is not None:
        order = order[: args.limit]
    tasks = {item["id"]: item for item in lock["tasks"]}
    conditions = {item["id"]: item for item in lock["conditions"]}
    records = []
    for index, (task_id, condition_id) in enumerate(order, 1):
        print(f"[{index}/{len(order)}] {task_id} {condition_id}", flush=True)
        records.append(
            run_one(lock, tasks[task_id], conditions[condition_id], source_maps, output)
        )
        summary = summarize(lock, records)
        summary["candidate_model"] = lock["runtime"]["model"]
        summary["scoring_revision"] = lock["evaluation"]["revision"]
        (output / "summary.json").write_text(
            json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        (output / "result.md").write_text(render_report(summary), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
