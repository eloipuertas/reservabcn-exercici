"""Tests for check_no_secrets.py. Fake secrets are built at run time, so this file stays clean."""

import importlib.util
import subprocess
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "check_no_secrets.py"
_spec = importlib.util.spec_from_file_location("check_no_secrets", SCRIPT)
scanner = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(scanner)

AWS = "AKIA" + "IOSFODNN7" + "EXAMPLE"
TOKEN = "prod_live_" + "9f8e7d6c5b4a3928"


def test_aws_key_is_found():
    assert scanner.scan_text(f"KEY={AWS}") == [(1, "aws-access-key")]


def test_token_assignment_is_found():
    assert scanner.scan_text(f"DEPLOY_TOKEN={TOKEN}") == [(1, "secret-assignment")]


def test_password_in_url_is_found():
    text = "DATABASE_URL=postgresql://user:" + "s3cr3t-pass" + "@db.example.com/app"
    assert scanner.scan_text(text) == [(1, "password-in-url")]


def test_placeholders_and_github_secret_references_are_ignored():
    text = "DEPLOY_TOKEN=CHANGE_ME_please_1234567\nenv: DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}\n"
    assert scanner.scan_text(text) == []


def test_message_does_not_contain_the_secret(tmp_path):
    (tmp_path / ".env.prod").write_text(f"DEPLOY_TOKEN={TOKEN}\n")
    problems = scanner.scan(tmp_path)
    assert len(problems) == 1
    assert TOKEN not in problems[0]


def test_example_files_and_ignored_files_are_skipped(tmp_path):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / ".gitignore").write_text(".env.prod\n")
    (tmp_path / ".env.prod").write_text(f"DEPLOY_TOKEN={TOKEN}\n")
    (tmp_path / ".env.prod.example").write_text(f"DEPLOY_TOKEN={TOKEN}\n")
    assert scanner.scan(tmp_path) == []
