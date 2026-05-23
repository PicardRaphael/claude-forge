---
titre: "Silent Assumptions — Karpathy anti-pattern coding IA"
resume: "Anti-pattern Karpathy : LLM fait hypothèses implicites sans vérifier. Un des 4 modes de failure du coding IA listés par Karpathy (sans hiérarchie)"
aliases:
  - "Silent Assumptions"
  - "silent assumptions"
  - "hypotheses implicites"
  - "karpathy anti-pattern"
  - "assumptions silencieuses"
type: technique
domaine: agents
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://x.com/karpathy/status/2015883857489522876"
tags:
  - "#type/technique"
  - "#domaine/agents"
---

## Description

Anti-pattern identifié par **Andrej Karpathy** (janvier 2026, tweet failure modes LLM coding) : le modèle fait des hypothèses implicites sur le contexte, les contraintes ou les attentes sans les vérifier explicitement. Conduit à du code qui "semble correct" mais ne répond pas au vrai problème.

⚠️ **Nuance attribution** : Karpathy liste 4 anti-patterns sans hiérarchie ("anti-pattern #1" n'est pas dans son verbatim — c'est une lecture interprétative forge). Les 4 modes : silent assumptions, overcomplexity, scope creep, vague execution.

> ✅ Verbatim Karpathy : *"models make wrong assumptions on your behalf and barrel ahead without checking. They don't manage their own confusion, don't ask for clarification, don't surface inconsistencies, don't present tradeoffs, don't push back when they should."*

## Comment l'éviter

- Toujours expliciter les contraintes et le contexte
- Vérifier les hypothèses avant d'implémenter
- Demander clarification plutôt que deviner
- Forcer le modèle à présenter ses tradeoffs et alternatives
- Pattern complémentaire : [[running-implementation-notes]] (Thariq) — capturer les décisions d'ambiguïté au fil de l'eau

## Liens

- [[MOC-Techniques]]
- [[Andrej Karpathy]]
- [[running-implementation-notes]]
- [[pattern-spec-driven-development]]
