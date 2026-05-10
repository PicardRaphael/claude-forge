---
titre: "PromptArmor — Défense contre l'injection de prompt"
resume: "ICLR 2026 : utiliser un LLM préprocesseur dédié (GPT-4o/4.1/o4-mini) pour détecter et neutraliser les injections de prompt, taux d'attaque < 1% sur AgentDojo"
aliases:
  - "PromptArmor"
  - "prompt armor"
  - "prompt injection defense LLM"
  - "arXiv 2507.15219"
  - "LLM preprocessor injection"
  - "defense prompt injection 2026"
domaine: technique
type: technique
derniere-maj: 2026-05-10
auteur: claude
sources:
  - "https://arxiv.org/abs/2507.15219"
tags:
  - "#type/technique"
  - "#domaine/agents"
  - "#domaine/securite"
---

## Description

Framework de défense contre les injections de prompt publié à ICLR 2026 (arXiv 2507.15219). Utilise un LLM **off-the-shelf** comme préprocesseur dédié pour détecter et neutraliser le contenu d'injection avant qu'il atteigne l'agent principal.

## Résultats (benchmark AgentDojo)

Avec GPT-4o, GPT-4.1 ou o4-mini comme préprocesseur :
- **Taux de faux positifs** < 1%
- **Taux de faux négatifs** < 1%
- **Taux de succès des attaques** : descend sous 1%

## Architecture

```
Input utilisateur/environnement
        ↓
┌─────────────────────┐
│   LLM Préprocesseur │  ← GPT-4o / o4-mini
│   (PromptArmor)     │  Détecte + neutralise injections
└─────────────────────┘
        ↓ contenu sanitisé
┌─────────────────────┐
│   Agent Principal   │
└─────────────────────┘
```

Le préprocesseur est **séparé** de l'agent. Il ne peut pas agir, seulement filtrer.

## Contexte : explosion des injections en production

Google a observé une **augmentation de 32%** des injections de prompt dans les pages web crawlées entre novembre 2025 et février 2026 (2-3 milliards de pages/mois crawlées).

### Patterns d'attaque courants en 2026

| Pattern | Description |
|---|---|
| Texte invisible | Taille 1px, couleur transparente, même fond |
| Commentaires HTML | `<!-- IGNORE PREVIOUS INSTRUCTIONS -->` |
| Metadata | Injections dans les attributs alt, title, meta |
| Instructions PayPal | Commandes cachées dans HTML invisible dans emails |

## Relation avec Dual-LLM Pattern

PromptArmor est une implémentation concrète du [[agents-securite#Pattern Dual-LLM|pattern Dual-LLM]] :
- Le préprocesseur = LLM quarantainé (lit le contenu non-fiable)
- L'agent principal = LLM privilégié (ne reçoit que le contenu sanitisé)

Différence clé : PromptArmor est **automatisé** et évalué sur benchmark, pas juste un pattern architectural.

## Quand utiliser

- Agents qui consomment du contenu web non-fiable (scraping, RAG sur web)
- Agents email ou traitement de documents externes
- Toute pipeline agent où l'input vient d'une source non-contrôlée

## Limites

- Coût additionnel : un LLM call supplémentaire par requête
- Le préprocesseur peut lui-même être attaqué (attaque méta-niveau)
- Efficace sur injections "dans le texte" — moins sur injections dans les structures de données

## Liens

- [[agents-securite]] — Sécurité agents, pattern Dual-LLM, OWASP agentic
- [[harness-engineering]] — Les contraintes déterministes dans le harness
- [[Context Engineering]] — Séparation trusted/untrusted dans la composition de contexte
- [[MOC-Techniques]]
