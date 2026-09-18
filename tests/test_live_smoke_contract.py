"""Offline tests for the opt-in host check; no host process or credentials are used."""

import json
import subprocess
from pathlib import Path

import pytest

from scripts.live_codex_smoke import smoke, subscription_environment


def test_api_credentials_are_not_forwarded(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "synthetic-key")
    monkeypatch.setenv("CODEX_API_KEY", "synthetic-key")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "synthetic-key")
    environment = subscription_environment()
    assert not any("API_KEY" in key for key in environment)


def test_api_authentication_is_refused(monkeypatch):
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            [], 0, "Logged in using an API key", ""
        ),
    )
    with pytest.raises(RuntimeError, match="subscription"):
        smoke("codex", {})


@pytest.mark.parametrize("mode", ["valid", "error", "wrong"])
def test_process_contract_and_failure_paths(monkeypatch, mode):
    def run(command, **kwargs):
        assert kwargs["timeout"] <= 60
        assert "shell" not in kwargs
        if command[1] == "login":
            return subprocess.CompletedProcess(command, 0, "Logged in using ChatGPT", "")
        assert "--ignore-user-config" in command
        assert "read-only" in command
        assert 'forced_login_method="chatgpt"' in command
        assert "features.shell_tool=false" in command
        expected = json.loads(kwargs["input"].split("\n", 1)[1])
        if mode == "wrong":
            expected["actor"] = "another"
        Path(command[command.index("--output-last-message") + 1]).write_text(json.dumps(expected))
        return subprocess.CompletedProcess(command, 1 if mode == "error" else 0, "", "")

    monkeypatch.setattr(subprocess, "run", run)
    if mode == "valid":
        assert smoke("codex", {})["schema_check"] == "pass"
    else:
        with pytest.raises(RuntimeError):
            smoke("codex", {})
