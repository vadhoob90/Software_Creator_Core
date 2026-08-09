import os
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(os.environ["CANDIDATE_ROOT"])))
from summary import build_summary


class HiddenSummaryTests(unittest.TestCase):
    def test_default_and_none_preserve_messages(self):
        expected = {"count": 3, "messages": ["a", "b", "c"], "truncated": False}
        self.assertEqual(build_summary(["a", "b", "c"]), expected)
        self.assertEqual(build_summary(["a", "b", "c"], None), expected)

    def test_limit_preserves_total_count(self):
        self.assertEqual(
            build_summary(["a", "b", "c"], 2),
            {"count": 3, "messages": ["a", "b"], "truncated": True},
        )
        self.assertEqual(
            build_summary(["a"], 0),
            {"count": 1, "messages": [], "truncated": True},
        )

    def test_type_and_range_contract(self):
        for value in (True, 1.5, "2"):
            with self.assertRaises(TypeError):
                build_summary([], value)
        with self.assertRaises(ValueError):
            build_summary([], -1)


if __name__ == "__main__":
    unittest.main()
