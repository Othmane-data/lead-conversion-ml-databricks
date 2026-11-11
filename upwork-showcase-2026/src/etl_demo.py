"""Reproducible, synthetic transaction cleaning and SQLite export."""
from pathlib import Path
import sqlite3
import numpy as np
import pandas as pd

rng = np.random.default_rng(20261111)
rows = []
for i in range(1,701):
    amount = round(float(rng.uniform(25, 2600)), 2)
    if i % 67 == 0: amount = np.nan
    elif i % 43 == 0: amount = -amount
    rows.append({"transaction_id":f"TX-{i:05d}",
                 "customer_id":f"  cust-{rng.integers(1, 170):04d}  ",
                 "amount":amount,
                 "status":rng.choice(["PAID","paid "," Paid","PENDING","pending"]),
                 "source":rng.choice(["POS","CRM","WEB"])})
rows.extend([dict(rows[i]) for i in range(24)])
raw = pd.DataFrame(rows)
out = Path("demo_outputs"); out.mkdir(exist_ok=True)
raw.to_csv(out / "raw_transactions.csv",index=False)
clean = raw.copy()
clean["customer_id"] = clean["customer_id"].str.strip().str.upper()
clean["status"] = clean["status"].str.strip().str.upper()
clean = clean.drop_duplicates("transaction_id").dropna(subset=["amount"])
clean = clean.loc[clean["amount"] >= 0].copy()
clean.to_csv(out / "clean_transactions.csv",index=False)
with sqlite3.connect(out / "clean_transactions.sqlite") as conn:
    clean.to_sql("fact_transactions",conn,if_exists="replace",index=False)
    count = conn.execute("SELECT COUNT(*) FROM fact_transactions").fetchone()[0]
print(f"Raw: {len(raw)} | Clean: {count} | Rejected: {len(raw)-count}")
print("Rules: unique ID, normalized text, amount present and nonnegative.")
