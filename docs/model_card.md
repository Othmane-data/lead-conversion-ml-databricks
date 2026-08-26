# Model Card — Lead Conversion Scoring Prototype

## Model purpose

Estimate a lead's probability of conversion so that a sales team can use the probability as a **prioritization signal**.

The model is intended for decision support. It is not designed to automatically reject, exclude or deprioritize a person without human review.

## Context

- Domain: professional training lead management
- Task: binary classification / probability ranking
- Final dataset: 383 leads
- Positive class: converted lead
- Positive rate: 31.85%
- Environment: Databricks workspace with Pandas and scikit-learn modelling

## Experimental partitions

| Partition | Leads | Conversions | Conversion rate |
|---|---:|---:|---:|
| Train | 230 | 77 | 33.48% |
| Validation | 77 | 22 | 28.57% |
| Test | 76 | 23 | 30.26% |

The test set is held out from model selection.

## Preprocessing

Categorical:
- most-frequent imputation
- One-Hot Encoding with unknown-category handling

Numeric:
- median imputation
- standardization

A scikit-learn `Pipeline` / `ColumnTransformer` applies preprocessing consistently.

## Candidate models

### Logistic Regression
- solver: `liblinear`
- max_iter: 1000
- class_weight: `balanced`
- random_state: 42

### Decision Tree
- max_depth: 4
- min_samples_leaf: 10
- class_weight: `balanced`
- random_state: 42

### Random Forest
- n_estimators: 100
- max_depth: 6
- min_samples_leaf: 5
- max_features: `sqrt`
- class_weight: `balanced`
- random_state: 42

## Validation performance

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 0.532 | 0.306 | 0.500 | 0.379 | 0.537 | 0.389 |
| Random Forest | 0.623 | 0.348 | 0.364 | 0.356 | 0.604 | 0.382 |
| Decision Tree | 0.468 | 0.289 | 0.591 | 0.388 | 0.467 | 0.277 |

## Selected model

**Logistic Regression**

Selection rationale:
- strongest validation PR-AUC;
- recall higher than Random Forest;
- directly usable probability output;
- easier to explain and operationalize;
- avoids choosing a more complex model based only on one global metric.

The choice is contextual and should be re-evaluated as data volume increases.

## Final test performance

After retraining on train + validation (307 leads):

| Metric | Value |
|---|---:|
| Accuracy | 0.684 |
| Precision | 0.484 |
| Recall | 0.652 |
| F1-score | 0.556 |
| ROC-AUC | 0.704 |
| PR-AUC | 0.501 |

Confusion matrix at threshold 0.50:
- TN = 37
- FP = 16
- FN = 8
- TP = 15

## Business interpretation

Test baseline conversion rate:
- 23 / 76 = 30.3%

Model-positive group:
- 31 leads
- 15 conversions
- conversion rate = 48.4%

Relative concentration:
- 48.4% / 30.3% ≈ 1.6x

This is evidence of useful historical ranking, not causal evidence of sales uplift.

## Known limitations

1. Dataset contains only 383 observations.
2. Validation and test partitions are small.
3. `budget_estime_eur` was unusable in the analysed run.
4. Threshold 0.50 is not optimized against measured business costs.
5. Hyperparameter optimization is intentionally limited.
6. Associations are predictive, not causal.
7. No prospective operational pilot has yet measured incremental business impact.
8. Data and behavioural patterns may drift over time.
9. Subgroup performance and fairness should be reviewed before operational deployment.

## Out-of-scope public outputs

Not published:
- individual lead scores;
- lead ranking;
- row-level data;
- direct identifiers;
- campaign/channel conversion performance;
- detailed modality-level coefficients / importances.

## Recommended monitoring

Predictive:
- recall
- precision
- PR-AUC
- calibration
- false-negative rate
- score distribution drift

Data:
- missingness
- duplicate rate
- category drift
- input schema / format errors

Business:
- conversion rate
- time to first contact
- leads processed
- follow-up volume
- conversions per unit of sales effort, if available

## Deployment principle

Use probability as a prioritization aid with human oversight.

Do not automatically exclude prospects solely because of a low model score.
