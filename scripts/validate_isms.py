#!/usr/bin/env python3
"""Validate that the ISMS lab is complete and internally consistent.

Run after scripts/build_isms.py:

    python scripts/validate_isms.py            # validates the repository this script lives in
    python scripts/validate_isms.py path/to/copy

Exit code 0 when every check passes, 1 otherwise. Every failure is printed with the file it concerns.
"""
from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

from openpyxl import load_workbook

DATA_CUT = date(2026, 10, 26)
ANNEX_A_SIZES = {5: 37, 6: 8, 7: 14, 8: 34}  # ISO/IEC 27001:2022 Annex A: 93 controls in four themes
EXPECTED_CONTROLS = [f"A.{theme}.{n}" for theme, size in ANNEX_A_SIZES.items() for n in range(1, size + 1)]
TREATMENT_OPTIONS = {"Modify", "Retain", "Avoid", "Share"}
ACTION_STATUSES = {"Planned", "In progress", "Done", "Overdue"}
SOA_STATUSES = {"Implemented", "Partially implemented", "Planned", "Not applicable"}
CA_STATUSES = {"Open", "In progress", "Closed"}
APPETITE_MAX = 9  # targets above Medium need an explicit Steering Committee exception, none are recorded
FIRST_DATA_ROW = 5

# Clause 9.3 inputs (9.3.2) and outputs (9.3.3) that the minutes must cover, by heading name.
MANAGEMENT_REVIEW_ITEMS = [
    "Status of actions from previous management reviews",
    "Changes in external and internal issues",
    "Changes in needs and expectations of interested parties",
    "Nonconformities and corrective actions",
    "Monitoring and measurement results",
    "Audit results",
    "Fulfilment of information security objectives",
    "Feedback from interested parties",
    "Results of risk assessment and status of risk treatment plan",
    "Opportunities for continual improvement",
    "Decisions on continual improvement opportunities",
    "Decisions on any needs for changes to the ISMS",
]

REFERENCE_PATTERNS = {
    "asset": re.compile(r"\bAST-\d{2}\b"),
    "risk": re.compile(r"\bR-\d{2}\b"),
    "action": re.compile(r"\bRTP-\d{2}\b"),
    "control": re.compile(r"\bA\.[5-8]\.\d{1,2}\b"),
    "requirement": re.compile(r"\bREQ-\d{2}\b"),
    "finding": re.compile(r"\b(?:NC|OBS)-\d{4}-\d{2}\b"),
    "evidence": re.compile(r"\bE-\d{2}\b"),
    "corrective action": re.compile(r"\bCA-\d{2}\b"),
    "improvement": re.compile(r"\bCI-\d{2}\b"),
    "review action": re.compile(r"\bMR\d-\d{2}\b"),
    "metric": re.compile(r"\bK[PR]I-\d{2}\b"),
}


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.checks = 0

    def check(self, condition: bool, message: str) -> None:
        self.checks += 1
        if not condition:
            self.errors.append(message)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def ids(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def table_ids(path: Path, pattern: str) -> list[str]:
    """IDs defined in the first column of markdown tables in a file."""
    found = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\|\s*(" + pattern + r")\s*\|", line)
        if match:
            found.append(match.group(1))
    return found


def heading_ids(path: Path, pattern: str) -> list[str]:
    found = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^#{2,4}\s+(" + pattern + r")\b", line)
        if match:
            found.append(match.group(1))
    return found


def valid_date(value: str) -> bool:
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def sheet_rows(ws, width: int) -> list[list[object]]:
    rows = []
    for row in ws.iter_rows(min_row=FIRST_DATA_ROW, max_col=width, values_only=True):
        if row[0] is None:
            continue
        rows.append(list(row))
    return rows


def validate(root: Path) -> Report:
    rep = Report()

    # ------------------------------------------------------------------ load
    assets = read_csv(root / "02-risk" / "asset-register.csv")
    risks = read_csv(root / "02-risk" / "risk-register.csv")
    actions = read_csv(root / "02-risk" / "risk-treatment-plan.csv")
    soa = read_csv(root / "03-soa" / "statement-of-applicability.csv")
    cas = read_csv(root / "04-audit" / "corrective-action-log.csv")
    improvements = read_csv(root / "05-review" / "continual-improvement-log.csv")
    audit_report = root / "04-audit" / "internal-audit-report-2026.md"
    minutes = root / "05-review" / "management-review-minutes-2026-10.md"
    parties = root / "01-context" / "interested-parties.md"

    asset_ids = {a["asset_id"] for a in assets}
    risk_by_id = {r["risk_id"]: r for r in risks}
    action_by_id = {a["action_id"]: a for a in actions}
    requirement_ids = set(table_ids(parties, r"REQ-\d{2}"))
    findings = heading_ids(audit_report, r"(?:NC|OBS)-\d{4}-\d{2}")
    evidence_ids = set(table_ids(audit_report, r"E-\d{2}"))
    review_actions = set(table_ids(minutes, r"MR\d-\d{2}"))
    metric_ids = set(table_ids(minutes, r"K[PR]I-\d{2}"))

    # ------------------------------------------------------------------ uniqueness
    for label, values in (
        ("asset", [a["asset_id"] for a in assets]),
        ("risk", [r["risk_id"] for r in risks]),
        ("treatment action", [a["action_id"] for a in actions]),
        ("corrective action", [c["ca_id"] for c in cas]),
        ("improvement", [c["ci_id"] for c in improvements]),
        ("finding", findings),
    ):
        dupes = [v for v, n in Counter(values).items() if n > 1]
        rep.check(not dupes, f"duplicate {label} IDs: {dupes}")

    # ------------------------------------------------------------------ Statement of Applicability
    soa_ids = [c["control_id"] for c in soa]
    counts = Counter(soa_ids)
    missing = [c for c in EXPECTED_CONTROLS if counts[c] == 0]
    duplicated = [c for c, n in counts.items() if n > 1]
    unknown = [c for c in counts if c not in EXPECTED_CONTROLS]
    rep.check(len(soa_ids) == 93, f"SoA: expected 93 rows, found {len(soa_ids)}")
    rep.check(not missing, f"SoA: Annex A controls missing: {missing}")
    rep.check(not duplicated, f"SoA: Annex A controls listed more than once: {duplicated}")
    rep.check(not unknown, f"SoA: IDs that are not ISO/IEC 27001:2022 Annex A controls: {unknown}")
    soa_by_id = {c["control_id"]: c for c in soa}
    applicable = {cid for cid, c in soa_by_id.items() if c["applicable"] == "Yes"}
    for cid, control in soa_by_id.items():
        rep.check(control["applicable"] in {"Yes", "No"}, f"SoA {cid}: applicable must be Yes or No")
        rep.check(control["implementation_status"] in SOA_STATUSES, f"SoA {cid}: unknown status {control['implementation_status']!r}")
        rep.check(bool(control["justification"].strip()), f"SoA {cid}: justification is empty")
        if control["applicable"] == "Yes":
            rep.check(
                bool(ids(control["linked_risks"]) or ids(control["linked_requirements"])),
                f"SoA {cid}: applicable control links to no risk and no requirement",
            )
            rep.check(control["implementation_status"] != "Not applicable", f"SoA {cid}: applicable but status is Not applicable")
        else:
            rep.check(control["implementation_status"] == "Not applicable", f"SoA {cid}: excluded control must have status Not applicable")
            rep.check(not ids(control["linked_risks"]), f"SoA {cid}: excluded control is used to treat {control['linked_risks']}")
        for risk_id in ids(control["linked_risks"]):
            rep.check(risk_id in risk_by_id, f"SoA {cid}: linked risk {risk_id} is not in the risk register")
        for req in ids(control["linked_requirements"]):
            rep.check(req in requirement_ids, f"SoA {cid}: requirement {req} is not defined in 01-context/interested-parties.md")
        for action_id in ids(control["treatment_actions"]):
            rep.check(action_id in action_by_id, f"SoA {cid}: treatment action {action_id} is not in the treatment plan")

    # ------------------------------------------------------------------ assets
    for asset in assets:
        rep.check(bool(ids(asset["linked_risks"])), f"asset {asset['asset_id']}: not covered by any risk")

    # ------------------------------------------------------------------ risk register
    actions_for_risk: dict[str, list[dict[str, str]]] = {rid: [] for rid in risk_by_id}
    for action in actions:
        for risk_id in ids(action["risk_ids"]):
            if risk_id in actions_for_risk:
                actions_for_risk[risk_id].append(action)
    for rid, risk in risk_by_id.items():
        scores = {}
        for stage in ("inherent", "residual", "target"):
            likelihood, impact = int(risk[f"{stage}_likelihood"]), int(risk[f"{stage}_impact"])
            rep.check(1 <= likelihood <= 5 and 1 <= impact <= 5, f"{rid}: {stage} likelihood/impact outside 1-5")
            rep.check(int(risk[f"{stage}_score"]) == likelihood * impact, f"{rid}: {stage} score is not likelihood x impact")
            scores[stage] = likelihood * impact
        rep.check(scores["residual"] <= scores["inherent"], f"{rid}: residual score above inherent score")
        rep.check(scores["target"] <= scores["residual"], f"{rid}: target score above residual score")
        rep.check(scores["target"] <= APPETITE_MAX, f"{rid}: target score {scores['target']} is outside the risk appetite")
        rep.check(risk["treatment_option"] in TREATMENT_OPTIONS, f"{rid}: unknown treatment option {risk['treatment_option']!r}")
        rep.check(bool(risk["owner"].strip()), f"{rid}: no risk owner")
        for asset_id in ids(risk["assets"]):
            rep.check(asset_id in asset_ids, f"{rid}: asset {asset_id} is not in the asset register")
        for req in ids(risk["requirements"]):
            rep.check(req in requirement_ids, f"{rid}: requirement {req} is not defined")
        rep.check(bool(ids(risk["annex_a_controls"])), f"{rid}: no Annex A control linked")
        for cid in ids(risk["annex_a_controls"]):
            rep.check(cid in applicable, f"{rid}: control {cid} is not an applicable control in the SoA")
        own_actions = actions_for_risk[rid]
        open_actions = [a for a in own_actions if a["status"] != "Done"]
        if risk["treatment_option"] == "Retain":
            rep.check(scores["residual"] <= APPETITE_MAX, f"{rid}: retained risk is above appetite")
            rep.check(not open_actions, f"{rid}: retained risk still has open actions")
            rep.check(scores["target"] == scores["residual"], f"{rid}: retained risk must have target equal to residual")
        else:
            rep.check(bool(own_actions), f"{rid}: {risk['treatment_option']} risk has no treatment action")
            if own_actions and not open_actions:
                rep.check(scores["target"] == scores["residual"], f"{rid}: all actions done, so target must equal residual")
        if scores["residual"] > APPETITE_MAX:
            rep.check(bool(open_actions), f"{rid}: residual above appetite with no open treatment action")
        rep.check(
            set(ids(risk["treatment_actions"])) == {a["action_id"] for a in own_actions},
            f"{rid}: treatment_actions column does not match the treatment plan",
        )

    # ------------------------------------------------------------------ treatment plan
    for aid, action in action_by_id.items():
        linked = ids(action["risk_ids"])
        rep.check(bool(linked), f"{aid}: no risk linked")
        for risk_id in linked:
            rep.check(risk_id in risk_by_id, f"{aid}: risk {risk_id} does not exist")
        risk_controls = {c for r in linked if r in risk_by_id for c in ids(risk_by_id[r]["annex_a_controls"])}
        for cid in ids(action["annex_a_controls"]):
            rep.check(cid in risk_controls, f"{aid}: control {cid} is not linked to any of its risks {linked}")
            if action["status"] != "Done" and cid in soa_by_id:
                rep.check(
                    soa_by_id[cid]["implementation_status"] != "Implemented",
                    f"SoA {cid}: marked Implemented while treatment action {aid} is still {action['status']}",
                )
        rep.check(action["status"] in ACTION_STATUSES, f"{aid}: unknown status {action['status']!r}")
        rep.check(bool(action["owner"].strip()), f"{aid}: no owner")
        if valid_date(action["start_date"]) and valid_date(action["due_date"]):
            start, due = date.fromisoformat(action["start_date"]), date.fromisoformat(action["due_date"])
            rep.check(start <= due, f"{aid}: start date after due date")
            if action["status"] in {"Planned", "In progress"}:
                rep.check(due >= DATA_CUT, f"{aid}: due {due} before the data cut but status is {action['status']}, should be Overdue")
            if action["status"] == "Overdue":
                rep.check(due < DATA_CUT, f"{aid}: marked Overdue but due date {due} is not past the data cut")
        else:
            rep.check(False, f"{aid}: start or due date is not an ISO date")

    # ------------------------------------------------------------------ audit findings and corrective actions
    finding_set = set(findings)
    nonconformities = [f for f in findings if f.startswith("NC-")]
    observations = [f for f in findings if f.startswith("OBS-")]
    rep.check(len(nonconformities) >= 2, f"audit report: at least 2 nonconformities required, found {len(nonconformities)}")
    rep.check(len(observations) >= 4, f"audit report: at least 4 observations required, found {len(observations)}")
    for ca in cas:
        cid = ca["ca_id"]
        rep.check(ca["finding_id"] in finding_set, f"{cid}: finding {ca['finding_id']} is not in the internal audit report")
        rep.check(ca["status"] in CA_STATUSES, f"{cid}: unknown status {ca['status']!r}")
        rep.check(valid_date(ca["due_date"]), f"{cid}: due date is not an ISO date")
        for field in ("root_cause", "corrective_action", "owner"):
            rep.check(bool(ca[field].strip()), f"{cid}: {field} is empty")
        if ca["status"] == "Closed":
            rep.check(bool(ca["effectiveness_review"].strip()), f"{cid}: closed without an effectiveness review")
        for risk_id in ids(ca["linked_risks"]):
            rep.check(risk_id in risk_by_id, f"{cid}: risk {risk_id} does not exist")
        for control in ids(ca["linked_controls"]):
            rep.check(control in soa_by_id, f"{cid}: control {control} is not in the SoA")
    covered = {ca["finding_id"] for ca in cas}
    for nc in nonconformities:
        rep.check(nc in covered, f"{nc}: nonconformity has no corrective action")

    # ------------------------------------------------------------------ management review
    headings = [line.lstrip("#").strip().lower() for line in minutes.read_text(encoding="utf-8").splitlines() if line.startswith("#")]
    for item in MANAGEMENT_REVIEW_ITEMS:
        rep.check(any(item.lower() in h for h in headings), f"management review minutes: no heading for '{item}'")
    rep.check(bool(metric_ids), "management review minutes: no KPI/KRI table")

    # ------------------------------------------------------------------ RACI: exactly one accountable role per activity
    raci_rows = 0
    in_raci = False
    for line in (root / "01-context" / "roles-and-responsibilities.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("| Activity |"):
            in_raci = True
            continue
        if in_raci and line.startswith("|---"):
            continue
        if in_raci and line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            raci_rows += 1
            rep.check(all(c in {"R", "A", "C", "I"} for c in cells[1:]), f"RACI '{cells[0]}': cells must be R, A, C or I")
            rep.check(cells[1:].count("A") == 1, f"RACI '{cells[0]}': exactly one A required, found {cells[1:].count('A')}")
        elif in_raci:
            break
    rep.check(raci_rows >= 10, f"RACI: expected at least 10 activities, found {raci_rows}")

    # ------------------------------------------------------------------ cross-references in every document
    defined = {
        "asset": asset_ids,
        "risk": set(risk_by_id),
        "action": set(action_by_id),
        "control": set(EXPECTED_CONTROLS),
        "requirement": requirement_ids,
        "finding": finding_set,
        "evidence": evidence_ids,
        "corrective action": {c["ca_id"] for c in cas},
        "improvement": {c["ci_id"] for c in improvements},
        "review action": review_actions,
        "metric": metric_ids,
    }
    for path in sorted(root.rglob("*")):
        if path.suffix not in {".md", ".csv"} or ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(root).as_posix()
        for kind, pattern in REFERENCE_PATTERNS.items():
            for ref in sorted(set(pattern.findall(text))):
                rep.check(ref in defined[kind], f"{rel}: references {kind} {ref}, which is not defined anywhere")

    # ------------------------------------------------------------------ workbooks agree with the CSV registers
    wb = load_workbook(root / "02-risk" / "ISMS-Risk-Workbook.xlsx")
    rep.check(not getattr(wb, "vba_archive", None), "ISMS-Risk-Workbook.xlsx must not contain macros")
    rep.check(wb.sheetnames == ["Method", "Assets", "Risk Register", "Heat Map", "Treatment Plan"], f"risk workbook sheets: {wb.sheetnames}")
    register = sheet_rows(wb["Risk Register"], 21)
    rep.check([r[0] for r in register] == [r["risk_id"] for r in risks], "risk workbook: Risk Register IDs differ from risk-register.csv")
    for row, risk in zip(register, risks):
        rep.check(
            [row[4], row[5], row[9], row[10], row[14], row[15]]
            == [int(risk[k]) for k in ("inherent_likelihood", "inherent_impact", "residual_likelihood", "residual_impact", "target_likelihood", "target_impact")],
            f"risk workbook: scores for {risk['risk_id']} differ from risk-register.csv",
        )
        rep.check(str(row[6]).startswith("="), f"risk workbook: inherent score for {risk['risk_id']} is not a formula")
    rep.check([r[0] for r in sheet_rows(wb["Assets"], 1)] == [a["asset_id"] for a in assets], "risk workbook: Assets differ from asset-register.csv")
    rep.check(
        [(r[0], r[7]) for r in sheet_rows(wb["Treatment Plan"], 8)] == [(a["action_id"], a["status"]) for a in actions],
        "risk workbook: Treatment Plan differs from risk-treatment-plan.csv",
    )
    wb = load_workbook(root / "03-soa" / "Statement-of-Applicability.xlsx")
    rep.check(not getattr(wb, "vba_archive", None), "Statement-of-Applicability.xlsx must not contain macros")
    soa_sheet = sheet_rows(wb["SoA"], 9)
    rep.check(
        [(r[0], r[3], r[5]) for r in soa_sheet] == [(c["control_id"], c["applicable"], c["implementation_status"]) for c in soa],
        "SoA workbook differs from statement-of-applicability.csv",
    )
    rep.check(bool(wb["SoA"].data_validations.dataValidation), "SoA workbook: status and applicability dropdowns missing")
    return rep


def main(argv: list[str]) -> int:
    root = Path(argv[1]).resolve() if len(argv) > 1 else Path(__file__).resolve().parents[1]
    report = validate(root)
    if report.errors:
        for error in report.errors:
            print(f"FAIL  {error}")
        print(f"\n{len(report.errors)} of {report.checks} checks failed.")
        return 1
    print(f"OK  {report.checks} checks passed: 93 Annex A controls once each, every link resolves, workbooks match the registers.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
