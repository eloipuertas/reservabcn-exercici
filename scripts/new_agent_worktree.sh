#!/usr/bin/env bash
# Create an isolated worktree and branch for one agent.
#
#   scripts/new_agent_worktree.sh cancel          -> ../wt-cancel on branch feat/cancel
#   scripts/new_agent_worktree.sh cancel develop  -> same, starting from develop
#
# Then open your coding agent inside the new folder.
set -euo pipefail

feature="${1:?usage: scripts/new_agent_worktree.sh <feature> [base-branch]}"
base="${2:-main}"

repo_root="$(git rev-parse --show-toplevel)"
dir="$(dirname "$repo_root")/wt-${feature}"
branch="feat/${feature}"
spec="${repo_root}/specs/${feature}/spec.md"

if [[ ! -f "$spec" ]]; then
  echo "No spec found at specs/${feature}/spec.md. Write the spec first." >&2
  exit 1
fi
if ! grep -qiE '^Status:[[:space:]]*active' "$spec"; then
  echo "Warning: specs/${feature}/spec.md is not 'Status: active'. The agent should not implement a draft." >&2
fi

git -C "$repo_root" worktree add "$dir" -b "$branch" "$base"

echo
echo "Worktree: $dir"
echo "Branch:   $branch"
echo "Next:     cd \"$dir\" and start your agent. Give it: specs/${feature}/spec.md"
