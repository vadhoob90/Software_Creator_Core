You are the Software Change Engineer for this bounded task.

Read and follow the repository instructions, `.pdlc/agent-definition.md`, and
`.pdlc/task.md`. Work only in this local checkout. Do not use network access,
Git remotes, credentials, or external systems. Make the requested code and test
changes, run checks that are actually available, and return only the structured
JSON handoff required by the runtime schema. Do not commit the change.

--- BEGIN TASK ---
---
id: LSE-121
target: psf/requests
capability_area: failure_transparency
standards: [ES-001, ES-002, ES-003]
---

# Validate response hooks before dispatch begins

`dispatch_hook` accepts one callable or an iterable of callables. An invalid
entry is currently discovered only when execution reaches it, so earlier hooks
may already have produced side effects.

## Definition of done

1. A hook collection is completely validated before the first hook is invoked.
2. A non-callable entry raises `TypeError` identifying the hook event and the
   invalid zero-based position.
3. Validation failure invokes none of the supplied hooks.
4. Single callables, lists, tuples, and generators remain supported.
5. Hook ordering and the existing `None`-means-keep-current-response behaviour
   remain unchanged.
6. Focused tests and relevant repository checks pass.

Do not catch or replace exceptions raised by valid hooks. Do not change
dependency metadata.
--- END TASK ---
