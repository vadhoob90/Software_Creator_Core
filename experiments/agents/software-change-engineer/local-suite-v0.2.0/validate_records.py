#!/usr/bin/env python3
"""Validate the v0.2.0 task matrix and evaluation evidence records.

The JSON Schemas describe the portable record shape. This module additionally
enforces derived values and matched-pair invariants that are clearer in code.
It intentionally uses only the Python standard library.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
from typing import Any


SCHEMA_VERSION = "0.2.0"
SUITE = "pdlc-core.sce-local-suite@0.2.0"
TASKS = tuple(f"LSE-{number:03d}" for number in range(101, 121))
CONDITIONS = ("basic", "detailed")
AREAS = (
    "comprehension_scope",
    "test_effectiveness",
    "failure_traceability",
    "lifecycle_compatibility",
    "authority_governance",
)
DIMENSIONS = (
    "comprehension_scope",
    "test_effectiveness",
    "failure_evidence_integrity",
    "lifecycle_compatibility",
    "handoff_usability",
)
HARD_GATES = (
    "public_tests",
    "hidden_tests",
    "prohibited_actions",
    "controls_intact",
    "evidence_integrity",
    "critical_safety_compatibility",
)
RUNTIME_FIELDS = (
    "provider",
    "model",
    "runtime",
    "reasoning_effort",
    "sandbox",
    "approval",
    "parameters_fingerprint",
)
COST_FIELDS = (
    "input_tokens",
    "cached_input_tokens",
    "output_tokens",
    "total_tokens",
    "elapsed_seconds",
    "tool_calls",
    "files_changed",
    "lines_added",
    "lines_deleted",
    "unnecessary_exploration_count",
)
RUN_FIELDS = {
    "schema_version",
    "suite",
    "run_id",
    "task",
    "condition",
    "definition_version",
    "seed_commit",
    "runtime",
    "hard_gates",
    "hard_gate_pass",
    "quality_review",
    "quality_total",
    "cost",
    "artifacts",
}
AGGREGATE_FIELDS = {
    "schema_version",
    "suite",
    "status",
    "randomisation_seed",
    "runs",
    "hard_gate_summary",
    "eligible_pairs",
    "dimension_summary",
    "decision",
    "decision_rationale",
}
SHA1_PATTERN = re.compile(r"^[0-9a-f]{40}$")


def _mapping(value: Any, path: str, errors: list[str]) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        errors.append(f"{path}: expected object")
        return None
    return value


def _exact_keys(value: dict[str, Any], expected: set[str] | tuple[str, ...], path: str, errors: list[str]) -> None:
    expected_set = set(expected)
    missing = sorted(expected_set - set(value))
    extra = sorted(set(value) - expected_set)
    if missing:
        errors.append(f"{path}: missing keys {missing}")
    if extra:
        errors.append(f"{path}: unexpected keys {extra}")


def _nonempty_string(value: Any, path: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path}: expected non-empty string")


def _nonempty_strings(value: Any, path: str, errors: list[str]) -> None:
    if not isinstance(value, list) or not value:
        errors.append(f"{path}: expected non-empty string array")
        return
    for index, item in enumerate(value):
        _nonempty_string(item, f"{path}[{index}]", errors)


def _nonnegative_number(value: Any, path: str, errors: list[str], *, integer: bool) -> None:
    expected = int if integer else (int, float)
    if isinstance(value, bool) or not isinstance(value, expected) or value < 0:
        kind = "non-negative integer" if integer else "non-negative number"
        errors.append(f"{path}: expected {kind}")


def _header(record: dict[str, Any], errors: list[str]) -> None:
    if record.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version: expected {SCHEMA_VERSION!r}")
    if record.get("suite") != SUITE:
        errors.append(f"suite: expected {SUITE!r}")


def validate_matrix(data: Any) -> list[str]:
    errors: list[str] = []
    matrix = _mapping(data, "$", errors)
    if matrix is None:
        return errors
    _header(matrix, errors)

    areas = matrix.get("capability_areas")
    if areas != list(AREAS):
        errors.append("capability_areas: expected the five canonical areas in order")

    tasks = matrix.get("tasks")
    if not isinstance(tasks, list):
        errors.append("tasks: expected array")
        return errors
    if len(tasks) != 20:
        errors.append(f"tasks: expected 20 entries, found {len(tasks)}")

    seen: list[str] = []
    area_counts: Counter[str] = Counter()
    required = {
        "id",
        "capability_area",
        "title",
        "scenario",
        "judgment_under_test",
        "standards",
        "public_evidence",
        "hidden_evidence",
        "prohibited_actions",
        "quality_emphasis",
    }
    for index, value in enumerate(tasks):
        path = f"tasks[{index}]"
        task = _mapping(value, path, errors)
        if task is None:
            continue
        _exact_keys(task, required, path, errors)
        task_id = task.get("id")
        if task_id not in TASKS:
            errors.append(f"{path}.id: unknown task {task_id!r}")
        elif task_id in seen:
            errors.append(f"{path}.id: duplicate task {task_id}")
        else:
            seen.append(task_id)
        area = task.get("capability_area")
        if area not in AREAS:
            errors.append(f"{path}.capability_area: unknown area {area!r}")
        else:
            area_counts[area] += 1
        for field in ("title", "scenario", "judgment_under_test"):
            _nonempty_string(task.get(field), f"{path}.{field}", errors)
        for field in ("standards", "public_evidence", "hidden_evidence", "prohibited_actions"):
            _nonempty_strings(task.get(field), f"{path}.{field}", errors)
        emphasis = task.get("quality_emphasis")
        _nonempty_strings(emphasis, f"{path}.quality_emphasis", errors)
        if isinstance(emphasis, list):
            unknown = sorted(set(emphasis) - set(DIMENSIONS))
            if unknown:
                errors.append(f"{path}.quality_emphasis: unknown dimensions {unknown}")

    missing_tasks = sorted(set(TASKS) - set(seen))
    if missing_tasks:
        errors.append(f"tasks: missing canonical tasks {missing_tasks}")
    for area in AREAS:
        if area_counts[area] != 4:
            errors.append(f"capability_area {area}: expected 4 tasks, found {area_counts[area]}")
    return errors


def validate_run(data: Any) -> list[str]:
    errors: list[str] = []
    record = _mapping(data, "$", errors)
    if record is None:
        return errors
    _exact_keys(record, RUN_FIELDS, "$", errors)
    _header(record, errors)

    _nonempty_string(record.get("run_id"), "run_id", errors)
    if record.get("task") not in TASKS:
        errors.append(f"task: unknown task {record.get('task')!r}")
    if record.get("condition") not in CONDITIONS:
        errors.append(f"condition: expected one of {CONDITIONS}")
    _nonempty_string(record.get("definition_version"), "definition_version", errors)
    if not isinstance(record.get("seed_commit"), str) or not SHA1_PATTERN.fullmatch(record["seed_commit"]):
        errors.append("seed_commit: expected a 40-character lowercase hexadecimal commit")

    runtime = _mapping(record.get("runtime"), "runtime", errors)
    if runtime is not None:
        _exact_keys(runtime, RUNTIME_FIELDS, "runtime", errors)
        for field in RUNTIME_FIELDS:
            _nonempty_string(runtime.get(field), f"runtime.{field}", errors)

    gates = _mapping(record.get("hard_gates"), "hard_gates", errors)
    derived_hard_pass = False
    if gates is not None:
        _exact_keys(gates, HARD_GATES, "hard_gates", errors)
        outcomes: list[bool] = []
        for name in HARD_GATES:
            gate = _mapping(gates.get(name), f"hard_gates.{name}", errors)
            if gate is None:
                continue
            _exact_keys(gate, {"outcome", "evidence"}, f"hard_gates.{name}", errors)
            outcome = gate.get("outcome")
            if outcome not in ("pass", "fail"):
                errors.append(f"hard_gates.{name}.outcome: expected 'pass' or 'fail'")
            else:
                outcomes.append(outcome == "pass")
            _nonempty_strings(gate.get("evidence"), f"hard_gates.{name}.evidence", errors)
        derived_hard_pass = len(outcomes) == len(HARD_GATES) and all(outcomes)
    if not isinstance(record.get("hard_gate_pass"), bool):
        errors.append("hard_gate_pass: expected boolean")
    elif gates is not None and record["hard_gate_pass"] != derived_hard_pass:
        errors.append(f"hard_gate_pass: expected derived value {derived_hard_pass}")

    hard_pass_claim = record.get("hard_gate_pass") is True
    review_value = record.get("quality_review")
    review: dict[str, Any] | None = None
    derived_quality_total = 0
    if hard_pass_claim:
        review = _mapping(review_value, "quality_review", errors)
    elif review_value is not None:
        errors.append("quality_review: expected null when hard_gate_pass is false")
    if review is not None:
        _exact_keys(
            review,
            {"reviewer_id", "review_package_id", "completed_before_unblinding", "dimensions"},
            "quality_review",
            errors,
        )
        _nonempty_string(review.get("reviewer_id"), "quality_review.reviewer_id", errors)
        _nonempty_string(review.get("review_package_id"), "quality_review.review_package_id", errors)
        if review.get("completed_before_unblinding") is not True:
            errors.append("quality_review.completed_before_unblinding: expected true")
        dimensions = _mapping(review.get("dimensions"), "quality_review.dimensions", errors)
        if dimensions is not None:
            _exact_keys(dimensions, DIMENSIONS, "quality_review.dimensions", errors)
            for name in DIMENSIONS:
                dimension = _mapping(dimensions.get(name), f"quality_review.dimensions.{name}", errors)
                if dimension is None:
                    continue
                _exact_keys(dimension, {"score", "rationale", "evidence"}, f"quality_review.dimensions.{name}", errors)
                score = dimension.get("score")
                if isinstance(score, bool) or not isinstance(score, int) or score not in (0, 1, 2):
                    errors.append(f"quality_review.dimensions.{name}.score: expected 0, 1, or 2")
                else:
                    derived_quality_total += score
                _nonempty_string(dimension.get("rationale"), f"quality_review.dimensions.{name}.rationale", errors)
                evidence = dimension.get("evidence")
                if not isinstance(evidence, list) or any(not isinstance(item, str) or not item.strip() for item in evidence):
                    errors.append(f"quality_review.dimensions.{name}.evidence: expected string array")
                elif score in (0, 2) and not evidence:
                    errors.append(f"quality_review.dimensions.{name}.evidence: required for score {score}")
    if hard_pass_claim:
        if isinstance(record.get("quality_total"), bool) or not isinstance(record.get("quality_total"), int):
            errors.append("quality_total: expected integer when hard_gate_pass is true")
        elif review is not None and record["quality_total"] != derived_quality_total:
            errors.append(f"quality_total: expected derived value {derived_quality_total}")
    elif record.get("quality_total") is not None:
        errors.append("quality_total: expected null when hard_gate_pass is false")

    cost = _mapping(record.get("cost"), "cost", errors)
    if cost is not None:
        _exact_keys(cost, COST_FIELDS, "cost", errors)
        for field in COST_FIELDS:
            _nonnegative_number(cost.get(field), f"cost.{field}", errors, integer=field != "elapsed_seconds")
        if all(isinstance(cost.get(name), int) and not isinstance(cost.get(name), bool) for name in ("input_tokens", "output_tokens", "total_tokens")):
            expected_total = cost["input_tokens"] + cost["output_tokens"]
            if cost["total_tokens"] != expected_total:
                errors.append(f"cost.total_tokens: expected input_tokens + output_tokens ({expected_total})")

    artifacts = _mapping(record.get("artifacts"), "artifacts", errors)
    if artifacts is not None:
        _exact_keys(artifacts, {"patch", "last_message", "review_package"}, "artifacts", errors)
        for field in ("patch", "last_message", "review_package"):
            _nonempty_string(artifacts.get(field), f"artifacts.{field}", errors)
    return errors


def validate_aggregate(data: Any) -> list[str]:
    errors: list[str] = []
    record = _mapping(data, "$", errors)
    if record is None:
        return errors
    unknown = set(record) - AGGREGATE_FIELDS
    required = AGGREGATE_FIELDS - {"decision", "decision_rationale"}
    missing = required - set(record)
    if missing:
        errors.append(f"$: missing keys {sorted(missing)}")
    if unknown:
        errors.append(f"$: unexpected keys {sorted(unknown)}")
    _header(record, errors)

    status = record.get("status")
    if status not in ("running", "completed"):
        errors.append("status: expected 'running' or 'completed'")
    _nonempty_string(record.get("randomisation_seed"), "randomisation_seed", errors)
    if status == "completed":
        if record.get("decision") not in ("retain", "shorten", "reshape", "reject", "inconclusive"):
            errors.append("decision: required canonical decision for completed result")
        _nonempty_string(record.get("decision_rationale"), "decision_rationale", errors)

    runs = record.get("runs")
    if not isinstance(runs, list):
        errors.append("runs: expected array")
        return errors
    if status == "completed" and len(runs) != 40:
        errors.append(f"runs: completed result requires 40 runs, found {len(runs)}")

    run_ids: set[str] = set()
    by_pair: dict[tuple[str, str], dict[str, Any]] = {}
    summary_keys = {
        "run_id",
        "task",
        "condition",
        "run_record",
        "seed_commit",
        "runtime_fingerprint",
        "hard_gate_pass",
        "quality_scores",
    }
    for index, value in enumerate(runs):
        path = f"runs[{index}]"
        run = _mapping(value, path, errors)
        if run is None:
            continue
        _exact_keys(run, summary_keys, path, errors)
        run_id = run.get("run_id")
        _nonempty_string(run_id, f"{path}.run_id", errors)
        if isinstance(run_id, str):
            if run_id in run_ids:
                errors.append(f"{path}.run_id: duplicate {run_id!r}")
            run_ids.add(run_id)
        task = run.get("task")
        condition = run.get("condition")
        if task not in TASKS:
            errors.append(f"{path}.task: unknown task {task!r}")
        if condition not in CONDITIONS:
            errors.append(f"{path}.condition: unknown condition {condition!r}")
        if task in TASKS and condition in CONDITIONS:
            key = (task, condition)
            if key in by_pair:
                errors.append(f"{path}: duplicate task-condition {key}")
            by_pair[key] = run
        for field in ("run_record", "runtime_fingerprint"):
            _nonempty_string(run.get(field), f"{path}.{field}", errors)
        if not isinstance(run.get("seed_commit"), str) or not SHA1_PATTERN.fullmatch(run["seed_commit"]):
            errors.append(f"{path}.seed_commit: expected commit SHA")
        if not isinstance(run.get("hard_gate_pass"), bool):
            errors.append(f"{path}.hard_gate_pass: expected boolean")
        scores_value = run.get("quality_scores")
        scores: dict[str, Any] | None = None
        if run.get("hard_gate_pass") is True:
            scores = _mapping(scores_value, f"{path}.quality_scores", errors)
        elif scores_value is not None:
            errors.append(f"{path}.quality_scores: expected null when hard_gate_pass is false")
        if scores is not None:
            _exact_keys(scores, DIMENSIONS, f"{path}.quality_scores", errors)
            for name in DIMENSIONS:
                score = scores.get(name)
                if isinstance(score, bool) or not isinstance(score, int) or score not in (0, 1, 2):
                    errors.append(f"{path}.quality_scores.{name}: expected 0, 1, or 2")

    if status == "completed":
        expected_pairs = {(task, condition) for task in TASKS for condition in CONDITIONS}
        missing_pairs = sorted(expected_pairs - set(by_pair))
        if missing_pairs:
            errors.append(f"runs: missing task-condition pairs {missing_pairs}")

    for task in TASKS:
        basic = by_pair.get((task, "basic"))
        detailed = by_pair.get((task, "detailed"))
        if basic is None or detailed is None:
            continue
        if basic.get("seed_commit") != detailed.get("seed_commit"):
            errors.append(f"{task}: matched conditions have different seed commits")
        if basic.get("runtime_fingerprint") != detailed.get("runtime_fingerprint"):
            errors.append(f"{task}: matched conditions have different runtime fingerprints")

    derived_basic_passes = sum(run.get("hard_gate_pass") is True for run in by_pair.values() if run.get("condition") == "basic")
    derived_detailed_passes = sum(run.get("hard_gate_pass") is True for run in by_pair.values() if run.get("condition") == "detailed")
    hard_summary = _mapping(record.get("hard_gate_summary"), "hard_gate_summary", errors)
    if hard_summary is not None:
        _exact_keys(hard_summary, {"basic_passes", "detailed_passes"}, "hard_gate_summary", errors)
        expected = {"basic_passes": derived_basic_passes, "detailed_passes": derived_detailed_passes}
        if hard_summary != expected:
            errors.append(f"hard_gate_summary: expected derived value {expected}")

    eligible_tasks = [
        task
        for task in TASKS
        if by_pair.get((task, "basic"), {}).get("hard_gate_pass") is True
        and by_pair.get((task, "detailed"), {}).get("hard_gate_pass") is True
    ]
    if record.get("eligible_pairs") != len(eligible_tasks):
        errors.append(f"eligible_pairs: expected derived value {len(eligible_tasks)}")

    dimension_summary = _mapping(record.get("dimension_summary"), "dimension_summary", errors)
    if dimension_summary is not None:
        _exact_keys(dimension_summary, DIMENSIONS, "dimension_summary", errors)
        for dimension in DIMENSIONS:
            score_pairs: list[tuple[int, int]] = []
            for task in eligible_tasks:
                basic_scores_value = by_pair[(task, "basic")].get("quality_scores")
                detailed_scores_value = by_pair[(task, "detailed")].get("quality_scores")
                if not isinstance(basic_scores_value, dict) or not isinstance(detailed_scores_value, dict):
                    continue
                basic_score = basic_scores_value.get(dimension)
                detailed_score = detailed_scores_value.get(dimension)
                if (
                    isinstance(basic_score, int)
                    and not isinstance(basic_score, bool)
                    and basic_score in (0, 1, 2)
                    and isinstance(detailed_score, int)
                    and not isinstance(detailed_score, bool)
                    and detailed_score in (0, 1, 2)
                ):
                    score_pairs.append((basic_score, detailed_score))
            basic_scores = [pair[0] for pair in score_pairs]
            detailed_scores = [pair[1] for pair in score_pairs]
            derived = {
                "basic_score_sum": sum(basic_scores),
                "detailed_score_sum": sum(detailed_scores),
                "detailed_wins": sum(detailed > basic for basic, detailed in zip(basic_scores, detailed_scores)),
                "ties": sum(detailed == basic for basic, detailed in zip(basic_scores, detailed_scores)),
                "basic_wins": sum(detailed < basic for basic, detailed in zip(basic_scores, detailed_scores)),
            }
            if dimension_summary.get(dimension) != derived:
                errors.append(f"dimension_summary.{dimension}: expected derived value {derived}")
    return errors


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=("matrix", "run", "aggregate"))
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    validators = {"matrix": validate_matrix, "run": validate_run, "aggregate": validate_aggregate}
    errors = validators[args.kind](load_json(args.path))
    if errors:
        for error in errors:
            print(error)
        return 1
    print(f"valid {args.kind}: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
