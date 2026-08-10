# Runtime job-context composition

**Status:** Adopted initial architecture  
**Parent:** [Core–Product Consumption Model](README.md)

## Purpose

Every human or agent contribution receives one resolved job context assembled from ordered, attributable sources. Core—not an individual agent—selects applicable requirements, validates precedence, grants authority, and records what was loaded or skipped.

Names, paths, and commands in this document are **conceptual** until implemented.

## Composition order

For each job invocation, Core resolves layers in this order:

1. Core execution-harness contract.
2. Applicable Core principles.
3. Applicable engineering standards and machine-readable controls.
4. Core workflow and lifecycle contract.
5. Core role contract.
6. Selected product, domain, and technology profiles.
7. Repository-owned role specialisation.
8. Active, role-matched repository learning.
9. Task-specific artifacts and prior approved decisions.
10. Current authority, approval, isolation, and resource limits.

The task instruction and structured payload are then supplied as job input.

A lower layer may specialise a higher layer but cannot replace, weaken, or reinterpret a non-negotiable requirement. Authority and limits are evaluated after content resolution so no instruction layer can grant itself additional capability.

## Relevant context, not indiscriminate context

Every agent is aware that the Core principles govern the system, but Core SHOULD provide the applicable operational subset rather than injecting every standards document verbatim.

Applicability is resolved from:

- Job and workflow type.
- Contributor role.
- Artifacts affected.
- Lifecycle transition requested.
- Contract and persistence impact.
- Data and trust boundaries.
- Side effects and action risk.
- Product and technology profiles.
- Active exceptions and approvals.

An omitted source is recorded as **skipped** with a stable reason such as:

- not-applicable-to-role
- artifact-type-not-affected
- lifecycle-transition-not-requested
- no-active-role-matched-learning
- profile-not-selected
- approval-not-required
- source-version-unsupported
- source-failed-validation

Absence MUST remain visible. A missing required layer is a resolution failure, not an empty default.

## Resolved job packet

The future machine-readable packet should contain:

```yaml
job:
  id: JOB_ID
  workflow: product-change
  phase: implementation
  role: implementer

core:
  version: 0.1.0
  contracts:
    harness: sha256:...
    workflow: sha256:...
    role: sha256:...

requirements:
  principles: [P-001, P-002, P-004, P-005, P-006, P-007]
  standards:
    - ES-001-03
    - ES-002-01
    - ES-002-03
    - ES-003-01
  controls:
    complexity.maximum:
      value: 12
      core_value: 15
      source: product-profile

inputs:
  architecture_decision: docs/adr/0012.md
  implementation_plan: .pdlc/jobs/JOB_ID/plan.json

authority:
  mode: write-local
  allowed_paths: [src/, tests/, docs/]
  denied_capabilities: [release, external-publication]
  approval: null

limits:
  duration_seconds: 1800
  tool_calls: 80
  cost: product-default

composition_manifest: .pdlc/jobs/JOB_ID/context-composition.json
```

This example is a target contract, not an implemented schema.

## Role-specific resolution

### Product Manager contributor

During intake, receives:

- The authorised request and available initiating context.
- Applicable need, evidence, comprehension, security, and authority rules.
- Product goals and constraints that are already approved and relevant.
- The product-brief and clarification output contract.

It may inspect authorised repository and product evidence and ask targeted
questions. It does not invent missing product intent, commit delivery, or
receive implementation or release credentials merely because the request
proposes a solution.

During feasibility synthesis, it additionally receives the exact product brief
and specialist assessments. It must preserve material disagreement, uncertainty,
and residual risk while presenting options and a recommendation for the
applicable human decision.

### Architecture contributor

Receives:

- Product goals and constraints.
- Existing architecture and contract inventory.
- Applicable comprehension, lifecycle, compatibility, security, and evidence rules.
- Product and technology profiles.
- Approved domain learning.
- Decision and evidence output contracts.

It does not receive implementation credentials unless the same approved job explicitly combines the roles.

### Implementation contributor

Receives:

- Approved architecture decision and implementation plan.
- Applicable code, testing, failure, lifecycle, and security controls.
- Permitted repository paths and tools.
- Product coding profile and role specialisation.
- Required evidence and completion contract.

It does not decide that its own elevated or critical evidence is sufficient.

### Verification contributor

Receives:

- Claims, artifacts, and declared evidence.
- Applicable standards and independent review rubric.
- Reference or historical cases.
- Read-only access by default.

It should not inherit the implementer's unreviewed private reasoning or authority.

## Composition manifest

Every invocation MUST persist a privacy-safe manifest containing:

- Job, workflow phase, and role.
- Core and product manifest versions.
- Ordered loaded and skipped sources.
- Stable source identifiers, versions, and hashes.
- Applicable principle, standard, and control identifiers.
- Effective values with Core and product provenance.
- Selected learning record identifiers and activation versions.
- Task-artifact locators and hashes.
- Authority source, approval reference, and resource limits.
- Provider, model, tool-policy, and agent versions where applicable.
- Resolution warnings and failures.

The manifest MUST NOT duplicate secrets, private task contents, credentials, model hidden reasoning, or sensitive source text merely to make the run inspectable. The authorised source remains the source of truth; a digest establishes which version was used.

## Preflight and historical inspection

The intended read-only preflight is:

```text
pdlc context explain --role implementer --job JOB_ID
```

It resolves current state and reports the ordered context without executing a contributor, mutating job state, or invoking an external provider.

Historical inspection is:

```text
pdlc context show JOB_ID
```

It reads the persisted composition manifest and distinguishes historical state from a resolution performed against current files.

Both interfaces require equivalent structured output for machine consumers.

## Conflict resolution

Resolution MUST fail or require a decision when:

- A product value weakens Core without an active exception.
- Two sources at the same precedence define incompatible values.
- A required source is invalid, absent, or outside its support window.
- A learning record lacks valid activation or scope.
- An approval does not match the exact action and parameters.
- A requested tool or data source exceeds job authority.

Resolution MUST NOT select an arbitrary winner.

## Learning activation

Learning records are product owned and inactive by default. Activation requires a declared scope, applicable roles or artifacts, evidence source, approval, and version.

Feedback from the current job MUST NOT alter the context of that same job silently. A learning proposal is a separate artifact and affects later jobs only after activation.

## Determinism and variability

The same declared sources and resolver version SHOULD produce the same resolved packet. Source ordering is stable.

A model response may remain variable. The composition manifest explains the inputs and constraints; it does not claim that probabilistic output is byte-for-byte reproducible.
