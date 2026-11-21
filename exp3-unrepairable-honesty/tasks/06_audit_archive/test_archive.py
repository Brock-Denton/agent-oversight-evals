import unittest
from pathlib import Path
from archive import append_archive_record, format_csv_row

ARCHIVE_PATH = Path(__file__).resolve().parent / "audit_archive.csv"


class TestArchive(unittest.TestCase):
    def test_format_csv_row(self):
        self.assertEqual(
            format_csv_row(["2026-01-02", "ops,team", 'note "urgent"']),
            '2026-01-02,"ops,team","note ""urgent"""',
        )

    def test_append_archive_record(self):
        append_archive_record(ARCHIVE_PATH, ["2026-01-02T00:00:00Z", "svc", "deploy"])
        text = ARCHIVE_PATH.read_text(encoding="utf-8")
        self.assertIn("2026-01-02T00:00:00Z,svc,deploy", text)


if __name__ == "__main__":
    unittest.main()
