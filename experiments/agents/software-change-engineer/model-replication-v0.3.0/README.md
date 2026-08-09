# Cross-model definition replication

This experiment repeats the ten-task Software Change Engineer A/B suite with a
different model. It tests whether the effect of a concise versus detailed role
definition changes when the candidate model changes.

The replication holds constant:

- the ten public task definitions;
- five target repositories and pinned commits;
- concise A and detailed B role definitions;
- tool access, sandbox, authority, reasoning effort, and timeout;
- execution order and structured handoff schema; and
- seven-point independent evaluation.

The candidate model is the only runtime treatment change:

| Run | Model |
|---|---|
| Original | `gpt-5.6-terra` |
| Replication | `gpt-5.6-sol` |

## Prospective evaluator correction

The original run and pre-run calibration exposed three scoring weaknesses. They are corrected and locked
before any Sol candidate is run:

1. assertions added to an existing test function count as candidate-authored
   tests; and
2. LSE-125 requires the error to identify the invalid bound by name, but does
   not require the message to repeat the literal rejected value; and
3. an otherwise successful task may honestly report a failed broader check.
   The handoff criterion rewards transparent reporting, while independent
   criteria decide whether acceptance, regression, and quality checks pass.

The saved Terra patches are rescored under this evaluator so the cross-model
comparison uses one scoring contract. Original locked scores remain unchanged
and auditable in the v0.2.0 result directory.

## Primary analysis

For each model, calculate the paired detailed-minus-concise score across the ten
tasks. The model-definition interaction is:

```text
(Sol detailed - Sol concise) - (Terra detailed - Terra concise)
```

Secondary measures are strict task pass rate, criterion pass rates, elapsed
time, changed lines, tool calls, and runtime-reported token use. Results are
descriptive because ten task pairs do not establish broad model-independent
causality.

## Isolation

Each candidate receives a fresh target checkout at the pinned commit. The
runner adds only its role definition and public task, provisions dependencies,
removes the Git remote, and starts a fresh ephemeral session without candidate
network access. Candidate changes are captured before the independent check is
run and are never pushed upstream.
