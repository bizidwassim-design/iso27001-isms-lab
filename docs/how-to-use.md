# How to reuse the lab for your own ISMS

The lab is a complete, fictional ISMS. You can use it three ways: **study** it, **train** a team on it, or **fork** it
as the skeleton of your own ISMS. This guide covers all three.

## 1. Study it in one sitting (about 90 minutes)

Follow one thread from start to finish and watch the IDs carry through:

1. Read [organisation-context.md](../01-context/organisation-context.md) — internal issue IN-4 says the
   joiner-mover-leaver process relies on email.
2. Find **R-03** in [risk-register.csv](../02-risk/risk-register.csv): inherent 12, residual 9, target 3, treated with
   A.5.18 and A.6.5.
3. Find **RTP-05** in [risk-treatment-plan.csv](../02-risk/risk-treatment-plan.csv): HR-to-Entra ID automation, due
   2026-12-15.
4. Open the [SoA](../03-soa/statement-of-applicability.csv) at **A.5.18**: *Partially implemented*, linked to R-03 and
   RTP-05.
5. Read **NC-2026-01** in the [audit report](../04-audit/internal-audit-report-2026.md): 3 of 25 leavers disabled late.
6. Read **CA-01** and **CA-02** in the [corrective-action log](../04-audit/corrective-action-log.csv): root cause, interim
   reconciliation, effectiveness check.
7. See **KPI-05** and objective **O-5** in the [management review](../05-review/management-review-minutes-2026-10.md).

Repeat with R-09 and NC-2026-02 (backup and recovery) or R-07 and OBS-2026-01 (OT network).

## 2. Run a training session

| Exercise | Time | What participants do | What good looks like |
|---|---|---|---|
| Score a risk | 20 min | Score R-22 independently with the [scales](../02-risk/risk-methodology.md), then compare | Scores within one point; disagreements traced to the scale wording |
| Challenge the SoA | 20 min | Argue for or against the exclusion of A.8.30 | The justification is tested against the scope and the contracts |
| Audit a control | 40 min | Using only the evidence table, decide whether OBS-2026-04 should have been a nonconformity | A reasoned grading against the definitions in the audit programme |
| Write a root cause | 20 min | Rewrite the root cause of CA-03 with a "5 whys" | A cause that the action actually removes |
| Chair the review | 30 min | Role-play the management review using the metrics pack | Decisions recorded for every clause 9.3.3 output |

Break something on purpose and run `python scripts/validate_isms.py`: delete a control from the SoA, point a
corrective action at a finding that does not exist, or reference a risk ID that is not defined. The validator names
the file and the broken link.

## 3. Fork it as your own ISMS

Work through the folders in order. Keep the IDs, file names and columns: the scripts depend on them.

### Step 1 — Context (week 1–2)

* Replace the organisation description, issues and sites in `01-context/organisation-context.md`.
* Rebuild the requirements register in `01-context/interested-parties.md`. Keep the `| REQ-nn |` first column; the
  validator reads it. Have counsel confirm your legal summaries.
* Rewrite the scope with real boundaries and justified exclusions; keep the policy short and signed by top management.
* Fill the RACI with your roles. One **A** per activity.

### Step 2 — Assets and risks (week 3–6)

* Replace `data/assets.csv` with your critical assets (start with 20 to 40; group similar ones).
* Replace `data/risks.csv`. Write each risk as event, cause and consequence. Score inherent, residual and target with
  the method in `02-risk/risk-methodology.md` (or change the scales there and in `scripts/build_isms.py`).
* Replace `data/treatment-actions.csv`. Every risk that is not retained needs at least one action.

### Step 3 — Statement of Applicability (week 6–7)

* Edit `data/annex-a-soa.csv`: decide applicable Yes/No, status and a one-line justification in your words for each of
  the 93 controls. Link requirements where no risk drives the control. Do not paste the standard's text.
* Run `python scripts/build_isms.py`. Linked risks and treatment actions are filled in for you.

### Step 4 — Operate, measure, audit (months 3–9)

* Define KPIs and KRIs with a source and formula before you report them (see OBS-2026-05).
* Plan the audit programme so that every clause is covered each year and every applicable control in three years.
* Record findings with evidence references and log corrective actions with root causes.

### Step 5 — Review and improve (month 9 onward)

* Use the generated metrics pack as the management review input; minute every clause 9.3 input and output under its
  own heading.
* Keep the continual-improvement log alive between reviews.

### Step 6 — Keep it consistent

```bash
python scripts/build_isms.py      # after every data change
python scripts/validate_isms.py   # before every commit
```

CI runs both, plus the unit tests, on every push and pull request.

## What the lab does not give you

* **Evidence.** The evidence references point at fictional exports. Your auditor will sample real, dated records.
* **The standard.** Buy ISO/IEC 27001:2022 (and ideally ISO/IEC 27002:2022 for control guidance) from ISO or your
  national body.
* **Certification.** Only an accredited certification body can certify an ISMS. This lab makes no such claim.

## Adapting the scripts

| You want to | Change |
|---|---|
| Use a 4×4 or 3×3 scale | `LEVELS`, `BANDS` in `build_isms.py`; `APPETITE_MAX` and the 1–5 checks in `validate_isms.py` |
| Rename the data cut date | `DATA_CUT` in both scripts |
| Add a column to the risk register | `data/risks.csv`, then `build_model` and the Risk Register sheet in `build_isms.py` |
| Add a consistency rule | A new `rep.check(...)` in `validate_isms.py` and a failing-case test in `tests/` |
