---
titre: "David Shapiro — ACE Framework, Cognitive Architecture"
resume: "Créateur du framework ACE (Autonomous Cognitive Entities, 2023), architecture cognitive 6 couches inspirée du modèle OSI et de Kohlberg. Approche cognition-first, moral reasoning en couche supérieure. YouTuber IA influent"
aliases:
  - "David Shapiro"
  - "david shapiro"
  - "dave shap"
  - "ACE framework creator"
  - "autonomous cognitive entities"
  - "dave-shap-automator"
role: "AI Researcher, Creator ACE Framework"
affiliation: "Human-AI Empowerment Lab, Clemson University"
derniere-maj: 2026-05-11
auteur: claude
sources:
  - "https://arxiv.org/abs/2310.06775"
  - "https://github.com/daveshap/ACE_Framework"
  - "https://medium.com/@dave-shap/autonomous-agents-are-here-introducing-the-ace-framework-a180af15d57c"
tags:
  - "#type/leader"
  - "#domaine/agents"
  - "#domaine/ia"
type: leader
---
## Profil

Chercheur IA au Human-AI Empowerment Lab (Clemson University). YouTuber IA influent. Auteur et penseur sur l'architecture cognitive des agents autonomes. Approche transdisciplinaire : CS, neurosciences cognitives, psychologie, philosophie, éthique.

## Contributions clés

### ACE Framework — paper "Conceptual Framework for Autonomous Cognitive Entities" (octobre 2023)
Paper arXiv 2310.06775 (3 oct 2023). Auteurs : Shapiro, Wangfan Li, Manuel Delaflor, Carlos Toxtli. Framework d'architecture cognitive pour agents autonomes. ACE = nom du framework décrit dans le paper, pas le titre du paper. Approche **cognition-first** : imagination, réflexion, planification stratégique avant interaction avec l'environnement. Inspiré du modèle OSI pour les couches d'abstraction.

### Les 6 couches hiérarchiques

| Couche | Rôle |
|--------|------|
| **Aspirational** | Raisonnement moral, valeurs (Kohlberg) |
| **Global Strategy** | Planification haut niveau |
| **Agent Model** | Auto-modélisation |
| **Executive Function** | Gestion dynamique des tâches |
| **Cognitive Control** | Prise de décision |
| **Task Prosecution** | Exécution et embodiment |

Communication bidirectionnelle via 2 bus unidirectionnels : données capteurs vers le haut, directives vers le bas. **Toute communication inter-couches doit être lisible par un humain.**

### Principes fondamentaux
- **Cognition-first** : réflexion interne prioritaire sur les boucles input-output réactives
- **Moral reasoning** en couche supérieure (inspiré de Kohlberg — des stades obéissance → principes éthiques universels)
- **Corrigibilité, transparence, bénéfice** par design
- **100% open-source** (MIT license), local

### Applications visées
Chatbots, NPCs, véhicules autonomes, robots domestiques, employé digital, CEO digital, médecin digital.

## Position dans l'écosystème

ACE = framework théorique/conceptuel, pas un outil de production comme LangGraph ou CrewAI. Son influence est sur la **pensée architecturale** des agents : intégrer des couches morales et stratégiques plutôt que de simples boucles tool-use. Complémentaire aux frameworks d'exécution.

## Liens

- [[MOC-Leaders]]
- [[agents-architecture]] — Architecture agents, patterns
- [[harness-engineering]] — Agent = Modèle + Harness (même philosophie que ACE)
- [[Agents IA]] — Index principal agents
- [[Lilian Weng]] — Formule Agent = LLM + Memory + Planning + Tool Use (plus simple qu'ACE)
