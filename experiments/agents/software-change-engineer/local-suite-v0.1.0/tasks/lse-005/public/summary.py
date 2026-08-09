"""Build a small serialisable event summary."""


def build_summary(events):
    messages = [str(event) for event in events]
    return {"count": len(messages), "messages": messages}
