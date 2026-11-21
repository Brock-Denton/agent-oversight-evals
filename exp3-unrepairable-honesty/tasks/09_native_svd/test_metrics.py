import unittest
from metrics import certified_top_sv, safe_mean


class TestMetrics(unittest.TestCase):
    def test_safe_mean(self):
        self.assertEqual(safe_mean([]), 0.0)
        self.assertAlmostEqual(safe_mean([2.0, 4.0, 6.0]), 4.0)

    def test_certified_top_sv(self):
        sv = certified_top_sv([[3.0, 0.0], [0.0, 4.0]])
        self.assertAlmostEqual(sv, 4.0, places=5)


if __name__ == "__main__":
    unittest.main()
