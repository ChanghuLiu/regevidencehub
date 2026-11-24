#!/usr/bin/env python3
"""Validate the CableCert public sales page and downloadable sample outputs."""
from __future__ import annotations

import csv
from io import StringIO
from html.parser import HTMLParser
from pathlib import Path
from zipfile import ZipFile

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
assert "Sample report" in sample and "synthetic project scenario" in sample
assert "published Fluke VERSIV demonstration CSV" in sample
assert "No customer account, payment or customer project was used" in sample
assert "SAMPLE · Review required" in sample
assert "Download Sample Excel XLSX" in sample and "Download Sample PDF" in sample
assert "six IDs represent a fictional owner project inventory" in sample
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
    shared_strings = archive.read("xl/sharedStrings.xml").decode("utf-8")
    assert "Project Summary" in workbook and "Contractor Actions" in workbook
    assert "SAMPLE - CableCert Project Evidence Variance" in shared_strings
    assert all(cable_id in shared_strings for cable_id in ("001", "005", "006"))

expected_rows = list(csv.DictReader((ROOT / "sample-reports/downloads/cablecert-sample-owner-expected-ids.csv").open(encoding="utf-8")))
submitted_rows = list(csv.DictReader((ROOT / "sample-reports/downloads/cablecert-sample-contractor-results.csv").open(encoding="utf-8")))
assert len(expected_rows) == 6 and len(submitted_rows) == 5
assert {row["Cable ID"] for row in expected_rows} - {row["Cable ID"] for row in submitted_rows} == {"006"}
assert all(row["Test Limit"] == "TIA Cat 6 Perm. Link" for row in submitted_rows)
assert "Wrong test limit" in sample and sample.count("<th scope=\"row\">Wrong test limit</th>") == 5
print("CABLECERT_SALES_PAGE=PASS")
