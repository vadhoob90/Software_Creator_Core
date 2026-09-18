# Engineering enforcement for the Core foundation

The adopted standards apply to Core itself. This document scopes the first
implementation's automated evidence; it does not mark every standard automated.

| Standard | Blocking checks in this increment | Still requires review |
| --- | --- | --- |
| ES-001 | Ruff formatting/lint, strict mypy, cyclomatic >15, cognitive >15, inward component dependencies and no cycles, schema/CLI tests, Markdown links | Naming, cohesion, abstractions and flagged size/nesting |
| ES-002 | Offline behavioural/contract/integration tests, separate total and changed line/branch coverage, baseline ratchet, targeted critical mutations, no skipped required tests | Test relevance, independent evidence and agent qualification |
| ES-003 | Outcome, stale evidence, duplicate/concurrent write, transaction rollback, recovery, corruption and error-redaction tests | Consumer recovery and local backup policy |
| ES-004 | Strict schema version rejection, snapshot preservation, package smoke tests | Future adoption, migration, compatibility windows and release decisions |
| ES-005 | Workspace/path/role boundaries, approval and replay checks, source/dependency/secret scans, read-only CI credentials | Host isolation, operator identity, real independence and external action authority |
| ES-006 | Input validation, secret minimisation, dependency/source scans and failure tests | Product-specific threat models; see the trust boundary in the implementation guide |

## Local commands

```sh
uv sync --frozen
uv run --no-sync ruff check src tests scripts
uv run --no-sync ruff format --check src tests scripts
uv run --no-sync mypy
uv run --no-sync python scripts/check_quality.py
uv run --no-sync pytest --cov=software_creator_core --cov-branch --cov-report=json --junitxml=/tmp/core-tests.xml
uv run --no-sync python scripts/check_test_report.py /tmp/core-tests.xml
uv run --no-sync python scripts/check_coverage.py
uv run --no-sync mutmut run --max-children 2
uv run --no-sync python scripts/check_mutations.py
uv run --no-sync bandit -q -r src/software_creator_core
uv run --no-sync python scripts/check_secrets.py
uv run --no-sync python .github/scripts/check_markdown_links.py
uv build
```

Dependency installation and the vulnerability audit use package registries and
advisory services. The default tests use synthetic local data and no model
services or production credentials. Live subscription usage is a separate,
explicit command, never a required CI test:

```sh
uv run --no-sync python scripts/live_codex_smoke.py --confirm-subscription-usage
```

This check verifies subscription connectivity and a response schema only. It
does not qualify an agent or claim a live end-to-end software-development run.
Codex's documented [non-interactive interface](https://developers.openai.com/codex/noninteractive)
and the locally installed CLI's help were checked when implementing it.

## Coverage and mutation scope

Production coverage covers the entire installed `software_creator_core` package.
The scripts and tests are not included in that product-code denominator; the
gate scripts have explicit positive and negative tests. Test code is excluded
from production complexity limits; hand-authored scripts are also measured for
complexity and size. There are no blanket production coverage exclusions.

Line and branch coverage are independent. Repository floors are 80%/75%; changed
production floors are 90%/85%; changed critical floors are 95%/90%. Critical
modules are contracts, policy, context, evidence, files, storage and service.
Changed scope uses added/modified statement lines and outgoing branches relative
to the PR base commit. An all-source pass is also required. A checked-in baseline
ratchets the total; CI compares with the base branch's baseline to prevent a PR
from lowering it. Baseline changes require the same review as test changes.

Mutation tests cover critical executable logic using the locked Mutmut version.
The gate requires at least the standard's 80% score and no unexplained surviving
mutant. Equivalent mutants need a specific reviewed rationale and a digest of
their diff; changes invalidate the exemption. Pydantic's declarative schemas and
decorated validator are exercised by contract/property tests; this Mutmut
version generates no mutants for that decorated validator.

Use fresh mutation outputs after changing the test inventory: the tool can reuse
cached associations that do not include newly added tests. CI starts from a
clean checkout. Local old outputs can be moved aside before rerunning.

## CI and release boundaries

The existing `documentation` and `Required checks` status names are preserved.
The aggregate now requires documentation, Python 3.11/3.12 tests, mutation,
security and package jobs. Workflows have bounded durations, pinned action
commits and read-only repository permissions. No model/API credentials are used.

CI uploads machine-readable coverage, complexity and mutation evidence, plus the
built distribution and its hashes. Publication, signing/attestation of a public
release, supported downstream upgrades and deployment require separate release
work. Do not treat a downloadable CI artifact as an approved production release.
