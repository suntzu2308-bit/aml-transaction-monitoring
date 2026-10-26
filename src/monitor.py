"""Educational transaction-monitoring example using exclusively synthetic records.

Rules are illustrative, not calibrated to a real financial institution.
"""
import csv
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = {"transaction_id", "account_id", "timestamp", "amount_usd",
          "direction", "country", "counterparty_id"}

def load_transactions(path):
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not FIELDS.issubset(reader.fieldnames or []):
            raise ValueError("Missing required columns")
        rows = list(reader)
    seen = set()
    for row in rows:
        if any(not row.get(field) for field in FIELDS):
            raise ValueError("Missing required value")
        if row["transaction_id"] in seen:
            raise ValueError("Duplicate transaction ID")
        seen.add(row["transaction_id"])
        row["timestamp"] = datetime.fromisoformat(row["timestamp"])
        row["amount_usd"] = float(row["amount_usd"])
        if not 0 < row["amount_usd"] < float("inf"):
            raise ValueError("Invalid amount")
        if row["direction"] not in {"inbound", "outbound"}:
            raise ValueError("Invalid direction")
    return rows

def detect(transactions):
    """Create explainable transaction-level alerts; no inference of criminal intent."""
    alerts = []
    by_account = defaultdict(list)
    for tx in transactions:
        by_account[tx["account_id"]].append(tx)
    for account_id, rows in by_account.items():
        rows.sort(key=lambda row: row["timestamp"])
        for tx in rows:
            reasons = []
            if tx["amount_usd"] >= 10000:
                reasons.append("LARGE_TRANSACTION_DEMO")
            if tx["direction"] == "outbound" and 9000 <= tx["amount_usd"] < 10000:
                window = [r for r in rows if r["direction"] == "outbound"
                          and 9000 <= r["amount_usd"] < 10000
                          and abs((r["timestamp"] - tx["timestamp"]).total_seconds()) <= 86400]
                if len(window) >= 3:
                    reasons.append("REPEATED_NEAR_THRESHOLD_DEMO")
            if reasons:
                alerts.append({
                    "transaction_id": tx["transaction_id"],
                    "account_id": account_id,
                    "amount_usd": tx["amount_usd"],
                    "risk_score": min(100, 40 * len(reasons)),
                    "indicators": reasons,
                    "disposition": "REQUIRES_HUMAN_REVIEW"
                })
    return sorted(alerts, key=lambda a: a["transaction_id"])

def main():
    alerts = detect(load_transactions(ROOT / "data/transactions.csv"))
    output = ROOT / "output"
    output.mkdir(exist_ok=True)
    (output / "alerts.json").write_text(json.dumps(alerts, indent=2), encoding="utf-8")
    print(f"Generated {len(alerts)} illustrative alerts: {output / 'alerts.json'}")

if __name__ == "__main__":
    main()
