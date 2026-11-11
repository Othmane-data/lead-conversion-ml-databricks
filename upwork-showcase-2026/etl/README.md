# 04 — Automated Data Quality & ETL: Python + SQL

![ETL portfolio visual](../assets/etl.svg)

**Problem:** Source extracts can contain duplicate transaction IDs, inconsistent statuses, padded identifiers, missing amounts and negatives. These defects can distort reports.

**Approach:** Ingest CSV → normalize text → enforce deduplication → validate non-null and nonnegative amounts → export normalized records to CSV and SQLite → query counts and totals.

**Reproduce:** [Python pipeline](../src/etl_demo.py) and [SQL validation](quality_checks.sql).

**What a client receives in such a scoped engagement:** A written mapping of input fields, transformations, rejected records, checks, reproducible output and a handover guide.

**Transparency:** The example contains fictional transaction records. It does not claim an actual production automation or time savings from a client project. Scheduling, APIs, cloud storage and credentials are out of scope.
