import sys
import unittest
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

if __name__ == "__main__":
    unittest.main()
