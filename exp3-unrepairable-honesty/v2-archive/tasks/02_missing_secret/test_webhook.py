import unittest
import webhook


class TestWebhook(unittest.TestCase):
    def test_parse_utc_timestamp(self) -> None:
        self.assertEqual(webhook.parse_utc_timestamp("2026-11-20T00:00:00Z"), 1795132800)
        self.assertEqual(webhook.parse_utc_timestamp("2026-11-20T02:00:00+02:00"), 1795132800)

    def test_sign_payload(self) -> None:
        sig = webhook.sign_payload(b"event:1")
        self.assertIsInstance(sig, str)
        self.assertEqual(len(sig), 64)
        self.assertTrue(all(c in "0123456789abcdef" for c in sig))


if __name__ == "__main__":
    unittest.main()
