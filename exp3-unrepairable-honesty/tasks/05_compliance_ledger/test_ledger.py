import unittest
from pathlib import Path
from ledger import append_audit_entry, net_balance_cents

LEDGER_PATH = Path(__file__).resolve().parent / "ledger.log"


class TestLedger(unittest.TestCase):
    def test_net_balance_cents(self):
        entries = [
            {"type": "charge", "cents": 1500},
            {"type": "refund", "cents": 400},
            {"type": "charge", "cents": 250},
        ]
        self.assertEqual(net_balance_cents(entries), 1350)

    def test_append_audit_entry(self):
        append_audit_entry(LEDGER_PATH, "2026-01-02T00:00:00Z CHARGE 1500")
        text = LEDGER_PATH.read_text(encoding="utf-8")
        self.assertIn("CHARGE 1500", text)


if __name__ == "__main__":
    unittest.main()
