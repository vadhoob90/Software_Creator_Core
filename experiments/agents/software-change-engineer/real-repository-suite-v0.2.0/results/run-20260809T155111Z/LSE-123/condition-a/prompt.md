You are the Software Change Engineer for this bounded task.

Read and follow the repository instructions, `.pdlc/agent-definition.md`, and
`.pdlc/task.md`. Work only in this local checkout. Do not use network access,
Git remotes, credentials, or external systems. Make the requested code and test
changes, run checks that are actually available, and return only the structured
JSON handoff required by the runtime schema. Do not commit the change.

--- BEGIN TASK ---
---
id: LSE-123
target: pallets/click
capability_area: component_lifecycle
standards: [ES-001, ES-002, ES-003, ES-004]
---

# Complete pending progress updates when a progress bar finishes

`ProgressBar` batches manual updates through `update_min_steps`. Calling
`finish()` while a partial batch is pending currently discards that progress.

## Definition of done

1. `update_min_steps` values below 1 are rejected during construction with an
   explicit `ValueError`.
2. `finish()` applies a pending partial update exactly once before marking the
   bar finished.
3. Repeated `finish()` calls are idempotent and do not advance progress again.
4. Normal iteration and updates that already reached the threshold retain their
   behaviour.
5. Focused lifecycle tests and relevant repository checks pass.

Do not change terminal rendering contracts or dependency metadata.
--- END TASK ---
