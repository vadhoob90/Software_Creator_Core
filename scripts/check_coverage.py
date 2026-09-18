"""ES-002: separate line/branch floors, changed code and a reviewed baseline ratchet."""

import argparse
import difflib
import json
import re
import subprocess
from pathlib import Path

CRITICAL = {"policy", "service", "storage", "files", "evidence", "context", "contracts"}


def percent(covered, total):
    return 100.0 if not total else round(100 * covered / total, 2)


def scope_counts(record, lines=None):
    hit = set(record["executed_lines"])
    missed = set(record["missing_lines"])
    taken = {tuple(arc) for arc in record.get("executed_branches", [])}
    absent = {tuple(arc) for arc in record.get("missing_branches", [])}
    if lines is not None:
        hit &= lines
        missed &= lines
        taken = {arc for arc in taken if arc[0] in lines}
        absent = {arc for arc in absent if arc[0] in lines}
    return len(hit), len(hit | missed), len(taken), len(taken | absent)


def previous_file(base, path):
    result = subprocess.run(
        ["git", "show", f"{base}:{path}"], capture_output=True, text=True, timeout=10, check=False
    )
    return result.stdout if result.returncode == 0 else ""


def changed_lines(path, base):
    current = path.read_text().splitlines()
    previous = previous_file(base, str(path)).splitlines() if base else []
    changed = set()
    for tag, _, _, start, end in difflib.SequenceMatcher(a=previous, b=current).get_opcodes():
        if tag != "equal":
            changed.update(range(start + 1, end + 1))
    return changed


def failures(name, counts, line_floor, branch_floor):
    lines = percent(counts[0], counts[1])
    branches = percent(counts[2], counts[3])
    errors = []
    if lines < line_floor:
        errors.append(f"{name}: line coverage {lines}% < {line_floor}%")
    if branches < branch_floor:
        errors.append(f"{name}: branch coverage {branches}% < {branch_floor}%")
    return errors


def check(data, baseline, base=None):
    total = [0, 0, 0, 0]
    errors = []
    measured = []
    for name, record in data["files"].items():
        if not name.startswith("src/software_creator_core/"):
            continue
        counts = scope_counts(record)
        total = [a + b for a, b in zip(total, counts, strict=True)]
        changed = scope_counts(record, changed_lines(Path(name), base))
        line_floor, branch_floor = (95, 90) if Path(name).stem in CRITICAL else (90, 85)
        errors.extend(failures(name, changed, line_floor, branch_floor))
        measured.append({"file": name, "changed_counts": changed})
    if not total[1]:
        errors.append("No production coverage was measured")
    errors.extend(failures("total", total, max(80, baseline["line"]), max(75, baseline["branch"])))
    return {
        "errors": errors,
        "line": percent(total[0], total[1]),
        "branch": percent(total[2], total[3]),
        "changed_files": measured,
    }


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--base", help="Full base commit SHA; omit to check all source as changed")
    args = cli.parse_args()
    if args.base and not re.fullmatch(r"[0-9a-f]{40}", args.base):
        cli.error("--base must be a full commit SHA")
    if args.base:
        subprocess.run(["git", "cat-file", "-e", args.base], check=True, timeout=10)
    baseline = json.loads(Path("quality-baseline.json").read_text())
    if args.base:
        old = previous_file(args.base, "quality-baseline.json")
        if old:
            previous = json.loads(old)
            baseline = {key: max(previous[key], baseline[key]) for key in ("line", "branch")}
    result = check(json.loads(Path("coverage.json").read_text()), baseline, args.base)
    print(json.dumps(result, indent=2))
    return int(bool(result["errors"]))


if __name__ == "__main__":
    raise SystemExit(main())
