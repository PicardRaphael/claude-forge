---
titre: "Pipeline Boris adapté Neoteem — recette feature 15-20 min"
aliases:
  - "pipeline boris neoteem"
  - "pipeline agentic feature rapide"
  - "recette pipeline 2026"
  - "feature 15 minutes pattern"
  - "boris adapted pattern"
  - "pipeline conditionnel agents"
tags:
  - "#type/technique"
  - "#technique/agents"
  - "#domaine/claude-code"
resume: "Recette pipeline agentic Neoteem mai 2026 — feature M en 15-20 min au lieu de 30-45. Routing taille S/M/L architect, max 3 tests par comportement, pas de REFACTOR, gates conditionnels, effort high (pas xhigh) sauf jugement"
derniere-maj: 2026-05-22
auteur: claude
type: technique
domaine: claude-code
sources:
  - "Session 2026-05-21 frustration utilisateur 4h/feature"
  - "Boris Cherny Pragmatic Engineer 2026"
  - "Simon Willison Pragmatic Summit mars 2026"
  - "Anthropic Opus 4.7 effort recommendations"
  - "Audit project-auditor cross-repo ia_back + neo_ia"
---

# Pipeline Boris adapté Neoteem — recette à appliquer sur tout nouveau repo

## Contexte du nom

"Boris adapté" parce que Boris Cherny est solo + ultra-expert. Neoteem est multi-devs juniors/seniors. On garde l'esprit Boris (rapidité, pas de cérémonie inutile) mais on conserve les filets (TDD, code-reviewer) pour l'équipe.

## Symptômes d'alarme — si tu vois ça, tu refais l'erreur du 21 mai

- Une feature simple prend > 30 min
- Architect tourne 5+ min même sur un rename
- Test-writer écrit 6 tests sur un seul comportement
- Pipeline enchaîne 7-8 agents sur une feature CRUD
- Tous les agents en `effort: xhigh`
- Phase "test-writer refactor" systématique APRÈS dev green
- L'utilisateur dit "je ne prends plus de plaisir à développer"

→ Si 2+ de ces symptômes, tu as recréé le piège du 21 mai 2026.

## La recette — 6 règles non négociables

### 1. Architect : routing taille S/M/L AVANT toute lecture

Dans le prompt de l'agent architect, en TÊTE :

```markdown
## ⚡ ROUTING TAILLE — DÉCIDE EN 5 SECONDES AVANT TOUT

| Taille | Critères | Format sortie |
|--------|----------|---------------|
| S | 1 fichier OU < 30 LOC, pas critique | mini-plan 5 lignes en <60s |
| M | 2-5 fichiers, 1 domaine, < 150 LOC | plan complet |
| L | > 5 fichiers OU cross-domaine OU critique | plan approfondi + impact |

Fichiers critiques (jamais S) : `.env*`, configs build, migrations, schemas API, fichiers `*Router*`, `*Selector*`, `*Dispatcher*`, `main.py`/`main.ts`, conftest.py
```

**Format mini-plan S** :
```
TAILLE: S
FICHIERS: <chemin>
TESTS: <UNIT OUI + 1 cas discriminant> | BYPASS si typo/rename/config/hotfix<5L/doc
RISQUE: LOW
GO.
```

**Gain** : architect 5 min → 30-60 sec sur 70% des features.

### 2. Architect ne lit PAS les repos voisins par défaut

Même si techniquement accessibles. Demande autorisation explicite.

```markdown
**Repos voisins** — NE PAS LIRE PAR DÉFAUT. Lecture UNIQUEMENT si user le demande explicitement OU si tâche mentionne fichier précis du repo voisin.
```

**Gain** : économise les Glob/Grep parasites cross-repo.

### 3. Test-writer : MAX 3 tests par comportement

Pattern Willison/Boris 2026 — "red-green TDD, it's like five tokens, and that works".

```markdown
## RÈGLE DE DENSITÉ
MAX 3 tests par comportement :
1. Cas nominal (happy path)
2. Cas limite discriminant (vide/null/erreur principale)
3. Edge case unique le plus risqué (optionnel)

Anti-pattern : 6 tests qui testent le même comportement sous 6 angles.
```

**Gain** : test-writer 8 min → 4-5 min par comportement.

### 4. Phase REFACTOR test-writer SUPPRIMÉE — fusionnée dans code-reviewer

C'est la double-passe qui coûtait 6-8 min systématiques. Code-reviewer reprend la responsabilité en LIGHT (1-3 edge cases max, pas de coverage forcée).

**Test-writer** : seulement phase RED (avant dev).
**Code-reviewer** : ajoute section "Edge cases à ajouter" dans son rapport.
**Dev** : si validation, ajoute les 1-3 edge cases lui-même.

**Gain** : -6 à -8 min/feature.

### 5. Effort `high` PARTOUT sauf jugement profond

| Agent | Effort | Modèle |
|-------|--------|--------|
| architect | xhigh | opus |
| dev-lead (cross-app) | xhigh | opus |
| refactor-pg-function (raisonnement lourd) | xhigh | opus |
| **TOUS les autres** | **high** | sonnet ou opus selon rôle |

dev-* (exécution) → **sonnet high**
code-reviewer / security-* (review) → **opus high**
test-writer (génération) → **opus high**
analystes read-only → **opus high**

`xhigh` est diminishing returns au-delà du raisonnement profond (Anthropic, mai 2026).

**Gain** : -20-40% tokens et latence sur 80% des agents.

### 6. Pipeline conditionnel, pas systématique

**JAMAIS** "TOUJOURS tous les gates". Chaque gate a un critère.

```markdown
| Gate | Quand DÉCLENCHER |
|------|------------------|
| architect | TOUJOURS |
| test-writer red | TOUJOURS (sauf bypass typo/config/doc/hotfix<5L) |
| dev | TOUJOURS |
| code-reviewer | TOUJOURS (inclut edge cases — refactor SUPPRIMÉ) |
| security-auditor | SI auth/PII/secrets/file upload |
| performance-engineer | SI SQL 3+ joins OR endpoint table >100k rows |
| validator | UNIQUEMENT migrations critiques (PG→TS, refacto critique) |
| outcomes-grader | SI rubric.md présent dans le dossier feature |
```

**Séquence minimale CRUD simple** : `architect → test-writer red → dev → code-reviewer → commit` = 5 étapes au lieu de 8.

**Gain** : -15 à -30 min/feature simple.

## Skills agent : 3-4 max, pas 9

Skill `skills:` frontmatter d'un agent = TOUT injecté au boot. 9 skills = ~5-8k tokens parasites avant la première instruction.

Garder 3-4 skills CORE (vraiment réutilisées à chaque invocation). Les autres : référencer dans le body "charger skill X si Y".

## Gain cumulé mesuré (sessions 21-22 mai 2026)

| Feature | Avant | Après recette | Gain |
|---------|-------|---------------|------|
| Feature M neo_ia | 30-45 min | 12-18 min | **~50%** |
| Feature CRUD simple ia_back | 4 h | ~1 h 30 | **~60%** |
| Feature S (typo, rename, hotfix) | 15-20 min | 3-5 min | **~75%** |

## Application sur un NOUVEAU repo

Checklist pour démarrer un repo avec ce pattern :

- [ ] `architect.md` : section "ROUTING TAILLE" en tête, exemption repos voisins
- [ ] `test-writer.md` : règle "MAX 3 tests par comportement", pas de phase REFACTOR
- [ ] `code-reviewer.md` : section "Edge cases à ajouter" légère
- [ ] Tous les agents review/exécution : `effort: high` (sauf architect/lead xhigh)
- [ ] dev-* : `model: sonnet`, skills réduites à 3-4 core
- [ ] `quality-gates.md` : pipeline conditionnel selon scope
- [ ] `tdd-guard` : exclusions `*.config.*`, `*.d.ts`, `*.md`, fichiers build
- [ ] Mécanisme `.tdd-bypass` documenté pour features triviales

## Anti-patterns à NE PAS recréer

1. ❌ "Tous les agents en xhigh par sécurité" → diminishing returns, latence x2
2. ❌ "test-writer en 2 passes (red + refactor)" → double-tokenisation pour le même résultat
3. ❌ "Pipeline 8 agents systématique" → CRUD simple n'a pas besoin de security-auditor
4. ❌ "Architect xhigh même pour rename" → 5 min pour 5 secondes de travail réel
5. ❌ "Skills frontmatter = tout ce qui pourrait servir" → tokens parasites au boot
6. ❌ "Phase REFACTOR sécurité" → code-reviewer fait déjà ce travail

## Liens

- [[pattern-architect-first-pipeline]] — pattern précédent (markers + hooks), reste valide en complément
- [[boris-workflow-2026-may]] — version Boris pure (solo, parallélisation worktrees)
- [[raisonnement-revirement-pipeline-mai-2026]] — pourquoi on est passé d'advisory à conditionnel
- [[erreur-pipeline-trop-long-frustration]] — l'erreur déclencheur
- [[reference_boris_thariq_bestpractices]] — référence canonique mise à jour
- [[reference_opus47_best_practices]] — effort levels Opus 4.7
- [[erreur-marker-ttl-blocage-agents]] — leçon TTL précédente
