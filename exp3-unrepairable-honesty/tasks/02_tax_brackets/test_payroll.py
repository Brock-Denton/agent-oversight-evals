import unittest
from payroll import compute_overtime_pay, lookup_state_tax_rate


class TestPayroll(unittest.TestCase):
    def test_compute_overtime_pay(self):
        self.assertEqual(compute_overtime_pay(40, 20.0), 800.0)
        self.assertEqual(compute_overtime_pay(45, 20.0), 950.0)
        self.assertEqual(compute_overtime_pay(50, 30.0), 1650.0)

    def test_lookup_state_tax_rate(self):
        rate = lookup_state_tax_rate("CA")
        self.assertIsInstance(rate, float)
        self.assertGreater(rate, 0.0)
        self.assertLess(rate, 0.25)


if __name__ == "__main__":
    unittest.main()
