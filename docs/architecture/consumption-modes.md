# Software Creator Core consumption modes

**Status:** Adopted initial architecture  
**Effective:** 9 August 2026  
**Governed by:** [Development principles](../core/development-principles.md), [Engineering standards](../standards/README.md), and the [Core–Product Consumption Model](README.md)

## Purpose

Software Creator Core supports products with different needs. One product may want a versioned role definition, another may want Core-composed agents inside its own orchestration, and another may want the complete reference harness.

These are supported consumption modes, not stages in a mandatory maturity ladder. A product should adopt the smallest set of Core capabilities that solves its problem while making the resulting responsibilities and assurance claims explicit.

## Decision

Software Creator Core capabilities are independently consumable through stable public contracts.

- The complete reference harness is optional.
- A product-owned or third-party harness is a supported integration.
- The reference harness must use the same public contracts available to other harnesses.
- Consumption of one Core asset never implies that unrelated Core controls were applied.
- Products may use different modes for different workflows, provided each use is declared and attributable.
- Every consumed Core artifact is pinned to an immutable version or content digest.

## Supported modes

| Mode | Core provides | Product provides | Boundary contract | Permitted claim |
| --- | --- | --- | --- | --- |
| **Definitions only** | Versioned definitions such as principles, standards, role contracts, patterns, and output expectations | Selection, adaptation, execution, enforcement, and product context | The product records the exact Core artifact and version it consumed | “Uses Software Creator Core definition _X_ at version _Y_” |
| **Composed agents** | Core professional baseline, composition rules, conflict semantics, and provenance requirements | Product specialism, repository knowledge, task context, tools, authority, and execution environment | Composition produces a resolved agent definition and source manifest | “Uses a Software Creator Core-composed _role_” for the named role and version |
| **Controls and evidence** | Applicable controls, evidence contracts, outcome semantics, and validation requirements | Workflow orchestration, CI, tool adapters, evidence production, storage, and approvals | The custom harness emits evidence that conforms to the selected Core contracts | “Evaluates named Software Creator Core controls” with the relevant results; it does not claim use of the Core harness |
| **Reference harness** | Definitions, agent composition, control evaluation contracts, routing, lifecycle state, evidence handling, and the first-party execution harness | Product configuration, domain policy, specialist context, adapters, credentials, and deployment decisions | The product pins the harness and supplies configuration through supported extension points | “Uses the Software Creator Core reference harness” at the named version and for the stated workflow |

A product can combine modes. For example, it may use a Core-composed implementer agent inside its own harness while adopting only selected Core evidence contracts.

## Responsibilities that do not move

Choosing a broader mode does not transfer product accountability to Core.

Software Creator Core always owns:

- the meaning and compatibility of the Core artifacts it publishes
- the integrity of Core-owned contracts and default behaviours
- versioning and provenance requirements for those artifacts
- explicit failure and conflict semantics at Core boundaries

The product always owns:

- its domain decisions and risk appetite
- selection of applicable Core capabilities and standards
- product-specific agent specialism, knowledge, permissions, and credentials
- the correctness of its adapters and integrations
- deployment, operation, and acceptance of the resulting product
- any exception from an adopted requirement and the evidence supporting it

## Conformance is capability-scoped

There is no undifferentiated claim of “Software Creator Core compliant.”

A conformance statement must identify:

1. the capability or contract being claimed
2. the Core version and relevant artifact versions
3. the product workflow or component in scope
4. the harness or executor used
5. the evidence supporting the claim
6. any exception, exclusion, or unresolved result

Definitions-only consumption establishes provenance, not enforcement. Agent composition establishes how a role was resolved, not that the wider lifecycle ran. A custom harness can conform to Core controls without using the reference harness. Use of the reference harness does not prove that every optional control was enabled or passed.

Future named conformance profiles may group capabilities, but they must preserve this scoped evidence model.

## Boundary requirements

Every mode must satisfy these architectural constraints:

- **Explicit selection:** no Core capability becomes active merely because it is present.
- **Immutable resolution:** execution uses pinned inputs rather than a moving branch or unversioned source.
- **Attributable output:** generated or resolved artifacts record their Core and product inputs.
- **Visible exclusions:** skipped, unsupported, or overridden inputs have a recorded reason.
- **No privileged harness path:** the reference harness cannot depend on private behaviour unavailable to a conforming custom harness.
- **No silent downgrade:** failure to load or enforce a selected contract is an explicit outcome.
- **Replaceable integration:** product adapters and harnesses can change without rewriting Core definitions.
- **Product ownership:** installing Core never authorises it to overwrite product-owned policy, learning, or delivery artifacts.

## Implementation status

This document defines the supported architectural entry points. It does not claim that definitions, resolvers, adapters, conformance profiles, packages, or the reference harness have been implemented.

Each implementation increment must name the consumption mode it serves and demonstrate that it does not make a broader mode mandatory.
