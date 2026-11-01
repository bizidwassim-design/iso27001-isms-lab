# Management review minutes — October 2026

| Document | ISMS-MR-02 · minutes approved by the CEO on 2026-10-30 · next review: April 2027 |
|---|---|
| ISO/IEC 27001:2022 reference | Clause 9.3.1 General · 9.3.2 Management review inputs · 9.3.3 Management review results |
| Meeting | 2026-10-29, 10:00–12:30, Dubai head office board room and Teams |
| Chair | CEO |
| Present | COO, CFO, Head of IT, Information Security Manager (secretary), Data Protection Officer, HR Director, Head of Digital, Warehouse Operations Director |
| Inputs circulated | [ISMS metrics pack](isms-metrics-pack.md) (data cut 2026-10-26), [internal audit report IA-2026](../04-audit/internal-audit-report-2026.md), [corrective-action log](../04-audit/corrective-action-log.csv), [risk register](../02-risk/risk-register.csv) v1.3, [SoA](../03-soa/statement-of-applicability.csv) v1.3 |

> Fictional minutes of a fictional organisation. Each clause 9.3.2 input and 9.3.3 output has its own heading so an
> auditor (and `scripts/validate_isms.py`) can find it.

## 1. Purpose

Second management review of the ISMS (the first was held on 2026-04-28). Purpose: decide whether the ISMS remains
suitable, adequate and effective, and what must change before the 2027 risk assessment.

## 2. Inputs (clause 9.3.2)

### 9.3.2 a) Status of actions from previous management reviews

| ID | Action from 2026-04-28 | Owner | Status | Comment |
|---|---|---|---|---|
| MR1-01 | Fund PIM and phishing-resistant MFA for admins and finance | Head of IT | Done | Delivered as RTP-01 and RTP-06 |
| MR1-02 | Complete PDPL records of processing and the breach notification playbook | Data Protection Officer | Done | Delivered as RTP-14 |
| MR1-03 | Approve the internal audit programme and train a second internal auditor | Information Security Manager | Partly done | Programme approved; second auditor in training until December |
| MR1-04 | Choose the OT segregation approach | Warehouse Operations Director | Done | Industrial firewall purchased (RTP-09) |
| MR1-05 | Define the KPI and KRI set for the Steering Committee | Information Security Manager | Done | Definitions were incomplete (OBS-2026-05), fixed by CA-09 |

### 9.3.2 b) Changes in external and internal issues

* **External**: peak season forecast at +35% volume against 2025, increasing the impact of a WMS outage (R-09). Two
  regional logistics peers reported ransomware incidents this quarter (EX-4). The insurer's renewal now asks for
  quarterly restore evidence.
* **Internal**: the conveyor line in Dubai was extended with four sortation controllers, which were not in the OT
  inventory (OBS-2026-01). Defender for Cloud Apps discovery found seven unsanctioned apps receiving customer data (R-22).
* **Decision**: the [organisation context](../01-context/organisation-context.md) stays valid; no change of scope needed.

### 9.3.2 c) Changes in needs and expectations of interested parties

* Insurer: restore evidence every quarter, now part of REQ-07.
* Port operator client: asked for written confirmation of where its cargo data is hosted; REQ-13 wording clarified
  (MR2-03).
* No new legal requirement identified; the DPO continues to track PDPL guidance.

### 9.3.2 d) Feedback on information security performance

#### d) 1. Nonconformities and corrective actions

Two minor nonconformities (NC-2026-01 leaver access, NC-2026-02 backup and recovery actions) and five observations from
IA-2026. Nine corrective actions logged: one closed and verified (CA-09), seven in progress, one open (CA-04, depends on
the DR test on 2026-11-20). None is past its due date (KRI-04).

#### d) 2. Monitoring and measurement results

| ID | Metric | Target | Q2 2026 | Q3 2026 | Status |
|---|---|---|---|---|---|
| KPI-01 | Awareness training completion | ≥ 95% | 82% | 88% | Amber |
| KPI-02 | Phishing simulation click rate | ≤ 5% | 9.1% | 6.4% | Amber |
| KPI-03 | Critical vulnerabilities on internet-facing systems fixed within 14 days | ≥ 95% | 78% | 91% | Amber |
| KPI-04 | Endpoints compliant with the Intune baseline | ≥ 98% | 96.2% | 98.4% | Green |
| KPI-05 | Leavers disabled by the end of their last working day | 100% | 84% | 88% | Red |
| KPI-06 | Admin roles eligible-only in PIM | 100% | 71% | 100% | Green |
| KPI-07 | Treatment actions completed by their due date | ≥ 90% | 100% (2 of 2) | 80% (8 of 10) | Red |
| KPI-08 | Planned restore tests performed | 100% | 33% (1 of 3) | 0% (0 of 3) | Red |
| KRI-01 | Risks with residual rating High or Critical | 0 Critical, ≤ 2 High | 1 Critical, 7 High | 0 Critical, 4 High | Amber |
| KRI-02 | P1 and P2 security incidents | ≤ 1 per quarter | 1 | 2 | Amber |
| KRI-03 | Mean time to contain P1 and P2 incidents | ≤ 4 h | 6.5 h | 3.2 h | Green |
| KRI-04 | Corrective actions past their due date | 0 | 0 | 0 | Green |
| KRI-05 | New suppliers with system access but no due diligence | 0 | — | 0 | Green |
| KRI-06 | Unsanctioned cloud apps receiving customer data | 0 | — | 7 | Red |

KRI-05 and KRI-06 were added after the audit; all 14 metrics now have a definition (CA-09). The two Q3 incidents were a
business email compromise attempt stopped by the supplier call-back check (R-01) and a ransomware precursor contained
on one laptop by EDR (R-02). Neither involved personal data.

#### d) 3. Audit results

The internal audit concluded that the ISMS conforms in the areas audited except for NC-2026-01 and NC-2026-02. Strengths:
PIM, phishing-resistant MFA, PDPL records. The penetration test of the portal (June) found no critical issue; two
high-severity findings were fixed within 30 days (RTP-07 is adding continuous testing).

#### d) 4. Fulfilment of information security objectives

| Objective | Result | Status |
|---|---|---|
| O-1 No notifiable personal data breach | 0 breaches in 2026 | On track |
| O-2 All target risk scores within appetite (≤ 9) | 25 of 25 (metrics pack) | Met |
| O-3 Two successful WMS DR tests a year | 0 of 2 | Not met (NC-2026-02) |
| O-4 Awareness ≥ 95% and click rate ≤ 5% | 88% and 6.4% | Not met, improving |
| O-5 Leavers disabled on time 100% | 88% | Not met (NC-2026-01) |

### 9.3.2 e) Feedback from interested parties

* Two of the five largest shippers returned their annual questionnaire review with no open items; one asked for DR test
  evidence, which will be sent after 2026-11-20.
* The insurer renewed cover with a condition on quarterly restore testing (see 9.3.2 c).
* The port operator's site audit of Northwind staff in August raised no finding.
* Staff suggestion box: drivers asked for a report-phishing button on mobile Outlook (done, CI-05).

### 9.3.2 f) Results of risk assessment and status of risk treatment plan

From the [metrics pack](isms-metrics-pack.md):

* 25 risks. Inherent: 6 Critical, 9 High, 10 Medium. Residual: 0 Critical, 4 High, 17 Medium, 4 Low. Target: 13 Low,
  12 Medium; every target is within appetite.
* The four High residual risks are R-07 and R-08 (OT network), and R-02 and R-23 (ransomware and backups). Their target
  scores depend on RTP-09, RTP-10, RTP-11 and RTP-23.
* Treatment plan: 24 actions — 9 done, 11 in progress, 2 planned, 2 overdue (RTP-12, RTP-23, both 26 days late at the
  data cut).
* SoA v1.3: 92 of 93 controls applicable (A.8.30 excluded); 63 implemented (68% of applicable), 28 partially
  implemented, 1 planned (A.8.11).
* Retained risks R-14, R-15, R-16 and R-25 confirmed by their owners.

### 9.3.2 g) Opportunities for continual improvement

Reviewed from the [continual-improvement log](continual-improvement-log.csv): automatic overdue reporting (CI-03),
toolbox-talk awareness (CI-06), a monthly threat summary from the managed SOC (CI-08) and an assessment of an
ISO/IEC 42001 extension for the AI route-optimisation pilot planned for 2027 (CI-07).

## 3. Results (clause 9.3.3)

### 9.3.3 Decisions on continual improvement opportunities

1. Approve CI-03, CI-06 and CI-08 as proposed.
2. CI-07: the ISM to present a short ISO/IEC 42001 gap view at the April 2027 review, before the AI pilot starts.
3. Awareness: move from online-only to shift-based toolbox talks for warehouse staff (CA-06).

### 9.3.3 Decisions on any needs for changes to the ISMS

1. **Scope**: no change.
2. **Policy**: add generative AI and the approved-tools list to the acceptable use policy (RTP-22).
3. **Risk treatment**: approve the revised dates for RTP-12 and RTP-23; the risk owner must re-approve any further slip.
4. **Resources**: approve AED 180k for OT firewall integration services (R-07) and a six-month contract engineer to
   remove the WMS key-person dependency (R-17).
5. **Documents**: approve SoA v1.3 and risk register v1.3.

### Actions

| ID | Action | Owner | Due |
|---|---|---|---|
| MR2-01 | Publish SoA v1.3 and risk register v1.3; record retention decisions for R-14, R-15, R-16 and R-25 | Information Security Manager | 2026-11-06 |
| MR2-02 | Contract the OT integration services and the WMS contract engineer | COO | 2026-11-30 |
| MR2-03 | Update REQ-13 wording and send the hosting confirmation to the port operator | Data Protection Officer | 2026-11-15 |
| MR2-04 | Automate overdue-action reporting in the Steering Committee pack (CA-03) | Information Security Manager | 2026-11-30 |
| MR2-05 | Start shift toolbox talks in both warehouses (CA-06) | HR Director | 2026-11-30 |
| MR2-06 | Run the WMS failover test and report the RTO and RPO achieved to the CEO within five working days (RTP-12, CA-04) | Head of IT | 2026-11-27 |
| MR2-07 | Update the acceptable use policy for generative AI and approved tools (RTP-22) | Information Security Manager | 2026-11-30 |
| MR2-08 | Schedule the 2027 risk assessment (February) and the next management review (April) | Information Security Manager | 2026-11-15 |

## 4. Conclusion

Top management concludes that the ISMS is **suitable and adequate**, and **effective with exceptions**: leaver access
and recovery testing. Both have corrective actions, owners and dates. Next review: April 2027.

*Approved: CEO, 2026-10-30.*
