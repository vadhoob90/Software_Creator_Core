# One-task pilot result

## Outcome

The vertical slice worked end to end: two public condition repositories were
created from the same product snapshot, an identical issue was published to
each, both candidates ran in fresh sessions without Git remotes, and the runner
retained runtime events, handoffs, patches, command evidence, and deterministic
evaluation.

The single observed pair does **not** support the hypothesis that the detailed
definition produces a better result. Condition A, the concise definition,
passed all 7 definition-of-done criteria. Condition B, the detailed definition,
passed 6 of 7. This is a pilot observation, not a general conclusion.

## Recorded conditions

| Property | Condition A | Condition B |
| --- | ---: | ---: |
| Definition size | 75 words / 628 bytes | 554 words / 4,271 bytes |
| Model | `gpt-5.6-terra` | `gpt-5.6-terra` |
| Candidate return code | 0 | 0 |
| Deterministic criteria | 7/7 | 6/7 |
| Primary pass | yes | no |
| Full test suite | pass, 557 tests | pass, 558 tests |
| Independent mypy | pass | pass |
| Independent Ruff lint | pass | fail: one 101-character test line |
| Changed paths | 4 | 3 |
| Changed lines | 82 | 126 |
| Completed tool calls | 11 | 13 |
| Elapsed candidate time | 202.276 s | 185.436 s |
| Runtime input tokens | 447,825 | 462,271 |
| Cached input tokens | 404,480 | 416,768 |
| Runtime output tokens | 5,305 | 6,250 |

Runtime token values are copied from each `turn.completed` event. They are not
candidate estimates. Prices are not applied because the experiment did not
lock a pricing schedule.

## What both candidates demonstrated

Both candidates:

- introduced an application-owned PDF boundary and delegated ingestion to it
- preserved the current supported-version behaviour and passed the full test
  suite
- tested the missing-dependency path and preserved the original `ImportError`
  in the exception chain
- left `pyproject.toml` and `uv.lock` unchanged
- explicitly identified `pypdf` 7 compatibility as unavailable, unverified,
  and deferred
- avoided commits, network actions, fake packages, and fabricated upgrade
  evidence

These results show that the task is solvable and does discriminate more than
functional correctness alone.

## Why Condition B failed

Condition B added a test line of 101 characters where the repository maximum is
100. The candidate ran focused and full tests but did not run Ruff, declared no
failed checks, and returned `outcome: success`. The independent evaluator ran
the repository's available lint command and found the error.

That failure is relevant to the experiment rather than evaluator noise: the
task required relevant available checks to pass or be identified precisely,
and the detailed definition explicitly called for available static evidence
and honest reporting of unrun checks.

Condition B also produced 54% more changed lines, 18% more completed tool calls,
3% more input tokens, and 18% more output tokens. It finished 8% faster. With
one pair, none of these differences can be separated from normal sampling
variation.

## Post-run harness audit

The pilot exposed two apparatus defects that must be fixed before expansion:

1. The initial telemetry parser counted both the start and completion event for
   each tool call. The stored records and summary now report completed events
   once (11 and 13). The raw JSONL is unchanged and the correction is recorded
   in each machine-readable record.
2. The original lock file hashed the task, definitions, and handoff schema, but
   not the runner and evaluator. The exact executed files have therefore been
   archived under `executed-protocol/` with SHA-256 hashes. The runner has been
   revised to archive its protocol automatically and can verify protocol hashes
   supplied by future lock files.

The post-pilot evaluator also adds the repository's Ruff formatting check for
future runs. This did not alter the sealed primary result above. The exact
evaluator used for this run remains in `executed-protocol/evaluate_pilot.py`.

## Limits on interpretation

- There is one task, one run per condition, and one product repository.
- Model outputs are stochastic; no repeat-run variance has been measured.
- The execution order was fixed, so elapsed time may include order and cache
  effects even though model sessions and workspaces were isolated.
- The public task and definitions make reproduction possible but cannot exclude
  prior exposure or benchmark contamination.
- `gpt-5.6-terra` and the Codex version are recorded, but an immutable provider
  backend snapshot is not available to this harness.
- The deterministic score measures the visible definition of done. No blinded,
  independent subjective review was performed in this pilot.

## Scale decision

The experiment is ready to move beyond one task only after a new lock includes
the corrected runner and evaluator hashes. A larger suite should preserve the
raw 7-point task score alongside the pass threshold, randomise or counterbalance
condition order, and preregister any cross-task statistical analysis before the
remaining outcomes are inspected.
