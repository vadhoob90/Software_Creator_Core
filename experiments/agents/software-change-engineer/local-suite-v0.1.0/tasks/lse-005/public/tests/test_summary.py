import unittest

from summary import build_summary


class SummaryTests(unittest.TestCase):
    def test_existing_summary(self):
        result = build_summary(["a", "b"])
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["messages"], ["a", "b"])


if __name__ == "__main__":
    unittest.main()
