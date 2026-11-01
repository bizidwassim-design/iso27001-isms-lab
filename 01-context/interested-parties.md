# Interested parties and their requirements

| Document | ISMS-CTX-02 · version 1.3 · owner: Information Security Manager · approved by: ISMS Steering Committee, 2026-10-29 · next review: 2027-04 |
|---|---|
| ISO/IEC 27001:2022 reference | Clause 4.2 Understanding the needs and expectations of interested parties |

> Fictional organisation. Laws and regulations are named so the lab is realistic; their obligations are summarised in our
> own words and are **not** a legal interpretation. Read the official texts and take legal advice for a real ISMS.

## How to read this register

Each requirement gets a stable `REQ-` ID. Risks in the [risk register](../02-risk/risk-register.csv) and controls in the
[Statement of Applicability](../03-soa/statement-of-applicability.csv) cite these IDs, and `scripts/validate_isms.py`
fails if anything cites an ID that is not defined below. The column *Addressed through ISMS?* records the clause 4.2 c)
decision: which of these needs the ISMS takes on.

## Requirements register

| ID | Interested party | Requirement (our summary) | Type | Addressed through ISMS? | Main controls and risks |
|---|---|---|---|---|---|
| REQ-01 | UAE data protection regulator; consignees; employees | **UAE PDPL** (Federal Decree-Law No. 45 of 2021): have a lawful basis and be transparent, honour data subject rights, secure personal data, notify qualifying breaches, keep records of processing, meet the conditions for transfers outside the UAE | Legal | Yes | A.5.34, A.5.31, A.8.10, A.8.12; R-10, R-11, R-12 |
| REQ-02 | Government-related clients (contractual flow-down) | **UAE Information Assurance Regulation**: align the security programme with its management and technical control families, give evidence of alignment for the priority controls on request | Contractual | Yes | A.5.7, A.8.9, A.8.15, A.8.16; R-19 |
| REQ-03 | E-commerce and retail shippers | Contract security schedule: ISO/IEC 27001-aligned ISMS, incident notification within 24 hours, annual questionnaire, right to audit | Contractual | Yes | A.5.24, A.5.26, A.5.35, A.8.25; R-03, R-05, R-18, R-20 |
| REQ-04 | Payment service provider (Fabrikam Pay) | Keep the card data environment out of scope by using the hosted page, complete the annual PCI DSS self-assessment for that model, protect API keys and webhooks | Contractual | Yes | A.5.20, A.8.24, A.8.26; R-06 |
| REQ-05 | Government-related port operator client | Background screening for staff working on its premises, badge and escort rules, data about its cargo kept in the UAE | Contractual | Yes | A.6.1, A.7.2, A.7.6; R-16, R-21 |
| REQ-06 | Customs and trade authorities | Keep shipment and declaration records complete, unaltered and retrievable for the mandated period | Legal | Yes | A.5.31, A.5.33 |
| REQ-07 | Cyber insurer | MFA for remote and privileged access, EDR on all endpoints and servers, immutable or offline backups, tested incident response plan | Contractual | Yes | A.8.2, A.8.5, A.8.7, A.8.13; R-01, R-02, R-04, R-23 |
| REQ-08 | Board and shareholders | Risk-based ISMS within the approved appetite, quarterly reporting, revenue protected during peak season | Business | Yes | A.5.1, A.5.4, A.5.36; R-09 |
| REQ-09 | Shippers and internal operations | WMS available 99.5% per month, recovery within 8 hours (RTO) with at most 1 hour of data loss (RPO) | Contractual | Yes | A.5.30, A.8.13, A.8.14, A.8.22; R-07, R-09, R-17 |
| REQ-10 | Employees and drivers | Privacy of HR and location data, clear and fair rules on acceptable use and discipline | Legal and ethical | Yes | A.5.10, A.6.4; R-14 |
| REQ-11 | Suppliers, carriers and the managed SOC provider | Clear, least-privilege access rules and security clauses agreed before access is granted | Contractual | Yes | A.5.19, A.5.20, A.5.22, A.6.6; R-13, R-24 |
| REQ-12 | UAE employment, commercial and copyright legislation | Lawful employment contracts and records, licensed software, retention of commercial records | Legal | Yes | A.5.32, A.5.33, A.6.1, A.6.2 |
| REQ-13 | Shippers and the data protection regulator | Customer personal data hosted in UAE cloud regions unless a transfer basis is documented | Contractual and legal | Yes | A.5.14, A.5.23, A.5.34; R-11, R-12 |
| REQ-14 | National cyber authorities and CERT | Report significant cyber incidents affecting clients in critical sectors, cooperate with investigations and keep evidence | Legal and contractual | Yes | A.5.5, A.5.25, A.5.28, A.8.15; R-19, R-20 |

## Parties considered and not retained as separate requirements

| Party | Reason |
|---|---|
| Local community and media | Reputational concerns are covered by REQ-03 and the incident communication plan |
| Competitors | No requirement on the ISMS |
| Free zone authority | Licence conditions carry no specific information security obligation beyond REQ-12 |

## Change log

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-02-05 | First approved register |
| 1.2 | 2026-06-18 | REQ-07 updated for the insurer's renewal conditions |
| 1.3 | 2026-10-29 | REQ-13 wording clarified after the management review (MR2-03) |
