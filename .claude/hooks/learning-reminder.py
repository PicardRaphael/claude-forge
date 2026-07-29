#!/usr/bin/env python3
"""Learning detector — Stop hook. Alerte SEULEMENT s'il reste de la matière.

Ancien comportement : rappel systématique à chaque fin de session. Mesure sur les
transcripts : 8 « rien à sauvegarder » et zéro capture attribuable au hook — la
capitalisation arrive PENDANT la session, poussée par les rules en pré-action.
Un rappel qui pose toujours la question est ignoré ; un détecteur qui ne parle
que quand il a trouvé quelque chose est lu.

Comportement : lit le transcript de la session (chemin fourni par le harness),
cherche des SIGNAUX d'apprentissage (feedback de Raphael, erreur corrigée, claim
mesurée fausse, gotcha) ET vérifie si une capitalisation a déjà eu lieu.
- signaux + aucune capitalisation -> decision:block en citant ce qui est détecté
- rien trouvé, ou déjà capitalisé   -> exit 0 SILENCIEUX

Anti-boucle : `stop_hook_active` (le hook précédent jetait son stdin, donc ne le
testait jamais) + marqueur par session_id (l'ancien marqueur était global : deux
sessions concurrentes se le volaient). Fail-open partout.
"""
import json
import os
import re
import sys
import tempfile

# Assez pour couvrir une session longue sans lire un fichier de plusieurs Mo.
_TAIL_LINES = 4000

# Signaux d'apprentissage — formulations de Raphael et faits mesurés.
_SIGNALS = (
    (re.compile(r"\b(?:faut (?:pas|jamais)|ne (?:refais|refait) (?:plus|jamais)|"
                r"attention (?:car|à|a)\b|c'est faux|c'est pas (?:ça|ca|bon)|"
                r"tu (?:as|a) tort|pas comme ça|pas comme ca)", re.I),
     "correction explicite de Raphael"),
    (re.compile(r"\b(?:desormais|dorenavant|à partir de maintenant|"
                r"a partir de maintenant|nouvelle (?:norme|règle|regle)|"
                r"devient la (?:norme|règle|regle))", re.I),
     "nouvelle norme énoncée"),
    (re.compile(r"\b(?:péri(?:mé|me)|obsol(?:è|e)te|plus (?:valide|à jour|a jour)|"
                r"claim fausse|fait faux|était faux|etait faux)", re.I),
     "doctrine mesurée périmée ou fausse"),
    (re.compile(r"\b(?:gotcha|piège découvert|piege decouvert|"
                r"gard(?:e|e-fou) (?:manquant|absent)|bug (?:trouvé|trouve|réel|reel))", re.I),
     "gotcha ou bug découvert"),
)

# Preuves qu'une capitalisation a déjà eu lieu dans la session.
_CAPITALIZED = re.compile(
    r"(?:memory/(?:feedback|reference|project|user)_[a-z0-9_-]+\.md"
    r"|mcp__forge-brain__(?:create_note|append_note|insert_section|update_note"
    r"|append_note_by_path|insert_section_by_path|update_note_by_path)"
    r"|Knowledge/(?:erreurs|critiques|decisions|questions)/)",
    re.I,
)


def _tail(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.readlines()[-_TAIL_LINES:]
    except OSError:
        return []


def _texts(lines):
    """Extrait le texte utile des events du transcript (user + assistant)."""
    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue
        try:
            event = json.loads(raw)
        except ValueError:
            continue
        message = event.get("message") or {}
        content = message.get("content")
        if isinstance(content, str):
            yield content
        elif isinstance(content, list):
            for block in content:
                if isinstance(block, dict):
                    if block.get("type") == "text":
                        yield block.get("text") or ""
                    elif block.get("type") == "tool_use":
                        yield json.dumps(block.get("input") or {}, ensure_ascii=False)


def analyse(lines):
    """Retourne (signaux détectés, capitalisation déjà faite)."""
    found, capitalized = [], False
    for text in _texts(lines):
        if not capitalized and _CAPITALIZED.search(text):
            capitalized = True
        for pattern, label in _SIGNALS:
            if label not in found and pattern.search(text):
                found.append(label)
    return found, capitalized


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    try:
        # Anti-boucle : ce Stop vient déjà d'un blocage de hook.
        if data.get("stop_hook_active"):
            sys.exit(0)

        session = str(data.get("session_id") or "nosession")
        marker = os.path.join(tempfile.gettempdir(), f"forge-learning-{session}")
        if os.path.exists(marker):
            sys.exit(0)

        transcript = data.get("transcript_path")
        if not transcript or not os.path.isfile(transcript):
            sys.exit(0)  # sans transcript, pas de détection possible

        signals, capitalized = analyse(_tail(transcript))
        if capitalized or not signals:
            sys.exit(0)  # silencieux : rien à dire

        # Il reste de la matière — on ne le dira qu'une fois par session.
        try:
            with open(marker, "w", encoding="utf-8") as fh:
                fh.write("1")
        except OSError:
            sys.exit(0)  # marqueur impossible -> ne pas risquer la boucle

        detected = "\n".join(f"  - {s}" for s in signals)
        reason = (
            "Signaux d'apprentissage détectés dans cette session, sans trace de "
            f"capitalisation :\n{detected}\n\n"
            "Capitaliser maintenant, ou dire en une ligne pourquoi ça ne le mérite pas :\n"
            "- `search_brain` d'abord — enrichir une note existante plutôt qu'en créer une\n"
            "- exception empirique -> `memory/feedback_*` + pointeur MEMORY.md\n"
            "- doctrine réutilisable -> note vault (corps réécrit en place, pas d'addendum)\n\n"
            "Ne RIEN inventer pour remplir la liste : un signal mal détecté se dit et se ferme."
        )
        print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False))
        sys.exit(0)
    except Exception:
        sys.exit(0)


if __name__ == "__main__":
    main()
