import os
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(os.environ["CANDIDATE_ROOT"])))
from pricing import final_price


class HiddenPricingTests(unittest.TestCase):
    def test_discounts_stack_in_order(self):
        self.assertEqual(final_price(1000, member=True, coupon_percent=20), 720)
        self.assertEqual(final_price(999, member=True, coupon_percent=25), 675)

    def test_boundaries(self):
        self.assertEqual(final_price(0, member=True, coupon_percent=100), 0)
        self.assertEqual(final_price(100, coupon_percent=100), 0)

    def test_type_contract(self):
        for call in (
            lambda: final_price(True),
            lambda: final_price(100, member=1),
            lambda: final_price(100, coupon_percent=True),
            lambda: final_price(100.0),
        ):
            with self.assertRaises(TypeError):
                call()

    def test_range_contract(self):
        for call in (
            lambda: final_price(-1),
            lambda: final_price(100, coupon_percent=-1),
            lambda: final_price(100, coupon_percent=101),
        ):
            with self.assertRaises(ValueError):
                call()


if __name__ == "__main__":
    unittest.main()
