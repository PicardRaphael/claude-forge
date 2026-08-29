---
titre: "Raisonnement — refonte du second cerveau forge"
resume: "Pivot 2026-08-29 : conserver l'autorité vault et la mémoire repo portable, mais passer à un rappel mesuré, une rétention à TTL et des capacités minimales."
aliases:
  - "refonte second cerveau forge"
  - "pivot memoire forge 2026"
  - "contrat rappel retention oubli"
  - "optimisation claude forge aout 2026"
type: knowledge
statut: active
derniere-maj: 2026-08-29
auteur: Codex
tags:
  - "#type/raisonnement"
  - "#projet/claude-forge"
  - "#domaine/memoire"
---

# Raisonnement — refonte du second cerveau forge

## Problème observé

Le système superpose mémoire repo, mémoire native, agent-memory, règles eager et hooks de rappel. Les tests structurels passent, mais le rappel réel produit des faux positifs et manque des projets nommés exactement. Les fichiers temporaires n'ont pas de TTL appliqué et le tier-2 reste indexé par le hook.

## Décisions

- Le vault forge-brain reste l'autorité pour profil, doctrine, projets stables et décisions.
- `memory/MEMORY.md` reste temporairement importé conformément à [[decision-memoire-dans-le-repo]] ; son retrait exige une réouverture formelle après evals.
- Le rappel automatique ne considère que les entrées actives de l'index, exclut tier-2, archives et mémoires expirées, et n'injecte aucun texte libre impératif.
- Les `project_*.md` portent `status` et `expires`; une expiration les rend froids jusqu'à revue.
- La mémoire des agents devient opt-in selon le rôle, jamais obligatoire par défaut.
- Les hooks mesurent des propriétés déterministes; ils ne décident pas sémantiquement quoi apprendre.
- Les règles globales sont réservées aux invariants; les workflows optionnels vivent dans des skills.
- Les chercheurs web restent read-only. Les mutations vault reviennent à la session principale avec permissions explicites.
- Les wildcards MCP mutateurs et permissions shell universelles sont supprimés.
- Claude et Codex partagent politiques et corpus de tests, mais gardent des adaptateurs runtime distincts.

## Mesures de sortie

Baseline de 30 à 50 prompts : precision@3, projet exact rappelé, faux rappels, rappels périmés, latence, contexte eager, prompts de permission et bypass adverses. Chaque vague conserve un rollback vérifié.

## Propagation

Surfaces à réaligner : AGENTS.md, CLAUDE.md, règles, creator skills, agents, hooks Claude/Codex, mémoire repo, agent-memory, canoniques `comment-ecrire-claudemd`, `comment-creer-skill`, `comment-creer-agent` et `comment-creer-hook`.
