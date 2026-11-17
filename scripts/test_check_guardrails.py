"""Tests for check_guardrails.py: a safe workflow passes, and each unsafe change is caught."""

import importlib.util
from pathlib import Path

import yaml

SCRIPT = Path(__file__).resolve().parent / "check_guardrails.py"
_spec = importlib.util.spec_from_file_location("check_guardrails", SCRIPT)
gr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gr)

SAFE = """
name: Deploy
on:
  push:
    branches: [main]
permissions:
  contents: read
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - run: ./deploy/deploy.sh
        env:
          DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
"""


def problems(text):
    data = yaml.safe_load(text)
    if True in data and "on" not in data:
        data["on"] = data.pop(True)
    return gr.check_deploy_workflow(data, text)


def ids(found):
    return sorted({p.split()[0] for p in found})


def test_safe_workflow_has_no_problems():
    assert problems(SAFE) == []


def test_missing_environment_is_caught():
    assert ids(problems(SAFE.replace("    environment: production\n", ""))) == ["GR-01"]


def test_write_all_and_missing_permissions_are_caught():
    write_all = SAFE.replace("permissions:\n  contents: read", "permissions: write-all")
    assert ids(problems(write_all)) == ["GR-02"]
    assert ids(problems(SAFE.replace("permissions:\n  contents: read\n", ""))) == ["GR-02"]


def test_deploying_from_any_branch_or_pull_request_is_caught():
    assert ids(problems(SAFE.replace("[main]", '["**"]'))) == ["GR-03"]
    assert ids(problems(SAFE.replace("push:\n    branches: [main]", "pull_request_target:"))) == [
        "GR-03"
    ]


def test_unpinned_action_is_caught():
    assert ids(problems(SAFE.replace("checkout@v4", "checkout@main"))) == ["GR-04"]
    assert problems(SAFE.replace("checkout@v4", "checkout@" + "a" * 40)) == []


def test_printing_a_secret_is_caught():
    text = SAFE.replace("./deploy/deploy.sh", 'echo "${{ secrets.DEPLOY_TOKEN }}"')
    assert ids(problems(text)) == ["GR-05"]


def test_codeowners_needs_specific_owners():
    full = "* @o/leads\n/deploy/ @o/ops\n/.github/workflows/deploy.yml @o/ops\n"
    full += "/scripts/check_guardrails.py @o/ops\n"
    assert gr.check_codeowners(full) == []
    assert ids(gr.check_codeowners("* @o/leads\n")) == ["GR-06"]
    same_as_default = full.replace("@o/ops", "@o/leads")
    assert ids(gr.check_codeowners(same_as_default)) == ["GR-06"]


def test_agents_md_boundaries_must_mention_deploy_and_secrets():
    ok = "# A\n\n## Boundaries\n\n- Never touch deploy/ or print a secret.\n\n## Style\n"
    assert gr.check_agents_md(ok) == []
    assert ids(gr.check_agents_md("# A\n\n## Boundaries\n\n- Be nice.\n")) == ["GR-07"]
    mention_elsewhere = "# A\n\n## Boundaries\n\n- Be nice.\n\n## Style\n\ndeploy/ secret\n"
    assert ids(gr.check_agents_md(mention_elsewhere)) == ["GR-07"]


def test_claude_settings_are_skipped_when_absent_and_checked_when_present():
    assert gr.check_claude_settings(None) == []
    weak = '{"permissions": {"deny": ["Edit(specs/**)"]}}'
    assert ids(gr.check_claude_settings(weak)) == ["GR-08"]
    strong = '{"permissions": {"deny": ["Edit(deploy/**)", "Bash(./deploy/*)"]}}'
    assert gr.check_claude_settings(strong) == []


def test_ci_must_run_both_checks():
    both = "run: python scripts/check_guardrails.py\nrun: python scripts/check_no_secrets.py"
    assert gr.check_ci(both) == []
    assert ids(gr.check_ci("run: pytest")) == ["GR-09"]
