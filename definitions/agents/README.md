# Agent definitions

**Status:** Experimental  
**Consumption mode:** [Definitions only](../../docs/architecture/consumption-modes.md#supported-modes)

PDLC Core agent definitions are versioned, platform-neutral professional baselines. A product may consume a definition directly, augment it with product specialism, and execute it using its own agent platform or harness.

No resolver, router, package, or PDLC Core runtime is required. Consuming a definition establishes provenance for that definition only; it does not show that agent composition, Core controls, lifecycle routing, or the reference harness ran.

## Admission gate

A proposed role must pass the [agent qualification gate](../../docs/agents/agent-qualification-gate.md) before it becomes a canonical PDLC Core agent. The gate requires a recurring accountable outcome, distinguishable expertise, measurable success, explicit boundaries, and retained competence evidence. Any competence or experience claim must then be demonstrated for an exact agent build under the [agent evaluation and qualification protocol](../../docs/agents/agent-evaluation-and-qualification-protocol.md).

Experimental artifacts may be used to learn, but they must not be represented as qualified roles until their qualification record passes every mandatory gate.

## Available definitions

| Role | Published version | Qualification status | Purpose |
| --- | --- | --- | --- |
| Implementer | [0.1.0](implementer/v0.1.0.md) | Experimental; reshape required | Historical first slice that exposed the need to separate the professional baseline from a specific accountable role |

## Direct consumption

1. Select an explicitly versioned definition file.
2. Pin the PDLC Core Git tag or commit that contains it. Do not consume a moving branch.
3. Record the repository, pinned ref, artifact path, and declared artifact version in the downstream product.
4. Keep product specialism separate and attributable.
5. Supply current-job authority, inputs, tools, and resource limits at execution time.

A minimal consumer record may look like this:

```yaml
core_definition:
  repository: https://github.com/vadhoob90/PDLC_Core
  ref: <immutable-tag-or-commit>
  path: definitions/agents/implementer/v0.1.0.md
  artifact_version: 0.1.0
product_specialisation:
  source: <product-owned-path-and-version>
```

This example records provenance; it is not a runtime configuration schema.

## Composition boundary

A product specialisation may add domain knowledge, technology practices, repository conventions, narrower permissions, stronger evidence requirements, and product-specific output contracts. It may extend or tighten the Core baseline but must not silently weaken or contradict it.

Conflicts must be surfaced before execution. A permitted deviation requires an explicit, product-owned exception satisfying the applicable Core standard; text ordering or prompt concatenation is not an exception mechanism.

## Version and lifecycle policy

- A published versioned file is immutable. A correction or behavioural change creates a new semantic version and path.
- Experimental versions may change incompatibly through a new version and do not carry a stable compatibility guarantee.
- Deprecation and removal follow [ES-004](../../docs/standards/ES-004-deliberate-compatible-reversible-evolution.md).
- Consumers remain on their pinned version until they deliberately adopt another.
- Failure to retrieve or validate the pinned definition is an explicit failure. A consumer must not silently fall back to another version.

## Format

Each definition combines machine-readable YAML frontmatter with a concise human-readable role contract. Stable headings make the contract traversable without binding it to a model provider, prompt format, agent framework, programming language, or harness.
