---
aliases:
  - critique Will vs ECC
  - deux doctrines Anthropic agents
  - minimum vs maximum agents paradoxe
  - agent client vs setup dev
  - résolution paradoxe Anthropic
resume: "Critique résolutive 26 mai 2026 — Will (CwC London, agent Stock Pilot livré client) prêche minimum d'agents. ECC (hackathon winner Anthropic) déploie 47 agents. Les 2 sont vrais : pas le même cas d'usage."
derniere-maj: 2026-05-26
tags:
  - "#type/critique"
  - "#domaine/agents"
  - "#statut/canonique"
---

# Critique résolutive — Will vs ECC, deux doctrines Anthropic

## Le paradoxe observé

26 mai 2026, en analysant deux sources Anthropic-validées :

**Source A : Will (Anthropic Applied AI), talk Code with Claude London**
- Cas : agent Stock Pilot (inventory management) LIVRÉ à un client
- Recommandation : minimum d'agents, frontier models can manage
- Réduit de 12 tools + 3 sub-agents à 3 tools + 1 sub-agent
- Eval 62% → 92%
- Doctrine : *"You just don't need as many sub-agents"*

**Source B : Affaan Mustafa (ECC), Grand Prize Anthropic Hacker Marathon**
- Cas : setup PERSONNEL pour développer avec Claude Code
- Recommandation : massivement spécialiser
- 28-47 agents, 119-181 skills, 60-79 commands
- 154K stars GitHub
- Jury : Boris Cherny, Cat Wu, Thariq Shihpar

**Contradiction apparente** : les deux sont validés par Anthropic. Lequel suivre ?

## Résolution

**Pas la même chose**. Les deux ont raison dans leur contexte.

### Cas A — Agent CLIENT en production

Quand on livre un agent à un end-user :
- Latency = critique
- Tokens = coût direct
- Reliability = essentielle
- Maintenance = coût récurrent

→ **Minimiser** les sub-agents fait sens. Frontier models (Opus 4.7) peuvent gérer beaucoup de complexité en un seul contexte. Sub-agent = communication breakdown + overhead.

### Cas B — Setup DEV personnel

Quand on développe AVEC Claude Code :
- Productivité dev = critique
- Spécialisation = gain de qualité
- Token cost = absorbé par usage personnel
- Reusabilité = élevée (mêmes skills réutilisées tous les jours)

→ **Spécialiser** fait sens. Chaque agent / skill = un pattern testé en production sur des mois.

## Croisement avec Google + MIT (arXiv 2512.08296)

Le paper Google/MIT donne le critère quantitatif :
- **Threshold 45%** : si single agent atteint > 45% success rate, multi-agent pas cost-effective
- **Tâches séquentielles** : multi-agent dégrade 39-70%
- **Tâches parallèles** : multi-agent gain +81%

Donc le vrai axe n'est pas "minimum vs maximum" mais :

**"Quel type de coordination pour ma tâche ?"**

| Cas | Coordination | Justification |
|-----|--------------|---------------|
| Agent livré client, tâche séquentielle | Single agent ou orchestrateur central | Sequential dégrade 39-70%, error 4.4x vs 17x |
| Dev personnel, tâches indépendantes | Multi-agent spécialisé | Parallel gain +81%, overhead absorbé |
| Audit / review d'un livrable existant | Validator read-only séparé | Anti-self-grading |
| Exploration / recherche | Researcher dédié | Pas de gain à mélanger explore+build |

## Implications pour forge

Forge = setup DEV personnel multi-projet. Donc :

1. ✅ **Justifié** d'avoir 16 agents + 30 skills + 14 hooks
2. ✅ **Justifié** de spécialiser (devils-advocate, project-auditor, skill-creator, etc.)
3. ❌ **Non justifié** : agents qui orchestrent (no CTO agent — déjà notre règle)
4. ⚠️ **À mesurer** : pour chaque agent forge, threshold single-agent success rate
5. ⚠️ **À éviter** : sub-agent sur tâche séquentielle simple (cf [[google-mit-scaling-agent-systems-2025]])

Pour les agents qu'on construit POUR les projets clients (ia_back, neo_ia agents Loji) :
- Suivre Will : minimum, frontier models, skills > sub-agents pour progressive disclosure
- Pas suivre ECC : c'est pour dev personnel, pas client

## Le piège à éviter

❌ Appliquer la doctrine ECC aux agents qu'on livre dans neo_ia (NeoChat, NeoDocs)
❌ Appliquer la doctrine Will à notre forge (under-tooling)
❌ Confondre les deux et bricoler "un peu des deux"

✅ Identifier le cas d'usage AVANT de choisir la doctrine

## Anti-pattern de drift doctrinal

Cette critique doit rester ACCESSIBLE pour éviter qu'on retombe dans la confusion. Si dans 3 mois quelqu'un dit "Will dit minimum, donc on supprime 10 agents forge" → renvoyer à cette note.

## Liens

- [[google-mit-scaling-agent-systems-2025]] — threshold quantitatif
- [[ecc-pattern-personal-dev-setup]] — Cas B détaillé
- [[affaan-mustafa-ecc-hackathon-winner]] — leader Cas B
- [[software-factory-pattern-2026]] — pattern intermédiaire
- [[comment-creer-agent]] — canonique forge à ajuster avec cette nuance
- [[methode-pivoter-doctrine]] — si on décide de pivoter
