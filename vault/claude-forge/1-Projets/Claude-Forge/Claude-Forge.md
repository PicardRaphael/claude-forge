---
titre: Claude-Forge
resume: Framework de productivité pour Claude Code — skills, agents, hooks, vault, mémoire
aliases:
  - claude-forge
  - forge
  - le forge
  - framework forge
type: context
status: active
derniere-maj: 2026-07-09
auteur: claude
tags:
  - "#type/context"
  - "#type/projet"
  - "#projet/claude-forge"
---

## Description

Framework personnel de productivité pour Claude Code, créé par [[Raphael-Picard|Raphael]]. Kit d'outillage sur-mesure qui génère dynamiquement des Skills, Rules, Hooks et Agents adaptés à n'importe quelle stack. Base de TOUS les projets Neoteem.

## Pourquoi ce projet

Transformer Claude Code d'un outil de coding en un **partenaire** (contrat Jarvis). Capitaliser chaque apprentissage. Vitrine de l'expertise IA de Raphael.

## Stack & composants

- ~40+ skills, 15+ agents, 14+ rules, 8+ hooks
- Vault Obsidian (forge-brain) comme mémoire infinie
- Auto Memory (MEMORY.md + fichiers)
- CLI Obsidian (obsidian-cli.sh)
- Python hooks (delegate-guard, vault-query-tracker/guard)
- Pipeline : architect-first → code-review → devil's advocate

## Contraintes

- Projet PERSONNEL, pas Neoteem
- Généraliste, pas de focus repos pro sauf demande
- CLAUDE.md ~100 lignes max, skills < 500 lignes
- Repos projet doivent rester autonomes sans claude-forge

## Liens

- [[Raphael-Picard|Raphael Picard]]
- [[Neoteem|Neoteem]]


## État récent (2026-07-09)

- **Sweep descriptions** : 21 skills ramenées ≤ 250 chars (−855 tokens résidents/session) ; doctrine budget/drop listing (CC ≥ 2.1.129) propagée dans skill-creator + checklist + rule.
- **Fusions forge-review 50 → 48** : cc-rag-ref → `rag-design/references/` ; web-search-canonical-source → rule + note [[verification-sources-canoniques]]. F2 (trio doctrine) en **measure-first** — hôte imposé [[methode-pivoter-doctrine]] (34 backlinks), protocole A/B dans `output/mesure-F2-fusion-doctrine.md`. 0 KILL. Arbitrage : perf de déclenchement > budget (feedback tier-1).
- **delegate-guard corrigé** (skills empilées CC ≥ 2.1.202 + fenêtre 15→80) : fix appliqué manuellement par Raphael (classifier self-mod), 39/39 tests, validé en réel. Cf [[raisonnement-debug-delegate-guard-empilement]].
- **Doctor poste perso** : defaultMode auto, context7 + connecteur GChat désactivés, 4 doublons mémoire locale purgés.

## État récent (2026-06-29)

- Orientation **agent-first** actée : forge-brain optimisé pour la boucle Jarvis (MCP/search), pas la navigation humaine Obsidian (débranchée). Cf [[decision-vault-agent-first]].
- Doctrine 22 mai en vigueur : hooks = lint/sécu/scope uniquement, jamais workflow agentique.
- Outillage : MCP forge-brain (22 outils), skills créatrices (skill/subagent/hook/claudemd-creator), `/done` maintient désormais les notes de contexte projet (étape 6-bis).
- Pivot agent-first **appliqué bout-en-bout** (11 foyers, advisor+DA) : SCHEMA refondu (raw/ retiré), vault-audit débarrassé de la logique MOC, `/recap` fixé (`find vault`→`find_by_property` MCP). Cf [[raisonnement-2026-06-27-vault-agent-first]].
- Reste hors-pivot : provider-reorg 14 juin (`02-Concurrents`/`03-Modeles` en dur dans quelques composants).
