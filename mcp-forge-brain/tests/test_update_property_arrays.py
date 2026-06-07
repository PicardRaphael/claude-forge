"""Tests update_property array-safe — splice chirurgical, zero-diff collateral.

Le coeur teste est le helper PUR `_set_property_in_frontmatter` (pas d'IO/DB/git).
Gate explicite (exigence Raphael) : modifier UNE propriete ne doit toucher QUE le span
de cette propriete — tout le reste du fichier reste byte-for-byte.
"""

import difflib

import pytest

from src.config import FTSWeights
from src.database import BrainDB
from src.indexer import parse_note
from src.tools.brain import BrainTools, _set_property_in_frontmatter, _render_yaml_value


# Frontmatter representatif calibre sur le reel du vault forge-brain
# (lu via MCP : aliases/sources bloc 2-espaces quotes doubles, date nue, resume accentue).
WITNESS = """---
titre: "Comment creer une skill"
resume: "Note canonique pour creer une skill — accents preserves : créé, à, déjà."
aliases:
  - "comment creer skill"
  - "creer une skill"
  - "skill best practices"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
derniere-maj: 2026-05-27
auteur: claude
type: technique
sources:
  - "https://www.claude.com/blog/skills-explained"
  - "github.com/anthropics/skills"
---

# Corps de la note

Texte du body avec un [[wikilink]] et du `code inline`.
"""


def _diff_lines(before: str, after: str) -> list[str]:
    return [
        ln for ln in difflib.unified_diff(
            before.splitlines(), after.splitlines(), lineterm="", n=0
        )
        if ln and not ln.startswith(("---", "+++", "@@"))
    ]


# ---------- GATE : diff chirurgical (zero diff collateral) ----------

def test_gate_modif_tags_diff_chirurgical():
    """Modifier tags (liste) -> SEUL le bloc tags change, rien d'autre."""
    after = _set_property_in_frontmatter(
        WITNESS, "tags", ["#type/technique", "#domaine/claude-code", "#statut/canonique"]
    )
    diff = _diff_lines(WITNESS, after)
    # Toutes les lignes du diff doivent concerner tags (ajout/suppression du bloc tags).
    for ln in diff:
        body = ln[1:]
        assert body.strip().startswith(("tags:", "- ", '- "')) or "#" in body, (
            f"Diff collateral detecte (hors tags) : {ln!r}\nDiff complet :\n" + "\n".join(diff)
        )
    # La date, le resume accentue, les aliases, sources NE bougent PAS.
    assert "derniere-maj: 2026-05-27" in after
    assert "créé, à, déjà" in after
    assert '  - "comment creer skill"' in after
    assert '  - "https://www.claude.com/blog/skills-explained"' in after
    # Le nouvel item est present, en style maison.
    assert '  - "#statut/canonique"' in after


def test_gate_modif_date_scalaire_zero_quote():
    """Modifier une date (scalaire) -> reste NON quotee (style vault), zero diff ailleurs."""
    after = _set_property_in_frontmatter(WITNESS, "derniere-maj", "2026-06-08")
    assert "derniere-maj: 2026-06-08" in after
    assert '"2026-06-08"' not in after  # pas de quote parasite
    diff = _diff_lines(WITNESS, after)
    assert len(diff) == 2, f"Attendu 2 lignes (- ancienne / + nouvelle date), eu : {diff}"
    # Le reste intact.
    assert "créé, à, déjà" in after
    assert '  - "#type/technique"' in after


# ---------- Comportements de base ----------

def test_array_bloc_preserve_structure():
    """Une liste produit un array bloc, pas un flow [a, b]."""
    after = _set_property_in_frontmatter(WITNESS, "aliases", ["x", "y"])
    assert "aliases:\n" in after
    assert '  - "x"' in after
    assert '  - "y"' in after
    assert "aliases: [" not in after  # jamais de flow


def test_scalaire_simple_ok():
    after = _set_property_in_frontmatter(WITNESS, "auteur", "raphael")
    assert "auteur: raphael" in after


def test_prop_absente_ajoutee_en_fin_frontmatter():
    after = _set_property_in_frontmatter(WITNESS, "statut", "canonique")
    assert "statut: canonique" in after
    # Ajout dans le frontmatter, pas dans le body.
    fm = after.split("---")[1]
    assert "statut: canonique" in fm


def test_note_sans_frontmatter():
    content = "# Juste un body\n\nSans frontmatter.\n"
    after = _set_property_in_frontmatter(content, "type", "note")
    assert after.startswith("---\ntype: note\n---\n")
    assert "# Juste un body" in after


def test_remplace_array_existant_sans_orphelins():
    """Le bug d'origine : remplacer un array ne doit pas laisser d'items orphelins."""
    after = _set_property_in_frontmatter(WITNESS, "tags", ["#nouveau"])
    # Les anciens items ne doivent plus apparaitre.
    assert "#type/technique" not in after
    assert "#domaine/claude-code" not in after
    assert '  - "#nouveau"' in after
    # Et le YAML reparse proprement (pas d'orphelins).
    import yaml
    fm = after.split("---")[1]
    parsed = yaml.safe_load(fm)
    assert parsed["tags"] == ["#nouveau"]


# ---------- Idempotence ----------

def test_idempotence_liste():
    once = _set_property_in_frontmatter(WITNESS, "tags", ["#a", "#b"])
    twice = _set_property_in_frontmatter(once, "tags", ["#a", "#b"])
    assert once == twice


def test_idempotence_scalaire():
    once = _set_property_in_frontmatter(WITNESS, "derniere-maj", "2026-06-08")
    twice = _set_property_in_frontmatter(once, "derniere-maj", "2026-06-08")
    assert once == twice


# ---------- Rendu valeur (unitaire) ----------

def test_render_liste_vide():
    assert _render_yaml_value("tags", []) == "tags: []"


def test_render_scalaire_avec_deux_points_quote():
    out = _render_yaml_value("titre", "Skill: la suite")
    assert out == 'titre: "Skill: la suite"'


def test_render_liste_echappe_guillemets():
    out = _render_yaml_value("aliases", ['dit "bonjour"'])
    assert '\\"bonjour\\"' in out


# ---------- Helper sur contenu CRLF brut (la branche EOL doit s'activer) ----------

def test_helper_preserve_crlf_contenu():
    """Helper appele sur une string CRLF -> sortie CRLF, pas de \\r\\r\\n ni de LF parasite."""
    content = "---\r\ntags:\r\n  - \"#a\"\r\nauteur: x\r\n---\r\n\r\nBody\r\n"
    after = _set_property_in_frontmatter(content, "tags", ["#a", "#b"])
    assert "\r\r\n" not in after
    assert after.replace("\r\n", "").count("\n") == 0  # zero LF orphelin
    assert '  - "#b"' in after
    assert "auteur: x" in after


def test_helper_preserve_lf_contenu():
    """Helper appele sur une string LF -> reste LF (aucun CRLF introduit)."""
    content = "---\ntags:\n  - \"#a\"\nauteur: x\n---\n\nBody\n"
    after = _set_property_in_frontmatter(content, "tags", ["#a", "#b"])
    assert "\r" not in after
    assert '  - "#b"' in after


# ---------- Tests LIVE byte-exact (chaine reelle BrainTools, IO disque) ----------
# Ces tests passent par read_text/write_text reels : ils attrapent les bugs de
# traduction de fins de ligne (LF->CRLF par write_text Windows) que les tests
# sur string pure ne voient pas.

def _live_tools(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    db = BrainDB(tmp_path / "t.db", FTSWeights(file_stem=10.0, content=1.0, aliases=8.0))
    db.create_schema()
    return BrainTools(db, vault, git_sync=None), vault


def test_live_fichier_lf_reste_lf(tmp_path):
    """GATE byte-exact : un fichier LF ne doit PAS etre converti en CRLF par l'IO."""
    tools, vault = _live_tools(tmp_path)
    note = vault / "note-lf.md"
    raw = b'---\ntags:\n  - "#a"\nauteur: x\n---\n\nBody LF.\n'
    note.write_bytes(raw)
    tools._db.index_note(
        parse_note(note.stem, "note-lf.md", note.read_text(encoding="utf-8")),
        note.stat().st_mtime,
    )
    tools.update_property("note-lf", "tags", ["#a", "#b"])
    after = note.read_bytes()
    assert b"\r\n" not in after, "Fichier LF converti en CRLF (diff full-file)"
    assert b'  - "#b"\n' in after


def test_live_fichier_crlf_reste_crlf(tmp_path):
    """GATE byte-exact : un fichier CRLF reste CRLF, sans \\r\\r\\n parasite."""
    tools, vault = _live_tools(tmp_path)
    note = vault / "note-crlf.md"
    raw = b'---\r\ntags:\r\n  - "#a"\r\nauteur: x\r\n---\r\n\r\nBody.\r\n'
    note.write_bytes(raw)
    tools._db.index_note(
        parse_note(note.stem, "note-crlf.md", note.read_text(encoding="utf-8")),
        note.stat().st_mtime,
    )
    tools.update_property("note-crlf", "tags", ["#a", "#b"])
    after = note.read_bytes()
    assert b"\r\r\n" not in after, "Double conversion CRLF -> \\r\\r\\n"
    assert after.replace(b"\r\n", b"").count(b"\n") == 0, "LF orphelin introduit"
    assert b'  - "#b"\r\n' in after


def test_live_reindex_preserve_autres_champs(tmp_path):
    """Apres update_property, le reparse relit tags ET les champs non touches."""
    tools, vault = _live_tools(tmp_path)
    note = vault / "note-r.md"
    raw = (
        b'---\r\ntitre: "T"\r\naliases:\r\n  - "x"\r\ntags:\r\n  - "#a"\r\n'
        b'derniere-maj: 2026-05-27\r\n---\r\n\r\nBody.\r\n'
    )
    note.write_bytes(raw)
    tools._db.index_note(
        parse_note(note.stem, "note-r.md", note.read_text(encoding="utf-8")),
        note.stat().st_mtime,
    )
    tools.update_property("note-r", "tags", ["#a", "#b", "#c"])
    # Parser les octets SANS traduction (comme la prod reindexe depuis new_content CRLF
    # en memoire) : verifie que parse_note sur CRLF ne pollue pas l'index avec des \r.
    reparsed = parse_note(note.stem, "note-r.md", note.read_bytes().decode("utf-8"))
    assert reparsed.tags == ["#a", "#b", "#c"]
    assert not any("\r" in t for t in reparsed.tags)  # pas de \r dans l'index
    assert reparsed.aliases == ["x"]
    assert reparsed.lint_warnings == []
    after = note.read_bytes()
    assert b'derniere-maj: 2026-05-27' in after  # champ non touche intact
