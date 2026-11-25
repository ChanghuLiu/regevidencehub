#!/usr/bin/env python3
"""Local checks for the RegEvidenceHub company portfolio taxonomy."""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
subprocess.run([sys.executable, str(ROOT / "scripts/build-mcp-market-catalog.py"), "--check"],
               check=True, cwd=ROOT, capture_output=True, text=True)
catalog = json.loads((ROOT / ".well-known/ai-catalog.json").read_text(encoding="utf-8"))
entries = catalog.get("entries", [])
assert len(entries) == 7, f"expected 7 active core entries, found {len(entries)}"
assert len({entry["name"] for entry in entries}) == 7, "catalog names must be unique"
assert all(entry.get("portfolioPlatform") == "RegEvidenceHub" for entry in entries)
counts = Counter(entry.get("portfolioLine") for entry in entries)
assert counts == Counter({"UK Regulatory Readiness": 5, "Industrial Quality Assurance": 2}), counts

machine_catalog = json.loads((ROOT / ".well-known/mcp-market.json").read_text(encoding="utf-8"))
assert machine_catalog["publisher"] == "Technologies RegEvidence inc."
assert machine_catalog["platform"] == "RegEvidenceHub"
assert machine_catalog["scope"] == "portfolio_taxonomy_only"
assert machine_catalog["product_count"] == 7
assert "factorytalk" not in json.dumps(machine_catalog).lower()
generated_lines = {row["name"]: row["product_line_label"] for row in machine_catalog["products"]}
assert generated_lines == {entry["name"]: entry["portfolioLine"] for entry in entries}
assert all(set(row) == {"product_id", "name", "product_line", "product_line_label", "product_url"}
           for row in machine_catalog["products"])
machine_product_keys = {key for row in machine_catalog["products"] for key in row}
assert "endpoint" not in machine_product_keys
assert "payment_boundary" not in machine_product_keys

expected = {entry["name"]: entry["portfolioLine"] for entry in entries}
for path, collection in ((".well-known/mcp.json", "servers"), (".well-known/agent-card.json", "products")):
    value = json.loads((ROOT / path).read_text(encoding="utf-8"))
    assert value.get("portfolioCompany") == "Technologies RegEvidence inc.", path
    rows = value.get(collection, [])
    assert {row["name"]: row.get("portfolioLine") for row in rows} == expected, path
    assert "factorytalk" not in json.dumps(value).lower(), path

tool_index = json.loads((ROOT / ".well-known/mcp-tools.json").read_text(encoding="utf-8"))
assert tool_index["observation_count"] == 12
assert tool_index["tool_definition_count"] == 72
assert all(row["product_id"] != "factorytalk" for row in tool_index["observations"])

for name in ("index.html", "products/index.html", "pricing/index.html", "developers/index.html", "claude.html", "llms.txt"):
    assert "factorytalk" not in (ROOT / name).read_text(encoding="utf-8").lower(), name
assert not (ROOT / "products/factorytalk.html").exists()

for name in ("index.html", "products/index.html", "about/index.html", "llms.txt"):
    page = (ROOT / name).read_text(encoding="utf-8")
    assert "Technologies RegEvidence inc." in page or name == "products/index.html", name
assert "AgentTrustLab" in json.loads((ROOT / ".well-known/agent-card.json").read_text(encoding="utf-8"))["description"]
product_page = (ROOT / "products/index.html").read_text(encoding="utf-8")
assert "UK regulatory preparation" in product_page
assert "Industrial file checks" in product_page
print("PORTFOLIO_TAXONOMY=PASS", dict(counts))
