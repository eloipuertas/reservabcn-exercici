"""Tests for check_dod.py (documentation part of the Definition of Done)."""

import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "check_dod.py"
_spec = importlib.util.spec_from_file_location("check_dod", SCRIPT)
dod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dod)

API = "# API\n\n## GET /things\n\ntext\n\n### DELETE /things/{id}\n"
CHANGELOG = "# Changelog\n\n## [Unreleased]\n\n- `demo`: something\n"


def test_everything_documented():
    endpoints = {("GET", "/things"), ("DELETE", "/things/{id}")}
    assert dod.check(endpoints, API, CHANGELOG, ["demo"]) == []


def test_undocumented_endpoint_is_reported():
    endpoints = {("GET", "/things"), ("PATCH", "/things/{id}")}
    problems = dod.check(endpoints, API, CHANGELOG, [])
    assert problems == ["DOD-01 docs/api.md has no section '## PATCH /things/{id}'"]


def test_missing_unreleased_heading_is_reported():
    problems = dod.check(set(), API, "# Changelog\n\n## [0.1.0]\n", [])
    assert any("[Unreleased]" in p for p in problems)


def test_spec_not_in_changelog_is_reported():
    problems = dod.check(set(), API, CHANGELOG, ["demo", "edit-party"])
    assert problems == ["DOD-02 CHANGELOG.md does not mention the spec 'edit-party'"]


def test_a_spec_name_inside_a_longer_name_does_not_count():
    changelog = "## [Unreleased]\n- `edit-party-rules`: who can change\n"
    problems = dod.check(set(), "", changelog, ["edit-party", "edit-party-rules"])
    assert len(problems) == 1
    assert "'edit-party'" in problems[0]


def test_active_specs_skips_drafts_and_templates(tmp_path):
    for name, status in [("a", "active"), ("b", "draft"), ("_template", "active")]:
        folder = tmp_path / name
        folder.mkdir()
        (folder / "spec.md").write_text(f"# Spec\n\nStatus: {status}\n")
    assert dod.active_specs(tmp_path) == ["a"]


def test_app_endpoints_ignores_docs_routes():
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/ping")
    def ping():
        return {}

    assert dod.app_endpoints(app) == {("GET", "/ping")}


def test_app_endpoints_sees_routes_of_included_routers():
    from fastapi import APIRouter, FastAPI

    router = APIRouter()

    @router.patch("/things/{id}")
    def change(id: int):
        return {}

    app = FastAPI()
    app.include_router(router)
    assert dod.app_endpoints(app) == {("PATCH", "/things/{id}")}
