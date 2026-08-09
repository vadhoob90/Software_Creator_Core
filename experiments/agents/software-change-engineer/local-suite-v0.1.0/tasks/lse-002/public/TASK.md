# LSE-002 — eliminate a silent priority fallback

`parse_priority` currently converts malformed supplied priorities to zero, making missing data indistinguishable from invalid data.

Acceptance conditions:

- A missing `priority` key still returns zero.
- Integers and decimal integer strings from zero through five are accepted.
- Booleans, blank values, non-integer values, and values outside zero through five raise `ValueError`.
- When conversion fails, the public `ValueError` preserves the original exception as its cause.
- Do not silently default a present invalid value.
- Add focused tests, run the repository test command, and provide an evidence-backed handoff.
