# Product repository lifecycle

**Status:** Adopted initial architecture  
**Parent:** [Core–Product Consumption Model](README.md)

## Purpose

This document defines how a downstream product repository is created, connected to Core, validated, operated, upgraded, repaired, and decommissioned without losing product ownership.

Commands and paths are **conceptual** until implemented.

## Lifecycle

```text
create or adopt
→ initialise
→ configure
→ validate
→ operate
→ learn
→ upgrade or migrate
→ recover or roll back
→ archive or remove Core
```

Every operation is idempotent where possible and produces an explicit report.

## Thin product repository

A typical product repository may contain:

```text
product/
├── README.md
├── AGENTS.md
├── pdlc.yaml
├── pdlc/
│   ├── agents/
│   ├── profiles/
│   ├── controls/
│   ├── evaluations/
│   ├── learnings/
│   └── exceptions/
├── .pdlc/
│   ├── jobs/
│   ├── upgrades/
│   └── state/
├── docs/
│   ├── requirements/
│   └── architecture/
├── src/
├── tests/
└── ecosystem dependency and lock files
```

The exact product layout remains product owned. Core requires only a small manifest and known configuration/runtime boundaries.

Core implementation code, generic contracts, built-in profiles, resolvers, and harnesses remain in the pinned dependency.

## Create a new product repository

The intended high-level operation is:

```text
pdlc product create PRODUCT_PATH --profile PRODUCT_PROFILE --core 0.1.0
```

Before writing, creation MUST preview:

- Destination and files to be created.
- Core source, version, and digest.
- Selected profiles and capabilities.
- Product-owned and Core-managed boundaries.
- Dependency and lock changes.
- Validation to be run.
- Any existing-path conflicts.

Application MUST:

- Refuse a dangerous or ambiguous destination.
- Create only missing files.
- Pin the requested immutable Core version.
- Establish product configuration and empty learning/evidence stores.
- Provide representative validation and smoke tests.
- Avoid invoking external providers.
- Preserve existing material if the destination is not empty.
- Produce a creation report.

Rerunning the same operation creates missing managed material and reports preserved product-owned files. It MUST NOT reset local customisation.

## Adopt an existing repository

The lower-level operation is:

```text
pdlc product init --workspace .
```

It connects an existing product repository to Core without imposing an unrelated product layout.

Initialisation MUST:

- Inspect language, dependency, CI, and documentation boundaries without changing them.
- Ask for or infer only reversible configuration.
- Create the manifest and missing PDLC directories.
- Offer profiles rather than silently selecting consequential policy.
- Identify existing standards and possible conflicts.
- Preserve repository guidance, source, tests, and history.
- Produce a decision list for ambiguous ownership.

Creation and initialisation are distinct because a complete new product and an established repository have different ownership risks.

## Configure and specialise

A product repository may add:

- Product, domain, and technology profiles.
- Role specialisations.
- Controls that extend or tighten Core.
- Evaluation cases.
- Local learning and activation policy.
- Additional approval points.
- Tool, provider, data, and environment restrictions.

Configuration changes MUST pass context resolution and standards validation. A weaker Core value requires an explicit exception.

## Validate

The intended command is:

```text
pdlc doctor --workspace .
```

Validation MUST distinguish:

- Core dependency integrity.
- Manifest and schema validity.
- Configuration resolution.
- Ownership and managed-boundary integrity.
- Standards and control conflicts.
- Agent and role-contract compatibility.
- Learning activation validity.
- Authority and security configuration.
- Historical job readability.
- Downstream test and evaluation readiness.

Results use explicit success, partial, degraded, cancelled, or failure outcomes. A summary identifies exact remediation.

A product repository is not considered ready merely because Core imports successfully.

## Operate

A product-development job begins with a natural-language or structured request. Core then:

1. Records the authorised request and acceptance criteria.
2. Classifies artifacts, lifecycle impact, and risk.
3. Selects an allowed workflow.
4. Resolves applicable Core and product context.
5. Previews consequential authority and actions.
6. Invokes human or agent contributors role by role.
7. Validates and persists each material artifact.
8. Enforces independent evidence and approval gates.
9. Produces an explicit final outcome.

Agents do not own workflow state and cannot skip required transitions.

## Learn

Observations and feedback from a completed job produce proposed learning records. A proposal includes source evidence, scope, affected roles or artifacts, risk, and expected future effect.

Learning is:

```text
proposed → reviewed → active or rejected → superseded or retired
```

It remains inactive until approved under product policy. Activation affects future jobs only. Product learning is never promoted into Core automatically.

## Upgrade

Upgrades follow [Versioned Core and product repositories](versioned-core-and-product-repositories.md):

1. Select an immutable target.
2. Run a read-only compatibility preview.
3. Review control, schema, profile, and template differences.
4. Resolve product decisions.
5. Apply transactionally.
6. Run Core and downstream validation.
7. Persist the report.
8. Restore the previous dependency and lock state on failure.

Product-owned agents, learning, tests, architecture, and product code are preserved.

## Repair and recovery

Every modifying lifecycle operation MUST record:

- Intended and completed steps.
- Previous durable state.
- Files or dependencies changed.
- Safe repeat behaviour.
- Rollback or roll-forward instructions.
- Unresolved side effects.

A repair operation SHOULD reconstruct missing managed indexes from immutable artifacts and product-owned sources. It MUST NOT invent approvals, evidence, or learning activation.

When automatic recovery cannot prove a safe result, Core stops with a decision-required or failure outcome.

## Archive

Archiving a product repository preserves:

- The pinned Core identity.
- Product manifest and configuration.
- Final job outcomes and evidence required by retention policy.
- Release provenance.
- Active exceptions and unresolved risks.
- Instructions for restoring required tooling.

Optional caches and reproducible transient artifacts may be removed according to policy.

## Remove or replace Core

Removing Core MUST begin with a read-only impact report identifying:

- Commands and workflows that will stop functioning.
- Core-managed files eligible for removal.
- Product-owned files that will remain.
- Historical artifacts requiring Core schemas for inspection.
- Equivalent export or migration options.
- Dependency and lock changes.
- Recovery feasibility.

Application requires product authority. It MUST NOT remove source, tests, decisions, learning, releases, or historical evidence merely because Core once coordinated them.

Replacing Core with another system follows the same export and preservation rules.

## Product-to-Core learning promotion

A generic-learning proposal is a deliberate contribution, not part of routine synchronisation.

The promotion flow is:

1. Identify repeated product evidence.
2. Remove product-specific assumptions.
3. Define the affected Core contract, pattern, control, or evaluation.
4. Test against more than one representative domain where practical.
5. Analyse compatibility and migration.
6. Review and accept in Core.
7. Release through an immutable Core version.
8. Let products adopt it through normal upgrades.

## Lifecycle acceptance tests

A conforming implementation must test:

- Creation into an empty destination.
- Safe refusal or preservation in a populated destination.
- Idempotent rerun after partial creation.
- Adoption of an existing repository.
- Missing and invalid dependencies.
- Tightened product controls.
- Unauthorised weakening attempts.
- Interrupted and failed upgrade.
- Transactional dependency restoration.
- Product-owned file preservation.
- Historical job inspection after upgrade.
- Removal preview and non-destructive application.
