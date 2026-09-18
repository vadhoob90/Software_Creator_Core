# Core workflow foundation — 0.1.0a1

This experimental implementation provides a local, evidence-led workflow for an
already clarified software change. It supplies five candidate role templates,
strict JSON contracts, explainable context, file handoffs for Codex and Claude
Code, and a persisted delivery workflow. It contains no model API client.

**Scope:** build Software Creator Core itself. Supplier Risk Engine was a
read-only design reference. Existing-product adoption, migration, upgrades,
and new-product generation are separate future work. This increment does not
complete every acceptance criterion in issue #9.

The [foundation decision record](foundation-decisions.md) documents the generic
extraction inventory, implementation tradeoffs and threat model.

## Install and inspect

Python 3.11 or newer is required. From this checkout:

```sh
uv sync --frozen
uv run --no-sync software-creator doctor
uv run --no-sync software-creator role software-engineer
uv run --no-sync software-creator schema job
uv run --no-sync software-creator schema contribution
uv run --no-sync python scripts/demo.py
```

The distribution is built locally/through CI; it has not been published to a
package registry. Consumers must not assume `pip install software-creator-core`
selects this reviewed artifact. `uv.lock` pins development and runtime inputs.

`role` and `schema` work without a workspace or job store. They permit
definitions-only use. A custom harness may use the same Python contracts and
policy functions without the CLI or SQLite store.

## What the roles do

| Candidate role | Accountable output in this increment |
| --- | --- |
| Product Manager | Clarified need, acceptance and unresolved questions; standalone template |
| Software Architect | Boundary and compatibility assessment; standalone template |
| Software Engineer | Implementation artifacts and supporting evidence |
| Quality Engineer | Independent verification against every acceptance criterion |
| Code Reviewer | Independent implementation review with criterion evidence |

These are **experimental, unqualified templates**. They are not canonical
qualified agent definitions under the qualification gate. Deterministic harness
tests and a host connectivity check do not establish agent competence. Issues
#3 and #6 remain relevant to independent agent evaluation.

## Delivery workflow

```text
awaiting-commitment → implementation → verification → review
                   → awaiting-acceptance → completed
```

The arrows represent separate calls, not an autonomous background loop.
Commitment and acceptance require the owner and exact current job digest.
Implementation, verification, and review need distinct contributor identities,
separate from the owner. Successful verification and review must cite passing
evidence for every acceptance criterion; any contradictory failure blocks them.
Incomplete, degraded and failed contributions end in `failed`, retaining their
original outcome. Cancellation ends in `cancelled`.

The current delivery route requires an already clarified brief/design. A job
declaring unresolved discovery or architecture needs is refused with
`brief-not-ready`; use the relevant standalone templates and human decisions
first. Risk is recorded, but this slice does not automatically infer risk,
select specialists, authorise elevated side effects, or execute releases.

## Use an existing subscription session

Create a disposable example workspace and store outside the source checkout.
Supply their paths explicitly; the commands below use `/tmp/core-example` as
an illustrative directory you have already created:

```sh
software-creator --workspace /tmp/core-example --store /tmp/core-example/jobs.sqlite3 create examples/job.json
software-creator --workspace /tmp/core-example --store /tmp/core-example/jobs.sqlite3 show addition-example
software-creator --workspace /tmp/core-example --store /tmp/core-example/jobs.sqlite3 approve addition-example --actor human-owner --digest DIGEST_FROM_SHOW
software-creator --workspace /tmp/core-example --store /tmp/core-example/jobs.sqlite3 handoff addition-example --role software-engineer --host codex
```

Read the returned packet in a Codex subscription session operating within that
workspace. For Claude Code, select `--host claude-code` and use an authenticated
Claude Code subscription session when available. Both handoffs use the same
packet and response schema. They do not start a subprocess or install a host.
`doctor` reports executable availability, not authentication or live readiness.

The session produces the permitted artifacts and a response JSON matching
`Contribution`. The packet supplies the job ID, revision, context digest, role,
brief, allowed evidence paths, and schema. Record the actual host/model and
outcome, not a fictional identity or claimed test result. Then submit:

```sh
software-creator --workspace /tmp/core-example --store /tmp/core-example/jobs.sqlite3 submit /tmp/engineer-response.json
```

Repeat handoff/submit for `quality-engineer`, then `code-reviewer`, using fresh
independent contributors. Finish with `show` and owner `approve` on the current
digest. Each role's response must list real file hashes. To compute one:

```sh
python -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('/tmp/core-example/calculator.py').read_bytes()).hexdigest())"
```

The harness checks evidence identity, scope, integrity and required coverage of
acceptance criteria. It does **not** establish that an asserted test was actually
run or that a passing result is substantively correct. The operator and
independent contributor must inspect that evidence. The automated demo actually
runs its known synthetic code; it does not execute arbitrary submitted code.

## Context and evidence boundaries

Explicitly selected profile, specialisation, approved learning, and task sources
are pinned by path, version, role, owner approval and SHA-256. Absent layers are
recorded as skipped. Core supplies an operational standards summary and role
contract. Role packets contain selected private text; retain them with the same
access restrictions as the source. Persisted composition manifests contain
hashes and references instead of duplicating that text.

Artifacts must be explicitly declared, regular workspace-relative files, at
most 256 KB each. Symbolic links and path escapes are rejected. After an artifact
is accepted, changing it invalidates subsequent evidence and final acceptance.
Use a new job for a revised change; no automatic repair loop is implemented.
The workspace identity is also bound to the job. Another workspace cannot reuse
its approvals even if its relative filenames match.

## Trust, authority and data handling

This release is a **single-operator local tool**, not a multi-user approval server
or an OS sandbox. Actor names and source approvals are operator attestations,
not authenticated identities. Distinct strings alone do not prove independent
review. Keep the store outside agent-write scope and let the human operator
run approval commands. Hosts must enforce filesystem, process, network and
credential restrictions for generated code; a prompt is not that enforcement.

The package never executes submitted commands/code, modifies product files,
starts an API client, publishes, merges or deploys. The human host session owns
any implementation side effects under its separately granted authority. No
provider credentials are requested by Core. The optional connectivity script
requires ChatGPT login, strips API-key environment variables and has no API
fallback. Claude Code has contract tests but no live validation on this machine.

The database holds briefs, contribution summaries, approvals and artifact
references. Do not put secrets or unnecessary private content in those fields.
Protect its directory using local OS access controls. Retention is operator
controlled: retain the journal and cited artifact versions for as long as their
evidence is needed. There is no remote telemetry or automatic learning upload.

## Persistence and recovery

SQLite commits one new validated snapshot per step. Optimistic revision checks
and SQLite write locking reject duplicate or concurrent submissions. A process
interruption leaves the previous commit or the complete new commit; reopen with
`show` before deciding what to submit next. Never blindly replay an approval.

`context` previews current inputs; `show` includes the historical manifests.
`cancel JOB --actor OWNER` stops an unfinished job. Failed/cancelled/completed
jobs are terminal for delivery; start a new job after correcting the cause.
Digests detect accidental corruption but do not protect against a malicious
operator with database access. Restore a verified backup for corruption; the
tool never resets or silently repairs a corrupt journal.

Only schema version `1` is supported. Unknown fields and future versions are
rejected. No database migration, downgrade, automatic upgrade, archive or delete
operation is implemented. Preserve the old environment/journal before trying a
future version. These alpha contracts may change before a stable release;
future supported migrations must be explicit and tested.

## Command outcomes

Results and errors are JSON; `--help` supplies human-readable guidance. An
accepted state-changing call reports `operation_outcome: success` separately
from `workflow_outcome`, which stays `partial` until owner acceptance. A failed
or cancelled job cannot be mistaken for a completed workflow.

Exit codes: `0` accepted/read-only command; `1` domain denial or storage failure;
`2` invalid input/usage; `3` a stored failed/cancelled workflow. Errors contain a
stable code, explanation and remediation, without echoing private input values.

## Build and verification

See the [engineering enforcement map](engineering-enforcement.md) for controls,
commands, exclusions and remaining review responsibilities. CI builds a wheel
and source distribution and publishes them as run artifacts with hashes. It
does not upload to a package registry or deploy a product.

The [validation record](validation.md) distinguishes checks actually run locally
from configured CI and still-unavailable live-host evidence.
