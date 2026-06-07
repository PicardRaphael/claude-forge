"""Tests validation create_note — partition BLOCABLE-DUR vs WARN-ONLY (Chantier 6-C).

Doctrine : la conformite du CONTENU est validee cote serveur MCP (source unique).
- BLOCABLE-DUR (rejette, rien n'est ecrit) : frontmatter absent · YAML invalide ·
  double cle aliases (que yaml.safe_load ne detecte PAS — PyYAML garde le dernier en silence).
- WARN-ONLY (note creee quand meme) : aliases<4 · aucun tag · wikilink->cible inexistante
  (les forward-refs roadmap G1 sont sains -> jamais un block).
Le helper _creation_blockers est PUR (teste isole) ; le reste passe par la chaine BrainTools.
"""

from src.config import FTSWeights
from src.database import BrainDB
from src.indexer import parse_note
from src.tools.brain import BrainTools, _creation_blockers


# ---------- Helper PUR : _creation_blockers ----------

CONFORME = """---
titre: "Note conforme"
aliases:
  - "a1"
  - "a2"
  - "a3"
  - "a4"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
derniere-maj: 2026-06-08
---

# Body
"""


def test_blockers_conforme_aucun():
    assert _creation_blockers(CONFORME) == []


def test_blockers_frontmatter_absent():
    blockers = _creation_blockers("# Juste un body, pas de frontmatter\n")
    assert len(blockers) == 1
    assert "frontmatter" in blockers[0].lower()


def test_blockers_bom_en_tete_signale_bom():
    """Un BOM en tete fait rater _FRONTMATTER_RE -> block, ET le message doit mentionner BOM."""
    content = "﻿---\ntitre: \"T\"\naliases:\n  - x\n---\n\nBody\n"
    blockers = _creation_blockers(content)
    assert len(blockers) == 1
    assert "BOM" in blockers[0]


def test_blockers_yaml_invalide():
    # Indentation cassee / structure YAML invalide.
    content = "---\ntitre: \"T\"\naliases:\n  - x\n   bad: : :\n---\n\nBody\n"
    blockers = _creation_blockers(content)
    assert any("YAML invalide" in b for b in blockers)


def test_blockers_double_cle_aliases_que_reparse_rate():
    """Deux cles aliases: separees -> PyYAML garde le dernier SANS lever.

    yaml.safe_load ne bronche pas ; seul le check regex dedie l'attrape.
    """
    content = (
        "---\n"
        "titre: \"T\"\n"
        "aliases:\n"
        "  - x\n"
        "aliases:\n"
        "  - y\n"
        "---\n\nBody\n"
    )
    # Preuve que le reparse seul est aveugle :
    import yaml
    assert isinstance(yaml.safe_load(content.split('---')[1]), dict)  # ne leve PAS
    # Mais le blocker l'attrape :
    blockers = _creation_blockers(content)
    assert any("aliases" in b.lower() and "deux fois" in b.lower() for b in blockers)


def test_blockers_aliases_inline_puis_items_orphelins():
    content = (
        "---\n"
        "titre: \"T\"\n"
        "aliases: [a, b]\n"
        "  - orphelin\n"
        "---\n\nBody\n"
    )
    blockers = _creation_blockers(content)
    assert any("aliases" in b.lower() for b in blockers)


def test_blockers_aliases_dans_body_pas_faux_positif():
    """Un `aliases:` cite dans le corps ne doit PAS declencher le block (scope frontmatter)."""
    content = (
        "---\n"
        "titre: \"T\"\n"
        "aliases:\n"
        "  - x\n"
        "---\n\n"
        "Dans le body je parle de aliases: et meme aliases: deux fois aliases:\n"
    )
    assert _creation_blockers(content) == []


# ---------- Chaine LIVE BrainTools ----------

def _live_tools(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    db = BrainDB(tmp_path / "t.db", FTSWeights(file_stem=10.0, content=1.0, aliases=8.0))
    db.create_schema()
    return BrainTools(db, vault, git_sync=None), vault


def test_create_conforme_passe(tmp_path):
    tools, vault = _live_tools(tmp_path)
    res = tools.create_note("ok.md", CONFORME)
    assert res.startswith("Note creee")
    assert "WARN" not in res
    assert (vault / "ok.md").exists()


def test_create_yaml_casse_bloque_et_rien_ecrit(tmp_path):
    tools, vault = _live_tools(tmp_path)
    content = "---\ntitre: \"T\"\naliases:\n  - x\n   bad: : :\n---\n\nBody\n"
    res = tools.create_note("casse.md", content)
    assert res.startswith("REFUS")
    assert "YAML invalide" in res
    # GATE : un block n'ecrit RIEN sur disque (pas de note orpheline).
    assert not (vault / "casse.md").exists()


def test_create_double_aliases_bloque(tmp_path):
    tools, vault = _live_tools(tmp_path)
    content = "---\ntitre: \"T\"\naliases:\n  - x\naliases:\n  - y\n---\n\nBody\n"
    res = tools.create_note("dup.md", content)
    assert res.startswith("REFUS")
    assert "aliases" in res.lower()
    assert not (vault / "dup.md").exists()


def test_create_bom_bloque(tmp_path):
    tools, vault = _live_tools(tmp_path)
    content = "﻿---\ntitre: \"T\"\naliases:\n  - x\n---\n\nBody\n"
    res = tools.create_note("bom.md", content)
    assert res.startswith("REFUS")
    assert "BOM" in res
    assert not (vault / "bom.md").exists()


def test_create_frontmatter_absent_bloque(tmp_path):
    tools, vault = _live_tools(tmp_path)
    res = tools.create_note("nofm.md", "# Pas de frontmatter\n\nBody.\n")
    assert res.startswith("REFUS")
    assert not (vault / "nofm.md").exists()


def test_create_forward_ref_passe_avec_warn(tmp_path):
    """Wikilink vers note inexistante (forward-ref roadmap) -> note CREEE + WARN, pas block."""
    tools, vault = _live_tools(tmp_path)
    content = (
        "---\n"
        "titre: \"Roadmap\"\n"
        "aliases:\n  - a1\n  - a2\n  - a3\n  - a4\n"
        "tags:\n  - \"#type/index\"\n  - \"#domaine/claude-code\"\n"
        "---\n\n"
        "Voir [[note-pas-encore-ecrite]] (roadmap G1).\n"
    )
    res = tools.create_note("roadmap.md", content)
    assert res.startswith("Note creee"), f"forward-ref ne doit PAS bloquer : {res}"
    assert "WARN" in res
    assert "note-pas-encore-ecrite" in res
    assert (vault / "roadmap.md").exists()  # bien creee


def test_create_aliases_insuffisants_passe_avec_warn(tmp_path):
    tools, vault = _live_tools(tmp_path)
    content = (
        "---\n"
        "titre: \"T\"\n"
        "aliases:\n  - seul\n"
        "tags:\n  - \"#type/technique\"\n  - \"#domaine/claude-code\"\n"
        "---\n\nBody\n"
    )
    res = tools.create_note("peu-alias.md", content)
    assert res.startswith("Note creee")
    assert "WARN" in res
    assert "aliases" in res.lower()
    assert (vault / "peu-alias.md").exists()


def test_create_lien_memory_tolere_pas_de_warn(tmp_path):
    """§5 : un wikilink vers feedback_/reference_ (memory hors vault) NE declenche PAS le warn."""
    tools, vault = _live_tools(tmp_path)
    content = (
        "---\n"
        "titre: \"T\"\n"
        "aliases:\n  - a1\n  - a2\n  - a3\n  - a4\n"
        "tags:\n  - \"#type/technique\"\n  - \"#domaine/claude-code\"\n"
        "---\n\n"
        "Cf [[feedback_un_truc]] et [[reference_autre]].\n"
    )
    res = tools.create_note("liens-memory.md", content)
    assert res.startswith("Note creee")
    assert "cible inexistante" not in res  # tolerance §5 : pas flagge
    assert (vault / "liens-memory.md").exists()


def test_create_aucun_tag_passe_avec_warn(tmp_path):
    tools, vault = _live_tools(tmp_path)
    content = (
        "---\n"
        "titre: \"T\"\n"
        "aliases:\n  - a1\n  - a2\n  - a3\n  - a4\n"
        "---\n\nBody sans tag.\n"
    )
    res = tools.create_note("sans-tag.md", content)
    assert res.startswith("Note creee")
    assert "WARN" in res
    assert "tag" in res.lower()
    assert (vault / "sans-tag.md").exists()
