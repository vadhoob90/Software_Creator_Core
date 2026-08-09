"""Deterministic integer-cent pricing."""


def final_price(price_cents, member=False, coupon_percent=0):
    """Apply member or coupon discount; combined use is currently defective."""
    result = price_cents
    if member:
        result -= result * 10 // 100
    elif coupon_percent:
        result -= result * coupon_percent // 100
    return result
