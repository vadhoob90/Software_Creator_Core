import os
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(os.environ["CANDIDATE_ROOT"])))
from priority import parse_priority


class HiddenPriorityTests(unittest.TestCase):
    def test_valid_range(self):
        for value in range(6):
            self.assertEqual(parse_priority({"priority": value}), value)
            self.assertEqual(parse_priority({"priority": str(value)}), value)

    def test_invalid_present_values_raise(self):
        for value in (True, False, "", "high", None, 1.5, -1, 6):
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_priority({"priority": value})

    def test_conversion_failure_preserves_cause(self):
        try:
            parse_priority({"priority": "high"})
        except ValueError as error:
            self.assertIsInstance(error.__cause__, ValueError)
        else:
            self.fail("invalid priority did not fail")


if __name__ == "__main__":
    unittest.main()
