# ISO/IEC 27001 ISMS Lab

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) [![CI](https://github.com/bizidwassim-design/iso27001-isms-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/bizidwassim-design/iso27001-isms-lab/actions/workflows/ci.yml) [![Fictional data](https://img.shields.io/badge/sample%20data-fictional-informational)](SECURITY.md)

> **No certification claim: this is a fictional training lab, not an audited ISMS.** Northwind Logistics FZ-LLC does not
> exist, no certification body has assessed anything here, and the laws named are summarised, not interpreted.

A complete **ISO/IEC 27001:2022 ISMS cycle** for one fictional 400-person UAE logistics company — context, risk
assessment, Statement of Applicability, internal audit and management review — where the same assets, risks, controls
and findings flow through every document. A build script generates the registers and workbooks from data, and a
validator proves that every ID resolves and all 93 Annex A controls are covered once.

> 🇫🇷 Résumé en français en bas de page.

## Layout

```
01-context/   organisation-context · interested-parties (REQ-01..14, incl. UAE PDPL and IA Regulation)
              isms-scope (boundaries, interfaces, exclusions) · information-security-policy · roles-and-responsibilities (RACI)
02-risk/      risk-methodology (5×5, acceptance criteria) · asset-register.csv · risk-register.csv (25 risks)
              risk-treatment-plan.csv (24 actions) · ISMS-Risk-Workbook.xlsx            ← generated except the methodology
03-soa/       statement-of-applicability.csv (93 controls) · Statement-of-Applicability.xlsx   ← generated
04-audit/     internal-audit-programme · internal-audit-report-2026 (2 NCs, 5 observations, 16 evidence refs)
              corrective-action-log.csv (9 actions with root cause)
05-review/    management-review-minutes-2026-10 (every clause 9.3 input and output, KPI/KRI table)
              isms-metrics-pack.md (generated) · continual-improvement-log.csv
data/         the sources you edit: assets, risks, treatment actions, SoA decisions
scripts/      build_isms.py (deterministic build) · validate_isms.py (consistency checks)
tests/        proves the validator fails on broken data
docs/         how-to-use.md — study it, train with it, fork it for your own ISMS
```

## Quick start

```bash
pip install openpyxl
python scripts/build_isms.py        # regenerate registers, workbooks and the metrics pack from data/
python scripts/validate_isms.py     # about 2,900 checks; exit code 1 on any broken link
python -m unittest discover -s tests -v
```

Then follow one thread end to end, as described in [docs/how-to-use.md](docs/how-to-use.md): internal issue IN-4 →
risk R-03 → treatment action RTP-05 → SoA A.5.18 → audit finding NC-2026-01 → corrective actions CA-01 and CA-02 →
KPI-05 in the management review.

## What's inside

| Stage | ISO/IEC 27001:2022 clauses | Files | What it demonstrates |
|---|---|---|---|
| Context | 4.1–4.4, 5.1–5.3 | `01-context/` | Issues, 14 requirements with stable IDs, a testable scope with interfaces and justified exclusions, a one-page policy with objectives, a RACI with one accountable role per activity |
| Risk | 6.1.2, 6.1.3, 8.2, 8.3 | `02-risk/` | 5×5 method with acceptance criteria and appetite, 20 assets, 25 risks with inherent / residual / target scores, all four treatment options, a dated treatment plan with 2 overdue actions |
| SoA | 6.1.3 d) | `03-soa/` | All 93 Annex A controls (ID and short title), own one-line justification, one exclusion, status, linked risks, requirements and actions |
| Audit | 9.2, 10.2 | `04-audit/` | Three-year risk-weighted programme, a report with 2 minor nonconformities and 5 observations traced to evidence, corrective actions with root cause and effectiveness review |
| Review | 9.1, 9.3, 10.1 | `05-review/` | Minutes with every 9.3.2 input and 9.3.3 output under its own heading, 14 KPIs and KRIs, decisions, resources, actions, continual-improvement log |

### The workbooks

| Workbook | Sheets | Built-in logic |
|---|---|---|
| `02-risk/ISMS-Risk-Workbook.xlsx` | Method · Assets · Risk Register · Heat Map · Treatment Plan | Score and rating are formulas; 1–5 and treatment-option dropdowns; rating colours; three live 5×5 heat maps (inherent, residual, target); overdue actions in red |
| `03-soa/Statement-of-Applicability.xlsx` | Summary · SoA | Live counts by theme and status, implemented share of applicable controls, Yes/No and status dropdowns |

### What the validator checks

* All 93 Annex A:2022 control IDs are present exactly once in the SoA, and nothing else is.
* Every applicable control links to at least one risk or requirement; an excluded control is used by no risk.
* Scores equal likelihood × impact; residual ≤ inherent; target ≤ residual; every target within appetite (≤ 9).
* Retained risks have no open actions; every other risk has at least one; when all actions are done, target = residual.
* Every risk ID referenced by the SoA and the treatment plan exists; each action's controls belong to its risks.
* A control cannot be *Implemented* while a treatment action on it is still open; overdue status matches the dates.
* Every corrective action references an existing finding; every nonconformity has a corrective action.
* The minutes cover each clause 9.3 input and output by name; the RACI has one **A** per activity.
* Every ID mentioned in any document (`AST-`, `R-`, `RTP-`, `A.x.y`, `REQ-`, `NC-`/`OBS-`, `E-`, `CA-`, `CI-`, `MR`, `KPI-`/`KRI-`) is defined.
* The workbooks match the CSV registers. CI also checks that the generated files are committed up to date (`git diff --exit-code`).

## Design choices

* **One organisation, one story.** A recruiter or auditor can pick any ID and follow it through context, risk, SoA,
  audit and review. That traceability is what an ISMS lead is actually judged on.
* **Three scores per risk.** Inherent shows exposure, residual shows today's controls, target shows what the plan buys.
  The validator stops "paper" risk reduction: a target only differs from residual while an action is still open.
* **Imperfect on purpose.** Two treatment actions are overdue, a nonconformity exists, objectives are missed. A
  realistic first-year ISMS has gaps; showing how they are handled is the point.
* **Data in, documents out.** Registers and workbooks are generated from four CSV files, so they cannot drift apart.
  The build is deterministic: running it twice gives byte-identical files.
* **Original wording.** ISO/IEC 27001 is referenced by clause number and Annex A ID with short titles only. The UAE
  PDPL and the UAE Information Assurance Regulation are named and summarised in our own words, never reproduced.

## Related repositories

| Repository | How it relates |
|---|---|
| [iso27001-iso42001-toolkit](https://github.com/bizidwassim-design/iso27001-iso42001-toolkit) | Blank templates and policies; this lab shows them filled in for one organisation |
| [application-risk-assessment-template](https://github.com/bizidwassim-design/application-risk-assessment-template) | Same 5×5 scoring bands, applied to a single application |
| [grc-control-crosswalk](https://github.com/bizidwassim-design/grc-control-crosswalk) | Maps the Annex A IDs used here to NIST CSF 2.0, CIS v8 and SOC 2 |
| [soc-detection-playbooks](https://github.com/bizidwassim-design/soc-detection-playbooks) | Detection content behind A.8.15, A.8.16 and the incident playbooks of RTP-20 |
| [ciso-executive-dashboard](https://github.com/bizidwassim-design/ciso-executive-dashboard) | Board-level view of the KPIs and KRIs reported in the management review |
| [public-scripts](https://github.com/bizidwassim-design/public-scripts) | Scripts that collect the kind of evidence cited in the audit report (sign-ins, access, configuration) |

## Contributing

Better worked examples, new consistency checks and translations are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).
Keep all data fictional and all wording original.

## Disclaimer

A training lab with fictional data, not legal advice and not an audited ISMS. It does not guarantee or imply
certification. Read the official texts of ISO/IEC 27001:2022, the UAE PDPL and the UAE IA Regulation, and have your own
ISMS reviewed by your auditor and counsel.

## AI assistance

Built with Claude Code as a coding and writing assistant, which is why it appears as a co-author on some commits.
**Editor and reviewer: Wassim Bizid**, who set the scope, the frameworks and the GRC approach, edited the content
and decided what was published. Automated tests in CI check the published outputs. This is a maintainer review,
not an independent one.

## License

[MIT](LICENSE).

---

## 🇫🇷 Résumé

Laboratoire open source montrant un **cycle complet de SMSI ISO/IEC 27001:2022** pour une entreprise de logistique
fictive des Émirats (Northwind Logistics FZ-LLC, 400 personnes) : contexte et parties intéressées (dont la loi PDPL et la
réglementation IA des Émirats), périmètre, politique, RACI, méthode de risque 5×5, 25 risques et plan de traitement,
Déclaration d'applicabilité couvrant les 93 mesures de l'Annexe A, programme et rapport d'audit interne (2 non-conformités,
5 observations), actions correctives et revue de direction couvrant chaque entrée et sortie de la clause 9.3. Registres et
classeurs Excel générés par script, cohérence vérifiée en CI. Données fictives, aucune prétention de certification. Licence MIT.
