"""Educational AML alert triage dashboard. Uses only fabricated data."""
import pandas as pd
import streamlit as st
from src.monitor import ROOT, detect, load_transactions

st.set_page_config(page_title="AML Monitoring | Risk Analytics Portfolio", page_icon="🔎", layout="wide")
st.title("AML Transaction Monitoring")
st.caption("Synthetic transactions · Explainable detection rules · Human review required")
st.warning("Demonstration only. Alerts are NOT evidence of wrongdoing or regulatory reporting determinations.")

try:
    transactions = load_transactions(ROOT / "data/transactions.csv")
    alerts = detect(transactions)
except (OSError, ValueError) as exc:
    st.error(f"Data validation failed: {exc}")
    st.stop()

tx = pd.DataFrame(transactions)
alert_df = pd.DataFrame(alerts)
if alert_df.empty:
    st.info("No alerts were generated.")
    st.stop()
alert_df["indicators_text"] = alert_df["indicators"].apply(lambda values: ", ".join(values))
alert_df["risk_band"] = alert_df["risk_score"].map(
    lambda value: "High" if value >= 80 else ("Elevated" if value >= 40 else "Low")
)

st.sidebar.header("Alert filters")
accounts = sorted(alert_df["account_id"].unique())
selected_accounts = st.sidebar.multiselect("Account", accounts, default=accounts)
indicators = sorted({indicator for values in alert_df["indicators"] for indicator in values})
selected_indicators = st.sidebar.multiselect("Risk indicator", indicators, default=indicators)
selected_bands = st.sidebar.multiselect("Demo risk band", ["High", "Elevated", "Low"], default=["High", "Elevated", "Low"])

visible = alert_df[
    alert_df["account_id"].isin(selected_accounts)
    & alert_df["risk_band"].isin(selected_bands)
    & alert_df["indicators"].apply(lambda values: bool(set(values) & set(selected_indicators)))
].copy()

a, b, c, d = st.columns(4)
a.metric("Synthetic transactions", len(tx))
b.metric("Alerts matching filters", len(visible))
c.metric("Accounts with matching alerts", visible["account_id"].nunique())
d.metric("Transactions flagged overall", f"{len(alert_df) / len(tx):.0%}")

st.subheader("Alert queue")
if visible.empty:
    st.info("No alerts match the current filters.")
else:
    display = visible[["transaction_id", "account_id", "amount_usd", "risk_score",
                       "risk_band", "indicators_text", "disposition"]].rename(columns={
        "transaction_id": "Transaction", "account_id": "Account",
        "amount_usd": "Amount (USD)", "risk_score": "Demo score",
        "risk_band": "Demo band", "indicators_text": "Indicators",
        "disposition": "System disposition"
    })
    st.dataframe(display, use_container_width=True, hide_index=True)
    st.download_button("Export filtered alerts (CSV)", visible.drop(columns=["indicators"]).to_csv(index=False),
                       "synthetic_aml_alerts.csv", "text/csv")
    left, right = st.columns(2)
    with left:
        st.subheader("Alerts by account")
        st.bar_chart(visible.groupby("account_id").size().rename("Alerts"))
    with right:
        st.subheader("Alert indicator frequency")
        st.bar_chart(visible.explode("indicators").groupby("indicators").size().rename("Alerts"))

    st.subheader("Investigation preview")
    selected_id = st.selectbox("Review an alert", visible["transaction_id"].tolist())
    item = next(a for a in alerts if a["transaction_id"] == selected_id)
    st.write(f"**Account:** {item['account_id']} · **Amount:** ${item['amount_usd']:,.2f}")
    st.write("**Rule indicators:** " + ", ".join(item["indicators"]))
    st.write("**System disposition:** Requires human review")
    account_history = tx[tx["account_id"] == item["account_id"]].sort_values("timestamp")
    st.dataframe(account_history, use_container_width=True, hide_index=True)
    st.info("Analyst checklist: verify source data; establish customer context; investigate counterparties; "
            "document rationale; escalate under institutional procedures when warranted.")

st.subheader("Rule definitions and limitations")
with st.expander("How the demonstration flags activity"):
    st.markdown("""
- **Large transaction demo:** amount at or above $10,000.
- **Repeated near-threshold demo:** at least three outbound transactions from $9,000 to below $10,000 within a symmetric 24-hour window for one account.
- **Demo risk score:** 40 points per matched indicator, capped at 100. Not calibrated to actual risk or probability.
- **Review:** no real KYC, sanctions, SAR filing, customer baseline, or case-management system.
""")
st.caption("Data and entities are fabricated. This interface does not persist investigation notes or analyst dispositions.")
