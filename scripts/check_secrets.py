"""Scan tracked and new source files without printing suspected secret values."""

import json
import subprocess
from pathlib import Path

from detect_secrets import SecretsCollection
from detect_secrets.settings import default_settings


def scan(paths):
    secrets = SecretsCollection()
    with default_settings() as settings:
        # Scanning must never send a suspected credential to a verification service.
        settings.disable_filters(
            "detect_secrets.filters.common.is_ignored_due_to_verification_policies"
        )
        for path in paths:
            if Path(path).is_file():
                secrets.scan_file(path)
    return [
        {"file": filename, "line": finding.line_number, "type": finding.type}
        for filename, finding in secrets
    ]


def main():
    result = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        capture_output=True,
        text=True,
        timeout=10,
        check=True,
    )
    paths = [
        p
        for p in result.stdout.split("\0")
        if p and Path(p).suffix in {".py", ".md", ".json", ".toml", ".yml", ".yaml", ".txt"}
    ]
    findings = scan(paths)
    print(json.dumps({"findings": findings}, indent=2))
    return int(bool(findings))


if __name__ == "__main__":
    raise SystemExit(main())
