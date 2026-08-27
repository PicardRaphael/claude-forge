---
titre: "Système de mémoire optimal — Codex ET ChatGPT (montage cross-tool)"
resume: "Doctrine canonique : règles versionnées, vault et profil contrôlés, recall natif séparé. Claude Code et Codex partagent les contrats, pas leurs états générés."
aliases:
  - "memoire codex chatgpt"
  - "systeme memoire optimal openai"
  - "memoire cross-tool codex"
  - "ou ranger le savoir codex"
  - "agents.md vs memories vs skills"
derniere-maj: 2026-08-27
auteur: codex
type: technique
sources:
  - "https://learn.chatgpt.com/docs/customization/memories"
  - "https://learn.chatgpt.com/docs/hooks"
  - "https://help.openai.com/en/articles/6825453-chatgpt-release-notes"
tags:
  - "#type/technique"
  - "#domaine/codex"
  - "#domaine/openai"
  - "#doctrine/2026"
---
# Système de mémoire optimal — Codex ET ChatGPT

> Canon au **27 août 2026**. La mémoire n'est pas un fichier unique : chaque couche a une autorité et un cycle de vie différents.

## Doctrine : trois couches, trois responsabilités

| Couche | Contenu | Autorité | Mutation |
|---|---|---|---|
| **Instructions** | conventions, commandes, règles de sécurité | `AGENTS.md`, adaptateur `CLAUDE.md`, skills | diff versionné + tests |
| **Connaissance contrôlée** | doctrine, décisions, faits corrigibles, profil explicite de Raphaël | vault forge-brain + `memory/` du repo | recherche avant écriture, enrichissement du foyer, provenance |
| **Recall natif** | souvenirs générés à partir des sessions | mémoire locale Codex ou mémoire ChatGPT | asynchrone, non autoritaire, jamais éditée comme source primaire |

Une préférence, une décision ou une correction importante ne doit pas vivre uniquement dans le recall natif. Elle doit être consolidée dans la couche contrôlée ou dans une règle versionnée.

## Codex

- `AGENTS.md` porte le contrat commun durable.
- `.agents/skills/` porte les procédures Codex, avec progressive disclosure.
- Les hooks servent à l'injection déterministe, au lint, à la sécurité et au scope ; ils ne décident pas seuls quoi apprendre ni quoi réécrire.
- La mémoire locale Codex est un magasin **séparé de ChatGPT web**, activé et contrôlé via `/memories`.
- Après activation, sa génération est en arrière-plan et peut être différée. Les sessions actives ou trop courtes peuvent être ignorées.
- L'état généré vit sous `~/.codex/memories`. OpenAI recommande de ne pas l'éditer à la main comme surface de contrôle principale.
- Cette mémoire reste donc en **shadow recall** : elle peut aider à rappeler, mais le vault, le profil versionné et `AGENTS.md` tranchent en cas de conflit.

## Claude Code

- `CLAUDE.md` reste un adaptateur court qui importe le contrat commun.
- `.claude/skills/` est la source canonique des workflows forge.
- Le vault est consulté via MCP uniquement.
- Les hooks détectent les signaux de capitalisation ; ils ne modifient pas silencieusement le vault ou le profil.
- `/done` consolide les apprentissages explicites et classifie : fait, préférence, correction, hypothèse, contexte temporaire.

## ChatGPT

La mémoire ChatGPT-app et la mémoire locale Codex sont deux systèmes distincts. Les instructions personnalisées, les Projects et les souvenirs ChatGPT peuvent guider les conversations, mais ne remplacent pas le contrat versionné du repo ni le vault.

## Workflow vivant des nouveautés

`cc-news` applique deux pipelines séparés :

1. **Collecte** : sources primaires, dates, versions, hash de provenance, budget borné.
2. **Application** : comparer au vault, corriger un foyer existant devenu faux, proposer un nouveau foyer si aucun n'existe, puis relire et journaliser.

Règles :

- une information volatile n'est jamais tenue pour actuelle sans vérification primaire ;
- une correction remplace l'affirmation obsolète, elle ne l'empile pas ;
- une note nouvelle est proposée avant création ;
- aucune note n'est supprimée automatiquement ;
- un échec d'écriture ne marque jamais la source comme traitée ;
- Claude et Codex partagent le contrat et l'état de fraîcheur, mais gardent des adaptateurs propres.

## Profil de Raphaël

Le foyer contrôlé est `memory/user_raphael_profile.md`.

- **Fait ou préférence explicite** : mise à jour autorisée, datée et sourcée.
- **Hypothèse** : proposée, jamais promue silencieusement.
- **Contexte temporaire** : non persisté.
- **Donnée sensible nouvelle** : validation humaine obligatoire.
- Toute correction de Raphaël remplace la valeur antérieure et conserve une provenance concise.

## Anti-patterns

- Mettre toute la mémoire dans `AGENTS.md`.
- Traiter le recall natif comme une base canonique.
- Éditer `~/.codex/memories` à la main pour piloter le système.
- Copier intégralement les skills Claude dans Codex et laisser les copies dériver.
- Créer une note pour chaque découverte sans rechercher un foyer existant.
- Laisser un statut « à jour » après une collecte réussie mais une écriture échouée.
- Déduire une préférence personnelle d'un seul comportement implicite.

## Wikilinks

- [[workflow-codex-optimal]]
- [[agents-md-codex]]
- [[comment-creer-skill-codex]]
- [[comment-creer-hook-codex]]
- [[loop-apprentissage-codex]]
- [[personnalisation-chatgpt-app]]
- [[pattern-vault-llm-karpathy]]
- [[methode-pivoter-doctrine]]
