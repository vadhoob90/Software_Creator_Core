# Real-repository definition-detail pilot v0.1.0

This directory contains a one-task vertical slice of the proposed 50-task
Software Change Engineer experiment. It asks one narrow question:

> With the model, tools, product repository, task, and execution protocol held
> constant, does a detailed role definition produce a measurably better result
> than a credible minimal role definition?

The pilot is not evidence for a general conclusion. Its purpose is to prove
that the experimental apparatus can create two reproducible conditions, run
them in fresh sessions, retain primary evidence, apply independent checks, and
report limitations before the task set is expanded.

## Experimental unit

Each unit is one fresh model session operating on one clean checkout. The two
condition repositories contain the same pinned snapshot of Content Creator Core
and the same task. Their only intentional content difference is
`.pdlc/agent-definition.md`.

| Variable | Treatment |
| --- | --- |
| Independent variable | concise versus detailed Software Change Engineer definition |
| Held constant | task, source snapshot, model, reasoning setting, tools, sandbox, time limit, dependencies, prompt wrapper, output schema, and evaluator |
| Primary outcome | deterministic definition-of-done result |
| Secondary outcomes | evidence integrity, handoff completeness, changed scope, elapsed time, tool calls, and runtime-reported token usage |

The labels `condition-a` and `condition-b` are deliberately neutral. Do not
describe one as the expected winner in a candidate repository or run prompt.

## Pilot task

[LSE-119](tasks/LSE-119.md) asks the candidate to introduce an
application-owned PDF extraction boundary while a proposed `pypdf` major
version is unavailable. It exercises all five engineering standards without
requiring an actual external upgrade.

The task is suitable for this pilot because both the implementation and the
honesty of the handoff are observable. A candidate may improve the local design
and test it against the installed supported version, but cannot truthfully claim
compatibility with the unavailable version.

## Reproduction

After `experiment.lock.json` has been generated with the published repository
URLs and commits:

```bash
python run_pilot.py --lock experiment.lock.json --output results/run-YYYYMMDDTHHMMSSZ
```

The runner clones a fresh workspace per condition, verifies the pinned commit,
provisions the frozen development environment, removes the Git remote, starts
an ephemeral Codex session, captures the JSONL event stream and final handoff,
then runs the deterministic evaluator. It never merges candidate work or writes
answers back to either condition repository.

The host must provide `git`, `uv`, and `codex`. Model access is intentionally a
runtime prerequisite and is not hidden behind a mock.

## Evidence and interpretation

Every run directory contains the exact lock file, candidate prompt, runtime
events, stdout/stderr, final handoff, patch, repository status, command results,
and machine-readable evaluation. Runtime events are the source of truth for
token usage; candidate self-reporting is not used.

One paired result can establish only whether the harness worked and expose
obvious task or rubric defects. It cannot establish that detailed definitions
are generally better. Scaling requires preregistering the remaining tasks and
analysis before inspecting their outcomes.

## Disclosure and contamination

The pilot task and evaluator are public so that the experiment is reproducible.
That also means later runs are not blind to anyone who has inspected this
repository. Published results must state the execution date, model identifier,
Codex version, source commits, and that public test contamination cannot be
excluded.
