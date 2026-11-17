#!/usr/bin/env python3
"""Test the guardrails around deployment, like a test suite for the rules of the game.

GR-01  deploy.yml: every job that deploys is tied to the GitHub Environment `production`.
GR-02  deploy.yml: permissions are declared and are not `write-all`.
GR-03  deploy.yml: it never runs on pull requests, and pushes only from `main`.
GR-04  deploy.yml: every `uses:` is pinned to a version tag or a commit SHA.
GR-05  deploy.yml: it does not print secrets or pipe downloads into a shell.
GR-06  CODEOWNERS: deployment files and these checks have their own owners.
GR-07  AGENTS.md: the Boundaries section forbids touching deploy/ and secrets.
GR-08  .claude/settings.json (only if it exists): deny rules for deploy/.
GR-09  ci.yml runs this check and check_no_secrets.py.

Exit code 0 when every guardrail holds, 1 otherwise. A skipped check is not a failure.
"""

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PINNED = re.compile(r"@(v\d[\w.]*|[0-9a-f]{40})$")
PROTECTED_PATHS = ["/deploy/", "/.github/workflows/deploy.yml", "/scripts/check_guardrails.py"]


def load_workflow(path: Path) -> dict | None:
    if not path.exists():
        return None
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    # YAML 1.1 reads the key `on` as the boolean True.
    if True in data and "on" not in data:
        data["on"] = data.pop(True)
    return data


def check_deploy_workflow(wf: dict | None, raw_text: str) -> list[str]:
    if wf is None:
        return ["GR-01 .github/workflows/deploy.yml does not exist"]
    problems = []
    jobs = wf.get("jobs") or {}

    # GR-01 every job runs inside the protected environment.
    for name, job in jobs.items():
        env = job.get("environment")
        env_name = env.get("name") if isinstance(env, dict) else env
        if env_name != "production":
            problems.append(f"GR-01 job '{name}' is not tied to the environment 'production'")

    # GR-02 permissions declared, not write-all.
    top = wf.get("permissions")
    declared = top is not None or all("permissions" in j for j in jobs.values())
    values = [top] + [j.get("permissions") for j in jobs.values()]
    if not declared:
        problems.append("GR-02 no permissions declared: the token gets the default permissions")
    if "write-all" in values:
        problems.append("GR-02 permissions is 'write-all'")

    # GR-03 triggers.
    triggers = wf.get("on") or {}
    if isinstance(triggers, str):
        triggers = {triggers: {}}
    elif isinstance(triggers, list):
        triggers = {name: {} for name in triggers}
    for bad in ("pull_request", "pull_request_target"):
        if bad in triggers:
            problems.append(f"GR-03 deploy.yml runs on {bad}")
    if "push" in triggers:
        push = triggers["push"] or {}
        if push.get("branches") != ["main"] or push.get("tags") or push.get("branches-ignore"):
            problems.append("GR-03 push must be limited to branches: [main]")

    # GR-04 pinned actions.
    for name, job in jobs.items():
        for step in job.get("steps") or []:
            ref = step.get("uses")
            if ref and not ref.startswith("./") and not PINNED.search(ref):
                problems.append(f"GR-04 '{ref}' in job '{name}' is not pinned to a tag or SHA")

    # GR-05 secrets and downloads.
    if re.search(r"(echo|printf|cat)[^\n]*\$\{\{\s*secrets\.", raw_text):
        problems.append("GR-05 a step prints a secret")
    if re.search(r"(curl|wget)[^\n|]*\|\s*(sudo\s+)?(ba)?sh", raw_text):
        problems.append("GR-05 a step pipes a download into a shell")
    return problems


def check_codeowners(text: str | None) -> list[str]:
    if text is None:
        return ["GR-06 .github/CODEOWNERS does not exist"]
    rules: dict[str, list[str]] = {}
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            pattern, *owners = line.split()
            rules[pattern] = owners  # the last matching line wins, as on GitHub
    default = set(rules.get("*", []))
    problems = []
    for path in PROTECTED_PATHS:
        owners = rules.get(path)
        if not owners:
            problems.append(f"GR-06 CODEOWNERS has no owner for {path}")
        elif set(owners) == default:
            problems.append(f"GR-06 {path} has the same owners as the default '*' rule")
    return problems


def boundaries_section(agents_md: str) -> str:
    match = re.search(r"^##\s+Boundaries\s*\n(.*?)(?=^##\s|\Z)", agents_md, re.M | re.S)
    return match.group(1) if match else ""


def check_agents_md(text: str | None) -> list[str]:
    if text is None:
        return ["GR-07 AGENTS.md does not exist"]
    section = boundaries_section(text)
    problems = []
    if "deploy/" not in section:
        problems.append("GR-07 Boundaries do not mention deploy/")
    if not re.search(r"secret", section, re.IGNORECASE):
        problems.append("GR-07 Boundaries do not mention secrets")
    return problems


def check_claude_settings(text: str | None) -> list[str]:
    if text is None:
        return []  # this team uses another tool: its own deny rules are not checked here
    deny = json.loads(text).get("permissions", {}).get("deny", [])
    problems = []
    if not any(rule.startswith(("Edit(deploy", "Write(deploy")) for rule in deny):
        problems.append("GR-08 .claude/settings.json does not deny editing deploy/")
    if not any(rule.startswith("Bash(") and "deploy" in rule for rule in deny):
        problems.append("GR-08 .claude/settings.json does not deny running deploy scripts")
    return problems


def check_ci(text: str | None) -> list[str]:
    if text is None:
        return ["GR-09 .github/workflows/ci.yml does not exist"]
    problems = []
    for script in ("check_guardrails.py", "check_no_secrets.py"):
        if script not in text:
            problems.append(f"GR-09 ci.yml does not run scripts/{script}")
    return problems


def read(path: Path) -> str | None:
    return path.read_text(encoding="utf-8") if path.exists() else None


def run(root: Path) -> list[str]:
    deploy = root / ".github" / "workflows" / "deploy.yml"
    problems = check_deploy_workflow(load_workflow(deploy), read(deploy) or "")
    problems += check_codeowners(read(root / ".github" / "CODEOWNERS"))
    problems += check_agents_md(read(root / "AGENTS.md"))
    problems += check_claude_settings(read(root / ".claude" / "settings.json"))
    problems += check_ci(read(root / ".github" / "workflows" / "ci.yml"))
    return problems


def main() -> int:
    problems = run(ROOT)
    for problem in problems:
        print(f"FAIL   {problem}")
    if not problems:
        print("ok     all guardrails hold")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
