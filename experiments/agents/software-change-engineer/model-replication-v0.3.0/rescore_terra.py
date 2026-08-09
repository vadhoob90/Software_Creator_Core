#!/usr/bin/env python3
"""Reconstruct and rescore the saved Terra patches with the v0.3 evaluator."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import run_replication as protocol

ROOT = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected JSON object: {path}")
    return value


def rescore_one(
    lock: dict[str, Any],
    task: dict[str, Any],
    condition: dict[str, Any],
    prior_root: Path,
    output_root: Path,
    source_maps: dict[str, str],
) -> dict[str, Any]:
    task_id = task["id"]
    condition_id = condition["id"]
    prior = prior_root / task_id / condition_id
    output = output_root / task_id / condition_id
    output.mkdir(parents=True, exist_ok=True)

    workspace, target_commit = protocol.prepare_workspace(
        task, condition, source_maps, output
    )
    patch_path = prior / "candidate.patch"
    apply_result = protocol.run(
        ["git", "apply", "--binary", str(patch_path)], cwd=workspace
    )
    if apply_result.returncode != 0:
        raise RuntimeError(
            f"failed to apply {task_id} {condition_id}: {apply_result.stderr}"
        )

    handoff_path = output / "handoff.json"
    shutil.copy2(prior / "handoff.json", handoff_path)
    shutil.copy2(patch_path, output / "candidate.patch")
    task_config = output / "task-config.json"
    task_config.write_text(json.dumps(task, indent=2) + "\n", encoding="utf-8")
    evaluation_path = output / "evaluation.json"
    evaluator = protocol.run(
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
    (output / "evaluator.stdout.txt").write_text(evaluator.stdout, encoding="utf-8")
    (output / "evaluator.stderr.txt").write_text(evaluator.stderr, encoding="utf-8")
    if not evaluation_path.exists():
        raise RuntimeError(f"evaluator produced no result: {evaluator.stderr}")

    prior_record = load_json(prior / "run-record.json")
    record = dict(prior_record)
    record.update(
        {
            "rescored_at": datetime.now(timezone.utc).isoformat(),
            "rescored_with": "model-replication-v0.3.0",
            "target_commit": target_commit,
            "source_patch_sha256": sha256(patch_path),
            "source_handoff_sha256": sha256(prior / "handoff.json"),
            "evaluation": load_json(evaluation_path),
            "workspace_retained_at": str(workspace),
        }
    )
    (output / "run-record.json").write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return record


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lock", type=Path, required=True)
    parser.add_argument("--prior-results", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-map", action="append", default=[])
    args = parser.parse_args()

    lock = load_json(args.lock.resolve())
    protocol.validate_lock(lock)
    prior_root = args.prior_results.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    shutil.copy2(args.lock.resolve(), output / "experiment.lock.json")
    source_maps = protocol.parse_source_maps(args.source_map)
    (output / "source-maps.json").write_text(
        json.dumps(source_maps, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    tasks = {task["id"]: task for task in lock["tasks"]}
    conditions = {condition["id"]: condition for condition in lock["conditions"]}
    records = []
    for index, (task_id, condition_id) in enumerate(lock["execution_order"], 1):
        print(f"[{index}/20] {task_id} {condition_id}", flush=True)
        records.append(
            rescore_one(
                lock,
                tasks[task_id],
                conditions[condition_id],
                prior_root,
                output,
                source_maps,
            )
        )

    summary = protocol.summarize(lock, records)
    summary["candidate_model"] = "gpt-5.6-terra"
    summary["scoring_revision"] = "0.3.0-corrected-before-replication"
    (output / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (output / "result.md").write_text(protocol.render_report(summary), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
