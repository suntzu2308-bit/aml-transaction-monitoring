import csv
import sqlite3
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from monitor import ROOT, detect, load_transactions

class SQLParityTests(unittest.TestCase):
    def test_detection_rules_match(self):
        with (ROOT / "data/transactions.csv").open(newline="", encoding="utf-8") as handle:
            raw = list(csv.DictReader(handle))
        db = sqlite3.connect(":memory:")
        try:
            db.execute("CREATE TABLE transactions (transaction_id TEXT, account_id TEXT, timestamp TEXT, amount_usd REAL, direction TEXT, country TEXT, counterparty_id TEXT)")
            db.executemany("INSERT INTO transactions VALUES (:transaction_id,:account_id,:timestamp,:amount_usd,:direction,:country,:counterparty_id)", raw)
            script = (ROOT / "sql/detection_rules.sql").read_text(encoding="utf-8")
            found = set()
            for statement in script.split(";"):
                if statement.strip():
                    for tx_id, account, amount, indicator in db.execute(statement):
                        found.add((tx_id, indicator))
            expected = {(alert["transaction_id"], indicator)
                        for alert in detect(load_transactions(ROOT / "data/transactions.csv"))
                        for indicator in alert["indicators"]}
            self.assertEqual(found, expected)
        finally:
            db.close()
