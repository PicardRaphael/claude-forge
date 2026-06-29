#!/usr/bin/env python3
"""
vault-audit/scripts/audit.py
Walks the forge-brain vault, checks each note quality, outputs a JSON report.

Usage:
  python scripts/audit.py [--vault-path PATH] [--output json|table] [--top N] [--full]
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from datetime import date, datetime

# Windows CP1252 fix
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

VAULT_RELATIVE = "vault/claude-forge"
SKIP_DIRS = {".obsidian", "Templates", ".git", ".claude", "agent-memory"}
SKIP_FILES = {"Bienvenue.md"}

# Frontmatter required fields per type (minimum set)
REQUIRED_FIELDS = ["titre", "resume", "aliases", "type", "derniere-maj", "auteur", "tags"]
OPTIONAL_FIELDS_BY_TYPE = {
    "feature": ["domaine", "sources"],
    "changelog": ["domaine", "sources"],
    "best-practice": ["domaine", "sources"],
    "concurrent": ["domaine", "sources"],
    "modele": ["domaine", "sources"],
    "technique": ["domaine", "sources"],
    "leader": ["role", "affiliation", "sources"],
    "knowledge": ["sources"],
    "prompt": ["domaine", "sources"],
    "erreur": ["sources"],
    "deprecation": ["domaine", "sources"],
}

# Expected sections per folder (template-based)
TEMPLATE_SECTIONS = {
    "01-Claude": ["## Liens"],
    "02-OpenAI": ["## Liens"],
    "03-Google": ["## Liens"],
    "08-xAI": ["## Liens"],
    "09-Anysphere": ["## Liens"],
    "10-Microsoft": ["## Liens"],
    "04-Techniques": ["## Liens"],
    "05-Leaders": ["## Liens"],
    "06-Industrie": ["## Liens"],
    "07-Prompts": ["## Liens"],
    "Knowledge/erreurs": ["## Liens"],
    "Knowledge/syntheses": ["## Liens"],
    "1-Projets": ["## Liens"],
    "2-Casquettes": ["## Liens"],
}

# Scoring weights (sum = 100)
WEIGHTS = {
    "frontmatter_complete": 30,
    "aliases_4plus": 20,
    "resume_informative": 15,
    "tags_structured": 10,
    "wikilinks_not_bare": 10,
    "sections_match": 10,
    "derniere_maj_fresh": 5,
}

STALE_DAYS = 30

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Returns (frontmatter_dict, body_text). frontmatter_dict is {} if not found."""
    if not content.startswith("---"):
        return {}, content
    end = content.find("\n---", 3)
    if end == -1:
        return {}, content
    fm_text = content[3:end].strip()
    body = content[end + 4:].lstrip("\n")
    fm = {}
    current_key = None
    current_list = None
    for line in fm_text.splitlines():
        # List item
        if line.startswith("  - ") or line.startswith("- "):
            item = line.lstrip(" -").strip().strip('"')
            if current_list is not None:
                current_list.append(item)
            continue
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"')
            if val == "" or val is None:
                # Possibly a list follows
                current_list = []
                fm[key] = current_list
                current_key = key
            elif val.startswith("[") and val.endswith("]"):
                # Inline YAML array: [a, b, c]
                inner = val[1:-1]
                items = [v.strip().strip('"').strip("'") for v in inner.split(",") if v.strip()]
                fm[key] = items
                current_key = key
                current_list = None
            else:
                fm[key] = val
                current_key = key
                current_list = None
    return fm, body


def score_note(path: Path, vault_root: Path, all_note_names: set) -> dict:
    """Compute quality score and issues for a single note."""
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        return {"path": str(path.relative_to(vault_root)), "score": 0, "grade": "D",
                "issues": [f"Cannot read file: {e}"], "fm": {}}

    fm, body = parse_frontmatter(content)
    issues = []
    partial_scores = {}

    # --- 1. Frontmatter completeness (30 pts) ---
    missing_fields = [f for f in REQUIRED_FIELDS if f not in fm or fm[f] in ("", [], None)]
    if missing_fields:
        issues.append(f"Frontmatter manquant : {', '.join(missing_fields)}")
        partial_scores["frontmatter_complete"] = max(0, WEIGHTS["frontmatter_complete"] - len(missing_fields) * 5)
    else:
        partial_scores["frontmatter_complete"] = WEIGHTS["frontmatter_complete"]

    # --- 2. Aliases >= 4 (15 pts) ---
    aliases = fm.get("aliases", [])
    if isinstance(aliases, str):
        aliases = [aliases] if aliases else []
    alias_count = len(aliases)
    if alias_count < 4:
        issues.append(f"Aliases insuffisants : {alias_count}/4 minimum")
        partial_scores["aliases_4plus"] = int(WEIGHTS["aliases_4plus"] * alias_count / 4)
    else:
        partial_scores["aliases_4plus"] = WEIGHTS["aliases_4plus"]

    # --- 3. Resume informative (10 pts) ---
    resume = fm.get("resume", "")
    if isinstance(resume, list):
        resume = " ".join(str(r) for r in resume)
    resume = str(resume).strip()
    titre = fm.get("titre", "")
    if isinstance(titre, list):
        titre = " ".join(str(t) for t in titre)
    titre = str(titre).strip()
    if not resume:
        issues.append("Resume vide")
        partial_scores["resume_informative"] = 0
    elif len(resume) < 40:
        issues.append(f"Resume trop court ({len(resume)} chars, min 40)")
        partial_scores["resume_informative"] = 5
    elif resume.lower() == titre.lower():
        issues.append("Resume identique au titre")
        partial_scores["resume_informative"] = 5
    else:
        partial_scores["resume_informative"] = WEIGHTS["resume_informative"]

    # --- 4. Tags structured: #type/X + #domaine/Y (10 pts) ---
    tags = fm.get("tags", [])
    if isinstance(tags, str):
        tags = [tags]
    has_type_tag = any(t.startswith("#type/") for t in tags)
    has_domaine_tag = any(t.startswith("#domaine/") for t in tags)
    note_type = fm.get("type", "")
    # leader + knowledge templates don't require domaine tag
    needs_domaine = note_type not in ("leader", "knowledge", "erreur")
    if not has_type_tag:
        issues.append("Tag #type/X manquant")
        partial_scores["tags_structured"] = 0
    elif needs_domaine and not has_domaine_tag:
        issues.append("Tag #domaine/Y manquant")
        partial_scores["tags_structured"] = 5
    else:
        partial_scores["tags_structured"] = WEIGHTS["tags_structured"]

    # --- 5. Wikilinks not bare URLs (10 pts) ---
    # Check body for [text](url) markdown links (internal)
    bare_internal = re.findall(r'\[([^\]]+)\]\((?!https?://)([^)]+\.md[^)]*)\)', body)
    if bare_internal:
        issues.append(f"Liens internes en markdown ({len(bare_internal)}) — utiliser [[wikilink]]")
        partial_scores["wikilinks_not_bare"] = 0
    else:
        partial_scores["wikilinks_not_bare"] = WEIGHTS["wikilinks_not_bare"]

    # --- 6. Sections match template (10 pts) ---
    # Find the template sections for this folder
    rel = path.relative_to(vault_root)
    folder_key = None
    for key in TEMPLATE_SECTIONS:
        if str(rel).replace("\\", "/").startswith(key):
            folder_key = key
            break
    if folder_key:
        required_sections = TEMPLATE_SECTIONS[folder_key]
        missing_sections = [s for s in required_sections if s not in body]
        if missing_sections:
            issues.append(f"Sections template manquantes : {', '.join(missing_sections)}")
            partial_scores["sections_match"] = 0
        else:
            partial_scores["sections_match"] = WEIGHTS["sections_match"]
    else:
        partial_scores["sections_match"] = WEIGHTS["sections_match"]

    # --- 7. derniere-maj freshness (5 pts) ---
    derniere_maj = fm.get("derniere-maj", "").strip()
    if not derniere_maj:
        issues.append("derniere-maj vide")
        partial_scores["derniere_maj_fresh"] = 0
    else:
        try:
            note_date = datetime.strptime(derniere_maj, "%Y-%m-%d").date()
            delta = (date.today() - note_date).days
            if delta > STALE_DAYS:
                issues.append(f"derniere-maj obsolete ({delta} jours)")
                partial_scores["derniere_maj_fresh"] = 0
            else:
                partial_scores["derniere_maj_fresh"] = WEIGHTS["derniere_maj_fresh"]
        except ValueError:
            issues.append(f"Format derniere-maj invalide : {derniere_maj}")
            partial_scores["derniere_maj_fresh"] = 0

    # --- Compute total score ---
    total = sum(partial_scores.values())
    if total >= 90:
        grade = "A"
    elif total >= 75:
        grade = "B"
    elif total >= 60:
        grade = "C"
    else:
        grade = "D"

    return {
        "path": str(rel).replace("\\", "/"),
        "name": path.stem,
        "score": total,
        "grade": grade,
        "issues": issues,
        "alias_count": alias_count,
        "fm": {k: fm.get(k, "") for k in ["type", "derniere-maj", "resume"]},
    }


def collect_all_note_names(vault_root: Path) -> set:
    """Collect all note stems for broken-link detection."""
    names = set()
    for p in vault_root.rglob("*.md"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        names.add(p.stem)
    return names


def detect_broken_wikilinks(vault_root: Path, all_names: set) -> list[dict]:
    """Find notes that contain [[Links]] pointing to non-existent notes."""
    broken = []
    for p in vault_root.rglob("*.md"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.name in SKIP_FILES:
            continue
        try:
            content = p.read_text(encoding="utf-8")
        except Exception:
            continue
        links = re.findall(r'\[\[([^\]|#]+)', content)
        bad = [l.strip() for l in links if l.strip() not in all_names]
        if bad:
            broken.append({
                "note": str(p.relative_to(vault_root)).replace("\\", "/"),
                "broken_links": bad,
            })
    return broken


def detect_orphans(vault_root: Path) -> list[str]:
    """Find notes with no incoming wikilinks from other notes."""
    # Build backlink map
    all_notes = {}
    for p in vault_root.rglob("*.md"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.name in SKIP_FILES:
            continue
        all_notes[p.stem] = {"path": p, "incoming": 0}

    for p in vault_root.rglob("*.md"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        try:
            content = p.read_text(encoding="utf-8")
        except Exception:
            continue
        links = re.findall(r'\[\[([^\]|#]+)', content)
        for l in links:
            name = l.strip()
            if name in all_notes and all_notes[name]["path"] != p:
                all_notes[name]["incoming"] += 1

    orphans = [
        str(data["path"].relative_to(vault_root)).replace("\\", "/")
        for stem, data in all_notes.items()
        if data["incoming"] == 0
    ]
    return sorted(orphans)


def run_audit(vault_root: Path, top_n: int = None, full: bool = False) -> dict:
    """Main audit runner. Returns full report dict."""
    all_names = collect_all_note_names(vault_root)

    results = []
    for p in sorted(vault_root.rglob("*.md")):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.name in SKIP_FILES:
            continue
        result = score_note(p, vault_root, all_names)
        results.append(result)

    # Sort by score ascending (worst first)
    results.sort(key=lambda r: r["score"])

    broken = detect_broken_wikilinks(vault_root, all_names)
    orphans = detect_orphans(vault_root)

    # Grade distribution
    grade_dist = {"A": 0, "B": 0, "C": 0, "D": 0}
    for r in results:
        grade_dist[r["grade"]] += 1

    # Average score
    avg_score = round(sum(r["score"] for r in results) / len(results), 1) if results else 0

    display = results if full else (results[:top_n] if top_n else results[:10])

    return {
        "total_notes": len(results),
        "avg_score": avg_score,
        "grade_distribution": grade_dist,
        "worst_notes": display,
        "broken_wikilinks": broken,
        "orphan_count": len(orphans),
        "orphans": orphans[:20],  # cap at 20 for readability
    }


def format_table(report: dict) -> str:
    """Render a markdown table report."""
    lines = []
    lines.append(f"# Audit vault forge-brain — {date.today()}")
    lines.append("")
    lines.append(f"**Notes analysées :** {report['total_notes']}  |  **Score moyen :** {report['avg_score']}/100")
    dist = report["grade_distribution"]
    lines.append(f"**Grades :** A={dist['A']}  B={dist['B']}  C={dist['C']}  D={dist['D']}")
    lines.append("")

    # Worst notes table
    lines.append("## Notes à corriger (worst first)")
    lines.append("")
    lines.append("| Note | Grade | Score | Problèmes |")
    lines.append("|------|-------|-------|-----------|")
    for r in report["worst_notes"]:
        name = r["name"][:40]
        problems = "; ".join(r["issues"][:3])
        if len(r["issues"]) > 3:
            problems += f" (+{len(r['issues'])-3})"
        lines.append(f"| {name} | {r['grade']} | {r['score']} | {problems} |")

    lines.append("")

    # Broken wikilinks
    if report["broken_wikilinks"]:
        lines.append("## Wikilinks cassés")
        lines.append("")
        for item in report["broken_wikilinks"][:15]:
            links_str = ", ".join(f"`[[{l}]]`" for l in item["broken_links"][:5])
            lines.append(f"- **{item['note']}** : {links_str}")
        if len(report["broken_wikilinks"]) > 15:
            lines.append(f"- ... et {len(report['broken_wikilinks'])-15} autres")
        lines.append("")

    # Orphans
    if report["orphans"]:
        lines.append(f"## Notes orphelines ({report['orphan_count']} total, top 20)")
        lines.append("")
        for o in report["orphans"][:20]:
            lines.append(f"- {o}")
        lines.append("")

    # Scoring rubric reminder
    lines.append("## Rubrique de scoring")
    lines.append("")
    lines.append("| Critère | Poids |")
    lines.append("|---------|-------|")
    lines.append("| Frontmatter complet (7 champs) | 30 |")
    lines.append("| Aliases ≥ 4 | 20 |")
    lines.append("| Resume informatif (>40 chars, ≠ titre) | 15 |")
    lines.append("| Tags #type/X + #domaine/Y | 10 |")
    lines.append("| Wikilinks internes (pas markdown) | 10 |")
    lines.append("| Sections template respectées | 10 |")
    lines.append("| derniere-maj < 30 jours | 5 |")
    lines.append("| **A** ≥ 90  **B** ≥ 75  **C** ≥ 60  **D** < 60 | |")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Audit forge-brain vault notes")
    parser.add_argument("--vault-path", default=None, help="Absolute path to vault root")
    parser.add_argument("--output", choices=["json", "table"], default="table")
    parser.add_argument("--top", type=int, default=None, help="Show top N worst notes (default 10)")
    parser.add_argument("--full", action="store_true", help="Show all notes (overrides --top)")
    args = parser.parse_args()

    if args.vault_path:
        vault_root = Path(args.vault_path)
    else:
        # Infer from script location: scripts/ → vault-audit/ → skills/ → .claude/ → project root
        script_dir = Path(__file__).parent
        project_root = script_dir.parent.parent.parent.parent
        vault_root = project_root / VAULT_RELATIVE

    if not vault_root.exists():
        print(f"ERROR: vault not found at {vault_root}", file=sys.stderr)
        sys.exit(1)

    report = run_audit(vault_root, top_n=args.top, full=args.full)

    if args.output == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(format_table(report))


if __name__ == "__main__":
    main()
