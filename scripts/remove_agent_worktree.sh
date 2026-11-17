#!/usr/bin/env bash
# Remove the worktree of a feature after its pull request is merged.
# The branch itself is kept; delete it on GitHub (or with `git branch -d`) when you are done.
set -euo pipefail

feature="${1:?usage: scripts/remove_agent_worktree.sh <feature>}"
repo_root="$(git rev-parse --show-toplevel)"
dir="$(dirname "$repo_root")/wt-${feature}"

git -C "$repo_root" worktree remove "$dir"
git -C "$repo_root" worktree prune
echo "Removed $dir"
