import json

import pytest

from scripts.check_mutations import check as mutations
from scripts.check_mutations import diff_digest
from scripts.check_secrets import scan
from scripts.check_test_report import check as report_passed


def test_mutation_gate_rejects_missing_surviving_and_incomplete_results(tmp_path):
    assert not mutations([])["passed"]
    path = tmp_path / "sample.meta"
    for statuses, passed in [
        ({"a": 1}, True),
        ({"a": 0}, False),
        ({"a": None}, False),
        ({"a": -9}, False),
    ]:
        path.write_text(json.dumps({"exit_code_by_key": statuses}))
        assert mutations([path])["passed"] is passed


def test_secret_scan_detects_injected_credential_without_echoing_it(tmp_path):
    path = tmp_path / "fixture.py"
    # Construct a synthetic signature at runtime so the repository contains no token.
    synthetic = "AKIA" + "A" * 16
    path.write_text(f'aws_access_key_id = "{synthetic}"\n')
    findings = scan([str(path)])
    assert findings
    assert synthetic not in json.dumps(findings)
    assert scan([str(tmp_path / "missing")]) == []


def test_equivalence_is_diff_bound_and_never_excuses_an_incomplete_run(tmp_path):
    path = tmp_path / "policy.py.meta"
    statuses = {str(i): 1 for i in range(5)} | {"equivalent": 0}
    path.write_text(json.dumps({"exit_code_by_key": statuses}))
    review = {"equivalent": {"reason": "Same wire representation", "diff_sha256": "abc"}}
    assert mutations([path], review, lambda _: "abc", required={"policy"})["passed"]
    assert not mutations([path], review, lambda _: "changed")["passed"]
    assert not mutations([path], review, lambda _: "abc", required={"context"})["passed"]
    assert not mutations([path, path], review, lambda _: "abc")["passed"]
    review["equivalent"]["reason"] = ""
    assert not mutations([path], review, lambda _: "abc")["passed"]
    review["equivalent"]["reason"] = "Same wire representation"
    for status in (None, -9, 1):
        statuses["equivalent"] = status
        path.write_text(json.dumps({"exit_code_by_key": statuses}))
        assert not mutations([path], review, lambda _: "abc")["passed"]


def test_equivalents_do_not_inflate_raw_score(tmp_path):
    path = tmp_path / "policy.py.meta"
    path.write_text(json.dumps({"exit_code_by_key": {"a": 1, "b": 0}}))
    result = mutations([path], {"b": {"reason": "Equivalent", "diff_sha256": "x"}}, lambda _: "x")
    assert result["raw_score"] == 50
    assert not result["passed"]


def test_diff_hash_ignores_status_but_not_mutation():
    diff = "--- file\n+++ file\n@@\n-a\n+b\n"
    assert diff_digest("# survived\n" + diff) == diff_digest("# killed\n" + diff)
    assert diff_digest("# survived\n" + diff) != diff_digest("# survived\n" + diff + "+c\n")
    with pytest.raises(ValueError):
        diff_digest("not a mutation")


def test_skipped_empty_and_failed_test_reports_block(tmp_path):
    path = tmp_path / "report.xml"
    for body, passed in [
        ("<testcase/>", True),
        ("", False),
        ("<testcase><skipped/></testcase>", False),
        ("<testcase><failure/></testcase>", False),
        ("<testcase><error/></testcase>", False),
    ]:
        path.write_text(f"<testsuite>{body}</testsuite>")
        assert report_passed(path) is passed
