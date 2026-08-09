# Validity and protocol review

## What was held constant

The Sol replication used the same ten public tasks, pinned repository commits,
concise and detailed definitions, execution order, tools, sandbox, authority,
timeout, reasoning effort, structured handoff, and seven evaluation criteria as
the Terra run. The candidate model was the sole planned runtime change.

Every candidate received a fresh checkout. The runner removed its Git remote
before execution, and no candidate patch was pushed to any target repository.
The saved source maps identify the local source clone and pinned commit used for
each task.

## Evaluator correction and calibration

The v0.2.0 evaluator had three defects that could change a score without
changing patch quality:

1. it did not count substantive assertions added to an existing test function
   as candidate-authored tests;
2. LSE-125 over-specified an error message by requiring the rejected literal,
   although the task required identification of the invalid bound; and
3. it penalised an honest successful handoff that reported a failed broader
   check, even when the independently selected acceptance, regression, and
   quality checks passed.

The first two corrections were identified from the original run. The third was
identified during a pre-run calibration attempt. That calibration was stopped
and excluded from all reported scores. The correction was then recorded in the
manifest and lock, the full Sol run was restarted with fresh sessions, and all
saved Terra patches were rescored with the same final evaluator. The original
v0.2.0 locked scores remain unchanged.

This ordering prevents the final Sol outcomes from selecting the correction,
but the correction was not fully prospective to the first calibration sample.
That is a limitation and is disclosed here rather than treating the calibration
as part of the experiment.

## Result

| Model | Concise A | Detailed B | Difference | Strict passes A/B |
|---|---:|---:|---:|---:|
| `gpt-5.6-terra` | 65/70 | 65/70 | 0 | 5/10 · 5/10 |
| `gpt-5.6-sol` | 64/70 | 68/70 | +4 | 5/10 · 8/10 |

For Sol, detailed B won four task pairs and lost none; six tied. The exact
two-sided sign-test p-value is 0.125. Three tasks passed strictly only under B,
and none passed only under A; the exact paired strict-pass p-value is 0.25.
These are directional observations, not conventionally significant results.

The Sol difference came primarily from focused upstream regressions (7/10 for
A and 10/10 for B) and one additional hidden acceptance pass (7/10 and 8/10).
Detailed B used 3.2% more input tokens, 5.8% more output tokens, and 4.5% more
candidate time, while making 2.6% fewer tool calls and changing 10.4% fewer
lines.

## Claims this evidence supports

- Definition efficacy cannot be treated as independent of the underlying model
  on the evidence from this task block.
- The detailed definition was associated with better Sol results in this run.
- More detail did not improve Terra's aggregate score in the same tasks.

## Claims this evidence does not support

- That detailed definitions generally improve software-engineering agents.
- That Sol will reproduce the four-point effect on another stochastic run.
- That the difference was caused by any single clause in the detailed
  definition.
- That either model is broadly more capable; this experiment estimates the
  definition effect, not general model quality.

There was one stochastic run per task, condition, and model, with only ten task
pairs. Repeated runs and/or a new preregistered task block are required to
estimate variance and test whether the interaction persists.

## Evidence map

- `terra-rescore-20260809T155111Z/` contains the corrected Terra evaluations
  reconstructed from the original saved candidate patches.
- `sol-run-20260809T165556Z/` contains all twenty fresh Sol sessions and their
  independent evaluations.
- `comparison-20260809/comparison.json` is the machine-readable cross-model
  comparison.
- `comparison-20260809/analysis.md` is the generated human-readable analysis.
- `evidence-sha256.txt` authenticates the published result files.
