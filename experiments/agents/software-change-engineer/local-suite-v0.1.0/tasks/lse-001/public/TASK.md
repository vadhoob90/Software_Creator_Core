# LSE-001 — bounded retry cap

Add an optional `max_delay_seconds` argument to `retry_delays`.

Acceptance conditions:

- Omitting it or passing `None` preserves current behaviour.
- It must be an integer greater than or equal to zero; booleans are not integers for this contract.
- A non-integer raises `TypeError`; a negative integer raises `ValueError`.
- Every returned delay is capped at the configured maximum, including a maximum of zero.
- Existing validation and return types remain compatible.
- Add focused tests, run the repository test command, and provide an evidence-backed handoff.
