-- SQLite checks on the fact_transactions table exported by src/etl_demo.py
SELECT COUNT(*) AS clean_rows FROM fact_transactions;
SELECT COUNT(DISTINCT transaction_id) AS unique_transactions FROM fact_transactions;
SELECT COUNT(*) AS invalid_amounts FROM fact_transactions
WHERE amount IS NULL OR amount < 0;
SELECT status, COUNT(*) AS n, ROUND(SUM(amount), 2) AS total_amount
FROM fact_transactions GROUP BY status ORDER BY n DESC;
