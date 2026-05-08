#!/usr/bin/env python3
"""
vault-audit/scripts/fix.py
Applies DETERMINISTIC fixes to forge-brain vault notes.

IMPORTANT: Only deterministic corrections are applied automatically:
  - Add missing frontmatter fields (empty/default values)
  - Normalize tag format (#type/X, #domaine/Y from existing type/domaine fields)
  - Add missing ## Liens section
  - Add MOC wikilink if folder has a known MOC and ## Liens exists

LLM-judgment tasks (alias enrichment, resume rewriting) are NEVER auto-applied.
They appear as "Suggestions" in the audit report only.

Usage:
  python scripts/fix.py [--vault-path PATH] [--dry-run] [--note "Name"]
"""

import re
import sys
import argparse
from pathlib import Path
from datetime import date

# Windows CP1252 fix
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

VAULT_RELATIVE = "vault/claude-forge"
SKIP_DIRS = {".obsidian", "Templates", ".git", ".claude", "agent-memory"}
SKIP_FILES = {"Bienvenue.md"}

REQUIRED_FIELDS = ["titre", "resume", "aliases", "type", "derniere-maj", "auteur", "tags"]

FOLDER_TO_MOC = {
    "01-Claude-Code": "MOC-Claude-Code",
    "02-Concurrents": "MOC-Concurrents",
    "03-Modeles": "MOC-Modeles",
    "04-Techniques": "MOC-Techniques",
    "05-Leaders": "MOC-Leaders",
    "06-Industrie": "MOC-Industrie",
    "07-Prompts": "MOC-Prompts",
}

DEFAULT_VALUES = {
    "titre": "",
    "resume": "",
    "aliases": [],
    "type": "",
    "derniere-maj": "",
    "auteur": "claude",
    "tags": [],
}


def parse_frontmatter_raw(content: str) -> tuple[str, str, str]:
    """Returns (before_fm, fm_text, after_fm). before_fm is '---\n'."""
    if not content.startswith("---"):
        return "", "", content
    end = content.find("\n---", 3)
    if end == -1:
        return "", "", content
    fm_text = content[3:end + 1]  # includes leading \n
    after = content[end + 4:]
    return "---", fm_text, after


def fm_has_field(fm_text: str, field: str) -> bool:
    """Check if frontmatter text contains a given field key."""
    return bool(re.search(rf'^{re.escape(field)}\s*:', fm_text, re.MULTILINE))


def add_missing_fm_fields(fm_text: str, existing_type: str = "") -> tuple[str, list[str]]:
    """Add missing required fields with empty/default values. Returns (new_fm, added_fields)."""
    added = []
    lines = fm_text.rstrip("\n").split("\n")

    for field in REQUIRED_FIELDS:
        if fm_has_field(fm_text, field):
            continue
        # Build YAML line(s) for default value
        default = DEFAULT_VALUES.get(field)
        if isinstance(default, list):
            new_line = f"{field}: []"
        elif field == "auteur":
            new_line = f'{field}: claude'
        elif field == "tags" and existing_type:
            new_line = f"tags:\n  - \"#type/{existing_type}\""
        else:
            new_line = f'{field}: ""'
        lines.append(new_line)
        added.append(field)
        fm_text = "\n".join(lines)

    return "\n".join(lines), added


def ensure_liens_section(body: str) -> tuple[str, bool]:
    """Add ## Liens section if missing. Returns (new_body, was_added)."""
    if "## Liens" in body:
        return body, False
    body = body.rstrip("\n") + "\n\n## Liens\n\n"
    return body, True


def add_moc_link(body: str, moc_name: str) -> tuple[str, bool]:
    """Add [[MOC-*]] link in ## Liens section if not present. Returns (new_body, was_added)."""
    if f"[[{moc_name}" in body:
        return body, False

    liens_match = re.search(r'(## Liens\s*\n)', body)
    if not liens_match:
        return body, False

    insert_pos = liens_match.end()
    body = body[:insert_pos] + f"- [[{moc_name}]]\n" + body[insert_pos:]
    return body, True


def fix_note(path: Path, vault_root: Path, dry_run: bool = False) -> dict:
    """Apply deterministic fixes to a single note. Returns fix report."""
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        return {"path": str(path.relative_to(vault_root)), "error": str(e), "fixes": []}

    rel = path.relative_to(vault_root)
    top_folder = rel.parts[0] if len(rel.parts) > 0 else ""
    expected_moc = FOLDER_TO_MOC.get(top_folder)

    # Parse raw frontmatter
    before, fm_text, after_fm = parse_frontmatter_raw(content)
    if not before:
        return {
            "path": str(rel).replace("\\", "/"),
            "fixes": [],
            "skipped": "No frontmatter found — manual fix required",
        }

    fixes = []
    new_fm = fm_text
    new_body = after_fm

    # Extract existing type for tag normalization
    type_match = re.search(r'^type\s*:\s*(.+)$', fm_text, re.MULTILINE)
    existing_type = type_match.group(1).strip().strip('"') if type_match else ""

    # 1. Add missing frontmatter fields
    new_fm, added_fields = add_missing_fm_fields(new_fm, existing_type)
    if added_fields:
        fixes.append(f"Champs ajoutés : {', '.join(added_fields)}")

    # 2. Ensure ## Liens section in body
    new_body, liens_added = ensure_liens_section(new_body)
    if liens_added:
        fixes.append("Section ## Liens ajoutée")

    # 3. Add MOC link
    if expected_moc:
        new_body, moc_added = add_moc_link(new_body, expected_moc)
        if moc_added:
            fixes.append(f"Lien [[{expected_moc}]] ajouté")

    # 4. Update derniere-maj if it was empty (we just set it)
    if "derniere-maj" in added_fields:
        today_str = date.today().isoformat()
        new_fm = re.sub(
            r'^(derniere-maj\s*:\s*).*$',
            rf'\g<1>{today_str}',
            new_fm,
            flags=re.MULTILINE
        )
        fixes.append(f"derniere-maj initialisé à {today_str}")

    if not fixes:
        return {
            "path": str(rel).replace("\\", "/"),
            "fixes": [],
        }

    # Reconstruct full content
    new_content = before + new_fm + "\n---" + new_body

    if not dry_run:
        path.write_text(new_content, encoding="utf-8")

    return {
        "path": str(rel).replace("\\", "/"),
        "fixes": fixes,
        "dry_run": dry_run,
    }


def main():
    parser = argparse.ArgumentParser(description="Fix forge-brain vault notes (deterministic only)")
    parser.add_argument("--vault-path", default=None)
    parser.add_argument("--dry-run", action="store_true", help="Show what would be fixed without writing")
    parser.add_argument("--note", default=None, help="Fix a single note by name (stem)")
    args = parser.parse_args()

    if args.vault_path:
        vault_root = Path(args.vault_path)
    else:
        script_dir = Path(__file__).parent
        project_root = script_dir.parent.parent.parent.parent
        vault_root = project_root / VAULT_RELATIVE

    if not vault_root.exists():
        print(f"ERROR: vault not found at {vault_root}", file=sys.stderr)
        sys.exit(1)

    if args.note:
        # Fix a single note
        matches = list(vault_root.rglob(f"{args.note}.md"))
        if not matches:
            print(f"ERROR: note '{args.note}' not found", file=sys.stderr)
            sys.exit(1)
        targets = matches[:1]
    else:
        targets = [
            p for p in sorted(vault_root.rglob("*.md"))
            if not any(part in SKIP_DIRS for part in p.parts)
            and p.name not in SKIP_FILES
        ]

    fixed_count = 0
    skipped_count = 0

    for p in targets:
        result = fix_note(p, vault_root, dry_run=args.dry_run)
        if result.get("error"):
            print(f"[ERROR] {result['path']} : {result['error']}")
        elif result.get("skipped"):
            print(f"[SKIP]  {result['path']} : {result['skipped']}")
            skipped_count += 1
        elif result["fixes"]:
            marker = "[DRY]" if args.dry_run else "[FIX]"
            print(f"{marker}  {result['path']}")
            for fix in result["fixes"]:
                print(f"         - {fix}")
            fixed_count += 1

    mode = "(dry run)" if args.dry_run else ""
    print(f"\n{fixed_count} notes modifiées {mode}, {skipped_count} ignorées sur {len(targets)} total")


if __name__ == "__main__":
    main()
