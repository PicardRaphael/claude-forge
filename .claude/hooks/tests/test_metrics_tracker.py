#!/usr/bin/env python3
"""Tests fonctionnels de metrics-tracker.py (journal d'usage, non bloquant).

PERIMETRE : le hook est un logger fail-open. Ces tests verifient le format du
journal, l'identification de la cible (`target`), l'absence de fuite du contenu
des outils, et la sortie 0 sur entree cassee ou disque en erreur.

HORS PERIMETRE, volontairement : que le hook soit bien CABLE dans settings.json.
Les hooks sont figes au demarrage de la session, donc la preuve d'armement ne
peut pas etre produite depuis la session qui les ajoute — elle se fait a la
session suivante via /hooks.

Lancer : py -m pytest .claude/hooks/tests/test_metrics_tracker.py -v
"""
import glob
import importlib.util
import io
import json
import os
import sys

import pytest

_hook_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "metrics-tracker.py",
)
_spec = importlib.util.spec_from_file_location("metrics_tracker", _hook_path)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)


def _run_hook(stdin_data, monkeypatch, tmp_path):
    """Execute main() avec ce stdin, journal redirige vers tmp_path."""
    monkeypatch.setattr(_mod, "METRICS_DIR", str(tmp_path))
    monkeypatch.setattr("sys.stdin", io.StringIO(stdin_data))
    with pytest.raises(SystemExit) as exc:
        _mod.main()
    return exc.value.code


def _records(tmp_path):
    files = glob.glob(str(tmp_path / "*.jsonl"))
    out = []
    for path in files:
        with open(path, encoding="utf-8") as fh:
            out.extend(json.loads(l) for l in fh if l.strip())
    return out


# ===========================================================================
# Nominal
# ===========================================================================

def test_log_normal(tmp_path, monkeypatch):
    """Un Read valide produit une ligne portant tous les champs attendus."""
    payload = json.dumps({
        "session_id": "abc123",
        "tool_name": "Read",
        "tool_input": {"file_path": "/some/file.py"},
        "tool_response": "line1\nline2\n",
    })
    assert _run_hook(payload, monkeypatch, tmp_path) == 0
    records = _records(tmp_path)
    assert len(records) == 1
    rec = records[0]
    assert rec["session_id"] == "abc123"
    assert rec["tool"] == "Read"
    assert isinstance(rec["input_chars"], int) and rec["input_chars"] > 0
    assert isinstance(rec["output_chars"], int) and rec["output_chars"] > 0
    assert isinstance(rec["estimated_tokens"], int)
    assert "ts" in rec


def test_log_mcp_tool(tmp_path, monkeypatch):
    """Le nom complet d'un outil MCP est journalise tel quel."""
    payload = json.dumps({
        "session_id": "mcp_session",
        "tool_name": "mcp__forge-brain__read_note",
        "tool_input": {"file": "comment-creer-hook"},
        "tool_response": {"content": "some vault content"},
    })
    assert _run_hook(payload, monkeypatch, tmp_path) == 0
    rec = _records(tmp_path)[0]
    assert rec["tool"] == "mcp__forge-brain__read_note"
    assert rec["estimated_tokens"] > 0


# ===========================================================================
# Identification de la cible — la raison d'etre du journal
# ===========================================================================

def test_target_skill(tmp_path, monkeypatch):
    """Un appel Skill nomme la skill : sans ca le journal est inexploitable."""
    payload = json.dumps({
        "session_id": "s",
        "tool_name": "Skill",
        "tool_input": {"skill": "done", "args": "capitalisation"},
        "tool_response": "ok",
    })
    assert _run_hook(payload, monkeypatch, tmp_path) == 0
    assert _records(tmp_path)[0]["target"] == "done"


def test_target_skill_scopee_worktree(tmp_path, monkeypatch):
    """Une skill scopee garde son prefixe : la normalisation est au lecteur."""
    payload = json.dumps({
        "session_id": "s",
        "tool_name": "Skill",
        "tool_input": {"skill": ".claude/worktrees/x:hook-creator"},
        "tool_response": "ok",
    })
    assert _run_hook(payload, monkeypatch, tmp_path) == 0
    assert _records(tmp_path)[0]["target"] == ".claude/worktrees/x:hook-creator"


def test_target_agent(tmp_path, monkeypatch):
    """Un dispatch d'agent nomme le type de sous-agent."""
    payload = json.dumps({
        "session_id": "s",
        "tool_name": "Agent",
        "tool_input": {"subagent_type": "repo-inspector", "prompt": "audit"},
        "tool_response": "rapport",
    })
    assert _run_hook(payload, monkeypatch, tmp_path) == 0
    assert _records(tmp_path)[0]["target"] == "repo-inspector"


def test_target_task_alias(tmp_path, monkeypatch):
    """Task est traite comme Agent (meme champ subagent_type)."""
    payload = json.dumps({
        "session_id": "s",
        "tool_name": "Task",
        "tool_input": {"subagent_type": "code-dev"},
        "tool_response": "ok",
    })
    assert _run_hook(payload, monkeypatch, tmp_path) == 0
    assert _records(tmp_path)[0]["target"] == "code-dev"


def test_target_slash_command(tmp_path, monkeypatch):
    """SlashCommand : seul le nom nu, jamais les arguments."""
    payload = json.dumps({
        "session_id": "s",
        "tool_name": "SlashCommand",
        "tool_input": {"command": "/recap --full contexte secret"},
        "tool_response": "ok",
    })
    assert _run_hook(payload, monkeypatch, tmp_path) == 0
    rec = _records(tmp_path)[0]
    assert rec["target"] == "recap"
    assert "secret" not in json.dumps(rec)


def test_target_absent_pour_outil_ordinaire(tmp_path, monkeypatch):
    """Un outil sans cible n'invente pas de target : la cle est absente."""
    payload = json.dumps({
        "session_id": "s",
        "tool_name": "Bash",
        "tool_input": {"command": "ls"},
        "tool_response": "a b c",
    })
    assert _run_hook(payload, monkeypatch, tmp_path) == 0
    assert "target" not in _records(tmp_path)[0]


def test_agent_sans_subagent_type(tmp_path, monkeypatch):
    """Agent sans type declare : cle omise plutot que chaine vide."""
    payload = json.dumps({
        "session_id": "s",
        "tool_name": "Agent",
        "tool_input": {"prompt": "fais un truc"},
        "tool_response": "ok",
    })
    assert _run_hook(payload, monkeypatch, tmp_path) == 0
    assert "target" not in _records(tmp_path)[0]


# ===========================================================================
# UserPromptSubmit — la commande tapee n'est pas un appel d'outil
# ===========================================================================

def test_slash_tapee_est_capturee(tmp_path, monkeypatch):
    """Une commande tapee par l'utilisateur ne passe par aucun outil.

    Sans cette branche, les skills les plus utilisees restent invisibles.
    """
    payload = json.dumps({
        "session_id": "s",
        "hook_event_name": "UserPromptSubmit",
        "prompt": "/done",
    })
    assert _run_hook(payload, monkeypatch, tmp_path) == 0
    rec = _records(tmp_path)[0]
    assert rec["tool"] == "UserPrompt"
    assert rec["target"] == "done"


def test_prompt_ordinaire_non_journalise(tmp_path, monkeypatch):
    """Un prompt qui n'est pas une commande n'ecrit rien : pas de collecte."""
    payload = json.dumps({
        "session_id": "s",
        "hook_event_name": "UserPromptSubmit",
        "prompt": "regarde ce bug dans le module de paiement",
    })
    assert _run_hook(payload, monkeypatch, tmp_path) == 0
    assert _records(tmp_path) == []


def test_prompt_slash_avec_arguments_ne_fuit_pas(tmp_path, monkeypatch):
    """Seul le nom de commande est retenu, jamais le texte qui suit."""
    payload = json.dumps({
        "session_id": "s",
        "hook_event_name": "UserPromptSubmit",
        "prompt": "/spec mot-de-passe-prod-2026 et le reste du contexte",
    })
    assert _run_hook(payload, monkeypatch, tmp_path) == 0
    rec = _records(tmp_path)[0]
    assert rec["target"] == "spec"
    assert "mot-de-passe-prod-2026" not in json.dumps(rec)


def test_prompt_balise_est_capture(tmp_path, monkeypatch):
    """Repli sur la forme balisee.

    Le harness livre aujourd'hui le prompt brut. S'il livrait la forme balisee,
    ce chemin cesserait d'enregistrer sans lever la moindre erreur — donc sans
    que rien ne le signale. Le repli coute une regex et supprime ce risque.
    """
    payload = json.dumps({
        "session_id": "s",
        "hook_event_name": "UserPromptSubmit",
        "prompt": "<command-name>/done</command-name>",
    })
    assert _run_hook(payload, monkeypatch, tmp_path) == 0
    rec = _records(tmp_path)[0]
    assert rec["tool"] == "UserPrompt"
    assert rec["target"] == "done"


def test_prompt_balise_avec_arguments_ne_fuit_pas(tmp_path, monkeypatch):
    """La garantie du chemin nominal vaut aussi sur le repli."""
    payload = json.dumps({
        "session_id": "s",
        "hook_event_name": "UserPromptSubmit",
        "prompt": (
            "<command-name>/spec</command-name>"
            "<command-args>mot-de-passe-prod-2026</command-args>"
        ),
    })
    assert _run_hook(payload, monkeypatch, tmp_path) == 0
    rec = _records(tmp_path)[0]
    assert rec["target"] == "spec"
    assert "mot-de-passe-prod-2026" not in json.dumps(rec)


# ===========================================================================
# Confidentialite — le journal ne doit porter que des tailles
# ===========================================================================

def test_aucun_contenu_outil_dans_le_journal(tmp_path, monkeypatch):
    """Ni tool_input ni tool_response ne doivent apparaitre dans le fichier."""
    payload = json.dumps({
        "session_id": "s",
        "tool_name": "Write",
        "tool_input": {"file_path": "/x.py", "content": "TOKEN_ULTRA_SECRET"},
        "tool_response": "REPONSE_CONFIDENTIELLE",
    })
    assert _run_hook(payload, monkeypatch, tmp_path) == 0
    brut = open(glob.glob(str(tmp_path / "*.jsonl"))[0], encoding="utf-8").read()
    assert "TOKEN_ULTRA_SECRET" not in brut
    assert "REPONSE_CONFIDENTIELLE" not in brut
    assert "/x.py" not in brut


# ===========================================================================
# Adverse — fail-open
# ===========================================================================

def test_stdin_absent(tmp_path, monkeypatch):
    """stdin vide : sortie 0, aucun fichier cree."""
    assert _run_hook("", monkeypatch, tmp_path) == 0
    assert glob.glob(str(tmp_path / "*.jsonl")) == []


def test_json_malformed(tmp_path, monkeypatch):
    """JSON casse : sortie 0, aucun fichier cree."""
    assert _run_hook("not json{", monkeypatch, tmp_path) == 0
    assert glob.glob(str(tmp_path / "*.jsonl")) == []


def test_payload_sans_nom_d_outil_n_ecrit_rien(tmp_path, monkeypatch):
    """Un payload qui ne nomme ni son event ni son outil n'est pas journalise.

    Sans cette garde, il tomberait dans le chemin outil et ecrirait une ligne
    {"tool": ""} — du bruit qu'aucune erreur ne viendrait signaler.
    """
    payload = json.dumps({"session_id": "s", "prompt": "un texte quelconque"})
    assert _run_hook(payload, monkeypatch, tmp_path) == 0
    assert _records(tmp_path) == []


def test_tool_input_non_dict(tmp_path, monkeypatch):
    """tool_input d'un type inattendu ne fait pas tomber le hook."""
    payload = json.dumps({
        "session_id": "s",
        "tool_name": "Skill",
        "tool_input": "une chaine, pas un objet",
        "tool_response": "ok",
    })
    assert _run_hook(payload, monkeypatch, tmp_path) == 0
    assert "target" not in _records(tmp_path)[0]


def test_write_permission_denied(tmp_path, monkeypatch):
    """OSError a l'ecriture : sortie 0, l'appel d'outil n'est pas casse."""
    payload = json.dumps({
        "session_id": "s1",
        "tool_name": "Write",
        "tool_input": {"file_path": "x.py"},
        "tool_response": "ok",
    })
    import builtins
    real_open = builtins.open

    def _blocked_open(path, *args, **kwargs):
        if str(path).endswith(".jsonl"):
            raise OSError("Permission denied")
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", _blocked_open)
    assert _run_hook(payload, monkeypatch, tmp_path) == 0


# ===========================================================================
# Resolution de chemin — un worktree ecrit dans le depot principal
# ===========================================================================

def test_repo_root_traverse_le_worktree(monkeypatch):
    """Depuis un worktree, la racine resolue est celle du depot principal.

    Sinon les metriques d'une session worktree disparaissent avec lui, alors
    que l'interet du journal est justement de s'accumuler.
    """
    faux = "C:/repo/.claude/worktrees/chantier/.claude/hooks/metrics-tracker.py"
    monkeypatch.setattr(_mod, "__file__", faux)
    assert _mod._repo_root().endswith("/repo")


def test_repo_root_hors_worktree(monkeypatch):
    """Hors worktree, la racine est le depot lui-meme."""
    faux = "C:/repo/.claude/hooks/metrics-tracker.py"
    monkeypatch.setattr(_mod, "__file__", faux)
    assert _mod._repo_root().replace("\\", "/").endswith("/repo")


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
