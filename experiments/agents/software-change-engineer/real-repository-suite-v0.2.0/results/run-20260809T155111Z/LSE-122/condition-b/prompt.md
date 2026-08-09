You are the Software Change Engineer for this bounded task.

Read and follow the repository instructions, `.pdlc/agent-definition.md`, and
`.pdlc/task.md`. Work only in this local checkout. Do not use network access,
Git remotes, credentials, or external systems. Make the requested code and test
changes, run checks that are actually available, and return only the structured
JSON handoff required by the runtime schema. Do not commit the change.

--- BEGIN TASK ---
---
id: LSE-122
target: pallets/click
capability_area: human_readability
standards: [ES-001, ES-002]
---

# Make generated short help measure visible ANSI width

Click's `_make_default_short_help` counts ANSI escape bytes as visible
characters. Styled help can therefore be shortened earlier than unstyled help
with the same visible text.

## Definition of done

1. Short-help length decisions use terminal-visible width rather than raw
   string length.
2. ANSI sequences are preserved exactly in returned help.
3. The stripped visible result never exceeds `max_length`.
4. Existing paragraph, sentence-ending, no-rewrap-marker, whitespace-collapse,
   and ellipsis behaviour remains unchanged.
5. Focused tests cover styled text both below and across the truncation boundary.
6. Relevant repository tests, formatting, and lint checks pass.

Keep this change within the existing short-help implementation; do not introduce
a second ANSI parser or change public APIs.
--- END TASK ---
