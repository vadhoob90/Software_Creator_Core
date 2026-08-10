# ES-002: Evidence and testing

**Status:** Adopted initial baseline  
**Governing principles:** [P-002: Works—and we prove it](../core/development-principles.md#p-002-we-will-create-software-that-worksand-we-will-prove-it); [P-006: Understand the need](../core/development-principles.md#p-006-we-will-understand-the-need-before-we-build)

**Default enforcement:** Documented

## Purpose

Claims about a product need, feasibility, behaviour, safety, compatibility,
performance, accessibility, or readiness must be supported by evidence
proportionate to the consequence of being wrong. Coverage measures execution,
not test effectiveness, so coverage floors are combined with discovery,
behavioural, fault-oriented, and risk-based requirements.

## Applicability

This standard applies to product requests, discovery and feasibility artifacts,
production code, prompts and agent behaviour, schemas, migrations, routing,
integrations, generated workspaces, commands, APIs, security controls, and the
enforcement harness itself.

## Requirements

### ES-002-00: Request readiness

Before specialist feasibility or substantial delivery commitment, an applicable
product request MUST have a versioned brief that identifies:

- The initiating request and current authority.
- The affected people or stakeholders and the problem or opportunity.
- The desired outcome and proposed success and guardrail evidence.
- Available evidence and its source.
- Scope, non-goals, constraints, dependencies, and known risks.
- Assumptions, unresolved questions, and stopping conditions.
- The specialist perspectives required for feasibility and why they are
  relevant.

The Product Manager MAY draft and refine the brief but MUST NOT invent product
intent. Missing product intent requires clarification. Questions that a
qualified specialist can investigate MAY remain open when their scope is
explicit.

Urgent, security, legal, regulatory, or otherwise mandatory work MAY use an
accelerated path. The path MUST still record its need, authority, risk, accepted
uncertainty, and reason normal readiness evidence could not be obtained.

### ES-002-01: Testable claims

Every material behavioural change MUST state:

- The observable claim being made.
- The relevant invariants and acceptance criteria.
- The boundary at which the claim will be tested.
- Important negative and failure cases.
- The evidence required for acceptance.

Tests MUST use meaningful assertions against observable behaviour. Executing code without checking the intended outcome is not sufficient evidence.

### ES-002-02: Required test boundaries

Changes MUST use the smallest test boundary that proves the claim, plus wider boundaries where integration risk exists.

As applicable, evidence MUST include:

- Unit tests for deterministic local behaviour.
- Contract tests for public or component boundaries.
- Integration tests for persistence, providers, tools, and generated artifacts.
- End-to-end tests for critical consumer journeys.
- Migration and compatibility tests for observable or persisted contracts.
- Security, accessibility, performance, or agent evaluations when those claims are made.

Duplicating the same assertion at every layer is not required.

### ES-002-03: Coverage floors

Coverage is measured over hand-authored production code. Explicitly identified generated, vendored, and unreachable defensive code may be excluded with review.

The initial blocking floors are:

| Scope | Line coverage | Branch coverage |
|---|---:|---:|
| Repository total | 80% | 75% |
| Changed production code | 90% | 85% |
| Changed critical code | 95% | 90% |

Critical code includes authority and permission checks, security boundaries, destructive or financial actions, persistence and migration logic, release integrity, routing policy, and exception or approval enforcement.

A change MUST NOT reduce total line or branch coverage below the greater of the fixed floor or the recorded baseline on main. Coverage changes smaller than the reporting tool's stable precision may be ignored when documented.

One hundred percent coverage MUST NOT be required indiscriminately. It MAY be required for a small, critical decision module when every meaningful path can be specified.

### ES-002-04: Behaviour beyond coverage

Applicable tests MUST cover:

- Expected success.
- Invalid and boundary inputs.
- Explicit failure and degraded outcomes.
- Timeout and retry exhaustion.
- Cancellation or interruption.
- Repeated execution and idempotency.
- Partial persistence and recovery.
- Migration, rollback, and historical compatibility.
- Concurrency where shared state can race.

A review MUST identify any relevant category intentionally omitted.

### ES-002-05: Mutation and property testing

Changed critical decision logic MUST undergo mutation testing when a maintained tool exists. The mutation score MUST be at least 80%, and no surviving mutant may bypass an authority, security, persistence, or release-integrity invariant.

Property or invariant testing SHOULD be used when the input space cannot be represented adequately by examples, including parsers, serializers, routing, state transitions, and generated structures.

A non-viable or equivalent mutant may be excluded only with a recorded explanation.

### ES-002-06: Deterministic baseline

The default required test suite MUST:

- Run without network access or production credentials.
- Control time, randomness, locale, and other nondeterministic inputs where material.
- Isolate mutable state between tests.
- Produce the same pass or fail result from the same source and declared inputs.
- Fail when required fixtures, tools, or dependencies are absent.

External-provider tests MUST be separately identified, bounded, and unable to conceal failure of the offline baseline.

### ES-002-07: Flake policy

A failing required test MUST NOT be converted into a pass through automatic retry. Retries may collect diagnostic evidence, but the original failure remains visible.

A flaky test must be fixed promptly or quarantined with:

- An owner.
- A tracking issue.
- A reason and impact.
- An expiry date.
- A replacement gate when the quarantined test protects elevated or critical behaviour.

Quarantine MUST be visible in CI and MUST NOT reduce the applicable coverage calculation silently.

### ES-002-08: Test independence and integrity

Tests MUST fail when the defect they protect against is introduced. Test doubles MUST preserve the contract relevant to the claim and MUST NOT mock away the behaviour under test.

Changes to tests, fixtures, rubrics, snapshots, or thresholds that make a production change pass require the same scrutiny as the production change. Approval and enforcement logic MUST have independent tests preventing self-approval or bypass.

### ES-002-09: Agent evaluations

Subjective or probabilistic agent behaviour MUST use versioned evaluation cases with:

- Representative and adversarial inputs.
- Explicit expected properties or scoring rubrics.
- A declared model, tools, policy, and configuration.
- Acceptance thresholds and variance handling.
- Retained results sufficient to reproduce or explain the decision.

Averages MUST NOT conceal a critical safety failure.

### ES-002-10: Feasibility synthesis and commitment

When a request requires specialist feasibility work, each assessment MUST
identify its scope, evidence, assumptions, uncertainty, risks, and recommended
investigations. A specialist MUST NOT claim authority outside its assigned
responsibility.

Before substantial delivery commitment, the Product Manager MUST produce a
versioned synthesis that:

- References the product brief and specialist assessments used.
- Preserves material disagreements and unresolved risks.
- Presents viable options, including defer, decline, research, prototype, or
  non-software responses where supported by the evidence.
- Describes expected value, affected people, duties, safety, cost or effort,
  opportunity cost, confidence, and material trade-offs without reducing every
  decision to a single economic score.
- Recommends a next step and identifies the evidence that could change it.
- Records the human authority required to proceed and the resulting decision.

The Product Manager MAY synthesise and recommend but MUST NOT silently overrule
a specialist finding or make a consequential commitment reserved for human
authority. The orchestrator MUST NOT advance the job past the commitment gate
until the required decision and accepted residual risk are recorded.

## Required verification

### Automated controls

When implementation exists, CI MUST:

- Run deterministic unit, contract, and applicable integration suites.
- Enforce line and branch coverage independently.
- Measure changed-code coverage.
- Run targeted mutation tests for changed critical logic.
- Detect skipped, quarantined, or unexpectedly retried tests.
- Publish machine-readable and human-readable results.
- Test the enforcement harness.

### Review controls

Reviewers MUST be able to answer:

- Does an applicable request brief distinguish human intent, evidence,
  assumptions, and specialist questions?
- Can feasibility contributors investigate without inventing the product goal?
- Does the feasibility synthesis preserve specialist disagreement and present
  meaningful options and trade-offs?
- Is the delivery commitment attributable to the required human authority?
- Would the tests fail for the defect they claim to prevent?
- Is the chosen boundary appropriate?
- Are important negative, recovery, and compatibility behaviours covered?
- Have mocks or snapshots replaced useful assertions?
- Do the metrics support confidence rather than merely satisfy a target?
- Are agent evaluation cases representative and resistant to threshold gaming?

## Evidence

The evidence package must include, as applicable, the request brief, specialist
feasibility evidence, Product Manager synthesis and commitment decision, test
results, separate line and branch coverage, changed-code coverage, mutation
results, declared exclusions, quarantine records, and evaluation
configuration.

## Further reading

- [Testing overview from Software Engineering at Google](https://abseil.io/resources/swe-book/html/ch11.html)
- [Branch coverage with coverage.py](https://coverage.readthedocs.io/en/7.14.0/branch.html)
- [Practical mutation testing at scale](https://research.google/pubs/practical-mutation-testing-at-scale-a-view-from-google/)
