---
titre: "Loop d'apprentissage Codex — compounding contrôlé"
resume: "Doctrine Codex : recall natif en arrière-plan, vault canonique pour profil et projets, règles versionnées et boucle sessions vers propositions vérifiées."
aliases:
  - "loop apprentissage codex"
  - "compounding codex"
  - "codex memories"
  - "scan sessions update skills"
  - "amelioration continue codex"
  - "codex auto memory"
derniere-maj: 2026-08-28
auteur: codex
type: technique
sources:
  - "https://learn.chatgpt.com/docs/customization/memories"
  - "https://learn.chatgpt.com/docs/automations"
  - "https://learn.chatgpt.com/docs/hooks"
tags:
  - "#type/technique"
  - "#domaine/codex"
  - "#domaine/workflow"
  - "#doctrine/2026"
---
# Loop d'apprentissage Codex — compounding contrôlé

> Canon au **28 août 2026**. Le compounding fiable ne consiste pas à laisser une mémoire générée réécrire les règles : il sépare recall, détection, validation et consolidation.

## Les trois briques

### 1. Recall natif local

Codex peut générer des souvenirs locaux à partir de sessions antérieures afin de rappeler du contexte utile.

- activation et contrôle via `/memories` ;
- génération en arrière-plan, donc potentiellement différée ;
- sessions actives ou trop courtes susceptibles d'être ignorées ;
- secrets retirés des champs générés ;
- état sous `~/.codex/memories` ;
- état généré, à ne pas éditer comme surface de contrôle principale ;
- magasin distinct de la mémoire ChatGPT web.

Ce recall est **consultatif**. Une règle qui doit toujours s'appliquer vit dans `AGENTS.md` ou une skill ; une connaissance corrigeable, un profil durable ou un projet stable vit dans forge-brain. La mémoire repo sert d'adaptateur, d'incident empirique précis ou d'état projet à durée courte.

### 2. Compétences versionnées

Les procédures reproductibles vivent dans `.agents/skills/`. Dans forge, les contrats de fond sont partagés sous `docs/second-brain/` et les adaptateurs Claude/Codex restent spécifiques à leur runtime.

Une session ne modifie une skill que si elle révèle une procédure récurrente et vérifiable, pas pour une préférence ponctuelle.

### 3. Boucle sessions vers amélioration

Une routine planifiée peut analyser les sessions récentes et détecter :

- erreurs récurrentes ;
- instructions répétées par Raphaël ;
- documentation devenue fausse ;
- friction d'une skill ;
- nouveau fait stable sur un outil.

La sortie correcte est d'abord une **proposition bornée**, avec preuve et foyer cible. L'application vient ensuite, avec diff, test et relecture.

## Cycle de référence

```text
sessions et sources primaires
        |
        v
détection + classification
        |
        v
proposition avec preuve et cible
        |
        v
validation humaine ou autorisation explicite
        |
        +--> AGENTS.md / skill : règle durable
        +--> vault : doctrine ou fait sourcé
        +--> Raphael-Picard / casquette : fait ou préférence explicite
        +--> 1-Projets/ + Knowledge/decisions : projet et choix durables
        +--> memory/project_*.md : phase temporaire avec expiration
        +--> rien : contexte temporaire ou hypothèse faible
        |
        v
tests + journal + état de fraîcheur
```

## Invariants

- Collecter une source et écrire une correction sont deux transactions distinctes.
- Une écriture échouée ne fait pas avancer l'état de fraîcheur.
- On enrichit un foyer existant avant de créer une note.
- Une information fausse est remplacée ; elle n'est pas simplement contredite plus bas.
- Une note nouvelle est proposée avant création, sauf foyer projet explicitement demandé.
- Aucune suppression de note vault n'est automatique.
- Un hook peut détecter ou injecter du contexte ; il ne décide pas seul d'une mutation sémantique.
- Le recall natif reste en shadow pendant les migrations et ne devient jamais la seule source de vérité.
- Le profil de Raphaël distingue fait explicite, préférence explicite, hypothèse et contexte temporaire.
- Une idée informelle ne crée pas un projet ; une demande explicite crée ou enrichit un hub unique.

## Workflow forge

- **Actualité** : `cc-news` collecte en sources primaires, compare au vault, corrige les foyers existants et propose les nouveaux.
- **Fin de session** : `done` consolide les décisions, corrections et signaux personnels explicites dans leurs foyers vault.
- **Projet** : `project-memory` crée/enrichit le hub explicite et classe les choix.
- **Recall Codex** : `memory-recall` injecte les foyers contrôlés au début du travail.
- **Détecteur Claude** : `learning-reminder` signale au Stop ce qui semble non capitalisé. Il n'est pas porté sur le Stop Codex : `additionalContext` n'y est pas supporté et `decision:"block"` y force la continuation.
- **État** : `.claude/skills/cc-news/references/freshness-state.json` conserve la date, la version et les hashes utiles.

## Anti-patterns

- Confondre recall natif et doctrine.
- Modifier directement `~/.codex/memories`.
- Scanner toutes les sessions sans budget ni fenêtre temporelle.
- Réécrire une skill entière à partir d'un seul incident.
- Faire écrire le même hook dans le vault et le profil.
- Simuler la parité Claude/Codex avec un champ de hook non supporté.
- Marquer une nouveauté traitée avant vérification de la mutation.
- Persister une donnée personnelle sensible ou une hypothèse sans validation.

## Wikilinks

- [[memoire-optimale-codex-chatgpt]]
- [[workflow-codex-optimal]]
- [[loops-codex]]
- [[comment-creer-skill-codex]]
- [[agents-md-codex]]
- [[comment-creer-hook-codex]]
- [[Raphael-Picard]]
- [[pattern-vault-llm-karpathy]]
