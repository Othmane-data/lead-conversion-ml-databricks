# 03 — AI Lead Scoring: Python & Machine Learning

![AI portfolio visual](../assets/ai.svg)

**Problem:** Rank prospects by estimated conversion probability so sales teams can prioritize their attention.

**Approach:**
1. Prepare a fictional lead dataset (source, engagement, page views, inactivity, contacts and target).
2. Separate training and holdout test data using stratification.
3. Apply one-hot encoding to categorical attributes and scaling to numerical attributes *inside* a scikit-learn Pipeline.
4. Fit Logistic Regression; evaluate ROC-AUC, precision, recall and score-tier distributions.
5. Explain potential business action and limitations before any real-world pilot.

**Code:** [Runnable Python demo](../src/ai_demo.py).

**Relevant existing body of work:** The account also documents a larger [lead-conversion model using 383 leads](https://github.com/Othmane-data/lead-conversion-ml-databricks/tree/main) and a separate [telco churn model](https://github.com/Othmane-data/telco-churn-pyspark-databricks).

**No invented outcomes:** This project uses synthetic data. A good holdout ROC-AUC does **not** prove a causal increase in sales, and deployment would require security, drift monitoring and operational validation.
