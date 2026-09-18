# Foundation validation — 2026-09-18

Scope: local validation of the experimental `0.1.0a1` Core-only implementation on
branch `codex/core-workflow-foundation`, based on repository commit
`a5734431452ce6c1b125e262f5d7e3d0522268e9`. This is not a production release,
independent agent qualification, or proof that the full issue #9 epic is complete.

| Check actually executed | Result |
| --- | --- |
| Locked suite on Python 3.11.15 | 142 passed; no skipped tests |
| Locked suite on Python 3.12.12 | 142 passed; no skipped tests |
| Production line / branch coverage | 99.76% / 99.07%; all-source and changed-code gates passed |
| Critical module coverage | 100% lines and branches; declarative/decorated contracts also tested |
| Maximum measured cyclomatic / cognitive complexity | 10 / 12 across source and hand-authored scripts; no review warnings |
| Critical mutation analysis | 805 mutations, 769 killed, 95.53% raw score; 36 documented equivalents, no unexplained survivors or incomplete results |
| Ruff lint/format and strict mypy | Passed; 12 production modules type-checked |
| Bandit, offline secret scan, locked runtime dependency audit | Passed; no known runtime dependency vulnerabilities returned by the audit |
| Markdown links and whitespace validation | Passed |
| Synthetic workflow executions | Addition and unrelated label-normalisation workspaces passed with actual local Python checks |
| Build/install | Wheel and source distribution built; clean-installed wheel completed the synthetic demo |
| Codex subscription connectivity | Live ChatGPT-authenticated session returned a schema-valid contribution; no API-key fallback |
| Claude Code | Equivalent handoff/response contracts tested offline; live execution unavailable on this machine |
| GitHub Actions | Workflow configured and structure checked locally; remote run not yet performed |

Mutation survivors were inspected individually. Their equivalences are SQL case,
equivalent current-schema JSON serialization modes, the default JSON ASCII flag,
a single extra bounded sentinel byte, and a synonymous UTF-8 codec name. Each
exemption in `mutation-equivalents.json` contains a rationale and exact diff
digest. The gate rejects new survivors, timeouts, missing reports, stale reviews
and altered mutation diffs. Equivalents do not inflate the raw score. These
exemptions remain subject to the same human code review as implementation/tests.

Mutmut does not generate mutants for the decorated Pydantic validator or SQLite
connection context manager in this tool version. Their contract, database-open,
failure, rollback and recovery tests still run; mutation coverage must not be
mistaken for complete defect detection. The uncovered production statement and
branch are the optional `cli.py` direct-module entry guard; installed CLI and
CLI dispatch are exercised separately.

## Evidence and reproducibility

Use the commands in [engineering enforcement](engineering-enforcement.md).
The local run produced coverage JSON/XML, JUnit XML, complexity measurements and
Mutmut metadata. CI reproduces those checks from the lockfile and uploads the
reports plus distribution artifacts; it does not publish to a package registry.
Fresh mutation output was used after adding the final test inventory.

The source bundle has an explicit inclusion list, so local caches, generated
state and unrelated untracked branding assets are not shipped. The secret scan
does not verify suspected credentials against network services.

## Not demonstrated

The live Codex check proves connectivity/schema handling only, not a live
end-to-end development job or role competence. The end-to-end contributors in
the test suite are explicitly synthetic. Handoff adapters require an operator's
authenticated session; there is no autonomous multi-agent dispatcher. Tests
cannot establish that arbitrary future contributor assertions are truthful.

No Supplier Risk Engine files were changed. No product adoption, upgrade,
migration, deployment, merge or package publication was performed. Core does
not contain a model API client. Package installation and vulnerability-advisory
lookups are the only network-dependent steps in the ordinary build checks.
