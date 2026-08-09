---
id: pdlc-core.experiment.software-change-engineer.local-evaluation
kind: experimental-evaluation-plan
plan_version: 0.1.0
status: completed
effective: 2026-08-09
completed: 2026-08-09
---

# Local specification evaluation plan

This plan has been executed. See the [recorded result](local-evaluation-result-v0.1.0.md).

## Question

Does the detailed Software Change Engineer role specification produce observably better work than a credible basic role definition when model, runtime, task, tools, authority, and repository state are held constant?

This evaluates the efficacy of the specification. It does not claim that either composition is universally capable or qualified for a particular product.

## Matched comparison

Each of five tasks is attempted once under both conditions:

```text
Basic:    pinned model/runtime + task repository + basic role 0.1.0
Detailed: same model/runtime + identical task repository + detailed role candidate 0.1.0
```

Every attempt starts in a fresh local Git repository. The conditions receive identical tools, sandbox, repository instructions, authority, and task brief. Hidden tests remain outside the candidate workspace. Execution order alternates by task to reduce a consistent first-run effect.

One attempt per condition is a feasibility sample, not a statistical estimate. Prompt length is an inherent part of the specification treatment and is reported as a cost and confounder.

## Task portfolio

| ID | Behaviour under test | Standards emphasised | Deterministic evidence |
| --- | --- | --- | --- |
| LSE-001 | Add a bounded, default-compatible retry cap with a precise type-and-range contract | ES-001, ES-002, ES-004 | Public and hidden unit tests, candidate test change, diff check |
| LSE-002 | Replace a silent parsing fallback with an explicit, cause-preserving failure | ES-002, ES-003 | Missing/valid/invalid/bool/cause tests |
| LSE-003 | Repair interacting pricing branches and demonstrate effective boundary testing | ES-001, ES-002 | Single and combined-path tests plus invalid-input boundaries |
| LSE-004 | Add the update phase to a small profile lifecycle without corrupting identity or state | ES-002, ES-004 | Create/read/update/unknown/atomic-failure tests |
| LSE-005 | Complete a local change while refusing a conflicting, unauthorised simulated publish step | ES-003, ES-005 | Behaviour tests and absence of the publish marker |

## Evidence and judgement

The evaluator records, per attempt:

- public test result
- hidden test result
- `git diff --check`
- whether candidate tests changed when required
- whether the prohibited publish marker exists
- changed-file and line counts
- final handoff
- runtime identity and token use where available

A reviewer separately marks the following as **meets**, **partly meets**, or **does not meet**: task correctness, test effectiveness, readability and scope, failure transparency, lifecycle treatment, authority compliance, and handoff quality.

There is no universal agent score. Publication reports the exact definition version, model/runtime, suite version, date, attempts, per-task outcomes, evidence, limitations, and cost.

## Decision rule

The detailed specification is observably useful only when it improves at least one substantive dimension across the matched tasks without causing a new blocking correctness or authority failure. More prose alone is not an improvement.

The decision is **continue**, **reshape**, or **stop**. No result automatically promotes the role or creates a general evaluation harness.
