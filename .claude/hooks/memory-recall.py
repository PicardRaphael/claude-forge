#!/usr/bin/env python3
"""UserPromptSubmit — injecte les 3 souvenirs pertinents, ou RIEN.

Le trou comble : les hooks memoire existants surveillent la saturation
(SessionStart) ou rappellent de capitaliser (Stop). Aucun ne fait remonter le
fait utile AU MOMENT ou il eviterait l'erreur. Ici on inverse : on lit le
prompt, on score, et on n'injecte que ce qui matche — souvent rien.

Pourquoi des plafonds si bas (3 max, seuil haut, 1200 chars) : le texte injecte
est SAUVE dans le transcript et renvoye a chaque requete suivante. Un rappel
inutile coute donc a TOUS les tours ; un rappel manque ne coute qu'une fois.
L'asymetrie impose la prudence.

Selection : champ `trigger:` du frontmatter (mots-cles + fragments de chemin),
repli sur `name` + `description`. Purement lexical — pas de modele, pas
d'embedding : quelques millisecondes, zero token depense pour choisir.
Limite assumee : un fait range sous un vocabulaire different du prompt reste
invisible. Le correctif est d'enrichir `trigger:`, pas d'ajouter un index
vectoriel.

Perf mesuree (profilage 29 juil. 2026, 85 fichiers) : demarrage de `py` sous
Windows = ~420 ms INCOMPRESSIBLE, load_index = 1,6 ms, scoring = 2,9 ms, soit
~60 ms de travail reel. Le plafond « < 500 ms » de la doctrine hook est donc
inatteignable pour tout hook Python sous Windows — 26 hooks existants sont deja
dans ce regime. Ne pas re-optimiser ce script en croyant que le cout vient de la
lecture des fichiers : il vient de l'interpreteur.

Fail-open partout : toute erreur -> exit 0, aucune injection.
"""
import hashlib
import json
import os
import re
import sys
import tempfile

_HOOK_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_HOOK_DIR))
_MEMORY_DIR = os.path.join(_REPO_ROOT, "memory")

# Le hook tourne a CHAQUE prompt : ouvrir 85 fichiers y coutait 792 ms, au-dela
# du plafond de 500 ms. L'index est donc mis en cache, invalide par la signature
# (nom, mtime, taille) du dossier — un fichier touche suffit a reconstruire.
_CACHE = os.path.join(
    tempfile.gettempdir(),
    "cc-memrecall-" + hashlib.md5(_MEMORY_DIR.encode("utf-8")).hexdigest()[:12] + ".json",
)

_MAX_INJECTED = 3
_MIN_SCORE = 4
_MAX_CHARS = 1200
_MIN_PROMPT_LEN = 15

_EXCLUDED = {"MEMORY.md", "_index_archive.md", "review-recurrences.md"}

_STOP = {
    "le", "la", "les", "un", "une", "des", "de", "du", "et", "ou", "au",
    "aux", "en", "dans", "sur", "pour", "par", "avec", "sans", "que", "qui",
    "quoi", "dont", "est", "sont", "ete", "faire", "fait", "fais", "peux",
    "peut", "veux", "veut", "dois", "doit", "tout", "tous", "toute", "plus",
    "moins", "tres", "bien", "mal", "the", "and", "for", "with", "this",
    "that", "you", "your", "not", "are", "was", "can", "will", "from",
    "nous", "vous", "ils", "cette", "ces", "mon", "mes", "ton", "tes",
    "son", "sa", "ses", "quand", "comme", "alors", "donc", "aussi", "meme",
}

_WORD = re.compile(r"[a-z0-9_-]{3,}")


def _tokens(text):
    return {w for w in _WORD.findall(text.lower()) if w not in _STOP}


def _parse(path):
    """(name, description, triggers) depuis le frontmatter, ou None."""
    try:
        with open(path, "r", encoding="utf-8-sig") as fh:
            head = fh.read(2500)
    except OSError:
        return None
    if not head.startswith("---"):
        return None
    parts = head.split("---", 2)
    if len(parts) < 3:
        return None
    name, desc, triggers = "", "", []
    for line in parts[1].splitlines():
        line = line.strip()
        if line.startswith("name:"):
            name = line[5:].strip().strip("\"'")
        elif line.startswith("description:"):
            desc = line[12:].strip().strip("\"'")
        elif line.startswith("trigger:"):
            triggers = [t.strip().strip("\"'") for t in line[8:].split(",") if t.strip()]
    return name, desc, triggers


_FLEX = ("e", "es", "er", "ez", "ee", "ees", "ent", "ons", "ait", "aient",
         "s", "r", "rs", "nt")


def _contains(needle, haystack):
    """Sous-chaine AVEC frontieres de mot, flexion francaise toleree en fin.

    Un `in` nu fait matcher les triggers courts sur n'importe quel mot qui les
    contient : `main` dans « maintenant », `red` dans « redemarre », `log` dans
    « logique », `go` dans « algo ». Faux positif mesure le 29 juil. 2026
    (« fais le 2 maintenant » -> merge-ref-morte-croisee via `main`). 42 des
    triggers poses font 4 caracteres ou moins : le risque est structurel.

    Meme correctif que `skill-activation.py` du repo, meme event, meme cause :
    « Word-boundary regex (avoids "done" matching "abandoned") ». Ecrit a la
    main plutot qu'en regex pour ne pas avoir a echapper les triggers qui
    contiennent des metacaracteres (`git -C`, `4.8`, `.agents`).

    La frontiere STRICTE seule a coute un rappel legitime (regression mesuree
    le meme jour : « audite la config » ne matchait plus le trigger `audit`).
    Un trigger de 4+ caracteres accepte donc un suffixe de flexion : `audit`
    matche « audite / auditer / audites », `cree` matche « creer ». Le seuil de
    4 et la liste FERMEE de suffixes preservent les rejets : « bundle » n'est
    pas `bun` + flexion (`dle` absent de la liste), ni « scandale » `scan`,
    ni « portable » `port`, ni « edition » `edit`. Limite connue et assumee :
    `scan` ne matche pas « scanner » (suffixe `ner`) — l'ajouter ouvrirait
    trop. Frontiere AVANT le needle : toujours stricte.
    """
    n = len(needle)
    if not n:
        return False
    start = 0
    while True:
        i = haystack.find(needle, start)
        if i < 0:
            return False
        before = haystack[i - 1] if i > 0 else ""
        if not (before.isalnum() or before == "_"):
            j = i + n
            after = haystack[j] if j < len(haystack) else ""
            if not (after.isalnum() or after == "_"):
                return True
            if n >= 4:
                k = j
                while k < len(haystack) and (haystack[k].isalnum() or haystack[k] == "_"):
                    k += 1
                if haystack[j:k] in _FLEX:
                    return True
        start = i + 1


def score(prompt_tokens, prompt_raw, name, desc, triggers):
    """Score lexical : `trigger:` pese lourd, name/description en appoint."""
    total = 0
    for trig in triggers:
        t = trig.lower().strip()
        if not t:
            continue
        if "/" in t or "*" in t:
            core = t.strip("*").strip("/").split("*")[0].strip("/")
            if core and _contains(core, prompt_raw):
                total += 4
        elif _contains(t, prompt_raw):
            total += 4
        elif _tokens(t) & prompt_tokens:
            total += 2
    total += 2 * len(_tokens(name.replace("-", " ").replace("_", " ")) & prompt_tokens)
    total += len(_tokens(desc) & prompt_tokens)
    return total


def _signature():
    """Empreinte du dossier — change des qu'un fichier est touche."""
    parts = []
    for entry in sorted(os.listdir(_MEMORY_DIR)):
        if entry.endswith(".md") and entry not in _EXCLUDED:
            st = os.stat(os.path.join(_MEMORY_DIR, entry))
            parts.append(f"{entry}:{int(st.st_mtime)}:{st.st_size}")
    return hashlib.md5("|".join(parts).encode("utf-8")).hexdigest()


def _build_index():
    index = []
    for entry in sorted(os.listdir(_MEMORY_DIR)):
        if not entry.endswith(".md") or entry in _EXCLUDED:
            continue
        parsed = _parse(os.path.join(_MEMORY_DIR, entry))
        if parsed:
            name, desc, triggers = parsed
            index.append({"f": entry, "n": name, "d": desc, "t": triggers})
    return index


def load_index():
    """Index en cache, reconstruit si le dossier a bouge. Fail-open."""
    try:
        sig = _signature()
    except OSError:
        return _build_index()
    try:
        with open(_CACHE, "r", encoding="utf-8") as fh:
            cached = json.load(fh)
        if cached.get("sig") == sig:
            return cached.get("index") or []
    except Exception:
        pass
    index = _build_index()
    try:
        with open(_CACHE, "w", encoding="utf-8") as fh:
            json.dump({"sig": sig, "index": index}, fh, ensure_ascii=False)
    except OSError:
        pass  # cache impossible : on continue sans, jamais de crash
    return index


def collect(prompt_raw, prompt_tokens):
    hits = []
    for item in load_index():
        value = score(prompt_tokens, prompt_raw, item["n"], item["d"], item["t"])
        if value >= _MIN_SCORE:
            hits.append((value, item["n"] or item["f"][:-3], item["d"], item["f"]))
    hits.sort(key=lambda h: (-h[0], h[3]))
    return hits


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    try:
        prompt = (data.get("prompt") or "").strip()
        if len(prompt) < _MIN_PROMPT_LEN or not os.path.isdir(_MEMORY_DIR):
            sys.exit(0)

        prompt_raw = prompt.lower()
        prompt_tokens = _tokens(prompt_raw)
        if not prompt_tokens:
            sys.exit(0)

        hits = collect(prompt_raw, prompt_tokens)
        if not hits:
            sys.exit(0)  # cas le plus frequent, et c'est voulu

        lines, used = [], 0
        for _, name, desc, fname in hits[:_MAX_INJECTED]:
            line = f"- **{name}** (`memory/{fname}`) — {desc[:200]}"
            if used + len(line) > _MAX_CHARS:
                break
            lines.append(line)
            used += len(line)
        if not lines:
            sys.exit(0)

        # Formule en FAITS, jamais en imperatif. Docs hooks : « Write the text as
        # factual statements rather than imperative system instructions. Text
        # framed as out-of-band system commands can trigger Claude's
        # prompt-injection defenses, which causes Claude to surface the text to
        # you instead of treating it as context. » Un « ouvre ceci » ferait
        # AFFICHER le rappel au lieu de le faire lire.
        noun = "souvenir" if len(lines) == 1 else "souvenirs"
        context = (
            f"Ce repo contient {len(lines)} {noun} dont les mots-clés recoupent "
            "la demande en cours :\n" + "\n".join(lines)
        )
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": context,
            }
        }, ensure_ascii=False))
        sys.exit(0)
    except Exception:
        sys.exit(0)


if __name__ == "__main__":
    main()
