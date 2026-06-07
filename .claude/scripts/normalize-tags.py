#!/usr/bin/env python3
"""Normalisation des tags du vault forge-brain — chantier 2/5.

Renomme/fusionne des tags dans le bloc `tags:` du frontmatter YAML, en
preservant EXACTEMENT le format liste YAML (indentation, guillemets) et les
fins de ligne d'origine (CRLF sur ce vault Windows).

Touche UNIQUEMENT les lignes `  - "#ancien/tag"` du bloc tags. Aucune autre
ligne du frontmatter ni du body n'est modifiee. Deduplique si une fusion cree
un doublon dans la meme note.

Usage :
    py normalize-tags.py --lot C                 # dry-run (defaut), n'ecrit rien
    py normalize-tags.py --lot C --apply         # ecrit pour de vrai
    py normalize-tags.py --lot all               # dry-run tous lots

MCP doit etre AU REPOS pendant --apply (le script ecrit hors MCP). Relancer
get_tags via MCP apres pour re-indexer.
"""
import argparse
import sys
import tempfile
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2] / "vault" / "claude-forge"

# Mapping ancien_tag -> nouveau_tag, par lot (sans le #, on matche avec).
# Valide avec Raphael (chantier 2/5, 7 juin 2026).
LOTS = {
    "C": {  # Formes projet : nom EXACT du repo (underscore neo_ia/ia_back, tiret claude-forge)
        "#projet/neo-ia": "#projet/neo_ia",
        "#projet/ia-back": "#projet/ia_back",
        "#projet/forge": "#projet/claude-forge",
        "#claude-forge": "#projet/claude-forge",  # tag nu sans prefixe
    },
    "A": {  # sujet/ -> domaine/ (synonymes de prefixe) + cibles tranchees
        "#sujet/mcp": "#domaine/mcp",
        "#sujet/hooks": "#domaine/hooks",
        "#sujet/workflow": "#domaine/workflow",
        "#sujet/agents": "#domaine/agents",
        "#sujet/doctrine": "#domaine/doctrine",
        "#domaine/forge-doctrine": "#domaine/doctrine",
        "#sujet/orchestration": "#domaine/orchestration",
        "#sujet/audit-thematique": "#domaine/audit",
        "#domaine/audit-vault": "#domaine/audit",
        "#sujet/karpathy": "#domaine/karpathy",
    },
    "B": {  # technique/ outil/ -> domaine/ (prouve redondant avec type/+domaine/)
        "#technique/agents": "#domaine/agents",
        "#technique/hooks": "#domaine/hooks",
        "#technique/testing": "#domaine/testing",
        "#outil/claude-code": "#domaine/claude-code",
        "#outil/atlassian": "#domaine/atlassian",
        "#outil/figma": "#domaine/figma",
    },
    "D": {  # projet -> arbitrage semantique
        "#projet/anthropic": "#domaine/anthropic",
        # projet/forge deja traite en C ; neoteem/neoteem-brain/neoteem-po NON fusionnes
    },
    "E1": {  # singletons : renommages / re-prefixages (logique rename eprouvee)
        # --- G4 : traine #sujet/* restante -> #domaine/* (fin du LOT A) ---
        "#sujet/claudemd": "#domaine/claudemd",
        "#sujet/llm-wiki": "#domaine/llm-wiki",
        "#sujet/memoire": "#domaine/memoire",
        "#sujet/methode": "#domaine/methode",
        "#sujet/skills": "#domaine/skills",
        "#sujet/skill": "#domaine/skills",        # unifie singulier/pluriel
        "#sujet/audit": "#domaine/audit",          # cible existante (5) -> dedup possible
        "#sujet/canoniques": "#domaine/canoniques",
        "#sujet/harness-engineering": "#domaine/harness-engineering",  # cible existante (4)
        "#sujet/maintenance": "#domaine/maintenance",
        "#sujet/patterns": "#domaine/patterns",    # cible existante (4)
        "#sujet/plugins": "#domaine/plugin",       # cible existante (1) #domaine/plugin
        "#sujet/portabilite": "#domaine/portabilite",
        "#sujet/prompt-engineering": "#domaine/prompt-engineering",    # cible existante (32) -> dedup possible
        "#sujet/securite": "#domaine/securite",    # cible existante (13) -> dedup possible
        "#sujet/specs": "#domaine/specs",
        "#sujet/tests": "#domaine/testing",        # cible existante (2) -> dedup possible
        "#sujet/tokens": "#domaine/tokens",
        "#sujet/validation-doctrine": "#domaine/validation-doctrine",
        "#sujet/vault": "#domaine/vault",          # cible existante (5) -> dedup possible
        # --- G2 : prefixes hors-convention -> axe canonique ---
        "#audit/doctrine": "#domaine/audit",
        "#audit/vault": "#domaine/audit",
        "#composant/agent": "#domaine/agents",
        "#composant/hook": "#domaine/hooks",
        "#doctrine": "#doctrine/2026",             # tag nu -> axe doctrine date
        "#meta/bilan": "#meta",
        "#meta/externe": "#meta",
        "#meta/lessons-learned": "#meta",
        "#meta/working-memory": "#meta",
        # --- G1 : typos / variantes -> forme dominante ---
        "#domaine/frameworks": "#domaine/framework",   # pluriel -> singulier
        "#type/techniques": "#type/technique",         # pluriel -> singulier
        "#domaine/ai-security": "#domaine/securite",   # EN -> FR
        "#domaine/ai-alignment": "#domaine/alignment", # variante prefixee
        "#pattern/prompting": "#domaine/prompt-engineering",
        "#pattern/prompt-engineering": "#domaine/prompt-engineering",
        "#type/test": "#domaine/testing",              # type mal prefixe -> domaine
        "#domaine/llm": "#domaine/ia",                 # LLM generique -> ia (note Elvis Saravia)
        "#type/industrie": "#type/news",               # trio veille -> type/news (sujet porte par domaine/)
        "#type/veille": "#type/news",
        # type/news garde tel quel (deja la cible)
    },
    "E2": {  # RETRAITS : valeur sentinelle "" = supprimer la ligne du tag (logique drop)
        "#personne/raphael": "",        # redondant #type/casquette sur sa note-racine (1 note)
        "#chantier/22mai2026": "",      # repere temporel mort, jamais en navigation (1 note)
        "#chantier/23mai2026": "",      # idem (1 note)
        "#position/critique": "",       # posture 1 leader, n'aide aucune nav de groupe (1 note)
    },
}

# Sentinelle de retrait : un mapping vers "" signifie « supprimer cette ligne de tag ».
REMOVE = ""


def load_lot(lot_name):
    if lot_name == "all":
        merged = {}
        for m in LOTS.values():
            merged.update(m)
        return merged
    if lot_name not in LOTS:
        sys.exit(f"Lot inconnu : {lot_name}. Choix : {', '.join(LOTS)} ou all")
    return LOTS[lot_name]


def split_frontmatter(raw_lines):
    """Retourne (start, end) index des lignes du frontmatter (--- ... ---), ou None."""
    if not raw_lines or raw_lines[0].rstrip("\r\n") != "---":
        return None
    for i in range(1, len(raw_lines)):
        if raw_lines[i].rstrip("\r\n") == "---":
            return (0, i)
    return None


def _process_inline(path, raw, tags_line, mapping, apply):
    """Traite une ligne `tags: ["#x", "#y", ...]` (inline array).

    Renomme via le mapping, deduplique en gardant la 1re occurrence et l'ordre,
    preserve l'eol et le style de guillemets observe.
    """
    line = raw[tags_line]
    eol = "\r\n" if line.endswith("\r\n") else ("\n" if line.endswith("\n") else "")
    body = line[: len(line) - len(eol)]
    # body = 'tags: ["#a", "#b"]' -> isoler l'interieur des crochets
    lb, rb = body.find("["), body.rfind("]")
    if lb == -1 or rb == -1 or rb < lb:
        return None
    inner = body[lb + 1 : rb]
    raw_items = [it.strip() for it in inner.split(",") if it.strip()]
    quoted_style = any(it.startswith('"') for it in raw_items)

    changes = []
    emitted = []
    dropped = 0
    removed = 0
    for it in raw_items:
        tag = it.strip().strip('"').strip("'")
        new_tag = mapping.get(tag, tag)
        if new_tag != tag:
            changes.append((tag, new_tag))
        if new_tag == REMOVE:        # sentinelle retrait : ne pas emettre
            removed += 1
            continue
        if new_tag in emitted:
            dropped += 1
            continue
        emitted.append(new_tag)

    if not changes:
        return None

    rendered = ", ".join(f'"{t}"' if quoted_style else t for t in emitted)
    new_body = body[: lb] + "[" + rendered + "]" + body[rb + 1 :]
    if apply:
        out = list(raw)
        out[tags_line] = new_body + eol
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.writelines(out)

    return {"path": path, "changes": changes, "dropped": dropped, "removed": removed}


def process_file(path, mapping, apply):
    # Lecture binaire-safe : preserve les fins de ligne d'origine (CRLF).
    with open(path, "r", encoding="utf-8", newline="") as f:
        raw = f.readlines()  # garde le \r\n de chaque ligne

    fm = split_frontmatter(raw)
    if fm is None:
        return None
    fm_start, fm_end = fm

    # Reperer la ligne tags: dans le frontmatter. Deux formats possibles :
    #   (a) liste YAML multi-lignes :  tags:\n  - "#x"\n  - "#y"
    #   (b) inline array          :  tags: ["#x", "#y"]
    tags_line = None
    inline = False
    for i in range(fm_start + 1, fm_end):
        stripped = raw[i].rstrip("\r\n").rstrip()
        if stripped == "tags:":
            tags_line = i  # format (a)
            break
        if stripped.startswith("tags:") and "[" in stripped:
            tags_line = i  # format (b) inline array
            inline = True
            break
        if stripped.startswith("tags:") and "#" in stripped and "[" not in stripped:
            # format (c) inline CSV : tags: #x, #y  — NON gere.
            # Signaler si la ligne contient un tag a fusionner (trou potentiel).
            for old in mapping:
                if old in stripped:
                    return {"path": path, "changes": [], "dropped": 0,
                            "warn": f"format CSV inline non gere contenant {old}: {stripped[:80]}"}
            return None
    if tags_line is None:
        return None  # aucune ligne tags: dans le frontmatter

    # ----- Format (b) : inline array sur une seule ligne -----
    if inline:
        return _process_inline(path, raw, tags_line, mapping, apply)

    # ----- Format (a) : liste YAML multi-lignes -----
    # Collecter les lignes d'items `  - "#tag"` qui suivent.
    changes = []
    seen_after = set()  # pour dedup : tags presents apres renommage
    item_indices = []
    for i in range(tags_line + 1, fm_end):
        stripped = raw[i].lstrip()
        if not stripped.startswith("- "):
            break  # fin du bloc liste
        item_indices.append(i)

    # Premiere passe : calculer les nouveaux tags + reperer doublons crees.
    new_lines = dict(zip(item_indices, (raw[i] for i in item_indices)))
    final_tags_order = []
    for i in item_indices:
        line = raw[i]
        eol = "\r\n" if line.endswith("\r\n") else ("\n" if line.endswith("\n") else "")
        body = line[: len(line) - len(eol)]
        indent = body[: len(body) - len(body.lstrip())]
        # extraire le tag : `- "#x"` ou `- #x`
        val = body.strip()[2:].strip()  # apres "- "
        quoted = val.startswith('"') and val.endswith('"')
        tag = val.strip('"') if quoted else val
        new_tag = mapping.get(tag, tag)
        if new_tag != tag:
            changes.append((tag, new_tag))
        final_tags_order.append((i, indent, quoted, new_tag, eol))

    if not changes:
        return None  # rien a faire dans cette note

    # Reconstruire les lignes en dedupliquant (garder 1re occurrence).
    emitted = set()
    rebuilt = {}
    drop = set()
    removed = 0
    for (i, indent, quoted, new_tag, eol) in final_tags_order:
        if new_tag == REMOVE:        # sentinelle retrait -> supprimer la ligne
            drop.add(i)
            removed += 1
            continue
        if new_tag in emitted:
            drop.add(i)  # doublon cree par fusion -> supprimer cette ligne
            continue
        emitted.add(new_tag)
        q = f'"{new_tag}"' if quoted else new_tag
        rebuilt[i] = f"{indent}- {q}{eol}"

    if apply:
        out = []
        for idx, line in enumerate(raw):
            if idx in drop:
                continue
            out.append(rebuilt.get(idx, line))
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.writelines(out)

    return {"path": path, "changes": changes, "dropped": len(drop) - removed, "removed": removed}


def _frontmatter_text(raw):
    """Retourne le bloc frontmatter (--- ... ---) comme une seule string."""
    fm = split_frontmatter(raw)
    if fm is None:
        return "(pas de frontmatter)"
    _, fm_end = fm
    return "".join(raw[: fm_end + 1])


def _show_frontmatter(substring, mapping):
    """Imprime le frontmatter AVANT/APRES d'une note, via une copie temporaire.

    N'ecrit JAMAIS dans le vault : copie le contenu dans un fichier temp, applique
    la vraie transformation (apply=True) sur la copie, compare. Garantit que
    l'APRES affiche est EXACTEMENT ce que --apply produirait.
    """
    import shutil
    matches = [p for p in sorted(VAULT.rglob("*.md")) if substring in p.name]
    if not matches:
        print(f"Aucune note ne matche : {substring}")
        return
    for path in matches:
        with open(path, "r", encoding="utf-8", newline="") as f:
            raw_before = f.readlines()
        before = _frontmatter_text(raw_before)
        # Copie temp + apply reel dessus
        tmp = Path(tempfile.gettempdir()) / ("show_" + path.name)
        shutil.copyfile(path, tmp)
        process_file(tmp, mapping, apply=True)
        with open(tmp, "r", encoding="utf-8", newline="") as f:
            after = _frontmatter_text(f.readlines())
        try:
            tmp.unlink()
        except Exception:
            pass
        print(f"\n===== {path.relative_to(VAULT)} =====")
        print("--- AVANT " + "-" * 50)
        print(before, end="")
        print("--- APRES " + "-" * 50)
        print(after, end="")
        print("-" * 60)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lot", required=True, help="C, A, B, D ou all")
    ap.add_argument("--apply", action="store_true", help="ecrit (defaut: dry-run)")
    ap.add_argument("--show", default="", help="substring d'un nom de note : imprime son frontmatter AVANT/APRES en memoire (n'ecrit JAMAIS)")
    args = ap.parse_args()

    mapping = load_lot(args.lot)

    if args.show:
        _show_frontmatter(args.show, mapping)
        return
    mode = "APPLY (ecriture)" if args.apply else "DRY-RUN (aucune ecriture)"
    print(f"=== Normalisation tags — LOT {args.lot} — {mode} ===")
    print(f"Vault : {VAULT}")
    print(f"Mapping ({len(mapping)} regles) :")
    for old, new in mapping.items():
        print(f"  {old:32s} -> {new if new != REMOVE else '(RETRAIT)'}")
    print("-" * 70)

    md_files = sorted(VAULT.rglob("*.md"))
    touched = 0
    total_changes = 0
    total_dropped = 0
    total_removed = 0
    warnings = []
    for path in md_files:
        res = process_file(path, mapping, args.apply)
        if res:
            if res.get("warn"):
                warnings.append((path.relative_to(VAULT), res["warn"]))
                continue
            touched += 1
            rel = path.relative_to(VAULT)
            diffs = ", ".join(f"{o}->{n if n != REMOVE else '(RETRAIT)'}" for o, n in res["changes"])
            dropnote = f"  [dedup: -{res['dropped']} doublon(s)]" if res["dropped"] else ""
            remnote = f"  [retrait: -{res.get('removed', 0)} ligne(s)]" if res.get("removed") else ""
            print(f"[{touched:3d}] {rel}")
            print(f"      {diffs}{dropnote}{remnote}")
            total_changes += len(res["changes"])
            total_dropped += res["dropped"]
            total_removed += res.get("removed", 0)
    print("-" * 70)
    print(f"Notes touchees : {touched} | renommages : {total_changes} | lignes dedupliquees : {total_dropped} | lignes retirees : {total_removed}")
    if warnings:
        print(f"\n⚠️  {len(warnings)} note(s) au format CSV inline NON gere (trou potentiel — traiter via MCP) :")
        for rel, w in warnings:
            print(f"  - {rel} : {w}")
    if not args.apply:
        print("DRY-RUN — aucune ecriture. Relancer avec --apply pour executer.")


if __name__ == "__main__":
    main()
