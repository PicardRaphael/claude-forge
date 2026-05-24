---
titre: "Lisa Crofoot"
resume: "Research PM Anthropic, doctrine 'scaffolding holds Claude back' (Code with Claude London 19 mai 2026), capability curve + task horizon, 8 frontier models en 12 mois"
aliases:
  - "lisa crofoot"
  - "Lisa Crofoot"
  - "L. Crofoot"
  - "anthropic lisa"
  - "research pm anthropic"
  - "lisa anthropic scaffolding"
derniere-maj: 2026-05-24
auteur: claude
sources:
  - "https://www.youtube.com/watch?v=AgQ4cwL5eOM"
  - "https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/"
  - "https://fortune.com/2026/05/21/claude-code-london-anthropic-ai-software-engineering/"
type: "leader"
tags:
  - "#type/leader"
  - "#domaine/claude-code"
  - "#org/anthropic"
---

## QUI

- **Rôle** : Research PM (Anthropic) — produit + recherche, focus capability curve et models
- **Org** : Anthropic — équipe Claude Code / Models
- **Période active** : 2025 → présent (référence canonique mai 2026)
- **Apparition publique majeure** : keynote d'ouverture Code with Claude London 19 mai 2026 (9-10am BST) aux côtés de Boris Cherny, Cat Wu, Angela Jiang, Katelyn Lesse

## POURQUOI ELLE EST PERTINENTE

Lisa Crofoot porte **la doctrine officielle Anthropic sur le rôle du scaffolding** dans les agents — c'est-à-dire tout ce qui n'est pas le modèle lui-même : hooks, rules, agents, prompts système, decision logic externe.

Sa thèse, formulée à Code with Claude London 19 mai 2026, est devenue la **référence canonique pour la doctrine "thinnest wrapper"** (note `reference-anthropic-thinnest-wrapper` à créer) et **a directement inspiré la refonte du 22 mai 2026** sur les repos ia_back et neo_ia (suppression de 7 hooks workflow par repo).

Elle est aussi la source canonique sur :
- La **capability curve** Anthropic (8 frontier models en 12 mois : Sonnet 3 → Opus 4.7 + Mythos preview)
- Le **task horizon** : minutes (2025) → hours (2026) → continuous (futur)
- Exemple Mythos : vulnérabilité OpenBSD vieille de 27 ans découverte par un modèle frontier

## CONTRIBUTIONS CLÉS

### 1. Doctrine "scaffolding holds Claude back" — Code with Claude London 19 mai 2026

**Citation canonique** (verbatim London 19 mai 2026) :

> "Designing for the next version of Cloud, not the current one. (...) Scaffolding is what we call the parts of the agent that aren't Claude. We're seeing that as models get smarter, the scaffolding that used to help can hold Claude back."
> — Lisa Crofoot, Code with Claude London 19 mai 2026

**Implications doctrinales** :

1. Le scaffolding (hooks, rules, agents custom) **devient une dette dès que le modèle s'améliore**
2. Concevoir pour **la prochaine version du modèle**, pas la version actuelle
3. Anti-pattern : encoder dans des hooks la structure d'un repo, des paths, des patterns workflow — ils deviennent obsolètes au prochain refacto
4. Pattern correct : **hooks = lint / security / scope** uniquement, **JAMAIS workflow**

Cette doctrine a été **appliquée le 22 mai 2026** sur les repos Neoteem (cf. [[raisonnement-22mai-doctrine-vs-enforcement]] et note `session-22mai-refonte-hooks` à créer).

### 2. Catégorie 5 des 9 catégories Thariq — "Harness Engineering / Scaffolding"

Dans la grille des **9 catégories de skills Thariq Shihipar**, la **catégorie 5 = scaffolding / harness engineering**. La doctrine Lisa Crofoot est la mise à jour officielle de cette catégorie : on garde le harness MINIMAL.

Référence croisée : la skill `harness-engineering` (catégorie Thariq) doit être étendue pour absorber Ratchet Principle (Osmani) + "scaffolding holds back" (Lisa Crofoot).

### 3. Capability curve — 8 frontier models en 12 mois

Verbatim London 19 mai 2026 :

> "We've shipped 8 frontier models in 12 months : Sonnet 3 → Opus 4.7 + Mythos preview"
> — Lisa Crofoot, Code with Claude London 19 mai 2026

Implication : le cycle de mise à jour modèle est **inférieur à 2 mois**. Tout scaffolding optimisé pour un modèle N sera testé sur modèle N+1 dans les 8 semaines.

### 4. Task horizon — minutes → hours → continuous

Évolution Anthropic des tâches que Claude peut compléter de manière autonome :

| Année | Task horizon |
|-------|--------------|
| 2025 | Minutes |
| 2026 | Hours |
| Futur | Continuous |

Co-citation Lisa Crofoot + Boris Cherny à London (Boris : "Now we're on the order of like double digit hours... the last model is like 30 hours").

### 5. Mythos — vulnérabilité OpenBSD 27 ans

Exemple emblématique cité à London : Mythos (preview model frontier Anthropic) a trouvé une **vulnérabilité OpenBSD vieille de 27 ans**.

Verbatim corroboré dans `audit-qualite-rapports-chantier.md` ("Mythos OpenBSD 27 ans" — verbatim Lisa Crofoot ✓).

## VERBATIM NOTABLES

> "Designing for the next version of Cloud, not the current one. (...) Scaffolding is what we call the parts of the agent that aren't Claude. We're seeing that as models get smarter, the scaffolding that used to help can hold Claude back."
> — Lisa Crofoot, Code with Claude London 19 mai 2026

> "8 frontier models in 12 months."
> — Lisa Crofoot, Code with Claude London 19 mai 2026

> "Mythos found a 27-year-old vulnerability in OpenBSD."
> — Lisa Crofoot, Code with Claude London 19 mai 2026 (avec Boris Cherny)

## APPLICATION FORGE (22 mai 2026)

La doctrine Lisa Crofoot a directement déclenché la **refonte du 22 mai 2026** :

- **Suppression de 7 hooks workflow** par repo (ia_back, neo_ia)
- Rétablissement de la règle : hooks = **lint/security/scope** UNIQUEMENT, JAMAIS workflow
- Révision de `feedback_enforce_not_advise` (chantier 22 mai)
- Voir [[raisonnement-22mai-doctrine-vs-enforcement]] et note `session-22mai-refonte-hooks` (à créer)

## CORRECTIONS D'ATTRIBUTION (chantier 22 mai 2026)

Le verbatim "Scaffolding holds Claude back" était initialement attribué à **Cat Wu** dans certaines notes — correction faite le 22 mai 2026 : il s'agit bien de **Lisa Crofoot** à Code with Claude London 19 mai 2026.

## WIKILINKS

- [[Boris Cherny]] — co-keynote London 19 mai 2026
- [[cat-wu]] — co-keynote London 19 mai 2026
- [[angela-jiang]] — co-keynote London 19 mai 2026
- [[Thariq Shihipar]] — 9 catégories de skills, catégorie 5 = scaffolding
- [[comment-ecrire-claudemd]] — la doctrine scaffolding s'applique à CLAUDE.md
- [[comment-creer-skill]] — skills ≠ scaffolding workflow
- [[comment-creer-agent]] — agents = scaffolding minimal
- [[workflow-claude-code-optimal]] — workflow sans scaffolding workflow
- [[methode-analyser-repo]] — audit des scaffoldings d'un repo

## SOURCES

### Sources primaires (Anthropic / équipe Claude Code)

- [Code with Claude London 2026 — full livestream YouTube AgQ4cwL5eOM](https://www.youtube.com/watch?v=AgQ4cwL5eOM) — keynote 19 mai 2026 (verbatim canonique scaffolding)

### Sources secondaires

- [MIT Tech Review — coding's future](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)
- [Fortune — London as AI-coding goes mainstream](https://fortune.com/2026/05/21/claude-code-london-anthropic-ai-software-engineering/)

### Notes internes chantier 22 mai 2026

- `recherche-youtube-talks.md` §1.3 (verbatim Lisa Crofoot)
- `recherche-youtube-watch-vibe-coding.md` (corroboration)
- `audit-qualite-rapports-chantier.md` (verbatim "Mythos OpenBSD 27 ans" confirmé)
- `PLAN-EXECUTION-FINAL.md` §4 (corrections d'attribution)
