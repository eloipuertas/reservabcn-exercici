#!/usr/bin/env python3
"""Look for secrets in the files of the repository (a small teaching scanner, not a product).

It scans the files git knows about (tracked, or untracked but not ignored). Without git it
walks the folder. Files named `*.example` and obvious placeholders are skipped.
A real project should add a maintained scanner (gitleaks, trufflehog, GitHub secret scanning).

Exit code 0 when nothing is found, 1 otherwise. The message never prints the secret itself.
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache", "node_modules"}
RULES = [
    ("aws-access-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("private-key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")),
    ("password-in-url", re.compile(r"://[^/\s:@]+:[^/\s@]{6,}@")),
    (
        "secret-assignment",
        re.compile(
            r"\b[A-Z0-9_]*(?:TOKEN|SECRET|PASSWORD|API_KEY)[A-Z0-9_]*\s*[=:]\s*['\"]?([A-Za-z0-9_\-]{16,})"
        ),
    ),
]
PLACEHOLDER = re.compile(
    r"(change[-_]?me|your[-_]|example|placeholder|<.*>|\$\{|xxxx)", re.IGNORECASE
)


def candidate_files(root: Path) -> list[Path]:
    """Files git knows about, or every file under root when git is not available."""
    try:
        out = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            cwd=root,
            capture_output=True,
            check=True,
        ).stdout.decode()
        return [root / name for name in out.split("\0") if name]
    except (OSError, subprocess.CalledProcessError):
        return [
            p
            for p in root.rglob("*")
            if p.is_file() and not (set(p.relative_to(root).parts) & SKIP_DIRS)
        ]


def scan_text(text: str) -> list[tuple[int, str]]:
    """Return (line number, rule name) for each suspicious line."""
    findings = []
    for number, line in enumerate(text.splitlines(), start=1):
        for name, pattern in RULES:
            match = pattern.search(line)
            if not match:
                continue
            if name == "secret-assignment" and PLACEHOLDER.search(match.group(0)):
                continue
            findings.append((number, name))
    return findings


def scan(root: Path) -> list[str]:
    problems = []
    for path in sorted(candidate_files(root)):
        if path.name.endswith(".example") or not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue  # binary or unreadable
        for number, rule in scan_text(text):
            problems.append(f"SEC {path.relative_to(root)}:{number} looks like a secret ({rule})")
    return problems


def main() -> int:
    problems = scan(ROOT)
    for problem in problems:
        print(f"FAIL   {problem}")
    if not problems:
        print("ok     no secrets found")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
