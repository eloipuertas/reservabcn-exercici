#!/usr/bin/env bash
# Course stub: it only prints what a real deployment would do. Nothing leaves your machine.
set -euo pipefail
: "${DEPLOY_TOKEN:?DEPLOY_TOKEN is not set}"
echo "[stub] would push image reservabcn:${GITHUB_SHA:-local} to PRODUCTION"
echo "[stub] would run database migrations on PRODUCTION"
echo "[stub] would switch traffic to the new version"
