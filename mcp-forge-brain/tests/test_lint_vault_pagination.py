"""Tests lint_vault : limit=0 (illimité), sélecteur category, défaut inchangé.

Pas de test IO byte-exact : lint_vault N'ÉCRIT RIEN (lit pour re-parser, aucun write_text).
Le gate byte-exact est inapplicable ici (établi au diagnostic #1).
"""

import pytest

from src.config import FTSWeights
from src.database import BrainDB
from src.indexer import parse_note
from src.tools.brain import BrainTools


@pytest.fixture
def vault_many_problems(tmp_path):
    """60 notes minimales : 0 tag, <4 aliases, orphelines (0 lien) -> tombent dans
    low_aliases + no_tags + orphans simultanément. Assez pour dépasser limit=50."""
    vault = tmp_path / "vault"
    vault.mkdir()
    db = BrainDB(tmp_path / "t.db", FTSWeights(file_stem=10.0, content=1.0, aliases=8.0))
    db.create_schema()
    for i in range(60):
        name = f"note{i:02d}.md"
        content = f'---\naliases: ["a{i}"]\n---\nBody sans tag ni wikilink {i}.\n'
        p = vault / name
        p.write_text(content, encoding="utf-8")
        db.index_note(parse_note(p.stem, name, content), p.stat().st_mtime)
    return BrainTools(db, vault, git_sync=None)


def _count_bullets_in_section(output: str, heading_prefix: str) -> int:
    """Compte les puces '- ' sous une section ## donnée, jusqu'au prochain ##."""
    lines = output.split("\n")
    count, in_section = 0, False
    for ln in lines:
        if ln.startswith("## "):
            in_section = ln.startswith(heading_prefix)
            continue
        if in_section and ln.startswith("- "):
            count += 1
    return count


def test_defaut_limit_50_inchange(vault_many_problems):
    """Le défaut reste limit=50 : pas plus de 50 puces par catégorie (60 notes en stock)."""
    out = vault_many_problems.lint_vault()  # défaut
    assert _count_bullets_in_section(out, "## Notes sans tag") == 50
    # Le total réel reste affiché.
    assert "60 total, top 50" in out


def test_limit_0_illimite(vault_many_problems):
    """limit=0 = liste complète : les 60 notes sans tag apparaissent."""
    out = vault_many_problems.lint_vault(limit=0)
    assert _count_bullets_in_section(out, "## Notes sans tag") == 60
    assert "60 total, tous" in out


def test_category_filtre_une_seule(vault_many_problems):
    """category ne retourne QUE la catégorie demandée (les autres absentes)."""
    out = vault_many_problems.lint_vault(category="no_tags")
    assert "## Notes sans tag" in out
    assert "## Notes avec aliases < 4" not in out
    assert "## Notes orphelines" not in out
    assert "## Wikilinks brises" not in out


def test_category_avec_limit_0(vault_many_problems):
    """category + limit=0 : la catégorie ciblée, en entier."""
    out = vault_many_problems.lint_vault(limit=0, category="no_tags")
    assert _count_bullets_in_section(out, "## Notes sans tag") == 60
    assert "## Notes avec aliases < 4" not in out


def test_category_invalide_erreur_propre(vault_many_problems):
    """category invalide -> message clair, pas de crash."""
    out = vault_many_problems.lint_vault(category="inexistante")
    assert out.startswith("REFUS:")
    assert "low_aliases" in out  # liste les valides
    assert "broken_wikilinks" in out


def test_broken_wikilinks_categorie_seule(vault_many_problems):
    """Le cas d'usage Ch.3 : récupérer la catégorie wikilinks brisés isolée."""
    out = vault_many_problems.lint_vault(limit=0, category="broken_wikilinks")
    assert "## Wikilinks brises" in out
    assert "## Notes sans tag" not in out
