---
titre: "Claude Fable 5 — modèle classe Mythos, grand public puis suspendu (export-control)"
resume: "Modèle Anthropic classe Mythos (au-dessus d'Opus), annoncé 9 juin 2026 (CC v2.1.170), 1M contexte par défaut, adaptive thinking only, fallback auto vers Opus 4.8 sur requêtes flaggées (cyber/bio). Suspendu avec Mythos 5 le 12 juin par directive export-control US ; Opus/Sonnet/Haiku non affectés."
aliases:
  - "Claude Fable 5"
  - "Fable 5"
  - "claude-fable-5"
  - "Mythos 5"
  - "Mythos-class model"
  - "Project Glasswing"
derniere-maj: 2026-06-16
auteur: claude
type: modele
sources:
  - "https://www.anthropic.com/news/claude-fable-5-mythos-5"
  - "https://code.claude.com/docs/en/changelog"
tags:
  - "#type/modele"
  - "#domaine/anthropic"
  - "#domaine/claude"
---

# Claude Fable 5

> Annoncé **9 juin 2026** (CC v2.1.170, verbatim changelog : *« a Mythos-class model that we've made safe for general use. Fable's capabilities exceed those of any model we've ever made generally available »*). Tier « Mythos-class » au-dessus d'Opus, rejoignant Opus/Sonnet/Haiku.

## Caractéristiques

- **1M tokens de contexte par défaut** (le suffixe `[1m]` des noms de modèle est normalisé/strippé depuis v2.1.173).
- **Adaptive thinking only** (comme Opus 4.8) : `budget_tokens` manuel → erreur 400. Le modèle décide quand/combien penser, calibré par effort × complexité.
- **Safety classifiers** : repli automatique vers **Opus 4.8** sur les requêtes flaggées (domaines cyber, bio). Si une org n'a pas Opus 4.8 activé, l'auto mode retombe sur le meilleur Opus disponible (fix v2.1.176).
- **Mythos 5** = même modèle sans les safety classifiers, disponibilité limitée via **Project Glasswing** (orgs approuvées uniquement).

## ⚠️ Suspension export-control (12 juin 2026)

Anthropic a reçu une **directive de contrôle d'export du gouvernement US** l'obligeant à **suspendre l'accès à Fable 5 ET Mythos 5**. Les autres modèles (Opus 4.8, Sonnet 4.6, Haiku 4.5) ne sont **pas affectés**. Référence pour différences Fable/Mythos : [anthropic.com/news/claude-fable-5-mythos-5](https://www.anthropic.com/news/claude-fable-5-mythos-5).

## Pertinence forge

C'est le modèle qui a fait tourner la session de découverte (run cc-news 16 juin) avant/pendant la fenêtre de suspension. À surveiller : réactivation éventuelle, et impact sur le défaut modèle (préférence Raphael = Opus 4.8, cf feedback memory `preference-modele-opus-4-8`). Ne pas basculer un défaut de config sur Fable 5 tant que la disponibilité n'est pas stable.

## Wikilinks

- [[CC juin 2026 - v2.1.160 ultracode]] — versions CC liées (v2.1.170 intro, fixes 173-176)
- [[MOC-Modeles]]
- [[CC 28 mai 2026 - Opus 4.8 + Dynamic Workflows]] — modèle de repli des classifiers
