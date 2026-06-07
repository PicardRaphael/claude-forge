---
titre: "@import AJOUTE une source mémoire, il ne REMPLACE pas l'auto-memory native"
resume: "Fait non anticipé (test 27 mai 2026) : ajouter @memory/MEMORY.md dans CLAUDE.md versionné charge bien la mémoire du repo (portabilité git acquise), mais l'auto-memory native ~/.claude/projects/<encoded>/memory/ reste injectée en parallèle — tronquée et divergente. L'orthogonalité a un revers : la source qu'on voulait remplacer reste active. Single source non atteinte sans désactiver/vider la native."
aliases:
  - "import ajoute pas remplace automemory"
  - "import double source memoire"
  - "auto-memory native persiste malgre import"
  - "divergence memoire claude code deux sources"
  - "single source memoire non atteinte import"
type: erreur
derniere-maj: 2026-06-07
auteur: claude
tags:
  - "#type/erreur"
  - "#domaine/claude-code"
  - "#domaine/memoire"
---
# @import ajoute une source, il ne remplace pas la native

## Le fait empirique (test 27 mai 2026)

Mettre `@memory/MEMORY.md` dans le CLAUDE.md versionné devait donner une mémoire portable par git ET une source unique. Le test de chargement a donné deux temps :

- L'`@import` fonctionne : `@memory/MEMORY.md` charge bien `<repo>/memory/MEMORY.md`, étiqueté « checked into the codebase ». La portabilité par git est acquise.
- Fait non anticipé : l'auto-memory native n'a pas disparu. Le harness injecte toujours `~/.claude/projects/<encoded>/memory/MEMORY.md` en parallèle — tronquée (« Only part of it was loaded ») et divergente (items de tête manquants).

## L'insight

L'orthogonalité (préférer un mécanisme qui s'ajoute au défaut plutôt qu'un réglage qui l'écrase, cf [[automemorydirectory-absolu-casse-multiprojet]]) évite de casser le scoping multi-repos, mais a un revers : la source qu'on voulait remplacer reste active. La « single source » visée n'est donc pas atteinte par le seul `@import` — la divergence réapparaît, sans script de sync. L'étape manquante = désactiver ou vider l'auto-memory native.

## Conséquence pratique

Sur un repo qui adopte `@import` pour sa mémoire, ne pas considérer la native comme remplacée : soit on vit avec deux sources (et on accepte la divergence), soit on vide/désactive la native pour atteindre la source unique. Le choix relève de l'ADR mémoire du repo.

## Liens

- [[architecture-decision-memoire-portable-import]] — la chaîne de raisonnement (l'insight orthogonalité y est posé puis nuancé)
- [[adr-memoire-hors-repo-non-portable]] — l'ADR connexe sur la portabilité mémoire
- [[automemorydirectory-absolu-casse-multiprojet]] — sa note jumelle (l'autre piste mémoire portable)
