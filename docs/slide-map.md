# Slide map: where each slide's idea lives in the repository

| Slide | Idea | Files |
|-------|------|-------|
| A coding agent is a model in a loop | Read, act, observe, decide; verify command as stop signal | `specs/*/spec.md` (Verify section), `AGENTS.md` (Done when) |
| Five things define a coding agent | Rules, tools, permissions, context, done | `AGENTS.md`, `.claude/agents/coder.md`, `.claude/settings.json`, spec |
| AGENTS.md: a README for agents | Short rules file; CLAUDE.md imports it | `AGENTS.md`, `CLAUDE.md` |
| A role is a file | Subagent definition with tools allowlist | `.claude/agents/*.md` |
| Five patterns for combining agents | Chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer | `docs/team-playbook.md` |
| One coding agent per team member | One spec, one branch, one folder | `specs/ownership.md`, `scripts/new_agent_worktree.sh` |
| Each agent works in its own worktree | `git worktree add/list/remove` | `scripts/new_agent_worktree.sh`, `scripts/remove_agent_worktree.sh` |
| Split the work by spec | Ownership table, shared contracts | `specs/ownership.md` |
| From agent pull request to merge | Pipeline of five steps | `.github/workflows/ci.yml`, `.github/pull_request_template.md` |
| What the machine checks and what a human decides | Gate table | `docs/human-in-the-loop.md`, `scripts/check_req_coverage.py` |
| Make the gates impossible to skip | CODEOWNERS + branch rules | `.github/CODEOWNERS`, `scripts/setup_branch_protection.sh` |
| The QA agent checks the work against the spec | Evaluator, read-only | `.claude/agents/qa-reviewer.md`, `.github/workflows/agent-review.yml` |
| The organizer agent coordinates the work | Proposes tasks, tracks progress | `.claude/agents/organizer.md`, `progress/` |
| The harness is everything around the model; guardrails are the part that limits or checks the agent | Layers | `docs/harness.md` |
| Four guardrails you set in files | Instructions, permissions, hooks, budgets | `.claude/settings.json`, `.claude/hooks/`, workflow `claude_args` |
| Memory has to live outside the context | Feature list, progress file | `progress/features.json`, `progress/progress.md` |
| Before the first agent pull request | Start-up checklist | `docs/team-playbook.md` (Day-one checklist) |
