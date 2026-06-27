---
name: python-script-refactor-masse
description: ALWAYS invoke when refactoring the same pattern across >10 files. DO NOT use sequential Edit tool calls -- one Python script with regex beats them all.
allowed-tools: Read, Write, Edit, Bash, Glob
effort: high
user-invocable: true
---

## Role

Template Python reutilisable pour refactors de masse (meme pattern, >10 fichiers).
Valide 25 mai 2026 sur ia_back : 308 lignes economisees en 1 commande vs sequence Edit.

## Quand utiliser

- Meme pattern a changer sur >10 fichiers
- Renommage variable/fonction/import
- Ajout/suppression de ligne selon critere
- Migration syntaxe

## Template Python

    #!/usr/bin/env python3
    import re, pathlib

    ROOT = pathlib.Path(r"[CHEMIN ABSOLU DU REPO]")  # resoudre via: git rev-parse --show-toplevel
    GLOB_PATTERN = "**/*.py"
    DRY_RUN = True  # mettre False pour appliquer

    OLD_PATTERN = re.compile(r"[PATTERN REGEX]")
    NEW_STRING = r"[REMPLACEMENT]"

    changed = []
    for fpath in ROOT.glob(GLOB_PATTERN):
        content = fpath.read_text(encoding="utf-8")
        new_content = OLD_PATTERN.sub(NEW_STRING, content)
        if new_content != content:
            changed.append(fpath)
            if not DRY_RUN:
                fpath.write_text(new_content, encoding="utf-8")

    print(f"{'DRY RUN -- ' if DRY_RUN else ''}Fichiers modifies : {len(changed)}")
    for f in changed:
        print(f"  {f.relative_to(ROOT)}")

## Etapes

1. Identifier le pattern : grep pour confirmer la portee avant d ecrire
2. Ecrire le script dans un fichier temporaire (ex: _refactor_tmp.py)
3. DRY_RUN = True : executer, verifier la liste des fichiers touches
4. DRY_RUN = False : executer pour appliquer
5. Supprimer le script temporaire apres validation

## Gotchas

- Toujours encoding="utf-8" sur read_text/write_text -- Windows utilise cp1252 par defaut
- Verifier ROOT avant execution : print(ROOT.exists()) -- chemin faux = 0 resultats silencieux
- re.escape() pour les patterns litteraux contenant . ( ) etc.
- Backreferences dans NEW_STRING :   fonctionnent dans re.sub pas str.replace
- JAMAIS  dans backticks shell -- quoting Windows casse tout
- Script temporaire = transitoire : supprimer apres application (anti-pattern .proposed)

## Exemples concrets

Renommage import (ia_back 25 mai 2026) :
    OLD_PATTERN = re.compile(r"from drizzle import (\w+)")
    NEW_STRING = r"from postgres import "

Suppression de ligne :
    lines = content.splitlines(keepends=True)
    new_lines = [l for l in lines if "DEPRECATED_CALL(" not in l]

## Apprentissage

Feedback source : feedback_refactor_masse_script_python_regex.md
Valide 25 mai 2026 ia_back : 308 lignes economisees vs Edit sequentiels.
Si nouveau pattern valide -> ajouter dans Exemples concrets.
