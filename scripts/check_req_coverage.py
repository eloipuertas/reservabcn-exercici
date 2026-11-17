#!/usr/bin/env python3
"""Check that every requirement ID of every active spec appears in the tests.

A spec is a file `specs/<feature>/spec.md`. Requirements are written as `- **REQ-01** ...`.
Only specs with the line `Status: active` are checked; drafts are skipped.
An ID counts as covered when the tests mention it, for example `REQ-01` in a docstring
or `test_req_01_...` in a function name (case and `-` versus `_` do not matter).

With `--spec NAME` (repeatable) only the specs with that folder name are checked. Use it when
several agents work in parallel, each on its own spec: every agent checks its own spec, and the
full check (no `--spec`) runs after the branches are merged.

Exit code 0 when everything is covered, 1 otherwise.
"""

import argparse
import re
import sys
from pathlib import Path

REQUIREMENT = re.compile(r"\*\*([A-Z]+-\d{2,})\*\*")
STATUS = re.compile(r"^Status:\s*(\w+)", re.MULTILINE)


def read_status(spec_text: str) -> str:
    match = STATUS.search(spec_text)
    return match.group(1).lower() if match else "draft"


def requirement_ids(spec_text: str) -> list[str]:
    return REQUIREMENT.findall(spec_text)


def is_covered(requirement_id: str, tests_text: str) -> bool:
    prefix, number = requirement_id.split("-", 1)
    pattern = rf"(?<![A-Za-z0-9]){re.escape(prefix)}[-_]{re.escape(number)}(?![0-9])"
    return re.search(pattern, tests_text, flags=re.IGNORECASE) is not None


def check(specs_dir: Path, tests_dir: Path, only: list[str] | None = None) -> list[str]:
    """Return a list of problems; an empty list means everything is covered.

    `only` limits the check to the specs with those folder names; an unknown name is a problem.
    """
    tests_text = "\n".join(p.read_text(encoding="utf-8") for p in sorted(tests_dir.rglob("*.py")))
    problems: list[str] = []
    if only:
        known = {p.parent.name for p in specs_dir.glob("*/spec.md")}
        problems += [f"{specs_dir / name}: no such spec" for name in only if name not in known]
    for spec_path in sorted(specs_dir.glob("*/spec.md")):
        if spec_path.parent.name.startswith("_"):
            continue  # templates
        if only and spec_path.parent.name not in only:
            continue
        text = spec_path.read_text(encoding="utf-8")
        if read_status(text) != "active":
            print(f"skip   {spec_path.parent.name}: status is not active")
            continue
        ids = requirement_ids(text)
        if not ids:
            problems.append(f"{spec_path}: active spec has no requirement IDs")
            continue
        missing = [i for i in ids if not is_covered(i, tests_text)]
        for requirement_id in missing:
            problems.append(f"{spec_path}: {requirement_id} is not mentioned in any test")
        if not missing:
            print(f"ok     {spec_path.parent.name}: {', '.join(ids)}")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--specs", type=Path, default=Path("specs"))
    parser.add_argument("--tests", type=Path, default=Path("tests"))
    parser.add_argument(
        "--spec", action="append", metavar="NAME", help="check only this spec folder (repeatable)"
    )
    args = parser.parse_args(argv)

    problems = check(args.specs, args.tests, args.spec)
    for problem in problems:
        print(f"FAIL   {problem}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
