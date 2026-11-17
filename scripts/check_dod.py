#!/usr/bin/env python3
"""Check the documentation part of the Definition of Done.

DOD-01  Every route of the app has a section `## METHOD /path` in docs/api.md.
DOD-02  CHANGELOG.md has a `## [Unreleased]` section, and every active spec folder
        is named somewhere in CHANGELOG.md.

Exit code 0 when everything is in place, 1 otherwise.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SECTION = re.compile(r"^#{2,3}\s+([A-Z]+)\s+(/\S*)\s*$", re.MULTILINE)
STATUS = re.compile(r"^Status:\s*(\w+)", re.MULTILINE)
IGNORED_METHODS = {"HEAD", "OPTIONS"}


def documented_endpoints(api_text: str) -> set[tuple[str, str]]:
    """Return the (METHOD, path) pairs that have a section in docs/api.md."""
    return {(method, path) for method, path in SECTION.findall(api_text)}


def app_endpoints(app) -> set[tuple[str, str]]:
    """Return the (METHOD, path) pairs the FastAPI app really serves.

    The OpenAPI schema is used because it lists the routes of included routers in every
    FastAPI version (the internal list of routes changes between versions).
    """
    paths = app.openapi().get("paths", {})
    return {
        (method.upper(), path)
        for path, operations in paths.items()
        for method in operations
        if method.upper() not in IGNORED_METHODS and method.lower() != "parameters"
    }


def active_specs(specs_dir: Path) -> list[str]:
    names = []
    for spec in sorted(specs_dir.glob("*/spec.md")):
        if spec.parent.name.startswith("_"):
            continue
        match = STATUS.search(spec.read_text(encoding="utf-8"))
        if match and match.group(1).lower() == "active":
            names.append(spec.parent.name)
    return names


def check(
    endpoints: set[tuple[str, str]], api_text: str, changelog_text: str, specs: list[str]
) -> list[str]:
    problems = []
    documented = documented_endpoints(api_text)
    for method, path in sorted(endpoints - documented):
        problems.append(f"DOD-01 docs/api.md has no section '## {method} {path}'")
    if not re.search(r"^##\s+\[Unreleased\]", changelog_text, flags=re.MULTILINE | re.IGNORECASE):
        problems.append("DOD-02 CHANGELOG.md has no '## [Unreleased]' section")
    for name in specs:
        # The name must stand alone: `edit-party` is not mentioned by `edit-party-rules`.
        if not re.search(rf"(?<![\w-]){re.escape(name)}(?![\w-])", changelog_text):
            problems.append(f"DOD-02 CHANGELOG.md does not mention the spec '{name}'")
    return problems


def main() -> int:
    sys.path.insert(0, str(ROOT))
    from app.main import app  # imported here so the tests of this file do not need the app

    problems = check(
        app_endpoints(app),
        (ROOT / "docs" / "api.md").read_text(encoding="utf-8"),
        (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"),
        active_specs(ROOT / "specs"),
    )
    for problem in problems:
        print(f"FAIL   {problem}")
    if not problems:
        print("ok     docs/api.md and CHANGELOG.md are up to date")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
