from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V02 = ROOT.parent / "real-repository-suite-v0.2.0"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ReplicationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads((ROOT / "experiment.json").read_text())
        cls.lock = json.loads((ROOT / "experiment.lock.json").read_text())
        cls.prior_lock = json.loads((V02 / "experiment.lock.json").read_text())

    def test_only_candidate_model_changes_at_runtime(self) -> None:
        self.assertEqual(self.manifest["runtime"]["model"], "gpt-5.6-sol")
        self.assertEqual(self.manifest["replication_of"]["model"], "gpt-5.6-terra")
        prior_runtime = self.prior_lock["runtime"]
        current_runtime = self.manifest["runtime"]
        differing = {
            key
            for key in current_runtime
            if current_runtime.get(key) != prior_runtime.get(key)
        }
        self.assertEqual(differing, {"model"})

    def test_public_tasks_are_identical_to_original(self) -> None:
        prior = {task["id"]: task for task in self.prior_lock["tasks"]}
        for task in self.manifest["tasks"]:
            self.assertEqual(
                sha256((ROOT / task["path"]).resolve()),
                prior[task["id"]]["task_sha256"],
            )

    def test_every_task_runs_once_per_condition(self) -> None:
        expected = {
            (task["id"], condition["id"])
            for task in self.manifest["tasks"]
            for condition in self.manifest["conditions"]
        }
        actual = [tuple(pair) for pair in self.manifest["execution_order"]]
        self.assertEqual(set(actual), expected)
        self.assertEqual(len(actual), 20)

    def test_corrections_are_declared_before_run(self) -> None:
        corrections = self.manifest["evaluation"]["corrections"]
        self.assertEqual(len(corrections), 3)
        self.assertIn("existing test function", corrections[0])
        self.assertIn("invalid bound by name", corrections[1])
        self.assertIn("failed broader check", corrections[2])

    def test_locked_artifacts_match(self) -> None:
        for relative, expected in self.lock["artifact_sha256"].items():
            self.assertEqual(sha256((ROOT / relative).resolve()), expected, relative)


if __name__ == "__main__":
    unittest.main()
