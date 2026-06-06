---
name: skills-externes-intouchables
description: Skills externes (kepano, source amont) = intouchables absolument, même description
metadata:
  type: feedback
---

Skills externes (obsidian-bases, json-canvas, obsidian-markdown, defuddle) : NE JAMAIS modifier
le SKILL.md, même pour corriger la description ou ajouter user-invocable. Modifier casse la synchro
avec la source amont.

**Why:** Raphael a tranché lors de l'audit 2026-06-06 : le principe est absolu, pas une demi-mesure.
Améliorer le déclenchement = .skill-triggers.json uniquement, jamais SKILL.md.

**How to apply:** À l'audit d'une skill, identifier d'abord si elle est externe (kepano/source amont).
Si oui : vérifier uniquement les références mortes, signaler les écarts sans les appliquer.
