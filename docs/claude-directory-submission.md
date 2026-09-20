# Claude Connectors Directory submission package

Prepared: 2026-09-20

This package is for the four RegEvidenceHub public AI-safe remote MCP surfaces. It intentionally excludes the commercial `/mcp` endpoints and all x402/Stripe/payment flows.

## Shared submission facts

- Company: RegEvidenceHub
- Company website: https://regevidencehub.com/
- Transport: Streamable HTTP
- Connection type: Universal URL, one listing per product
- Authentication: None
- Access model: Public, read-only, payment-free connector surface
- Documentation hub: https://regevidencehub.com/claude.html
- Support: https://regevidencehub.com/support/
- Privacy policy: https://regevidencehub.com/privacy/
- Terms: https://regevidencehub.com/terms/
- Suggested categories: Legal, Productivity
- Personal health data: No. CQC tooling is provider-compliance workflow guidance and explicitly instructs users not to submit patient records or full care files.
- Sponsored content: No
- Financial transactions: No
- Conversation-data collection: No beyond bounded request/tool inputs needed to answer the call and operational telemetry described by the product service.
- Tool behavior: Read-only. Each exposed tool carries a title and `readOnlyHint: true`.
- Test account credentials: Not applicable because these public AI-safe endpoints do not require authentication.
- Allowed link URIs: None required; these connector tools do not use `ui/open-link`.
- Reviewer test method: Exercise every exposed tool through Claude as a custom connector or MCP Inspector before submission.

## 1. UK Taxi PHV Licensing

- Server URL: https://taxi.regevidencehub.com/ai/mcp
- Server name: RegEvidenceHub — UK Taxi PHV Licensing
- Tagline: Evidence-linked taxi and PHV licensing preflight
- Suggested permanent slug: regevidencehub-uk-taxi-phv
- Documentation URL: https://regevidencehub.com/products/taxi.html
- Read/write classification: Read-only
- Account or plan prerequisite: None
- Primary use cases:
  - List supported England taxi/private-hire licensing authorities.
  - Check official-source freshness and review state.
  - Run a bounded one-authority licensing preflight from user-supplied facts.
  - Compare supported authorities without inferring missing applicant facts.
- Listing description:
  RegEvidenceHub UK Taxi PHV Licensing provides read-only, evidence-linked preflight for supported England taxi and private-hire licensing authorities. Claude can list supported authorities, inspect official-source freshness, run a bounded applicant or fleet preflight, and compare requirements across supported authorities. The connector uses deterministic regulatory rules and fails closed when evidence or critical facts are insufficient. It does not expose payment, checkout, regulator approval, or legal advice.
- First reviewer prompt:
  List supported authorities, then run a Birmingham preflight for an applicant aged 27 who has held a driving licence for exactly two years.
- Expected safety behavior:
  Treat exact-boundary or conflicting source conditions explicitly and do not invent licensing-authority approval.

## 2. CQC Provider Compliance

- Server URL: https://cqc.regevidencehub.com/ai/mcp
- Server name: RegEvidenceHub — CQC Provider Compliance
- Tagline: CQC provider compliance workflow navigation
- Suggested permanent slug: regevidencehub-cqc-compliance
- Documentation URL: https://regevidencehub.com/products/cqc.html
- Read/write classification: Read-only
- Account or plan prerequisite: None
- Primary use cases:
  - Choose the appropriate CQC provider-registration, provider-change, or statutory-notification workflow.
  - Check official evidence/source status.
  - Identify bounded fact categories required before a compliance preflight.
  - Avoid inferring provider status, regulated activities, locations, manager roles, or event facts.
- Listing description:
  RegEvidenceHub CQC Provider Compliance is a read-only navigator for England CQC provider-registration, provider-change, and statutory-notification workflows. Claude can identify the relevant workflow, inspect evidence status, and list the bounded facts needed for a later preflight. The connector is designed to use only user-supplied facts and not to infer missing provider, activity, location, role, or incident information. It does not expose payment, checkout, patient-record processing, CQC approval, or legal advice.
- First reviewer prompt:
  Choose the right workflow for an already-registered provider that wants to add a new regulated activity, then list the facts needed.
- Expected safety behavior:
  Ask for missing compliance facts instead of defaulting or inferring them.

## 3. UK Premises Licensing

- Server URL: https://premises.regevidencehub.com/ai/mcp
- Server name: RegEvidenceHub — UK Premises Licensing
- Tagline: UK premises licensing workflow preflight
- Suggested permanent slug: regevidencehub-uk-premises-licensing
- Documentation URL: https://regevidencehub.com/products/premises.html
- Read/write classification: Read-only
- Account or plan prerequisite: None
- Primary use cases:
  - List supported local licensing authorities.
  - Check whether a named authority is supported.
  - Prepare the minimum facts for a Licensing Act 2003 premises workflow.
  - Avoid inferring local policy for unsupported authorities.
- Listing description:
  RegEvidenceHub UK Premises Licensing provides read-only discovery and preflight preparation for supported local licensing authorities and Licensing Act 2003 workflows. Claude can list supported authorities, check support for a named authority, and identify the facts needed before a premises-licensing preflight. The connector uses only user-supplied facts and does not infer local rules for unsupported authorities. It does not issue licensing decisions, expose payment or checkout, represent regulator approval, or provide legal advice.
- First reviewer prompt:
  Check whether Westminster City Council is supported, then list the starting facts for on-premises alcohol sales.
- Expected safety behavior:
  Do not infer missing authority, venue, activity, alcohol, hours, exemption, or local-policy facts.

## 4. UK Sponsor Change

- Server URL: https://works.regevidencehub.com/ai/mcp
- Server name: RegEvidenceHub — UK Sponsor Change
- Tagline: UK Skilled Worker sponsor change preflight
- Suggested permanent slug: regevidencehub-uk-sponsor-change
- Documentation URL: https://regevidencehub.com/products/works.html
- Read/write classification: Read-only
- Account or plan prerequisite: None
- Primary use cases:
  - List supported Skilled Worker sponsor-change events.
  - Check official GOV.UK sponsor-guidance freshness.
  - Assess salary, role, work-location, absence, delayed-start, stopping-sponsorship, TUPE, merger, takeover, and organization changes.
  - Return AFFECTED, NOT_AFFECTED, REVIEW_REQUIRED, or INSUFFICIENT_INPUT without inventing missing compliance facts.
- Listing description:
  RegEvidenceHub UK Sponsor Change is a read-only evidence-linked preflight for UK Skilled Worker sponsor-duty changes. Claude can check supported event types, inspect official GOV.UK evidence status, and assess common employee or organization changes with deterministic rules. Missing facts remain missing so the engine can return INSUFFICIENT_INPUT instead of guessing. The connector does not expose payment, checkout, Home Office approval, or legal advice.
- First reviewer prompt:
  Assess a permanent Skilled Worker salary decrease with role and work location unchanged. Do not assume whether the same salary option remains met.
- Expected safety behavior:
  Preserve omitted facts such as `same_salary_option_still_met` as missing and return an insufficient-input state when required.

## External portal gate

Remote MCP directory submission itself must be performed from a Claude Team or Enterprise organization by an Owner/Primary Owner or another Enterprise member with the delegated Directory permission. Until that organization-level portal access exists, the four endpoints remain installable as Claude custom connectors but cannot be submitted to the public Connectors Directory from an individual Claude plan.
