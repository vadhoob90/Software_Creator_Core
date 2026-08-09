# Core and product repository responsibility model

**Status:** Adopted initial architecture  
**Parent:** [Core–Product Consumption Model](README.md)

## Purpose

This document defines the authority and ownership boundary between PDLC Core and a downstream product repository. The boundary prevents reusable mechanisms from becoming entangled with one product while allowing product teams to specialise behaviour deliberately.

## Core responsibility

PDLC Core owns reusable mechanisms and non-negotiable contracts, including:

- Principles, engineering standards, and their identifiers.
- Common product-development terminology and schemas.
- Job, outcome, event, evidence, exception, and approval contracts.
- Workflow-state and transition machinery.
- Context resolution, precedence, and provenance.
- Routing protocols and generic role contracts.
- Control definitions and enforcement interfaces.
- Execution, validation, evaluation, and upgrade harnesses.
- Generic patterns, profiles, templates, and adapters.
- Security, authority, isolation, and resource-boundary mechanisms.
- Compatibility and migration rules for Core-owned contracts.

Core MUST remain useful without importing a product repository's domain knowledge. A feature belongs in Core only when it expresses a reusable mechanism or a broadly applicable invariant.

## Product repository responsibility

The downstream product repository owns policy and behaviour specific to the product, including:

- Product goals, requirements, architecture, and terminology.
- Technology choices and repository structure.
- Product-specific standards that tighten or extend Core.
- Domain schemas, rules, adapters, and integrations.
- Repository-owned agent specialisations.
- Product and technology profiles.
- Evaluation cases, fixtures, and acceptance thresholds.
- Product decisions, implementation, tests, and release artifacts.
- Repository and domain learning.
- Local exceptions, risk acceptance, and approval records.
- Operational history and product-specific retention policy.

The product repository remains the source of truth for its mutable product state. Core MUST NOT silently rewrite that state.

## Ownership classes

Every managed path or artifact MUST be assigned one ownership class:

| Class | Owner | Upgrade behaviour |
|---|---|---|
| Core packaged | Core | Replaced only by installing a new immutable Core version |
| Core managed | Core with explicit boundary | Updated transactionally inside a marked or generated boundary |
| Product owned | Product repository | Preserved; changes require product authority |
| Generated evidence | Execution record | Immutable after finalisation except for append-only annotations |
| External reference | External owner | Referenced with version or digest where material |

Unclassified mutable files are treated as product owned.

## Permitted specialisation

A product repository MAY:

- Add domain definitions and profiles.
- Add or specialise roles beneath the Core role contract.
- Add workflows that use valid Core transitions.
- Add controls and evaluations.
- Tighten numeric or qualitative requirements.
- Add approval points.
- Restrict tools, authority, providers, or data.
- Add compatible schemas and adapters.
- Record local learning.

A specialisation MUST identify its source and the Core contract it extends.

## Restricted changes

A product repository MUST NOT silently:

- Remove or weaken a Core MUST requirement.
- Increase authority beyond the active job grant.
- Convert a failure, partial, degraded, or cancelled outcome into success.
- Disable provenance, evidence, isolation, or approval requirements.
- Change a Core-owned schema incompatibly.
- Replace workflow-state validation with agent discretion.
- Allow a role specialisation to replace its Core role contract.
- Modify the policy evaluating the same execution.

A necessary deviation uses the exception mechanism from the [Engineering standards catalogue](../standards/README.md#exceptions). Resolution retains both the Core value and the approved effective value.

## Agents and orchestration

Agents are specialised contributors, not autonomous owners of the development lifecycle.

Core MUST:

- Select the permitted workflow transition.
- Resolve and validate the role context.
- Grant only job-scoped capabilities.
- Validate structured responses.
- Persist material artifacts and provenance.
- Determine whether evidence satisfies the transition gate.
- Escalate decisions requiring human authority.

An agent MAY propose a transition or decision but MUST NOT advance its own work past an approval or independent-verification boundary.

A human may perform any contributor role. Agent contracts describe jobs, not a mandatory model executor.

## Product learning

Learning discovered during product work remains product owned initially. It may affect later jobs only when its activation policy permits it.

A proposed promotion into Core MUST include:

- The observed problem and product context.
- Evidence that the local response improved an outcome.
- Evidence that the learning is not tied to one domain.
- The proposed Core contract, pattern, control, or evaluation change.
- Compatibility and migration impact.
- Representative tests or evaluation cases.
- A human-reviewed decision.

Core MUST NOT ingest downstream learning automatically.

## Boundary examples

| Concern | Core owns | Product repository owns |
|---|---|---|
| Architecture work | Architecture job and evidence contracts | The product architecture and ADRs |
| Testing | Coverage semantics and harness interfaces | Product fixtures and domain acceptance cases |
| Agents | Generic role contract and authority boundary | Role specialisation and domain instructions |
| Routing | Valid transition and routing protocol | Product routes permitted within that protocol |
| Security | Least-authority and approval mechanisms | Product data classification and additional restrictions |
| Learning | Learning record and activation contract | Local observations, feedback, and approved records |
| Release | Release evidence and approval contract | Product deployment mechanism and environment policy |

## Review questions

A boundary change is acceptable only when reviewers can answer:

- Is this reusable mechanism or product-specific policy?
- Which owner can change it?
- Can a Core upgrade preserve all product-owned state?
- Can the product tighten the behaviour without forking Core?
- Could the specialisation weaken a non-negotiable contract?
- Is provenance sufficient to explain the effective result?
- Does the design avoid promoting one product's preference into every consumer?
