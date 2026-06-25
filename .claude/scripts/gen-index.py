#!/usr/bin/env python3
"""Génère .claude/INDEX.md — index déterministe des skills + agents du repo.

But : qu'un agent (Cowork / Claude Code) trouve le bon objet par son NOM EXACT
sans inventer. AUCUN LLM dans la boucle : on parse le frontmatter YAML réel.

Sources de vérité (lecture seule) :
  - name + description  ← premier bloc frontmatter `---...---` de chaque
                          .claude/skills/<nom>/SKILL.md et .claude/agents/<nom>.md
  - triggers (optionnel) ← .claude/.skill-triggers.json (jamais modifié ici)

Sortie : .claude/INDEX.md — tableau par objet : nom | chemin | description | triggers.
Si l'objet n'est pas dans .skill-triggers.json → triggers = "— (dans description)".

Propriétés : déterministe (tri alpha), idempotent, échoue proprement en nommant
le fichier fautif si un frontmatter est absent/malformé.

Usage : py .claude/scripts/gen-index.py [--check]
  (sans arg) régénère .claude/INDEX.md
  --check    n'écrit rien ; exit 1 si INDEX.md serait différent (utile pre-commit/CI)

Windows / cross-machine : chemins via __file__, jamais de chemin absolu en dur.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# --- Chemins, tous dérivés de __file__ (cross-machine) ---
_SCRIPT_DIR = Path(__file__).resolve().parent          # .claude/scripts
_CLAUDE_DIR = _SCRIPT_DIR.parent                        # .claude
_REPO_DIR = _CLAUDE_DIR.parent                          # racine repo

SKILLS_GLOB = "skills/*/SKILL.md"
AGENTS_GLOB = "agents/*.md"
TRIGGERS_PATH = _CLAUDE_DIR / ".skill-triggers.json"
INDEX_PATH = _CLAUDE_DIR / "INDEX.md"

NO_TRIGGER = "— (dans description)"


class FrontmatterError(Exception):
    """Frontmatter absent ou champ requis manquant — porte le chemin fautif."""


def parse_frontmatter(text: str, rel_path: str) -> dict[str, str]:
    """Extrait name + description du PREMIER bloc frontmatter `---...---`.

    Volontairement minimal : on ne lit que le bloc d'en-tête (jamais le body, qui
    peut contenir un faux `description:` dans un template — cas skill-creator).
    Suppose des valeurs mono-ligne (vérifié : 100 % du corpus forge l'est).
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise FrontmatterError(f"{rel_path}: pas de frontmatter (1re ligne != '---')")

    fields: dict[str, str] = {}
    closed = False
    for line in lines[1:]:
        if line.strip() == "---":
            closed = True
            break
        # clé de premier niveau uniquement : "clef: valeur" sans indentation
        if line and not line[0].isspace() and ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            if key in ("name", "description") and key not in fields:
                fields[key] = value.strip()

    if not closed:
        raise FrontmatterError(f"{rel_path}: frontmatter non fermé (pas de '---' final)")
    for required in ("name", "description"):
        if not fields.get(required):
            raise FrontmatterError(f"{rel_path}: champ '{required}' manquant ou vide")
    return fields


def cell(value: str) -> str:
    """Neutralise un texte pour une cellule de tableau Markdown."""
    return value.replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ").strip()


def load_triggers() -> dict[str, str]:
    """{name: 'trig1 · trig2 · ...'} depuis .skill-triggers.json. {} si absent."""
    if not TRIGGERS_PATH.exists():
        return {}
    try:
        data = json.loads(TRIGGERS_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise FrontmatterError(f".skill-triggers.json illisible : {exc}") from exc

    out: dict[str, str] = {}
    for name, entry in data.items():
        if not isinstance(entry, dict):
            continue
        trigs: list[str] = []
        if isinstance(entry.get("triggers"), list):
            trigs = [str(t) for t in entry["triggers"]]
        elif isinstance(entry.get("triggers_by_subject"), dict):
            for subj_list in entry["triggers_by_subject"].values():
                if isinstance(subj_list, list):
                    trigs.extend(str(t) for t in subj_list)
        if trigs:
            out[name] = " · ".join(trigs)
    return out


def collect(glob: str) -> list[dict[str, str]]:
    """Parse tous les fichiers d'un glob. Retourne la liste triée par name."""
    rows: list[dict[str, str]] = []
    for path in sorted((_CLAUDE_DIR).glob(glob)):
        rel = path.relative_to(_REPO_DIR).as_posix()
        fm = parse_frontmatter(path.read_text(encoding="utf-8"), rel)
        rows.append({"name": fm["name"], "path": rel, "description": fm["description"]})
    rows.sort(key=lambda r: r["name"].lower())
    return rows


def render_table(rows: list[dict[str, str]], triggers: dict[str, str]) -> str:
    lines = [
        "| Nom exact | Chemin | Description | Triggers |",
        "|---|---|---|---|",
    ]
    for r in rows:
        trig = triggers.get(r["name"], NO_TRIGGER)
        lines.append(
            f"| `{cell(r['name'])}` | `{cell(r['path'])}` | "
            f"{cell(r['description'])} | {cell(trig)} |"
        )
    return "\n".join(lines)


def build_index() -> str:
    skills = collect(SKILLS_GLOB)
    agents = collect(AGENTS_GLOB)
    triggers = load_triggers()

    parts = [
        "# INDEX — Skills & Agents de claude-forge",
        "",
        "> Généré automatiquement par `.claude/scripts/gen-index.py` "
        "(pre-commit). NE PAS éditer à la main.",
        "> Trouve un objet par son **Nom exact** ci-dessous — jamais d'invention.",
        "",
        f"## Skills ({len(skills)})",
        "",
        render_table(skills, triggers),
        "",
        f"## Agents ({len(agents)})",
        "",
        render_table(agents, triggers),
        "",
    ]
    return "\n".join(parts)


def main() -> int:
    try:
        content = build_index()
    except FrontmatterError as exc:
        print(f"[gen-index] ERREUR : {exc}", file=sys.stderr)
        return 2

    check = "--check" in sys.argv[1:]
    current = INDEX_PATH.read_text(encoding="utf-8") if INDEX_PATH.exists() else None

    if check:
        if current != content:
            print("[gen-index] INDEX.md obsolète — lance py .claude/scripts/gen-index.py", file=sys.stderr)
            return 1
        print("[gen-index] INDEX.md à jour.")
        return 0

    if current == content:
        print("[gen-index] INDEX.md déjà à jour (aucune écriture).")
        return 0

    # newline="\n" : sortie LF stable, pas de CRLF Windows (diff byte-exact)
    INDEX_PATH.write_text(content, encoding="utf-8", newline="\n")
    print(f"[gen-index] INDEX.md régénéré ({len(content)} octets).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
