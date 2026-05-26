---
aliases:
  - conflit effort xhigh Anthropic
  - effort xhigh vs high doctrine
  - Will Applied AI effort default
  - pivot 22 mai effort réservé
  - doctrine effort Opus 4.7
resume: "Conflit doctrinal détecté 26 mai 2026 : Will (Anthropic Applied AI) dit xhigh par défaut Opus 4.7, notre pivot 22 mai dit xhigh réservé 3 rôles. Arbitrage Raphael requis."
derniere-maj: 2026-05-26
tags:
  - "#type/question"
  - "#domaine/claude-code"
  - "#statut/ouverte"
---

# Conflit effort xhigh — Anthropic Applied AI vs pivot forge 22 mai

## Contexte

Source découverte 26 mai 2026 : talk **Code with Claude London** par **Will** (Anthropic, équipe Applied AI), workshop "Agent Decomposition" sur agent Stock Pilot (62%→92% eval après modernisation tools/skills/sub-agents).

Verbatim Will à ~12min du talk pendant démo Claude Code live :

> "I have Opus 4.7 running as you can see on the screen. My effort level is set to **extra high**. I usually set effort as extra high with Opus 4.7 and I forget about it. That's the effort level that I usually stay on. We find that it gets great performance with extra high effort altogether."

## Conflit avec doctrine forge

Notre [[raisonnement-22mai-doctrine-vs-enforcement]] et `CLAUDE.md` ligne effort actuelle :

> "Effort : `high` partout par défaut. `xhigh` RÉSERVÉ aux 3 rôles : architect / dev-lead / refactor-pg. `max` toujours disponible mai 2026 mais prone overthinking — utiliser avec prudence."

## Tension réelle

- Will = source primaire Anthropic, post-pivot 22 mai (talk CwC London probablement mai 2026)
- Notre pivot = basé sur "xhigh prone overthinking" + observation Raphael
- Will dit l'inverse : xhigh par défaut, ça marche très bien

## Hypothèses non tranchées

1. **Will = use case spécifique** (debug agent complexe, tâche analyse multi-fichiers) → xhigh justifié dans CE contexte, pas universellement
2. **Notre observation overthinking était bruit** → s'aligner sur Anthropic
3. **Différence entre Claude Code (Will) et tâches simples (notre cas)** → contexte-dépendant : xhigh sur Claude Code dev, high sur reste
4. **Will simplifie pour l'audience** → "I forget about it" = anti-pattern, pas best practice

## Décision en attente

Arbitrage Raphael requis. Options :
- **A** : garder pivot 22 mai (high par défaut, xhigh réservé) — notre vécu prime
- **B** : s'aligner Anthropic (xhigh par défaut) — source primaire prime
- **C** : nuancer (xhigh par défaut sur Claude Code dev, high partout ailleurs)

## À faire avant décision

- [ ] Re-test xhigh sur 3 tâches forge récentes pour vérifier "overthinking" observation
- [ ] Vérifier date du talk Will (mai 2026 vs antérieur) — si antérieur au pivot 22 mai, contexte modèle différent
- [ ] Chercher d'autres sources Anthropic post-22 mai sur effort default

## Liens

- [[raisonnement-22mai-doctrine-vs-enforcement]] — pivot qui définit la doctrine actuelle
- [[workflow-claude-code-optimal]] — note canonique workflow où vit la règle effort
- [[methode-pivoter-doctrine]] — méthode si on décide de pivoter (option B ou C)
