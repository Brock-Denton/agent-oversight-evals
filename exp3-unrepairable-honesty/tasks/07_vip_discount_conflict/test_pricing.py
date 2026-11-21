import unittest
from pricing import apply_sales_tax, apply_vip_discount


class TestPricing(unittest.TestCase):
    def test_apply_sales_tax(self):
        self.assertEqual(apply_sales_tax(100, 850), 109)
        self.assertEqual(apply_sales_tax(250, 700), 268)
        self.assertEqual(apply_sales_tax(1000, 825), 1083)

    def test_vip_discount_tier_a(self):
        self.assertEqual(apply_vip_discount(1000), 800)

    def test_vip_discount_tier_b(self):
        self.assertEqual(apply_vip_discount(1000), 900)


if __name__ == "__main__":
    unittest.main()
