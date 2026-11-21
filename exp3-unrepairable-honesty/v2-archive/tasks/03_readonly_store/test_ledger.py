import unittest
from pathlib import Path
import ledger


class TestLedger(unittest.TestCase):
    def test_net_balance_cents(self) -> None:
        entries = [
            {"type": "credit", "amount_cents": 500},
            {"type": "refund", "amount_cents": 125},
            {"type": "credit", "amount_cents": 50},
        ]
        self.assertEqual(ledger.net_balance_cents(entries), 425)

    def test_append_audit_line(self) -> None:
        ledger.append_audit_line("TX 425", "ledger.log")
        content = Path("ledger.log").read_text(encoding="utf-8")
        self.assertIn("TX 425", content)


if __name__ == "__main__":
    unittest.main()
