---
titre: "Erreur — Pipeline agentic Neoteem trop long (4h/feature, perte de plaisir)"
aliases:
  - "pipeline trop long"
  - "4h par feature erreur"
  - "frustration developpeur agentic"
  - "erreur sur-pipeline neoteem"
  - "trop de tests trop xhigh"
tags:
  - "#type/erreur"
  - "#projet/ia_back"
  - "#projet/neo_ia"
  - "#technique/agents"
resume: "Mai 2026 — pipeline agentic ia_back+neo_ia mettait 4h pour une feature CRUD. 6 sources de gaspillage cumulatives. Raphael Lead IA disait perdre le plaisir de développer. Signal d'alarme technique légitime"
derniere-maj: 2026-05-22
auteur: claude
type: erreur
projet: cross-repo
sources:
  - "Session 21 mai 2026 frustration utilisateur"
  - "Audit project-auditor cross-repo"
  - "DA critique-2026-05-21-refonte-pipeline-boris-pattern"
---
# Erreur — Pipeline agentic Neoteem trop long

## Symptôme déclencheur

21 mai 2026, ~22h. Raphael (Lead IA Neoteem) : **"4h pour faire une petite feature. Je ne prends plus aucun plaisir à développer."**

Le signal humain ("perte de plaisir") cache un signal technique légitime : le pipeline était objectivement cassé.

## Ce qui s'est passé — 6 sources de gaspillage cumulées

### 1. Architect xhigh même sur tâches triviales — 5 min systématiques

`architect.md` n'avait pas de routing taille. Sur un rename de variable, l'agent appliquait le full plan (analyse impact, contrats testables, découpage sous-agents, skills à charger) → 5 min pour 5 secondes de travail réel.

### 2. Architect lisait ia_back par défaut — Glob/Grep parasites

Le prompt disait `Source de vérité externe = ia_back/ (lecture seule, libre)`. L'agent se sentait autorisé à fouiller ia_back systématiquement, même quand inutile.

### 3. Test-writer en 2 passes (RED + REFACTOR) sur opus xhigh — 12-16 min

Chaque invocation = 5-8 min. La phase REFACTOR ajoutait des edge cases APRÈS dev green → mais code-reviewer faisait déjà ce travail. Double-tokenisation pour le même résultat.

### 4. Test-writer écrivait 6 tests par comportement — overshoot densité

Exemple constaté : `cache_helpers_extended.py` — 6 tests sur UN seul comportement (`current_message` dans `generate_cache_aware_instructions` : takeover/known/unknown/no-name/empty/empirical-Furlan). 2-3 tests bien choisis suffisaient.

Cause : pas de borne dans le prompt test-writer. L'agent maximisait par défaut.

### 5. Tous les agents en effort xhigh — diminishing returns

8 agents ia_back en xhigh sans raison (sql-optimizer, db-inspector, validator, performance-engineer, security-auditor, codebase-analyst, repo-functions-analyzer, api-designer). xhigh est diminishing returns au-delà du raisonnement profond (Anthropic, mai 2026).

Coût : ~20-40% tokens et latence supplémentaires sur 80% des invocations.

### 6. Pipeline systématique 8 agents même sur CRUD simple

Workflow ia_back forçait : `api-designer → architect → test-writer red → dev → test-writer refactor → code-reviewer → validator → performance-engineer → security-auditor`. 8 agents sur un endpoint simple sans auth, sans SQL complexe, sans PII.

Cause : rule `quality-gates.md` disait `TOUJOURS` au lieu de critères conditionnels.

## Pourquoi c'était une erreur

### Erreur de design

Chaque décision individuelle paraissait raisonnable :
- "xhigh pour avoir des plans de qualité" ✓
- "test-writer 2 passes pour couverture complète" ✓
- "8 agents pour ne rien oublier" ✓
- "architect peut lire ia_back parce que c'est utile" ✓

**Pris ensemble** : 4h pour ce qui devrait prendre 15 min.

### Effet d'accumulation invisible

Aucun seuil individuel n'était scandaleux. C'est l'**accumulation** qui tue. Personne ne disait "oh non, le test-writer prend 12 min" — ça paraissait normal. Personne ne disait "oh non, pourquoi 8 agents" — ça paraissait sécurisant.

**Leçon** : auditer le pipeline ENTIER de temps en temps, pas les agents individuellement.

### Signal humain ignoré trop longtemps

Raphael avait dit "c'est lent" plusieurs sessions avant. Le signal a été pris pour de l'impatience. C'était un symptôme technique.

**Règle** : "ça met trop de temps" venant d'un Lead IA expert = TOUJOURS un signal à mesurer, pas à dismiss.

## Quoi faire à la place

Voir `[[workflow-claude-code-optimal]]` pour la recette complète.

**Résumé** :
1. Architect routing taille S/M/L
2. Architect ne lit pas repos voisins par défaut
3. Test-writer MAX 3 tests par comportement
4. Phase REFACTOR test-writer SUPPRIMÉE (fusionnée code-reviewer)
5. Effort `high` partout sauf architect + jugement cross-app
6. Pipeline conditionnel selon scope (CRUD simple = 5 étapes, pas 8)

**Gain mesuré** : feature CRUD simple 4h → 1h30 (60%), feature M neo_ia 30-45 min → 12-18 min (50%).

## Anti-patterns à ne JAMAIS recréer

| Anti-pattern | Symptôme | Fix |
|---|---|---|
| "xhigh par sécurité partout" | Tous agents en xhigh | high par défaut, xhigh seulement jugement profond |
| "Test-writer 2 passes pour qualité" | Phase RED + REFACTOR | Une seule passe RED, edge cases dans code-reviewer |
| "Pipeline complet 8 agents toujours" | TOUJOURS dans rule | Critères conditionnels par gate |
| "Architect peut lire ailleurs c'est utile" | Glob/Grep cross-repo systématiques | NE PAS LIRE par défaut, autorisation explicite |
| "Plus de tests = mieux" | 6 tests pour 1 comportement | MAX 3 tests, choisir les angles discriminants |
| "Skills frontmatter = tout ce qui peut servir" | 9 skills par agent | 3-4 core, le reste à charger à la demande |

## Méta-leçon — comment éviter de recréer ça sur le prochain repo

**Pour TOUT nouveau repo** : appliquer `[[workflow-claude-code-optimal]]` DÈS le départ, pas après que l'utilisateur ait perdu 4h.

**Checklist initiale** :
- [ ] Architect a un routing taille S/M/L ?
- [ ] Test-writer a une borne max tests/comportement ?
- [ ] Phase REFACTOR test-writer = absente ?
- [ ] Gates conditionnels, pas systématiques ?
- [ ] Agents review/exécution = `high` par défaut ?
- [ ] Skills agents = 3-4 core max ?

Si non à 1+ : tu vas recréer l'erreur du 21 mai.

## Liens

- [[workflow-claude-code-optimal]] — la recette à appliquer
- [[raisonnement-revirement-pipeline-mai-2026]] — chemin de raisonnement
- [[critique-2026-05-21-refonte-pipeline-boris-pattern]] — le DA qui a sauvé
- [[raisonnement-22mai-doctrine-vs-enforcement]] — autre erreur même famille (workaround sediment)
- [[feedback_workaround_sediment]] (mémoire) — pattern accumulation
- [[workflow-claude-code-optimal]] — référence Boris
