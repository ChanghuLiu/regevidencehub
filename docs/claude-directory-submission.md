# Claude directory preparation — eight RegEvidenceHub products

Updated: 2026-10-01. This guide supersedes the earlier four-product, Team/Enterprise-only packet.

## Submission route and state

Submit each remote server as a separate MCP connector at https://claude.ai/directory/manage.
Pro, Max, Team and Enterprise accounts can submit; Free accounts cannot. Pro/Max use the account owner; Team/Enterprise use the appropriate organization permissions.
A custom connector, a third-party directory request, an OpenAI review and an Anthropic directory submission are separate states. No Anthropic submission receipt is recorded here.

## Endpoint and access inventory

| Product | Proposed branded server URL | Access boundary | Tools observed |
| --- | --- | --- | ---: |
| RegEvidenceHub — UK Taxi PHV Licensing | https://taxi.regevidencehub.com/ai/mcp | Public AI endpoint; payment-free and read-only | 5 |
| RegEvidenceHub — CQC Provider Compliance | https://cqc.regevidencehub.com/ai/mcp | Public AI endpoint; payment-free and read-only | 4 |
| RegEvidenceHub — UK Premises Licensing | https://premises.regevidencehub.com/ai/mcp | Public AI endpoint; payment-free and read-only | 4 |
| RegEvidenceHub — UK Sponsor Change | https://works.regevidencehub.com/ai/mcp | Public AI endpoint; payment-free and read-only | 4 |
| RegEvidenceHub Waste | https://waste.regevidencehub.com/ai/mcp | Public AI endpoint; payment-free and read-only | 9 |
| RegEvidenceHub CableCert | https://cablecert.regevidencehub.com/mcp | Discovery/status without authentication; commercial audit/reviewer access needs verification | 3 |
| FactoryTalk Import Preflight | https://factorytalk.regevidencehub.com/mcp | Discovery/status without authentication; commercial audit/reviewer access needs verification | 2 |
| OPC UA NodeSet Gate | https://nodeset.regevidencehub.com/ai/mcp | Discovery/status without authentication; commercial audit/reviewer access needs verification | 5 |

Oct 1 discovery checked 36 tools. Every tool has a title in its annotations and boolean readOnlyHint, destructiveHint and openWorldHint fields. This is metadata evidence, not proof that every tool has run in Claude.
NodeSet's upload creation/append tools write temporary memory. Its uploaded audit consumes IDs. Do not classify all five NodeSet tools as read-only.

## Listing and reviewer materials

Use product documentation and privacy URLs, a working support contact, the existing product icon and accurate scope descriptions. Public support: launchcircle.server@gmail.com. Shared publisher website: https://regevidencehub.com/.
The public installation guide is https://regevidencehub.com/claude.html. Five regulatory endpoints exclude commercial checkout/payment flows. The industrial candidates retain their existing commercial audit boundary; do not describe them as universally free.

## Remaining gates

1. Publisher access: last observed Claude account was Free. Confirm a paid plan before portal submission.
2. Run each exposed tool in Claude; retain actual prompts, tool arguments and outcomes. Do not attest from tools/list, an OpenAI result or a Grok connection alone.
3. Reuse and verify each product icon. Existing FactoryTalk and NodeSet directory PNGs are 512 × 512; other assets must be obtained from their existing releases.
4. Establish reviewer access for commercial audits without changing paid execution policy or making a self-funded payment to manufacture evidence.
5. Complete company/identity and the portal's actual category selections. The authorized publisher must complete policy/terms acknowledgments.
6. For the no-auth regulatory surfaces, explain that no test login is required; do not invent credentials.
7. Submit, then record the actual Anthropic receipt and review state. Do not mark these drafts submitted or published.

## Current official references

- https://claude.com/docs/directory/publish
- https://claude.com/docs/connectors/building/submission
- https://claude.com/docs/connectors/building/review-criteria

OpenAI review submissions and existing Grok connections are preserved. Selection Lab remains internal and is excluded.

## Product listing drafts

### 1. RegEvidenceHub — UK Taxi PHV Licensing

- Proposed slug: regevidencehub-uk-taxi-phv
- One-liner: Evidence-linked taxi and PHV licensing preflight for supported England authorities.
- Documentation: https://regevidencehub.com/products/taxi.html
- Privacy: https://regevidencehub.com/privacy/
- Support: https://regevidencehub.com/support/
- Behavior: read_only
- Access: This selected public AI endpoint is payment-free; commercial endpoints are excluded.

Read-only licensing preflight for supported England taxi and private-hire authorities. List coverage, inspect source freshness, check one-authority applicant or fleet facts, and compare supported authorities. Results preserve missing facts and source review states. This connector does not submit applications, issue licences or provide legal advice.

First reviewer prompt: Which England taxi and private-hire licensing authorities can this service check?

### 2. RegEvidenceHub — CQC Provider Compliance

- Proposed slug: regevidencehub-cqc-compliance
- One-liner: Navigate CQC registration, provider-change and statutory-notification workflows.
- Documentation: https://regevidencehub.com/products/cqc.html
- Privacy: https://regevidencehub.com/privacy/
- Support: https://regevidencehub.com/support/
- Behavior: read_only
- Access: This selected public AI endpoint is payment-free; commercial endpoints are excluded.

Read-only guidance for England CQC provider-registration, provider-change and statutory-notification workflows. Identify the relevant workflow, inspect official evidence status and list the fact categories needed for a preflight. It does not infer provider facts, process patient records, file with CQC or provide clinical or legal decisions.

First reviewer prompt: What can the CQC compliance connector help a provider prepare?

### 3. RegEvidenceHub — UK Premises Licensing

- Proposed slug: regevidencehub-uk-premises-licensing
- One-liner: Prepare supported premises-licensing workflows without guessing local policies.
- Documentation: https://regevidencehub.com/products/premises.html
- Privacy: https://regevidencehub.com/privacy/
- Support: https://regevidencehub.com/support/
- Behavior: read_only
- Access: This selected public AI endpoint is payment-free; commercial endpoints are excluded.

Read-only preparation for supported local licensing authorities and Licensing Act 2003 workflows. List coverage, check one authority and identify the facts needed for a premises-licensing preflight. The connector does not issue licensing decisions, infer unsupported local rules, submit filings or process payment.

First reviewer prompt: What does this premises-licensing connector support?

### 4. RegEvidenceHub — UK Sponsor Change

- Proposed slug: regevidencehub-uk-sponsor-change
- One-liner: Evidence-linked preflight for UK Skilled Worker sponsor-duty changes.
- Documentation: https://regevidencehub.com/products/works.html
- Privacy: https://regevidencehub.com/privacy/
- Support: https://regevidencehub.com/support/
- Behavior: read_only
- Access: This selected public AI endpoint is payment-free; commercial endpoints are excluded.

Read-only sponsor-duty change preflight using user-supplied Skilled Worker and organization facts. List supported change events, check GOV.UK evidence status and assess bounded salary, role, location, absence or organizational changes. Missing decisive facts remain missing. The connector does not file Home Office reports, approve immigration status or provide legal representation.

First reviewer prompt: What UK sponsor changes can this connector help screen?

### 5. RegEvidenceHub Waste

- Proposed slug: regevidencehub-england-waste
- One-liner: Evidence-linked England waste routes, registration readiness and permit-change preflight.
- Documentation: https://waste.regevidencehub.com/plugin
- Privacy: https://waste.regevidencehub.com/plugin/privacy
- Support: https://regevidencehub.com/support/
- Behavior: read_only
- Access: This selected public AI endpoint is payment-free; commercial endpoints are excluded.

Read-only England waste-operation preflight, carrier/broker/dealer registration lifecycle guidance, Digital Waste Tracking receiving-site readiness and current-versus-proposed permit-change screening. The public AI endpoint is payment-free. It preserves missing or conflicted facts and source evidence. It does not assign waste codes, determine hazardous classification, submit regulatory records or approve operations.

First reviewer prompt: Show the England scope and supported waste-operation roles and activities.

### 6. RegEvidenceHub CableCert

- Proposed slug: regevidencehub-cablecert
- One-liner: Reconcile cable certification CSV evidence against an owner-supplied link inventory.
- Documentation: https://cablecert.regevidencehub.com/
- Privacy: https://cablecert.regevidencehub.com/privacy
- Support: https://cablecert.regevidencehub.com/support
- Behavior: read_only
- Access: Discovery/status is no-auth; commercial audit/payment and reviewer access require final verification. No settlement/payment performed.

Structured-cabling certification evidence QA from contractor CSV exports. Inspect available fields, reconcile expected cable IDs, identify missing/unexpected links, trace duplicate or retest lineage and compare an owner-supplied expected test limit. It reports evidence exceptions with source provenance; it does not certify cabling, determine TIA compliance, establish safety or accept contractor work. Audit access may require payment under the commercial endpoint.

First reviewer prompt: Inspect a CSV with Cable ID, Test Summary and Test Limit columns and identify the available evidence fields.

### 7. FactoryTalk Import Preflight

- Proposed slug: factorytalk-import-preflight
- One-liner: Check FactoryTalk View tag and alarm CSV import contracts before import.
- Documentation: https://factorytalk.regevidencehub.com/
- Privacy: https://factorytalk.regevidencehub.com/privacy
- Support: https://factorytalk.regevidencehub.com/support
- Behavior: read_only
- Access: Discovery/status is no-auth; commercial audit/payment and reviewer access require final verification. No settlement/payment performed.

Deterministic static checks for supported FactoryTalk View tag, digital-alarm and analog-alarm CSV import layouts. Reports schema markers, record-shape errors, required-field issues, duplicate names and bounded alarm-contract findings. It does not connect to a PLC/HMI, import files, validate runtime behavior, commission equipment or certify machine safety. Audit access may require payment under the commercial endpoint.

First reviewer prompt: Check a supported official FactoryTalk View tag CSV before import.

### 8. OPC UA NodeSet Gate

- Proposed slug: opc-ua-nodeset-gate
- One-liner: Compare OPC UA NodeSet2 XML revisions for deterministic structural compatibility findings.
- Documentation: https://nodeset.regevidencehub.com/
- Privacy: https://nodeset.regevidencehub.com/privacy
- Support: https://nodeset.regevidencehub.com/support
- Behavior: read plus temporary in-memory writes and upload consumption
- Access: Discovery/status is no-auth; commercial audit/payment and reviewer access require final verification. No settlement/payment performed.

Static compatibility preflight between baseline and candidate OPC UA NodeSet2 XML revisions. Identifies additions, removals and bounded type/reference changes while resolving namespace identities. A temporary chunked-upload workflow supports larger documents and consumes upload IDs after audit. Results do not certify runtime interoperability, commissioning or safety. Audit/payment behavior on the candidate AI path still needs reviewer-access verification.

First reviewer prompt: What does the NodeSet compatibility service check and what does it not certify?
