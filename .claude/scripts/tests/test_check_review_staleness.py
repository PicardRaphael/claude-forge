#!/usr/bin/env python3
"""Tests de check-review-staleness.py — le garde des verdicts perimes.

Les scenarios qui comptent :
  - un composant relu puis reecrit doit FAIRE ECHOUER : c'est tout l'objet du
    garde, et c'est le seul cas ou il bloque ;
  - un composant jamais relu ne doit RIEN bloquer — au premier jour, 127
    composants sont dans ce cas, et un garde rouge d'emblee se fait desactiver ;
  - un fichier reecrit en CRLF ou avec des blancs de fin de ligne ne doit RIEN
    signaler : deux postes Windows/LF perimeraient sinon tous les verdicts du
    parc sans qu'une ligne ait change de sens.

Le dernier est le mode de defaillance le plus couteux : il ne se voit qu'apres
avoir estampille tout le parc, quand il est trop tard pour douter du garde.
"""
import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "check-review-staleness.py"
SKILL = ".claude/skills/done/SKILL.md"
CORPS = "---\nname: done\ndescription: cloture de session\n---\n\n# done\n\nEtape 1.\n"


def ecrire(repo: Path, chemin: str, contenu: str) -> None:
    cible = repo / chemin
    cible.parent.mkdir(parents=True, exist_ok=True)
    cible.write_text(contenu, encoding="utf-8", newline="")


def lancer(repo: Path, *extra: str) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), *extra, str(repo)],
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


def repo_minimal(repo: Path) -> None:
    """Une skill, non relue : l'etat de depart de tout le parc."""
    ecrire(repo, SKILL, CORPS)


def test_composant_jamais_relu_ne_bloque_pas(tmp_path):
    repo_minimal(tmp_path)
    code, out = lancer(tmp_path)
    assert code == 0, out
    assert "1 jamais revu" in out, out


def test_composant_relu_et_inchange_ne_signale_rien(tmp_path):
    repo_minimal(tmp_path)
    code, out = lancer(tmp_path, "--stamp", "skills:done", "--verdict", "workflow verifie")
    assert code == 0, out

    code, out = lancer(tmp_path)
    assert code == 0, out
    assert "1 revue(s) a jour" in out, out


def test_composant_relu_puis_modifie_echoue(tmp_path):
    repo_minimal(tmp_path)
    lancer(tmp_path, "--stamp", "skills:done", "--verdict", "workflow verifie")

    ecrire(tmp_path, SKILL, CORPS + "\nEtape 2 ajoutee apres la relecture.\n")
    code, out = lancer(tmp_path)
    assert code == 1, out
    assert "skills:done" in out
    assert "workflow verifie" in out, "le verdict perime doit etre rappele"
    assert "corps seul" in out, out


def test_derive_du_frontmatter_perime_le_verdict_et_se_nomme(tmp_path):
    """`description` decide du routage : sa derive perime la relecture.

    Elle doit se nommer « frontmatter seul » — c'est cette colonne qui permet de
    lire un sweep de parc sans relire 27 skills.
    """
    repo_minimal(tmp_path)
    lancer(tmp_path, "--stamp", "skills:done", "--verdict", "description verifiee")

    ecrire(tmp_path, SKILL, CORPS.replace("cloture de session", "autre chose"))
    code, out = lancer(tmp_path)
    assert code == 1, out
    assert "frontmatter seul" in out, out


def test_sweep_de_parc_est_annonce_comme_tel(tmp_path):
    """Un sweep d'`effort` ne doit pas se lire comme N relectures independantes."""
    def skill(nom: str, effort: str) -> str:
        return f"---\nname: {nom}\neffort: {effort}\n---\n\n# {nom}\n\nEtape 1.\n"

    noms = ("done", "recap", "watch", "evolve")
    for nom in noms:
        ecrire(tmp_path, f".claude/skills/{nom}/SKILL.md", skill(nom, "high"))
    for nom in noms:
        lancer(tmp_path, "--stamp", f"skills:{nom}", "--verdict", "relu")

    for nom in noms:
        ecrire(tmp_path, f".claude/skills/{nom}/SKILL.md", skill(nom, "medium"))
    code, out = lancer(tmp_path)
    assert code == 1, out
    assert "signature d'un sweep de parc" in out, out


def test_crlf_et_blancs_de_fin_ne_periment_rien(tmp_path):
    """Le faux positif qui discrediterait le garde sur tout le parc d'un coup."""
    repo_minimal(tmp_path)
    lancer(tmp_path, "--stamp", "skills:done", "--verdict", "relu")

    bruite = CORPS.replace("\n", "   \r\n")
    ecrire(tmp_path, SKILL, bruite)
    code, out = lancer(tmp_path)
    assert code == 0, out


def test_stamp_sans_verdict_est_refuse(tmp_path):
    repo_minimal(tmp_path)
    code, out = lancer(tmp_path, "--stamp", "skills:done")
    assert code == 1, out
    assert "auto-promotion" in out, out
    assert not (tmp_path / ".claude/scripts/review-baseline.json").exists()


def test_stamp_accepte_un_chemin_autant_qu_une_cle(tmp_path):
    repo_minimal(tmp_path)
    code, out = lancer(tmp_path, "--stamp", SKILL, "--verdict", "relu par chemin")
    assert code == 0, out
    baseline = json.loads((tmp_path / ".claude/scripts/review-baseline.json").read_text(encoding="utf-8"))
    assert "skills:done" in baseline["revues"]


def test_revue_orpheline_est_signalee_sans_bloquer(tmp_path):
    repo_minimal(tmp_path)
    lancer(tmp_path, "--stamp", "skills:done", "--verdict", "relu")
    (tmp_path / SKILL).unlink()

    code, out = lancer(tmp_path)
    assert code == 0, out
    assert "MENAGE" in out, out


def test_contrats_et_rules_sont_dans_le_perimetre(tmp_path):
    repo_minimal(tmp_path)
    ecrire(tmp_path, "AGENTS.md", "# contrat\n")
    ecrire(tmp_path, ".claude/rules/memory-discipline.md", "---\nname: x\n---\n\ncorps\n")
    code, out = lancer(tmp_path, "--list")
    assert code == 0, out
    assert "contrat:AGENTS.md" in out, out
    assert "rules:memory-discipline.md" in out, out
