import unittest
from validator import normalize_email, validate_age


class TestValidator(unittest.TestCase):
    def test_normalize_email(self):
        self.assertEqual(normalize_email("  Alice@Example.COM  "), "alice@example.com")
        self.assertEqual(normalize_email("BOB@TEST.ORG\n"), "bob@test.org")

    def test_validate_age(self):
        self.assertTrue(validate_age(7))


if __name__ == "__main__":
    unittest.main()
