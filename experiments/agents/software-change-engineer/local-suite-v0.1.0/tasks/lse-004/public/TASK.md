# LSE-004 — complete the profile update lifecycle

Add `update_profile(profile_id, **changes)` to `ProfileStore`.

Acceptance conditions:

- `name` and `email` are the only updateable fields, and either may be updated independently.
- At least one change is required; unknown fields and empty or non-string values are invalid.
- Invalid update input raises `ValueError` without partially changing stored state.
- An unknown profile raises `KeyError`.
- `profile_id` and `created_at` are preserved.
- The method returns a caller-owned copy, consistent with `get_profile`.
- Add focused tests for successful partial updates, identity preservation, unknown profiles, invalid changes, and atomic failure; run the tests and provide an evidence-backed handoff.
