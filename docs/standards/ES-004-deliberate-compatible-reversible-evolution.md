# ES-004: Deliberate, compatible, and reversible evolution

**Status:** Adopted initial baseline  
**Governing principle:** [P-004: Evolves without losing trust](../core/development-principles.md#p-004-we-will-create-software-that-can-evolve-without-losing-trust)

**Default enforcement:** Documented

## Purpose

Every stateful component, released capability, and observable contract must
have an intentional lifecycle. Changes must preserve downstream value, expose
unsupported transitions, and provide operational readiness, migration,
rollback, feedback, and retirement evidence proportional to risk without
introducing speculative infrastructure.

## Applicability

This standard applies to public and internal contracts, schemas, configuration,
persisted state, prompts and agent definitions, generated artifacts, packages,
commands, APIs, routing policies, models, dependencies, released components,
and applicable operational and retirement artifacts.

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

### ES-004-11: Proportionate operational readiness

Software intended for an operational environment MUST identify, in proportion
to its consequence and delivery model:

- The product owner and operational owner.
- The supported environment, dependencies, capacity assumptions, and known
  failure boundaries.
- Health and user-impact signals required to recognise material degradation.
- Support, escalation, recovery, rollback or roll-forward, and safe-disablement
  expectations.
- Backup, restoration, retention, and integrity-verification needs.
- The release evidence and human authority required before activation.

Not every artifact is a continuously operated service. Libraries, local tools,
batch software, agent definitions, and offline artifacts MAY satisfy this
requirement through support, compatibility, recovery, and consumer guidance
rather than service-level objectives or continuous monitoring.

PDLC MAY generate or validate operational-readiness artifacts during a bounded
job. That does not make PDLC the downstream product's monitoring, deployment,
or incident-management system.

### ES-004-12: Outcome and feedback contract

Before a material release or activation, the product MUST identify the evidence
that will show whether the affected outcome improved, remained acceptable, or
regressed. The contract MUST include, where applicable:

- The intended outcome and relevant baseline.
- Success and guardrail measures.
- Qualitative or quantitative evidence sources.
- A review owner and review point or condition.
- Evidence that would trigger investigation, iteration, rollback, suspension,
  or retirement.

The evidence method MUST be appropriate to the decision. Statistical
significance, online experimentation, or continuous telemetry MUST NOT be
required where qualitative research, operational evidence, compliance review,
or another method better fits the product and risk.

Feedback MAY be supplied to a later PDLC job manually or through an authorised
integration. It MUST NOT silently change the context or policy of the job that
produced it.

### ES-004-13: Retirement and data disposition

Material retirement MUST begin with an impact assessment covering:

- The evidence and authority supporting retirement.
- Affected people, consumers, integrations, contracts, and dependencies.
- Notice and support periods appropriate to risk, commitments, available
  replacements, and urgency.
- Migration, export, compatibility, redirection, or replacement options.
- Data retention, deletion, anonymisation, archival, legal hold, and
  restoration requirements by data category.
- Release, access, credential, infrastructure, documentation, and support
  changes.
- The point of no return, recovery feasibility, retained evidence, and
  accountable approval.

No universal notice period or data action applies to every product. The chosen
policy MUST be explicit, justified, and consistent with applicable product,
legal, contractual, security, and consumer obligations.

An agent MAY assemble evidence, draft communication, or execute bounded,
reversible retirement steps within authority. Consequential retirement and
irreversible disposition require the applicable human approval.

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
- Operational-readiness artifact and recovery checks.
- Outcome-contract and scheduled-review checks where applicable.
- Retirement-impact, consumer-notice, and data-disposition checks.

### Review controls

Reviewers MUST be able to answer:

- Which contracts and persisted formats change?
- Can existing supported consumers continue unchanged?
- Are every supported and unsupported lifecycle transition explicit?
- Is migration safe under interruption and repetition?
- What happens to state created by the newer version during rollback?
- Is each compatibility layer necessary and temporary?
- Has speculative machinery been avoided?
- Is the software operable and recoverable in its declared delivery model?
- How will the team learn whether the released change achieved its outcome?
- Can the product be retired without abandoning consumers, obligations, data,
  or required evidence?

## Evidence

The evidence package must include the contract inventory, lifecycle impact,
compatibility results, migration and reversal results, consumer-impact
analysis, applicable operational-readiness and outcome contracts, retirement
impact where relevant, and active deprecations or exceptions.

## Further reading

- [Semantic Versioning](https://semver.org/)
- [Google AIP-180: Backwards compatibility](https://google.aip.dev/180)
- [Kubernetes deprecation policy](https://kubernetes.io/docs/reference/using-api/deprecation-policy/)
- [Google Engineering Practices: small changes](https://google.github.io/eng-practices/review/developer/small-cls.html)
