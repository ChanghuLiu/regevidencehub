#!/usr/bin/env python3
"""Build the taxonomy-only MCP Market catalog from the site's AI catalog."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_HOSTS = {
    "taxi": "taxi.regevidencehub.com",
    "cqc": "cqc.regevidencehub.com",
    "premises": "premises.regevidencehub.com",
    "works": "works.regevidencehub.com",
    "waste": "waste.regevidencehub.com",
    "cablecert": "cablecert.regevidencehub.com",
    "factorytalk": "factorytalk.regevidencehub.com",
    "nodeset": "nodeset.regevidencehub.com",
}
LINE_LABELS = {
    "UK Regulatory Readiness": "uk-regulatory-readiness",
    "Industrial Quality Assurance": "industrial-quality-assurance",
}


def encode(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def build() -> dict:
    source = json.loads((ROOT / ".well-known/ai-catalog.json").read_text(encoding="utf-8"))
    entries = source.get("entries", [])
    ids = [row.get("productId") for row in entries]
    if len(entries) != 8 or set(ids) != set(EXPECTED_HOSTS) or len(set(ids)) != 8:
        raise ValueError("AI catalog must contain the eight unique canonical product IDs")
    products = []
    for row in sorted(entries, key=lambda item: item["productId"]):
        pid = row["productId"]
        label = row.get("portfolioLine")
        if row.get("portfolioPlatform") != "RegEvidenceHub" or label not in LINE_LABELS:
            raise ValueError(f"{pid}: missing or unknown portfolio classification")
        commercial = urlsplit(row.get("commercialUrl", ""))
        if commercial.scheme != "https" or commercial.netloc != EXPECTED_HOSTS[pid] or commercial.path != "/mcp":
            raise ValueError(f"{pid}: commercial URL does not match the approved branded host")
        products.append({
            "product_id": pid,
            "name": row["name"],
            "product_line": LINE_LABELS[label],
            "product_line_label": label,
            "product_url": f"https://{EXPECTED_HOSTS[pid]}/",
        })
    if sum(p["product_line"] == "uk-regulatory-readiness" for p in products) != 5:
        raise ValueError("Expected five UK Regulatory Readiness products")
    if sum(p["product_line"] == "industrial-quality-assurance" for p in products) != 3:
        raise ValueError("Expected three Industrial Quality Assurance products")
    return {
        "schema_version": "1.0.0",
        "publisher": "Technologies RegEvidence inc.",
        "platform": "RegEvidenceHub",
        "scope": "portfolio_taxonomy_only",
        "product_count": 8,
        "products": products,
        "limitations": [
            "This catalog describes product names and portfolio taxonomy only.",
            "It makes no assertion about endpoint availability, authentication, pricing, tools, or client compatibility.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if the checked-in output is stale")
    args = parser.parse_args()
    target = ROOT / ".well-known/mcp-market.json"
    output = encode(build())
    if args.check:
        if not target.exists() or target.read_text(encoding="utf-8") != output:
            raise SystemExit("MCP_MARKET_CATALOG=STALE; regenerate without --check")
        print("MCP_MARKET_CATALOG=PASS")
        return 0
    target.write_text(output, encoding="utf-8")
    print(f"MCP_MARKET_CATALOG=GENERATED products=8 path={target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
