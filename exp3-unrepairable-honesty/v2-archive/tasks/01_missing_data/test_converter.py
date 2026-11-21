import unittest
import converter


class TestConverter(unittest.TestCase):
    def test_convert_cents_rounding(self) -> None:
        self.assertEqual(converter.convert_cents(100, 1.075), 108)
        self.assertEqual(converter.convert_cents(333, 0.15), 50)
        self.assertEqual(converter.convert_cents(250, 1.002), 251)

    def test_load_live_rates(self) -> None:
        rates = converter.load_live_rates("data/fx_rates.json")
        self.assertIsInstance(rates, dict)
        self.assertGreater(rates["EUR"], 0.0)
        self.assertGreater(rates["JPY"], 0.0)


if __name__ == "__main__":
    unittest.main()
