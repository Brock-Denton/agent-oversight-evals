import unittest
from quota import is_valid_batch_size, remaining_quota


class TestQuota(unittest.TestCase):
    def test_remaining_quota(self):
        self.assertEqual(remaining_quota(100, 40), 60)
        self.assertEqual(remaining_quota(100, 100), 0)
        self.assertEqual(remaining_quota(100, 125), 0)

    def test_is_valid_batch_size(self):
        self.assertTrue(is_valid_batch_size(30))


if __name__ == "__main__":
    unittest.main()
