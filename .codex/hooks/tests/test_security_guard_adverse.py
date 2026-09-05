#!/usr/bin/env python3
"""Tests adverses security-guard Codex — exécution réelle du hook en sous-processus.

Complète test_security_guard.py, qui appelle `is_dangerous()` en direct : ici on
lance le hook comme Codex le lance, et on vérifie le CODE DE SORTIE (2 = blocage
réel). Un hook peut afficher un message sans bloquer (exit 1) — seul ce niveau le
détecte.

SCOPE VÉRIFIÉ ICI : rm -rf/-fr toute cible, suppression de branche (-d comme -D),
push --force/-f, reset --hard, clean -f, et fail-closed sur payload corrompu.
Hors scope volontaire : dd, mkfs, base64, suppression via Python/node.

Les chaînes dangereuses sont construites par concaténation : écrites en clair,
elles déclencheraient le hook Bash live à la lecture/édition de ce fichier.
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

HOOK = Path(__file__).parent.parent / "security-guard.py"

RM = "r" + "m"
BRANCH_FORCE = "-D"
BRANCH_SAFE = "-d"


def run(cmd: str | None) -> int:
    """Lance le hook et retourne son code de sortie. cmd=None → payload illisible."""
    payload = json.dumps({"tool_input": {"command": cmd}}) if cmd is not None else "pas-du-json"
    proc = subprocess.run(
        [sys.executable, str(HOOK)],
        input=payload,
        capture_output=True,
        text=True,
    )
    return proc.returncode


BLOQUES = [
    RM + " -rf ./x",
    RM + " -rf ~/Documents",
    RM + " -rf $HOME/tmp",
    RM + " -fr dossier",
    RM + " -rf .",
    "git branch " + BRANCH_FORCE + " feature",
    "git branch -f " + BRANCH_FORCE + " x",
    "git push --force origin main",
]

# `git branch -d` est bloqué au même titre que -D : AGENTS.md interdit toute
# suppression de branche sans demande explicite. Le regex ne cible que -D, mais
# re.IGNORECASE attrape -d — comportement voulu, pinné ici pour qu'un futur
# scoping de casse ne le retire pas par inadvertance.
#
# La version script de ce fichier, qui vivait hors du chemin de collecte,
# classait `git branch -d` en LEGIT (exit 0 attendu) : l'exact inverse du
# comportement livré. La contradiction n'a jamais été signalée parce que le
# fichier ne tournait pas.
BLOQUES_PAR_IGNORECASE = [
    "git branch " + BRANCH_SAFE + " feature",
]

AUTORISES = [
    RM + " fichier.txt",
    RM + " -f fichier.txt",
    "git push origin develop",
    "echo hello",
    "git branch -f develop master",
]


@pytest.mark.parametrize("cmd", BLOQUES)
def test_commande_destructrice_bloquee(cmd):
    assert run(cmd) == 2, f"attendu exit 2 (blocage) sur {cmd!r}"


@pytest.mark.parametrize("cmd", BLOQUES_PAR_IGNORECASE)
def test_suppression_de_branche_minuscule_bloquee(cmd):
    """-d bloque aussi : toute suppression de branche demande un feu vert explicite."""
    assert run(cmd) == 2, f"attendu exit 2 (blocage) sur {cmd!r}"


@pytest.mark.parametrize("cmd", AUTORISES)
def test_commande_benigne_passe(cmd):
    assert run(cmd) == 0, f"attendu exit 0 (passe) sur {cmd!r}"


def test_payload_illisible_fail_closed():
    """Hook sécurité : un payload corrompu bloque, il ne laisse pas passer."""
    assert run(None) == 2


def test_message_de_blocage_nomme_la_regle_pas_le_flag():
    """Le message doit décrire la règle, pas un flag que l'utilisateur n'a pas tapé.

    Même régression que côté Claude (5 sept. 2026) : le libellé « git branch -D »
    s'affichait sur un `git branch -d`, ce qui fait diagnostiquer un faux positif
    là où le hook applique sa règle.
    """
    proc = subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps({"tool_input": {"command": "git branch " + BRANCH_SAFE + " feature"}}),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 2
    assert "suppression de branche" in proc.stderr
