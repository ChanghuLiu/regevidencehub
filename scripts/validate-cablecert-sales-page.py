#!/usr/bin/env python3
"""Validate the CableCert public sales page and downloadable sample outputs."""
from __future__ import annotations

import csv
from io import BytesIO
from html.parser import HTMLParser
from pathlib import Path
from zipfile import ZipFile
from openpyxl import load_workbook
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            self.hrefs.extend(value for key, value in attrs if key == "href" and value)


product = (ROOT / "products/cablecert.html").read_text(encoding="utf-8")
sample = (ROOT / "sample-reports/cablecert-synthetic.html").read_text(encoding="utf-8")

for deliverable in (
    "Project Variance Report",
    "Contractor Remediation List",
    "Downloadable Excel XLSX / PDF",
):
    assert deliverable in product, f"product page missing deliverable: {deliverable}"
for term in ("$19 USD", "one report execution", "24 hours to reopen", "no automatic renewal"):
    assert term in product, f"product page missing current offer term: {term}"
assert "sign in to bind the case to your account" in product
assert "Sample report" in sample and "fictional project scenario" in sample
assert "Every Cable ID, result, timestamp and setup label in this example is synthetic" in sample
assert "No customer project, third-party test results, account or payment was used" in sample
assert "SAMPLE · Review required" in sample
assert "Download Sample Excel XLSX" in sample and "Download Sample PDF" in sample
assert "six IDs represent a fictional owner project inventory" in sample
assert "does not submit an expected test limit" in sample
assert "Wrong test limit" not in sample and "Fluke" not in sample and "Lynch Networks" not in sample
assert "cablecert-synthetic-result.json" not in sample

links = Links()
links.feed(sample)
for href in links.hrefs:
    if href.startswith(("https://", "mailto:", "#")):
        continue
    path = href.split("#", 1)[0].split("?", 1)[0]
    target = ROOT / path.lstrip("/")
    if target.is_dir():
        target = target / "index.html"
    assert target.is_file(), f"broken local sample link: {href}"

xlsx = ROOT / "sample-reports/downloads/cablecert-sample-project-variance.xlsx"
pdf = ROOT / "sample-reports/downloads/cablecert-sample-project-variance.pdf"
assert xlsx.stat().st_size > 1000 and pdf.read_bytes().startswith(b"%PDF-")
with ZipFile(xlsx) as archive:
    assert "xl/workbook.xml" in archive.namelist()
    assert "xl/worksheets/sheet1.xml" in archive.namelist()
    workbook = archive.read("xl/workbook.xml").decode("utf-8")
    assert "Project Summary" in workbook and "Contractor Actions" in workbook

with (ROOT / "sample-reports/downloads/cablecert-sample-owner-expected-ids.csv").open(encoding="utf-8", newline="") as f:
    expected_ids = [row["Cable ID"] for row in csv.DictReader(f)]
with (ROOT / "sample-reports/downloads/cablecert-sample-contractor-results.csv").open(encoding="utf-8", newline="") as f:
    submitted_rows = list(csv.DictReader(f))
submitted_ids = [row["Cable ID"] for row in submitted_rows]
assert expected_ids == [f"CC-SYN-{i:03d}" for i in range(1, 7)]
assert len(submitted_rows) == 6 and len(set(submitted_ids)) == 5
assert all(cable_id.startswith("CC-SYN-") for cable_id in submitted_ids)
assert all(row["Test Limit"] == "Synthetic example only" for row in submitted_rows)
assert sum(row["Test Summary"] == "FAIL" for row in submitted_rows) == 1
assert sum(row["Cable ID"] == "CC-SYN-002" for row in submitted_rows) == 2
assert set(expected_ids) - set(submitted_ids) == {"CC-SYN-006"}
assert "CC-SYN-006" in sample and "CC-SYN-002" in sample
assert "cablecert-sample-contractor-results.csv</code>, rows 3 and 4" in sample

workbook = load_workbook(xlsx, data_only=True, read_only=True)
summary_sheet = workbook["Project Summary"]
assert str(summary_sheet["A1"].value).startswith("SAMPLE")
assert "not test evidence" in str(summary_sheet["A2"].value)
actions_sheet = workbook["Contractor Actions"]
assert str(actions_sheet["A1"].value).startswith("SAMPLE ONLY")
header = [cell.value for cell in actions_sheet[2]]
assert header[:6] == ["No.", "Priority", "Issue", "Cable ID", "Required contractor action", "Evidence source"]
action_rows = [row for row in actions_sheet.iter_rows(min_row=3, values_only=True) if row[0] is not None]
assert len(action_rows) == 3
assert not any(cell.data_type == "f" for sheet in workbook.worksheets for row in sheet.iter_rows() for cell in row)
assert {(row[2], row[3]) for row in action_rows} == {
    ("MISSING", "CC-SYN-006"),
    ("DUPLICATE_OR_RETEST", "CC-SYN-002"),
    ("FAILED_RESULT", "CC-SYN-002"),
}
assert all("cablecert-sample-contractor-results.csv row" in row[5] for row in action_rows if row[3] != "CC-SYN-006")

pdf_reader = PdfReader(str(pdf))
pdf_text = "\n".join(page.extract_text() or "" for page in pdf_reader.pages)
normalized_pdf_text = " ".join(pdf_text.split())
assert len(pdf_reader.pages) >= 2 and "SAMPLE · FICTIONAL PROJECT SCENARIO" in normalized_pdf_text
assert "CC-SYN-006" in pdf_text and "CC-SYN-002" in pdf_text
assert "cablecert-sample-contractor-results.csv row 3" in normalized_pdf_text
assert "Fluke" not in normalized_pdf_text and "WRONG_TEST_LIMIT" not in normalized_pdf_text
print("CABLECERT_SALES_PAGE=PASS")
