---
name: cd-sous-dossier-fausse-chemins-relatifs
description: "Un cd dans un sous-dossier (ex: mcp-forge-brain/) persiste entre Bash calls et fait taper les commandes relatives suivantes (ls .claude/, git ls-files, find) dans le mauvais dossier — faux constat 'le dossier est vide'. Repartir du git rev-parse --show-toplevel"
metadata:
  type: feedback
---

Un `cd` dans un sous-dossier persiste entre les Bash calls (le CWD ne se réinitialise pas). Les commandes relatives suivantes (`ls .claude/`, `git ls-files .claude/`, `find .claude`) tapent alors dans `<sous-dossier>/.claude/` au lieu de la racine du repo. Résultat : faux constat alarmant « le dossier est vide / les fichiers ont disparu ».

**Why:** Session 2026-05-27 (Mémoire Portable). Après `cd mcp-forge-brain && pytest`, mes `ls .claude/` regardaient `mcp-forge-brain/.claude/` (qui ne contient qu'`agent-memory/`). J'ai cru pendant 4 tours que skills/agents/hooks/settings.json avaient disparu, alors qu'ils étaient intacts à la racine. Fausse alerte pure, causée par le CWD déplacé.

**How to apply:**
1. Pour un diagnostic de structure repo, TOUJOURS partir d'un chemin absolu ou faire `cd "$(git rev-parse --show-toplevel)"` en début de commande.
2. Si un constat est surprenant (« dossier vide », « fichier disparu », « 0 tracké »), vérifier `pwd` AVANT de conclure. Un constat contre-intuitif = d'abord suspecter l'environnement (CWD, scope), pas les données.
3. Lié au feedback existant : `git -C <path>` plutôt que `cd <path> && git` ([[git-C-pas-cd-multi-repo]]). Même cause racine : le CWD persistant.

Référence : [[verify-exhaustive-claims]] (corollaire baseline tests même session).
