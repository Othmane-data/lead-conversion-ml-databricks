# Lead Conversion Prediction — Machine Learning on Databricks

> **Business-oriented lead-scoring proof of concept** for a professional-training context: turn heterogeneous prospect data into a reproducible conversion probability that can help sales teams prioritize follow-up — while preserving human decision-making and protecting personal and business-sensitive information.

[Version française](README_FR.md) · [Public notebook](notebooks/lead_conversion_ml_databricks_public.ipynb) · [Model card](docs/model_card.md) · [Public data dictionary](docs/data_dictionary.md) · [Privacy & GDPR](docs/privacy_rgpd.md) · [Reproducibility](docs/reproducibility.md)

---

## Executive snapshot

| Item | Result |
|---|---:|
| Final modelling dataset | **383 leads** |
| Converted leads | **122 (31.85%)** |
| Non-converted leads | **261 (68.15%)** |
| Train / validation / test | **230 / 77 / 76** |
| Candidate models | Logistic Regression, Decision Tree, Random Forest |
| Selected model | **Logistic Regression** |
| Test ROC-AUC | **0.704** |
| Test PR-AUC | **0.501** |
| Test recall | **0.652** |
| Test precision | **0.484** |
| Test F1-score | **0.556** |
| Test accuracy | **0.684** |
| Prioritized-group conversion rate @ 0.50 | **48.4%** |
| Test-set baseline conversion rate | **30.3%** |
| Relative concentration of conversions | **≈ 1.6×** |

**What the project demonstrates:** a reproducible methodology can produce a useful **ranking signal** from historical lead data.  
**What it does not demonstrate yet:** that using the score **causes** a higher conversion rate. That requires a prospective operational pilot.

---

# 1. Business problem

A sales team cannot always treat every incoming lead immediately or with the same intensity. Leads differ in maturity, financing situation, requested training, engagement and response to commercial contact, while sales capacity remains limited.

The operational question is therefore:

> **To what extent can a Machine Learning model improve lead qualification and prioritization in professional training?**

The objective is not to automate the commercial decision. The model should provide a **probability of conversion** that can support a more consistent order of treatment.

A useful system must answer four questions:

1. Can historical lead information separate higher- from lower-conversion prospects?
2. Which model offers the best trade-off between ranking performance, recall and interpretability?
3. Can the predicted probability be translated into an operational prioritization rule?
4. Can this be done without publishing personal data or commercially sensitive internal information?

---

# 2. Why this is a business project, not only a classification exercise

The core challenge is not simply to call `fit()` on an algorithm.

The project starts with a fragmented prospect dataset and follows the complete decision chain:

```text
Business need
    ↓
Data consolidation
    ↓
Data-quality rules
    ↓
Privacy / leakage controls
    ↓
Feature preparation
    ↓
Temporal train / validation / test split
    ↓
Common preprocessing pipeline
    ↓
3 candidate classifiers
    ↓
Validation comparison
    ↓
Champion selection
    ↓
One-time test evaluation
    ↓
Probability → prioritization
    ↓
Operational pilot and monitoring
```

The final output is therefore both:
- a **predictive prototype**;
- a **decision-support framework** that can be discussed with marketing and sales users.

---

# 3. Public portfolio and confidentiality boundary

The original project used internal prospect data. This public repository deliberately does **not** publish the original dataset or any row-level export.

The public release excludes:

- names and first names;
- email addresses;
- telephone numbers;
- exact row-level prospect records;
- individual lead scores and rankings;
- detailed conversion performance by acquisition channel;
- detailed conversion performance by campaign;
- detailed conversion performance by training offer;
- modality-level model coefficients / feature weights that could reveal internal commercial patterns;
- the private Databricks table name and private workspace structure.

This is stricter than replacing a name with a sequential ID. A pseudonymous identifier can still be personal data if a person remains re-identifiable. The public portfolio therefore shares **methodology and aggregate results**, not a row-level “anonymized” dataset.

See [`docs/privacy_rgpd.md`](docs/privacy_rgpd.md).

---

# 4. Data origin and construction

The practical work began from a small prospect table containing mainly identification information. The modelling base was then progressively consolidated with marketing, training, financing, behavioural and commercial-interaction variables.

The initial working base contained roughly **300 rows**. After consolidation, harmonisation and enrichment, the final modelling dataset contained **383 leads**.

One row represents one lead.

The modelling schema is organized into the following families:

| Family | Examples of variables | Role |
|---|---|---|
| Time | `annee_inscription`, `mois_inscription` | Capture registration context over time |
| Acquisition | `canal_acquisition`, `campagne_base` | Describe where the lead came from |
| Profile | `pays_residence`, `statut_professionnel` | General prospect context |
| Training | `categorie_formation`, `format_formation`, `niveau_formation`, `duree_heures` | Describe the requested training |
| Financing | `eligible_cpf`, `mode_financement`, `budget_estime_eur` | Financing context |
| Engagement | `formulaire_complete`, `demande_brochure`, `participation_webinaire` | Pre-conversion engagement signals |
| Sales interaction | `reponse_appel`, `rendez_vous`, `nb_relances`, `delai_premier_contact_jours` | Commercial-contact signals |
| Digital activity | `nb_clics_annonce`, `nb_visites_site` | Observed digital engagement |
| Target | `conversion` | 1 = converted, 0 = not converted |

Technical fields such as `id_lead`, registration date and temporal partition are retained for traceability but are not used as direct predictive inputs.

Detailed definitions and publication rules are documented in [`docs/data_dictionary.md`](docs/data_dictionary.md).

---

# 5. Data-quality work

Data preparation is a central part of the result.

The workflow includes:

- duplicate detection through the technical lead identifier;
- normalization of categorical strings;
- conversion and validation of numeric fields;
- date parsing;
- restriction of the target to valid binary values;
- standardized names for train / validation / test partitions;
- separation between identification fields and modelling features;
- exclusion of information that would only become available after the commercial outcome.

A notable issue appeared during execution: `budget_estime_eur` was stored as text and its numeric conversion produced **100% missing values**. Scikit-learn therefore skipped this feature during imputation.

The limitation is intentionally documented instead of being hidden.

![Missing values](assets/01_data_quality_missing_values.png)

### Why this matters

A portfolio project should not present a cleaner story than the actual experiment. The budget issue shows an important real-world lesson: **data-type quality can matter more than model complexity**.

---

# 6. Target distribution

The final dataset contains:

| Conversion | Leads | Share |
|---|---:|---:|
| Non-converted | **261** | **68.15%** |
| Converted | **122** | **31.85%** |
| Total | **383** | **100%** |

![Target distribution](assets/02_target_distribution.png)

The positive class is a minority class, although the imbalance is not extreme. For that reason, accuracy alone is not a sufficient decision criterion.

The evaluation also uses precision, recall, F1-score, ROC-AUC, PR-AUC and confusion matrices.

For a lead-prioritization use case, **false negatives** are particularly important: they are real conversions that the model fails to place in the positive / priority group at the selected threshold.

---

# 7. Confidential exploratory analysis

Internal exploratory analysis was performed across commercial dimensions such as acquisition channel, financing mode, training category and campaign.

Those detailed results are **not reproduced here** because they can reveal internal commercial effectiveness.

The public version focuses on the analytical method and safe aggregate evidence required to evaluate the ML prototype.

This is an intentional portfolio design choice, not a missing analytical step.

---

# 8. Temporal experimental design

The dataset is split into three predefined temporal partitions:

| Partition | Leads | Conversions | Conversion rate | Share |
|---|---:|---:|---:|---:|
| Train | **230** | **77** | 33.48% | 60.1% |
| Validation | **77** | **22** | 28.57% | 20.1% |
| Test | **76** | **23** | 30.26% | 19.8% |
| Total | **383** | **122** | 31.85% | 100% |

![Partition distribution](assets/03_partition_distribution.png)

- **Train:** fit model parameters.
- **Validation:** compare candidate models and choose the champion.
- **Test:** evaluate the selected model once after the selection decision.

This prevents the final test set from becoming part of the model-selection process.

---

# 9. Preprocessing pipeline

All candidate models use the same preparation logic.

## Categorical variables

```text
SimpleImputer(strategy="most_frequent")
        ↓
OneHotEncoder(handle_unknown="ignore")
```

## Numeric variables

```text
SimpleImputer(strategy="median")
        ↓
StandardScaler()
```

The transformations are wrapped in a `ColumnTransformer`, then combined with the estimator inside a scikit-learn `Pipeline`.

This architecture provides two important safeguards:

1. preprocessing is fitted only on the relevant training data;
2. the same transformations are consistently applied to validation, test and future scoring data.

---

# 10. Candidate models

Three models are compared under the same experimental protocol.

### Logistic Regression

```python
LogisticRegression(
    solver="liblinear",
    max_iter=1000,
    class_weight="balanced",
    random_state=42
)
```

Why include it: naturally probabilistic, interpretable and easy to explain to business users.

### Decision Tree

```python
DecisionTreeClassifier(
    max_depth=4,
    min_samples_leaf=10,
    class_weight="balanced",
    random_state=42
)
```

Why include it: intuitive rules and a useful non-linear benchmark.

### Random Forest

```python
RandomForestClassifier(
    n_estimators=100,
    max_depth=6,
    min_samples_leaf=5,
    max_features="sqrt",
    class_weight="balanced",
    n_jobs=1,
    random_state=42
)
```

Why include it: handles non-linear relationships and reduces the variance of a single tree.

The hyperparameters are intentionally simple because the dataset is small. Extensive tuning on a small validation set would increase the risk of selecting a configuration that fits one specific partition.

---

# 11. Validation results

The three models are trained on **230 leads** and compared on the **77-lead validation set**.

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 0.532 | 0.306 | **0.500** | 0.379 | 0.537 | **0.389** |
| Random Forest | **0.623** | **0.348** | 0.364 | 0.356 | **0.604** | 0.382 |
| Decision Tree | 0.468 | 0.289 | **0.591** | **0.388** | 0.467 | 0.277 |

![Validation model comparison](assets/04_validation_model_comparison.png)

There is no universal winner.

- Random Forest has the strongest validation accuracy and ROC-AUC.
- Decision Tree has the highest recall and slightly highest F1.
- Logistic Regression has the best PR-AUC and higher recall than Random Forest.

This is exactly why the champion should not be chosen from one metric alone.

---

# 12. ROC and Precision–Recall analysis

## ROC curves

![Validation ROC curves](assets/05_validation_roc_curves.png)

Random Forest shows the best global discrimination on validation with ROC-AUC **0.604**. Logistic Regression reaches **0.537**, while the Decision Tree is at **0.467**.

## Precision–Recall curves

![Validation Precision–Recall curves](assets/06_validation_precision_recall_curves.png)

For this use case, PR-AUC is especially useful because it focuses attention on the positive class: converted leads.

- Logistic Regression: **0.389**
- Random Forest: **0.382**
- Decision Tree: **0.277**

The margin over Random Forest is small, so interpretability and recall remain part of the decision.

---

# 13. Validation confusion matrices

At threshold **0.50**, the errors become operationally visible.

## Logistic Regression

![Logistic validation confusion matrix](assets/07_validation_confusion_logistic_regression.png)

- TN = 30
- FP = 25
- FN = 11
- TP = 11

It detects **11 of 22 converted leads**.

## Decision Tree

![Decision-tree validation confusion matrix](assets/08_validation_confusion_decision_tree.png)

- TN = 23
- FP = 32
- FN = 9
- TP = 13

It detects the most converted leads but at the price of a large number of false positives.

## Random Forest

![Random-Forest validation confusion matrix](assets/09_validation_confusion_random_forest.png)

- TN = 40
- FP = 15
- FN = 14
- TP = 8

It reduces unnecessary positive classifications, but misses more real conversions.

---

# 14. Why Logistic Regression is selected

The selected model is **Logistic Regression**.

The decision is not based on accuracy. It is based on the overall business / modelling trade-off:

- highest validation **PR-AUC = 0.389**;
- validation **recall = 0.500**, higher than Random Forest;
- directly usable probability output suitable for ranking;
- simpler model to document and explain;
- validation performance close enough to the more complex alternative that transparency becomes valuable.

This choice is specific to this prototype. It does not imply that Logistic Regression is always preferable to Random Forest.

---

# 15. Final model retraining

After the validation decision, the selected Logistic Regression is retrained on:

```text
Train + Validation = 230 + 77 = 307 leads
```

The final model is then evaluated once on the untouched **76-lead test set**.

---

# 16. Final test performance

| Metric | Test result |
|---|---:|
| Accuracy | **0.684** |
| Precision | **0.484** |
| Recall | **0.652** |
| F1-score | **0.556** |
| ROC-AUC | **0.704** |
| PR-AUC | **0.501** |

The test scores are higher than the validation results, but this should **not** be interpreted as proof that the model improved after selection. With only 76 test observations, a few predictions can materially change the metrics.

---

# 17. Final test confusion matrix

![Final Logistic Regression confusion matrix](assets/10_test_confusion_logistic_regression.png)

At threshold 0.50:

| | Predicted non-converted | Predicted converted |
|---|---:|---:|
| Actual non-converted | **37** | **16** |
| Actual converted | **8** | **15** |

The model identifies **15 of the 23 actual conversions**.

The **8 false negatives** are commercially important: these are actual conversions that would not be included in the model-positive group at the reference threshold.

The threshold must therefore be treated as an operational parameter rather than a fixed statistical truth.

---

# 18. From model metric to business signal

The central business result can be expressed without publishing any individual score.

On the test cohort:

- **23 / 76 = 30.3%** of leads converted overall;
- the model classifies **31 leads** as positive at threshold 0.50;
- **15 of those 31** actually convert;
- the positive/prioritized group therefore converts at **48.4%**;
- **48.4% / 30.3% ≈ 1.6×**.

| Business indicator | Value |
|---|---:|
| Test cohort conversion rate | **30.3%** |
| Leads in model-positive group | **31** |
| Conversions in model-positive group | **15** |
| Positive-group conversion rate | **48.4%** |
| Relative concentration / lift | **≈ 1.6×** |
| Recall | **65.2%** |

### Interpretation

The model concentrates more historical conversions in the prioritized group than an undifferentiated treatment of the whole test cohort.

That is evidence that the score contains **ranking information**.

It is **not** evidence that a salesperson using the score will necessarily create 1.6× more conversions. The score has only been evaluated on historical outcomes.

---

# 19. Threshold as a business parameter

The 0.50 threshold is an experimental reference.

### Lower threshold
- more leads prioritized;
- higher recall;
- fewer missed conversions;
- more false positives;
- greater commercial workload.

### Higher threshold
- fewer leads prioritized;
- potentially higher precision;
- lower commercial workload;
- more risk of missing genuine conversions.

The appropriate threshold therefore depends on the number of leads the team can process, the cost of a missed conversion, the cost of unnecessary follow-up and the expected lead value.

The score is better interpreted as a **ranking mechanism** than as a hard automated yes/no decision.

---

# 20. Human-in-the-loop operating principle

The intended use is:

```text
Lead information
      ↓
Model probability
      ↓
Priority / order of treatment
      ↓
Human commercial review
      ↓
Contact / follow-up decision
```

The prototype is **not designed to automatically reject or exclude a prospect**.

This matters both operationally and from a data-protection perspective. Profiling and automated decision-making can raise specific GDPR concerns when a system makes decisions without meaningful human involvement, especially where those decisions have legal or similarly significant effects.

---

# 21. Privacy by design and GDPR-oriented publication

The public repository follows a conservative privacy-by-design approach.

## Data minimization
Only information necessary to explain the project is published. No original row-level data is shared.

## Direct identifiers
Names, first names, emails and telephone numbers are excluded from the modelling perimeter and from the repository.

## Pseudonymous identifiers
A technical `id_lead` was used internally for traceability. It is **not treated as anonymous data** and individual ID-level outputs are not published.

## Quasi-identifiers and profiling variables
Variables such as geography, professional status and behavioural interactions can still relate to identifiable people in an internal dataset. Their row-level values are not included in this repository.

## Business confidentiality
Detailed conversion rates by campaign/channel, individual scores and modality-level model weights are withheld because privacy protection and business confidentiality are separate requirements.

## Human oversight
The score is documented as decision support rather than an automatic exclusion rule.

See [`docs/privacy_rgpd.md`](docs/privacy_rgpd.md) for the full public-release policy and official references.

---

# 22. Limitations

This project should be read as a **proof of concept**.

1. **Small sample:** only 383 leads are available.
2. **Small validation/test sets:** 77 and 76 observations make metrics sensitive to a few classification changes.
3. **Budget variable failure:** `budget_estime_eur` could not be exploited in the analysed execution.
4. **Reference threshold not cost-optimized:** 0.50 was not selected from a measured sales-capacity or cost function.
5. **Limited hyperparameter optimization:** aggressive tuning would be difficult to justify on this sample.
6. **Predictive, not causal:** feature associations do not prove that changing a variable will cause conversion.
7. **No prospective business validation:** historical ranking performance does not demonstrate incremental sales impact.
8. **Potential drift:** campaigns, customer behaviour and training demand can evolve.
9. **Fairness and subgroup monitoring:** subgroup performance and possible unfair effects should be reviewed before operational deployment.

---

# 23. Recommended operational pilot

A future validation should compare:

```text
Reference process
vs.
Score-assisted prioritization process
```

The test protocol should be defined **before** looking at outcomes.

Recommended indicators:

### Commercial
- conversion rate;
- time to first contact;
- number of follow-ups;
- percentage of leads actually processed;
- conversions per unit of commercial effort, if available.

### Predictive
- precision;
- recall;
- PR-AUC;
- calibration;
- distribution of scores;
- false-negative rate.

### Data quality
- missing-value rate;
- duplicate rate;
- category drift;
- input-format failures.

A production decision should then be based on both **business gain** and **model stability**.

---

# 24. Technology stack

| Layer | Technology |
|---|---|
| Workspace / traceability | Databricks |
| Data access | Databricks table → Pandas |
| Data manipulation | Python, Pandas, NumPy |
| Preprocessing | scikit-learn `Pipeline`, `ColumnTransformer` |
| Categorical encoding | `OneHotEncoder` |
| Numeric preparation | `SimpleImputer`, `StandardScaler` |
| Models | Logistic Regression, Decision Tree, Random Forest |
| Evaluation | scikit-learn metrics |
| Visualization | Matplotlib / scikit-learn displays |

**Important:** this is not presented as a distributed Big Data architecture. With 383 rows, PySpark-based modelling would add complexity without analytical value.

---

# 25. Repository structure

```text
lead-conversion-ml-databricks/
│
├── README.md
├── README_FR.md
├── requirements.txt
├── .gitignore
│
├── assets/
│   ├── 01_data_quality_missing_values.png
│   ├── 02_target_distribution.png
│   ├── 03_partition_distribution.png
│   ├── 04_validation_model_comparison.png
│   ├── 05_validation_roc_curves.png
│   ├── 06_validation_precision_recall_curves.png
│   ├── 07_validation_confusion_logistic_regression.png
│   ├── 08_validation_confusion_decision_tree.png
│   ├── 09_validation_confusion_random_forest.png
│   └── 10_test_confusion_logistic_regression.png
│
├── notebooks/
│   └── lead_conversion_ml_databricks_public.ipynb
│
├── results/
│   ├── validation_metrics.csv
│   ├── test_metrics.csv
│   ├── partition_summary.csv
│   └── business_summary.csv
│
├── data/
│   └── README.md
│
└── docs/
    ├── data_dictionary.md
    ├── model_card.md
    ├── privacy_rgpd.md
    └── reproducibility.md
```

---

# 26. Reproducibility

The public notebook documents the processing and modelling pipeline, but the original prospect dataset is intentionally not distributed.

Therefore the repository provides **methodological reproducibility**, not public row-level data reproducibility.

To rerun the project in an authorized internal environment:

1. provide a compliant table with the documented schema;
2. define the private Databricks table name;
3. ensure personal-identification fields remain outside the predictive feature set;
4. reproduce the temporal partitions;
5. run the common preprocessing pipeline;
6. compare models on validation;
7. lock the model choice;
8. evaluate test once;
9. validate threshold and business impact on future cohorts.

See [`docs/reproducibility.md`](docs/reproducibility.md).

---

# 27. Key takeaways

1. **Data preparation was more important than algorithm complexity.**
2. **No model dominated every validation metric.**
3. **Logistic Regression was selected for the PR-AUC / recall / interpretability trade-off.**
4. **The final model reached ROC-AUC 0.704, PR-AUC 0.501 and recall 0.652 on test.**
5. **The model-positive group concentrated conversions from a 30.3% baseline to 48.4% — about 1.6×.**
6. **This is ranking evidence, not causal proof of sales uplift.**
7. **The score should support human prioritization, not automatically exclude prospects.**
8. **Row-level personal data, individual scores and internal commercial performance are intentionally absent from the public repository.**

---

## Public-release note

This repository is a portfolio representation of a professional thesis project. It intentionally exposes the analytical method and safe aggregate results while withholding the original dataset and confidential operational outputs.

No original prospect record is required to understand the business problem, modelling logic, evaluation protocol or conclusions.