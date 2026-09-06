#!/usr/bin/env python3
"""Tests de check-twin-drift.py — le garde des propagations oubliees.

Les deux scenarios qui comptent sont tires du reel :
  - le libelle du security-guard corrige cote Claude et pas cote Codex
    (5 sept. 2026) doit etre signale ;
  - le meme fichier ecrit avec des regex sur une ligne d'un cote et sur
    plusieurs de l'autre ne doit RIEN signaler — c'est du formatage, et le
    signaler ferait 24 lignes de bruit sur une paire pourtant alignee.

Un garde qui crie sur du formatage se fait ignorer ; c'est le mode de
defaillance qu'on evite ici, pas seulement le faux negatif.
"""
import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "check-twin-drift.py"


def ecrire(repo: Path, chemin: str, contenu: str) -> None:
    cible = repo / chemin
    cible.parent.mkdir(parents=True, exist_ok=True)
    cible.write_text(contenu, encoding="utf-8")


def lancer(repo: Path, *extra: str) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), *extra, str(repo)],
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout


def repo_minimal(repo: Path) -> None:
    """Une paire de hooks identiques : socle sain sur lequel greffer un ecart."""
    corps = 'MSG = "suppression de branche -d/-D (demande explicite requise)"\n'
    ecrire(repo, ".claude/hooks/security-guard.py", corps)
    ecrire(repo, ".codex/hooks/security-guard.py", corps)


def test_paire_alignee_ne_signale_rien(tmp_path):
    repo_minimal(tmp_path)
    code, out = lancer(tmp_path)
    assert code == 0, out


def test_libelle_corrige_d_un_seul_cote_est_signale(tmp_path):
    """Le cas reel : Claude corrige, Codex laisse en arriere."""
    repo_minimal(tmp_path)
    ecrire(tmp_path, ".codex/hooks/security-guard.py", 'MSG = "git branch -D ancien libelle"\n')
    code, out = lancer(tmp_path)
    assert code == 1
    assert "security-guard.py" in out
    assert "suppression de branche" in out


def test_formatage_des_regex_ne_produit_aucun_ecart(tmp_path):
    """Regex sur une ligne vs sur plusieurs : meme sens, aucun signal."""
    ecrire(
        tmp_path,
        ".claude/hooks/g.py",
        'P = (\n    r"\\bgit\\b(?:\\s+-C\\s+\\S+)*"\n    r"\\s+branch\\b[^\\r\\n]*\\s-D\\b",\n'
        '    "suppression de branche (demande explicite requise)",\n)\n',
    )
    ecrire(
        tmp_path,
        ".codex/hooks/g.py",
        'P = (r"\\bgit\\b(?:\\s+-C\\s+\\S+)*\\s+branch\\b[^\\r\\n]*\\s-D\\b", '
        '"suppression de branche (demande explicite requise)")\n',
    )
    code, out = lancer(tmp_path)
    assert code == 0, out


def test_adaptateur_exec_jamais_signale(tmp_path):
    """Un jumeau qui execute la source de l'autre n'a rien a driver."""
    ecrire(tmp_path, ".claude/hooks/memory-recall.py", 'A = "un message tres different"\n')
    ecrire(
        tmp_path,
        ".codex/hooks/memory-recall.py",
        '_S = "peu importe"\nexec(compile(open("x").read(), "x", "exec"), globals())\n',
    )
    code, out = lancer(tmp_path)
    assert code == 0, out


def test_effort_divergent_est_signale(tmp_path):
    """Le cas repo-inspector : effort xhigh d'un cote, high de l'autre."""
    repo_minimal(tmp_path)
    ecrire(tmp_path, ".claude/agents/repo-inspector.md", "---\nname: ri\neffort: high\n---\ncorps\n")
    ecrire(tmp_path, ".codex/agents/repo-inspector.md", "---\nname: ri\neffort: xhigh\n---\ncorps\n")
    code, out = lancer(tmp_path)
    assert code == 1
    assert "effort" in out
    assert "xhigh" in out


def test_champ_absent_d_un_cote_est_une_adaptation(tmp_path):
    """Un champ que seule une surface declare n'est pas une derive."""
    repo_minimal(tmp_path)
    ecrire(tmp_path, ".claude/skills/s/SKILL.md", "---\nname: s\neffort: high\nmodel: opus\n---\nx\n")
    ecrire(tmp_path, ".agents/skills/s/SKILL.md", "---\nname: s\neffort: high\n---\nx\n")
    code, out = lancer(tmp_path)
    assert code == 0, out


def test_composant_sans_jumeau_est_signale(tmp_path):
    repo_minimal(tmp_path)
    ecrire(tmp_path, ".claude/hooks/tout-neuf.py", 'X = "un message assez long ici"\n')
    code, out = lancer(tmp_path)
    assert code == 1
    assert "tout-neuf.py" in out
    assert "sans jumeau" in out


def test_baseline_tait_le_connu_mais_pas_le_neuf(tmp_path):
    repo_minimal(tmp_path)
    ecrire(tmp_path, ".claude/hooks/claude-only.py", 'X = "un message assez long ici"\n')
    code, _ = lancer(tmp_path, "--update-baseline")
    assert code == 0
    assert (tmp_path / ".claude/scripts/twin-drift-baseline.json").exists()

    code, out = lancer(tmp_path)
    assert code == 0, out  # la divergence figee se tait

    ecrire(tmp_path, ".codex/hooks/security-guard.py", 'MSG = "un libelle qui a derive"\n')
    code, out = lancer(tmp_path)
    assert code == 1, "une divergence NOUVELLE doit passer outre la baseline"
    assert "security-guard.py" in out
    assert "claude-only.py" not in out


def test_baseline_illisible_ne_masque_rien(tmp_path):
    """Fail-safe : une baseline corrompue ne doit pas faire taire le garde."""
    repo_minimal(tmp_path)
    ecrire(tmp_path, ".codex/hooks/security-guard.py", 'MSG = "un libelle qui a derive"\n')
    ecrire(tmp_path, ".claude/scripts/twin-drift-baseline.json", "{ pas du json")
    code, out = lancer(tmp_path)
    assert code == 1, out


def test_baseline_porte_son_avertissement(tmp_path):
    repo_minimal(tmp_path)
    ecrire(tmp_path, ".claude/hooks/claude-only.py", 'X = "un message assez long ici"\n')
    lancer(tmp_path, "--update-baseline")
    data = json.loads((tmp_path / ".claude/scripts/twin-drift-baseline.json").read_text(encoding="utf-8"))
    assert "acceptees" in data
    assert "faire taire" in data["_lisez_moi"]


def test_repo_sans_claude_fail_open(tmp_path):
    code, out = lancer(tmp_path)
    assert code == 0
    assert "SKIP" in out


# ===========================================================================
# Menage de la baseline — un ratchet accumule ses entrees mortes
# ===========================================================================

def test_entree_baseline_perimee_est_signalee(tmp_path):
    """Une divergence figee puis corrigee laisse derriere elle une entree que
    plus rien ne distingue d'une divergence active. Le garde doit la nommer."""
    repo_minimal(tmp_path)
    baseline = tmp_path / ".claude" / "scripts" / "twin-drift-baseline.json"
    baseline.parent.mkdir(parents=True, exist_ok=True)
    baseline.write_text(
        json.dumps({
            "acceptees": {
                "hooks:security-guard.py": [
                    "message d'un seul cote : un ecart depuis corrige"
                ]
            }
        }),
        encoding="utf-8",
    )

    code, sortie = lancer(tmp_path)
    assert code == 0
    assert "[MENAGE]" in sortie
    assert "un ecart depuis corrige" in sortie


def test_baseline_a_jour_ne_declenche_pas_le_menage(tmp_path):
    """Aucune entree morte : pas de bruit. Un garde qui crie pour rien s'ignore."""
    repo_minimal(tmp_path)
    baseline = tmp_path / ".claude" / "scripts" / "twin-drift-baseline.json"
    baseline.parent.mkdir(parents=True, exist_ok=True)
    baseline.write_text(json.dumps({"acceptees": {}}), encoding="utf-8")

    code, sortie = lancer(tmp_path)
    assert code == 0
    assert "[MENAGE]" not in sortie
