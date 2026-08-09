---
id: pdlc-core.experiment.software-change-engineer
kind: agent-experiment
experiment_version: 0.1.0
status: active
started: 2026-08-09
completed: 2026-08-09
---

# Software Change Engineer experiment

## Question

Does the detailed Software Change Engineer specification produce more correct, verifiable, standards-aligned work than a credible basic specification when everything else is held constant?

This experiment deliberately tests specification efficacy before PDLC Core creates runtime capability passports, a model matrix, a benchmark registry, or a canonical agent definition.

## Experimental composition

```text
same local task repository + same task + same model/runtime
├── credible basic role 0.1.0
└── detailed role candidate 0.1.0
```

Five self-contained synthetic repositories exercise different parts of the role. Evaluator-owned hidden tests remain outside each candidate workspace. No downstream product code, knowledge, or CI is imported.

That synthetic 0.1.0 comparison is complete. A public real-repository pilot now
tests the apparatus needed for a planned 50-task comparison; it does not change
the recorded synthetic result.

## Artifacts

1. [Role candidate](role-candidate-v0.1.0.md)
2. [Basic control role](basic-role-v0.1.0.md)
3. [Local evaluation plan](local-evaluation-plan-v0.1.0.md)
4. [Local task suite and evaluator](local-suite-v0.1.0/README.md)
5. [Local evaluation result](local-evaluation-result-v0.1.0.md), with attributable per-attempt JSON and patches

### Version 0.2.0 in progress

1. [Twenty-task evaluation protocol](local-evaluation-protocol-v0.2.0.md)
2. [Task matrix, reviewer guidance, schemas, and validators](local-suite-v0.2.0/README.md)

The earlier twenty-task design remains useful input, but it is not the active
execution plan. The [one-task real-repository pilot](real-repository-pilot-v0.1.0/README.md)
holds the product repository, task, model, tools, and runtime constant while
varying only the deployed definition. Its [sealed result](real-repository-pilot-v0.1.0/results/run-20260809T145232Z/result.md)
validates the vertical slice and records the harness defects found before
scaling.

The 50-task comparison has not started. Task construction, protocol hashing,
order randomisation, and statistical analysis must be preregistered before its
outcomes are inspected.

## Version 0.1.0 deliberate limits

- One basic and one detailed role definition.
- Five small synthetic task repositories.
- One pinned model/runtime.
- One execution per condition and task.
- Standard-library public and hidden tests plus a small review rubric.
- Local orchestration only; no downstream repositories or remote CI.

These limits make the experiment unsuitable for formal qualification under the [agent evaluation and qualification protocol](../../../docs/agents/agent-evaluation-and-qualification-protocol.md). They are sufficient to test whether the approach produces useful evidence at a maintainable cost.

## Version 0.1.0 decision

**Reshape.** Both conditions passed all five deterministic task gates. The detailed definition produced more consistent lifecycle and evidence handoffs but consumed approximately 51% more model tokens without changing an outcome. Retain that useful discipline in a materially shorter candidate before testing again.

No agent definition is promoted automatically. Promotion requires a separate [agent qualification gate](../../../docs/agents/agent-qualification-gate.md) record and formal evidence.
