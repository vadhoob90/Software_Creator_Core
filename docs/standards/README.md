# Engineering standards

**Status:** Adopted initial baseline  
**Effective:** 9 August 2026  
**Derived from:** [Development principles](../core/development-principles.md)

Engineering standards are the second layer of PDLC Core governance. The principles explain why the system is built in a particular way; these standards state what must be true in design, implementation, and verification.

The standards are intentionally independent of any agent, programming language, or CI provider. Humans, agents, linters, test harnesses, reviewers, and release gates must all apply the same requirements.

## Standards catalogue

| ID | Standard | Governing principles |
|---|---|---|
| ES-001 | [Comprehension and usability](ES-001-comprehension-and-usability.md) | P-001: People and machines can understand and use |
| ES-002 | [Evidence and testing](ES-002-evidence-and-testing.md) | P-002: Works—and we prove it; P-006: Understand the need |
| ES-003 | [Explicit, traceable, and recoverable execution](ES-003-explicit-traceable-recoverable-execution.md) | P-002: Works—and we prove it; P-004: Evolves without losing trust; P-005: Human responsibility |
| ES-004 | [Deliberate, compatible, and reversible evolution](ES-004-deliberate-compatible-reversible-evolution.md) | P-004: Evolves without losing trust |
| ES-005 | [Secure, bounded, and human-governed automation](ES-005-secure-bounded-human-governed-automation.md) | P-005: Human responsibility; P-007: Secure and respectful software |
| ES-006 | [Secure and respectful software](ES-006-secure-and-respectful-software.md) | P-007: Secure and respectful software |

A principle may govern more than one standard, and a standard may serve more
than one principle. Applicability is determined by the affected artifacts,
lifecycle operations, trust boundaries, and risks—not solely by the role
performing the work.

## Normative language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHOULD**, **SHOULD NOT**, and **MAY** describe requirement strength:

- **MUST** and **MUST NOT** are release requirements.
- **SHOULD** and **SHOULD NOT** require either compliance or a recorded reason for deviation.
- **MAY** identifies an allowed option, not a requirement.
- A rule marked **review** requires explicit human or independent-agent judgement.
- A rule marked **automated** is intended to be measured mechanically.

## Enforcement maturity

Every control must declare its actual enforcement state:

1. **Documented** — the rule exists and is applied through review.
2. **Measured** — automation reports the result but does not block.
3. **Blocking** — automation prevents acceptance when the rule fails.
4. **Exception** — a temporary, approved deviation is active.

A documented control MUST NOT be described as automated, and a measured control MUST NOT be described as blocking. Until an enforcement harness exists, all controls in this catalogue are **documented** unless a standard says otherwise.

## Common applicability

These standards apply to:

- Product requests, briefs, feasibility assessments, syntheses, and commitment
  decisions when a PDLC workflow governs them.
- Hand-authored source code and configuration.
- Prompts, agent definitions, routing rules, and tool policies.
- Schemas, commands, APIs, and public contracts.
- Generated artifacts for which PDLC Core is responsible.
- Tests, fixtures, migrations, release automation, and enforcement code.
- Applicable operational-readiness, outcome, deprecation, and retirement
  artifacts.
- Documentation that defines expected behaviour.

Vendored, generated, or experimental material may be excluded from a particular metric only when the boundary and reason are explicit. Exclusion from a metric does not exclude the material from security, lifecycle, or behavioural requirements.

## Risk classification

Controls may vary according to consequence:

- **Standard:** failure is local, reversible, and does not cross a sensitive boundary.
- **Elevated:** failure can corrupt persisted state, break downstream consumers, expose private data, invoke an external side effect, or cause material operational cost.
- **Critical:** failure can bypass authority, cause irreversible or financial action, compromise security, alter release integrity, or affect many downstream consumers.

When classifications conflict, the highest applicable risk governs. A change to classification requires the same review as a change to the corresponding control.

## Evidence package

A completed change must make its evidence discoverable. As applicable, the evidence package includes:

- The standards and controls applied.
- Design decisions and unresolved risks.
- Static-analysis and test results.
- Coverage and mutation results.
- Compatibility, migration, recovery, and security results.
- Provenance for material generated or released artifacts.
- Review decisions and active exceptions.

The implementer may assemble evidence but MUST NOT be the sole authority deciding that elevated or critical work is compliant.

## Exceptions

An exception is permitted only when literal compliance would create disproportionate harm and the governing principle remains protected by compensating controls.

Every exception MUST include:

- Control identifier.
- Affected scope.
- Concrete rationale.
- Risk and compensating controls.
- Accountable owner.
- Approval record.
- Expiry date or removal condition.
- Tracking item for remediation.

Exceptions MUST be visible in review and CI output. Permanent exceptions require changing the standard instead of repeatedly extending a waiver.

## Baselines and ratchets

Numeric thresholds are safety floors, not definitions of quality. A green baseline must be recorded when measurement is introduced. Future changes MUST NOT weaken that baseline or a fixed minimum without an approved standards change.

Threshold changes require:

- Evidence that the metric predicts a relevant risk.
- Impact analysis against representative repositories or artifacts.
- A migration plan when existing consumers would fail.
- A versioned change to this catalogue.

## Ownership and change process

Engineering standards are versioned product contracts. Changes must be small, reviewed, and traceable to a principle or observed failure.

A standards change must state:

- Why the current rule is insufficient.
- Whether it tightens, relaxes, or clarifies behaviour.
- Which controls, agents, templates, or consumers are affected.
- How adoption and rollback work.
- What evidence will show that the change improved outcomes.

## Further reading

- [Development principles](../core/development-principles.md)
- [RFC 2119 requirement language](https://www.rfc-editor.org/rfc/rfc2119)
- [Google Engineering Practices: what to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
