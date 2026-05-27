---
name: repo-scope-guard-hook
description: Triplet auth-detector+repo-scope-guard+auth-cleanup bloquant acces repos voisins neot-v2/ depuis neo_ia
metadata: 
  node_type: memory
  type: project
  originSessionId: e3438a06-ff07-4470-93a8-d0fcd072063d
---

Paire de hooks (+ cleanup) déployée dans neo_ia pour contrôler l'accès aux repos voisins de neot-v2/.

**Why:** neo_ia ne doit accéder qu'à neo_ia/ et ia_back/ sans permission explicite. Les autres ~60 repos de neot-v2 sont hors scope sauf autorisation Raphael dans le prompt.

**How to apply:** Pattern réutilisable pour tout repo avec voisins dans un répertoire parent commun.

## Fichiers

- `.claude/hooks/auth-detector.py` — UserPromptSubmit : détecte phrases d'autorisation → crée markers `.repo-auth-<repo>`
- `.claude/hooks/repo-scope-guard.py` — PreToolUse : résout tous les chemins, bloque si hors neo_ia/ia_back sans marker
- `.claude/hooks/auth-cleanup.py` — SessionStart : supprime tous `.repo-auth-*` au démarrage

## Design decisions

- `[\w-]+` dans les regex (pas `\w+`) pour capturer les noms avec tirets (mcp-obsidian-brain, neoteem-brain, etc.)
- `Path.resolve(strict=False)` — le fichier peut ne pas encore exister (Write d'un nouveau fichier)
- CWD depuis stdin JSON (`data.get("cwd")`), pas `os.getcwd()` — fiable avec additionalDirectories
- Whitelist dynamique via `os.listdir(neot-v2/)` — jamais de liste hardcodée
- Markers sans TTL : existence seule, reset complet SessionStart
- Chemins hors neot-v2/ (system, home, stdlib) → toujours autorisés
- Bash : split sur espaces, filter tokens avec `/` ou `\`, résolution contre cwd — pas de regex fragile

## Patterns reconnus (auth-detector)

- `autorisé X` / `autorisé l'accès à X` / `autorisé le repo X`
- `regarde X` / `regarde dans X` / `regarde le repo X`
- `check X` / `check dans X` / `check le repo X`
- `accès au X` / `accès à X`
- `tu peux aller dans X` / `tu peux regarder X`

## Tests comportementaux validés

- Read ../bdd/foo.sql → exit 2 (bdd bloqué)
- Read ../ia_back/... → exit 0 (libre)
- Read app/main.py → exit 0 (dans neo_ia)
- Read ../bdd/ avec marker → exit 0 (autorisé)
- auth-detector "autorise bdd" → marker créé
- auth-detector "regarde le code" → pas de marker (mot non-repo)
- auth-detector "regarde mcp-obsidian-brain" → marker avec tiret créé
- auth-cleanup → supprime tous les markers existants
