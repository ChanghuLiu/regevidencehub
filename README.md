# RegEvidenceHub

Static customer-facing portfolio site for RegEvidenceHub.

## Design goals

- zero server runtime and zero database dependency
- plain HTML/CSS suitable for GitHub Pages
- customer-first explanation of the product portfolio
- separate AI-safe and commercial MCP boundaries
- machine-discovery surfaces for crawlers and agents
- no third-party fonts, scripts, analytics, or tracking by default

## Publish with GitHub Pages

1. In repository **Settings → Pages**, choose **Deploy from a branch**.
2. Select branch **main**, folder **/(root)**, then Save.
3. Keep `CNAME` set to `regevidencehub.com`.
4. Configure the apex/root DNS for GitHub Pages.
5. After DNS resolves, enable **Enforce HTTPS** in GitHub Pages settings.

Product subdomains remain hosted by their existing production services.

## Local portfolio taxonomy check

After changing the eight-product catalog or product-line labels, run:

```bash
python3 scripts/validate-portfolio-taxonomy.py
```

This validates the existing eight-entry catalog and its five/three line split. It does not probe product endpoints or change publication state.

The machine-readable `/.well-known/mcp-market.json` is exported from the v1.0.0-dev.2 Product Manifest and checked against its strict public allowlist schema. From the development baseline directory, regenerate it with:

```bash
PYTHONPATH=src python3 -m market_baseline.cli export-site --root . --site-root /path/to/regevidencehub
```

This is an explicit local release step, not an automatic website build. The generated file intentionally labels product metadata `OWNER_REVIEW_REQUIRED` and all endpoint states `NOT_REPROBED` until reviewed evidence changes those states.
