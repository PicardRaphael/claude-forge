---
titre: "Split crédit programmatique Claude — 15 juin 2026 (À VÉRIFIER)"
resume: "Annonce multi-sources tierces : à partir du 15 juin 2026, l'usage programmatique (Agent SDK, GitHub Actions, claude -p, frameworks tiers) tirerait sur un crédit mensuel dédié séparé des limites d'abonnement chat. NON confirmé en source primaire Anthropic au 2 juin 2026 — montants par tier non vérifiés"
aliases:
  - "split crédit programmatique"
  - "agent credits 15 juin"
  - "programmatic usage billing Claude"
  - "crédit Agent SDK séparé"
  - "facturation usage agentique Anthropic"
type: industrie
domaine: anthropic
derniere-maj: 2026-06-02
statut: a-verifier
auteur: claude
sources:
  - "https://www.infoworld.com/article/4171274/anthropic-puts-claude-agents-on-a-meter-across-its-subscriptions.html"
  - "https://www.it-connect.tech/vibe-coding-claude-unlimited-api-ends-on-june-15-2026/"
  - "https://github.blog/changelog/2026-06-01-updates-to-github-copilot-billing-and-plans/"
tags:
  - "#type/industrie"
  - "#domaine/anthropic"
  - "#statut/a-verifier"
---

> [!warning] Statut : À VÉRIFIER (non confirmé source primaire au 2 juin 2026)
> Cette note capitalise une **annonce relayée par plusieurs sources tierces indépendantes**, mais **absente de anthropic.com/news ET de support.claude.com/release-notes** au moment du scan (2 juin 2026). Les montants par tier ne sont PAS confirmés. Re-vérifier après le 15 juin. Cf [[feedback_llm_deep_research_version_numbers]] (chiffres aggregateurs = risque hallucination).

## Claim

À partir du **15 juin 2026**, Anthropic séparerait l'**usage programmatique** de Claude des limites d'abonnement chat standard. L'usage via **Agent SDK, GitHub Actions, `claude -p` et frameworks tiers** tirerait sur un **crédit mensuel dédié**, facturé à des tarifs API, distinct et non reportable.

Montants relayés (NON confirmés primaire) : Pro ~20 $/mois, Max 5x ~100 $, Max 20x ~200 $.

## Pourquoi c'est crédible malgré l'absence primaire

- **Corroboration multi-sources indépendantes** : InfoWorld + it-connect + devtoolpicks, non liées entre elles.
- **Miroir confirmé chez le concurrent** : GitHub Copilot a annoncé un changement de facturation analogue (usage-based, AI Credits) le **1er juin 2026**, lui confirmé en source primaire (github.blog). Mouvement d'industrie cohérent.
- **L'index news n'est pas l'endroit d'une politique billing** : ce type d'info vit souvent sur support.claude.com ou un post /news/ daté hors-index — absence ≠ inexistence.

## Impact forge (si confirmé)

⚠️ **Actionnable** : les setups forge qui consomment de l'API programmatique (Agent SDK, GitHub Actions, exécutions `claude -p`, Dynamic Workflows lancés en batch) seraient facturés sur un crédit séparé des limites interactives. À budgéter si vrai.

## À faire

- [ ] Re-vérifier sur anthropic.com/news + support.claude.com **après le 15 juin 2026**
- [ ] Si confirmé : retirer le bandeau `statut: a-verifier`, poser les montants vérifiés, déplacer l'impact forge en certain
- [ ] Si infirmé : supprimer la note (delete_note)

## Liens

- [[CC juin 2026 - v2.1.160 ultracode]] — drop CC du même run (juin 2026)
- [[MOC-Industrie]]
