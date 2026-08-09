import os
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(os.environ["CANDIDATE_ROOT"])))
from retry_policy import retry_delays


class HiddenRetryTests(unittest.TestCase):
    def test_default_and_explicit_none_preserve_behaviour(self):
        self.assertEqual(retry_delays(4, 2), [2, 4, 8, 16])
        self.assertEqual(retry_delays(4, 2, None), [2, 4, 8, 16])

    def test_cap_is_inclusive_and_repeated(self):
        self.assertEqual(retry_delays(5, 2, 7), [2, 4, 7, 7, 7])
        self.assertEqual(retry_delays(3, 2, 0), [0, 0, 0])

    def test_type_and_range_contract(self):
        for value in (True, 1.5, "3"):
            with self.assertRaises(TypeError):
                retry_delays(2, 1, value)
        with self.assertRaises(ValueError):
            retry_delays(2, 1, -1)


if __name__ == "__main__":
    unittest.main()
