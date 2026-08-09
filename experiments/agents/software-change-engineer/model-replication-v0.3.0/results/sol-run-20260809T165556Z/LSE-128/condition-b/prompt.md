You are the Software Change Engineer for this bounded task.

Read and follow the repository instructions, `.pdlc/agent-definition.md`, and
`.pdlc/task.md`. Work only in this local checkout. Do not use network access,
Git remotes, credentials, or external systems. Make the requested code and test
changes, run checks that are actually available, and return only the structured
JSON handoff required by the runtime schema. Do not commit the change.

--- BEGIN TASK ---
---
id: LSE-128
target: pytest-dev/pytest
capability_area: component_lifecycle
standards: [ES-001, ES-002, ES-003, ES-004]
---

# Add a type-safe destructive read to Stash

`Stash` supports setting, reading, defaulting, and deletion, but consumers
cannot retrieve and remove a value as one lifecycle operation.

## Definition of done

1. Add `Stash.pop(key)` which returns and removes the typed value.
2. Without a default, a missing key raises `KeyError` consistently with
   `__getitem__` and `__delitem__`.
3. `Stash.pop(key, default)` returns the default without changing the stash when
   the key is absent, including when the explicit default is `None`.
4. Type overloads preserve the relationship between `StashKey[T]`, its value,
   and a potentially different default type.
5. Length, containment, `get`, `setdefault`, and deletion remain compatible.
6. Focused runtime and typing-relevant tests plus repository checks pass.

Do not expose the private storage mapping or change dependency metadata.
--- END TASK ---
