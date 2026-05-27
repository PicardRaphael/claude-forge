---
titre: "ADR en attente — la mémoire forge vit hors du repo (non portable)"
resume: "Constat découvert en session A1 (27 mai 2026) : les fichiers mémoire (feedback_*, MEMORY.md) vivent dans ~/.claude/projects/<repo-encoded>/memory/, hors du repo git claude-forge. Donc non versionnés, non portables vers un autre PC. Décision de migration reportée à une session dédiée."
aliases:
  - "memoire hors repo"
  - "memoire non portable"
  - "adr memoire dans le repo"
  - "versionner la memoire forge"
  - "migration memoire pc perso"
derniere-maj: 2026-05-27
auteur: claude
type: decision
statut: en-attente
tags:
  - "#type/decision"
  - "#projet/claude-forge"
  - "#sujet/memoire"
---

# ADR en attente — la mémoire forge vit hors du repo (non portable)

> Statut : EN ATTENTE (pas tranchée). Décision de migration reportée à une session dédiée pour ne pas mélanger une décision d'architecture avec une feature (A1).

## Contexte

Découvert en session A1 (27 mai 2026, MCP search_sessions). Au moment de committer un `chore(memory)`, constat : le fichier mémoire durci (`feedback_mcp_alias_ambigu_chemin_exact.md`) ne fait PAS partie du repo git `Documents/claude-forge`.

Chemin réel de la mémoire : `~/.claude/projects/C--Users-raphael-picard-neote-Documents-claude-forge/memory/`. C'est l'auto-memory du harness Claude Code, rangée par projet encodé sous le home utilisateur, **hors de l'arbre du repo**.

## Conséquence

- La mémoire (feedback_*, reference_*, user_*, project_*, MEMORY.md) n'est **pas versionnée** dans le repo.
- Elle n'est **pas portable** : sur un autre PC (PC perso, autre machine), elle ne suit pas le `git clone`. Tout le compounding relationnel (74 feedbacks indexés dans MEMORY.md) serait perdu.
- Le vault forge-brain, lui, EST dans le repo (`vault/claude-forge/`) donc portable. Asymétrie : savoir technique portable, mémoire relationnelle non.

## Options (à évaluer en session dédiée)

1. **Statu quo** — mémoire reste dans `~/.claude/`. Simple, mais perte au changement de machine.
2. **Symlink / copie versionnée** — `vault/claude-forge/memory/` dans le repo, symlink depuis `~/.claude/`. Versionne mais risque de divergence et le harness écrit dans le chemin natif.
3. **Script de sync** — backup périodique `~/.claude/.../memory/` → `vault/` (ou inverse au clone). Hook SessionStart / Task Scheduler.
4. **Migration vers le vault** — déplacer les feedbacks dans `vault/Knowledge/` (déjà la frontière mémoire↔vault documentée). Mais le harness recharge MEMORY.md depuis le chemin natif, pas depuis le vault.

Chaque option a un coût et un risque de divergence harness vs repo. À trancher avec advisor + devils-advocate.

## Déclencheur de réactivation

- **Migration vers un PC perso** ou changement de machine de travail.
- **Besoin explicite de versionner / partager la mémoire** (ex: sauvegarde, audit, reproductibilité).
- Si la mémoire dépasse une taille critique et qu'on veut un historique git de son évolution.

## Pourquoi reporté

Décision d'architecture (où vit la mémoire, comment la sync) ≠ feature A1 (search_sessions). Ne pas mélanger les concerns dans une session ni dans des commits. Cf doctrine commits séparés par concern.

## Appels

- [[mcp-alias-ambigu-chemin-exact]] — feedback mémoire durci la même session (le bug qui a révélé le constat)
- [[pattern-vault-llm-karpathy]] — le vault, lui, est portable car dans le repo


## Mise à jour — test de validation (27 mai 2026)

L'option 4 (migration via @import dans CLAUDE.md versionné) a été IMPLÉMENTÉE et TESTÉE. L'@import charge bien la mémoire portable du repo. **Mais le risque de divergence redouté dans les options 2 et 3 s'est matérialisé sur l'option 4 aussi** : l'auto-memory native (`~/.claude/projects/`) reste injectée en parallèle, tronquée et divergente (231 L repo vs 229 L native). L'@import ajoute une source, ne remplace pas la native. **Reste à faire pour clore l'ADR** : désactiver/vider l'auto-memory native afin d'obtenir la single source. Cf [[import-ajoute-pas-remplace-automemory]] + résultat détaillé dans [[architecture-decision-memoire-portable-import]].