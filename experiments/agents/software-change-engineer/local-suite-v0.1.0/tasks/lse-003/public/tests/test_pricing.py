import unittest

from pricing import final_price


class PricingTests(unittest.TestCase):
    def test_no_discount(self):
        self.assertEqual(final_price(1000), 1000)

    def test_member_discount(self):
        self.assertEqual(final_price(1000, member=True), 900)

    def test_coupon_discount(self):
        self.assertEqual(final_price(1000, coupon_percent=20), 800)


if __name__ == "__main__":
    unittest.main()
