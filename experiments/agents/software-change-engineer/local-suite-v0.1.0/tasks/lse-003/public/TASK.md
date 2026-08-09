# LSE-003 — interacting discount branches

Repair `final_price` and demonstrate the behaviour with effective tests.

Acceptance conditions:

- `price_cents` is a non-negative integer, excluding booleans.
- `member` is a boolean.
- `coupon_percent` is an integer from zero through 100, excluding booleans.
- Members receive 10% off using integer floor arithmetic.
- A coupon is applied to the already member-discounted price, also using integer floor arithmetic.
- The two discounts therefore stack; neither branch suppresses the other.
- Invalid types raise `TypeError`; invalid ranges raise `ValueError`.
- Add focused tests for individual, combined, boundary, and failure paths; run the tests and provide an evidence-backed handoff.
