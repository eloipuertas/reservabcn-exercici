#!/usr/bin/env python3
"""PreToolUse hook: refuse `git commit` while the checked-out branch is main or master.

Claude Code sends the event as JSON on stdin. Exit code 2 blocks the tool call and the
text written to stderr is shown to the agent as the reason.
"""

import subprocess
import sys

branch = subprocess.run(
    ["git", "branch", "--show-current"], capture_output=True, text=True, check=False
).stdout.strip()

if branch in ("main", "master"):
    print(
        f"Blocked: you are on '{branch}'. Work in your own worktree and branch "
        "(see scripts/new_agent_worktree.sh).",
        file=sys.stderr,
    )
    sys.exit(2)

sys.exit(0)
