You are the Software Change Engineer for this bounded task.

Read and follow the repository instructions, `.pdlc/agent-definition.md`, and
`.pdlc/task.md`. Work only in this local checkout. Do not use network access,
Git remotes, credentials, or external systems. Make the requested code and test
changes, run checks that are actually available, and return only the structured
JSON handoff required by the runtime schema. Do not commit the change.

--- BEGIN TASK ---
---
id: LSE-124
target: Textualize/rich
capability_area: compatible_evolution
standards: [ES-001, ES-002, ES-003, ES-004]
---

# Add explicit binary file-size formatting

Rich exposes decimal SI file-size formatting but no corresponding IEC binary
formatter.

## Definition of done

1. `rich.filesize.binary()` formats powers of 1024 using `KiB`, `MiB`, `GiB`,
   `TiB`, `PiB`, `EiB`, `ZiB`, and `YiB`.
2. It supports the same `precision` and `separator` options as `decimal()`.
3. Zero, one byte, values below the first unit, fractional units, and large
   values behave consistently with the existing decimal formatter.
4. Negative sizes passed to either public formatter fail explicitly with
   `ValueError` and do not return misleading output.
5. `binary` is exported alongside `decimal`; existing decimal output is
   otherwise unchanged.
6. Focused tests and relevant repository checks pass.

Reuse the existing formatting boundary rather than duplicating its algorithm.
--- END TASK ---
