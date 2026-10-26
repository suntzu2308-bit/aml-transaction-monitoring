import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from monitor import ROOT, detect, load_transactions

class MonitoringTests(unittest.TestCase):
    def test_sample_alerts(self):
        alerts = detect(load_transactions(ROOT / "data/transactions.csv"))
        self.assertEqual({a["transaction_id"] for a in alerts},
                         {"T002", "T003", "T004", "T007"})
        self.assertTrue(all(a["disposition"] == "REQUIRES_HUMAN_REVIEW" for a in alerts))

    def test_no_alerts_on_small_transfers(self):
        rows = load_transactions(ROOT / "data/transactions.csv")
        self.assertEqual(detect([r for r in rows if r["account_id"] == "A400"]), [])

    def test_large_transaction_boundary(self):
        rows = [{
            "transaction_id": "X", "account_id": "A", "timestamp": datetime(2026, 1, 1),
            "amount_usd": 10000.0, "direction": "inbound", "country": "US",
            "counterparty_id": "C"
        }]
        self.assertEqual(detect(rows)[0]["indicators"], ["LARGE_TRANSACTION_DEMO"])
        rows[0]["amount_usd"] = 9999.99
        self.assertEqual(detect(rows), [])

    def test_near_threshold_requires_three(self):
        rows = [{
            "transaction_id": str(i), "account_id": "A",
            "timestamp": datetime(2026, 1, 1, 12, i),
            "amount_usd": 9500.0, "direction": "outbound",
            "country": "US", "counterparty_id": "C"
        } for i in range(3)]
        self.assertEqual(len(detect(rows[:2])), 0)
        self.assertEqual(len(detect(rows)), 3)

    def test_duplicate_transaction_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tx.csv"
            header = "transaction_id,account_id,timestamp,amount_usd,direction,country,counterparty_id\n"
            row = "X,A,2026-01-01T12:00:00,100,outbound,US,C\n"
            path.write_text(header + row + row, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Duplicate transaction ID"):
                load_transactions(path)

    def test_zero_amount_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tx.csv"
            path.write_text(
                "transaction_id,account_id,timestamp,amount_usd,direction,country,counterparty_id\n"
                "X,A,2026-01-01T12:00:00,0,outbound,US,C\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Invalid amount"):
                load_transactions(path)

if __name__ == "__main__":
    unittest.main()
