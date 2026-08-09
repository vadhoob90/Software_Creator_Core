from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest


SUITE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SUITE))

import validate_records as validation


def valid_run() -> dict[str, object]:
    dimensions = {
        name: {"score": 2, "rationale": "Observable, attributable behaviour.", "evidence": ["patch:1"]}
        for name in validation.DIMENSIONS
    }
    gates = {
        name: {"outcome": "pass", "evidence": [f"check:{name}"]}
        for name in validation.HARD_GATES
    }
    return {
        "schema_version": "0.2.0",
        "suite": validation.SUITE,
        "run_id": "lse-101-basic-attempt-1",
        "task": "LSE-101",
        "condition": "basic",
        "definition_version": "0.1.0",
        "seed_commit": "a" * 40,
        "runtime": {
            "provider": "example",
            "model": "example-model",
            "runtime": "example-runtime@1",
            "reasoning_effort": "fixed",
            "sandbox": "workspace-write",
            "approval": "never",
            "parameters_fingerprint": "sha256:example",
        },
        "hard_gates": gates,
        "hard_gate_pass": True,
        "quality_review": {
            "reviewer_id": "reviewer-a",
            "review_package_id": "package-random-a",
            "completed_before_unblinding": True,
            "dimensions": dimensions,
        },
        "quality_total": 10,
        "cost": {
            "input_tokens": 100,
            "cached_input_tokens": 20,
            "output_tokens": 30,
            "total_tokens": 130,
            "elapsed_seconds": 4.5,
            "tool_calls": 3,
            "files_changed": 2,
            "lines_added": 12,
            "lines_deleted": 4,
            "unnecessary_exploration_count": 0,
        },
        "artifacts": {
            "patch": "evidence/patches/example.patch",
            "last_message": "evidence/messages/example.md",
            "review_package": "evidence/review-packages/package-random-a.json",
        },
    }


def valid_aggregate() -> dict[str, object]:
    runs: list[dict[str, object]] = []
    for task in validation.TASKS:
        for condition in validation.CONDITIONS:
            runs.append(
                {
                    "run_id": f"{task.lower()}-{condition}-attempt-1",
                    "task": task,
                    "condition": condition,
                    "run_record": f"evidence/results/{task.lower()}-{condition}.json",
                    "seed_commit": (task[-1].lower() if task[-1].isalpha() else "a") * 40,
                    "runtime_fingerprint": "sha256:fixed-runtime",
                    "hard_gate_pass": True,
                    "quality_scores": {name: 1 for name in validation.DIMENSIONS},
                }
            )
    dimension_summary = {
        name: {
            "basic_score_sum": 20,
            "detailed_score_sum": 20,
            "detailed_wins": 0,
            "ties": 20,
            "basic_wins": 0,
        }
        for name in validation.DIMENSIONS
    }
    return {
        "schema_version": "0.2.0",
        "suite": validation.SUITE,
        "status": "completed",
        "randomisation_seed": "documented-seed",
        "runs": runs,
        "hard_gate_summary": {"basic_passes": 20, "detailed_passes": 20},
        "eligible_pairs": 20,
        "dimension_summary": dimension_summary,
        "decision": "inconclusive",
        "decision_rationale": "Fixture with tied conditions.",
    }


class MatrixTests(unittest.TestCase):
    def test_published_matrix_is_valid(self) -> None:
        matrix = validation.load_json(SUITE / "task-matrix-v0.2.0.json")
        self.assertEqual([], validation.validate_matrix(matrix))

    def test_matrix_requires_four_tasks_per_area(self) -> None:
        matrix = validation.load_json(SUITE / "task-matrix-v0.2.0.json")
        matrix["tasks"][0]["capability_area"] = "test_effectiveness"
        errors = validation.validate_matrix(matrix)
        self.assertTrue(any("expected 4 tasks" in error for error in errors))


class RunTests(unittest.TestCase):
    def test_valid_run(self) -> None:
        self.assertEqual([], validation.validate_run(valid_run()))

    def test_hard_pass_is_derived(self) -> None:
        record = valid_run()
        record["hard_gates"]["hidden_tests"]["outcome"] = "fail"
        self.assertIn("hard_gate_pass: expected derived value False", validation.validate_run(record))

    def test_quality_total_is_derived(self) -> None:
        record = valid_run()
        record["quality_total"] = 9
        self.assertIn("quality_total: expected derived value 10", validation.validate_run(record))

    def test_review_must_precede_unblinding(self) -> None:
        record = valid_run()
        record["quality_review"]["completed_before_unblinding"] = False
        self.assertTrue(any("completed_before_unblinding" in error for error in validation.validate_run(record)))

    def test_failed_run_has_no_quality_score(self) -> None:
        record = valid_run()
        record["hard_gates"]["hidden_tests"]["outcome"] = "fail"
        record["hard_gate_pass"] = False
        record["quality_review"] = None
        record["quality_total"] = None
        self.assertEqual([], validation.validate_run(record))


class AggregateTests(unittest.TestCase):
    def test_valid_completed_aggregate(self) -> None:
        self.assertEqual([], validation.validate_aggregate(valid_aggregate()))

    def test_pair_requires_same_seed(self) -> None:
        record = valid_aggregate()
        record["runs"][1]["seed_commit"] = "b" * 40
        self.assertTrue(any("different seed commits" in error for error in validation.validate_aggregate(record)))

    def test_summary_is_derived(self) -> None:
        record = valid_aggregate()
        record["dimension_summary"]["handoff_usability"]["detailed_wins"] = 1
        self.assertTrue(any("dimension_summary.handoff_usability" in error for error in validation.validate_aggregate(record)))


class SchemaTests(unittest.TestCase):
    def test_schema_documents_parse(self) -> None:
        for path in (SUITE / "schemas").glob("*.schema.json"):
            with self.subTest(path=path.name):
                with path.open(encoding="utf-8") as handle:
                    schema = json.load(handle)
                self.assertEqual("https://json-schema.org/draft/2020-12/schema", schema["$schema"])


if __name__ == "__main__":
    unittest.main()
