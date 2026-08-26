# Privacy, Confidentiality and GDPR-Oriented Public Release

## Scope

This document describes the **public portfolio publication policy** for the lead-conversion ML project.

It does not certify the legal compliance of the organization's complete internal processing. GDPR compliance depends on the controller's purposes, legal basis, information duties, retention periods, security, rights-management processes and other organizational measures that are outside the scope of this public repository.

## Why the raw dataset is not published

The original operational context contained or could be linked to personal information about prospects.

Examples of direct identifiers include:
- name;
- first name;
- email address;
- telephone number.

The internal dataset also contains contextual and behavioural fields that can relate to a natural person, such as geography, professional status, interactions and campaign history.

For a public GitHub repository, the safest publication decision is therefore:

> **Do not publish the row-level dataset.**

Only the schema, methodology and aggregate results are released.

## Anonymization vs pseudonymization

The CNIL distinguishes anonymization from pseudonymization:

- anonymization should make identification impossible in practice and irreversibly;
- pseudonymization replaces direct identifiers with aliases or indirect identifiers but can remain reversible or linkable;
- pseudonymized data remain personal data under the GDPR when individuals can still be identified with additional information.

For that reason, replacing a person's name with `lead_alias_001` is **not automatically equivalent to anonymization**.

The public repository therefore does not publish prospect-level technical IDs, individual scores or row-level quasi-identifiers.

Official reference:
- CNIL — *L’anonymisation de données personnelles*: https://www.cnil.fr/fr/technologies/lanonymisation-de-donnees-personnelles
- CNIL — *Identifier les données personnelles*: https://www.cnil.fr/fr/identifier-les-donnees-personnelles

## Data minimization

GDPR Article 5 includes the principle of data minimization: personal data should be adequate, relevant and limited to what is necessary for the stated purpose.

The public portfolio applies this principle by publishing:
- aggregate counts;
- aggregate model metrics;
- safe visualizations;
- schema and modelling logic.

It does not publish information that is unnecessary to demonstrate the project.

Official reference:
- Regulation (EU) 2016/679, Article 5: https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32016R0679

## Data protection by design and by default

GDPR Article 25 requires appropriate technical and organizational measures to implement data-protection principles effectively and ensure that, by default, only data necessary for each specific purpose are processed.

For the public release, this translates into:
- no raw data;
- no direct identifiers;
- no individual predictions;
- no internal commercial rankings;
- no unnecessary exact dates at row level;
- no private table/workspace identifiers.

Official reference:
- Regulation (EU) 2016/679, Article 25: https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32016R0679

## Profiling and human oversight

Lead scoring can constitute profiling when personal data are processed automatically to evaluate or predict aspects relating to a person.

The intended use of this prototype is:
- estimate a conversion probability;
- use it as a prioritization signal;
- keep a human salesperson in the decision loop.

The repository explicitly does **not** recommend a fully automated exclusion rule based only on the model score.

Where a system is used for automated individual decision-making with legal or similarly significant effects, additional GDPR requirements can apply. The exact applicability must be assessed in the real deployment context.

Official reference:
- EDPB — *Automated decision-making and profiling*: https://www.edpb.europa.eu/documents/guideline/automated-decision-making-and-profiling_en

## Business confidentiality

Privacy and business confidentiality are different concerns.

The original analysis contains potentially sensitive internal information such as:
- conversion rates by acquisition channel;
- campaign-level effectiveness;
- training-category performance;
- detailed modality-level feature weights;
- individual lead scores and ranking.

Those results are withheld from the public portfolio even when they are aggregate, because they could reveal internal commercial performance.

## Publication matrix

| Information | Public? | Rationale |
|---|---|---|
| Business problem | Yes | Necessary to understand use case |
| Dataset size | Yes | Aggregate and non-identifying |
| Target balance | Yes | Aggregate |
| Train/validation/test counts | Yes | Aggregate |
| Model hyperparameters | Yes | Methodological |
| Validation/test metrics | Yes | Aggregate |
| Confusion matrices | Yes | Aggregate |
| Direct identifiers | No | Personal data |
| Row-level records | No | Re-identification risk |
| Technical lead IDs in outputs | No | Pseudonymous, not necessarily anonymous |
| Individual scores | No | Profiling / confidentiality |
| Lead ranking | No | Profiling / confidentiality |
| Detailed channel/campaign performance | No | Business-sensitive |
| Detailed modality coefficients/importances | No | Business-sensitive and potential profiling insight |
| Private Databricks table/workspace identifiers | No | Internal system information |

## Recommended controls for a real operational deployment

A real deployment should additionally document and validate, as applicable:
- lawful basis and purpose limitation;
- information provided to data subjects;
- retention schedule;
- access control;
- security and logging;
- process for data-subject rights;
- data-quality governance;
- model versioning;
- threshold governance;
- subgroup / fairness monitoring;
- human review and escalation;
- impact assessment where required by the organization and legal context.

## Public-release conclusion

The portfolio intentionally demonstrates the ML workflow **without requiring publication of the original prospect data**.

That design preserves the project's technical and business value while reducing unnecessary privacy and confidentiality risk.
