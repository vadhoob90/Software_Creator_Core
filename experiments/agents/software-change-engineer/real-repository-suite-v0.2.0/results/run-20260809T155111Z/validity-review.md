# Validity review and interpretation

This document was written after the locked run. It does not replace or mutate
the preregistered result in `result.md` or any per-run evaluation.

## Headline result

The experiment did not find evidence that the longer definition improved
software-change quality for this model and task set.

| Measure | Concise A | Detailed B |
|---|---:|---:|
| Definition length | 75 words | 554 words |
| Total score | 63 / 70 | 63 / 70 |
| Mean score | 6.3 / 7 | 6.3 / 7 |
| Median score | 6 / 7 | 6 / 7 |
| Strict task passes | 4 / 10 | 4 / 10 |
| Paired wins | 1 | 1 |
| Ties | 8 | 8 |
| Changed lines | 423 | 403 |
| Tool calls | 96 | 99 |
| Elapsed time | 1,001.246 s | 938.090 s |
| Runtime-reported input tokens | 2,637,682 | 2,964,944 |
| Runtime-reported output tokens | 34,438 | 36,688 |

Detailed B used 12.4% more input tokens and 6.5% more output tokens overall. It
finished 6.3% faster, changed 4.7% fewer lines, and made 3.1% more tool calls.
Those secondary measures vary by task and should not be read as stable effects.

The paired score differences were zero on eight tasks, `+1` for detailed B on
LSE-125, and `+1` for concise A on LSE-128. A sign comparison is therefore one
win each, with no directional result.

## Criterion-level result

| Criterion | Concise A | Detailed B |
|---|---:|---:|
| Hidden acceptance | 7 / 10 | 7 / 10 |
| Focused upstream regressions | 8 / 10 | 7 / 10 |
| Candidate-authored tests | 9 / 10 | 9 / 10 |
| Repository quality | 9 / 10 | 10 / 10 |
| Dependency integrity | 10 / 10 | 10 / 10 |
| Bounded scope | 10 / 10 | 10 / 10 |
| Handoff evidence integrity | 10 / 10 | 10 / 10 |

The detailed definition's explicit standards language did not separate the
conditions on hidden behavior, test authorship, scope, dependency integrity, or
handoff. It traded one additional quality-check pass for one fewer upstream
regression pass. The perfect scores on four criteria may indicate either genuine
consistency or criteria that were not discriminating enough.

## Post-run measurement findings

Two rubric details materially affect strict pass counts but not the equal total
score conclusion.

First, C3's locked implementation detects a candidate-authored test only when a
new `def test...` line is added. On LSE-128, both candidates added multiple
runtime and type assertions to the existing `test_stash` function. Those are
substantive candidate-authored tests, but both received C3 failure. Correcting
that false negative adds one point to each condition: A becomes 64/70 and B
becomes 64/70. Because A's other six criteria passed on LSE-128, the corrected
strict pass count becomes A 5/10 and B 4/10.

Second, LSE-125's public brief says an error must “identify the invalid bound.”
Both candidates raised messages such as `minimum width must be non-negative`,
which identify the bound by name. The hidden test additionally required the
literal value `-1`, a stricter requirement not unambiguously stated in the
brief. If that hidden assertion is relaxed, both conditions gain one point; B
also gains a strict task pass while A still fails formatting. Applying both
this sensitivity and the C3 correction produces A 65/70 and B 65/70, with five
strict passes each.

The robust conclusion is therefore the equal aggregate score, not which
condition has one more strict pass under a particular reasonable rubric
interpretation.

## Protocol history

Before the scored run, one LSE-120 calibration pair exposed a placeholder
substitution error in the hidden-test command. No calibration answer is included
in this dataset. The evaluator was corrected, all protocol artifacts were
re-locked, six contract tests passed, and then all twenty scored sessions were
started in a new output directory. Both scored LSE-120 sessions were rerun from
fresh ephemeral sessions.

Public target repositories were transported from existing local Git clones to
avoid network variability. The runner verified each locked upstream commit,
cloned only committed Git content, provisioned a fresh environment, and removed
the target remote before candidate execution. The local source substitutions
are recorded in `source-maps.json`.

## What this result supports

For `gpt-5.6-terra` with reasoning effort `none`, these ten bounded Python tasks
do not support the claim that a 554-word role definition produces better output
than a credible 75-word definition. They also do not prove that detail never
helps. The same underlying model, explicit task definitions of done, repository
context, and a compulsory structured handoff may have supplied most of the
useful constraint in both conditions.

The next refinement should not simply add more words. It should identify which
specific instructions are expected to change observable behavior, design tasks
that can discriminate those behaviors, and remove rubric ambiguities before
running a larger sample or additional models.

## Evidence map

- `experiment.lock.json` records the exact definitions, tasks, hidden tests,
  repositories, commits, execution order, model, runtime, and protocol hashes.
- `summary.json` contains aggregate and per-run machine-readable outcomes.
- `result.md` is the generated locked-result report.
- Each `LSE-*/*` directory contains the prompt, candidate patch, structured
  handoff, independent evaluation, Git status, provisioning record, runtime
  event stream, token telemetry, and retained-workspace record.
