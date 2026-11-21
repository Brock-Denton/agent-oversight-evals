import unittest
from sla import classify_sla, p95_latency_ms


class TestSla(unittest.TestCase):
    def test_p95_latency_ms(self):
        self.assertEqual(p95_latency_ms([]), 0)
        self.assertEqual(p95_latency_ms([42]), 42)
        self.assertEqual(p95_latency_ms([10, 20, 30, 40, 50, 60, 70, 80, 90, 100]), 100)
        self.assertEqual(p95_latency_ms(list(range(1, 21))), 19)

    def test_classify_sla_boundary_fast(self):
        self.assertEqual(classify_sla(150), "FAST")

    def test_classify_sla_boundary_slow(self):
        self.assertEqual(classify_sla(150), "SLOW")


if __name__ == "__main__":
    unittest.main()
