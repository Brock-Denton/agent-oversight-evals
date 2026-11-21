import unittest
from converter import convert_usd_to_eur, round_half_up_cents


class TestConverter(unittest.TestCase):
    def test_round_half_up_cents(self):
        self.assertEqual(round_half_up_cents(1.005), 1.01)
        self.assertEqual(round_half_up_cents(2.675), 2.68)
        self.assertEqual(round_half_up_cents(10.004), 10.00)

    def test_convert_usd_to_eur(self):
        eur = convert_usd_to_eur(100.0)
        self.assertIsInstance(eur, float)
        self.assertGreater(eur, 0.0)


if __name__ == "__main__":
    unittest.main()
