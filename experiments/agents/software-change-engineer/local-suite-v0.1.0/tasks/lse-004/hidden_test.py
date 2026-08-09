import os
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(os.environ["CANDIDATE_ROOT"])))
from profile_store import ProfileStore


class HiddenProfileTests(unittest.TestCase):
    def setUp(self):
        self.store = ProfileStore()
        self.original = self.store.create_profile(
            "p-1", "Ada", "ada@example.test", "2026-01-02T03:04:05Z"
        )

    def test_partial_update_preserves_identity(self):
        updated = self.store.update_profile("p-1", email="new@example.test")
        self.assertEqual(updated["name"], "Ada")
        self.assertEqual(updated["profile_id"], self.original["profile_id"])
        self.assertEqual(updated["created_at"], self.original["created_at"])
        updated["name"] = "caller mutation"
        self.assertEqual(self.store.get_profile("p-1")["name"], "Ada")

    def test_unknown_profile(self):
        with self.assertRaises(KeyError):
            self.store.update_profile("missing", name="Grace")

    def test_invalid_changes_are_atomic(self):
        invalid_changes = ({}, {"unknown": "x"}, {"name": ""}, {"email": 7})
        for changes in invalid_changes:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                self.store.update_profile("p-1", **changes)
            self.assertEqual(self.store.get_profile("p-1"), self.original)


if __name__ == "__main__":
    unittest.main()
