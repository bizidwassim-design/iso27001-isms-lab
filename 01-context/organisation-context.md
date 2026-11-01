# Organisation context

| Document | ISMS-CTX-01 · version 1.2 · owner: Information Security Manager · approved by: ISMS Steering Committee, 2026-02-05 · next review: 2027-02 |
|---|---|
| ISO/IEC 27001:2022 reference | Clause 4.1 Understanding the organisation and its context |

> Fictional organisation. Northwind Logistics FZ-LLC does not exist; every name, number and system below is invented for training.

## 1. Who we are

Northwind Logistics FZ-LLC is a third-party logistics company with **about 400 staff**. It runs freight forwarding,
contract warehousing and last-mile delivery for e-commerce and retail shippers in the UAE.

| Site | What happens there | People |
|---|---|---|
| Dubai head office | Management, finance, IT, customer service, digital team | 120 |
| Dubai distribution centre | Contract warehousing, automated conveyor and sortation line, server room | 170 |
| Abu Dhabi branch office | Sales and customer service for Abu Dhabi clients | 25 |
| Abu Dhabi cross-dock | Inbound consolidation and outbound dispatch, comms room | 85 |

The fleet of 140 delivery vehicles is operated from both warehouses. About 90 drivers use a delivery app on company phones.

## 2. How the business depends on information

* **Microsoft 365 and Entra ID** for email, collaboration, identities and device management (Intune).
* **NWL-WMS**, the warehouse management system, on Azure virtual machines in the UAE North region. During the
  November to January peak, dispatch volumes triple and the WMS becomes the single point of failure for revenue.
* **Northwind Track**, the customer portal built in-house: shipment booking, tracking and proof of delivery. It holds
  consignee names, addresses, phone numbers, delivery photos and signatures.
* **Payments integration** with the payment service provider Fabrikam Pay through a hosted payment page; Northwind
  never stores card numbers.
* **Contoso ERP** (SaaS, hosted in the EU) for finance and procurement; **Fabrikam HR** (SaaS) for HR records.
* **Warehouse OT network** in Dubai: conveyor PLCs, sortation controllers and two Windows HMI workstations supported by
  the conveyor vendor.
* **Fleet telematics** from a SaaS supplier hosted outside the UAE.
* **Managed SOC** from Contoso Managed Services, using Microsoft Sentinel in Northwind's own subscription.

## 3. External issues

| # | Issue | Why it matters to the ISMS |
|---|---|---|
| EX-1 | The UAE Personal Data Protection Law (PDPL) applies to consignee and employee data | Lawful processing, rights handling, breach notification and cross-border transfer conditions shape controls (REQ-01, REQ-13) |
| EX-2 | Government-related clients flow down the UAE Information Assurance Regulation in their contracts | Northwind must show alignment with its priority controls to keep those contracts (REQ-02) |
| EX-3 | Large shippers send detailed security questionnaires and ask for ISO/IEC 27001 alignment | Losing a top-five client would cost about a fifth of revenue (REQ-03) |
| EX-4 | Business email compromise and ransomware are the most common attacks on regional logistics firms | Drives R-01, R-02 and R-23 |
| EX-5 | Cyber insurance renewal now requires MFA, EDR and immutable backups | Conditions are listed as REQ-07 |
| EX-6 | E-commerce growth and peak-season volume | Capacity and availability risks to the WMS and portal (R-09) |
| EX-7 | Wider use of SaaS and generative AI tools by staff | Data leaves approved services (R-22) |

## 4. Internal issues

| # | Issue | Why it matters to the ISMS |
|---|---|---|
| IN-1 | IT team of nine; WMS integration knowledge concentrated in one engineer | Key-person risk (R-17) |
| IN-2 | Warehouse workforce is multilingual and works in three shifts | Awareness must be delivered on the floor, not only online (R-21) |
| IN-3 | OT network was installed by the conveyor vendor and is routable from the corporate LAN | Segregation gap (R-07, R-08) |
| IN-4 | Joiner-mover-leaver process relies on email between HR and IT | Late account removal (R-03) |
| IN-5 | The portal team ships every two weeks and is adding security testing to the pipeline | Secure development risks (R-05, R-18) |
| IN-6 | Leadership has approved an ISMS budget and wants an externally credible ISMS within 18 months | Resources and priorities for the risk treatment plan |

## 5. How this document is used

Issues are reviewed at every management review (clause 9.3.2 b). A change in an issue triggers a check of the
[interested parties](interested-parties.md), the [scope](isms-scope.md) and the [risk register](../02-risk/risk-register.csv).
