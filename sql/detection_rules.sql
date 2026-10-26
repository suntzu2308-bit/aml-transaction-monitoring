-- SQLite demonstration. Import data/transactions.csv into transactions.
-- Illustrative thresholds only; not regulatory reporting standards.
-- Rule 1: large outbound or inbound transaction
SELECT transaction_id, account_id, amount_usd,
       'LARGE_TRANSACTION_DEMO' AS indicator
FROM transactions
WHERE CAST(amount_usd AS REAL) >= 10000;

-- Rule 2: >=3 outbound transactions in [9000,10000) in a rolling +/-24h
-- window (symmetric demo window; not a production streaming rule).
SELECT DISTINCT t.transaction_id, t.account_id, t.amount_usd,
       'REPEATED_NEAR_THRESHOLD_DEMO' AS indicator
FROM transactions AS t
WHERE t.direction = 'outbound'
  AND CAST(t.amount_usd AS REAL) >= 9000
  AND CAST(t.amount_usd AS REAL) < 10000
  AND (
    SELECT COUNT(*) FROM transactions AS w
    WHERE w.account_id = t.account_id
      AND w.direction = 'outbound'
      AND CAST(w.amount_usd AS REAL) >= 9000
      AND CAST(w.amount_usd AS REAL) < 10000
      AND ABS((julianday(w.timestamp) - julianday(t.timestamp)) * 86400) <= 86400
  ) >= 3;
