---
titre: "Système de mémoire optimal — Codex ET ChatGPT (montage cross-tool)"
resume: "Doctrine canonique : règles versionnées, profil/projets/doctrine dans forge-brain, mémoire repo temporaire ou empirique, recall natif séparé."
aliases:
  - "memoire codex chatgpt"
  - "systeme memoire optimal openai"
  - "memoire cross-tool codex"
  - "ou ranger le savoir codex"
  - "agents.md vs memories vs skills"
derniere-maj: 2026-08-28
auteur: codex
type: technique
sources:
  - "https://learn.chatgpt.com/docs/customization/memories"
  - "https://learn.chatgpt.com/docs/hooks"
  - "https://help.openai.com/en/articles/6825453-chatgpt-release-notes"
  - "[[raisonnement-2026-08-28-profil-projets-vault-canoniques]]"
tags:
  - "#type/technique"
  - "#domaine/codex"
  - "#domaine/openai"
  - "#doctrine/2026"
---
# Système de mémoire optimal — Codex ET ChatGPT

> Canon au **28 août 2026**. La mémoire n'est pas un fichier unique : chaque
> couche a une autorité et un cycle de vie différents.

## Doctrine : trois couches, trois responsabilités

| Couche | Contenu | Autorité | Mutation |
|---|---|---|---|
| **Instructions** | conventions, commandes, règles de sécurité | `AGENTS.md`, adaptateur `CLAUDE.md`, skills | diff versionné + tests |
| **Connaissance contrôlée** | doctrine, décisions, projets stables, profil/casquettes de Raphaël | vault forge-brain | recherche avant écriture, enrichissement du foyer, provenance |
| **Contexte local** | adaptateurs, incidents empiriques, phases projet temporaires | `memory/` du repo | delta versionné, TTL pour le temporaire |
| **Recall natif** | souvenirs générés à partir des sessions | mémoire locale Codex ou mémoire ChatGPT | asynchrone, non autoritaire, jamais éditée comme source primaire |

Une préférence, une décision ou une correction importante ne doit pas vivre
uniquement dans le recall natif. Elle rejoint le foyer contrôlé adapté.

## Codex

- `AGENTS.md` porte le contrat commun durable.
- `.agents/skills/` porte des adaptateurs Codex minces vers les noyaux partagés.
- Les hooks servent à l'injection déterministe, au lint, à la sécurité et au
  scope ; ils ne décident pas seuls quoi apprendre ni quoi réécrire.
- La mémoire locale Codex est séparée de ChatGPT web et peut être différée.
- Son état sous `~/.codex/memories` reste en **shadow recall** : en cas de
  conflit, forge-brain, `AGENTS.md` et les documents versionnés tranchent.

## Claude Code

- `CLAUDE.md` reste un adaptateur court qui importe le contrat commun.
- `.claude/skills/` contient les noyaux de workflow partagés par ce repo.
- Le vault est consulté et modifié via MCP uniquement.
- Les hooks détectent des signaux de capitalisation ; ils ne modifient pas
  silencieusement le vault ou le profil.
- `/done` consolide les apprentissages explicites.
- `project-memory` crée le foyer d'un projet explicitement démarré et conserve
  ses choix durables.

## ChatGPT

La mémoire ChatGPT-app et la mémoire locale Codex sont deux systèmes distincts.
Les instructions personnalisées, Projects et souvenirs ChatGPT peuvent guider
les conversations, mais ne remplacent pas le contrat versionné ni le vault.

## Workflow vivant des nouveautés

`cc-news` sépare :

1. **Collecte** : sources primaires, dates, versions, provenance, budget borné.
2. **Application** : comparer au vault, corriger un foyer actif devenu faux,
   proposer un nouveau foyer si aucun n'existe, puis relire et journaliser.

Une correction remplace l'affirmation active obsolète sans effacer l'historique.
Une note nouvelle de veille reste proposée avant création. Un échec d'écriture
ne marque jamais la source comme traitée.

## Profil de Raphaël

Le foyer canonique est [[Raphael-Picard]], complété par les notes de casquettes.

- **Fait ou préférence explicite** : enrichir/corriger le foyer adapté, avec
  provenance concise.
- **Détail de casquette** : écrire dans la casquette ; garder seulement le résumé
  utile dans le profil central.
- **Hypothèse** : proposer, jamais promouvoir silencieusement.
- **Contexte temporaire** : ne pas persister dans le profil.
- **Donnée sensible nouvelle** : validation humaine obligatoire.
- **Adaptateur repo** : `memory/user_raphael_profile.md` pointe vers le vault et
  ne duplique aucune biographie.

## Projets et choix

Une demande explicite « crée/démarre le projet X » autorise la création d'un hub
sous `1-Projets/`. Une idée évoquée ne crée rien. Les choix actifs réversibles
restent dans le hub ; seules les décisions structurantes justifient une note
reliée sous `Knowledge/decisions/`. La phase en cours reste dans
`memory/project_*.md` avec expiration.

## Anti-patterns

- Mettre toute la mémoire dans `AGENTS.md`.
- Traiter le recall natif comme une base canonique.
- Éditer `~/.codex/memories` à la main pour piloter le système.
- Conserver deux biographies actives de Raphaël.
- Copier intégralement les skills Claude dans Codex et laisser les copies dériver.
- Créer une note pour chaque découverte sans rechercher un foyer existant.
- Créer un ADR pour chaque choix technique.
- Laisser un statut « à jour » après une écriture échouée.
- Déduire une préférence personnelle d'un seul comportement implicite.

## Wikilinks

- [[Raphael-Picard]]
- [[Claude-Forge]]
- [[raisonnement-2026-08-28-profil-projets-vault-canoniques]]
- [[workflow-codex-optimal]]
- [[agents-md-codex]]
- [[comment-creer-skill-codex]]
- [[loop-apprentissage-codex]]
- [[personnalisation-chatgpt-app]]
- [[pattern-maintenance-hybride-corpus-accumulatif]]
- [[methode-pivoter-doctrine]]
