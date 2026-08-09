# ES-001: Comprehension and usability

**Status:** Adopted initial baseline  
**Governing principle:** [Comprehension and usability come first](../core/development-principles.md#1-comprehension-and-usability-come-first)  
**Default enforcement:** Documented

## Purpose

PDLC Core must minimise the effort required for a human or machine to discover, understand, use, and safely change a capability. Readability is a system property covering code, schemas, prompts, repository structure, commands, errors, documentation, and generated artifacts.

## Applicability

This standard applies to hand-authored implementation code, agent and routing definitions, public contracts, configuration, documentation, examples, and generated interfaces maintained by PDLC Core.

## Requirements

### ES-001-01: Explicit responsibilities

Each component MUST have one describable responsibility, explicit inputs and outputs, and declared dependencies. Dependencies between named components MUST be directed; cycles across declared component boundaries are prohibited.

### ES-001-02: Intention-revealing interfaces

Names MUST express domain intent. Public commands, APIs, schemas, agents, and configuration MUST make required inputs, defaults, constraints, outcomes, and next actions discoverable to both humans and machines.

Public interfaces MUST include:

- A concise purpose.
- Input and output definitions.
- At least one representative example.
- Failure outcomes and remediation.
- Version or compatibility expectations where observable downstream.

### ES-001-03: Control-flow complexity

For each hand-authored production function or equivalent executable unit:

- Cyclomatic complexity from 11 through 15 MUST produce a review warning.
- Cyclomatic complexity greater than 15 MUST block acceptance.
- Cognitive complexity greater than 15 MUST block acceptance when a reliable analyser exists for the implementation language.
- More than four nested control-flow levels MUST produce a review warning.

A threshold exception requires evidence that decomposition would make the behaviour less cohesive or less understandable, plus focused tests covering each material path. Generated, vendored, declarative, and test code may use different measurements, but any exclusion MUST be explicit.

The metric is a guardrail. Passing it does not establish readability.

### ES-001-04: Size as a review signal

A function exceeding 60 logical lines or a hand-authored source file exceeding 500 logical lines MUST trigger a cohesion review. Size alone MUST NOT block acceptance; reviewers must decide whether the artifact still has a clear responsibility and can be understood in context.

### ES-001-05: Visible behaviour

Important control flow, state transitions, fallbacks, and side effects MUST be visible in the primary implementation path. Metaprogramming, implicit global state, hidden mutation, or clever compression SHOULD NOT be used when a direct expression is reasonably available.

### ES-001-06: Useful explanation

Comments and documentation MUST explain constraints, intent, trade-offs, or non-obvious decisions. They MUST NOT be used as a substitute for making implementation understandable.

Documentation and examples MUST change with the behaviour they describe. Broken internal links, invalid examples, and undocumented public interfaces are acceptance failures.

### ES-001-07: Human and machine usability

A public capability MUST provide stable machine-readable structure and a concise human-readable representation. Commands MUST provide actionable help and stable exit semantics. Errors MUST identify what failed, why it matters, and what the consumer can do next without exposing sensitive implementation detail.

Where PDLC Core creates or governs a user interface, applicable accessibility requirements are release requirements.

### ES-001-08: Necessary abstraction

An abstraction MUST serve a current, demonstrated use case. A new extension point, framework, compatibility layer, or generic indirection requires at least two concrete consumers or a documented boundary that must vary independently now.

## Required verification

### Automated controls

When the relevant implementation exists, CI MUST:

- Enforce formatting and language-appropriate static analysis.
- Measure cyclomatic complexity and, where supported, cognitive complexity.
- Report size and nesting review signals.
- Detect component dependency cycles.
- Validate schemas and representative examples.
- Check internal documentation links.
- Verify public commands or APIs expose help or interface descriptions.

### Review controls

Reviewers MUST be able to answer:

- Can the responsibility and primary path be explained without reconstructing hidden state?
- Are names and boundaries expressed in the product domain?
- Can a new human or agent discover how to use the capability?
- Does each abstraction earn its cost?
- Would a simpler expression preserve the required behaviour?
- Do documentation, examples, and errors match reality?

## Evidence

The change evidence must include applicable static-analysis results, complexity warnings or exceptions, documentation checks, and the review decision for any flagged size or abstraction.

## Further reading

- [ESLint cyclomatic complexity rule](https://eslint.org/docs/latest/rules/complexity)
- [Google Engineering Practices: code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
- [Command Line Interface Guidelines](https://clig.dev/)
- [JSON Schema specification](https://json-schema.org/specification)
- [Web Content Accessibility Guidelines](https://www.w3.org/WAI/standards-guidelines/wcag/)
