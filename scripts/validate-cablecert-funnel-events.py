#!/usr/bin/env python3
"""Check the consent-gated CableCert entry event wiring."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
script = (ROOT / "assets/analytics-consent.js").read_text(encoding="utf-8")
pages = [
    (ROOT / "products/cablecert.html").read_text(encoding="utf-8"),
    (ROOT / "sample-reports/cablecert-synthetic.html").read_text(encoding="utf-8"),
]

assert '"cablecert_report"' in script
assert 'cablecert_report: "cablecert"' in script
assert '`${funnelPrefix(product)}_cta_click`' in script
assert 'event_scope: "paid_report_funnel"' in script
assert 'if (readConsent() !== "granted") return;' in script
# Preserve pre-existing Works / Premises CTA telemetry and prevent double binding.
assert 'document.querySelectorAll("[data-ga4-funnel-cta]")' in script
assert 'element.getAttribute("data-ga4-funnel-cta")' in script
assert 'if (!element.hasAttribute("data-ga4-funnel-cta"))' in script
assert 'a[href^="https://cablecert.regevidencehub.com/start"]' in script
assert sum(page.count('href="https://cablecert.regevidencehub.com/start"') for page in pages) == 3
for page in pages:
    assert 'analytics-consent.js' in page
print("CABLECERT_FUNNEL_ENTRY_EVENT=PASS")
