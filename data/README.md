# Data Availability

The original lead dataset is **not included** in this public repository.

## Why

The source data come from a professional prospect-management context and contain or may be linked to:
- direct personal identifiers;
- pseudonymous technical identifiers;
- behavioural information;
- commercial-interaction information;
- campaign and channel information;
- business-sensitive performance information.

Publishing a row-level file would create unnecessary re-identification and confidentiality risk.

## What is published instead

The repository provides:
- the modelling schema in `docs/data_dictionary.md`;
- aggregate dataset statistics;
- aggregate model metrics;
- confusion matrices and safe aggregate visualizations;
- a public notebook with confidential outputs removed.

## Dataset size used in the executed experiment

- Total: 383 leads
- Converted: 122
- Non-converted: 261
- Train: 230
- Validation: 77
- Test: 76

## Important terminology

The absence of names does not automatically make row-level data anonymous.

A technical alias such as `lead_alias_001` can be pseudonymous rather than anonymous if linkage or re-identification remains possible.

For this reason, no row-level “anonymized” dataset is distributed here.
