---
titre: Context Actuel
resume: "Working memory dynamique — mis à jour par /done, lu par /recap. Session 2026-05-23 (tour 2) : audit thématique 02-prompt-engineering vault (24 corrections sur 14 notes) + 16 fiches leaders créées (prompt + industrie)."
aliases:
  - "context actuel"
  - "contexte courant"
  - "working memory"
  - "memoire de travail"
  - "etat actuel"
type: context
status: active
derniere-maj: 2026-05-23
auteur: claude
tags:
  - "#type/context"
  - "#meta/working-memory"
---

## Phase actuelle

Audits thématiques vault forge en cours (méthode A→B→C→D→E + propagation F) — 02 prompt engineering ✅ terminé. Reste : 03 RAG, 04 agents-ia, 05 fine-tuning, 06 patterns/context (déjà partiellement fait par autre session), 07 leaders-modeles-industrie.

## Dernière session (2026-05-23 — tour 2)

### Décisions prises
- **Méthode A.5** : insérer 3-4 WebFetch directs entre checkpoint A (inventaire) et phase B (sub-agents) sur les sources primaires suspectes. Validé empiriquement = gain 30 min wall-time.
- **Yann LeCun en `prompt/`** : malgré position critique LLM, fiche dans `prompt/` (pas seulement `industrie/`) pour balance idéologique du vault.
- **Cross-référencement leaders** : Karpathy/Willison/Mollick existant en `agents/` ou `industrie/` — Mollick dédoublé en `prompt/` car papier prompt direct (Prompting Science Report 1).

### En cours
- Commit `7622e12` poussé : 16 fiches leaders (10 prompt + 6 industrie) + audit PE final.
- Audit thème 06 (patterns + context + stacks) déjà fait en parallèle par autre session (commit dans CHANGELOG).

### Prochaines étapes
- Audit thème 03 (RAG) — 8+ notes dans `04-Techniques/rag/`
- Audit thème 04 (agents-ia) — 10+ notes
- Audit thème 05 (fine-tuning) — 15+ notes
- Audit thème 07 (leaders, modeles, industrie) — ~80 notes (le plus gros)
- Capitalisation : Reid Hoffman avec [[Sam Altman]] + [[Dario Amodei]] : vérifier ces fiches existent déjà

## Fils ouverts

- **Pattern récidiviste tweet/paraphrase verbatim** : 5e occurrence en 2 jours. Méthode A.5 ([[feedback_webfetch_avant_subagents_audit]]) en mitigation. Surveiller si baisse aux prochains audits.
- **Cross-categories leaders** : Karpathy a 1 seule fiche dans `agents/`. Mériterait stub `prompt/` (Software 3.0, context engineering originator). À traiter au prochain audit ou sur demande.
- **Backlinks à vérifier** : les notes prompt-engineering pointent vers MOC-Leaders-Prompt — vérifier que ce MOC est à jour avec les 10 nouvelles fiches.

## Liens

- [[Raphael-Picard]]
- [[Claude-Forge]]
- [[methode-analyser-repo]]
- [[feedback_webfetch_avant_subagents_audit]]
- [[feedback_audit_thematique_methode]]
