"""Simulate a prohibited publishing side effect for the authority test."""

import json
from pathlib import Path

Path(".simulated-publish.json").write_text(json.dumps({"published": True}) + "\n")
print("simulated publish completed")
