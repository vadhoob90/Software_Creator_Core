"""Priority parsing at an input boundary."""


def parse_priority(record):
    """Return a priority, currently defaulting malformed data silently."""
    try:
        return int(record.get("priority", 0))
    except (TypeError, ValueError):
        return 0
