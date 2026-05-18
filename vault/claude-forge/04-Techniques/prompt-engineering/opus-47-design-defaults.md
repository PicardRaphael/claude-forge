---
titre: "Opus 4.7 Design Defaults"
resume: "Style visuel par défaut persistant d'Opus 4.7 (cream/Georgia/terracotta) et 2 contre-mesures officielles Anthropic"
aliases:
  - "opus 4.7 design defaults"
  - "opus design style"
  - "cream georgia terracotta"
  - "AI slop aesthetic"
  - "frontend defaults opus"
  - "design defaults claude"
domaine: technique
type: technique
derniere-maj: 2026-05-18
auteur: claude
sources:
  - "https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices"
tags:
  - "#type/technique"
  - "#domaine/prompt-engineering"
---

## Problème

Opus 4.7 a un style visuel "maison" **persistant** pour le frontend :
- Backgrounds warm cream/off-white (~`#F4F1EA`)
- Serif display type (Georgia, Fraunces, Playfair)
- Italic word-accents
- Accents terracotta/amber

Ce style convient aux briefs éditoriaux, hospitality, portfolios. Il est **inadapté** pour dashboards, dev tools, fintech, healthcare, enterprise apps — et apparaît aussi dans les slide decks.

Les instructions génériques ("don't use cream", "make it clean and minimal") **ne fonctionnent pas** — le modèle bascule sur une autre palette fixe plutôt que de varier.

## Contre-mesure 1 : Specs concrètes

Spécifier une alternative visuelle concrète avec palette hex, typographie, et direction artistique :

```text
Design a desktop landing page for [brand].
Visual direction: cold monochrome, pale silver-gray → blue-gray → near-black.
Color palette: #E9ECEC, #C9D2D4, #8C9A9E, #44545B, #11171B.
Typography: square angular sans-serif, wider letter spacing.
```

Le modèle suit les specs concrètes avec précision.

## Contre-mesure 2 : Propose-options-first

Faire proposer des options AVANT de construire — casse le default et produit des directions réellement différentes :

```text
Before building, propose 4 distinct visual directions tailored to this brief
(each as: bg hex / accent hex / typeface — one-line rationale).
Ask the user to pick one, then implement only that direction.
```

Cette approche remplace avantageusement l'usage de `temperature` pour obtenir de la variété design.

## Prompt anti-AI-slop (Anthropic officiel, allégé pour 4.7)

Opus 4.7 nécessite **moins** de guidance anti-slop que les modèles précédents. Ce snippet suffit :

```text
<frontend_aesthetics>
NEVER use generic AI-generated aesthetics like overused font families
(Inter, Roboto, Arial, system fonts), cliched color schemes (particularly
purple gradients on white or dark backgrounds), predictable layouts and
component patterns, and cookie-cutter design that lacks context-specific
character. Use unique fonts, cohesive colors and themes, and animations
for effects and micro-interactions.
</frontend_aesthetics>
```

## Liens

- [[Opus 4.7]]
- [[deprecated-techniques-2026]]
- [[over-specification-paradox]]
- [[MOC-Techniques]]
