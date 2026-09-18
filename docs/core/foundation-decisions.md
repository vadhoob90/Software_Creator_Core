# Foundation decisions and extraction inventory

Status: implemented experimental design, subject to owner review. This is the
Core-only vertical slice of [issue #9](https://github.com/vadhoob90/Software_Creator_Core/issues/9),
not the existing-product adoption release described by the wider epic.

## Request and acceptance

Build the reusable software-development mechanism without modifying any product
repository. Support Codex and Claude Code subscription-session handoffs, explicit
human authority, inspectable context, independently submitted verification and
review, and durable outcomes. Prove behaviour with synthetic local execution and
enforce Core's own engineering standards. No model API client or API-key fallback.

Stop delivery on an unresolved brief/design, invalid authority, stale inputs,
failed evidence, interruption requiring state inspection, or host unavailability.
Do not publish, deploy, qualify agents or migrate products as a side effect.

## Generic inventory and disposition

The reference review informed these boundaries; no private product prompts,
source, records or specialisations were copied into this repository.

| Observed component/pattern | Destination and decision |
| --- | --- |
| Professional role prompts | Core experimental role templates; five accountable outputs, with three delivery roles actively routed |
| Orchestration and route selection | Optional Core policy/service; state transitions enforced outside prompts, fixed bounded delivery route for this slice |
| Job, contribution and evidence payloads | Independently importable versioned Core schemas |
| Product paths, tools, domain knowledge and acceptance | Product-owned declared inputs; no product name or repository layout embedded in the harness |
| Standards and reusable authority controls | Core baseline plus deterministic policy checks; host enforces OS/process/network restrictions |
| Profiles, specialisations and approved learning | Product-owned files; explicit role selection, owner attestation, version and digest pinning |
| Assistant-specific command wrappers | Codex/Claude Code file-handoff adapters over the same contracts; no duplicated canonical prompts |
| Historical run artifacts and review | Product/operator-owned workspace files and local journal; private context text omitted from composition manifests |
| Agent evaluations | Separate qualification work; harness tests are not competence evidence |
| Adoption, upgrade, rollback and product regression | Deferred separate activity; do not edit Supplier Risk Engine |

## Implementation choices

- **Python 3.11+ package and CLI:** strict Pydantic v2 JSON schemas and a small
  standard-library persistence layer. This does not prescribe a downstream
  product's implementation language. The lockfile pins tooling and dependencies.
- **SQLite append-only snapshots:** atomic compare-and-append supports local
  recovery and prevents stale writes. It is not a hostile multi-user trust store.
  Snapshot hashes detect accidental corruption, not deliberate database forgery.
- **Pure policy plus optional service:** definitions and controls remain usable
  independently. Filesystem, storage and host concerns are outside policy.
- **Explicit file handoff:** uses existing authenticated assistant sessions,
  requires no provider SDK, and works when Claude Code is not installed. This is
  less automated than a subprocess adapter; no unattended host execution is
  claimed. The host supplies the actual artifacts and contribution response.
- **Fixed route for a clarified change:** engineer → quality engineer → reviewer,
  bounded by owner commitment and acceptance. Discovery/architecture templates
  are inspectable but not autonomous routes. Proportional routing and retries
  require further design and evidence.
- **Fail closed on changed evidence:** accepted files must retain their hashes
  through acceptance. A repair uses a new job in this alpha. Approval signs the
  current snapshot digest by operator attestation, not cryptographic identity.

## Threat model and limitations

Assets are private context, local product files, review evidence and approval
history. Relevant threats include untrusted context, forged actor labels,
path traversal, oversized artifacts, stale/replayed approvals, changed evidence,
concurrent writes, corruption and misleading completion claims.

Strict contracts, explicit source selection, bounded relative-file reads,
workspace identity, evidence hashes, revision checks and negative tests address
the application's declared boundaries. A local adversary able to change files
concurrently can race filesystem checks; the Core process is not a sandbox.
Protect the store and its parent directory from agent writes, use isolated host
workspaces, and retain artifact versions. Actor independence and the truth of
test/review assertions remain operator responsibilities. Context instructions
are untrusted data; the host must enforce authority even if a prompt asks more.

There is no remote service, credential vault, telemetry, automatic learning
promotion, package publication, deployment, migration or product adoption here.
Future stable release work needs real-host representative workflows, independent
role evaluation, consumer lifecycle compatibility and separately authorised
product integration evidence. See the [implementation guide](implementation.md)
and [engineering enforcement map](engineering-enforcement.md).
