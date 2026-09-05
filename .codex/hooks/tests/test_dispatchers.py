#!/usr/bin/env python3
"""Tests des dispatchers pre-bash-guards / pre-write-guards (Codex).

Les dispatchers agrègent plusieurs gardes derrière un seul spawn Python. Ces
tests vérifient qu'un dispatcher relaie bien le blocage de la garde sous-jacente
(exit 2) et laisse passer le reste (exit 0) — sans quoi l'agrégation aurait
silencieusement désarmé les gardes.

La version script de ce fichier mesurait aussi le gain de temps du dispatcher
face à trois spawns séparés. Ce chrono ne vérifie rien : il ne peut pas échouer,
et sa valeur varie d'une machine à l'autre. Il n'est pas porté ici — une suite
de tests répond par vert ou rouge, pas par une durée.

Les chaînes dangereuses sont construites par concaténation : écrites en clair,
elles déclencheraient le hook Bash live à la lecture/édition de ce fichier.
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

HOOKS = Path(__file__).parent.parent
REPO = HOOKS.parent.parent

RM = "r" + "m"
BRANCH_FORCE = "-D"


def run(script: str, payload: dict) -> int:
    proc = subprocess.run(
        [sys.executable, str(HOOKS / script)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
    )
    return proc.returncode


def bash_payload(cmd: str) -> dict:
    return {"tool_name": "Bash", "tool_input": {"command": cmd}}


def write_payload(path: str) -> dict:
    return {
        "tool_name": "Edit",
        "tool_input": {
            "file_path": path,
            "old_string": "un ancien contenu substantiel de plus de vingt caracteres",
            "new_string": "un nouveau contenu substantiel de plus de vingt caracteres aussi",
        },
    }


@pytest.mark.parametrize(
    "cmd",
    [
        RM + " -rf ./x",
        "git branch " + BRANCH_FORCE + " feat",
    ],
)
def test_bash_dispatcher_relaie_le_blocage(cmd):
    assert run("pre-bash-guards.py", bash_payload(cmd)) == 2


@pytest.mark.parametrize("cmd", ["echo bonjour", "git status"])
def test_bash_dispatcher_laisse_passer_le_benin(cmd):
    assert run("pre-bash-guards.py", bash_payload(cmd)) == 0


def test_write_dispatcher_bloque_edit_direct_de_skill():
    """delegate-guard doit continuer à protéger les SKILL.md à travers le dispatcher.

    La cible est une skill Codex RÉELLE : `.agents/skills/` est la surface des
    adaptateurs Codex. La version script visait `.codex/skills/recap/SKILL.md`,
    un dossier qui n'existe pas — le garde ne regardant que le chemin, le test
    passait sans jamais prouver qu'une skill livrée était protégée.
    """
    skill = REPO / ".agents" / "skills" / "recap" / "SKILL.md"
    assert skill.exists(), f"cible de test absente : {skill}"
    assert run("pre-write-guards.py", write_payload(str(skill))) == 2


def test_write_dispatcher_laisse_passer_hors_scope():
    hors_scope = REPO / "memory" / "x.md"
    assert run("pre-write-guards.py", write_payload(str(hors_scope))) == 0
