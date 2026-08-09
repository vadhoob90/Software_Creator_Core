# ES-003: Explicit, traceable, and recoverable execution

**Status:** Adopted initial baseline  
**Governing principle:** [Every execution is explicit, traceable, and recoverable](../core/development-principles.md#3-every-execution-is-explicit-traceable-and-recoverable)  
**Default enforcement:** Documented

## Purpose

Every operation must produce an honest, inspectable outcome. Failures and degraded behaviour must remain visible, significant results must be explainable, and interrupted or partially completed work must have an intentional recovery path.

## Applicability

This standard applies to functions and services, commands and APIs, agents and tools, routing and orchestration, persistence, migrations, external-provider calls, generators, builds, and releases.

## Requirements

### ES-003-01: Explicit outcome model

Every operation that can fail, degrade, be cancelled, or partially complete MUST expose a stable outcome classification.

The common classifications are:

- **success** — the requested outcome completed as specified.
- **partial** — a declared subset completed and the remainder is identified.
- **degraded** — an alternate, weaker mode completed and is identified.
- **cancelled** — execution stopped intentionally before completion.
- **failure** — the requested outcome did not complete.

An operation MUST NOT report success when required persistence, validation, approval, or downstream side effects failed. Partial and degraded outcomes MUST NOT be encoded as ordinary success.

### ES-003-02: Failure contracts

Failures crossing a component boundary MUST have a stable machine-readable code or type, a concise human-readable explanation, retryability or permanence where known, and an actionable remediation or escalation path.

Errors MUST preserve the causal chain needed for diagnosis. They MUST NOT expose credentials, private inputs, internal stack traces, or sensitive infrastructure details to an unauthorised consumer.

HTTP interfaces using a general error envelope SHOULD follow [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html).

### ES-003-03: No silent suppression

An exception or failed result MUST be:

- Resolved completely within the current boundary.
- Propagated unchanged.
- Translated into a documented higher-level outcome while retaining its cause.

Empty catch blocks, ignored failed promises, unobserved task failures, default-value substitution after unexpected failure, and log-only handling of a required operation are prohibited.

Expected optional absence is not a failure, but it MUST be represented distinctly from an unexpected error.

### ES-003-04: Visible fallback

A fallback MUST declare:

- The condition that activates it.
- The capability or quality lost.
- Whether the result remains acceptable.
- The event recorded for diagnosis.
- How the caller can disallow it when strict behaviour is required.

Fallback activation MUST be visible in the outcome and evidence. A fallback MUST NOT weaken security, authority, validation, or persistence guarantees.

### ES-003-05: Bounded execution

Every loop, retry policy, recursive workflow, external call, queue wait, and agent tool chain MUST have an explicit termination condition.

External and potentially blocking operations MUST define an appropriate timeout. Retries MUST define maximum attempts, retryable conditions, backoff, and final outcome. Retried writes MUST be idempotent or protected against duplicate effects.

Time, concurrency, token, step, and cost limits MUST be configurable at the boundary responsible for the work. Exhausting a limit produces an explicit non-success outcome.

### ES-003-06: Consistent persistence

A state-changing operation MUST define its atomicity boundary. It MUST NOT claim completion before durable state reaches the promised condition.

Multi-step writes MUST use a transaction, staged commit, compensating action, or resumable state machine appropriate to the risk. Recovery MUST avoid destructive overwrite by default. Persisted state MUST be validated before and after migration or restoration.

### ES-003-07: Cancellation and recovery

Long-running or multi-step work MUST define whether it is cancellable, resumable, restartable, or rollback-only. Cancellation MUST stop new side effects and leave state in a declared condition.

Recovery instructions MUST identify:

- The last known durable checkpoint.
- Work that may safely be repeated.
- Side effects requiring reconciliation.
- The route to resume, compensate, or roll back.
- Conditions requiring human intervention.

### ES-003-08: Traceability

Elevated and critical executions MUST retain enough privacy-safe information to explain the result:

- Correlation or execution identifier.
- Initiating actor and authority source.
- Input, configuration, schema, prompt, agent, model, tool, and dependency versions where material.
- Route and significant decisions.
- Start, completion, and outcome.
- Artifacts or state changed.
- Fallbacks, retries, approvals, and exceptions.

Logs and traces MUST be structured at machine-consumable boundaries. Diagnostic records MUST use data minimisation and redaction; secrets MUST NOT be logged.

### ES-003-09: Reproducibility and provenance

Builds, releases, and significant generated artifacts MUST identify reviewed source and declared inputs. Immutable artifacts MUST have a digest.

Deterministic work SHOULD reproduce byte-for-byte from the same declared inputs. Where nondeterminism is inherent, the evidence MUST identify enough configuration and external variation to explain why results can differ.

## Required verification

### Automated controls

When implementation exists, CI MUST exercise:

- Exceptions and explicit failure outcomes.
- Timeout and retry exhaustion.
- Fallback activation and strict-mode rejection.
- Cancellation and interrupted writes.
- Duplicate requests and idempotency.
- Corrupt, missing, and partially migrated state.
- Resume, compensation, and rollback.
- Diagnostic redaction.
- Provenance and artifact-digest generation.

Static analysis SHOULD reject known ignored-result and empty-handler patterns.

### Review controls

Reviewers MUST be able to answer:

- Can every observable non-success state be distinguished?
- Could any required failure be mistaken for success?
- Are fallback and retry policies bounded and visible?
- Is persisted state safe after interruption?
- Is there enough privacy-safe evidence to explain the result?
- Can an operator or agent recover without guessing?

## Evidence

The evidence package must include outcome-contract changes, fault-oriented test results, recovery or rollback evidence where applicable, redaction results, and provenance for material artifacts.

## Further reading

- [RFC 9457: Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457.html)
- [Effective troubleshooting from Google SRE](https://sre.google/sre-book/effective-troubleshooting/)
- [Monitoring distributed systems from Google SRE](https://sre.google/sre-book/monitoring-distributed-systems/)
- [Definition of reproducible builds](https://reproducible-builds.org/docs/definition/)
- [SLSA provenance](https://slsa.dev/spec/v1.2/provenance)
