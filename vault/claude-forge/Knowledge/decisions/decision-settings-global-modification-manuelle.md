---
titre: "ADR — Modifications du settings global = manuelles via diff fourni"
resume: "Décision actée 2026-05-27 : toute modification de ~/.claude/settings.json (hooks, permissions, env) se fait manuellement par Raphael à partir d'un diff fourni par l'agent — jamais automatiquement. Cohérent avec le hard-block classifier Anthropic et la doctrine humain-dans-la-boucle."
aliases:
  - "settings global manuel"
  - "modification settings.json manuelle"
  - "hard-block classifier settings"
  - "diff settings fourni"
  - "humain dans la boucle settings"
type: decision
statut: accepte
derniere-maj: 2026-05-27
auteur: claude
tags:
  - "#type/decision"
  - "#projet/claude-forge"
  - "#sujet/securite"
---

# ADR — Modifications du settings global = manuelles via diff fourni

> Statut : ACCEPTÉ — 2026-05-27.

## Contexte

`~/.claude/settings.json` (global, user-scope) est sous **hard-block classifier Anthropic** (self-modification protection) : un agent ne peut pas l'éditer directement. Certaines features l'exigent (hooks globaux, permissions, variables d'env, certains réglages user-scope refusés en project-scope pour raison sécu).

## Décision

L'agent **fournit un diff précis** sous 3 formes (diff brut + fichier complet attendu + commandes de vérification), Raphael **applique à la main**. Jamais de bypass du classifier.

## Pourquoi

- Le hard-block existe pour une raison légitime (un repo cloné ne doit pas pouvoir rediriger des écritures sensibles).
- Bypasser créerait un précédent durable et trahirait la doctrine "humain dans la boucle by design" — un point de différenciation forge identifié.
- Coût marginal : 30 secondes de copier-coller vs un précédent de contournement.

## Conséquences

- Les features nécessitant le settings global ne sont jamais "auto-installées" — toujours présentées comme diff à valider.
- Note : la mémoire portable de forge ([[decision-memoire-dans-le-repo]]) a justement été conçue pour ÉVITER toute modif du settings global (via `@import` dans CLAUDE.md versionné). Cette ADR reste la règle générale pour les cas où le settings global est réellement requis.

## Appels

- [[decision-memoire-dans-le-repo]] — cas où on a délibérément évité le settings global
- [[delegate-guard-env-var-blocked]] — autre cas de protection self-modification
