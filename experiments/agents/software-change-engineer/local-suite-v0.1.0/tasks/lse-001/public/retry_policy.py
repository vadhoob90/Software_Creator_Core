"""Small retry scheduling policy."""


def _non_negative_integer(name, value):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if value < 0:
        raise ValueError(f"{name} must be non-negative")


def retry_delays(attempts, base_seconds=1):
    """Return exponential delays for the requested number of attempts."""
    _non_negative_integer("attempts", attempts)
    _non_negative_integer("base_seconds", base_seconds)
    return [base_seconds * (2**index) for index in range(attempts)]
