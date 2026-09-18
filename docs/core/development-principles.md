# Development principles

**Status:** Adopted

**Adopted:** 9 August 2026

**Revised:** 10 August 2026

These principles are promises about the software PDLC helps people create and
the way that work is carried out. They guide the design of Software Creator Core, its
definitions, agents, optional execution harnesses, public contracts, generated
products, and product-development workflows.

In these principles, **we** means the people and authorised agents
participating in a PDLC-governed job. **Machines** includes agents, automation,
and software systems that consume the interfaces and artifacts created through
that job.

The promises are deliberately human-readable, but they are not slogans. Every
principle must influence design, implementation, and verification. Objective
requirements become automated checks where practical; requirements that
depend on judgement become explicit review questions. Exceptions are visible,
owned, justified, and time-bounded.

The principles appear in the order a team is likely to encounter them, not in
identifier order. Identifiers are stable governance contracts: P-001, P-002,
P-004, and P-005 retain their initial meaning; P-006 and P-007 are new; and the
initial P-003 is retired to the still-active ES-003 execution standard.

PDLC is an on-demand, human-directed product-development foundation. It helps
teams design and verify software that can be operated responsibly; it does not
silently become the production control plane for downstream products.

## P-006: We will understand the need before we build

Software should begin with a real need, not an assumed solution. We will ask,
listen, investigate, and make uncertainty visible before committing substantial
delivery effort.

A request may propose an implementation. The Product Manager may clarify and
challenge that proposal, but neither it nor another agent may invent product
intent. Research, prototypes, and technical spikes are legitimate ways to
reduce uncertainty; the principle prevents premature commitment, not
exploration.

### Design

- Describe the affected people or stakeholders, their present situation, and
  the outcome they need before selecting a solution.
- Record the available evidence, constraints, assumptions, non-goals, risks,
  and unresolved questions.
- Define how success will be recognised and what evidence would cause the team
  to stop, defer, or change direction.
- Distinguish missing product intent from questions that research or specialist
  feasibility work can answer.
- Make discovery and assurance proportionate to novelty, uncertainty, risk,
  cost, and reversibility.

### Implementation

- Ask targeted questions that respond to the request and known context instead
  of administering an indiscriminate questionnaire.
- Produce a versioned product brief containing the request, authority, affected
  people, problem, desired outcome, evidence, scope, constraints, assumptions,
  success measures, stopping conditions, and open questions.
- Identify which specialist perspectives are required for feasibility and why;
  do not invoke roles that cannot materially improve the decision.
- Allow urgent, legal, security, and mandatory work to use an accelerated path
  while keeping its authority, need, risk, and accepted uncertainty explicit.
- Prevent substantial solution commitment until the request-readiness gate is
  satisfied or an authorised exception is recorded.

### Verification

Review must establish that the product brief represents the initiating human's
intent, distinguishes evidence from assumption, and gives feasibility
contributors enough context to investigate without inventing the product goal.
Every downstream feasibility or delivery artifact must identify the brief
version it used. A request is not ready merely because every form field is
populated.

### Further reading

- [How the discovery phase works](https://www.gov.uk/service-manual/agile-delivery/how-the-discovery-phase-works)
- [Design Council Double Diamond](https://www.designcouncil.org.uk/our-resources/the-double-diamond/)
- [User research in discovery](https://www.gov.uk/service-manual/user-research/user-research-in-discovery)

## P-001: We will create software that people and machines can understand and use

Software should respect the time, abilities, and circumstances of the people
and machines that use, operate, maintain, or build upon it.

Code is an interface to maintainers and agents, just as commands, schemas,
documentation, errors, and generated artifacts are interfaces to consumers.
Human-readable and machine-readable interfaces must express consistent meaning.
Machine usability never implies permission to act.

### Design

- Use cohesive components with explicit responsibilities and directed
  dependencies.
- Prefer intention-revealing domain names and visible control flow.
- Make capabilities, constraints, state, authority, and next actions
  discoverable.
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
- Treat accessibility as part of usability whenever PDLC produces or governs a
  user interface.

### Verification

Readability, complexity, documentation, schema, interface, accessibility, and
architecture checks should expose avoidable cognitive or operational load.
Numeric limits are review signals and hard safety boundaries, not definitions
of good design. Representative onboarding and traversal tasks should prove
that a new person or authorised agent can find and correctly use a capability
without hidden knowledge.

### Further reading

- [What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
- [Command Line Interface Guidelines](https://clig.dev/)
- [JSON Schema specification](https://json-schema.org/specification)
- [Web Content Accessibility Guidelines overview](https://www.w3.org/WAI/standards-guidelines/wcag/)

## P-002: We will create software that works—and we will prove it

We will not ask anyone to rely on an unsupported claim. Claims about a need,
decision, behaviour, quality, safety, compatibility, performance, or readiness
must be supported by evidence proportionate to the consequence of being wrong.

Software must also tell the truth when it cannot complete its work. Success,
partial success, degradation, cancellation, and failure must remain
distinguishable. No component or agent may manufacture success, swallow a
failure, or silently substitute weaker behaviour.

### Design

- Define observable behaviour, invariants, failure modes, acceptance criteria,
  and required evidence before choosing test mechanics.
- Match evidence to the claim and risk: research, analysis, unit, integration,
  contract, end-to-end, security, performance, accessibility, or agent
  evaluation.
- Make components testable through public contracts.
- Define stable outcome and failure classifications at component and workflow
  boundaries.
- Design recovery, retry, cancellation, rollback, and resume behaviour with the
  primary workflow.
- Identify the inputs, versions, configuration, route, contributor, decisions,
  and outputs required to explain a material result.

### Implementation

- Add focused tests with behavioural changes and characterization tests before
  risky structural changes.
- Test negative paths, recovery, idempotency, migrations, repeated execution,
  partial failure, and relevant concurrency.
- Measure statement and branch coverage independently, using ratcheted floors
  rather than treating a target as a definition of quality.
- Use property or invariant testing where examples cannot adequately describe
  the input space, and mutation testing selectively on changed critical logic.
- Propagate failures or convert them into explicit typed outcomes; make every
  fallback visible and record why it was selected.
- Bound retries, time, recursion, concurrency, and cost; make retried operations
  idempotent where possible.
- Use atomic persistence, privacy-safe diagnostics, and provenance appropriate
  to the result.
- Keep the offline verification baseline deterministic, isolated from
  credentials and the network, and intolerant of unexplained flakes.

### Verification

A change is not complete merely because tests ran. Review must establish that
the evidence addresses the actual claim, that tests would fail for the defect
they protect against, and that important failure and recovery paths were
exercised. Subjective agent behaviour requires versioned cases, explicit
rubrics, thresholds, and retained results. Release evidence must connect the
reviewed source and declared build inputs to the resulting artifact.

### Further reading

- [Testing overview from Software Engineering at Google](https://abseil.io/resources/swe-book/html/ch11.html)
- [Practical mutation testing at scale](https://research.google/pubs/practical-mutation-testing-at-scale-a-view-from-google/)
- [Definition of reproducible builds](https://reproducible-builds.org/docs/definition/)
- [SLSA provenance](https://slsa.dev/spec/v1.2/provenance)

## P-007: We will create software that is secure and respects the people it serves

Security, privacy, safety, and human dignity are foundations, not features
added at the end. We will protect the people, information, systems, and
relationships entrusted to the software we help create.

Protection must be proportionate to the context and consequence. A product
repository owns its domain-specific threat model and policy, while PDLC owns
reusable security requirements, evidence contracts, and safe defaults.

### Design

- Identify people affected, trust boundaries, actors, assets, data
  classifications, threats, abuse cases, and foreseeable misuse.
- Minimise the data, authority, exposure, and dependency surface required to
  achieve the intended outcome.
- Design secure defaults, explicit authorisation, isolation, safe failure, and
  recovery with the primary workflow.
- Treat privacy, accessibility, informed control, and protection from avoidable
  harm as product requirements.
- Select security and assurance requirements according to the highest
  applicable product, data, action, and deployment risk.

### Implementation

- Validate untrusted inputs and outputs at every trust boundary.
- Enforce authentication and authorisation independently of interface
  visibility or client behaviour.
- Protect secrets and sensitive information in storage, transit, diagnostics,
  fixtures, generated artifacts, and build or release systems.
- Inventory, pin where practical, and audit dependencies and build inputs.
- Collect and retain only the data required for a declared purpose and period,
  subject to applicable legal, contractual, archival, and safety obligations.
- Make security-significant failures visible without exposing sensitive
  details.

### Verification

Threat models and abuse cases must become proportionate security, permission,
privacy, isolation, supply-chain, and adversarial tests. CI should scan source,
dependencies, and secrets; verify locked inputs; and exercise least-authority
configurations. Review must identify residual risk, accountable acceptance, and
the product context in which the evidence is valid. Consuming a PDLC definition
alone is not evidence that downstream software is secure.

### Further reading

- [NIST Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final)
- [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/)
- [OWASP Software Assurance Maturity Model](https://owaspsamm.org/)
- [Web Content Accessibility Guidelines overview](https://www.w3.org/WAI/standards-guidelines/wcag/)

## P-004: We will create software that can evolve without losing trust

Useful software will change. We will make change deliberate and protect the
people, machines, and systems that depend on the behaviour already promised.

Software must be designed proportionately for its useful life: creation,
release, operation, learning, maintenance, recovery, migration, deprecation,
and retirement. PDLC helps a team define and verify those responsibilities; it
does not assume continuous operational control of the downstream product.

### Design

- Identify public, persisted, generated, operational, and downstream-consumed
  contracts.
- Define supported states, transitions, invariants, ownership, retention,
  operational expectations, and terminal states.
- Design compatibility, migration, and reversal before changing an observable
  contract.
- Define proportionate operational ownership, health evidence, recovery, and
  support expectations before release.
- Define the outcome and guardrail evidence that will show whether released
  software continues to meet its intended need.
- Prefer the smallest seam required by current consumers; do not introduce
  speculative lifecycle frameworks.

### Implementation

- Keep changes small, independently verifiable, and releasable where practical.
- Version public contracts and immutable releases deliberately.
- Provide deprecation warnings, context-appropriate support windows,
  compatibility readers, and migration guidance before removal.
- Preserve user-owned and downstream-owned state during generation, upgrade,
  rollback, and recovery.
- Separate substantial refactoring from behavioural change.
- Make rollback or roll-forward possible without silently corrupting or
  discarding newer state.
- Treat retirement as a planned transition covering consumers, migration,
  communications, data disposition, retained evidence, and recovery needs.

### Verification

Lifecycle evidence should cover supported and invalid transitions, repeat
operations, migrations, rollback or roll-forward, historical compatibility,
operational readiness, retention, and deletion where applicable. Feedback must
be reviewed against the declared outcome and guardrails rather than treated as
an automatic mandate. Retirement review must prove that affected consumers,
obligations, data, and restoration needs have been addressed.

### Further reading

- [Semantic Versioning](https://semver.org/)
- [Small changes from Google Engineering Practices](https://google.github.io/eng-practices/review/developer/small-cls.html)
- [Google AIP-180: Backwards compatibility](https://google.aip.dev/180)
- [UK Government guidance on retiring a service](https://www.gov.uk/service-manual/agile-delivery/retiring-your-service)

## P-005: We will use agents and automation to strengthen human judgement, not replace human responsibility

Agents and automation should extend human capability without obscuring who has
authority or who remains accountable. The ability to perform an action does
not imply permission to perform it.

Humans retain product intent and control at consequential boundaries. Agents
may clarify, investigate, propose, implement, and verify within bounded roles,
but they do not acquire ownership merely because they can complete the work.

### Design

- Assign explicit, qualified responsibilities: the Product Manager clarifies
  and synthesises; specialists own bounded assessments; the orchestrator owns
  workflow state; independent contributors verify consequential claims.
- Define trust boundaries, capabilities, data access, approval points, and
  escalation paths for every role.
- Grant the minimum filesystem, network, credential, tool, and data access
  required for the current job.
- Separate planning, decision, approval, execution, and verification where
  consequences justify it.
- Provide previews, interruption, resumption, override, and safe
  decommissioning proportionate to the work.

### Implementation

- Validate agent inputs and outputs against explicit contracts.
- Treat prompts, retrieved content, tool results, dependencies, models,
  external services, and inter-agent messages as potentially untrusted.
- Require scoped, risk-proportionate approval for irreversible, externally
  visible, privileged, financial, or sensitive-data actions.
- Preserve disagreements, assumptions, authority, decisions, tool use, and
  state changes without logging secrets or private content unnecessarily.
- Prevent an agent from approving its own consequential work or advancing past
  an independent-verification boundary.
- Isolate tenants, workspaces, memories, and credentials; bound delegation,
  retries, time, tokens, concurrency, and cost.
- Fail safely when authority, validation, or required oversight is absent.

### Verification

Threat models and abuse cases must become permission, isolation,
prompt-injection, data-exfiltration, confused-deputy, resource-limit, and
approval-boundary tests. Review must prove that each role was necessary and
qualified for its responsibility, that conflicting findings remained visible,
and that a person could understand, interrupt, and recover consequential
automation.

### Further reading

- [NIST AI Risk Management Framework Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)
- [NIST guidance on AI risk management and human-AI interaction](https://airc.nist.gov/airmf-resources/airmf/appendices/app-c-ai-risk-management-and-human-ai-interaction/)
- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)

## Enforcement model

Every rule derived from these principles must state:

1. The promise and risk it protects.
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

- What human or organisational need does this change serve, and what evidence
  distinguishes that need from an assumed solution?
- Can affected people and machines understand and correctly use it?
- What evidence proves its claims and intended behaviour?
- Are success, partial, degraded, cancelled, and failure outcomes honest and
  recoverable?
- Does it protect the people, information, and systems entrusted to it?
- Can it be changed, operated, migrated, and retired without silently breaking
  trust?
- Are agent responsibilities, authority, specialist disagreements, and human
  control explicit?
- Do documentation and examples still match reality?
- Is every exception explicit, owned, justified, and time-bounded?

## Transition from the initial principles

This revision changes the voice and organisation of the initial principles
without weakening their controls:

| Initial principle | Current treatment |
|---|---|
| P-001: Comprehension and usability come first | Expanded without changing its identifier |
| P-002: Every claim requires evidence | Expanded without changing its identifier; request evidence is also governed by new P-006 |
| P-003: Every execution is explicit, traceable, and recoverable | Principle retired; all controls remain in ES-003 under P-002, P-004, and P-005 |
| P-004: Evolution is deliberate, compatible, and reversible | Expanded without changing its identifier |
| P-005: Automation is secure, bounded, and human-governed | Expanded without changing its identifier; product security is separated into new P-007 |

P-006 adds need and request readiness. P-007 adds security and respect for the
created software. The ES-001 through ES-005 identifiers remain stable.
Standards may serve more than one principle; there is no requirement for a
one-to-one mapping.
