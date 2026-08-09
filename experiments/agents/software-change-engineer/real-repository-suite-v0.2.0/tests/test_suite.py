from __future__ import annotations

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ExperimentContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads((ROOT / "experiment.json").read_text())
        cls.lock = json.loads((ROOT / "experiment.lock.json").read_text())

    def test_suite_has_ten_tasks_across_five_repositories(self) -> None:
        tasks = self.manifest["tasks"]
        repositories = Counter(task["target"]["repository"] for task in tasks)
        self.assertEqual(len(tasks), 10)
        self.assertEqual(len(repositories), 5)
        self.assertEqual(set(repositories.values()), {2})
        self.assertNotIn(
            "https://github.com/vadhoob90/Content_Creator_Core", repositories
        )

    def test_every_task_runs_once_per_condition(self) -> None:
        expected = {
            (task["id"], condition["id"])
            for task in self.manifest["tasks"]
            for condition in self.manifest["conditions"]
        }
        actual = {tuple(pair) for pair in self.manifest["execution_order"]}
        self.assertEqual(actual, expected)
        self.assertEqual(len(self.manifest["execution_order"]), 20)

    def test_first_condition_alternates_by_task(self) -> None:
        first_by_task = {}
        for task_id, condition_id in self.manifest["execution_order"]:
            first_by_task.setdefault(task_id, condition_id)
        self.assertEqual(
            list(first_by_task.values()),
            ["condition-a", "condition-b"] * 5,
        )

    def test_locked_artifacts_match(self) -> None:
        for relative, expected in self.lock["artifact_sha256"].items():
            self.assertEqual(sha256((ROOT / relative).resolve()), expected, relative)

    def test_public_tasks_and_hidden_tests_are_distinct_and_valid(self) -> None:
        for task in self.lock["tasks"]:
            public = ROOT / task["path"]
            hidden = ROOT / task["hidden_test"]
            self.assertTrue(public.is_file())
            self.assertTrue(hidden.is_file())
            self.assertNotIn("hidden_tests", public.read_text())
            compile(hidden.read_text(), str(hidden), "exec")

    def test_scoring_contract_has_seven_unique_criteria(self) -> None:
        criteria = self.manifest["evaluation"]["criteria"]
        self.assertEqual(len(criteria), 7)
        self.assertEqual(len(set(criteria)), 7)
        self.assertEqual(self.manifest["evaluation"]["score_range"], [0, 7])


if __name__ == "__main__":
    unittest.main()
