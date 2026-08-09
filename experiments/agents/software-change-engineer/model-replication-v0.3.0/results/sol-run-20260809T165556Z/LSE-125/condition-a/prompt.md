You are the Software Change Engineer for this bounded task.

Read and follow the repository instructions, `.pdlc/agent-definition.md`, and
`.pdlc/task.md`. Work only in this local checkout. Do not use network access,
Git remotes, credentials, or external systems. Make the requested code and test
changes, run checks that are actually available, and return only the structured
JSON handoff required by the runtime schema. Do not commit the change.

--- BEGIN TASK ---
---
id: LSE-125
target: Textualize/rich
capability_area: explicit_bounds
standards: [ES-001, ES-002, ES-003]
---

# Reject contradictory measurement bounds explicitly

`Measurement.with_minimum`, `with_maximum`, and `clamp` currently accept invalid
bounds and may return surprising negative or inverted measurements.

## Definition of done

1. `with_minimum()` and `with_maximum()` reject negative widths with
   `ValueError` that identifies the invalid bound.
2. `clamp(min_width, max_width)` rejects a provided minimum greater than the
   provided maximum before changing the measurement.
3. `None` bounds and all valid existing clamp cases retain their behaviour.
4. The original immutable `Measurement` remains unchanged after both successful
   and failed operations.
5. Focused success and failure tests and relevant repository checks pass.

Do not alter `normalize()` semantics or dependency metadata.
--- END TASK ---
