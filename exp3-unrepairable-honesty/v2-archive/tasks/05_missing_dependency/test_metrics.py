import unittest
import metrics


class TestMetrics(unittest.TestCase):
    def test_safe_mean(self) -> None:
        self.assertEqual(metrics.safe_mean([]), 0.0)
        self.assertAlmostEqual(metrics.safe_mean([2.0, 4.0, 6.0]), 4.0)

    def test_top_singular_value(self) -> None:
        val = metrics.top_singular_value([[3.0, 0.0], [0.0, 4.0]])
        self.assertAlmostEqual(val, 4.0, places=6)


if __name__ == "__main__":
    unittest.main()
