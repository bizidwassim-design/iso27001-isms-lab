# Internal audit report IA-2026

| Document | ISMS-AUD-02 · version 1.0 · issued 2026-10-02 · lead auditor: finance controls team (internal) · distribution: ISMS Steering Committee |
|---|---|
| ISO/IEC 27001:2022 reference | Clause 9.2 Internal audit · Clause 10.2 Nonconformity and corrective action |
| Audit window | 2026-09-14 to 2026-09-25, Dubai head office, Dubai distribution centre, remote sessions with Abu Dhabi |

> Fictional audit of a fictional organisation, written as a model report. Not an audit opinion on any real ISMS and not
> a certification audit.

## 1. Objective, scope and criteria

* **Objective**: determine whether the ISMS conforms to Northwind's own requirements and to ISO/IEC 27001:2022, and
  whether it is effectively implemented and maintained (clause 9.2.1).
* **Scope**: clauses 4 to 10 and the Annex A focus areas of IA-2026 in the [audit programme](internal-audit-programme.md).
* **Criteria**: ISO/IEC 27001:2022; the [information security policy](../01-context/information-security-policy.md) and
  topic policies; the [SoA](../03-soa/statement-of-applicability.csv) v1.2; the [risk treatment plan](../02-risk/risk-treatment-plan.csv).
* **Method**: interviews, document review, system observation and sampling. Samples were drawn at random from complete
  populations exported by the auditees in the auditor's presence.

## 2. Summary

The ISMS is established and operating. Leadership commitment is visible, the risk method is applied consistently and the
Statement of Applicability is traceable to risks and requirements. Two minor nonconformities and five observations were
raised. No major nonconformity was found.

| Grade | Count | IDs |
|---|---|---|
| Major nonconformity | 0 | — |
| Minor nonconformity | 2 | NC-2026-01, NC-2026-02 |
| Observation | 5 | OBS-2026-01 to OBS-2026-05 |

### Strengths noted

* Privileged access is fully under PIM with approval; no standing Global Administrator assignment (E-10).
* Phishing-resistant MFA rolled out to finance and admins ahead of plan (E-11).
* PDPL records of processing are complete and approved; the DPO demonstrated a data subject request end to end (E-16).

## 3. Findings

### NC-2026-01 — Leaver access not removed on time

* **Grade**: minor nonconformity
* **Requirement**: Annex A A.5.18 Access rights and A.6.5 Responsibilities after termination, as implemented by the
  access control policy section 6 (accounts disabled by the end of the last working day).
* **Finding**: 3 of 25 leavers sampled between January and August 2026 still had enabled Entra ID accounts 6, 9 and 14
  days after their last working day. One of the three accounts signed in to Outlook on the web 3 days after the
  person's departure (sign-in from the person's registered device, no data downloaded according to the audit log).
* **Evidence**: E-01, E-02, E-03
* **Linked risk**: R-03 (residual 9, Medium). The control gap is already in the treatment plan as RTP-05, but no interim
  measure was in place.

### NC-2026-02 — Risk treatment actions for backup and recovery not implemented as planned

* **Grade**: minor nonconformity
* **Requirement**: clause 8.3 (implement the risk treatment plan) and clause 6.1.3 e) (risk owners approve the plan);
  Annex A A.8.13 Information backup and A.5.30 ICT readiness for business continuity.
* **Finding**: RTP-12 (WMS failover test, due 2026-09-30) and RTP-23 (quarterly restore tests) were not performed.
  Only one of six planned restore tests for Q2 and Q3 has evidence. The due dates passed without a revised date approved
  by the risk owner, and the overdue status was not reported to the Steering Committee in September.
* **Evidence**: E-04, E-05, E-06
* **Linked risks**: R-09, R-23 and R-02. R-02 and R-23 are High at residual; their target scores depend on these actions.

### OBS-2026-01 — OT asset inventory incomplete

* **Requirement**: A.5.9 Inventory of information and other associated assets.
* **Observation**: the walk-down of the conveyor line found 6 devices (the two HMI workstations and four sortation
  controllers) missing from the OT inventory, and firmware versions absent for 38% of PLCs. RTP-10 is in progress.
* **Evidence**: E-07
* **Linked risks**: R-07, R-08

### OBS-2026-02 — Awareness completion below objective on warehouse shifts

* **Requirement**: clause 7.3 Awareness; A.6.3 Information security awareness, education and training; objective O-4.
* **Observation**: overall completion 88% against a 95% objective; night-shift warehouse staff at 71%. The online course
  is in English only and needs a laptop that most shift staff do not have.
* **Evidence**: E-08
* **Linked risk**: R-21

### OBS-2026-03 — Portal log retention below the logging standard

* **Requirement**: A.8.15 Logging; logging standard requires 12 months for internet-facing applications.
* **Observation**: the portal's application logs are kept for 30 days in Application Insights and are not yet sent to
  Sentinel. RTP-19 addresses this, due 2026-12-31.
* **Evidence**: E-09
* **Linked risk**: R-19

### OBS-2026-04 — Supplier access granted before due diligence

* **Requirement**: A.5.19 Information security in supplier relationships; supplier security policy section 3.
* **Observation**: 2 of 6 suppliers onboarded in 2026 (a carrier and a customs broker) received portal API credentials
  before their security questionnaire was returned. Both questionnaires were later completed with no high-risk answers.
* **Evidence**: E-12, E-13
* **Linked risk**: R-24

### OBS-2026-05 — KPI definitions incomplete

* **Requirement**: clause 9.1 b) and c) (methods, and when monitoring and measuring is performed).
* **Observation**: 3 of the 12 KPIs and KRIs reported to the Steering Committee have no documented data source or
  calculation method, so trends cannot be reproduced (KPI-03, KPI-07, KRI-03).
* **Evidence**: E-14

## 4. Evidence register

| Ref | Evidence | Source | Collected |
|---|---|---|---|
| E-01 | Leaver list January–August 2026 (82 leavers), random sample of 25 | Fabrikam HR export | 2026-09-16 |
| E-02 | Entra ID account status and disable dates for the 25 sampled leavers | Entra ID audit log export | 2026-09-16 |
| E-03 | Sign-in log extract for the three late accounts | Entra ID sign-in logs | 2026-09-17 |
| E-04 | Risk treatment plan v1.2 with status history | ISMS SharePoint site | 2026-09-15 |
| E-05 | Restore test records Q2–Q3 2026 (one record found) | IT team site, Azure Backup job history | 2026-09-18 |
| E-06 | Steering Committee minutes July–September 2026 | ISMS SharePoint site | 2026-09-15 |
| E-07 | OT inventory spreadsheet compared with walk-down photographs | Warehouse Operations; auditor walk-down | 2026-09-21 |
| E-08 | Awareness completion report by department and shift | Learning management system export | 2026-09-22 |
| E-09 | Application Insights retention setting and Sentinel data connector list | Azure portal, observed | 2026-09-22 |
| E-10 | PIM role assignment report | Entra ID PIM export | 2026-09-17 |
| E-11 | Authentication methods report for finance and admin groups | Entra ID report | 2026-09-17 |
| E-12 | Supplier onboarding records 2026 (6 suppliers) | ERP supplier register | 2026-09-23 |
| E-13 | Portal API key issue dates for the two suppliers | Portal admin audit trail | 2026-09-23 |
| E-14 | KPI definitions sheet and Q2 Steering Committee pack | ISMS SharePoint site | 2026-09-24 |
| E-15 | Statement of Applicability v1.2 and risk register v1.2 (traced 5 risks) | ISMS SharePoint site | 2026-09-15 |
| E-16 | Records of processing and a data subject request walkthrough | DPO | 2026-09-24 |

## 5. Conclusion

The ISMS conforms to ISO/IEC 27001:2022 in the areas audited, except for the two minor nonconformities above. The
auditee agreed all findings at the closing meeting on 2026-09-25. Corrective actions with root causes are in the
[corrective-action log](corrective-action-log.csv) and the results feed the
[management review](../05-review/management-review-minutes-2026-10.md).
