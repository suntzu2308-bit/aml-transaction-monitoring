# AML Transaction Monitoring — Synthetic Portfolio Demonstration

An educational, reproducible **Python + SQL** transaction-monitoring prototype. It validates a synthetic transaction dataset, applies two explainable detection rules, generates review alerts, and documents a human investigation workflow.

**This is not a deployed compliance system. Alerts are indicators requiring review, not findings of wrongdoing.**

## Quick start
Python 3.10+; no external packages required. From the repository root:

```bash
python src/monitor.py
python -m unittest discover -s tests -v
```

The script generates `output/alerts.json` with transaction IDs, account IDs, risk scores, indicators and human-review dispositions.

## Repository structure
- `data/transactions.csv`: fabricated accounts and transfers
- `src/monitor.py`: CSV validation, rule evaluation, explainable alerts and JSON export
- `sql/detection_rules.sql`: equivalent detection concepts for SQLite
- `tests/test_monitor.py`: regression tests for positive and negative examples
- `docs/investigation_workflow.md`: triage, investigation, escalation and limitations

## Illustrative rules and findings
1. **Large transaction:** any transfer of $10,000 or more (illustrative threshold).
2. **Repeated near-threshold outbound transfers:** three or more transfers of $9,000–$9,999.99 within a symmetric 24-hour window for the same account.

The fabricated sample is designed to produce **four alerts**: T002, T003, T004 and T007. This is an expected synthetic test fixture, not a real-world detection result. Scores are explanatory demo values, **not validated probability estimates**.

## Data quality and reproducibility
Required columns, missing values, duplicate transaction IDs, direction, timestamp and positive finite amounts are checked. The code uses Python's standard library. SQL is supplied as a separate query example; production SQL/Python parity and database integration remain future work.

## Limitations and next steps
This prototype lacks customer baselines, KYC/CDD context, beneficial ownership, sanctions screening, transaction networks, investigation case management, analyst feedback and jurisdiction-specific regulatory logic. Thresholds are **not** compliance advice. Potential enhancements include risk segmentation, precision/recall testing on labeled synthetic cases, SQL integration, CI, and analyst dashboards.

## Privacy and license
All data is fabricated. No private customer information, API keys, confidential algorithms or actual SARs are included. MIT licensed.
