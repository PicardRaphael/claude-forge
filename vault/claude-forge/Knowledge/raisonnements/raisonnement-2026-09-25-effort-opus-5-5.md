---
titre: "Pivot du 25 septembre 2026 — l'effort high n'est plus « le défaut officiel » sur Opus"
resume: "Opus 5.5 devient l'alias opus avec un effort API par défaut medium et aucun niveau de départ recommandé. Pivot validé par Raphaël : forge garde high posé explicitement, comme choix délibéré et non plus comme alignement sur le défaut ; aucun frontmatter ne bouge avant un sweep Opus 5.5 à n=3 runs par niveau (medium vs high)."
aliases:
  - "pivot effort Opus 5.5"
  - "effort medium Opus 5.5"
  - "raisonnement effort 25 septembre"
  - "high choix délibéré"
  - "sweep Opus 5.5"
derniere-maj: 2026-09-25
auteur: claude
type: raisonnement
sources:
  - "https://platform.claude.com/docs/en/build-with-claude/effort"
  - "https://platform.claude.com/docs/en/models/overview"
  - "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md"
tags:
  - "#type/raisonnement"
  - "#domaine/claude-code"
  - "#doctrine/2026"
---

# Pivot effort — Opus 5.5 (25 sept. 2026)

## Déclencheur

Run `cc-news` du 25 sept. 2026. CC v2.1.280 (22 sept.) fait d'[[Opus 5.5]] le modèle Opus par défaut : l'alias `opus` de tous les frontmatters forge y résout sans modification de fichier.

## Ce que dit la source (crédit MAX)

Page [Effort](https://platform.claude.com/docs/en/build-with-claude/effort), section *Recommended effort levels for Claude Opus 5.5* :

> « Claude Opus 5.5 supports all five effort levels, and `medium` is the default (Claude Opus 5 and earlier Opus models default to `high`, so a request that omits `effort` runs one level lower than it did on Claude Opus 5). […] Run an effort sweep on your own evals rather than carrying settings over from an earlier model »

Contraste : les sections Opus 5 et Fable 5.1 disent « **Start with `high`, the default** ». La section Opus 5.5 ne donne aucun point de départ.

## Doctrine avant le pivot

[[effort-opus-47-doctrine-anthropic-2026]] et `memory/feedback_allocation_modele_effort.md` justifiaient `high` comme « point de départ officiel sur Opus 5 / Fable 5 / Sonnet 5 ». La justification tenait tant que `opus` voulait dire Opus 5.

## Contradiction

Sur le modèle que forge utilise réellement pour ses agents de jugement, `high` n'est plus ni le défaut ni une recommandation. La règle « sweep à chaque changement de modèle » (Fable 5.1, 5 sept.) est **renforcée** ; seule la justification « défaut officiel » tombe.

## Décision (Raphaël, 25 sept. 2026 — verdict [v] sur `doctrine-impact-check`)

1. Garder `effort: high` **posé explicitement** dans les frontmatters, comme **choix délibéré** — plus présenté comme le défaut officiel.
2. Savoir qu'un composant **sans `effort:`** tourne désormais en `medium` sur Opus.
3. **Aucun frontmatter ne bouge** avant un sweep Opus 5.5 à **n=3 runs par niveau** (`medium` vs `high`), protocole du sweep Opus 5 du 5 sept. (même agent read-only, même cible, prompt gelé, critère = un fichier lu en plus qui change la conclusion).

Pourquoi ne pas passer à `medium` tout de suite : le sweep Opus 5 à n=1 montrait une variance inter-runs élevée entre deux niveaux voisins ; descendre un agent de jugement sur une absence de mesure reproduirait l'erreur que ce sweep disciplinait.

## Propagation

| Surface | Action |
|---|---|
| [[effort-opus-47-doctrine-anthropic-2026]] | ligne Opus 5.5 + section pivot |
| [[doctrine-par-modele-opus5-fable5]] | amendement Opus 5.5 |
| `memory/feedback_allocation_modele_effort.md` | description + paragraphe Opus 5.5 |
| `memory/feedback_preference_modele_opus.md` | alias `opus` → Opus 5.5, repli Opus 5 puis 4.8 |
| `memory/MEMORY.md` | ligne d'index preference-modele-opus |
| skill `subagent-creator` | « point de départ officiel » → choix délibéré |
| skill `cc-features-ref` | défaut Opus + exemple PermissionRequest agent-type (interdit v2.1.280) |
| `CLAUDE.md` forge | inchangé : « Effort `high` par défaut » décrit déjà le choix forge, pas le défaut API |

## Reste ouvert

- Sweep Opus 5.5 non exécuté à la date du pivot.
- Test session fraîche (étape 5 de [[methode-pivoter-doctrine]]) à faire.
