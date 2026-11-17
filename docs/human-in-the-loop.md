# Human in the loop: where people decide

Principle: automate whatever is checkable, keep people for judgment and responsibility.

| Gate | Enforced by | Human involved |
|------|-------------|----------------|
| Spec becomes `active` | CODEOWNERS on `/specs/` + branch rule "Require review from Code Owners" | Product owner |
| Agent may not edit specs, CI, agent files | `.claude/settings.json` deny rules (and CODEOWNERS as the second line) | Lead owns the files |
| Agent may not push or merge | deny rules `Bash(git push *)`, `Bash(git merge *)`; hook blocks commits on `main` | Member pushes |
| Lint and tests pass | CI job `test`, required status check | None (machine) |
| Every requirement ID has a test | `scripts/check_req_coverage.py` in CI | None (machine) |
| Diff matches the spec | QA agent (advisory comment) | Reviewer reads it |
| Right problem solved | Pull request review | Code owner |
| Merge | Branch rule: pull request + status checks + code owner approval | Code owner |

## Reviewer checklist

1. Read the spec first, then the diff. Do not start from the agent's summary.
2. Is every requirement ID covered by a test that would fail if the code were wrong?
3. Is there anything in the diff that no requirement asked for?
4. Are boundaries tested (for example exactly 2 hours before the start)?
5. Could one diner see or change another diner's data?
6. Did the QA agent miss anything, or raise a false alarm? Note it: it improves the role file.

## What humans never delegate

- Changing a spec's meaning.
- Accepting a change to a shared contract.
- Merging.
- Turning a safety rule off because "it is in the way".

## Two weak spots to know about

- Approval fatigue: a reviewer who clicks approve without reading defeats the gate. Keep pull requests small.
- Self-grading: an agent that checks its own work shares its own blind spots. That is why the QA agent has a separate context and read-only tools, and why CI runs independently of both.
