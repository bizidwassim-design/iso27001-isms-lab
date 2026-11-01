#!/usr/bin/env python3
"""Prove the validator passes on the lab and fails when the ISMS is made inconsistent.

Run with:  python -m unittest discover -s tests -v
"""
from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_isms  # noqa: E402


class ValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.copy = Path(self._tmp.name) / "lab"
        shutil.copytree(ROOT, self.copy, ignore=shutil.ignore_patterns(".git", "__pycache__"))

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def replace(self, relative: str, old: str, new: str) -> None:
        path = self.copy / relative
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text, f"test fixture text not found in {relative}")
        path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")

    def errors(self) -> list[str]:
        return validate_isms.validate(self.copy).errors

    def assertFlagged(self, fragment: str) -> None:
        errors = self.errors()
        self.assertTrue(any(fragment in e for e in errors), f"expected an error containing {fragment!r}, got {errors[:5]}")

    def test_lab_as_shipped_is_valid(self) -> None:
        self.assertEqual(self.errors(), [])

    def test_duplicate_and_missing_annex_a_control(self) -> None:
        self.replace("03-soa/statement-of-applicability.csv", "A.5.2,Organizational", "A.5.1,Organizational")
        self.assertFlagged("controls missing: ['A.5.2']")
        self.assertFlagged("listed more than once: ['A.5.1']")

    def test_applicable_control_without_risk_or_requirement(self) -> None:
        self.replace("03-soa/statement-of-applicability.csv", ",,REQ-08,", ",,,")
        self.assertFlagged("links to no risk and no requirement")

    def test_corrective_action_for_unknown_finding(self) -> None:
        self.replace("04-audit/corrective-action-log.csv", "CA-09,OBS-2026-05", "CA-09,OBS-2026-09")
        self.assertFlagged("CA-09: finding OBS-2026-09 is not in the internal audit report")

    def test_treatment_action_for_unknown_risk(self) -> None:
        self.replace("02-risk/risk-treatment-plan.csv", "RTP-17,R-17", "RTP-17,R-99")
        self.assertFlagged("RTP-17: risk R-99 does not exist")

    def test_management_review_missing_clause_9_3_input(self) -> None:
        self.replace("05-review/management-review-minutes-2026-10.md", "#### d) 3. Audit results", "#### d) 3. Other")
        self.assertFlagged("no heading for 'Audit results'")

    def test_dangling_reference_in_a_document(self) -> None:
        self.replace("01-context/organisation-context.md", "Drives R-01, R-02 and R-23", "Drives R-01, R-02 and R-26")
        self.assertFlagged("references risk R-26")

    def test_control_implemented_while_treatment_open(self) -> None:
        self.replace(
            "03-soa/statement-of-applicability.csv",
            "Partially implemented,R-01;R-21,REQ-07",
            "Implemented,R-01;R-21,REQ-07",
        )
        self.assertFlagged("marked Implemented while treatment action")


if __name__ == "__main__":
    unittest.main()
