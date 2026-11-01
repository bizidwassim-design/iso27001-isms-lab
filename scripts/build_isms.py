#!/usr/bin/env python3
"""Build the generated ISMS registers, workbooks and metrics pack from data/.

Sources (edit these):
    data/assets.csv             asset inventory
    data/risks.csv              risk assessment (likelihood and impact scores, treatment option, Annex A links)
    data/treatment-actions.csv  risk treatment plan actions
    data/annex-a-soa.csv        Statement of Applicability decisions for the 93 Annex A controls

Outputs (never edit by hand, rerun this script):
    02-risk/asset-register.csv, 02-risk/risk-register.csv, 02-risk/risk-treatment-plan.csv
    02-risk/ISMS-Risk-Workbook.xlsx
    03-soa/statement-of-applicability.csv, 03-soa/Statement-of-Applicability.xlsx
    05-review/isms-metrics-pack.md

The output is deterministic: running the script twice produces byte-identical files.
"""
from __future__ import annotations

import csv
import io
import re
import zipfile
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.worksheet import Worksheet

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

ORG = "Northwind Logistics FZ-LLC"
DATA_CUT = date(2026, 10, 26)  # the date the registers were frozen for the management review pack
STAMP = (2026, 10, 26, 0, 0, 0)

LEVELS = {
    1: ("Rare", "Negligible"),
    2: ("Unlikely", "Minor"),
    3: ("Possible", "Moderate"),
    4: ("Likely", "Major"),
    5: ("Almost certain", "Severe"),
}
BANDS: list[tuple[int, int, str]] = [(1, 4, "Low"), (5, 9, "Medium"), (10, 14, "High"), (15, 25, "Critical")]
ACCEPTANCE = {
    "Low": "Accepted by the risk owner",
    "Medium": "Accepted by the risk owner; reviewed quarterly by the ISM",
    "High": "Outside appetite: treat, or Steering Committee may retain for at most 12 months",
    "Critical": "Not acceptable: treat immediately and escalate to the Board",
}
TREATMENT_OPTIONS = ["Modify", "Retain", "Avoid", "Share"]
ACTION_STATUSES = ["Planned", "In progress", "Done", "Overdue"]
SOA_STATUSES = ["Implemented", "Partially implemented", "Planned", "Not applicable"]
THEMES = {"5": "Organizational", "6": "People", "7": "Physical", "8": "Technological"}
CIA = {1: "Low", 2: "Medium", 3: "High"}

FILL = {
    "Low": "C6EFCE",
    "Medium": "FFEB9C",
    "High": "F8CBAD",
    "Critical": "FF7C80",
    "Implemented": "C6EFCE",
    "Partially implemented": "FFEB9C",
    "Planned": "F8CBAD",
    "Not applicable": "D9D9D9",
    "Done": "C6EFCE",
    "In progress": "FFEB9C",
    "Overdue": "FF7C80",
}
HEADER_FILL = PatternFill("solid", fgColor="1F3864")
HEADER_FONT = Font(bold=True, color="FFFFFF")
TITLE_FONT = Font(bold=True, size=14, color="1F3864")
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
FIRST_DATA_ROW = 5  # row 1 title, row 2 subtitle, row 4 header


# --------------------------------------------------------------------------- helpers
def split_ids(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def control_key(control_id: str) -> tuple[int, int]:
    _, theme, number = control_id.split(".")
    return int(theme), int(number)


def join_controls(ids: set[str] | list[str]) -> str:
    return ";".join(sorted(set(ids), key=control_key))


def join_ids(ids: set[str] | list[str]) -> str:
    return ";".join(sorted(set(ids)))


def band(score: int) -> str:
    for low, high, name in BANDS:
        if low <= score <= high:
            return name
    raise ValueError(f"score {score} outside 1-25")


def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


# --------------------------------------------------------------------------- model
def build_model() -> dict[str, list[dict[str, object]]]:
    assets = read_csv("assets.csv")
    risks = read_csv("risks.csv")
    actions = read_csv("treatment-actions.csv")
    soa_source = read_csv("annex-a-soa.csv")

    actions_by_risk: dict[str, list[str]] = defaultdict(list)
    for action in actions:
        for risk_id in split_ids(action["risk_ids"]):
            actions_by_risk[risk_id].append(action["action_id"])

    risks_by_asset: dict[str, set[str]] = defaultdict(set)
    risks_by_control: dict[str, set[str]] = defaultdict(set)
    actions_by_control: dict[str, set[str]] = defaultdict(set)

    risk_rows: list[dict[str, object]] = []
    for risk in risks:
        scores = {}
        for stage in ("inherent", "residual", "target"):
            likelihood = int(risk[f"{stage}_likelihood"])
            impact = int(risk[f"{stage}_impact"])
            scores[stage] = (likelihood, impact, likelihood * impact)
        for asset_id in split_ids(risk["assets"]):
            risks_by_asset[asset_id].add(risk["risk_id"])
        for control_id in split_ids(risk["annex_a_controls"]):
            risks_by_control[control_id].add(risk["risk_id"])
        target_band = band(scores["target"][2])
        risk_rows.append(
            {
                "risk_id": risk["risk_id"],
                "risk_statement": risk["risk_statement"],
                "assets": join_ids(split_ids(risk["assets"])),
                "owner": risk["owner"],
                "inherent_likelihood": scores["inherent"][0],
                "inherent_impact": scores["inherent"][1],
                "inherent_score": scores["inherent"][2],
                "inherent_rating": band(scores["inherent"][2]),
                "existing_controls": risk["existing_controls"],
                "residual_likelihood": scores["residual"][0],
                "residual_impact": scores["residual"][1],
                "residual_score": scores["residual"][2],
                "residual_rating": band(scores["residual"][2]),
                "treatment_option": risk["treatment_option"],
                "target_likelihood": scores["target"][0],
                "target_impact": scores["target"][1],
                "target_score": scores["target"][2],
                "target_rating": target_band,
                "acceptance_decision": ACCEPTANCE[target_band],
                "annex_a_controls": join_controls(split_ids(risk["annex_a_controls"])),
                "requirements": join_ids(split_ids(risk["requirements"])),
                "treatment_actions": join_ids(actions_by_risk.get(risk["risk_id"], [])),
            }
        )

    action_rows: list[dict[str, object]] = []
    for action in actions:
        due = date.fromisoformat(action["due_date"])
        late = (DATA_CUT - due).days if action["status"] != "Done" and due < DATA_CUT else 0
        for control_id in split_ids(action["annex_a_controls"]):
            actions_by_control[control_id].add(action["action_id"])
        action_rows.append(
            {
                "action_id": action["action_id"],
                "risk_ids": join_ids(split_ids(action["risk_ids"])),
                "action": action["action"],
                "annex_a_controls": join_controls(split_ids(action["annex_a_controls"])),
                "owner": action["owner"],
                "start_date": action["start_date"],
                "due_date": action["due_date"],
                "status": action["status"],
                "days_late_at_data_cut": late,
                "progress_note": action["progress_note"],
            }
        )

    asset_rows: list[dict[str, object]] = []
    for asset in assets:
        c, i, a = (int(asset[k]) for k in ("confidentiality", "integrity", "availability"))
        asset_rows.append(
            {
                "asset_id": asset["asset_id"],
                "name": asset["name"],
                "type": asset["type"],
                "location": asset["location"],
                "owner": asset["owner"],
                "description": asset["description"],
                "confidentiality": c,
                "integrity": i,
                "availability": a,
                "criticality": CIA[max(c, i, a)],
                "linked_risks": join_ids(risks_by_asset.get(asset["asset_id"], set())),
            }
        )

    soa_rows: list[dict[str, object]] = []
    for control in soa_source:
        cid = control["control_id"]
        soa_rows.append(
            {
                "control_id": cid,
                "theme": THEMES[cid.split(".")[1]],
                "title": control["title"],
                "applicable": control["applicable"],
                "justification": control["justification"],
                "implementation_status": control["implementation_status"],
                "linked_risks": join_ids(risks_by_control.get(cid, set())),
                "linked_requirements": join_ids(split_ids(control["requirements"])),
                "treatment_actions": join_ids(actions_by_control.get(cid, set())),
            }
        )
    soa_rows.sort(key=lambda row: control_key(str(row["control_id"])))

    return {"assets": asset_rows, "risks": risk_rows, "actions": action_rows, "soa": soa_rows}


# --------------------------------------------------------------------------- workbooks
def title_block(ws: Worksheet, title: str, subtitle: str) -> None:
    ws["A1"] = title
    ws["A1"].font = TITLE_FONT
    ws["A2"] = subtitle
    ws["A2"].font = Font(italic=True, color="595959")


def write_table(ws: Worksheet, headers: list[str], rows: list[list[object]], widths: list[int]) -> None:
    for col, header in enumerate(headers, start=1):
        cell = ws.cell(row=FIRST_DATA_ROW - 1, column=col, value=header)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = CENTER
        cell.border = BORDER
    for r, values in enumerate(rows, start=FIRST_DATA_ROW):
        for col, value in enumerate(values, start=1):
            cell = ws.cell(row=r, column=col, value=value)
            cell.alignment = WRAP
            cell.border = BORDER
    for col, width in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(col)].width = width
    last_row = FIRST_DATA_ROW + max(len(rows), 1) - 1
    ws.auto_filter.ref = f"A{FIRST_DATA_ROW - 1}:{get_column_letter(len(headers))}{last_row}"
    ws.freeze_panes = ws.cell(row=FIRST_DATA_ROW, column=2)


def colour_by_text(ws: Worksheet, cell_range: str, values: list[str]) -> None:
    for value in values:
        ws.conditional_formatting.add(
            cell_range,
            CellIsRule(operator="equal", formula=[f'"{value}"'], fill=PatternFill("solid", fgColor=FILL[value])),
        )


def add_list_validation(ws: Worksheet, cell_range: str, options: list[str]) -> None:
    dv = DataValidation(type="list", formula1='"' + ",".join(options) + '"', allow_blank=False)
    dv.error = "Choose a value from the list"
    ws.add_data_validation(dv)
    dv.add(cell_range)


def add_score_validation(ws: Worksheet, cell_range: str) -> None:
    dv = DataValidation(type="whole", operator="between", formula1="1", formula2="5")
    dv.error = "Likelihood and impact are scored 1 to 5"
    ws.add_data_validation(dv)
    dv.add(cell_range)


def rating_formula(score_cell: str) -> str:
    return f'=IF({score_cell}>=15,"Critical",IF({score_cell}>=10,"High",IF({score_cell}>=5,"Medium","Low")))'


def save_deterministic(wb: Workbook, path: Path) -> None:
    """Save the workbook with fixed metadata and fixed zip entry timestamps."""
    stamp = datetime(*STAMP)
    wb.properties.creator = ORG
    wb.properties.lastModifiedBy = ORG
    wb.properties.created = stamp
    wb.properties.modified = stamp
    buffer = io.BytesIO()
    wb.save(buffer)  # openpyxl stamps dcterms:modified with the wall clock, fixed below
    iso = stamp.strftime("%Y-%m-%dT%H:%M:%SZ").encode()
    out = io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(buffer.getvalue())) as src, zipfile.ZipFile(out, "w") as dst:
        for info in src.infolist():
            payload = src.read(info.filename)
            if info.filename == "docProps/core.xml":
                payload = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", rb"\g<1>" + iso + rb"\g<2>", payload)
            entry = zipfile.ZipInfo(info.filename, date_time=STAMP)
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o600 << 16
            dst.writestr(entry, payload, compresslevel=6)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(out.getvalue())


def build_risk_workbook(model: dict[str, list[dict[str, object]]], path: Path) -> None:
    wb = Workbook()

    # Method
    ws = wb.active
    ws.title = "Method"
    title_block(ws, f"{ORG} — ISMS risk workbook", f"Fictional training data. Data cut {DATA_CUT.isoformat()}. Generated by scripts/build_isms.py")
    ws["A4"], ws["B4"], ws["C4"] = "Score", "Likelihood", "Impact"
    for cell in (ws["A4"], ws["B4"], ws["C4"]):
        cell.fill, cell.font, cell.border = HEADER_FILL, HEADER_FONT, BORDER
    for level, (likelihood, impact) in LEVELS.items():
        for col, value in enumerate((level, likelihood, impact), start=1):
            ws.cell(row=4 + level, column=col, value=value).border = BORDER
    ws["A11"], ws["B11"], ws["C11"] = "Band", "Score range", "Acceptance rule"
    for cell in (ws["A11"], ws["B11"], ws["C11"]):
        cell.fill, cell.font, cell.border = HEADER_FILL, HEADER_FONT, BORDER
    for offset, (low, high, name) in enumerate(BANDS, start=12):
        ws.cell(row=offset, column=1, value=name).fill = PatternFill("solid", fgColor=FILL[name])
        ws.cell(row=offset, column=2, value=f"{low}–{high}")
        ws.cell(row=offset, column=3, value=ACCEPTANCE[name])
        for col in (1, 2, 3):
            ws.cell(row=offset, column=col).border = BORDER
    ws["A17"] = "Treatment options: Modify (reduce with controls) · Retain (accept) · Avoid (stop the activity) · Share (contract or insure)"
    ws["A18"] = "Scores and ratings in the Risk Register sheet are formulas: change a likelihood or impact and they recalculate."
    ws.column_dimensions["A"].width = 14
    ws.column_dimensions["B"].width = 18
    ws.column_dimensions["C"].width = 80

    # Assets
    ws = wb.create_sheet("Assets")
    title_block(ws, "Asset register", "C/I/A rated 1 (Low) to 3 (High); criticality is the highest of the three")
    headers = ["Asset ID", "Name", "Type", "Location", "Owner", "Description", "C", "I", "A", "Criticality", "Linked risks"]
    rows = [[a[k] for k in ("asset_id", "name", "type", "location", "owner", "description", "confidentiality", "integrity", "availability", "criticality", "linked_risks")] for a in model["assets"]]
    write_table(ws, headers, rows, [10, 34, 16, 30, 26, 50, 5, 5, 5, 12, 24])

    # Risk register
    ws = wb.create_sheet("Risk Register")
    title_block(ws, "Risk register", "Inherent = no controls · Residual = controls operating at the data cut · Target = after open treatment actions")
    headers = [
        "Risk ID", "Risk statement", "Assets", "Owner",
        "Inh. L", "Inh. I", "Inh. score", "Inh. rating",
        "Existing controls",
        "Res. L", "Res. I", "Res. score", "Res. rating",
        "Treatment", "Tgt. L", "Tgt. I", "Tgt. score", "Tgt. rating",
        "Annex A controls", "Requirements", "Treatment actions",
    ]
    rows = []
    for offset, risk in enumerate(model["risks"]):
        r = FIRST_DATA_ROW + offset
        rows.append([
            risk["risk_id"], risk["risk_statement"], risk["assets"], risk["owner"],
            risk["inherent_likelihood"], risk["inherent_impact"], f"=E{r}*F{r}", rating_formula(f"G{r}"),
            risk["existing_controls"],
            risk["residual_likelihood"], risk["residual_impact"], f"=J{r}*K{r}", rating_formula(f"L{r}"),
            risk["treatment_option"], risk["target_likelihood"], risk["target_impact"], f"=O{r}*P{r}", rating_formula(f"Q{r}"),
            risk["annex_a_controls"], risk["requirements"], risk["treatment_actions"],
        ])
    write_table(ws, headers, rows, [8, 60, 18, 24, 6, 6, 7, 10, 50, 6, 6, 7, 10, 10, 6, 6, 7, 10, 30, 16, 16])
    last = FIRST_DATA_ROW + len(rows) - 1
    for col in ("E", "F", "J", "K", "O", "P"):
        add_score_validation(ws, f"{col}{FIRST_DATA_ROW}:{col}{last}")
    add_list_validation(ws, f"N{FIRST_DATA_ROW}:N{last}", TREATMENT_OPTIONS)
    for col in ("H", "M", "R"):
        colour_by_text(ws, f"{col}{FIRST_DATA_ROW}:{col}{last}", [name for _, _, name in BANDS])

    # Heat map
    ws = wb.create_sheet("Heat Map")
    title_block(ws, "Heat maps (live counts from the Risk Register sheet)", "Rows: likelihood 5 to 1 · Columns: impact 1 to 5")
    blocks = [("Inherent", "E", "F", 1), ("Residual", "J", "K", 9), ("Target", "O", "P", 17)]
    for label, l_col, i_col, start_col in blocks:
        ws.cell(row=4, column=start_col, value=f"{label} risk").font = Font(bold=True)
        for impact in range(1, 6):
            cell = ws.cell(row=5, column=start_col + impact, value=f"I={impact}")
            cell.font, cell.alignment = Font(bold=True), CENTER
        for row_offset, likelihood in enumerate(range(5, 0, -1)):
            row = 6 + row_offset
            ws.cell(row=row, column=start_col, value=f"L={likelihood}").font = Font(bold=True)
            for impact in range(1, 6):
                cell = ws.cell(
                    row=row,
                    column=start_col + impact,
                    value=(
                        f"=COUNTIFS('Risk Register'!${l_col}${FIRST_DATA_ROW}:${l_col}${last},{likelihood},"
                        f"'Risk Register'!${i_col}${FIRST_DATA_ROW}:${i_col}${last},{impact})"
                    ),
                )
                cell.fill = PatternFill("solid", fgColor=FILL[band(likelihood * impact)])
                cell.alignment, cell.border = CENTER, BORDER
        for col in range(start_col, start_col + 6):
            ws.column_dimensions[get_column_letter(col)].width = 7
        ws.column_dimensions[get_column_letter(start_col + 6)].width = 3

    # Treatment plan
    ws = wb.create_sheet("Treatment Plan")
    title_block(ws, "Risk treatment plan", f"Status as at the data cut {DATA_CUT.isoformat()}; days late is counted to that date")
    headers = ["Action ID", "Risks", "Action", "Annex A controls", "Owner", "Start", "Due", "Status", "Days late", "Progress note"]
    rows = [[a[k] for k in ("action_id", "risk_ids", "action", "annex_a_controls", "owner")]
            + [date.fromisoformat(str(a["start_date"])), date.fromisoformat(str(a["due_date"]))]
            + [a["status"], a["days_late_at_data_cut"], a["progress_note"]] for a in model["actions"]]
    write_table(ws, headers, rows, [9, 12, 60, 22, 26, 11, 11, 12, 9, 50])
    last = FIRST_DATA_ROW + len(rows) - 1
    for r in range(FIRST_DATA_ROW, last + 1):
        ws.cell(row=r, column=6).number_format = "yyyy-mm-dd"
        ws.cell(row=r, column=7).number_format = "yyyy-mm-dd"
    add_list_validation(ws, f"H{FIRST_DATA_ROW}:H{last}", ACTION_STATUSES)
    colour_by_text(ws, f"H{FIRST_DATA_ROW}:H{last}", ["Done", "In progress", "Planned", "Overdue"])

    save_deterministic(wb, path)


def build_soa_workbook(model: dict[str, list[dict[str, object]]], path: Path) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Summary"
    title_block(ws, f"{ORG} — Statement of Applicability (ISO/IEC 27001:2022 Annex A)", "Control IDs and short titles only; justifications are the organisation's own. Fictional training data")
    last = FIRST_DATA_ROW + len(model["soa"]) - 1
    themes = list(THEMES.values())
    ws.cell(row=4, column=1, value="Status")
    for col, theme in enumerate(themes + ["Total"], start=2):
        ws.cell(row=4, column=col, value=theme)
    for col in range(1, len(themes) + 3):
        cell = ws.cell(row=4, column=col)
        cell.fill, cell.font, cell.border, cell.alignment = HEADER_FILL, HEADER_FONT, BORDER, CENTER
    for row, status in enumerate(SOA_STATUSES + ["All controls"], start=5):
        ws.cell(row=row, column=1, value=status).border = BORDER
        for col, theme in enumerate(themes, start=2):
            if status == "All controls":
                formula = f"=COUNTIF(SoA!$B${FIRST_DATA_ROW}:$B${last},\"{theme}\")"
            else:
                formula = (
                    f"=COUNTIFS(SoA!$B${FIRST_DATA_ROW}:$B${last},\"{theme}\","
                    f"SoA!$F${FIRST_DATA_ROW}:$F${last},\"{status}\")"
                )
            ws.cell(row=row, column=col, value=formula).border = BORDER
        total = ws.cell(row=row, column=len(themes) + 2, value=f"=SUM(B{row}:{get_column_letter(len(themes) + 1)}{row})")
        total.border, total.font = BORDER, Font(bold=True)
        if status in FILL:
            ws.cell(row=row, column=1).fill = PatternFill("solid", fgColor=FILL[status])
    ws["A11"] = "Implemented share of applicable controls"
    ws["B11"] = f"=F5/(F9-F8)"
    ws["B11"].number_format = "0%"
    ws.column_dimensions["A"].width = 40
    for col in range(2, len(themes) + 3):
        ws.column_dimensions[get_column_letter(col)].width = 15

    ws = wb.create_sheet("SoA")
    title_block(ws, "Statement of Applicability", "Linked risks and treatment actions are derived from the risk register and treatment plan by the build script")
    headers = ["Control ID", "Theme", "Title", "Applicable", "Justification", "Implementation status", "Linked risks", "Linked requirements", "Treatment actions"]
    rows = [[c[k] for k in ("control_id", "theme", "title", "applicable", "justification", "implementation_status", "linked_risks", "linked_requirements", "treatment_actions")] for c in model["soa"]]
    write_table(ws, headers, rows, [10, 15, 44, 11, 70, 20, 22, 22, 20])
    add_list_validation(ws, f"D{FIRST_DATA_ROW}:D{last}", ["Yes", "No"])
    add_list_validation(ws, f"F{FIRST_DATA_ROW}:F{last}", SOA_STATUSES)
    colour_by_text(ws, f"F{FIRST_DATA_ROW}:F{last}", SOA_STATUSES)
    ws.conditional_formatting.add(
        f"D{FIRST_DATA_ROW}:D{last}",
        FormulaRule(formula=[f'D{FIRST_DATA_ROW}="No"'], fill=PatternFill("solid", fgColor=FILL["Not applicable"])),
    )
    save_deterministic(wb, path)


# --------------------------------------------------------------------------- metrics pack
def md_table(headers: list[str], rows: list[list[object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    lines += ["| " + " | ".join(str(v) for v in row) + " |" for row in rows]
    return "\n".join(lines)


def heat_map(risks: list[dict[str, object]], stage: str) -> str:
    cells: dict[tuple[int, int], list[str]] = defaultdict(list)
    for risk in risks:
        cells[(int(risk[f"{stage}_likelihood"]), int(risk[f"{stage}_impact"]))].append(str(risk["risk_id"]))
    rows = []
    for likelihood in range(5, 0, -1):
        row: list[object] = [f"**L{likelihood}** {LEVELS[likelihood][0]}"]
        for impact in range(1, 6):
            row.append(", ".join(cells.get((likelihood, impact), [])) or "·")
        rows.append(row)
    return md_table(["Likelihood \\ Impact"] + [f"I{i} {LEVELS[i][1]}" for i in range(1, 6)], rows)


def build_metrics_pack(model: dict[str, list[dict[str, object]]], path: Path) -> None:
    risks, actions, soa = model["risks"], model["actions"], model["soa"]
    band_names = [name for _, _, name in BANDS]
    counts = {stage: Counter(str(r[f"{stage}_rating"]) for r in risks) for stage in ("inherent", "residual", "target")}
    options = Counter(str(r["treatment_option"]) for r in risks)
    status = Counter(str(a["status"]) for a in actions)
    due = [a for a in actions if date.fromisoformat(str(a["due_date"])) <= DATA_CUT]
    due_done = [a for a in due if a["status"] == "Done"]
    applicable = [c for c in soa if c["applicable"] == "Yes"]
    soa_status = Counter(str(c["implementation_status"]) for c in soa)
    top = sorted(risks, key=lambda r: (-int(r["residual_score"]), str(r["risk_id"])))[:8]
    overdue = [a for a in actions if a["status"] == "Overdue"]

    parts = [
        "# ISMS metrics pack",
        "",
        f"> Generated by `scripts/build_isms.py` from `data/` — do not edit by hand. Data cut: **{DATA_CUT.isoformat()}**. "
        f"Organisation: {ORG} (fictional). This pack is input to the management review "
        "([minutes](management-review-minutes-2026-10.md)).",
        "",
        "## Risk profile",
        "",
        md_table(
            ["Rating", "Inherent", "Residual", "Target"],
            [[name] + [counts[s].get(name, 0) for s in ("inherent", "residual", "target")] for name in band_names]
            + [["**Total**", len(risks), len(risks), len(risks)]],
        ),
        "",
        "Treatment options: " + " · ".join(f"{opt} {options.get(opt, 0)}" for opt in TREATMENT_OPTIONS) + ".",
        "",
        "### Residual heat map",
        "",
        heat_map(risks, "residual"),
        "",
        "### Target heat map (after open treatment actions)",
        "",
        heat_map(risks, "target"),
        "",
        "### Highest residual risks",
        "",
        md_table(
            ["Risk", "Owner", "Residual", "Target", "Treatment", "Actions"],
            [[r["risk_id"], r["owner"], f"{r['residual_score']} {r['residual_rating']}", f"{r['target_score']} {r['target_rating']}",
              r["treatment_option"], r["treatment_actions"] or "—"] for r in top],
        ),
        "",
        "## Risk treatment plan",
        "",
        md_table(["Status", "Actions"], [[s, status.get(s, 0)] for s in ACTION_STATUSES] + [["**Total**", len(actions)]]),
        "",
        f"Actions due on or before the data cut: **{len(due)}**; completed: **{len(due_done)}**; "
        f"on-time rate **{round(100 * len(due_done) / len(due)) if due else 100}%**.",
        "",
        md_table(
            ["Overdue action", "Risks", "Owner", "Due", "Days late"],
            [[a["action_id"], a["risk_ids"], a["owner"], a["due_date"], a["days_late_at_data_cut"]] for a in overdue],
        ) if overdue else "No overdue actions.",
        "",
        "## Statement of Applicability",
        "",
        md_table(["Status", "Controls"], [[s, soa_status.get(s, 0)] for s in SOA_STATUSES] + [["**Total**", len(soa)]]),
        "",
        f"Applicable controls: **{len(applicable)}** of {len(soa)}. Implemented share of applicable controls: "
        f"**{round(100 * soa_status.get('Implemented', 0) / len(applicable))}%**.",
        "",
    ]
    write_text(path, "\n".join(parts))


# --------------------------------------------------------------------------- main
def main() -> None:
    model = build_model()
    write_csv(ROOT / "02-risk" / "asset-register.csv", list(model["assets"][0].keys()), model["assets"])
    write_csv(ROOT / "02-risk" / "risk-register.csv", list(model["risks"][0].keys()), model["risks"])
    write_csv(ROOT / "02-risk" / "risk-treatment-plan.csv", list(model["actions"][0].keys()), model["actions"])
    write_csv(ROOT / "03-soa" / "statement-of-applicability.csv", list(model["soa"][0].keys()), model["soa"])
    build_risk_workbook(model, ROOT / "02-risk" / "ISMS-Risk-Workbook.xlsx")
    build_soa_workbook(model, ROOT / "03-soa" / "Statement-of-Applicability.xlsx")
    build_metrics_pack(model, ROOT / "05-review" / "isms-metrics-pack.md")
    print(
        f"Built {len(model['assets'])} assets, {len(model['risks'])} risks, "
        f"{len(model['actions'])} treatment actions, {len(model['soa'])} SoA controls."
    )


if __name__ == "__main__":
    main()
