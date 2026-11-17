"""Tests for check_req_coverage.py (the CI traceability check).

This file lives in scripts/, not tests/, on purpose: the check scans tests/ for requirement IDs,
and the fixture strings below must not count as coverage.
"""

import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "check_req_coverage.py"
_spec = importlib.util.spec_from_file_location("check_req_coverage", SCRIPT)
checker = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(checker)


def make_repo(tmp_path, status, spec_ids, test_text):
    spec_dir = tmp_path / "specs" / "demo"
    spec_dir.mkdir(parents=True)
    lines = [f"- **{i}** WHEN x, the system SHALL y." for i in spec_ids]
    (spec_dir / "spec.md").write_text(f"# Spec\n\nStatus: {status}\n\n" + "\n".join(lines))
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    (tests_dir / "test_demo.py").write_text(test_text)
    return tmp_path / "specs", tests_dir


def test_all_requirements_covered(tmp_path):
    specs, tests = make_repo(tmp_path, "active", ["REQ-01", "REQ-02"], '"""REQ-01"""\n# req_02\n')
    assert checker.check(specs, tests) == []


def test_missing_requirement_is_reported(tmp_path):
    specs, tests = make_repo(tmp_path, "active", ["REQ-01", "REQ-02"], '"""REQ-01"""\n')
    problems = checker.check(specs, tests)
    assert len(problems) == 1
    assert "REQ-02" in problems[0]


def test_draft_specs_are_skipped(tmp_path):
    specs, tests = make_repo(tmp_path, "draft", ["REQ-01"], "")
    assert checker.check(specs, tests) == []


def test_prefix_must_match_exactly(tmp_path):
    # NOREQ-01 in a test must not count as covering REQ-01.
    specs, tests = make_repo(tmp_path, "active", ["REQ-01"], "# NOREQ-01\n")
    assert len(checker.check(specs, tests)) == 1


def test_active_spec_without_ids_fails(tmp_path):
    specs, tests = make_repo(tmp_path, "active", [], "")
    assert len(checker.check(specs, tests)) == 1


def add_spec(tmp_path, name, ids, status="active"):
    spec_dir = tmp_path / "specs" / name
    spec_dir.mkdir(parents=True)
    lines = [f"- **{i}** WHEN x, the system SHALL y." for i in ids]
    (spec_dir / "spec.md").write_text(f"# Spec\n\nStatus: {status}\n\n" + "\n".join(lines))


def test_only_checks_the_named_spec(tmp_path):
    specs, tests = make_repo(tmp_path, "active", ["REQ-01"], '"""REQ-01"""')
    add_spec(tmp_path, "other", ["OTH-01"])  # active and not covered
    assert len(checker.check(specs, tests)) == 1
    assert checker.check(specs, tests, only=["demo"]) == []


def test_only_reports_a_missing_requirement_of_the_named_spec(tmp_path):
    specs, tests = make_repo(tmp_path, "active", ["REQ-01", "REQ-02"], '"""REQ-01"""')
    problems = checker.check(specs, tests, only=["demo"])
    assert len(problems) == 1
    assert "REQ-02" in problems[0]


def test_only_with_an_unknown_name_is_a_problem(tmp_path):
    specs, tests = make_repo(tmp_path, "active", ["REQ-01"], '"""REQ-01"""')
    problems = checker.check(specs, tests, only=["typo"])
    assert len(problems) == 1
    assert "no such spec" in problems[0]
