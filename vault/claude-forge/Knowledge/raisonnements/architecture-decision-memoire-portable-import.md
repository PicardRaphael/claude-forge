---
titre: "architecture-decision — mémoire portable cross-machine sans casser le multi-repos"
resume: "Chaîne de raisonnement qui a mené du choix autoMemoryDirectory (cassé en multi-projets) vers @import dans CLAUDE.md versionné. Le pivot : un mécanisme validé sur un repo isolé peut être faux sur le workflow réel multi-repos."
aliases:
  - "raisonnement memoire portable"
  - "choix mecanisme memoire repo"
  - "reasoning portable memory claude code"
  - "memory mechanism decision chain"
  - "automemorydirectory vs import"
  - "memoire cross-machine multi-repos"
type: raisonnement
domaine: claude-forge
derniere-maj: 2026-05-27
auteur: claude
tags:
  - "#type/raisonnement"
  - "#domaine/claude-code"
---
## Problème

Rendre la mémoire de claude-forge portable cross-machine (suivre le `git clone`) SANS fusionner les mémoires des autres repos (neo_ia, ia_back, neoteem-brain). La mémoire vit par défaut hors repo (`~/.claude/projects/<encoded>/memory/`), donc perdue au changement de machine.

## Contexte

Workflow multi-repos. Chaque repo doit garder SA mémoire versionnée dans SON `memory/`. Contrainte : pas de modif du settings global si évitable (hard-block classifier), pas de setup lourd par machine.

## Chaîne de raisonnement

1. **Première approche** : `autoMemoryDirectory` (user-scope) pointant vers `<repo>/memory/` en chemin absolu. Validé car satisfait le workflow cross-machine de claude-forge isolé. Confirmé par la doc comme seule voie où le chargement NATIF lit depuis le repo.
2. **Faille détectée (par Raphael, pas par moi)** : `autoMemoryDirectory` est GLOBAL. En chemin absolu, il s'applique à TOUS les repos → fusion de toutes les mémoires dans `claude-forge/memory/`. Validé sur le cas isolé, cassé sur le cas réel multi-projets.
3. **Recherche d'une variable dynamique** : `autoMemoryDirectory: "${CLAUDE_PROJECT_DIR}/memory"` résoudrait par-repo. Vérifié empiriquement (doc + env shell) : NON supporté (valeur = chemin statique, pas d'expansion). Piste morte.
4. **Fait empirique clé** : le scoping par-repo est DÉJÀ le défaut (chaque repo a son dossier encodé). Le problème n'existe QUE si on force un chemin fixe. Donc ne RIEN forcer côté auto-memory native, et chercher un mécanisme orthogonal.
5. **Pivot** : le mécanisme `@import` de CLAUDE.md. Une ligne `@memory/MEMORY.md` dans CLAUDE.md, path résolu relativement au fichier (verbatim doc). Chaque repo charge SA mémoire.
6. **Affinage (advisor)** : mettre l'`@import` dans le CLAUDE.md VERSIONNÉ (pas CLAUDE.local.md). CLAUDE.md suit le clone → zéro setup par machine. Variante dominante.
7. **Validation** : doc confirme les 2 conditions (import dans CLAUDE.md versionné OK + path relatif au fichier). Mode de défaillance favorable (visible si KO, vs sync silencieux).

## Insight clé

**Un mécanisme validé sur le cas simplifié de la tâche (un seul repo) peut être faux sur le cas réel (multi-repos).** La question discriminante n'était pas "est-ce que ça marche pour claude-forge" mais "est-ce que ça marche quand il y a 5 repos". Le second insight : quand le comportement par défaut fait déjà ce qu'on veut (scoping par-repo), ne pas le surcharger — chercher un mécanisme ORTHOGONAL (`@import`) qui s'ajoute sans casser le défaut, plutôt qu'un réglage global qui l'écrase.

## Résultat

Décision actée : `@memory/MEMORY.md` dans CLAUDE.md versionné, mémoire dans `<repo>/memory/`, écriture /done sur la même cible. Zéro setup machine, zéro settings global, portable par git. ADR [[decision-memoire-dans-le-repo]]. Reste à valider par test de chargement (redémarrage session).

## Réutilisation

Utiliser ce raisonnement quand : on choisit un mécanisme de configuration "global" (settings user-scope, variable d'env, chemin fixe) pour résoudre un besoin observé sur UN projet, alors que l'environnement réel est multi-projets. Vérifier l'impact sur les AUTRES projets avant de valider. Et : préférer un mécanisme orthogonal qui s'ajoute au défaut plutôt qu'un réglage qui l'écrase.

## Liens

- [[decision-memoire-dans-le-repo]]
- [[automemorydirectory-absolu-casse-multiprojet]]
- [[mcp-paths-relatifs-portabilite]]


## Résultat du test de validation (27 mai 2026)

Le test de chargement annoncé ("reste à valider par test — redémarrage session") a été exécuté. Résultat en deux temps :

- ✅ **L'`@import` fonctionne** : `@memory/MEMORY.md` (CLAUDE.md L100) charge bien `<repo>/memory/MEMORY.md` (231 L), étiqueté *"checked into the codebase"* dans le contexte injecté. La portabilité par git est acquise.
- ⚠️ **Fait non anticipé par la chaîne de raisonnement** : l'auto-memory NATIVE n'a pas disparu. Le harness injecte TOUJOURS `~/.claude/projects/<encoded>/memory/MEMORY.md` en parallèle (229 L, **tronquée** — `Only part of it was loaded` — et **divergente** : 2 items de tête manquants). L'`@import` AJOUTE une source, il ne REMPLACE pas la native.

**Conséquence sur l'insight** : "préférer un mécanisme orthogonal qui s'ajoute au défaut plutôt qu'un réglage qui l'écrase" était juste pour éviter de casser le scoping multi-repos — mais l'orthogonalité a un revers : la source qu'on voulait remplacer reste active. La single source visée par [[decision-memoire-dans-le-repo]] (option "script de sync rejetée pour éviter la divergence à 2 sources") n'est PAS atteinte : la divergence réapparaît, sans script. Étape manquante = désactiver/vider l'auto-memory native. Cf [[import-ajoute-pas-remplace-automemory]].