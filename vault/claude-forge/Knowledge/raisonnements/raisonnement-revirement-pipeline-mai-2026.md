---
titre: "Revirement pipeline mai 2026 — de retire architect à pipeline conditionnel"
aliases:
  - "revirement pipeline mai 2026"
  - "raisonnement boris adapte"
  - "pourquoi pas retire architect"
  - "advisor da pipeline neoteem"
  - "decision pipeline conditionnel"
tags:
  - "#type/raisonnement"
  - "#domaine/claude-code"
  - "#technique/agents"
resume: "Capture du raisonnement multi-étapes — la session a commencé sur retire architect (frustration 4h/feature), DA a démoli, on a pivoté vers rends architect rapide puis pipeline conditionnel. Précieux pour comprendre POURQUOI"
derniere-maj: 2026-05-22
auteur: claude
type: raisonnement
sources:
  - "Session 2026-05-21 Raphael frustration 4h"
  - "Advisor Anthropic 3 appels"
  - "Devil's advocate critique-2026-05-21-refonte-pipeline-boris-pattern.md"
  - "Project-auditor neo_ia + ia_back"
  - "Recherche web Boris/Willison/Anthropic 2026"
---

# Revirement pipeline mai 2026 — chemin de raisonnement

## Question de départ

Raphael (Lead IA, 22h+) : "4h pour faire une feature. Je ne prends plus aucun plaisir à développer. Faites ce que Boris fait."

## Étape 1 — Hypothèse initiale (FAUSSE) : "retire architect"

**Logique** : Boris n'utilise pas d'agent architect séparé, il utilise Plan Mode natif. Donc retire architect-guard, bascule en Plan Mode.

**Design proposé** :
- Retirer `architect-guard.py`
- Plan Mode natif CC pour features S/M
- Conserver `tdd-guard` intouché
- Code-reviewer sur PR/commit uniquement
- Ajouter classifier PreToolUse qui force Plan Mode si > 1 fichier OR > 50 LOC OR fichier critique

## Étape 2 — Devil's Advocate démonte (4 BLOCKING)

Le DA a sauvé la session. Critique stockée dans `Knowledge/critiques/critique-2026-05-21-refonte-pipeline-boris-pattern.md`.

**Bloquants** :

1. **Plan Mode CC ne laisse pas de trace persistante vérifiable par hook** → retombe en advisory 80% (pattern documenté défaillant 3 fois)
2. **Classifier path+LOC = 30-40% faux-négatifs** : 30 LOC dans `tool_selector.py` casse OATS, 1 ligne change ordre middlewares = bug auth, rename méthode = propage silencieusement
3. **Chaîne marker cassée sans remplacement** : commit-guard lit `.architect-marker`, le retirer brise toute la chaîne aval
4. **Liste fichiers critiques incomplète** : manque agents/, packages/shared/, *Router*, *Selector*, *Dispatcher*, lockfiles, conftest

**Et argument doctrinal massif** : Raphael lui-même (Lead IA) a skippé les rules "OBLIGATOIRE" le 7 mai. Si le Lead skip, le junior skip plus. Boris est solo + expert. Collègues Neoteem ne sont ni l'un ni l'autre.

## Étape 3 — Pivot 1 : "rends architect rapide" (PARTIEL)

Diagnostic alternatif du DA : **le vrai coût n'est pas l'existence d'architect, c'est sa lenteur sur scope petit**.

**Design pivot 1** :
- Garder architect-first (filet collègues conservé)
- Ajouter routing taille S/M/L en tête du prompt architect
- Mode mini-plan S : 5 lignes en <60s
- Mode plan complet pour M/L comme avant

**Appliqué** sur architect.md neo_ia + ia_back.

## Étape 4 — Frustration utilisateur persiste

Raphael : "architect met encore du temps car il lit beaucoup le repo ia_back, peut-être faut changer ça".

**Découverte** : prompt architect disait `Source de vérité externe = ia_back/ (lecture seule, libre)`. L'agent se sentait autorisé à fouiller ia_back systématiquement.

**Fix** : changer en `repos voisins NE PAS LIRE PAR DÉFAUT, autorisation explicite requise`.

## Étape 5 — Vraie cause : test-writer

Raphael : "ce n'est pas l'architect, c'est test-writer qui met sa vie".

**Analyse** :
- Test-writer 2 passes (RED + REFACTOR) sur opus xhigh = 12-16 min
- 6 tests pour 1 comportement (cache_helpers — takeover/known/unknown/empty/no-name/empirical)
- Effort xhigh sur écriture de tests = surcalibré

**Pivot 2 design** :
- Effort xhigh → high
- MAX 3 tests par comportement (pattern Willison "red-green TDD, it's like five tokens")
- Phase REFACTOR SUPPRIMÉE (fusionnée dans code-reviewer)

## Étape 6 — Audit global : pipeline trop dense

Project-auditor cross-repo découvre :
- ia_back : 8 agents enchaînés systématiquement (api-designer → architect → test-writer → dev → test-writer refactor → code-reviewer → validator → perf → security)
- 8 agents en effort xhigh sans raison (sql-optimizer, db-inspector, validator, etc.)
- tdd-guard bloque `*.config.ts`, `*.md`, renames purs

**Pivot 3 — décision finale** : pipeline conditionnel, pas systématique.

```
| Gate | Quand DÉCLENCHER |
| security-auditor | SI auth/PII/secrets/file upload |
| performance-engineer | SI SQL 3+ joins OR table > 100k rows |
| validator | UNIQUEMENT migrations PG→TS |
| outcomes-grader | SI rubric.md présent |
```

CRUD simple = 5 étapes au lieu de 8.

## Leçons du revirement

### 1. Ne JAMAIS faire le premier design proposé sans DA

Si je n'avais pas appelé devil's advocate, j'aurais retiré architect-guard, brisé la chaîne marker, et créé 3-4 incidents collègues dans les 30 jours.

**Règle** : décisions doctrinales cross-repo → advisor + DA OBLIGATOIRES avant code.

### 2. Le bon problème n'est presque jamais le premier identifié

Raphael a dit successivement :
- "architect met trop de temps" → vrai mais pas la cause principale
- "test-writer met sa vie" → vrai, contribue
- "trop de tests par feature" → vrai cause root
- "8 agents enchaînés c'est trop" → vrai cause root #2

**Règle** : creuser au-delà du symptôme initial. Audit auditor cross-repo a révélé ce que ni Raphael ni moi ne voyait.

### 3. Boris solo ≠ Neoteem équipe

Tentation : copier Boris à 100%. Réalité : Boris solo + expert + accepte le risque cognitif. Neoteem équipe + juniors + filets nécessaires.

**Adaptation correcte** :
- Esprit Boris (rapidité, pas de cérémonie inutile) ✅
- Sécurité collègues (TDD, code-reviewer, gates conditionnels) ✅
- Différence fast-lane vs strict en mode strict pour tous (asymétrie = piège) ✅

### 4. Frustration utilisateur = signal technique légitime

Raphael "je ne prends plus de plaisir à développer" = ce n'était pas du whining. C'était un symptôme de pipeline cassé. Pris au sérieux → diagnostic révèle effectivement 50% de gaspillage récupérable.

**Règle** : "ça met trop de temps" ≠ "le dev est impatient". Toujours mesurer.

### 5. Mesurer avant d'optimiser

J'ai estimé "fusion hooks PreToolUse = 30-100s/feature gain". Mesure terrain : 136ms × 5 hooks = 680ms/Write = 15-25s/feature. **3-7× moins que l'estimation**.

→ J'ai annulé la fusion (risque élevé pour gain modeste). Pattern `measure-before-optimize-tests` validé une fois de plus.

## Décisions finales appliquées (commit f6d89e0 neo_ia + bc109aa ia_back, 22 mai 2026)

Voir `[[pipeline-boris-adapte-neoteem]]` pour la recette complète.

## Liens

- [[pipeline-boris-adapte-neoteem]] — la recette finale
- [[critique-2026-05-21-refonte-pipeline-boris-pattern]] — le DA qui a sauvé la session
- [[erreur-pipeline-trop-long-frustration]] — l'erreur de départ
- [[pattern-architect-first-pipeline]] — pattern précédent compatible
- [[boris-workflow-2026-may]] — Boris pur (référence)
- [[advisor-da-before-proposing]] (mémoire) — confirmé une fois de plus
- [[measure-before-optimize-tests]] (mémoire) — confirmé sur fusion hooks
