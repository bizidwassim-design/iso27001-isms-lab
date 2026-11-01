# ISMS scope statement

| Document | ISMS-CTX-03 · version 1.1 · owner: Information Security Manager · approved by: CEO for the ISMS Steering Committee, 2026-02-05 · next review: 2027-02 |
|---|---|
| ISO/IEC 27001:2022 reference | Clause 4.3 Determining the scope of the ISMS · Clause 4.4 Information security management system |

> Fictional organisation, written as a worked example of a scope that an auditor can test.

## Scope statement

> The information security management system of Northwind Logistics FZ-LLC covers the **provision of freight
> forwarding, contract warehousing and last-mile delivery services** to business customers in the UAE, including the
> **customer portal, warehouse management, payment integration and supporting corporate IT**, operated from the Dubai
> head office, the Dubai distribution centre, the Abu Dhabi branch office and the Abu Dhabi cross-dock, in accordance
> with the Statement of Applicability version 1.3 dated 2026-10-29.

## What is inside

| Dimension | In scope |
|---|---|
| Services | Freight forwarding, contract warehousing, last-mile delivery, customer service |
| Sites | Dubai head office; Dubai distribution centre (including server room and OT network); Abu Dhabi branch office; Abu Dhabi cross-dock (including comms room) |
| People | All 400 employees, plus contractors and agency staff with system or site access |
| Information | Customer and consignee data, shipment and customs records, payment records, employee records, supplier data |
| Technology | Microsoft 365, Entra ID, Intune; NWL-WMS on Azure; Northwind Track portal and its CI/CD pipeline; payments webhook service; corporate endpoints, driver phones, scanners; networks, SD-WAN and firewalls; warehouse OT network; CCTV and access control; backups |
| Processes | All processes in the [RACI](roles-and-responsibilities.md), including joiner-mover-leaver, change, incident, supplier and continuity management |

## Boundaries and interfaces

The ISMS controls what Northwind owns or configures. Where a supplier operates a service, Northwind controls the
**interface**: the contract, the access it grants, the configuration it owns and the monitoring it performs.

| Interface | Northwind controls | Supplier controls (outside the ISMS, managed through A.5.19–A.5.23) |
|---|---|---|
| Microsoft 365 and Azure | Tenant and subscription configuration, identities, data, logging, backups | Data centres, platform operations |
| Contoso ERP and Fabrikam HR (SaaS) | User access, data entered, integration accounts, contract | Application hosting and operations |
| Fabrikam Pay hosted payment page | API keys, webhook service, refund approval workflow | Card data capture and processing |
| Fleet telematics SaaS | Users, data shared, contract and transfer basis | Platform and device telemetry |
| Contoso Managed Services (SOC) | Analytics rules, access granted, escalation rules, contract | Analyst staffing and its own internal IT |
| Conveyor vendor | OT network boundary, remote-access path, change approval | PLC and HMI software engineering |

## Exclusions

| Excluded | Justification | Risk of exclusion |
|---|---|---|
| Vehicle engine control units and in-cab dashcams | Owned and operated by the vehicle leasing company; Northwind has no access to them | Low; telematics data that Northwind receives is in scope (AST-18) |
| Client-owned systems used on the port operator's premises | Owned and operated by the client under its own security programme; Northwind staff follow the client's rules (REQ-05) | Low; Northwind staff behaviour on site is in scope |
| Annex A control A.8.30 Outsourced development | No development is contracted out (see the [SoA](../03-soa/statement-of-applicability.csv)) | Revisited if any development is outsourced |

No ISMS clause (4 to 10) is excluded.

## Dependencies that the scope relies on

* The building landlord in Dubai provides perimeter security for the head office tower (contract with security clause).
* Internet and SD-WAN connectivity from two carriers (A.8.21).
* Power from the utility, backed by UPS and generator (R-25).
