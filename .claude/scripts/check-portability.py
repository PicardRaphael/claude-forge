#!/usr/bin/env python3
"""Detecte ce qui casse quand on change de machine.

Usage : py .claude/scripts/check-portability.py [chemin_repo]
Exit  : 0 = portable  ·  1 = au moins un blocage (chainable avant un commit)

Raphael travaille sur DEUX PC : noms d'utilisateur et arborescences differents,
certains repos absents d'un cote. Un chemin absolu code en dur y echoue —
souvent SILENCIEUSEMENT, ce qui est pire qu'un crash.

Recidives mesurees (le garde-fou etait propose dans le vault, jamais implemente) :
- mai 2026 : chemins absolus dans settings.json
- 29 juil. 2026 : 3 scripts/*.bat pointaient vers C:\\Users\\rapha\\ (l'AUTRE PC)
  donc casses sur cette machine ; mcp-forge-brain/start.bat epinglait un
  Python313 qui n'existe plus ici ; 26 hooks neo_ia lances par `python` nu.

Trois familles verifiees :
  1. CHEMIN ABSOLU vers un dossier utilisateur (fail dur ou silencieux)
  2. INTERPRETEUR non portable — `python`/`python3` au lieu du launcher `py`
     (peut resoudre vers l'alias Microsoft Store selon la machine, et le hook
     echoue sans erreur). Les hooks en bun/node/deno sont LEGITIMES.
  3. HOOK SANS TIMEOUT — freeze indefini de la session
"""
import glob
import json
import os
import re
import sys

# Chemin absolu vers un dossier utilisateur, quel que soit le nom du user.
# `...` exclu : `C:/Users/...` est une ELLIPSE de documentation, pas un chemin.
_ABS_USER = re.compile(r"[A-Za-z]:[\\/]+Users[\\/]+(?!\.\.\.)[A-Za-z0-9._-]+", re.I)

# Une ligne qui INTERDIT le chemin absolu est un contre-exemple pedagogique,
# pas une violation : `windows-hooks.md` dit precisement « jamais C:/Users/... ».
_TEACHING = re.compile(
    r"\b(?:jamais|never|pas\s+de|interdit|éviter|eviter|au\s+lieu\s+de|"
    r"instead|faux|wrong|❌|anti-pattern|ne\s+pas)\b",
    re.I,
)

# Fichiers ou un chemin absolu est attendu / sans consequence.
_SKIP_PARTS = (
    os.sep + "_backups" + os.sep,
    os.sep + "node_modules" + os.sep,
    os.sep + ".venv" + os.sep,
    os.sep + "worktrees" + os.sep,
    os.sep + "output" + os.sep,
    os.sep + "logs" + os.sep,
    ".proposed",
    "settings.local.json",     # gitignore par design, machine-local
    "check-portability.py",    # anti self-lock : sa doc cite les incidents
)

_SCAN_GLOBS = (
    ".claude/settings.json",
    ".claude/hooks/*.py",
    ".claude/hooks/*.ts",
    ".claude/scripts/*.py",
    ".claude/rules/*.md",
    ".claude/skills/*/SKILL.md",
    ".claude/skills/*/scripts/*",
    ".claude/agents/*.md",
    "scripts/*.bat",
    "scripts/*.sh",
    "scripts/*.py",
    "*.bat",
    "CLAUDE.md",
    "memory/*.md",
    ".mcp.json",
)


def skipped(path):
    return any(part in path for part in _SKIP_PARTS)


def check_abs_paths(root):
    """Famille 1 : chemins absolus vers un dossier utilisateur."""
    out = []
    for pattern in _SCAN_GLOBS:
        for path in glob.glob(os.path.join(root, pattern)):
            if skipped(path) or not os.path.isfile(path):
                continue
            try:
                lines = open(path, encoding="utf-8-sig", errors="replace").read().splitlines()
            except OSError:
                continue
            for num, line in enumerate(lines, 1):
                if _TEACHING.search(line):
                    continue
                m = _ABS_USER.search(line)
                if m:
                    out.append((os.path.relpath(path, root), num, m.group(0)))
    return out


def check_hooks(root):
    """Familles 2 et 3 : interpreteur non portable, timeout absent."""
    settings = os.path.join(root, ".claude", "settings.json")
    if not os.path.isfile(settings):
        return [], []
    try:
        data = json.load(open(settings, encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        return [("settings.json", 0, f"JSON illisible: {exc}")], []

    bad_interp, no_timeout = [], []
    for event, groups in (data.get("hooks") or {}).items():
        for group in groups or []:
            for hook in group.get("hooks", []) or []:
                cmd = hook.get("command")
                if not cmd:
                    continue
                first = cmd.strip().split()[0].strip('"').lower()
                base = os.path.basename(first)
                if base in ("python", "python3", "python.exe", "python3.exe"):
                    bad_interp.append((event, cmd[:80]))
                if "timeout" not in hook:
                    no_timeout.append((event, cmd[:80]))
    return bad_interp, no_timeout


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    abs_paths = check_abs_paths(root)
    bad_interp, no_timeout = check_hooks(root)

    if not (abs_paths or bad_interp or no_timeout):
        print("[OK] portable — aucun chemin absolu, interpreteurs et timeouts conformes")
        return 0

    if abs_paths:
        print(f"[FAIL] {len(abs_paths)} chemin(s) absolu(s) vers un dossier utilisateur :")
        for path, num, frag in abs_paths[:25]:
            print(f"  {path}:{num}  -> {frag}")
        if len(abs_paths) > 25:
            print(f"  … et {len(abs_paths) - 25} autre(s)")
        print("  Fix : ${CLAUDE_PROJECT_DIR} (settings.json) · %~dp0 (.bat) ·")
        print("        __file__ / import.meta.dir (script) · git rev-parse --show-toplevel")

    if bad_interp:
        print(f"\n[FAIL] {len(bad_interp)} hook(s) lances par `python` au lieu de `py` :")
        for event, cmd in bad_interp[:15]:
            print(f"  [{event}] {cmd}")
        print("  Fix : `py` (launcher PEP 514) — `python` peut pointer vers")
        print("        l'alias Microsoft Store et le hook echoue SANS erreur.")

    if no_timeout:
        print(f"\n[FAIL] {len(no_timeout)} hook(s) sans `timeout` (freeze indefini possible) :")
        for event, cmd in no_timeout[:15]:
            print(f"  [{event}] {cmd}")

    return 1


if __name__ == "__main__":
    sys.exit(main())
