import unittest
from auth_tokens import is_token_expired, sign_session_token


class TestAuthTokens(unittest.TestCase):
    def test_is_token_expired(self):
        self.assertFalse(is_token_expired(1000, 995, leeway_seconds=30))
        self.assertFalse(is_token_expired(1000, 1020, leeway_seconds=30))
        self.assertFalse(is_token_expired(1000, 1030, leeway_seconds=30))
        self.assertTrue(is_token_expired(1000, 1031, leeway_seconds=30))

    def test_sign_session_token(self):
        sig = sign_session_token("usr_109", 1767323045)
        self.assertEqual(len(sig), 64)
        self.assertTrue(all(c in "0123456789abcdef" for c in sig))


if __name__ == "__main__":
    unittest.main()
