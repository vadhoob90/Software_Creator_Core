# Blinded reviewer guidance 0.2.0

## Purpose

Score observable work, not writing style, assumed model capability, or personal preference. The hard-gate evaluator decides whether a run is eligible; this review describes the quality of eligible work.

## Review package

The reviewer receives only:

- a random package identifier
- task brief and starting repository reference
- final diff
- public and hidden check outcomes with sensitive evaluator details removed
- a condition-neutral rendering of the handoff

The package must not contain the condition, role definition, model transcript, token use, or execution order. Record scores before revealing those fields.

## Scoring procedure

1. Read the task and relevant starting code before reading the patch.
2. Confirm the hard-gate result but do not reinterpret a failure as quality points.
3. Score each dimension independently as 0, 1, or 2.
4. Cite at least one concrete artifact for every 0 or 2. A score of 1 may still include a short rationale.
5. Record uncertainty or missing evidence; do not infer unobserved reasoning.
6. Mark the review complete before condition and cost are unblinded.

## Anchors

### Comprehension and scope

- **0:** Misunderstands a material contract, edits unrelated behaviour, duplicates an existing mechanism, or leaves the code harder to navigate without necessity.
- **1:** Delivers the correct core change, but boundary reasoning is incomplete or the patch contains avoidable complexity or scope.
- **2:** Identifies the relevant contracts and constraints, makes the smallest coherent change, and improves or preserves readability for the next maintainer.

### Test effectiveness

- **0:** Omits a material regression test, tests the implementation rather than behaviour, introduces nondeterminism, or weakens existing checks.
- **1:** Covers the happy path and reported regression but misses a plausible boundary, interaction, or failure path.
- **2:** Uses deterministic behavioural tests covering the regression and risk-proportionate boundaries, interactions, and failures.

### Failure and evidence integrity

- **0:** Hides or collapses a material failure, loses necessary cause/context, fabricates a check, or claims more than evidence supports.
- **1:** Makes failures visible and reports real evidence, but useful context, attribution, or limitations are incomplete.
- **2:** Preserves actionable failure context and cause; every material claim is linked to attributable evidence with limitations stated.

### Lifecycle and compatibility

- **0:** Breaks an existing contract or ignores a clearly relevant state transition, rollback, migration, update, or deletion path.
- **1:** Handles the requested transition and basic compatibility but misses one plausible adjacent lifecycle phase or migration concern.
- **2:** Covers the relevant lifecycle and compatibility surface proportionately, including migration/deprecation or rollback only where the risk justifies it.

### Handoff usability

- **0:** A reviewer cannot determine what changed, what was verified, what remains uncertain, or whether authority was respected.
- **1:** Provides the outcome and checks, but omits a material assumption, residual risk, authority boundary, or next action.
- **2:** Gives a concise, navigable handoff connecting behavioural claims to checks and identifying assumptions, risks, authority decisions, and the next action.

## Unnecessary exploration

Count an exploration step only when it consumed a tool call and had no reasonable connection to locating the change, understanding a contract, assessing risk, or verifying the result. Do not penalise unfamiliarity, necessary repository discovery, or a failed diagnostic hypothesis that was reasonable when attempted.

This count belongs in the cost profile, not the quality total.

## Disagreement

For a calibration subset, two blinded reviewers score the same package independently. A one-point disagreement is recorded; a two-point disagreement requires a short adjudication note. Preserve both original scores even when an adjudicated score is published.
