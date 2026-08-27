---
titre: "MOC — OpenAI Codex"
resume: "Index du savoir Codex : configuration, skills, hooks, subagents, loops, mémoire contrôlée et arbitrage avec ChatGPT."
aliases:
  - "MOC Codex"
  - "index codex"
  - "codex doctrine"
  - "openai codex map"
  - "index openai codex"
type: index
derniere-maj: 2026-08-27
auteur: codex
sources:
  - "https://learn.chatgpt.com/docs/"
tags:
  - "#type/index"
  - "#domaine/codex"
---
# OpenAI Codex

> Index actionnable. Les versions, modèles, prix et disponibilités sont volatils : les vérifier dans les sources officielles avant de les citer ou d'en déduire une règle.

## Doctrine

- [[workflow-codex-optimal]] — carte générale et séquence de travail ; ses valeurs volatiles sont datées.
- [[agents-md-codex]] — instructions projet durables, nesting et taille combinée.
- [[config-toml-profils-codex]] — configuration machine/projet et profils.
- [[comment-creer-skill-codex]] — skills Codex et sidecar `agents/openai.yaml`.
- [[comment-creer-hook-codex]] — hooks, trust model et événements ; revérifier le catalogue officiel avant modification.
- [[subagents-cloud-codex]] — délégation, tâches cloud et automations.
- [[loops-codex]] — exécution non interactive et routines.
- [[loop-apprentissage-codex]] — recall natif en shadow + boucle contrôlée sessions vers propositions.
- [[memoire-optimale-codex-chatgpt]] — séparation instructions, connaissance contrôlée et recall natif.
- [[codex-vs-chatgpt-seul]] — arbitrage Codex/ChatGPT.

## Mémoire : règle courte

- `AGENTS.md` et les skills portent ce qui doit toujours s'appliquer.
- Le vault et le dossier `memory/` portent les connaissances contrôlées et corrigeables.
- La mémoire locale Codex est un recall généré en arrière-plan, distinct de ChatGPT web et non autoritaire.
- Les contrats de second cerveau sont partagés ; les adaptateurs Claude et Codex ne sont pas des copies byte-identiques.

## Fraîcheur

Pour toute question « quoi de neuf », utiliser `cc-news` :

1. vérifier les sources primaires OpenAI ;
2. comparer aux foyers existants ;
3. remplacer les affirmations devenues fausses ;
4. proposer les nouveaux foyers ;
5. relire les mutations et mettre à jour l'état de fraîcheur.

Une note datée reste un instantané historique. Elle ne doit pas être présentée comme l'état actuel sans vérification.

## ChatGPT

- [[personnalisation-chatgpt-app]] — instructions, Projects, mémoire et GPTs.
- La mémoire ChatGPT et la mémoire locale Codex sont séparées.

## Leaders et industrie

- [[Thibault Sottiaux]]
- [[Michael Bolin]]
- [[Fouad Matin]]
- [[Andrew Ambrosino]]
- [[Gabriel Peal]]
- [[Josh McKinney]]
- [[Shao-Qian Mah]]
- [[Simon Willison]]
- [[OpenAI Codex]]
- [[MOC-Outils-IA]]
- [[MOC-Claude-Code]]
- [[Agent Skills Spec]]
