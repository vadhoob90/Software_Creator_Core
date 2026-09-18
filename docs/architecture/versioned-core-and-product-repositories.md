# Versioned Core and product repositories

**Status:** Adopted initial architecture  
**Parent:** [Core–Product Consumption Model](README.md)

## Purpose

A product repository consumes Software Creator Core as an immutable, versioned dependency. The product remains thin, portable, and independently owned while Core can release improvements through an explicit compatibility and upgrade lifecycle.

Names and commands in this document are **conceptual** until an implementation is released.

## Dependency model

A product repository MUST pin an immutable Core release and commit the dependency resolution needed to reproduce it.

Accepted references are:

- A published semantic version.
- A full immutable artifact digest.
- A full reviewed commit identifier for an approved private or diagnostic source.

A product repository MUST NOT:

- Track Core's moving default branch.
- Use an abbreviated commit identifier.
- Clone or copy the Core implementation into its repository.
- Use a Git submodule as the runtime dependency.
- Depend on an undeclared local path in a released or shared configuration.

The implementation ecosystem may differ by consumer, but the resolved Core identity MUST be inspectable through one standard product manifest.

## Product manifest

The future product manifest should declare at least:

```yaml
schema_version: 1

core:
  source: registry
  version: 0.1.0
  digest: sha256:...

profiles:
  - product-default

repository:
  configuration: pdlc/
  runtime_state: .pdlc/

compatibility:
  minimum_core: 0.1.0
```

The manifest is product owned. Core validates it but does not silently change declared policy.

## Distribution responsibilities

A Core release MUST provide:

- Immutable version and artifact identity.
- Changelog and compatibility classification.
- Versioned schemas and generic contracts.
- Migration and deprecation notes.
- Validation or conformance entry point.
- Provenance connecting the artifact to reviewed source.
- Supported upgrade and rollback information.

A product repository MUST retain:

- Its Core version and resolved lock or digest.
- Product-specific configuration.
- Downstream validation and evaluation cases.
- Its latest upgrade report.
- Any compatibility decisions or exceptions.

## Managed and product-owned material

Core may create a small, explicitly marked managed section in a product file when necessary—for example, a README dependency summary. It MUST update only that marked section.

Existing product agents, policies, configuration, learning, tests, architecture, implementation, and history are product owned and MUST NOT be overwritten by an upgrade.

A newly introduced template MAY be offered when its destination does not exist. When a product-owned destination exists, Core reports a decision instead of replacing it.

## Compatibility result

An upgrade preview MUST separate these claims:

1. **Dependency resolution:** can the requested Core artifact be obtained and pinned?
2. **Current repository readiness:** does current product configuration conform to the target Core?
3. **Historical usability:** do retained job and evidence artifacts remain inspectable and meaningful?
4. **Behavioural compatibility:** do downstream tests and evaluations still satisfy their declared requirements?

Each finding uses one classification:

- **compatible** — no product decision or migration is required.
- **automatically_migratable** — a deterministic, reversible migration is available.
- **decision_required** — product authority must choose between valid alternatives.
- **blocking** — safe application is not currently possible.

A summary MUST NOT collapse a blocking finding into a general success.

## Upgrade preview

The conceptual command:

```text
pdlc core upgrade --to 0.2.0
```

performs a read-only preview. It should report:

- Current and target Core identities.
- Dependency and lock changes.
- New, changed, deprecated, and removed contracts.
- Standards and control differences.
- Product overrides affected by new Core values.
- New templates and product-owned path conflicts.
- Schema and historical-artifact compatibility.
- Required migrations and irreversible boundaries.
- Downstream validation commands.
- Expected manual decisions.
- Rollback feasibility.

The preview MUST NOT modify the product repository, invoke external providers, or create a development job.

## Upgrade application

The conceptual command:

```text
pdlc core upgrade --to 0.2.0 --apply
```

requires the reviewed preview and explicit product authority. Application MUST:

1. Verify that source state still matches the preview.
2. Capture the previous dependency and lock state.
3. Apply only deterministic approved migrations.
4. Preserve product-owned paths.
5. Update managed boundaries.
6. Run Core conformance checks.
7. Run product validation, tests, and applicable evaluations.
8. Persist the upgrade report.
9. Commit the new dependency identity only after validation.

If a required validation fails, Core MUST restore the previous dependency and lock state. A failed restoration is an explicit critical failure with recovery instructions.

## Conflict resolution

A product override is evaluated against the target Core contract:

- A tighter requirement remains valid unless the target makes it incoherent.
- An extension remains valid when its schema and namespace remain compatible.
- A weaker value requires an active exception.
- A removed Core capability requires migration or an explicit product decision.
- A product-owned file conflict is never resolved through silent overwrite.

A conflict SHOULD block only affected capabilities when safe isolation is possible. Global integrity, authority, or schema failures block the upgrade.

## Versioning and deprecation

Core follows the [evolution standard](../standards/ES-004-deliberate-compatible-reversible-evolution.md). A Core release MUST classify breaking, compatible, and experimental changes from the consumer's perspective.

Deprecation begins before removal and includes:

- Replacement or migration path.
- First deprecated version.
- Planned removal version.
- Support window.
- Detection in product validation.
- Historical-artifact implications.

## Release and downstream validation flow

1. Implement and validate a reusable change in Software Creator Core.
2. Produce an immutable release and provenance.
3. Run the reference-product compatibility suite.
4. Publish the release and migration guidance.
5. Preview the upgrade in each product repository.
6. Resolve product decisions.
7. Apply and run downstream checks.
8. Persist and review the upgrade evidence.
9. Roll out independently per product.

Core release success does not imply downstream product success.

## Removal

Removing Core from a product repository MUST preserve product-owned artifacts and explain which Core-dependent commands, schemas, or historical views will no longer work. Destructive cleanup requires an explicit target list and product authority.
