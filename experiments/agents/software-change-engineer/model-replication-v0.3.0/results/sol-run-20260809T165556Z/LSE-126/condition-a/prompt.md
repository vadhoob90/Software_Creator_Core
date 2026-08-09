You are the Software Change Engineer for this bounded task.

Read and follow the repository instructions, `.pdlc/agent-definition.md`, and
`.pdlc/task.md`. Work only in this local checkout. Do not use network access,
Git remotes, credentials, or external systems. Make the requested code and test
changes, run checks that are actually available, and return only the structured
JSON handoff required by the runtime schema. Do not commit the change.

--- BEGIN TASK ---
---
id: LSE-126
target: encode/httpx
capability_area: secure_diagnostics
standards: [ES-001, ES-002, ES-003, ES-005]
---

# Redact API-key headers from diagnostic representations

`Headers.__repr__` redacts authorization headers, but common API-key header
names can still expose credentials in logs and debugging output.

## Definition of done

1. Representations redact values for `X-API-Key` and `API-Key` in addition to
   the existing authorization header names.
2. Matching is case-insensitive and works for both string and byte inputs.
3. Every occurrence of a repeated sensitive header is redacted.
4. Actual mapping access, `raw`, `items`, and `multi_items` retain the original
   values; only the representation is affected.
5. Existing non-sensitive and authorization representation behaviour is
   unchanged.
6. Focused tests and relevant repository checks pass.

Keep the sensitive-name policy centralized and do not log or publish real
credentials in tests or handoff evidence.
--- END TASK ---
