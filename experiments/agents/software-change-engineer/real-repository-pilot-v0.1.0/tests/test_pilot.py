from __future__ import annotations

import importlib.util
import json
from pathlib import Path

PILOT_ROOT = Path(__file__).resolve().parents[1]


def load_runner():
    spec = importlib.util.spec_from_file_location(
        "run_pilot", PILOT_ROOT / "run_pilot.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_experiment_references_existing_frozen_artifacts() -> None:
    manifest = json.loads((PILOT_ROOT / "experiment.json").read_text(encoding="utf-8"))

    assert (PILOT_ROOT / manifest["task"]["path"]).is_file()
    assert len(manifest["conditions"]) == 2
    assert manifest["execution_order"] == ["condition-a", "condition-b"]
    for condition in manifest["conditions"]:
        assert (PILOT_ROOT / condition["definition_path"]).is_file()


def test_lock_hashes_every_executed_protocol_artifact() -> None:
    runner = load_runner()
    lock = json.loads((PILOT_ROOT / "experiment.lock.json").read_text(encoding="utf-8"))
    sources = {
        "run_pilot.py": PILOT_ROOT / "run_pilot.py",
        "evaluate_pilot.py": PILOT_ROOT / "evaluate_pilot.py",
        "handoff.schema.json": PILOT_ROOT / "schemas" / "handoff.schema.json",
        "experiment.json": PILOT_ROOT / "experiment.json",
        "task.md": PILOT_ROOT / "tasks" / "LSE-119.md",
    }

    assert set(lock["protocol_sha256"]) == set(sources)
    assert lock["protocol_sha256"] == {
        name: runner.sha256(path) for name, path in sources.items()
    }


def test_conditions_differ_and_task_is_condition_neutral() -> None:
    condition_a = (PILOT_ROOT / "conditions" / "condition-a.md").read_text(
        encoding="utf-8"
    )
    condition_b = (PILOT_ROOT / "conditions" / "condition-b.md").read_text(
        encoding="utf-8"
    )
    task = (PILOT_ROOT / "tasks" / "LSE-119.md").read_text(encoding="utf-8")

    assert condition_a != condition_b
    assert len(condition_b) > len(condition_a)
    assert "condition-a" not in task
    assert "condition-b" not in task
    assert "detailed" not in task.lower()
    assert "concise" not in task.lower()


def test_candidate_prompt_is_stable_and_disallows_external_actions() -> None:
    runner = load_runner()
    prompt = runner.candidate_prompt("# Example task\n")

    assert ".pdlc/agent-definition.md" in prompt
    assert "Do not use network access" in prompt
    assert "Do not commit" in prompt
    assert prompt.count("# Example task") == 1


def test_runtime_telemetry_counts_completed_tool_calls_once(tmp_path) -> None:
    runner = load_runner()
    events = tmp_path / "events.jsonl"
    events.write_text(
        "\n".join(
            [
                json.dumps(
                    {"type": "item.started", "item": {"type": "command_execution"}}
                ),
                json.dumps(
                    {"type": "item.completed", "item": {"type": "command_execution"}}
                ),
                json.dumps(
                    {
                        "type": "turn.completed",
                        "usage": {"input_tokens": 12, "output_tokens": 3},
                    }
                ),
            ]
        ),
        encoding="utf-8",
    )

    assert runner.parse_runtime_events(events) == {
        "event_count": 3,
        "tool_call_count": 1,
        "usage": {"input_tokens": 12, "output_tokens": 3},
    }


def test_handoff_schema_is_strict_json_object() -> None:
    schema = json.loads((PILOT_ROOT / "schemas" / "handoff.schema.json").read_text())

    assert schema["type"] == "object"
    assert schema["additionalProperties"] is False
    assert {"checks", "authority", "unverified_claims"}.issubset(schema["required"])
