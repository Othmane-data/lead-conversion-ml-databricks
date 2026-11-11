"""Synthetic lead-scoring proof of concept; no customer data."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, precision_score, recall_score

rng = np.random.default_rng(20261111)
n = 2200
source = rng.choice(["Organic", "Referral", "Paid", "Social", "Direct"], n)
engagement = rng.integers(0, 11, n)
views = rng.poisson(5, n) + 1
inactive_days = rng.integers(0, 31, n)
touches = rng.integers(0, 5, n)
boost = pd.Series(source).map({"Organic": .25,"Referral": .85,"Paid": .08,"Social": -.25,"Direct": .35}).to_numpy()
signal = -2.4 + .24*engagement + .08*views - .045*inactive_days + .16*touches + boost + rng.normal(0,.3,n)
probability = 1 / (1 + np.exp(-signal))
target = rng.binomial(1, probability)
df = pd.DataFrame({"source": source, "engagement_score": engagement,
                   "page_views": views, "days_inactive": inactive_days,
                   "contact_count": touches, "converted": target})
X, y = df.drop(columns="converted"), df["converted"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=.25, stratify=y, random_state=42)
transformer = ColumnTransformer([
    ("category", OneHotEncoder(handle_unknown="ignore"), ["source"]),
    ("numbers", StandardScaler(), ["engagement_score", "page_views", "days_inactive", "contact_count"])
])
pipeline = Pipeline([("features", transformer), ("model", LogisticRegression(max_iter=1000))])
pipeline.fit(X_train, y_train)
scores = pipeline.predict_proba(X_test)[:, 1]
print("Synthetic test leads:", len(y_test))
print("ROC-AUC:", round(roc_auc_score(y_test, scores), 3))
print("Precision:", round(precision_score(y_test, scores >= .5), 3))
print("Recall:", round(recall_score(y_test, scores >= .5), 3))
print("Note: predictive rankings do not prove a causal uplift in sales.")
out = Path("demo_outputs"); out.mkdir(exist_ok=True)
df.to_csv(out / "synthetic_leads.csv", index=False)
