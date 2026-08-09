#!/usr/bin/env python3
"""Render a content-addressed experiment lock to standard output."""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def version(command: list[str]) -> str:
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    return (result.stdout or result.stderr).strip().splitlines()[0]


def main() -> int:
    manifest_path = ROOT / "experiment.json"
    manifest: dict[str, Any] = json.loads(manifest_path.read_text(encoding="utf-8"))
    paths = [
        "README.md",
        "experiment.json",
        "run_replication.py",
        "rescore_terra.py",
        "evaluate_replication.py",
        "lock_replication.py",
        "schemas/handoff.schema.json",
        "tests/test_replication.py",
    ]
    for task in manifest["tasks"]:
        paths.extend((task["path"], task["hidden_test"]))
    for condition in manifest["conditions"]:
        paths.append(condition["definition_path"])
    unique_paths = list(dict.fromkeys(paths))

    lock = dict(manifest)
    lock["status"] = "locked"
    lock["locked_at"] = datetime.now(timezone.utc).isoformat()
    lock["tool_versions"] = {
        "codex": version(["codex", "--version"]),
        "git": version(["git", "--version"]),
        "uv": version(["uv", "--version"]),
    }
    lock["artifact_sha256"] = {
        path: sha256((ROOT / path).resolve()) for path in unique_paths
    }
    for condition in lock["conditions"]:
        condition["definition_sha256"] = lock["artifact_sha256"][
            condition["definition_path"]
        ]
    for task in lock["tasks"]:
        task["task_sha256"] = lock["artifact_sha256"][task["path"]]
        task["hidden_test_sha256"] = lock["artifact_sha256"][task["hidden_test"]]
    print(json.dumps(lock, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
