@AGENTS.md

## Claude Code

- The role files are in `.claude/agents/`: `coder`, `qa-reviewer`, `organizer`. Use the `coder` role for implementation work.
- Permissions and hooks are in `.claude/settings.json`. They enforce the Boundaries section of AGENTS.md; do not try to work around a denied action, report it instead.
- Use plan mode before touching any shared contract file.
