---
name: automemorydirectory-absolu-casse-multiprojet
description: "autoMemoryDirectory en chemin ABSOLU est global et fusionne les mémoires de TOUS les projets dans un seul dossier — casse le scoping multi-repos. Par défaut Claude Code scope déjà la mémoire par projet (~/.claude/projects/<encoded>/memory/). Voie élégante = variable projet si supportée"
metadata:
  type: feedback
---

`autoMemoryDirectory` avec un chemin ABSOLU (`C:\...\claude-forge\memory`) dans `~/.claude/settings.json` est **global** : il s'applique à TOUS les projets de la machine, fusionnant toutes leurs mémoires dans un seul dossier. À ÉVITER dès qu'il y a plus d'un projet sur la machine (cas multi-repos : claude-forge, neo_ia, ia_back, neoteem-brain, neofront).

**Why:** Session 2026-05-27 (Mémoire Portable). J'avais validé `autoMemoryDirectory` absolu sur le seul critère "satisfait le workflow cross-machine de claude-forge", sans tester l'hypothèse multi-projets. Raphael a un workflow multi-repos où chaque mémoire doit suivre SON repo. Le chemin absolu aurait fait lire/écrire la mémoire de neo_ia, ia_back, etc. dans `claude-forge/memory/`. Erreur de cadrage : validé pour un projet, cassé pour le réel multi-projets.

**Fait empirique confirmé** : SANS aucun `autoMemoryDirectory`, Claude Code scope déjà la mémoire par projet — chaque repo a son dossier encodé `~/.claude/projects/<encoded-repo-path>/memory/` (vérifié : 6 projets distincts, chacun son memory/). Le scoping par-projet est le comportement par défaut. Le problème de fusion n'apparaît QUE si on force un chemin absolu unique.

**How to apply:**
1. NE JAMAIS mettre `autoMemoryDirectory` en chemin absolu dès qu'il y a >1 projet sur la machine.
2. `autoMemoryDirectory: "${CLAUDE_PROJECT_DIR}/memory"` en global → NON SUPPORTÉ (doc Anthropic : valeur = chemin statique absolu/`~`, pas d'expansion de variable). Vérifié.
3. **Solution retenue** : `@import @memory/MEMORY.md` dans le CLAUDE.md VERSIONNÉ. Path résolu relativement au CLAUDE.md (verbatim doc), donc chaque repo charge SA mémoire. Zéro setup machine, zéro settings global, scoping par-repo natif préservé. Cf [[decision-memoire-dans-le-repo]].
4. Leçon de cadrage : valider une décision d'archi sur le cas RÉEL (multi-projets ici), pas sur le cas simplifié de la tâche courante.

Référence vault : [[decision-memoire-dans-le-repo]] (à amender selon la solution retenue).
