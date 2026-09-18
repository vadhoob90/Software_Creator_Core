"""ES-001: cyclomatic/cognitive complexity, cohesion signals and inward dependencies."""

import ast
import json
from pathlib import Path

from cognitive_complexity.api import get_cognitive_complexity
from radon.complexity import cc_visit
from radon.raw import analyze

LAYERS = {
    "__init__": 0,
    "contracts": 0,
    "errors": 0,
    "files": 1,
    "roles": 1,
    "policy": 1,
    "storage": 2,
    "context": 2,
    "evidence": 2,
    "hosts": 3,
    "service": 3,
    "cli": 4,
}
CONTROL = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.Try, ast.With, ast.AsyncWith, ast.Match)


def nesting(node, depth=0):
    current = depth + int(isinstance(node, CONTROL))
    return max([current, *(nesting(child, current) for child in ast.iter_child_nodes(node))])


def complexity_findings(source, filename):
    tree = ast.parse(source)
    errors, warnings, measurements = [], [], []
    blocks = cc_visit(source)
    functions = [b for b in blocks if not hasattr(b, "methods")]
    for block in functions:
        measurements.append(
            {"file": filename, "function": block.name, "cyclomatic": block.complexity}
        )
        if block.complexity > 15:
            errors.append(f"{filename}:{block.lineno}: cyclomatic {block.complexity} > 15")
        elif block.complexity > 10:
            warnings.append(f"{filename}:{block.lineno}: review cyclomatic {block.complexity}")
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            failed, review, measurement = function_findings(node, source, filename)
            errors.extend(failed)
            warnings.extend(review)
            measurements.append(measurement)
    if analyze(source).lloc > 500:
        warnings.append(f"{filename}: review file size > 500")
    return errors, warnings, measurements


def function_findings(node, source, filename):
    cognitive = get_cognitive_complexity(node)
    errors, warnings = [], []
    if cognitive > 15:
        errors.append(f"{filename}:{node.lineno}: cognitive {cognitive} > 15")
    if nesting(node) > 4:
        warnings.append(f"{filename}:{node.lineno}: review nesting > 4")
    if analyze(ast.get_source_segment(source, node)).lloc > 60:
        warnings.append(f"{filename}:{node.lineno}: review function size > 60")
    return errors, warnings, {"file": filename, "function": node.name, "cognitive": cognitive}


def import_edges(module, source):
    edges = set()
    for node in ast.walk(ast.parse(source)):
        edges.update((module, target) for target in import_targets(node))
    return edges


def import_targets(node):
    if isinstance(node, ast.ImportFrom) and node.level:
        return [(node.module or "__init__").split(".")[0]]
    if isinstance(node, ast.Import):
        return [
            name.name.split(".")[1]
            for name in node.names
            if name.name.startswith("software_creator_core.")
        ]
    if isinstance(node, ast.ImportFrom) and (node.module or "").startswith(
        "software_creator_core."
    ):
        return [node.module.split(".")[1]]
    return []


def dependency_errors(edges):
    errors = []
    for source, target in sorted(edges):
        if source not in LAYERS or target not in LAYERS:
            errors.append(f"Undeclared component: {source} -> {target}")
        elif LAYERS[source] <= LAYERS[target]:
            # Strictly descending edges also prove the absence of component cycles.
            errors.append(f"Dependency must point inward: {source} -> {target}")
    return errors


def report(root):
    errors, warnings, measurements, edges = [], [], [], set()
    for path in sorted(root.glob("*.py")):
        source = path.read_text()
        failed, review, metrics = complexity_findings(source, path.name)
        errors.extend(failed)
        warnings.extend(review)
        measurements.extend(metrics)
        edges.update(import_edges(path.stem, source))
    errors.extend(dependency_errors(edges))
    return {
        "errors": errors,
        "review_warnings": warnings,
        "measurements": measurements,
        "exclusions": "Test code and declarative fixtures; scripts checked separately.",
    }


def main():
    result = report(Path("src/software_creator_core"))
    for path in sorted(Path("scripts").glob("*.py")):
        errors, warnings, metrics = complexity_findings(path.read_text(), str(path))
        result["errors"].extend(errors)
        result["review_warnings"].extend(warnings)
        result["measurements"].extend(metrics)
    print(json.dumps(result, indent=2))
    return int(bool(result["errors"]))


if __name__ == "__main__":
    raise SystemExit(main())
