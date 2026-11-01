# Roles and responsibilities

| Document | ISMS-CTX-04 · version 1.1 · owner: Information Security Manager · approved by: ISMS Steering Committee, 2026-02-05 · next review: 2027-02 |
|---|---|
| ISO/IEC 27001:2022 reference | Clause 5.1 Leadership and commitment · Clause 5.3 Organisational roles, responsibilities and authorities · Annex A A.5.2, A.5.3, A.5.4 |

> Fictional organisation. People are named by role only.

## Governance bodies

| Body | Members | Meets | Decides |
|---|---|---|---|
| Board | Shareholders' representatives, CEO | Quarterly | Risk appetite, ISMS budget, escalated Critical risks |
| ISMS Steering Committee | CEO (chair), COO, CFO, Head of IT, Information Security Manager, Data Protection Officer, HR Director | Monthly; acts as the management review forum twice a year | Policy approval, risk acceptance above Medium, priorities, resources |
| Security working group | Information Security Manager (lead), Head of IT, Head of Digital, Warehouse Operations Director, Facilities Manager, Procurement Manager | Fortnightly | Day-to-day treatment actions, control operation, incident lessons |

## Key roles

| Role | Main ISMS responsibilities |
|---|---|
| CEO | Top management sponsor; signs the policy; chairs the Steering Committee and the management review |
| Information Security Manager (ISM) | Runs the ISMS: risk method, SoA, metrics, awareness, internal audit programme, supplier security reviews; reports to the CEO, independent of IT operations |
| Head of IT | Owns identity, endpoint, cloud, backup and network controls; risk owner for most technology risks |
| Head of Digital | Owns the customer portal, its pipeline and secure development |
| Data Protection Officer (DPO) | PDPL compliance, records of processing, data subject requests, breach notification decisions |
| Warehouse Operations Director | Owns the WMS as a business service and the OT network |
| HR Director | Screening, contracts, awareness logistics, joiner-mover-leaver triggers, disciplinary process |
| Procurement Manager | Supplier due diligence, contract clauses, supplier register |
| Facilities Manager | Physical security, utilities, CCTV and access control |
| Transport Operations Manager | Driver devices and the telematics supplier |
| Risk owners | Accept or treat their risks, approve treatment plan dates, report progress |
| Internal auditor | Trained auditor from the finance controls team, independent of the areas audited |
| All staff | Follow policy, complete training, report events |

## RACI for the ISMS cycle

R = responsible (does the work) · A = accountable (one per activity, signs off) · C = consulted · I = informed.

| Activity | CEO | Steering Committee | ISM | Head of IT | DPO | Risk owners | Process owners | Internal auditor |
|---|---|---|---|---|---|---|---|---|
| Define context, interested parties and scope | A | C | R | C | C | I | C | I |
| Approve the information security policy | A | R | R | C | C | I | I | I |
| Set information security objectives | A | R | R | C | C | C | C | I |
| Maintain the risk methodology | I | A | R | C | C | C | I | I |
| Run the annual risk assessment | I | A | R | R | C | R | C | I |
| Accept residual risk (Low and Medium) | I | I | C | C | C | A | I | I |
| Accept residual risk (High, time-limited) | A | R | C | C | C | R | I | I |
| Approve the risk treatment plan | I | A | R | C | C | R | C | I |
| Maintain the Statement of Applicability | I | A | R | C | C | C | C | I |
| Operate technical controls | I | I | C | A | I | R | R | I |
| Joiner-mover-leaver process (HR Director as process owner) | I | I | C | R | I | I | A | I |
| Awareness and training (HR Director as process owner) | I | I | R | C | C | I | A | I |
| Manage information security incidents | I | I | A | R | R | C | C | I |
| Notify personal data breaches | I | C | C | C | A | I | I | I |
| Supplier security due diligence (Procurement Manager as process owner) | I | I | C | C | C | I | A | I |
| Monitor and measure (KPI/KRI pack) | I | I | A | R | R | R | R | I |
| Plan and perform internal audits | I | I | A | C | C | C | C | R |
| Manage nonconformities and corrective actions | I | I | A | R | R | R | R | C |
| Conduct the management review | A | R | R | C | C | C | C | C |

Every row has exactly one **A**; `scripts/validate_isms.py` checks this. Process owners are the managers named in the
activity (for example the Facilities Manager for physical security, the Head of Digital for the portal).
