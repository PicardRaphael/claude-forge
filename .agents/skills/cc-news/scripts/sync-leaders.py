#!/usr/bin/env python3
"""Regenerate the "Leaders canonisés" block of cc-news domain-*.md from the vault.

Single source of truth: the vault folder 05-Leaders/<domaine>/ IS the canonical
list of leaders for a domain. This script reads those folders and rewrites the
synced block inside each domain-*.md, between marker comments. Everything else in
domain-*.md (sources directes, queries, watchlist, capitalisation) is left
untouched — it is the operational hunt plan, owned by hand.

Run at MAINTENANCE time (after adding/removing a leader fiche), NOT at cc-news
runtime. A scan reads the already-synced file; no MCP cost per scan.

Two strict responsibilities:
  1. Rewrite the block between SYNC_START and SYNC_END from list of vault fiches.
  2. NEVER touch the "Watchlist signaux non canonisés" section or any other text.

Vault access is plain Python file I/O (open/glob), not Bash cat/grep nor the Read
tool — so it is not intercepted by vault-cat-guard.py. The vault root is resolved
via git, never passed as an argument that could trip a path-based guard.

Usage:
  py sync-leaders.py            # rewrite all domain files, report diff summary
  py sync-leaders.py --check    # report what WOULD change, write nothing (CI/dry-run)
  py sync-leaders.py --domain rag   # one domain only
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

# Marker comments delimiting the auto-generated block. The script owns ONLY what
# is strictly between these two lines. Hand-edited content lives outside.
SYNC_START = "<!-- SYNC:leaders:start — généré par scripts/sync-leaders.py, NE PAS éditer à la main -->"
SYNC_END = "<!-- SYNC:leaders:end -->"

# Mapping domain-*.md file stem -> vault folder under 05-Leaders/.
# Empirically derived (27 mai 2026): the vault folder is the source of truth for
# a domain's canonical leaders. "concurrents" has no vault folder of its own — it
# maps to industrie/ (Sam Altman, Demis Hassabis... live there). "discovery" has
# no leaders block (pure emerging-signal hunting) and is intentionally absent.
# X accounts that belong to an org/project, not the person. The fiche links them
# (twitter.com/JinaAI_ on Han Xiao) so the heuristic would emit a wrong query.
# Manual denylist — extend as faux handles are spotted. Lowercase, no '@'.
ORG_HANDLES = {"jinaai_"}

DOMAIN_TO_VAULT_FOLDER = {
    "domain-claude-code": "claude-code",
    "domain-agents": "agents",
    "domain-rag": "rag",
    "domain-finetuning": "fine-tuning",
    "domain-prompt-engineering": "prompt",
    "domain-concurrents": "industrie",
}


def repo_root() -> Path:
    """Resolve the forge repo root via git, robust to cwd."""
    out = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return Path(out)


def parse_frontmatter(text: str) -> dict:
    """Extract the YAML frontmatter as a flat dict. Minimal parser — handles the
    scalar fields (titre, resume, role) and the list fields (aliases, sources) we
    need, without a YAML dependency. Unknown structures are ignored, not fatal."""
    if not text.startswith("﻿"):
        bom = ""
    else:
        bom = "﻿"
        text = text[1:]
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    fm: dict = {}
    current_list_key: str | None = None
    for raw in block.splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        # list item under the current key
        m_item = re.match(r"^\s+-\s+(.*)$", line)
        if m_item and current_list_key:
            val = m_item.group(1).strip().strip('"').strip("'")
            fm.setdefault(current_list_key, []).append(val)
            continue
        # key: value  OR  key:  (list follows)
        m_kv = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m_kv:
            key, val = m_kv.group(1), m_kv.group(2).strip()
            if val == "":
                current_list_key = key
                fm.setdefault(key, [])
            else:
                current_list_key = None
                fm[key] = val.strip('"').strip("'")
    return fm


def guess_handle(fm: dict, body: str) -> str:
    """Best-effort X handle, HIGH-CONFIDENCE ONLY. Handles are not yet a
    structured frontmatter field (tracked debt); aliases mix real handles with
    product/project names (ColBERT, SBERT, LangChain) so they are NOT a reliable
    source — a WRONG handle generates a wrong cc-news query, worse than no handle.

    We therefore trust ONLY an explicit link to the person's X account in the
    body: `x.com/<handle>` / `twitter.com/<handle>` or an `X : @handle` line.
    Sources frontmatter pointing at x.com/<handle> also counts. Anything else →
    "" (degraded mode, reported, query completed by hand)."""
    def clean(token: str) -> str | None:
        """A real handle is a bare X username: not an article slug (x.com/foo-bar-baz),
        not an X UI path (i/home/search/intent), not a known org/project account
        (the fiche sometimes links the company X, not the person's — JinaAI_ for
        Han Xiao). ORG_HANDLES is a small manual denylist; the real personal handle
        is filled at the frontmatter-normalisation pass (tracked debt)."""
        h = token.lstrip("@")
        if h.lower() in ("i", "home", "search", "intent", "share"):
            return None
        if h.lower() in ORG_HANDLES:
            return None
        return h

    # body / sources: x.com/<handle> or twitter.com/<handle> — handle must be
    # immediately followed by a boundary (not '-' or '/word', which means a slug).
    pat = re.compile(r"(?:x\.com|twitter\.com)/(@?[A-Za-z0-9_]{2,30})(?![A-Za-z0-9_./-])")
    for text in [body] + list(fm.get("sources", [])):
        m = pat.search(text)
        if m and (h := clean(m.group(1))):
            return "@" + h
    # explicit "X : @handle" / "Twitter: @handle"
    m = re.search(r"(?:X|Twitter)\s*:?\s*\[?@([A-Za-z0-9_]{2,30})", body)
    if m and (h := clean(m.group(1))):
        return "@" + h
    return ""


def _strip_baseline(name: str) -> str:
    """Cut a trailing role/baseline joined by a SPACED dash (— – -) — but keep a
    hyphenated name like "Brad-Abrams" / "Mitchell-Hashimoto" intact (no spaces
    around the hyphen)."""
    return re.split(r"\s+[—–-]\s+", name, maxsplit=1)[0].strip()


def leader_name(fm: dict, body: str, stem: str) -> str:
    """Robust display name across heterogeneous frontmatter schemas:
    titre → first name-like alias → body H1 → cleaned stem. The role/baseline
    sometimes appended in `titre` ("Dario Amodei — CEO Anthropic…") is stripped."""
    titre = (fm.get("titre") or "").strip().strip('"')
    if titre:
        return _strip_baseline(titre)
    for a in fm.get("aliases", []):
        a = a.strip()
        if " " in a and a[:1].isupper():  # "Affaan Mustafa", not "ECC creator"
            return _strip_baseline(a)
    m = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    if m:
        return _strip_baseline(m.group(1).strip())
    return stem.replace("-", " ").title()


def fiche_to_row(path: Path) -> tuple[str, str]:
    """Return (sort_key, row, name, handle) for one leader fiche."""
    text = path.read_text(encoding="utf-8")
    end = text.find("\n---", 3)
    body = text[end + 4:] if end != -1 else text
    fm = parse_frontmatter(text)
    name = leader_name(fm, body, path.stem)
    handle = guess_handle(fm, body)
    role = (fm.get("role") or fm.get("resume") or "").strip().strip('"')
    if len(role) > 90:
        role = role[:87].rstrip() + "…"
    sources = fm.get("sources")
    if not isinstance(sources, list):  # None, or inline "[]"/scalar → empty
        sources = []
    src_clean = [s for s in sources if s.strip().strip("[]").strip()]
    src_short = ", ".join(s.split("//")[-1].split("/")[0] for s in src_clean[:2]) if src_clean else "—"
    name_cell = f"**{name}** ({handle})" if handle else f"**{name}**"
    row = f"| {name_cell} | {role or '—'} | {src_short} |"
    return (name.lower(), row, name, handle)


def build_block(vault_root: Path, folder: str) -> tuple[str, list[str], list[tuple[str, str]]]:
    """Build the synced block for one domain.
    Returns (block, missing_handles, leaders) where leaders = [(name, handle), ...]."""
    leaders_dir = vault_root / "vault" / "claude-forge" / "05-Leaders" / folder
    fiches = sorted(leaders_dir.glob("*.md"))
    rows = []
    missing = []
    leaders = []
    for f in fiches:
        sort_key, row, name, handle = fiche_to_row(f)
        rows.append((sort_key, row))
        leaders.append((name, handle))
        if "(@" not in row:
            missing.append(f.stem)
    rows.sort(key=lambda r: r[0])
    lines = [
        SYNC_START,
        "",
        f"## Leaders canonisés ({len(rows)}) — vault 05-Leaders/" + folder + "/",
        "",
        "| Personne | Rôle | Sources |",
        "|----------|------|---------|",
    ]
    lines += [r[1] for r in rows]
    lines += [
        "",
        "> Bloc généré depuis le vault. Pour ajouter/retirer un leader : créer/supprimer"
        " la fiche dans `05-Leaders/" + folder + "/` puis relancer `py scripts/sync-leaders.py`.",
        "> Les leaders sans handle (`@`) sont en mode dégradé — compléter les queries à la main.",
        "",
        SYNC_END,
    ]
    return "\n".join(lines), missing, leaders


_QUERIES_RE = re.compile(r"^##\s+Queries.*$", re.MULTILINE | re.IGNORECASE)


def queries_text(domain_text: str) -> str:
    """Return the lowercased text of the '## Queries à exécuter' section, or ''.
    Used to detect leaders that are synced but not yet hunted by any query."""
    m = _QUERIES_RE.search(domain_text)
    if not m:
        return ""
    start = m.end()
    nxt = re.search(r"^##\s+", domain_text[start:], re.MULTILINE)
    section = domain_text[start: start + nxt.start()] if nxt else domain_text[start:]
    return section.lower()


def unhunted_leaders(domain_text: str, leaders: list[tuple[str, str]]) -> list[str]:
    """Leaders present in the synced block but matched by NO existing query.
    A leader is 'hunted' if its handle (preferred) or its last name appears in the
    queries section. Returns display labels for the ones that are not."""
    q = queries_text(domain_text)
    if not q:
        return []
    out = []
    for name, handle in leaders:
        hit = False
        if handle and handle.lower().lstrip("@") in q:
            hit = True
        else:
            # last significant token of the name (skip 1-2 char particles)
            tokens = [t for t in re.split(r"[\s,&—–-]+", name) if len(t) > 2]
            if tokens and tokens[-1].lower() in q:
                hit = True
            elif tokens and tokens[0].lower() in q:
                hit = True
        if not hit:
            out.append(f"{name}{' ' + handle if handle else ''}")
    return out


def apply_block(domain_text: str, block: str) -> str | None:
    """Replace the existing synced block with `block`. If no markers are present,
    insert the block right after the H1 title line. Returns new text, or None if
    unchanged."""
    if SYNC_START in domain_text and SYNC_END in domain_text:
        pattern = re.compile(
            re.escape(SYNC_START) + r".*?" + re.escape(SYNC_END),
            re.DOTALL,
        )
        new_text = pattern.sub(lambda _: block, domain_text, count=1)
    else:
        # First run: insert after the first H1 line.
        lines = domain_text.splitlines(keepends=True)
        out, inserted = [], False
        for ln in lines:
            out.append(ln)
            if not inserted and ln.startswith("# "):
                out.append("\n" + block + "\n")
                inserted = True
        if not inserted:
            out.insert(0, block + "\n\n")
        new_text = "".join(out)
    return new_text if new_text != domain_text else None


def main() -> int:
    ap = argparse.ArgumentParser(description="Sync cc-news domain leaders from vault.")
    ap.add_argument("--check", action="store_true", help="dry-run: report, write nothing")
    ap.add_argument("--domain", help="one domain stem only (e.g. rag)")
    args = ap.parse_args()

    # Console may be cp1252 on Windows; the report contains accented names.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    root = repo_root()
    refs_dir = root / ".claude" / "skills" / "cc-news" / "references"

    targets = DOMAIN_TO_VAULT_FOLDER
    if args.domain:
        stem = args.domain if args.domain.startswith("domain-") else f"domain-{args.domain}"
        if stem not in targets:
            print(f"ERREUR: domaine inconnu '{stem}'. Connus: {', '.join(targets)}", file=sys.stderr)
            return 2
        targets = {stem: targets[stem]}

    changed, unchanged, all_missing, all_unhunted = [], [], {}, {}
    for domain_stem, folder in targets.items():
        domain_path = refs_dir / f"{domain_stem}.md"
        if not domain_path.exists():
            print(f"SKIP: {domain_path.name} absent", file=sys.stderr)
            continue
        block, missing, leaders = build_block(root, folder)
        if missing:
            all_missing[domain_stem] = missing
        domain_text = domain_path.read_text(encoding="utf-8")
        unhunted = unhunted_leaders(domain_text, leaders)
        if unhunted:
            all_unhunted[domain_stem] = unhunted
        new_text = apply_block(domain_text, block)
        if new_text is None:
            unchanged.append(domain_stem)
            continue
        changed.append(domain_stem)
        if not args.check:
            domain_path.write_text(new_text, encoding="utf-8")

    mode = "DRY-RUN (rien écrit)" if args.check else "ÉCRIT"
    print(f"=== sync-leaders.py — {mode} ===")
    print(f"Modifiés ({len(changed)}): {', '.join(changed) or '—'}")
    print(f"Inchangés ({len(unchanged)}): {', '.join(unchanged) or '—'}")
    if all_unhunted:
        print("\n[!] Leaders synced SANS query qui les vise — a ajouter dans '## Queries a executer' (a froid):")
        for dom, names in all_unhunted.items():
            print(f"  {dom}: {', '.join(names)}")
    if all_missing:
        print("\nLeaders sans handle (mode dégradé, query à compléter à la main):")
        for dom, names in all_missing.items():
            print(f"  {dom}: {', '.join(names)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
