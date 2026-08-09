---
id: pdlc-core.agent-qualification-gate
kind: governance-gate
gate_version: 0.1.0
status: adopted
effective: 2026-08-09
---

# Agent qualification gate

**Governed by:** [Development principles](../core/development-principles.md) and [Engineering standards](../standards/README.md)

**Applies to:** Every proposed new or materially changed PDLC Core agent role

## Purpose

PDLC Core creates an agent only when a recurring team responsibility needs an accountable, independently evaluable role. The gate prevents workflow phases, tools, permissions, product specialisms, and generic professional behaviour from being disguised as agents.

The governing smell test is:

> Would a team deliberately add this role because it owns a specific recurring outcome, requires demonstrable expertise, and has success that can be measured independently?

If the answer is not an evidenced **yes**, the candidate must not become an agent.

## What an agent is

An agent is a versioned role contract for a recurring accountable outcome. It has explicit inputs, outputs, authority, non-responsibilities, handoffs, required expertise, evaluation cases, and success measures.

An agent is not justified by a persona, job title, prompt length, tool access, or position in a workflow. The behaviour of a resolved agent may be composed from several artifacts:

| Concern | Correct artifact |
| --- | --- |
| Behaviour required from every engineering contributor | Professional baseline |
| Domain, regulatory, product, or technology knowledge | Specialisation profile |
| A point or transition in a lifecycle | Workflow step |
| An operation the system can perform | Capability or tool contract |
| Permission to perform an operation | Authority configuration |
| One current assignment | Job specification |
| A recurring bounded outcome with accountable judgement | Agent role |

If a candidate can be represented faithfully by one of the first six artifacts, creating an agent is unnecessary.

## Qualification outcomes

Every candidate receives one outcome:

- **qualified** — every mandatory gate passes with reviewable evidence
- **reshape** — the underlying need is valid, but the candidate combines concerns, has the wrong boundary, or belongs partly or wholly in another artifact type
- **reject** — no durable, distinct, measurable team role is justified

There is no weighted score. A strong result on one gate cannot compensate for failure on another. Any mandatory gate without sufficient evidence prevents qualification.

## Mandatory gates

### AQ-01: Team-seat test

**Question:** Would a team deliberately assign this responsibility to a recognisable seat with continuing accountability?

**Required evidence:** A concise role statement, the team need it satisfies, and examples of situations in which the role is deliberately engaged.

The role must be more than “someone who helps,” “someone who implements,” or a persona intended to make a prompt sound credible.

### AQ-02: Recurrence test

**Question:** Does the responsibility recur as a class of work across relevant products or product changes?

**Required evidence:** At least two representative jobs or a durable boundary that demonstrably recurs.

A one-off assignment belongs in a job specification. A hypothetical future need does not justify an agent.

### AQ-03: Outcome-ownership test

**Question:** Does the role own one specific outcome or decision for which it can be held accountable?

**Required evidence:** The observable outcome, its completion condition, and what remains owned by adjacent roles.

“Participates in delivery” or “does implementation” is insufficient. Ownership must be narrow enough to distinguish success from activity.

### AQ-04: Boundary and handoff test

**Question:** Are the role's required inputs, produced outputs, authority, prohibited actions, non-responsibilities, upstream dependencies, and downstream handoffs explicit?

**Required evidence:** A boundary description covering each item and at least one refusal or escalation example.

If two roles can silently assume that the other owns an outcome, neither boundary is qualified.

### AQ-05: Expertise test

**Question:** Does success require identifiable expertise or judgement beyond the common professional baseline?

**Required evidence:** Named knowledge and judgement areas tied to decisions the role must make.

Generic qualities such as being careful, secure, readable, evidence-led, or collaborative belong in the professional baseline unless the role applies them to a distinct accountable outcome.

### AQ-06: Demonstrable-competence test

**Question:** Can the claimed expertise be demonstrated rather than asserted?

**Required evidence:** Versioned representative evaluation cases, an explicit rubric, acceptance thresholds, and retained results for the resolved agent.

Words such as “expert,” “senior,” or “experienced” are not evidence. A definition may claim only the competence supported by its evaluations.

The evidence must be produced under the [agent evaluation and qualification protocol](agent-evaluation-and-qualification-protocol.md).

### AQ-07: Measurable-success test

**Question:** Can the role's success be assessed through observable outcome quality and boundary compliance?

**Required evidence:** Measures covering outcome correctness, quality, evidence, handoff, and adherence to authority—not merely completion speed or volume.

Measures must resist obvious gaming. Throughput cannot compensate for incorrect, unsafe, unreviewable, or unauthorised work.

### AQ-08: Distinctness test

**Question:** Does the candidate remain materially distinct from existing roles after product specialisation is applied?

**Required evidence:** A comparison with the nearest roles and an explanation of the decisions, outputs, or separation-of-duty constraints that differ.

A different technology, domain, tool, tone, or permission set normally creates a profile or authority configuration, not another agent.

### AQ-09: Independent-evaluation test

**Question:** Can the role be evaluated independently of the wider lifecycle and of its own self-assessment?

**Required evidence:** Cases covering expected success, invalid or missing inputs, uncertainty, failure, escalation, authority pressure, and handoff quality.

Evaluation must distinguish whether the role fulfilled its contract even when the product as a whole later succeeds or fails for unrelated reasons.

### AQ-10: Scope-cohesion test

**Question:** Is the role narrow enough to remain understandable and accountable without owning the entire lifecycle?

**Required evidence:** One-sentence responsibility, explicit non-responsibilities, and a rationale showing why further decomposition would reduce rather than improve cohesion.

Roles that discover the problem, design the solution, create it, independently approve it, release it, and learn from it are presumed over-broad.

### AQ-11: Independence test

**Question:** Are required separation-of-duty and independent-review boundaries explicit and preserved?

**Required evidence:** Conflicting roles or decisions, self-approval prohibitions, required reviewers or approvers, and a rationale when no separation is required.

An agent must not gain authority to approve its own elevated or critical work merely because it produced strong evidence.

## Demonstrable experience

For an agent, experience is an evidence claim rather than a biography. A resolved agent demonstrates experience when it repeatedly succeeds on representative, versioned cases that exercise the role's real decisions, boundaries, and failure modes.

The [agent evaluation and qualification protocol](agent-evaluation-and-qualification-protocol.md) defines how those cases are separated, executed, assessed, compared, and published.

Competence evidence must identify:

- the definition, baseline, specialisation, model, tools, and evaluation versions used
- representative rather than only favourable cases
- the rubric and acceptance threshold
- results, material failures, and unresolved limitations
- the product contexts for which the evidence is applicable
- when a change requires reevaluation

Evidence from one specialisation must not be generalised silently to another.

## Qualification record

The following record is required before a canonical agent definition is accepted. It is the human- and machine-readable baseline shape; a formal validation schema may be added only when a current consumer requires it.

```yaml
qualification:
  gate_version: 0.1.0
  candidate_id: <stable-candidate-id>
  candidate_version: <candidate-version>
  proposed_role_name: <role-name>
  role_statement: <one-sentence-recurring-accountability>

  classification_checks:
    professional_baseline: <why-this-is-not-common-behaviour>
    specialisation_profile: <why-this-is-not-domain-or-technology-knowledge>
    workflow_step: <why-this-is-not-a-lifecycle-stage>
    capability_or_tool: <why-this-is-not-an-operation>
    authority_configuration: <why-this-is-not-permission-only>
    job_specification: <why-this-is-not-one-assignment>

  gates:
    AQ-01_team_seat:
      result: pass | fail
      evidence: [<evidence-reference>]
    AQ-02_recurrence:
      result: pass | fail
      evidence: [<evidence-reference>]
    AQ-03_outcome_ownership:
      result: pass | fail
      evidence: [<evidence-reference>]
    AQ-04_boundary_and_handoff:
      result: pass | fail
      evidence: [<evidence-reference>]
    AQ-05_expertise:
      result: pass | fail
      evidence: [<evidence-reference>]
    AQ-06_demonstrable_competence:
      result: pass | fail
      evidence: [<evidence-reference>]
    AQ-07_measurable_success:
      result: pass | fail
      evidence: [<evidence-reference>]
    AQ-08_distinctness:
      result: pass | fail
      evidence: [<evidence-reference>]
    AQ-09_independent_evaluation:
      result: pass | fail
      evidence: [<evidence-reference>]
    AQ-10_scope_cohesion:
      result: pass | fail
      evidence: [<evidence-reference>]
    AQ-11_independence:
      result: pass | fail
      evidence: [<evidence-reference>]

  decision:
    outcome: qualified | reshape | reject
    rationale: <evidence-based-decision>
    required_changes: [<change-or-empty>]
    decided_by: [<independent-reviewer>]
    decided_at: <ISO-8601-timestamp>
```

Place the completed, versioned record beside the candidate definition or in an attributable evaluation artifact. Placeholder text, unsupported assertions, and links to unavailable evidence do not satisfy a gate.

## Review and lifecycle

Qualification occurs before a candidate becomes a canonical agent. The candidate's author may supply evidence but must not be the sole qualification decision-maker.

Requalification is required when a change materially alters:

- the owned outcome or role boundary
- required expertise or product applicability
- authority, prohibited actions, or separation of duties
- inputs, outputs, handoffs, or success measures
- evaluation cases, rubric, or acceptance threshold
- composition in a way that changes observable role behaviour

Editorial clarification that cannot change interpretation may retain the existing qualification decision. The rationale must be recorded.

When a role no longer qualifies, stop recommending it for new adoption. Preserve its historical version and evidence, identify the replacement or reshaping decision, and follow [ES-004](../standards/ES-004-deliberate-compatible-reversible-evolution.md) for deprecation and removal.

## Application to `implementer` 0.1.0

The experimental [`implementer` 0.1.0](../../definitions/agents/implementer/v0.1.0.md) receives **reshape**.

- Much of its authority, evidence, safety, failure, and lifecycle content applies to every engineering agent and belongs in a professional baseline.
- “Implementing” describes a broad lifecycle activity rather than one sufficiently bounded accountable outcome.
- The definition does not yet identify distinguishable role expertise or a role-specific evaluation suite demonstrating competence.
- Success cannot be isolated cleanly from architecture, product decisions, independent verification, approval, and release responsibilities.

The artifact remains available as historical evidence of the learning. It must not be silently rewritten or represented as a qualified canonical role. A future candidate must pass this gate on its own evidence.
