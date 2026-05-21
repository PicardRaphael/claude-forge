---
titre: "Critique — Repartition Opus/Sonnet ia_back + neo_ia"
resume: "DA sur downgrade devs Sonnet high : BLOQUER tant que contradiction memoire all-opus non resolue. dev-neochat a risque. 3 memoires contradictoires a nettoyer."
aliases:
  - "critique opus sonnet repartition"
  - "critique model downgrade ia_back neo_ia"
  - "critique sonnet devs agents"
  - "DA opus vs sonnet mai 2025"
type: critique
domaine: claude-code
derniere-maj: 2026-05-21
auteur: devils-advocate
tags:
  - "#type/critique"
  - "#domaine/claude-code"
  - "#projet/ia-back"
  - "#projet/neo-ia"
sources:
  - "Session 2026-05-21 — repartition Opus/Sonnet"
---

## Verdict

**Bloquants : 1 | Avertissements : 4 | Nitpicks : 2**

**Decision recommandee :** BLOQUER (contradiction memoire) puis LIVRER AVEC CORRECTIONS

## Bloquant — Contradiction memoire canonique

`feedback_all_opus.md` (16 jours, plus recente) dit : *"Tous les agents doivent etre opus. Zero sonnet. Ne JAMAIS mettre sonnet sur un agent de repos projet."*

La proposition met 6 agents en Sonnet. Les deux ne peuvent pas coexister.

**Resolution requise :** Soit reecrire `feedback_all_opus.md` pour reflechir la nouvelle politique, soit revert les agents en Opus.

## Avertissements

1. **dev-neochat Sonnet high** : domaine le plus complexe (LangGraph multi-agent, AgentBlueprint, HybridToolSelector, interrupt handlers). Bugs de graphe subtils echappent aux tests unitaires. Considerer Opus high.

2. **Conflit frontmatter/body** : `validator.md` (xhigh vs medium dans body), `dev.md` (high vs medium dans body). Opus 4.7 est litteral — le body peut creer de la confusion.

3. **3 memoires contradictoires** : opus47_workflow (gates=sonnet), all_opus (zero sonnet), proposition (devs=sonnet). Nettoyer les obsoletes.

4. **Pas de metriques** : economie tokens non mesuree, taux de correction code-reviewer sur code Sonnet vs Opus inconnu. Optimisation a l'aveugle.

## Nitpicks

- "Advisor Strategy" dans commits = trompeur, creer confusion historique
- Body effort text dans agents est vestige des migrations successives

## Si je devais le faire marcher

1. Trancher la contradiction memoire (reecrire ou revert)
2. Remonter dev-neochat en Opus high (compromis cout/qualite)
3. Harmoniser frontmatter/body des agents touches
4. Mesurer taux de FAIL code-reviewer pendant 2-4 semaines
5. Considerer hook de validation model/effort pour empecher drift

## Agents valides sans reserve

- `refactor-pg-function` Opus xhigh : correct, migration legacy critique
- `validator` Opus xhigh : correct, hard gate behavioral equivalence
- `schema-mapper` Sonnet high : correct, read-heavy doc generation
- `dev-shared-tools` Sonnet high : correct, tools LangChain independants
- `dev-neodoc`/`dev-neomail` Sonnet high : acceptable, scope plus simple que NeoChat

## Candidat over-engineered

- `db-inspector` Opus xhigh pour des `psql \d+` templates : Sonnet high suffirait. Mais read-only + plan mode limite le risque. Nitpick.

## Liens

- [[erreur-advisory-rules-insuffisantes]] — rules advisory = 80% compliance, hook necessaire
- [[critique-tdd-neo-ia-proposal]] — precedent Sonnet pour execution
