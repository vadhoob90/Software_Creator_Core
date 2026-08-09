import unittest

from priority import parse_priority


class PriorityTests(unittest.TestCase):
    def test_missing_defaults_to_zero(self):
        self.assertEqual(parse_priority({}), 0)

    def test_integer_string_is_accepted(self):
        self.assertEqual(parse_priority({"priority": "3"}), 3)


if __name__ == "__main__":
    unittest.main()
