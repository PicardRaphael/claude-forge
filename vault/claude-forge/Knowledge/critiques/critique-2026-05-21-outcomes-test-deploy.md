---
titre: "Critique — Deploiement /outcomes-test sur ia_back + neo_ia"
resume: "3 bloquants : rubric templates ne couvrent pas les plans architect (use case principal), outcomes absent de la chaine markers, pattern parite forcee byte-identical"
aliases:
  - critique outcomes test deploy
  - critique outcomes grader ia_back neo_ia
  - DA outcomes test mai 2026
  - devil advocate outcomes
type: knowledge
domaine: claude-code
derniere-maj: 2026-05-21
auteur: devils-advocate
tags:
  - "#type/knowledge"
  - "#type/critique"
  - "#projet/ia-back"
  - "#projet/neo-ia"
  - "#domaine/claude-code"
sources:
  - "Session 2026-05-21 — deploiement outcomes-test"
---

## Verdict

**BLOQUER** — 3 bloquants, 3 avertissements, 2 nitpicks.

## 3 Bloquants

### 1. Templates rubric ne couvrent pas le use case principal
La rule dit "lancer /outcomes-test apres architect" (cible = plans/specs). Les 4 templates dans references/ couvrent : Skill CC, Agent CC, Hook CC, CLAUDE.md. Zero template pour un plan architect ou une spec technique. 100% des invocations via la rule tombent dans le fallback "suggerer un template inadapte".

### 2. Outcomes absent de la chaine architect-marker
architect-guard (TS sur ia_back, Python sur neo_ia) utilise .architect-marker pour gater les dev agents. Le marker est pose par l'architect. Les dev agents partent des que le marker existe — que outcomes ait tourne ou non. Rule "OBLIGATOIRE" sans hook = ~80% compliance (3 incidents documentes).

### 3. Copie byte-identical = parite forcee
Meme fichier (138L skill + 93L agent + 103L templates + 21L rule) sur forge, ia_back (TS hexagonal), neo_ia (Python LangGraph). Templates de criteres CC sur des repos qui produisent du code metier, pas des composants Claude Code.

## Chemin recommande

1. Template plan-spec dans rubric-templates.md avec criteres par stack
2. Hook outcomes-guard dans la chaine markers (bloque dev si .outcomes-marker absent)
3. Au moins 1 RUBRIC.md reel par repo
4. Adapter templates par nature de repo
5. Forge = reference canonique, repos = instances specialisees (pas byte-identical)

## Pattern identifie

Reprise du pattern parite forcee multi-repo ([[critique-2026-05-13-setup-lojii]]). Meme cause racine : copier un mecanisme generique sans adapter au contexte cible.

Aggravant : la rule advisory sans hook est exactement le pattern documente dans [[erreur-advisory-rules-insuffisantes]] (3 incidents, ~80% compliance).

## Liens

- [[erreur-advisory-rules-insuffisantes]] — rules advisory = 80% compliance, hook obligatoire
- [[critique-2026-05-13-setup-lojii]] — parite forcee precedent
- [[ia_back]] — repo cible TypeScript hexagonal
- [[neo_ia]] — repo cible Python LangGraph monorepo
