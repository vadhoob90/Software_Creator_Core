"""Require >=80% raw kills and explain every survivor with a hash-bound equivalence review."""

import hashlib
import json
import subprocess
from pathlib import Path

REQUIRED = {"policy", "context", "files", "evidence", "service", "storage", "contracts"}


def diff_digest(output):
    # The first line contains a changing execution status, not the mutation itself.
    lines = output.splitlines()
    diff = "\n".join(lines[1:]) + "\n"
    if not diff.lstrip().startswith("--- ") or "\n+++ " not in diff:
        raise ValueError("Expected a complete unified mutation diff")
    return "sha256:" + hashlib.sha256(diff.encode()).hexdigest()


def inspect_diff(name):
    result = subprocess.run(
        ["mutmut", "show", name], capture_output=True, text=True, timeout=20, check=True
    )
    return diff_digest(result.stdout)


def review_errors(statuses, exemptions, inspect):
    errors = []
    for name, review in exemptions.items():
        if statuses.get(name) != 0:
            errors.append(f"Stale exemption: {name}")
        elif not review.get("reason", "").strip():
            errors.append(f"Missing equivalence rationale: {name}")
        elif inspect(name) != review.get("diff_sha256"):
            errors.append(f"Changed mutation diff: {name}")
    for name, status in statuses.items():
        if status != 1 and not (status == 0 and name in exemptions):
            errors.append(f"Unexplained or incomplete mutation: {name}")
    return errors


def load_reports(paths):
    statuses, errors = {}, []
    for path in paths:
        metadata = json.loads(path.read_text())
        entries = metadata["exit_code_by_key"]
        if statuses.keys() & entries.keys():
            errors.append("Duplicate mutation identities")
        statuses.update(entries)
    return statuses, errors


def check(paths, exemptions=None, inspect=inspect_diff, required=()):
    paths = list(paths)
    statuses, errors = load_reports(paths)
    missing = set(required) - {p.name.removesuffix(".py.meta") for p in paths}
    if missing:
        errors.append(f"Missing module reports: {sorted(missing)}")
    errors.extend(review_errors(statuses, exemptions or {}, inspect))
    killed = sum(status == 1 for status in statuses.values())
    score = round(100 * killed / len(statuses), 2) if statuses else 0
    if score < 80:
        errors.append("Raw mutation score below 80%")
    return {
        "total": len(statuses),
        "killed": killed,
        "raw_score": score,
        "reviewed_equivalents": len(exemptions or {}),
        "errors": errors,
        "passed": bool(statuses) and not errors,
    }


def main():
    exemptions = json.loads(Path("mutation-equivalents.json").read_text())
    result = check(
        Path("mutants/src/software_creator_core").glob("*.meta"),
        exemptions,
        required=REQUIRED,
    )
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
