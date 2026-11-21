import unittest
import validator


class TestValidator(unittest.TestCase):
    def test_normalize_email(self) -> None:
        self.assertEqual(validator.normalize_email("  Alice@Example.COM \n"), "alice@example.com")

    def test_validate_age(self) -> None:
        self.assertTrue(validator.validate_age(7, "schema.json"))


if __name__ == "__main__":
    unittest.main()
