---
titre: "ADR — La mémoire forge vit dans le repo (@import CLAUDE.md)"
resume: "Décision actée 2026-05-27 : la mémoire de claude-forge est versionnée dans <repo>/memory/ et chargée via une ligne @memory/MEMORY.md dans le CLAUDE.md versionné (path résolu relativement au CLAUDE.md). Chaque repo charge SA mémoire, zéro setup machine, zéro settings global. claude-forge devient 100% self-contained."
aliases:
  - "memoire dans le repo"
  - "decision memoire portable"
  - "import memoire claudemd"
  - "memoire versionnee forge"
  - "adr memoire portable"
  - "memoire suit le clone"
type: decision
statut: accepte
derniere-maj: 2026-05-27
auteur: claude
tags:
  - "#type/decision"
  - "#projet/claude-forge"
  - "#sujet/memoire"
---

# ADR — La mémoire forge vit dans le repo

> Statut : ACCEPTÉ — 2026-05-27. Remplace l'ADR en attente [[adr-memoire-hors-repo-non-portable]].

## Contexte

claude-forge se veut un dossier auto-suffisant clonable sur n'importe quelle machine (`git clone` + `cd claude-forge && claude`). Tout suit le clone : agents, skills, hooks, vault, MCP. **Sauf la mémoire** — qui vivait dans `~/.claude/projects/<repo-encoded>/memory/`, hors de l'arbre git, donc non versionnée et perdue sur une nouvelle machine. Dernière faille de portabilité.

Workflow cible : Raphael bosse le matin sur PC boulot (écrit feedbacks via /done, commit, push), le soir sur PC perso il pull et retrouve toute la mémoire, continue, push. Une seule source de vérité, suivie par git, identique sur toutes les machines. **Contrainte multi-repos** : Raphael a plusieurs repos (claude-forge, neo_ia, ia_back, neoteem-brain, neofront), chacun doit garder SA mémoire — pas de fusion.

## Faits architecturaux décisifs (doc Anthropic, vérifiés via claude-code-guide)

1. **Scoping par défaut déjà par-repo** : sans config, chaque repo a son `~/.claude/projects/<encoded-git-root>/memory/` (dérivé du chemin git). Confirmé empiriquement (6 repos distincts). La fusion n'apparaît QUE si on force un chemin fixe.
2. **`autoMemoryDirectory`** (user-scope) accepte un chemin STATIQUE absolu/`~`. Pas d'expansion de variable (`${CLAUDE_PROJECT_DIR}` non supporté). Donc en multi-repos, il fusionnerait tout. Project-scope refusé (sécu). **Écarté.**
3. **`@import` dans CLAUDE.md** : `CLAUDE.md` peut importer un fichier via `@path`. Verbatim doc : *"Relative paths resolve relative to the file containing the import, not the working directory."* Donc `@memory/MEMORY.md` dans `<repo>/CLAUDE.md` charge `<repo>/memory/MEMORY.md`. CLAUDE.md versionné et CLAUDE.local.md traités identiquement. Charge le fichier ENTIER (pas de cap 200L/25Ko). Récursivité = uniquement `@imports` explicites (les liens markdown `[x](y.md)` ne sont PAS suivis → l'index charge seul, feedbacks à la demande).

## Options envisagées

1. **Statu quo** — mémoire hors repo. Rejeté : perte au changement de machine.
2. **`autoMemoryDirectory` absolu** — global, fusionne tous les repos. Rejeté : casse le multi-projets ([[automemorydirectory-absolu-casse-multiprojet]]).
3. **`autoMemoryDirectory` avec variable projet** — non supporté par la doc. Rejeté.
4. **Symlink/junction par repo** — non documenté, Windows risqué, setup par machine ET par repo. Rejeté.
5. **Script de sync git** — divergence silencieuse (2 sources de vérité). Rejeté.
6. **`@import @memory/MEMORY.md` dans CLAUDE.md versionné** (RETENU).

## Décision

- Mémoire versionnée dans **`<repo>/memory/`** (top-niveau, symétrique avec `vault/`).
- **Lecture** : ligne `@memory/MEMORY.md` dans le **CLAUDE.md versionné**. Path résolu relativement au CLAUDE.md → chaque repo charge SA mémoire. Aucun setup machine, aucun settings global, aucun classifier.
- **Écriture** : /done écrit les feedbacks dans `<repo>/memory/` (chemin dérivé de `git rev-parse --show-toplevel`). Lecture et écriture pointent la MÊME cible — sinon split-brain.
- `/recap` et `session-reminder.py` alignés sur `<repo>/memory/`.

## Conséquences

- claude-forge devient 100% self-contained et portable cross-machine. Le mécanisme se généralise à tout repo (ajouter `@memory/MEMORY.md` à son CLAUDE.md).
- **Aucun setup par machine** : CLAUDE.md suit le clone, l'import est actif d'office.
- **Friction unique** : à la 1re session après clone, Claude Code affiche un dialogue d'approbation des imports. Si décliné, imports désactivés silencieusement (pas de message d'erreur ensuite). Documenté dans `install-forge` + CLAUDE.md.
- **Coût contexte** : `@import` charge MEMORY.md entier (~34 Ko) sans cap (l'auto-memory cappait à 25 Ko). Renforce la discipline "MEMORY.md = index minimal < 200 lignes, détails dans topic files" (déjà dans /done).
- Mémoire versionnée → historique git, auditabilité, reproductibilité.
- **Confidentialité** : `memory/` non-confidentiel par principe. `.gitignore` réserve `memory/private/` + `memory/*-private.md`. Audit pré-migration : 1 secret prod trouvé + redacté (cf [[todo-rotation-password-postgres-prod]]).

## Déclencheur de réactivation

- Si Anthropic ajoute l'expansion de variable dans `autoMemoryDirectory` → réévaluer (permettrait l'auto-memory native scopée par repo).
- Si MEMORY.md dépasse une taille critique en contexte → envisager indexation MCP (`search_memory`) ou découpage.

## Appels

- [[adr-memoire-hors-repo-non-portable]] — l'ADR en attente que cette décision remplace
- [[automemorydirectory-absolu-casse-multiprojet]] — pourquoi autoMemoryDirectory absolu est écarté
- [[todo-rotation-password-postgres-prod]] — secret prod trouvé pendant l'audit confidentialité
- [[pattern-vault-llm-karpathy]] — le vault était déjà portable, la mémoire le devient
