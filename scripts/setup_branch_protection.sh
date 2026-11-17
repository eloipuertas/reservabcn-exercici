#!/usr/bin/env bash
# Turn on the human-in-the-loop gates for the main branch with the GitHub CLI.
#
#   scripts/setup_branch_protection.sh OWNER/REPO
#
# Needs admin rights on the repository and `gh auth login`. Read the JSON below before you run it:
# it also applies to administrators (enforce_admins) and needs the CI job named "test".
# You can set the same rules by hand: Settings > Branches (or Rulesets) > main.
set -euo pipefail

repo="${1:?usage: scripts/setup_branch_protection.sh OWNER/REPO}"

gh api --method PUT "repos/${repo}/branches/main/protection" --input - <<'JSON'
{
  "required_status_checks": { "strict": true, "contexts": ["test"] },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 1,
    "require_code_owner_reviews": true,
    "dismiss_stale_reviews": true
  },
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
JSON

echo "Branch protection set on ${repo}:main"
