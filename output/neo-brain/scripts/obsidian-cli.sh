#!/usr/bin/env bash
# Wrapper obsidian CLI — resout le bon binaire selon l'OS et le shell
# Probleme : Git Bash sur Windows resout "obsidian" vers Obsidian.exe (GUI)
# au lieu de Obsidian.com (console/CLI). Ce wrapper corrige ca.

resolve_obsidian() {
  # 1. Windows : Obsidian.com (console) > Obsidian.exe (GUI)
  if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    # Chercher Obsidian.com dans les chemins connus
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

  # 2. Fallback : obsidian dans le PATH (macOS, Linux, ou CLI installee globalement)
  if command -v obsidian &>/dev/null; then
    echo "obsidian"
    return 0
  fi

  echo "ERROR: Obsidian CLI introuvable. Verifier que Obsidian est installe et que 'cli' est active dans obsidian.json" >&2
  return 1
}

OBSIDIAN_BIN=$(resolve_obsidian) || exit 1
exec "$OBSIDIAN_BIN" "$@"
