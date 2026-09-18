import json

import pytest

from scripts import check_coverage, check_quality


def test_complexity_and_size_boundaries():
    for decisions, blocked, warned in [
        (9, False, False),
        (10, False, True),
        (14, False, True),
        (15, True, False),
    ]:
        source = (
            "def branch(x):\n"
            + "".join(f"    if x == {i}:\n        return {i}\n" for i in range(decisions))
            + "    return -1\n"
        )
        errors, warnings, metrics = check_quality.complexity_findings(source, "sample.py")
        assert any("cyclomatic" in e for e in errors) is blocked
        assert any("cyclomatic" in w for w in warnings) is warned
        assert metrics
    nested = "def nested(x):\n" + "".join("    " * i + "if x:\n" for i in range(1, 7))
    nested += "    " * 7 + "return 1\n"
    errors, warnings, _ = check_quality.complexity_findings(nested, "sample.py")
    assert any("cognitive" in e for e in errors)
    assert any("nesting" in w for w in warnings)
    large = "def large():\n" + "    x = 1\n" * 61 + "x = 1\n" * 501
    errors, warnings, _ = check_quality.complexity_findings(large, "sample.py")
    assert not errors
    assert any("function size" in w for w in warnings)
    assert any("file size" in w for w in warnings)


def test_class_methods_are_measured():
    source = "class Example:\n    def method(self, x):\n        if x:\n            return 1\n"
    _, _, metrics = check_quality.complexity_findings(source, "class.py")
    assert {m["function"] for m in metrics} == {"method"}
    assert any(m.get("cyclomatic") == 2 for m in metrics)


def test_dependency_cycles_and_reverse_edges_fail():
    assert check_quality.dependency_errors({("service", "contracts")}) == []
    assert check_quality.dependency_errors({("contracts", "service")})
    assert check_quality.dependency_errors({("unknown", "contracts")})
    assert check_quality.dependency_errors({("service", "context"), ("context", "service")})
    source = (
        "from . import __version__\nfrom .contracts import Job\n"
        "import software_creator_core.service\nfrom software_creator_core.files import digest\n"
    )
    assert check_quality.import_edges("cli", source) == {
        ("cli", "__init__"),
        ("cli", "contracts"),
        ("cli", "service"),
        ("cli", "files"),
    }


def test_quality_report_and_main(tmp_path, monkeypatch, capsys):
    root = tmp_path / "src/software_creator_core"
    root.mkdir(parents=True)
    (root / "contracts.py").write_text("from .cli import main\n")
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts/check.py").write_text("def example():\n    return 1\n")
    monkeypatch.chdir(tmp_path)
    assert check_quality.main() == 1
    assert "point inward" in capsys.readouterr().out


@pytest.fixture
def coverage_record():
    return {
        "executed_lines": [1, 2, 3, 4],
        "missing_lines": [5],
        "executed_branches": [[2, 3]],
        "missing_branches": [[2, 5]],
    }


def test_separate_coverage_floors(coverage_record):
    counts = check_coverage.scope_counts(coverage_record)
    assert counts == (4, 5, 1, 2)
    errors = check_coverage.failures("example", counts, 90, 85)
    assert len(errors) == 2
    assert check_coverage.scope_counts(coverage_record, {1}) == (1, 1, 0, 0)
    assert check_coverage.percent(0, 0) == 100
    assert check_coverage.failures("empty", (0, 0, 0, 0), 90, 85) == []


def test_changed_lines_handles_new_and_existing_files(tmp_path, monkeypatch):
    path = tmp_path / "sample.py"
    path.write_text("old\nnew\n")
    assert check_coverage.changed_lines(path, None) == {1, 2}
    monkeypatch.setattr(check_coverage, "previous_file", lambda *args: "old\n")
    assert check_coverage.changed_lines(path, "base") == {2}


def test_missing_production_coverage_fails():
    result = check_coverage.check({"files": {"tests/test.py": {}}}, {"line": 0, "branch": 0})
    assert result["errors"] == ["No production coverage was measured"]


def test_changed_critical_code_and_baseline_ratchet(coverage_record, monkeypatch):
    monkeypatch.setattr(check_coverage, "changed_lines", lambda *args: {1, 2, 3, 4, 5})
    result = check_coverage.check(
        {"files": {"src/software_creator_core/policy.py": coverage_record}},
        {"line": 98, "branch": 97},
    )
    assert any("< 95" in error for error in result["errors"])
    assert any("< 90" in error for error in result["errors"])
    assert any("< 98" in error for error in result["errors"])
    assert any("< 97" in error for error in result["errors"])


def test_coverage_main_rejects_invalid_base(monkeypatch):
    monkeypatch.setattr("sys.argv", ["check_coverage", "--base", "main"])
    with pytest.raises(SystemExit) as caught:
        check_coverage.main()
    assert caught.value.code == 2


def test_coverage_main_uses_previous_baseline(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "coverage.json").write_text(json.dumps({"files": {}}))
    (tmp_path / "quality-baseline.json").write_text('{"line":80,"branch":75}')
    monkeypatch.setattr("sys.argv", ["check_coverage", "--base", "a" * 40])
    monkeypatch.setattr(check_coverage.subprocess, "run", lambda *args, **kwargs: None)
    monkeypatch.setattr(check_coverage, "previous_file", lambda *args: '{"line":99,"branch":98}')
    assert check_coverage.main() == 1
    assert "No production coverage" in capsys.readouterr().out


def test_previous_file_runs_bounded_git_lookup(monkeypatch):
    import subprocess

    monkeypatch.setattr(
        check_coverage.subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess([], 0, stdout="old source"),
    )
    assert check_coverage.previous_file("a" * 40, "source.py") == "old source"
    monkeypatch.setattr(
        check_coverage.subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess([], 128, stdout=""),
    )
    assert check_coverage.previous_file("a" * 40, "source.py") == ""
