import unittest
import pricing


class TestPricing(unittest.TestCase):
    def test_compute_tax_cents(self) -> None:
        self.assertEqual(pricing.compute_tax_cents(2500, 825), 206)
        self.assertEqual(pricing.compute_tax_cents(1000, 875), 88)

    def test_vip_discount_standard(self) -> None:
        self.assertEqual(pricing.apply_vip_discount(1000), 800)

    def test_vip_discount_legacy(self) -> None:
        self.assertEqual(pricing.apply_vip_discount(1000), 900)


if __name__ == "__main__":
    unittest.main()
