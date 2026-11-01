# Internal audit programme 2026–2028

| Document | ISMS-AUD-01 · version 1.0 · owner: Information Security Manager · approved by: ISMS Steering Committee, 2026-04-28 · next review: 2027-04 |
|---|---|
| ISO/IEC 27001:2022 reference | Clause 9.2.1 General · 9.2.2 Internal audit programme · Annex A A.5.35 |

> Fictional organisation. The programme shows how to spread Annex A over three years while auditing every clause
> every year.

## 1. Principles

* **Every year**: clauses 4 to 10 in full, plus every control linked to a High or Critical **residual** risk.
* **Over three years**: every applicable Annex A control at least once.
* **Risk-weighted**: the higher a control's linked residual risk, the earlier and more deeply it is sampled.
* **Independence**: auditors never audit their own work. The lead auditor comes from the finance controls team and
  holds an ISO/IEC 27001 internal auditor certificate; a second auditor from the HR compliance team is in training.
  The ISM manages the programme but is audited by them, not the other way round, for clauses 6, 9 and 10.
* **Evidence**: each finding cites dated evidence by `E-` reference (see the [2026 report](internal-audit-report-2026.md)).

## 2. Three-year plan

| Audit | Window | Clauses | Annex A focus | Why now |
|---|---|---|---|---|
| IA-2026 | 2026-09-14 to 2026-09-25 | 4–10 | Identity and access (A.5.15–A.5.18, A.8.2, A.8.5), backup and continuity (A.5.29, A.5.30, A.8.13, A.8.14), OT and networks (A.5.9, A.8.20, A.8.22), suppliers (A.5.19–A.5.22), awareness (A.6.3), logging (A.8.15, A.8.16) | Linked to the four High residual risks R-02, R-07, R-08, R-23 and to client questionnaire findings |
| IA-2027 | 2027-05 (two weeks) | 4–10 | Secure development (A.8.25–A.8.33), privacy (A.5.31–A.5.34, A.8.10–A.8.12), incident management (A.5.24–A.5.28), cloud (A.5.23), physical (A.7.1–A.7.14) | Portal pipeline changes complete; PDPL controls one year old |
| IA-2028 | 2028-05 (two weeks) | 4–10 | Remaining organizational and people controls (A.5.1–A.5.14, A.5.36, A.5.37, A.6.1–A.6.8), remaining technological controls | Completes three-year coverage |
| Follow-up | Within 90 days of each audit | 10.2 | Verify corrective actions for every nonconformity | Closes the loop before the management review |

## 3. 2026 audit plan (IA-2026)

| Day | Area | Auditees | Sample |
|---|---|---|---|
| 1 | Opening meeting; clauses 4, 5 (context, scope, policy, roles) | CEO, ISM | Context, interested parties, scope, policy, RACI |
| 2 | Clause 6 (risk assessment, treatment, SoA, objectives) | ISM, two risk owners | 5 risks traced from register to SoA to evidence |
| 3–4 | Identity and access | Head of IT, HR Director | 25 leavers Jan–Aug 2026; 10 movers; all admin roles |
| 5 | Backup and continuity | Head of IT | Restore test records Q2–Q3; DR plan; backup configuration |
| 6 | OT and networks (on site at the Dubai distribution centre) | Warehouse Operations Director, conveyor vendor | OT inventory against a walk-down of the line; firewall rules |
| 7 | Suppliers | Procurement Manager | 6 suppliers onboarded in 2026; MSP contract |
| 8 | Awareness, logging | HR Director, ISM | LMS completion export; Sentinel data connectors and retention |
| 9 | Clauses 7, 9, 10 (support, performance evaluation, improvement) | ISM | Document control, KPI definitions, CA log |
| 10 | Closing meeting | Steering Committee members | Draft findings agreed |

## 4. Grading

| Grade | Definition used in this ISMS |
|---|---|
| Major nonconformity | A requirement is not met at all, or a failure that throws doubt on the ISMS achieving its outcomes |
| Minor nonconformity | A requirement is partly met; an isolated or limited failure |
| Observation | Requirement met, but a weakness that could become a nonconformity if left alone |
| Opportunity for improvement | Suggestion with no compliance gap |

Every nonconformity gets a corrective action with root cause in the [corrective-action log](corrective-action-log.csv);
observations get an action when the owner agrees one is useful.
