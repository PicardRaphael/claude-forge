---
name: meta-generator-pending
description: Méta-prompt routine higher-order pour générer bibliothèque ~40 prompts analyse — EN ATTENTE exécution post audit dogfooding + review tête reposée
metadata: 
  node_type: memory
  type: project
  originSessionId: 4403f197-2d1a-42ea-b19e-8bb88a8b1a30
---

# Méta-prompt bibliothèque prompts d'analyse — EN ATTENTE

## Localisation

`vault/claude-forge/07-Prompts/analyse/_META-GENERATOR.md`

## Décisions Raphael (2026-05-23)

- **Mode** : full batch + review groupée (pas un-par-un)
- **Localisation cible** : `vault/claude-forge/07-Prompts/analyse/`
- **Scope** : 10 catégories (~40 prompts)

## Bloqueurs avant exécution

1. ✅ Audit Claude Code 23 mai DONE
2. 🔄 Audit Claude-forge dogfooding (08) EN COURS — BLOQUE
3. 🆕 Review méta-prompt à tête reposée — BLOQUE
4. ✅ Validation localisation DONE

**Why:** Méta-prompt rédigé fin de session longue (audit thématique CC + propagation + capitalisation). Risque erreur de design qui se propagerait dans 40 prompts générés.

**How to apply:** Quand Raphael dira "go" demain ou plus tard, lire `_META-GENERATOR.md` (la note vault contient le prompt complet prêt à coller en session fraîche). Vérifier que les 2 bloqueurs restants sont verts avant de lancer.

## Wikilinks
- [[meta-prompt-bibliotheque]] (alias de la note vault)
- [[methode-analyser-repo]]
- [[sequence-canonique-modification]]
