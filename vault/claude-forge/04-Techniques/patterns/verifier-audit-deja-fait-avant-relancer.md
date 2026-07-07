---
titre: "Pattern — Vérifier qu'un audit thématique n'a pas déjà été fait avant de relancer"
resume: "Checklist mécanique en 4 étapes à exécuter AVANT toute phase A d'audit thématique vault : derniere-maj des notes, recherche Knowledge/erreurs/, context-actuel.md, CHANGELOG. Prévient les audits redondants coûteux en tokens."
aliases:
  - "verifier audit deja fait"
  - "pre-check audit vault"
  - "audit redondant prevention"
  - "checklist avant audit thematique"
  - "audit deduplication guard"
derniere-maj: 2026-07-07
auteur: claude
type: technique
tags:
  - "#type/pattern"
  - "#domaine/vault"
  - "#domaine/claude-code"
  - "#pattern/audit"
---

# Pattern — Vérifier qu'un audit thématique n'a pas déjà été fait

## Problème

Le 2026-05-23 : audit thématique 04 agents-ia lancé alors que toutes les notes du dossier dataient déjà du 23 mai et référençaient `Knowledge/erreurs/agents-ia-22-claims-fausses-2026-05-23`. Pareil pour le thème 06 patterns/context déjà fait par une autre session en parallèle.

Résultat : audit redondant = perte de tokens + risque de re-corriger ce qui était déjà correct.

## Checklist — AVANT phase A de tout audit thématique

Exécuter mécaniquement dans cet ordre :

1. `mcp__forge-brain__list_notes(folder="<dossier-cible>")` → noter les `derniere-maj` du frontmatter. Si la majorité = date du jour ou veille → fort indicateur d'audit déjà fait.

2. `mcp__forge-brain__search_brain(query="<theme>-claims-fausses", limit=5)` → chercher une note `Knowledge/erreurs/<theme>-claims-fausses-YYYY-MM-DD` existante.

3. Lire `vault/claude-forge/0-Inbox/context-actuel.md` → section "Dernière session" liste les audits récents par thème.

4. Lire `vault/claude-forge/CHANGELOG.md` (10 premières lignes) → audits sont logués chronologiquement.

## Décision

- **Audit déjà fait → STOP.** Ne pas relancer.
- **User insiste** → demander : correction des erreurs résiduelles détectées depuis, ou audit fresh sur claims nouveaux apparus depuis la dernière session ?
- **Partiellement fait** (certains sous-thèmes seulement) → identifier précisément les sous-thèmes non couverts et limiter le scope à ceux-ci uniquement.

## Wikilinks

- [[audit-puis-vagues-paralleles]] — méthode d'exécution d'audit massif (phases A→B→C→D)
- [[feedback_audit_thematique_methode]] — méthode sub-agents clusters + checkpoint A avant B
- [[feedback_consolidate_searches]] — ne jamais chercher 2× la même info
