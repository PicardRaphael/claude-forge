---
titre: "Pivot doctrinal — profil et projets canoniques dans forge-brain"
resume: "Le vault devient l'unique source active pour le profil durable de Raphaël, ses casquettes, ses projets stables et leurs décisions ; la mémoire repo devient adaptateur, incident empirique ou état temporaire."
aliases:
  - "pivot second cerveau 28 aout"
  - "profil Raphael vault canonique"
  - "projets vault canoniques"
  - "fin duplication profil memory vault"
  - "project memory doctrine"
type: raisonnement
derniere-maj: 2026-08-28
auteur: codex
sources:
  - "[[Raphael-Picard]]"
  - "[[Claude-Forge]]"
  - "[[memoire-optimale-codex-chatgpt]]"
  - "[[methode-pivoter-doctrine]]"
  - "demande explicite de Raphaël, session 2026-08-28"
tags:
  - "#type/raisonnement"
  - "#domaine/vault"
  - "#domaine/codex"
  - "#domaine/claude-code"
  - "#doctrine/2026"
---

# Pivot doctrinal — profil et projets canoniques dans forge-brain

## Constat

Le système entretenait deux biographies actives : [[Raphael-Picard]] dans le vault et `memory/user_raphael_profile.md` dans le repo. Les préférences récentes étaient écrites dans le second sans enrichir le premier. Le même décalage existait pour les projets : les foyers stables vivaient sous `1-Projets/`, mais aucun workflow ne garantissait leur création ni la capture des choix actés.

Ce doublonnage rendait les mises à jour invisibles selon l'outil et réactivait des états périmés après compaction ou rappel natif.

## Décision

1. [[Raphael-Picard]] est le foyer canonique du profil durable et du mode de collaboration de Raphaël.
2. Les détails propres à une responsabilité ou un domaine de vie enrichissent la casquette correspondante ; une nouvelle casquette n'apparaît que pour un domaine durable autonome.
3. `memory/user_raphael_profile.md` reste un adaptateur mince pour la compatibilité Claude/Codex. Il ne contient plus de biographie dupliquée.
4. Les projets stables vivent sous `1-Projets/`. Une demande explicite de création autorise un hub unique ; une idée simplement évoquée ne crée rien.
5. Les choix réversibles restent dans le hub. Une note sous `Knowledge/decisions/` n'est créée que pour une décision structurante avec alternatives, conséquences ou coût de retour.
6. `memory/project_*.md` porte uniquement une phase temporaire avec expiration.
7. Les mémoires natives Claude/Codex restent actives en shadow recall et cèdent devant le vault et les contrats versionnés.
8. Les hooks détectent des signaux déterministes mais ne décident ni n'écrivent sémantiquement ; la session principale reste l'unique writer du vault.
9. La parité de runtime n'est pas simulée : le détecteur `learning-reminder` reste un Stop hook Claude. Codex utilise les règles, skills et `memory-recall`, car son Stop ne supporte pas ce retour advisory sans forcer une continuation.

## Autorisation et vie privée

`/done`, « retiens/mémorise ceci » et « crée/démarre le projet X » autorisent les deltas non sensibles correspondant à leur demande. Une hypothèse personnelle, une nouvelle donnée sensible ou la suppression d'une note entière reste soumise à validation explicite.

## Foyers propagés

- `AGENTS.md` et l'adaptateur `CLAUDE.md`
- `.claude/rules/memory-discipline.md`
- `docs/second-brain/session-capture.md`
- `docs/second-brain/project-capture.md`
- skills `done`, `forge-brain` et `project-memory`
- adaptateurs Codex sous `.agents/skills/`
- détecteur `learning-reminder` Claude ; rappel `memory-recall` Codex
- [[memoire-optimale-codex-chatgpt]]
- [[loop-apprentissage-codex]]
- [[personnalisation-chatgpt-app]]
- [[Raphael-Picard]]
- [[Claude-Forge]]

## Condition de falsification

Si la lecture du profil vault devient mesurablement trop coûteuse ou rate des préférences pertinentes, améliorer le rappel ciblé ou l'adaptateur. Ne recréer une seconde biographie locale qu'après une comparaison mesurée prouvant qu'un pointeur mince ne suffit pas.
