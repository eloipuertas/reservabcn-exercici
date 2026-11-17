# The harness and its guardrails

## Vocabulary

- **Harness**: everything around the model. The loop and context management, tools, instructions, permissions, hooks, memory files, and the outer loop of CI and people.
- **Guardrails**: the part of the harness whose job is to limit or check what the agent does. They are not a separate thing next to the harness; they are inside it.
- **Capabilities** are the other part of the harness: they make the agent able to work (loop, tools, memory). They are not guardrails.
- A **soft guardrail** is advice the agent may ignore (instructions). A **hard guardrail** is enforced by the tool or by the repository, whether or not the agent read the rule (permissions, hooks, budgets, CI with human review).

"Guardrails" is the word the course and the industry use for the blockers an agent should have. Product documentation usually speaks of permissions, hooks and settings, so do not expect to find the word there.

When an agent misbehaves, change the harness before blaming the model.

## Where each part of the harness lives

| Part | Kind | File | Notes |
|------|------|------|-------|
| Instructions | Soft guardrail | `AGENTS.md`, `CLAUDE.md` | Loaded every session. Advice, not enforcement. Keep short and specific. |
| Role | Capability (its tool list also limits) | `.claude/agents/*.md` | Frontmatter: name, description, tools, model. Body: the role's system prompt. Own context window. |
| Permissions | Hard guardrail | `.claude/settings.json` | Allow, ask, deny. Evaluated deny, then ask, then allow; first match wins. |
| Hooks | Hard guardrail | `.claude/hooks/*.py` + `settings.json` | Run at fixed points. Exit code 2 blocks. Used here: no commits on `main`; no stopping with red tests. |
| Budgets | Hard guardrail | `claude_args` in workflows (`--max-turns`), `timeout-minutes` | Caps cost and time in CI. |
| Memory | Capability | `progress/features.json`, `progress/progress.md`, git history | Notes that survive between sessions. |
| Outer loop | Hard guardrail | `.github/` | CI, CODEOWNERS, PR template, branch rules. A person still has to review. |

## Failure modes of long-running agents, and the fix in this repo

| Failure | Fix |
|---------|-----|
| Tries to do everything at once | One task per commit; feature list; one spec per agent |
| Declares the project done too early | `passes: false` until tests pass on `main` |
| Leaves half-done, undocumented work | `progress/progress.md` entry at the end of every session; descriptive commits |
| Marks things done without testing | Rule in `AGENTS.md`; Stop hook runs the tests; CI re-runs them |
| Wastes time finding the commands | Commands listed in `AGENTS.md` |

## Changing the harness safely

Weakening a guardrail is the riskiest change: treat removing a rule, a permission or a CI step as a security change.

1. Make the change in its own pull request (the files are CODEOWNERS-protected).
2. Say what failure it addresses. A rule without a failure behind it is clutter.
3. Rehearse on a tiny feature before the team relies on it.
4. Re-read it every few weeks: contradictory or outdated rules lead to arbitrary behaviour.

## Porting to another tool

Keep `AGENTS.md`, `specs/`, CI and CODEOWNERS as they are. Re-create the role files, permissions and hooks in the other tool's format. Check whether it reads `AGENTS.md` directly.

## Sources

- Anthropic, Building effective agents.
- Anthropic, Effective harnesses for long-running agents.
- agents.md (the AGENTS.md format).
- Claude Code documentation: memory (CLAUDE.md), subagents, hooks, permissions, GitHub Actions.
- GitHub documentation: About code owners, About protected branches.
- Git documentation: git-worktree.
