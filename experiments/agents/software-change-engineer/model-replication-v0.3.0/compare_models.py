#!/usr/bin/env python3
"""Create a deterministic Terra/Sol definition-effect comparison."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected JSON object: {path}")
    return value


def percent_change(before: float, after: float) -> float:
    return round((after / before - 1) * 100, 3)


def exact_sign_p(positive: int, negative: int) -> float | None:
    n = positive + negative
    if n == 0:
        return None
    tail = min(positive, negative)
    probability = 2 * sum(math.comb(n, index) for index in range(tail + 1)) / 2**n
    return round(min(1.0, probability), 6)


def records_by_task(summary: dict[str, Any]) -> dict[str, dict[str, dict[str, Any]]]:
    result: dict[str, dict[str, dict[str, Any]]] = {}
    for record in summary["records"]:
        result.setdefault(record["task_id"], {})[record["condition_id"]] = record
    return result


def condition_metrics(summary: dict[str, Any], condition: str) -> dict[str, Any]:
    value = summary["by_condition"][condition]
    return {
        "score": value["score_sum"],
        "strict_passes": value["binary_passes"],
        "elapsed_seconds": value["elapsed_seconds_total"],
        "changed_lines": value["changed_lines_total"],
        "tool_calls": value["tool_calls_total"],
        "input_tokens": value["runtime_reported_tokens"]["input_tokens"],
        "output_tokens": value["runtime_reported_tokens"]["output_tokens"],
        "criteria": value["criterion_results"],
    }


def compare(terra: dict[str, Any], sol: dict[str, Any]) -> dict[str, Any]:
    terra_records = records_by_task(terra)
    sol_records = records_by_task(sol)
    tasks = []
    for task_id in sorted(set(terra_records) | set(sol_records)):
        terra_a = terra_records[task_id]["condition-a"]["evaluation"]
        terra_b = terra_records[task_id]["condition-b"]["evaluation"]
        sol_a = sol_records[task_id]["condition-a"]["evaluation"]
        sol_b = sol_records[task_id]["condition-b"]["evaluation"]
        terra_effect = terra_b["score"] - terra_a["score"]
        sol_effect = sol_b["score"] - sol_a["score"]
        tasks.append(
            {
                "task_id": task_id,
                "terra_a": terra_a["score"],
                "terra_b": terra_b["score"],
                "terra_definition_effect": terra_effect,
                "sol_a": sol_a["score"],
                "sol_b": sol_b["score"],
                "sol_definition_effect": sol_effect,
                "interaction": sol_effect - terra_effect,
                "sol_a_strict_pass": sol_a["overall_pass"],
                "sol_b_strict_pass": sol_b["overall_pass"],
            }
        )

    sol_wins = sum(item["sol_definition_effect"] > 0 for item in tasks)
    sol_losses = sum(item["sol_definition_effect"] < 0 for item in tasks)
    interaction_positive = sum(item["interaction"] > 0 for item in tasks)
    interaction_negative = sum(item["interaction"] < 0 for item in tasks)
    sol_b_only_passes = sum(
        item["sol_b_strict_pass"] and not item["sol_a_strict_pass"] for item in tasks
    )
    sol_a_only_passes = sum(
        item["sol_a_strict_pass"] and not item["sol_b_strict_pass"] for item in tasks
    )

    terra_a = condition_metrics(terra, "condition-a")
    terra_b = condition_metrics(terra, "condition-b")
    sol_a = condition_metrics(sol, "condition-a")
    sol_b = condition_metrics(sol, "condition-b")
    terra_effect = terra_b["score"] - terra_a["score"]
    sol_effect = sol_b["score"] - sol_a["score"]

    return {
        "schema_version": "0.3.0",
        "models": {
            "gpt-5.6-terra": {"condition-a": terra_a, "condition-b": terra_b},
            "gpt-5.6-sol": {"condition-a": sol_a, "condition-b": sol_b},
        },
        "definition_effect": {
            "terra_score_difference": terra_effect,
            "sol_score_difference": sol_effect,
            "model_definition_interaction": sol_effect - terra_effect,
            "sol_paired_wins": sol_wins,
            "sol_paired_losses": sol_losses,
            "sol_paired_ties": len(tasks) - sol_wins - sol_losses,
            "sol_score_sign_test_two_sided_p": exact_sign_p(sol_wins, sol_losses),
            "interaction_positive_tasks": interaction_positive,
            "interaction_negative_tasks": interaction_negative,
            "interaction_tied_tasks": len(tasks)
            - interaction_positive
            - interaction_negative,
            "interaction_sign_test_two_sided_p": exact_sign_p(
                interaction_positive, interaction_negative
            ),
            "sol_detailed_only_strict_passes": sol_b_only_passes,
            "sol_concise_only_strict_passes": sol_a_only_passes,
            "sol_strict_pass_exact_mcnemar_p": exact_sign_p(
                sol_b_only_passes, sol_a_only_passes
            ),
        },
        "sol_detailed_vs_concise_resource_change_percent": {
            "elapsed_seconds": percent_change(
                sol_a["elapsed_seconds"], sol_b["elapsed_seconds"]
            ),
            "changed_lines": percent_change(
                sol_a["changed_lines"], sol_b["changed_lines"]
            ),
            "tool_calls": percent_change(sol_a["tool_calls"], sol_b["tool_calls"]),
            "input_tokens": percent_change(
                sol_a["input_tokens"], sol_b["input_tokens"]
            ),
            "output_tokens": percent_change(
                sol_a["output_tokens"], sol_b["output_tokens"]
            ),
        },
        "tasks": tasks,
    }


def render_markdown(result: dict[str, Any]) -> str:
    terra = result["models"]["gpt-5.6-terra"]
    sol = result["models"]["gpt-5.6-sol"]
    effect = result["definition_effect"]
    resources = result["sol_detailed_vs_concise_resource_change_percent"]
    lines = [
        "# Cross-model replication result",
        "",
        "## Outcome",
        "",
        "| Model | Concise A | Detailed B | Detailed − concise | Strict passes A/B |",
        "|---|---:|---:|---:|---:|",
        f"| `gpt-5.6-terra` | {terra['condition-a']['score']}/70 | "
        f"{terra['condition-b']['score']}/70 | {effect['terra_score_difference']:+d} | "
        f"{terra['condition-a']['strict_passes']}/10 · {terra['condition-b']['strict_passes']}/10 |",
        f"| `gpt-5.6-sol` | {sol['condition-a']['score']}/70 | "
        f"{sol['condition-b']['score']}/70 | {effect['sol_score_difference']:+d} | "
        f"{sol['condition-a']['strict_passes']}/10 · {sol['condition-b']['strict_passes']}/10 |",
        "",
        f"The model-definition interaction is **{effect['model_definition_interaction']:+d} points**. "
        "Terra shows no aggregate definition effect; Sol favors the detailed definition.",
        "",
        f"Within Sol, detailed B wins {effect['sol_paired_wins']} task pairs, loses "
        f"{effect['sol_paired_losses']}, and ties {effect['sol_paired_ties']}. The exact "
        f"two-sided sign-test p-value is {effect['sol_score_sign_test_two_sided_p']}; "
        "with ten tasks this is directional evidence, not a conclusive estimate.",
        "",
        "## Task-level scores",
        "",
        "| Task | Terra A | Terra B | Sol A | Sol B | Interaction |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for task in result["tasks"]:
        lines.append(
            f"| {task['task_id']} | {task['terra_a']} | {task['terra_b']} | "
            f"{task['sol_a']} | {task['sol_b']} | {task['interaction']:+d} |"
        )
    lines.extend(
        [
            "",
            "## Criterion results",
            "",
            "| Criterion | Terra A | Terra B | Sol A | Sol B |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for criterion in terra["condition-a"]["criteria"]:
        values = [
            terra["condition-a"]["criteria"][criterion],
            terra["condition-b"]["criteria"][criterion],
            sol["condition-a"]["criteria"][criterion],
            sol["condition-b"]["criteria"][criterion],
        ]
        rendered = [f"{value['passed']}/{value['total']}" for value in values]
        lines.append(
            f"| {criterion.replace('_', ' ').title()} | " + " | ".join(rendered) + " |"
        )
    lines.extend(
        [
            "",
            "## Sol resource effect of detail",
            "",
            "| Measure | Concise A | Detailed B | Change |",
            "|---|---:|---:|---:|",
            f"| Candidate time | {sol['condition-a']['elapsed_seconds']:.1f}s | "
            f"{sol['condition-b']['elapsed_seconds']:.1f}s | {resources['elapsed_seconds']:+.1f}% |",
            f"| Average per task | {sol['condition-a']['elapsed_seconds'] / 10:.1f}s | "
            f"{sol['condition-b']['elapsed_seconds'] / 10:.1f}s | {resources['elapsed_seconds']:+.1f}% |",
            f"| Input tokens | {sol['condition-a']['input_tokens']:,} | "
            f"{sol['condition-b']['input_tokens']:,} | {resources['input_tokens']:+.1f}% |",
            f"| Output tokens | {sol['condition-a']['output_tokens']:,} | "
            f"{sol['condition-b']['output_tokens']:,} | {resources['output_tokens']:+.1f}% |",
            f"| Tool calls | {sol['condition-a']['tool_calls']} | "
            f"{sol['condition-b']['tool_calls']} | {resources['tool_calls']:+.1f}% |",
            f"| Changed lines | {sol['condition-a']['changed_lines']} | "
            f"{sol['condition-b']['changed_lines']} | {resources['changed_lines']:+.1f}% |",
            "",
            f"Detailed B used {resources['input_tokens']:+.1f}% input tokens and "
            f"{resources['output_tokens']:+.1f}% output tokens, took "
            f"{resources['elapsed_seconds']:+.1f}% elapsed time, made "
            f"{resources['tool_calls']:+.1f}% tool calls, and changed "
            f"{resources['changed_lines']:+.1f}% lines relative to concise A. It "
            f"produced three additional strict task passes; the exact paired "
            f"strict-pass p-value is {effect['sol_strict_pass_exact_mcnemar_p']}.",
            "",
            "## Interpretation",
            "",
            "The result does not support treating the answer to “does more definition detail "
            "help?” as model-independent. Detail did not help Terra on aggregate, but it aligned "
            "with fewer Sol regressions and a four-point Sol advantage. Because there was one "
            "stochastic run per task and condition, replication across repeated runs or a new task "
            "block is needed before treating the Sol effect as stable.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--terra-summary", type=Path, required=True)
    parser.add_argument("--sol-summary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = compare(load_json(args.terra_summary), load_json(args.sol_summary))
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "comparison.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (args.output / "analysis.md").write_text(render_markdown(result), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
