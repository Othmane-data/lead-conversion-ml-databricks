# Reproducibility Guide

## Reproducibility level

This public repository provides **methodological reproducibility**.

The original prospect dataset is not published because it contains or may be linkable to personal and business-sensitive information.

Therefore a public user can inspect:
- the modelling schema;
- cleaning logic;
- preprocessing pipeline;
- model definitions;
- aggregate executed results;
- safe visual outputs.

A public user cannot reproduce the exact row-level execution without an authorized dataset with the same schema.

## Environment

The experiment was executed in Databricks.

The modelling layer uses:
- Python
- Pandas
- NumPy
- Matplotlib
- scikit-learn

Spark is used to read the private Databricks table before conversion to Pandas. The model itself is not presented as a distributed PySpark workload.

## Expected source schema

See:
- `docs/data_dictionary.md`

The private source must contain:
- technical fields;
- the documented categorical variables;
- the documented numeric variables;
- binary target `conversion`.

## Public notebook configuration

The public notebook uses a placeholder:

```python
TABLE_NAME = "<private_catalog>.<private_schema>.<private_leads_table>"
```

An authorized internal user should replace this with the actual table name.

The public repository must not be updated with that internal source value.

## Execution order

1. Load authorized internal data.
2. Normalize column names.
3. Select only required fields.
4. Clean IDs, categories, dates and numeric values.
5. Remove duplicates.
6. Validate the binary target.
7. Validate temporal partition values.
8. Inspect missingness.
9. Build train / validation / test datasets.
10. Fit preprocessing within the model pipeline.
11. Train all candidate models on train.
12. Evaluate candidates on validation.
13. Select the model without consulting test.
14. Retrain selected model on train + validation.
15. Evaluate test once.
16. Translate probability into a business prioritization signal.
17. Validate the score prospectively before claiming commercial uplift.

## Current executed aggregate results

Validation:

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 0.532 | 0.306 | 0.500 | 0.379 | 0.537 | 0.389 |
| Random Forest | 0.623 | 0.348 | 0.364 | 0.356 | 0.604 | 0.382 |
| Decision Tree | 0.468 | 0.289 | 0.591 | 0.388 | 0.467 | 0.277 |

Final Logistic Regression test:

| Metric | Value |
|---|---:|
| Accuracy | 0.684 |
| Precision | 0.484 |
| Recall | 0.652 |
| F1 | 0.556 |
| ROC-AUC | 0.704 |
| PR-AUC | 0.501 |

## Known reproducibility issue

`budget_estime_eur` was stored in text format. The analysed run converted the entire field to missing numeric values.

Before a future re-run:
- normalize currency formatting;
- remove currency symbols and thousands separators safely;
- validate numeric conversion;
- assert a reasonable non-missing rate before fitting.

Any future corrected run should be treated as a **new model version**, not silently substituted for the published result.

## Confidential outputs

Do not add these to GitHub:
- source CSV/XLSX exports;
- internal Databricks table extracts;
- row-level predictions;
- individual score files;
- lead ranking;
- names/emails/phone numbers;
- campaign-level commercial performance;
- private credentials or workspace URLs.

## Suggested versioning

For future experiments record:
- execution date;
- data window;
- number of leads;
- model version;
- preprocessing version;
- threshold;
- validation metrics;
- test or out-of-time metrics;
- business pilot results.

This will make performance drift and model evolution traceable.
