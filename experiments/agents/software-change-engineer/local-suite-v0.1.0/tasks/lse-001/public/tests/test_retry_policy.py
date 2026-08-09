import unittest

from retry_policy import retry_delays


class RetryDelayTests(unittest.TestCase):
    def test_default_schedule(self):
        self.assertEqual(retry_delays(4, 2), [2, 4, 8, 16])

    def test_zero_attempts(self):
        self.assertEqual(retry_delays(0), [])


if __name__ == "__main__":
    unittest.main()
