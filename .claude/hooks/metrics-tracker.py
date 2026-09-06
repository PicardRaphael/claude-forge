#!/usr/bin/env python3
"""Journalise l'usage des outils et des commandes dans .claude/_metrics/<date>.jsonl.

Ce que ce hook mesure vraiment :
  - QUEL outil a ete appele, et sur QUELLE cible quand l'outil en porte une
    (champ `target` : nom de skill, type de sous-agent, nom de commande).
  - La TAILLE des entrees/sorties d'outil, en caracteres.

Ce qu'il ne mesure PAS : `estimated_tokens` est un proxy de volume d'I/O outils
(chars / 3.3), jamais les tokens API reels de la session — un hook ne voit ni le
contexte cumule ni la facturation. La cle est conservee parce que les skills
io-daily / io-week la consomment.

Deux evenements alimentent le meme journal :
  - PostToolUse      : un outil vient de s'executer.
  - UserPromptSubmit : une commande slash a ete tapee. Ce chemin n'est PAS un
    appel d'outil et resterait invisible autrement, alors qu'il porte les
    invocations de skills les plus frequentes. Seul le NOM de la commande est
    retenu, jamais le texte du prompt.

Non bloquant : sortie 0 en toute circonstance, y compris sur payload illisible
ou disque en erreur. Une metrique perdue ne doit jamais casser un appel d'outil.
"""
import json
import os
import re
import sys
from datetime import datetime, timezone

METRICS_DIR = None

# Outils dont l'identite de la cible vit dans un champ nomme de tool_input.
_TARGET_KEYS = {
    "Skill": "skill",
    "Agent": "subagent_type",
    "Task": "subagent_type",
}

# Forme balisee d'une commande dans un prompt : <command-name>/done</command-name>.
# Seul le nom est capture — jamais ce qui suit, ou les arguments fuiraient.
_BALISE_COMMANDE = re.compile(r"<command-name>\s*/?([A-Za-z0-9_:-]+)", re.IGNORECASE)


def _repo_root():
    """Racine du depot principal, meme depuis un worktree.

    Les hooks d'un worktree vivent sous <repo>/.claude/worktrees/<nom>/.claude/
    hooks/. Ecrire les metriques la-bas les perdrait a la suppression du
    worktree, alors que l'interet du journal est de s'accumuler dans la duree.
    Toutes les surfaces ecrivent donc dans le journal du depot principal.

    Resolution par __file__ et non par CLAUDE_PROJECT_DIR : cette variable n'est
    pas garantie peuplee dans le process d'un hook, et __file__ reste juste quel
    que soit le cwd d'ou le hook est declenche.
    """
    here = os.path.abspath(__file__)
    parts = here.replace("\\", "/").split("/")
    for i in range(len(parts) - 1, 0, -1):
        if parts[i] == "worktrees" and parts[i - 1] == ".claude":
            return "/".join(parts[: i - 1])
    return os.path.dirname(os.path.dirname(os.path.dirname(here)))


def _get_metrics_dir(data):
    return os.path.join(_repo_root(), ".claude", "_metrics")


def _char_count(value):
    try:
        return len(json.dumps(value, default=str))
    except Exception:
        return len(str(value))


def _command_name(raw):
    """Nom nu d'une commande slash : '/done --force' -> 'done'.

    Ne retourne que le premier token, jamais les arguments : ils peuvent
    contenir du texte utilisateur qui n'a rien a faire dans un journal.

    Le harness livre le prompt tel qu'il a ete tape — c'est cette forme brute
    que lit skill-activation.py pour se taire sur les commandes slash. La forme
    balisee est acceptee en repli : si elle devenait un jour la seule livree, ce
    chemin cesserait d'enregistrer sans qu'aucune erreur ne le signale, ce qui
    est exactement le genre de dette silencieuse que ce journal existe pour
    lever.
    """
    cmd = str(raw or "").strip()
    if not cmd.startswith("/"):
        balise = _BALISE_COMMANDE.search(cmd)
        return balise.group(1) if balise else ""
    cmd = cmd[1:].strip()
    if not cmd:
        return ""
    name = cmd.split()[0]
    return name if name.replace("-", "").replace("_", "").replace(":", "").isalnum() else ""


def _target(tool_name, tool_input):
    """Identifiant de la cible d'un outil, chaine vide s'il n'en porte pas.

    Lu directement dans le tool_input de l'appel, sans parser le transcript :
    l'identite est presente dans l'appel lui-meme. Ce hook n'attribue jamais un
    outil quelconque a la skill qui l'a cause — ca demanderait le transcript et
    ce n'est pas ce qui est promis ici.
    """
    if not isinstance(tool_input, dict):
        return ""
    key = _TARGET_KEYS.get(tool_name)
    if key:
        return str(tool_input.get(key) or "")
    if tool_name == "SlashCommand":
        return _command_name(tool_input.get("command"))
    return ""


def _build_record(data):
    """Enregistrement a journaliser, ou None s'il n'y a rien a retenir."""
    event = data.get("hook_event_name", "")

    if event == "UserPromptSubmit":
        prompt = data.get("prompt", "")
        name = _command_name(prompt)
        if not name:
            return None
        tool_name = "UserPrompt"
        target = name
        input_chars = len(str(prompt))
        output_chars = 0
    else:
        tool_name = data.get("tool_name", "")
        # Sans nom d'outil, il n'y a rien a attribuer. Un payload inattendu
        # tomberait ici et remplirait le journal de {"tool": ""} sans erreur.
        if not tool_name:
            return None
        tool_input = data.get("tool_input", {})
        target = _target(tool_name, tool_input)
        input_chars = _char_count(tool_input)
        output_chars = _char_count(data.get("tool_response", ""))

    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "session_id": data.get("session_id", ""),
        "tool": tool_name,
        "input_chars": input_chars,
        "output_chars": output_chars,
        "estimated_tokens": int((input_chars + output_chars) / 3.3),
    }
    if target:
        record["target"] = target
    return record


def main():
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            sys.exit(0)
        data = json.loads(raw)
    except Exception:
        sys.exit(0)

    try:
        record = _build_record(data)
        if record is None:
            sys.exit(0)

        metrics_dir = METRICS_DIR if METRICS_DIR is not None else _get_metrics_dir(data)
        os.makedirs(metrics_dir, exist_ok=True)

        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        log_path = os.path.join(metrics_dir, f"{today}.jsonl")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    except Exception:
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
