# Ten-task real-repository suite

This experiment tests whether a detailed Software Change Engineer role
definition produces better work than a credible concise definition when every
other controlled input is held constant.

It extends the one-task pilot with ten paired tasks across five mature public
Python repositories. Content Creator Core is not a target in this suite.

| Repository | Tasks | Capability emphasis |
|---|---|---|
| `psf/requests` | LSE-120–121 | atomic updates and explicit failure |
| `pallets/click` | LSE-122–123 | human-readable output and lifecycle completion |
| `Textualize/rich` | LSE-124–125 | compatible evolution and explicit bounds |
| `encode/httpx` | LSE-126–127 | secure diagnostics and immutable lifecycle |
| `pytest-dev/pytest` | LSE-128–129 | typed lifecycle and deterministic time |

Each target is pinned to a commit. The concise and detailed definitions, public
tasks, hidden tests, evaluator, runner, output schema, execution order, model,
and runtime settings are content-addressed by `experiment.lock.json` before the
scored run begins.

## Isolation

For each task and condition, the runner creates a fresh target checkout,
checks out the pinned commit, adds the locked definition and task as a local
experiment baseline, provisions dependencies, removes the Git remote, and then
starts a fresh ephemeral Codex session. The candidate cannot see the hidden
test and cannot push to the target repository. Candidate changes are captured
as a patch before independent evaluation.

The `--source-map` runner option may substitute an existing local Git clone for
transport efficiency. The expected public repository and commit remain locked,
the checked-out commit is verified, and the substitution is recorded in the
run directory.

## Measurement

Every answer receives a binary pass and a seven-point score:

1. hidden acceptance tests;
2. focused upstream regression checks;
3. candidate-authored tests;
4. repository quality checks;
5. dependency integrity;
6. bounded scope; and
7. structured handoff evidence integrity.

The score preserves more information than pass/fail while the strict binary
result remains easy to interpret. Aggregate reporting includes paired scores,
criterion pass rates, changed lines, elapsed time, tool calls, and
runtime-reported token usage.

## Run

```console
python run_suite.py --lock experiment.lock.json
```

Use `--tasks LSE-120,LSE-121` for a subset, `--limit 2` for a runner smoke test,
or repeat `--source-map REPOSITORY=LOCAL_CLONE` to use verified local clones.
Run evidence is written beneath `results/`; candidate workspaces are retained
and their paths recorded so an evaluation can be audited.

This is a controlled within-model comparison, not a universal ranking of either
definition. A ten-task result may reveal a useful pattern but cannot establish
that the result generalises to every model, repository, or software role.
