# Public Data Dictionary

This document describes the modelling schema used in the lead-conversion proof of concept.

**Important:** the repository does not contain the original row-level dataset. The table below documents column roles and public-release handling only.

| Variable | Family | Type | Used as model input? | Public handling |
|---|---|---|---|---|
| `id_lead` | Technical identification | string | No | Values withheld. Internal traceability only. |
| `date_inscription` | Technical / time | date | No direct input | Exact row-level dates withheld. |
| `partition_temporelle` | Experimental design | category | No | Aggregate partition counts published. |
| `annee_inscription` | Time | categorical | Yes | Schema published; row-level values withheld. |
| `mois_inscription` | Time | categorical | Yes | Schema published; row-level values withheld. |
| `pays_residence` | Profile / geography | categorical | Yes | Values not published at row level; potential quasi-identifier. |
| `canal_acquisition` | Acquisition | categorical | Yes | Detailed performance by modality withheld. |
| `campagne_base` | Acquisition | categorical | Yes | Campaign names and performance withheld from public outputs. |
| `categorie_formation` | Training | categorical | Yes | Detailed conversion performance withheld. |
| `format_formation` | Training | categorical | Yes | Schema only. |
| `niveau_formation` | Training | categorical | Yes | Schema only. |
| `eligible_cpf` | Financing | categorical | Yes | Schema only. |
| `mode_financement` | Financing | categorical | Yes | Detailed performance by modality withheld. |
| `statut_professionnel` | Profile | categorical | Yes | Row-level values withheld. |
| `formulaire_complete` | Engagement | categorical | Yes | Row-level values withheld. |
| `demande_brochure` | Engagement | categorical | Yes | Row-level values withheld. |
| `reponse_appel` | Commercial interaction | categorical | Yes | Row-level values withheld. |
| `rendez_vous` | Commercial interaction | categorical | Yes | Row-level values withheld. |
| `participation_webinaire` | Engagement | categorical | Yes | Row-level values withheld. |
| `duree_heures` | Training | numeric | Yes | Aggregate methodology only. |
| `budget_estime_eur` | Financing | numeric | Intended | Unusable in analysed run after text-to-number conversion produced 100% missing values. |
| `nb_clics_annonce` | Digital activity | numeric | Yes | Row-level values withheld. |
| `nb_visites_site` | Digital activity | numeric | Yes | Row-level values withheld. |
| `nb_relances` | Commercial interaction | numeric | Yes | Row-level values withheld. |
| `delai_premier_contact_jours` | Commercial interaction | numeric | Yes | Row-level values withheld. |
| `conversion` | Target | binary | Target | Only aggregate counts/metrics published. |

## Direct identifiers excluded from modelling and publication

The original operational context included direct identifiers used for prospect follow-up, such as names, first names, email addresses and telephone numbers.

These fields:
- are not predictive features in the public modelling description;
- are not included in this repository;
- are not included in any public output.

## Feature families

The model uses information available before the commercial outcome:
- time;
- acquisition;
- prospect context;
- training;
- financing;
- engagement;
- commercial interactions;
- digital activity.

Post-outcome information is excluded to reduce target leakage.

## Public-release principle

This is **not** a row-level anonymized dataset. No row-level dataset is distributed at all.

That decision avoids presenting pseudonymization as anonymization and minimizes re-identification risk in a public GitHub context.
