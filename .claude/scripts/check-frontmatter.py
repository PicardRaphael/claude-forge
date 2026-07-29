#!/usr/bin/env python3
"""Valide le frontmatter YAML des composants .claude/ et memory/.

Usage    : py .claude/scripts/check-frontmatter.py [chemin_repo]
Exit     : 0 = tous valides · 1 = au moins un cassé (chainable avant un commit)

Piege couvert : le motif deux-points-espace dans un scalaire YAML non quote
("Modes: mode=audit", "date : 25 juillet") leve une ScannerError et rend le
composant INVISIBLE silencieusement — ni erreur au chargement, ni warning.
Correctif : remplacer ": " par " — " dans la valeur, ou quoter la chaine.
"""
import glob
import os
import sys

try:
    import yaml
except ImportError:
    print("[SKIP] PyYAML absent — validation impossible (fail-open)")
    sys.exit(0)

PATTERNS = (
    ".claude/skills/*/SKILL.md",
    ".claude/agents/*.md",
    ".claude/rules/*.md",
    "memory/*.md",
)


def iter_files(root):
    for pattern in PATTERNS:
        yield from glob.glob(os.path.join(root, pattern))


def check(path):
    """Retourne None si valide, sinon la première ligne de l'erreur."""
    try:
        text = open(path, encoding="utf-8-sig").read()
    except OSError as exc:
        return f"illisible: {exc}"
    if not text.startswith("---"):
        return None  # pas de frontmatter = légitime pour certains .md
    parts = text.split("---")
    if len(parts) < 3:
        return "frontmatter non fermé"
    try:
        yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        return str(exc).split("\n")[0]
    return None


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    broken, total = [], 0
    for path in sorted(iter_files(root)):
        total += 1
        err = check(path)
        if err:
            broken.append((os.path.relpath(path, root), err))

    if broken:
        print(f"[FAIL] {len(broken)}/{total} frontmatter(s) cassé(s) :")
        for path, err in broken:
            print(f"  {path}\n      -> {err}")
        print("\nCause fréquente : ': ' dans un scalaire non quoté. Remplacer par ' — '.")
        return 1

    print(f"[OK] {total} frontmatters valides")
    return 0


if __name__ == "__main__":
    sys.exit(main())
