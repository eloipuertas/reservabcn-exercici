# Team playbook: from spec to merge with agents

## Roles

| Role | Who | Does |
|------|-----|------|
| Member | each student | Owns one spec. Runs a coder agent on it. Reads the whole diff. Opens the pull request. |
| Lead | one student | Owns shared contracts and `app/main.py`. Reviews agent and CI settings. |
| Product owner | one student or the teacher | Approves specs (`Status: active`). Owner of `/specs/`. |
| Coder agent | one per member | Implements one spec in one worktree. |
| QA agent | shared | Reviews a pull request against its spec. Read-only. |
| Organizer agent | shared | Proposes tasks and assignments, updates progress files, flags overlaps. |

## Day-one checklist

- [ ] Ownership table filled in (`specs/ownership.md`): one spec, one set of files per member.
- [ ] `.github/CODEOWNERS` has real teams or users.
- [ ] Branch rules on `main`: pull request, status check `test`, code owner review.
- [ ] `AGENTS.md` fits your project (commands, boundaries). Under about 200 lines.
- [ ] Everyone can run `pytest` and `ruff check .` locally.
- [ ] Tiny rehearsal: one trivial feature through the whole path before the real work starts.

## For each feature

1. **Write the spec** (human). Use `specs/_template/spec.md`. Requirements have IDs, one trigger and one response. Add Out of scope and a verify command.
2. **Ask the agent to read it back** before it codes: which files, which formulas or rules, which assumptions? Fix misunderstandings in the spec, not in the code.
3. **Get tasks**. Ask the organizer to draft `progress/proposed/<feature>-tasks.md`. Review it. If approved, copy it to `specs/<feature>/tasks.md`.
4. **Approve the spec**: set `Status: active` in a pull request that the owners of `/specs/` review.
5. **Create the worktree**: `scripts/new_agent_worktree.sh <feature>`.
6. **Run the coder agent** in that folder, with the spec and the task list as input.
7. **Read the diff** yourself. If it did something the spec did not ask for, remove it or change the spec.
8. **Open the pull request** and fill in the template.
9. **CI and QA agent run.** Fix red CI by giving the failing output to your agent. Treat the QA agent's comment as advice.
10. **Human review** by a code owner. Approve, or request changes with a reason.
11. **Merge**, then `scripts/remove_agent_worktree.sh <feature>` and update `progress/progress.md`.

## When things go wrong

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Two pull requests conflict | Two specs touched the same file | Split the file or move the shared part into its own pull request (shared contract). |
| The agent adds an unrequested endpoint | Spec has no Out of scope | Add it to the spec; delete the extra code. |
| The agent keeps asking questions | Spec is silent or ambiguous | Answer in the spec (new requirement ID), not in chat. |
| The agent stops after the first task | No feature list or progress file | Use `progress/features.json` and `progress.md`; tell the agent to read them first. |
| CI does not start on the agent's commit | Commits pushed with the default workflow token do not trigger workflows | Push as a user, or use a GitHub App token. |
| An action is denied | `.claude/settings.json` deny rule | Intended. Ask the owner of the file instead of working around it. |
