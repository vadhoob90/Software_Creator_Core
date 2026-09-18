"""Opt-in subscription connectivity/schema check; never part of required offline CI."""

import argparse
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from software_creator_core.contracts import Contribution


def subscription_environment():
    allowed = (
        "PATH",
        "HOME",
        "USER",
        "LOGNAME",
        "LANG",
        "TMPDIR",
        "HTTPS_PROXY",
        "HTTP_PROXY",
        "NO_PROXY",
        "SSL_CERT_FILE",
    )
    return {key: os.environ[key] for key in allowed if key in os.environ}


def smoke(executable, environment):
    auth = subprocess.run(
        [executable, "login", "status"],
        env=environment,
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    if auth.returncode or "Logged in using ChatGPT" not in auth.stdout + auth.stderr:
        raise RuntimeError("ChatGPT subscription authentication is required; API auth is refused.")
    expected = {
        "schema_version": "1",
        "job_id": "subscription-smoke",
        "revision": 0,
        "context_digest": "0" * 64,
        "role": "software-engineer",
        "actor": "smoke-engineer",
        "host": "codex",
        "model": "subscription-default-not-qualified",
        "outcome": "failure",
        "summary": "Connectivity check only; no implementation or qualification claimed.",
        "artifacts": [],
        "evidence": [],
    }
    with tempfile.TemporaryDirectory(prefix="software-core-live-") as directory:
        output = Path(directory) / "response.json"
        command = [
            executable,
            "exec",
            "--ignore-user-config",
            "--ignore-rules",
            "--ephemeral",
            "--skip-git-repo-check",
            "--sandbox",
            "read-only",
            "--json",
            "-c",
            'forced_login_method="chatgpt"',
            "-c",
            "features.shell_tool=false",
            "-c",
            'web_search="disabled"',
            "--output-last-message",
            str(output),
            "-",
        ]
        result = subprocess.run(
            command,
            cwd=directory,
            env=environment,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
            input="Use no tools. Return exactly this JSON, without fences:\n"
            + json.dumps(expected),
        )
        if result.returncode:
            raise RuntimeError("Codex session failed; no API fallback was attempted.")
        response = Contribution.model_validate_json(output.read_text())
        if response.model_dump(mode="json") != expected:
            raise RuntimeError("The host did not satisfy the requested response contract.")
    return {
        "host": "codex",
        "authentication": "ChatGPT",
        "schema_check": "pass",
        "scope": "connectivity only; not agent competence or end-to-end development",
    }


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--confirm-subscription-usage", action="store_true", required=True)
    cli.parse_args()
    executable = shutil.which("codex")
    if not executable:
        raise SystemExit("Codex CLI is unavailable. Install it and sign in with ChatGPT.")
    print(json.dumps(smoke(executable, subscription_environment()), indent=2))


if __name__ == "__main__":
    main()
