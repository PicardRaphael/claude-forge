#!/usr/bin/env python3
"""Tests de check-orphan-tests.py — le garde qui detecte les suites inertes.

Un garde-fou sans test peut se desarmer en silence, ce qui est exactement le
defaut qu'il traque. Les cas pinnes ici sont ceux qui ont reellement piege
l'ecriture du script le 5 sept. 2026 :
  - tests/integration/ compte comme une arborescence de tests (pas « hors
    tests/ ») ;
  - un sous-projet portant son propre pyproject.toml sort du perimetre ;
  - une PROSE citant `pytest <chemin>` ne declare aucune suite ;
  - un chemin inexistant dans AGENTS.md n'en declare pas davantage.

Les deux derniers sont les plus importants : un faux chemin declare une suite
vivante a tort, donc produit un faux negatif — le garde se tait alors qu'il
devrait crier.
"""
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parent.parent / "check-orphan-tests.py"

BLOC_STANDARD = """# Repo de test

## Verification locale

```powershell
py -m pytest .claude/hooks/tests -q
```
"""


def ecrire(repo: Path, chemin: str, contenu: str = "def test_x():\n    pass\n") -> None:
    cible = repo / chemin
    cible.parent.mkdir(parents=True, exist_ok=True)
    cible.write_text(contenu, encoding="utf-8")


def lancer(repo: Path) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), str(repo)],
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout


def test_test_hors_dossier_tests_est_signale(tmp_path):
    ecrire(tmp_path, "AGENTS.md", BLOC_STANDARD)
    ecrire(tmp_path, ".claude/hooks/tests/test_ok.py")
    ecrire(tmp_path, ".claude/hooks/test_orphelin.py")
    code, out = lancer(tmp_path)
    assert code == 1
    assert "test_orphelin.py" in out
    assert "test_ok.py" not in out


def test_test_dans_suite_declaree_passe(tmp_path):
    ecrire(tmp_path, "AGENTS.md", BLOC_STANDARD)
    ecrire(tmp_path, ".claude/hooks/tests/test_ok.py")
    code, out = lancer(tmp_path)
    assert code == 0, out


def test_suite_non_declaree_est_signalee(tmp_path):
    """Un dossier tests/ peuple mais absent d'AGENTS.md ne tourne jamais."""
    ecrire(tmp_path, "AGENTS.md", BLOC_STANDARD)
    ecrire(tmp_path, ".codex/hooks/tests/test_jamais_lance.py")
    code, out = lancer(tmp_path)
    assert code == 1
    assert "test_jamais_lance.py" in out


def test_sous_dossier_de_tests_reste_dans_la_suite(tmp_path):
    """tests/integration/ appartient a l'arborescence tests/, pas « hors tests/ »."""
    ecrire(tmp_path, "AGENTS.md", BLOC_STANDARD)
    ecrire(tmp_path, ".claude/hooks/tests/integration/test_bout_en_bout.py")
    code, out = lancer(tmp_path)
    assert code == 0, out


def test_sous_projet_autonome_est_hors_perimetre(tmp_path):
    """Un pyproject.toml declare sa propre collecte : ses tests ne sont pas juges ici."""
    ecrire(tmp_path, "AGENTS.md", BLOC_STANDARD)
    ecrire(tmp_path, ".claude/hooks/tests/test_ok.py")
    ecrire(tmp_path, "mcp-truc/pyproject.toml", "[tool.pytest.ini_options]\n")
    ecrire(tmp_path, "mcp-truc/tests/test_interne.py")
    ecrire(tmp_path, "mcp-truc/test_a_la_racine.py")
    code, out = lancer(tmp_path)
    assert code == 0, out
    assert "mcp-truc" not in out


def test_prose_citant_pytest_ne_declare_aucune_suite(tmp_path):
    """Hors bloc de code, `pytest <chemin>` est un exemple, pas une invocation."""
    agents = BLOC_STANDARD + "\nLe script lit les lignes `pytest .` de ce fichier.\n"
    ecrire(tmp_path, "AGENTS.md", agents)
    ecrire(tmp_path, ".codex/hooks/tests/test_jamais_lance.py")
    code, out = lancer(tmp_path)
    assert code == 1, "la prose a declare tout le repo comme collecte"
    assert "test_jamais_lance.py" in out


def test_chemin_inexistant_ne_declare_aucune_suite(tmp_path):
    """Une commande pointant vers un dossier absent ne rend rien vivant."""
    agents = "```powershell\npy -m pytest .claude/hooks/tests -q\npy -m pytest .disparu/tests -q\n```\n"
    ecrire(tmp_path, "AGENTS.md", agents)
    ecrire(tmp_path, ".claude/hooks/tests/test_ok.py")
    code, out = lancer(tmp_path)
    assert code == 0, out
    assert "1 suite(s) declaree(s)" in out


def test_agents_md_absent_verifie_quand_meme_la_famille_1(tmp_path):
    ecrire(tmp_path, ".claude/hooks/test_orphelin.py")
    code, out = lancer(tmp_path)
    assert code == 1
    assert "test_orphelin.py" in out


def test_repo_sans_aucun_test_ne_hurle_pas(tmp_path):
    """Fail-open : mauvais repo ou repo neuf ne doit pas produire un echec."""
    ecrire(tmp_path, "AGENTS.md", BLOC_STANDARD)
    code, out = lancer(tmp_path)
    assert code == 0
    assert "SKIP" in out


@pytest.mark.parametrize("ignore", ["node_modules", "worktrees", "__pycache__"])
def test_arborescences_ignorees(tmp_path, ignore):
    ecrire(tmp_path, "AGENTS.md", BLOC_STANDARD)
    ecrire(tmp_path, ".claude/hooks/tests/test_ok.py")
    ecrire(tmp_path, f"{ignore}/test_pas_a_nous.py")
    code, out = lancer(tmp_path)
    assert code == 0, out
