import unittest
from webhook import format_utc_iso, sign_payload


class TestWebhook(unittest.TestCase):
    def test_format_utc_iso(self):
        self.assertEqual(format_utc_iso(0), "1970-01-01T00:00:00Z")
        self.assertEqual(format_utc_iso(1767323045), "2026-01-02T03:04:05Z")

    def test_sign_payload(self):
        sig = sign_payload(b"event=invoice.paid&id=42")
        self.assertEqual(len(sig), 64)
        self.assertTrue(all(c in "0123456789abcdef" for c in sig))


if __name__ == "__main__":
    unittest.main()
