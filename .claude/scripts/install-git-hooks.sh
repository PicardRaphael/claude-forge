#!/bin/sh
# Installe les git hooks versionnés de .claude/scripts/ vers .git/hooks/.
# .git/ n'étant pas versionné, relancer ce script après un clone.
# Idempotent : recopie + chmod à chaque exécution.
#
# Usage : sh .claude/scripts/install-git-hooks.sh

set -e

# Racine du repo (résolu via git, fonctionne quel que soit le cwd)
REPO_ROOT=$(git rev-parse --show-toplevel)
HOOKS_DST="$REPO_ROOT/.git/hooks"
HOOKS_SRC="$REPO_ROOT/.claude/scripts"

install_hook() {
  name=$1
  cp "$HOOKS_SRC/$name" "$HOOKS_DST/$name"
  chmod +x "$HOOKS_DST/$name" 2>/dev/null || true
  echo "[install-git-hooks] $name installé dans .git/hooks/"
}

install_hook pre-commit

echo "[install-git-hooks] OK."
