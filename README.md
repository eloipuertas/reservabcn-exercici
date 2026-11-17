# reservabcn-exercici

Repository for the exercise session "From the user story to the code, and from the code to the process"
(Software Engineering, Universitat de Barcelona). It is the ReservaBCN API from the course slides
"Agents, Teams and CI", plus what the exercise needs. The instructions are on the student sheet, not here.

Tool-agnostic parts: `AGENTS.md`, `specs/`, CI, CODEOWNERS, `scripts/`. Claude Code specific parts:
`CLAUDE.md` and `.claude/`. If your agent tool reads another file, point it at `AGENTS.md`.

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
git init -b main && git add . && git commit -m "starter"
git switch -c feat/edit-party
pytest -q                                # 46 tests, all green
```

## The commands of the project

| Command | What it checks |
|---------|----------------|
| `pytest -q` | Tests of the API and of the checkers in `scripts/` |
| `ruff check .` | Lint |
| `python scripts/check_req_coverage.py` | Every requirement ID of an active spec has a test |
| `python scripts/check_dod.py` | `docs/api.md` and `CHANGELOG.md` are up to date (used in part 2) |
| `python scripts/check_guardrails.py` | The guardrails around deployment hold (used in part 3) |
| `python scripts/check_no_secrets.py` | No secrets in the files of the repository (used in part 3) |

## Layout

```
AGENTS.md  CLAUDE.md          Rules for the coding agent
specs/                        constitution, ownership table, one folder per feature
app/  tests/                  The API and its tests
docs/api.md  CHANGELOG.md     Documentation that the Definition of Done will require
deploy/                       Image and deployment script (course stubs, they print only)
.github/workflows/            ci.yml and deploy.yml
.github/CODEOWNERS            Who must approve changes to which paths
.claude/                      Role files, permissions and hooks (Claude Code only)
scripts/                      Checkers and worktree helpers
```

## Notes

- Nothing here deploys anything. `deploy/deploy.sh` only prints. The secrets in `deploy/.env.prod` are fake.
- The workflows were not run on GitHub for this exercise repository. The branch rules and the
  environment gate need a real GitHub repository and admin rights; the exercise only edits the files.
