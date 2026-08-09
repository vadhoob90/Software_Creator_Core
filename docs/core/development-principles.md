# Development principles

**Status:** Adopted  
**Adopted:** 9 August 2026

These principles are the foundation of PDLC Core. They guide the design of its
definitions, agents, execution harnesses, routing logic, public contracts,
generated products, and development process.

They are decision rules, not slogans. Every principle must influence design,
implementation, and verification. Objective requirements should become
automated checks. Requirements that depend on judgement should become explicit
review questions. Exceptions must never be silent.

## 1. Comprehension and usability come first

PDLC Core must minimise the cognitive and operational effort required for
humans and machines to understand, navigate, change, and correctly use the
system.

Code is an interface to maintainers and agents, just as commands, schemas,
documentation, errors, and generated artifacts are interfaces to consumers.
Because code is read and changed more often than it is originally written,
clarity takes precedence over cleverness and premature generality.

### Design

- Use cohesive components with explicit responsibilities and directed
  dependencies.
- Prefer intention-revealing domain names and visible control flow.
- Make capabilities, constraints, state, and next actions discoverable.
- Design human-readable and machine-readable interfaces together.
- Introduce abstractions only when current, demonstrated use cases justify
  them.

### Implementation

- Keep functions, modules, prompts, schemas, and routes small enough to
  understand in context.
- Use comments to explain constraints and decisions, not to restate unclear
  implementation.
- Provide concise help, representative examples, structured output, stable exit
  semantics, and actionable errors.
- Keep repository structure and documentation consistent with the conceptual
  model exposed to downstream consumers.
- Treat accessibility as part of usability whenever PDLC Core produces or
  governs a user interface.

### Verification

Readability, complexity, documentation, schema, interface, and architecture
checks should expose avoidable cognitive load. Numeric limits are review
signals and hard safety boundaries; they are not definitions of good design.
Representative onboarding and traversal tasks should prove that a new human or
agent can find and use a capability without hidden knowledge.

### Further reading

- [What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
- [Command Line Interface Guidelines](https://clig.dev/)
- [JSON Schema specification](https://json-schema.org/specification)
- [Web Content Accessibility Guidelines overview](https://www.w3.org/WAI/standards-guidelines/wcag/)

## 2. Every claim requires evidence

Claims about behaviour, quality, safety, compatibility, performance, or
readiness must be supported by proportionate evidence. Automated tests are the
primary evidence for repeatable behaviour, but a coverage percentage alone is
not evidence that the right assertions exist.

An effective automated test suite gives maintainers justified confidence that
important behaviour works, meaningful breakage will be detected, and the
system can change safely.

### Design

- Define observable behaviour, invariants, failure modes, and acceptance
  criteria before choosing test mechanics.
- Make components testable through their public contracts.
- Separate deterministic offline evaluation from bounded tests that require
  external providers.
- Match the test boundary to the risk: unit, integration, contract, generated
  workspace, command/API, end-to-end, security, performance, accessibility, or
  agent evaluation.

### Implementation

- Add focused tests with behavioural changes and characterization tests before
  risky structural changes.
- Measure statement and branch coverage independently, using ratcheted floors
  rather than treating a target as a ceiling.
- Test negative paths, recovery, idempotency, migrations, repeated generation,
  and partial failure.
- Use property or invariant testing where examples cannot adequately describe
  the input space.
- Use mutation testing selectively on changed or critical logic to show that
  tests detect plausible faults.
- Keep the offline baseline deterministic, isolated from credentials and the
  network, and intolerant of unexplained flakes.
- Test the enforcement harness itself.

### Verification

A change is not complete merely because tests ran. Review must establish that
the tests would fail for the defect they are intended to prevent, exercise the
right boundary, make useful assertions, and remain maintainable. Subjective
agent behaviour requires versioned cases, explicit rubrics, thresholds, and
retained evaluation evidence.

### Further reading

- [Testing overview from Software Engineering at Google](https://abseil.io/resources/swe-book/html/ch11.html)
- [Branch coverage measurement with coverage.py](https://coverage.readthedocs.io/en/7.14.0/branch.html)
- [Practical mutation testing at scale](https://research.google/pubs/practical-mutation-testing-at-scale-a-view-from-google/)

## 3. Every execution is explicit, traceable, and recoverable

Every operation must produce an honest, inspectable outcome. Success, partial
success, degradation, cancellation, and failure must be distinguishable. No
component may swallow a failure, silently substitute weaker behaviour, or
claim that state was persisted when it was not.

Executions should be reproducible where the underlying system permits it and
attributable where variation is unavoidable.

### Design

- Define stable outcome and failure classifications at component boundaries.
- Design recovery, retry, cancellation, rollback, and resume behaviour with the
  primary workflow.
- Make important state and transitions observable without exposing secrets or
  private inputs.
- Identify the inputs, versions, configuration, route, agent or model,
  decisions, and outputs needed to explain a result.

### Implementation

- Propagate failures or convert them into explicit typed outcomes.
- Make fallbacks visible and record why they were selected.
- Bound retries, time, recursion, concurrency, and cost; make retried operations
  idempotent where possible.
- Use atomic persistence and avoid destructive recovery by default.
- Emit privacy-safe structured diagnostics, correlation identifiers, and
  actionable remediation.
- Record provenance and hashes for released artifacts and significant generated
  outputs.
- Pin relevant dependencies and inputs so a result can be recreated or its
  variation explained.

### Verification

Fault-oriented tests should cover exceptions, timeouts, corrupt state,
interrupted writes, provider failure, retry exhaustion, rollback, and
diagnostic redaction. Tests should reject false success and silent degradation.
Release verification should prove that artifacts correspond to reviewed source
and declared build inputs.

### Further reading

- [Effective troubleshooting from Google SRE](https://sre.google/sre-book/effective-troubleshooting/)
- [Monitoring distributed systems from Google SRE](https://sre.google/sre-book/monitoring-distributed-systems/)
- [Definition of reproducible builds](https://reproducible-builds.org/docs/definition/)
- [SLSA provenance](https://slsa.dev/spec/v1.2/provenance)

## 4. Evolution is deliberate, compatible, and reversible

Every stateful component and every observable contract has an intentional
lifecycle. Change should happen through small, independently verifiable
increments with clear migration and rollback paths.

The lifecycle considered for a component or artifact is:

create → inspect → validate → update → activate or deactivate → version or
migrate → recover or roll back → archive or delete

Not every transition must be implemented immediately. Unsupported transitions
must be explicit, and speculative extension frameworks must not be introduced
solely because a transition might be needed later.

### Design

- Identify public, persisted, generated, and downstream-consumed contracts.
- Define supported states, transitions, invariants, ownership, retention, and
  terminal states.
- Design compatibility and migration before changing an observable contract.
- Prefer the smallest seam required by current consumers.
- Keep each increment releasable and give it one coherent purpose.

### Implementation

- Version public contracts and immutable releases deliberately.
- Provide deprecation warnings, support windows, compatibility readers, and
  migration guidance before removal.
- Preserve user-owned and downstream-owned state during generation and upgrade.
- Separate substantial refactoring from behavioural change.
- Avoid permanent forwarding layers and unused abstractions disguised as
  compatibility.
- Make rollback possible without corrupting or silently discarding newer state.

### Verification

Lifecycle tests should cover supported transitions, invalid transitions,
repeat operations, migrations, rollback, retention, and deletion where
applicable. Historical fixtures and consumer contract tests should prove
compatibility. Each change should include its tests and documentation and leave
the default branch usable.

### Further reading

- [Semantic Versioning](https://semver.org/)
- [Small changes from Google Engineering Practices](https://google.github.io/eng-practices/review/developer/small-cls.html)
- [Google AIP-180: Backwards compatibility](https://google.aip.dev/180)
- [Kubernetes deprecation policy](https://kubernetes.io/docs/reference/using-api/deprecation-policy/)

## 5. Automation is secure, bounded, and human-governed

Agents and automated workflows must operate within explicit authority. The
ability to perform an action does not imply permission to perform it. Humans
retain responsibility and control at consequential boundaries.

Security, privacy, and safety are lifecycle concerns and default design
constraints, not a final hardening phase.

### Design

- Define trust boundaries, actors, data classifications, capabilities, and
  approval points.
- Grant the minimum filesystem, network, credential, tool, and data access
  required for the current task.
- Separate planning, decision, approval, and execution where consequences
  justify it.
- Provide dry runs, previews, interruption, resumption, override, and safe
  decommissioning.
- Treat prompts, retrieved content, tool results, dependencies, models, and
  external services as potentially untrusted inputs.

### Implementation

- Validate inputs and outputs at every trust boundary.
- Require scoped, risk-proportionate approval for irreversible, externally
  visible, privileged, financial, or sensitive-data actions.
- Preserve an audit trail of authority, decisions, tool use, and state changes
  without logging secrets or private content unnecessarily.
- Isolate tenants, workspaces, memories, and credentials.
- Pin and audit dependencies, protect the build and release path, and produce
  supply-chain evidence appropriate to the artifact.
- Enforce limits on tool chains, recursion, retries, time, tokens, and cost.
- Fail safely when authority, validation, or required oversight is absent.

### Verification

Threat models and abuse cases should become security, permission, isolation,
prompt-injection, data-exfiltration, adversarial, and approval-boundary tests.
CI should scan dependencies and source, verify locked inputs, and exercise
least-authority configurations. Human review remains required where context and
consequence cannot be reduced to a reliable automated rule.

### Further reading

- [NIST AI Risk Management Framework Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)
- [NIST guidance on AI risk management and human-AI interaction](https://airc.nist.gov/airmf-resources/airmf/appendices/app-c-ai-risk-management-and-human-ai-interaction/)
- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)
- [NIST Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final)
- [SLSA build track](https://slsa.dev/spec/v1.2/build-track-basics)

## Enforcement model

Every future rule derived from these principles should state:

1. The principle and risk it serves.
2. The design and implementation consequence.
3. The automated evidence, if the requirement is objective.
4. The human-review evidence, if judgement is required.
5. The remediation path when the rule fails.
6. The owner, rationale, and expiry of any temporary exception.

Quality thresholds should start from a documented green baseline and ratchet
upward when the signal is actionable. A metric must not become a target that
distorts the behaviour it was introduced to protect. Enforcement code is
production infrastructure and must itself be tested.

## Change review

A change is ready only when reviewers can answer:

- Which principle or user outcome does this change advance?
- Is it easier to understand and use after the change?
- What evidence proves the intended behaviour?
- Are every success, degraded, and failure outcome explicit?
- Is provenance sufficient to explain significant outputs?
- Have lifecycle, compatibility, migration, and rollback been considered?
- Is the change small enough to understand and reverse independently?
- Are agent authority, security, privacy, and human-control boundaries
  preserved?
- Do documentation and examples still match reality?
- Is every exception explicit, owned, and time-bounded?
