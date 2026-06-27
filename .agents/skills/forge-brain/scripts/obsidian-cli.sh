#!/usr/bin/env bash
# Wrapper obsidian CLI — résout le bon binaire selon l'OS et le shell
# Problème : Git Bash sur Windows résout "obsidian" vers Obsidian.exe (GUI)
# au lieu de Obsidian.com (console/CLI). Ce wrapper corrige ça.

resolve_obsidian() {
  # 1. Windows : Obsidian.com (console) > Obsidian.exe (GUI)
  if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    local candidates=(
      "/c/Program Files/Obsidian/Obsidian.com"
      "$LOCALAPPDATA/Programs/Obsidian/Obsidian.com"
      "$APPDATA/../Local/Programs/Obsidian/Obsidian.com"
    )
    for candidate in "${candidates[@]}"; do
      if [[ -f "$candidate" ]]; then
        echo "$candidate"
        return 0
      fi
    done
  fi

  # 2. Fallback : obsidian dans le PATH (macOS, Linux, ou CLI installée globalement)
  if command -v obsidian &>/dev/null; then
    echo "obsidian"
    return 0
  fi

  echo "ERROR: Obsidian CLI introuvable. Vérifier que Obsidian est installé et que 'cli' est activé dans obsidian.json" >&2
  return 1
}

OBSIDIAN_BIN=$(resolve_obsidian) || exit 1
exec "$OBSIDIAN_BIN" "$@"
