# Persisted job and evidence artifact model

**Status:** Adopted initial architecture  
**Parent:** [Core–Product Consumption Model](README.md)

## Purpose

Durable product-development state belongs in structured, versioned artifacts rather than chat history or an agent's memory. The artifact model makes decisions, transitions, evidence, authority, and outcomes inspectable after an execution ends or Core evolves.

Paths and schemas in this document are **conceptual** until implemented.

## Job identity and location

Each workflow execution has an immutable job identifier. Core-managed runtime records live beneath:

```text
.pdlc/jobs/<job-id>/
```

Authored product artifacts—source, tests, architecture decisions, documentation, and release configuration—remain in normal product-owned locations. The job record references those artifacts rather than copying them unnecessarily.

## Conceptual job record

```text
.pdlc/jobs/<job-id>/
├── manifest.json
├── request.json
├── context-composition.json
├── workflow-state.json
├── events.jsonl
├── decisions/
│   └── architecture-decision.json
├── plans/
│   ├── implementation-plan.json
│   └── evidence-plan.json
├── evidence/
│   ├── static-analysis.json
│   ├── tests.json
│   ├── coverage.json
│   ├── compatibility.json
│   └── security.json
├── reviews/
│   ├── architecture-review.json
│   └── implementation-review.json
├── approvals/
│   └── approval.json
├── exceptions/
│   └── exception.json
└── outcome.json
```

Only applicable artifacts are created. The manifest records required, present, absent, and intentionally skipped artifacts.

## Artifact envelope

Every structured job artifact MUST use a common envelope:

```yaml
schema: pdlc://artifacts/evidence/test-result/v1
artifact_id: ARTIFACT_ID
job_id: JOB_ID
artifact_type: test-result
version: 1
status: final
created_at: 2026-08-09T12:00:00Z
created_by:
  type: harness
  id: test-runner
source:
  core_version: 0.1.0
  product_revision: FULL_COMMIT
  inputs:
    - path: tests/
      digest: sha256:...
authority:
  reference: JOB_AUTHORITY_ID
content:
  result: passed
  ...
integrity:
  digest: sha256:...
supersedes: null
```

The envelope separates artifact identity and provenance from its type-specific content.

## Required job artifacts

### Manifest

The manifest indexes all job artifacts, schemas, versions, ownership, integrity digests, and retention classification. It is the entry point for inspection.

### Request

The request records the authorised product outcome, scope, initiating actor, constraints, risk classification, and acceptance criteria. Sensitive task content may remain in an authorised product file referenced by digest.

### Context composition

The composition manifest follows [Runtime job-context composition](runtime-job-context-composition.md) and records exactly which Core and product sources governed each contributor invocation.

### Workflow state

Workflow state records the current phase, valid next transitions, completed gates, blockers, and authority required. It is changed only through validated transitions.

### Events

The event stream is append-only and records material transitions, contributor invocations, tool boundaries, approvals, failures, recovery, and finalisation. Events link to detailed artifacts rather than embedding large or sensitive content.

### Outcome

The final outcome uses the classifications from [ES-003](../standards/ES-003-explicit-traceable-recoverable-execution.md):

- success
- partial
- degraded
- cancelled
- failure

It identifies delivered artifacts, unmet acceptance criteria, active exceptions, recovery or next actions, and the evidence used for the decision.

A job MUST NOT have more than one current final outcome. A reopened job creates a new outcome version and records the superseded result.

## Decision artifacts

Material architecture, product, compatibility, security, and exception decisions MUST record:

- Decision required.
- Context and constraints.
- Alternatives considered.
- Chosen option and rationale.
- Applicable principles and standards.
- Consequences and follow-up.
- Deciding authority.
- Review and approval state.
- Product artifact created or changed.

A contributor's private reasoning is not a decision artifact. Persisted rationale must be concise, reviewable, and safe to disclose to its authorised audience.

## Plans

A plan translates an approved decision into bounded work. It identifies:

- Inputs and dependencies.
- Steps and responsible roles.
- Expected product artifacts.
- Applicable controls.
- Required evidence.
- Authority and approval boundaries.
- Recovery and rollback.
- Completion and stop conditions.

The evidence plan MUST exist before implementation for elevated and critical changes.

## Evidence

Evidence artifacts prove specific claims. Each item MUST identify:

- Claim or control evaluated.
- Subject and exact version.
- Method, tool, and configuration.
- Input or fixture versions.
- Result and observed measurements.
- Expected threshold or rubric.
- Exclusions and limitations.
- Time and producer.
- Integrity digest and raw-result locator where retained.

A summary MUST preserve a failed critical result even when aggregate metrics pass.

Evidence types may include static analysis, tests, coverage, mutation, schema validation, compatibility, migration, recovery, performance, accessibility, security, agent evaluation, and release provenance.

## Reviews and independence

A review artifact records the claims inspected, evidence considered, findings, unresolved risks, requested changes, and decision.

For elevated or critical work, the reviewer MUST be independent of the contributor for the decision being verified. Independence can be provided by a separate human, agent invocation with isolated context, or deterministic gate appropriate to the claim. The implementer MUST NOT be the sole authority marking its own elevated or critical work compliant.

## Approval

An approval artifact identifies:

- Approver identity and authority basis.
- Exact action, target, and material parameters.
- Evidence and preview reviewed.
- Risk and irreversible boundary.
- Approval time and expiry.
- Conditions and permitted variance.
- Whether the approval was used.

A changed material parameter invalidates the approval. Approval for a plan is not automatically approval for execution.

## Exceptions

An exception artifact follows the [standards exception contract](../standards/README.md#exceptions). It is linked from every result affected by the deviation and remains visible until expiry or remediation.

## Lifecycle and immutability

Artifact states are:

```text
draft → proposed → reviewed → approved or rejected → final → superseded → archived
```

Not every artifact uses every state. Valid transitions are defined by the artifact schema.

Final evidence and decision artifacts are immutable. Corrections create a new version that points to the superseded artifact. Append-only annotations may add discovery or retention metadata without changing the historical decision.

## Privacy and data minimisation

Job records MUST NOT become a shadow store of source, credentials, private prompts, personal data, or model hidden reasoning.

Core MUST:

- Reference authorised product artifacts by stable locator and digest where possible.
- Store only fields required for workflow integrity and explanation.
- Apply classification, access, retention, and deletion policy.
- Redact secrets before persistence.
- Keep tenant and product records isolated.
- Record that a sensitive input was used without copying it unnecessarily.

## Retention and deletion

The product repository owns retention policy within Core minimum integrity requirements.

Deletion MUST identify:

- Artifacts selected.
- Historical views or claims affected.
- External or product artifacts not deleted.
- Required authority.
- Recovery expectation.
- Tombstone or audit record retained.

Deleting a job record MUST NOT delete product source or release artifacts through an implicit cascade.

## Inspection

The intended interfaces are:

```text
pdlc job show JOB_ID
pdlc job evidence JOB_ID
pdlc job history JOB_ID
pdlc job verify JOB_ID
```

Human-readable output and stable structured output must represent the same underlying artifacts.
