# Risk assessment and treatment methodology

| Document | ISMS-RSK-01 · version 1.1 · owner: Information Security Manager · approved by: ISMS Steering Committee, 2026-02-05 · next review: 2027-02 |
|---|---|
| ISO/IEC 27001:2022 reference | Clause 6.1.2 Information security risk assessment · 6.1.3 Information security risk treatment · 8.2 · 8.3 |

> Fictional organisation. The method is deliberately simple so that two assessors scoring the same scenario land on the
> same number.

## 1. When we assess

* Once a year in full (the 2026 assessment ran from 2026-02-16 to 2026-03-05; register v1.0 approved 2026-03-12).
* When something significant changes: a new system, supplier, site or regulation, a major incident or an audit finding.
* At each data cut for the management review, residual scores are refreshed to reflect controls actually operating.

## 2. How we describe a risk

One sentence that names **the event, its cause and its consequence**, linked to the assets in the
[asset register](asset-register.csv). Example (R-03): *accounts of leavers stay enabled because HR does not notify IT in
time, allowing unauthorised access to email and the WMS*. Each risk has one **risk owner**: the manager with the
authority and budget to treat it.

## 3. Scales

| Score | Likelihood (within 12 months) | Impact (worst credible outcome) |
|---|---|---|
| 1 | **Rare** — not expected; no known occurrence in the sector | **Negligible** — under AED 50k, no customer notices, no personal data |
| 2 | **Unlikely** — could happen; seen in the sector | **Minor** — AED 50k–250k, one customer affected, WMS down under 2 h, a handful of records |
| 3 | **Possible** — has happened to peers in the last two years | **Moderate** — AED 250k–1m, several customers, WMS down 2–8 h, a notifiable breach of a few hundred records |
| 4 | **Likely** — has happened to us or happens to peers yearly | **Major** — AED 1m–5m, loss of a key customer, WMS down over 8 h (RTO missed), regulator involvement |
| 5 | **Almost certain** — expected, or already happening | **Severe** — over AED 5m, several key customers lost, multi-day outage at peak, licence or contract termination |

Score impact on the **worst** of financial, customer, operational, legal and personal-data consequences.

## 4. Score, rating and acceptance criteria

`score = likelihood × impact` (1 to 25).

| Rating | Score | Acceptance criterion (clause 6.1.2 a) 1) |
|---|---|---|
| Low | 1–4 | Accepted by the risk owner |
| Medium | 5–9 | Accepted by the risk owner; reviewed quarterly by the ISM |
| High | 10–14 | Outside appetite: treat. The Steering Committee may retain it for at most 12 months with a recorded rationale |
| Critical | 15–25 | Not acceptable: treat immediately and escalate to the Board |

**Risk appetite: every risk must have a target score of 9 or less.** The validator enforces this on the register.

## 5. Three scores per risk

| Score | Meaning |
|---|---|
| Inherent | Plausible exposure if none of the listed controls existed |
| Residual | With the controls actually operating at the data cut (evidence available) |
| Target | Once every open treatment action for the risk is complete |

Rules checked by `scripts/validate_isms.py`: residual ≤ inherent; target ≤ residual; target within appetite; a
*Retain* risk has no open actions and target = residual; any other option has at least one action; when all of a risk's
actions are done, target = residual (the benefit has been realised).

## 6. Treatment options (clause 6.1.3)

| Option | Use when | Example |
|---|---|---|
| Modify | Controls can bring the risk down at a sensible cost | R-07 OT segregation firewall |
| Retain | Residual is already within appetite | R-16 physical intrusion at the cross-dock |
| Avoid | Stopping the activity is cheaper than controlling it | R-12 overseas file-transfer website withdrawn |
| Share | A contract or insurance moves part of the consequence | R-06 payment provider liability clause |

For each treated risk we compare the chosen controls with Annex A (clause 6.1.3 c) so nothing necessary is missed, and
the result is the [Statement of Applicability](../03-soa/statement-of-applicability.csv). Treatment actions go into the
[risk treatment plan](risk-treatment-plan.csv) with an owner, start and due date; the risk owner approves the plan and
any later change of date.

## 7. Files and how they are produced

You edit the sources in `data/`; `python scripts/build_isms.py` computes scores, ratings, acceptance decisions and links,
then writes the CSV registers, `ISMS-Risk-Workbook.xlsx` (with live formulas, dropdowns and heat maps) and the
[metrics pack](../05-review/isms-metrics-pack.md).
