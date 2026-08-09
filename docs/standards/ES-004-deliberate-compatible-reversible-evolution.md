# ES-004: Deliberate, compatible, and reversible evolution

**Status:** Adopted initial baseline  
**Governing principle:** [Evolution is deliberate, compatible, and reversible](../core/development-principles.md#4-evolution-is-deliberate-compatible-and-reversible)  
**Default enforcement:** Documented

## Purpose

Every stateful component and observable contract must have an intentional lifecycle. Changes must preserve downstream value, expose unsupported transitions, and provide migration and rollback proportional to risk without introducing speculative infrastructure.

## Applicability

This standard applies to public and internal contracts, schemas, configuration, persisted state, prompts and agent definitions, generated artifacts, packages, commands, APIs, routing policies, models, dependencies, and released components.

## Requirements

### ES-004-01: Lifecycle declaration

Each stateful component or externally observable artifact MUST identify its supported lifecycle from:

create → inspect → validate → update → activate or deactivate → version or migrate → recover or roll back → archive or delete

The declaration MUST identify:

- Supported states and transitions.
- Preconditions, invariants, and terminal states.
- State owner and source of truth.
- Retention and deletion expectations.
- Recovery and rollback behaviour.
- Transitions intentionally unsupported.

Only transitions needed by current consumers must be implemented. Unsupported transitions MUST fail explicitly and MUST NOT be simulated through destructive recreation without the consumer's informed choice.

### ES-004-02: Contract inventory

A change MUST identify affected:

- Public interfaces and schemas.
- Persisted formats and migrations.
- Generated formats intended for downstream ownership.
- Commands, configuration, and environment contracts.
- Agent inputs, outputs, tools, prompts, and routing behaviour.
- Events, logs, and other operational contracts.
- Supported versions and external dependencies.

Observable behaviour is a contract even when it was not originally documented.

### ES-004-03: Versioning

Released contracts MUST use an explicit versioning policy. Semantic Versioning SHOULD be used for packages and comparable public interfaces.

A change is breaking when a supported consumer must change to retain previously promised behaviour. Renaming, removal, stricter validation, default changes, error-shape changes, reordered side effects, or reduced permissions may be breaking even when types compile.

Experimental contracts MUST be marked, bounded, and excluded from compatibility guarantees explicitly.

### ES-004-04: Backward compatibility

A non-breaking evolution MUST preserve existing supported consumers or provide a compatibility reader or adapter. Writers SHOULD emit the newest format while readers accept all versions in the declared support window.

Compatibility layers MUST have an owner and removal condition. Permanent forwarding modules or indefinite dual behaviour are prohibited unless they are the supported public contract.

### ES-004-05: Deprecation

Removal or breaking change requires:

- A visible deprecation notice.
- A replacement or migration path.
- The first deprecated version and planned removal version.
- A declared support window.
- Consumer-impact evidence.
- Tests for both old and new behaviour during the window.

The default minimum support window is one minor release and 90 days, whichever is longer. A shorter window requires an exception for an urgent security, legal, or integrity risk. Pre-release or explicitly experimental contracts may declare a shorter policy before consumers adopt them.

### ES-004-06: Migration

A migration MUST define:

- Source and target versions.
- Preconditions and validation.
- Idempotency or repeat behaviour.
- Forward transformation.
- Treatment of unknown or future fields.
- Failure and partial-completion outcomes.
- Backup, checkpoint, or recovery strategy.
- Rollback feasibility and the point after which rollback is unsafe.
- Verification of resulting state.

Destructive migration MUST require explicit authority and a recoverable backup or a documented reason recovery is impossible.

### ES-004-07: Reversibility

Elevated and critical changes MUST have a tested rollback, roll-forward, feature-disable, or compensating plan before activation. The plan MUST preserve state created by the newer version or explicitly identify why preservation is impossible.

Rollback MUST NOT silently discard, reinterpret, or corrupt newer state. If reversal is unsafe after a point of no return, that boundary requires explicit approval before it is crossed.

### ES-004-08: Small coherent increments

Each change MUST have one coherent purpose and leave the default branch usable. Refactoring SHOULD be separated from behavioural change unless separation would increase risk.

A change SHOULD be independently reviewable, testable, releasable, and reversible. Size is not a substitute for cohesion, but reviewers must request decomposition when unrelated decisions cannot be evaluated independently.

### ES-004-09: No speculative lifecycle machinery

A framework, extension point, migration engine, compatibility layer, or generic lifecycle abstraction MUST be justified by a current transition or consumer. Future possibility alone is insufficient.

The simplest implementation satisfying current lifecycle and compatibility requirements SHOULD be chosen. Known future requirements may influence a clean seam, but MUST NOT require unused implementation.

### ES-004-10: Safe ownership boundaries

Generators and migrations MUST distinguish PDLC-owned state from human- or downstream-owned state. Repeated generation or upgrade MUST preserve consumer-owned content unless replacement is explicit, previewed, and authorised.

Deletion and archival MUST be scoped, confirmable, and observable. Material deletion MUST have a declared recovery expectation.

## Required verification

### Automated controls

When implementation exists, CI MUST include applicable:

- State-transition and invalid-transition tests.
- Repeated create, update, and generation tests.
- Historical-fixture and consumer-contract tests.
- Forward migration, interrupted migration, and repeat migration tests.
- Rollback or roll-forward tests.
- Deprecation and version-policy checks.
- Preservation tests for consumer-owned state.
- Documentation checks for supported versions and migration paths.

### Review controls

Reviewers MUST be able to answer:

- Which contracts and persisted formats change?
- Can existing supported consumers continue unchanged?
- Are every supported and unsupported lifecycle transition explicit?
- Is migration safe under interruption and repetition?
- What happens to state created by the newer version during rollback?
- Is each compatibility layer necessary and temporary?
- Has speculative machinery been avoided?

## Evidence

The evidence package must include the contract inventory, lifecycle impact, compatibility results, migration and reversal results, consumer-impact analysis, and active deprecations or exceptions.

## Further reading

- [Semantic Versioning](https://semver.org/)
- [Google AIP-180: Backwards compatibility](https://google.aip.dev/180)
- [Kubernetes deprecation policy](https://kubernetes.io/docs/reference/using-api/deprecation-policy/)
- [Google Engineering Practices: small changes](https://google.github.io/eng-practices/review/developer/small-cls.html)
