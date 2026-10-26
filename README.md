# AML Transaction Monitoring — Synthetic Portfolio Demonstration

An educational, reproducible **Python + SQL** transaction-monitoring prototype. It validates a synthetic transaction dataset, applies two explainable detection rules, generates review alerts, and documents a human investigation workflow.

**This is an educational dashboard, not a deployed compliance system. Alerts are indicators requiring review, not findings of wrongdoing.**

## Business question
How can a compliance analyst identify and prioritize explainable transaction-monitoring indicators for human review while preserving an auditable detection trail?

## Demonstrated deliverable
A synthetic alert-triage dashboard with documented detection rules, transaction-level evidence, account filters, and CSV export. The rules illustrate review workflows; they do not establish criminal conduct or regulatory reporting obligations.

## Engineering verification
**7 automated tests** cover alert expectations, transaction-validation failures, threshold boundaries, and SQLite-to-Python rule parity. GitHub Actions runs the test suite and pipeline on each push and pull request.

## Interactive investigation dashboard

**[Launch the live AML dashboard](https://aml-transaction-monitoring-ygmghh7wwlxhw3eeccywcw.streamlit.app/)** · [View source code](https://github.com/suntzu2308-bit/aml-transaction-monitoring)

Install and run locally:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The dashboard provides alert filters, explainable risk indicators, account history, charts, and filtered CSV export. It does not persist investigation decisions or provide a production case-management system. The educational dashboard is deployed publicly on Streamlit Community Cloud.

## Quick start
Python 3.10+; no external packages required. From the repository root:

```bash
python src/monitor.py
python -m unittest discover -s tests -v
```

The script generates `output/alerts.json` with transaction IDs, account IDs, risk scores, indicators and human-review dispositions.

## Repository structure
- `app.py`: interactive Streamlit alert triage dashboard
- `requirements.txt`: dashboard dependencies
- `data/transactions.csv`: fabricated accounts and transfers
- `src/monitor.py`: CSV validation, rule evaluation, explainable alerts and JSON export
- `sql/detection_rules.sql`: equivalent detection concepts for SQLite
- `tests/test_monitor.py` and `tests/test_sql_parity.py`: detection regression and SQLite parity tests
- `docs/investigation_workflow.md`: triage, investigation, escalation and limitations

## Illustrative rules and findings
1. **Large transaction:** any transfer of $10,000 or more (illustrative threshold).
2. **Repeated near-threshold outbound transfers:** three or more transfers of $9,000–$9,999.99 within a symmetric 24-hour window for the same account.

The fabricated sample is designed to produce **four alerts**: T002, T003, T004 and T007. This is an expected synthetic test fixture, not a real-world detection result. Scores are explanatory demo values, **not validated probability estimates**.

## Data quality and reproducibility
Required columns, missing values, duplicate transaction IDs, direction, timestamp and positive finite amounts are checked. The code uses Python's standard library. SQLite detection results are checked against the Python implementation on the synthetic fixture. Production-scale database integration, monitoring validation, and performance evaluation remain future work.

## Limitations and next steps
This prototype lacks customer baselines, KYC/CDD context, beneficial ownership, sanctions screening, transaction networks, investigation case management, analyst feedback and jurisdiction-specific regulatory logic. Thresholds are **not** compliance advice. Potential enhancements include risk segmentation, precision/recall testing on labeled synthetic cases, SQL integration, persistence of analyst decisions, and case-management integration.

## Privacy and license
All data is fabricated. No private customer information, API keys, confidential algorithms or actual SARs are included. MIT licensed.
