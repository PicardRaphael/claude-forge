---
description: "Route durable knowledge to forge-brain and keep repo memory limited to adapters, empirical incidents, and temporary project state"
---

# Discipline du second cerveau

## Autorités

| Information | Foyer canonique |
|---|---|
| identité, objectifs et préférences durables de Raphaël | `Raphael-Picard` dans forge-brain |
| responsabilité ou domaine de vie durable | casquette existante sous `2-Casquettes/` |
| connaissance, doctrine et erreur généralisable | note canonique forge-brain |
| contexte stable d'un projet | foyer sous `1-Projets/` |
| décision structurante | note sous `Knowledge/decisions/`, reliée au projet |
| incident empirique précis | `memory/feedback_*.md` |
| phase temporaire d'un projet | `memory/project_*.md` avec date d'expiration |
| rappel natif Claude/Codex | shadow recall, jamais autoritaire |

`memory/user_raphael_profile.md` est un adaptateur vers `Raphael-Picard`, pas un
foyer concurrent. Ne jamais y recopier la biographie ou les préférences.

## Rappel au début d'une tâche

Utiliser `memory/MEMORY.md` comme index et lire seulement les feedbacks ou états
temporaires dont le déclencheur correspond à la tâche. Les anciens
`memory/reference_*.md` restent consultables, mais toute nouvelle connaissance
réutilisable rejoint le vault. Ne pas charger le corpus mémoire en bloc.

## Avant d'écrire

1. Chercher le concept seul dans forge-brain.
2. Lire entièrement les foyers candidats.
3. Enrichir le foyer qui couvre déjà le sujet.
4. Créer uniquement si aucun foyer n'est adapté et si le sujet mérite une note
   autonome ; un fait isolé n'entraîne pas une nouvelle note.

Une information peut enrichir plusieurs notes seulement si chaque delta relève
réellement de leur responsabilité : par exemple le profil principal et une
casquette métier. Ne pas recopier le même paragraphe dans plusieurs foyers.

## Profil Raphaël

Lire `docs/second-brain/session-capture.md` avant toute mutation.

| Signal | Action |
|---|---|
| fait ou préférence explicite, durable, non sensible | corriger/enrichir `Raphael-Picard` ou la casquette adaptée |
| hypothèse ou interprétation | proposer sous « À confirmer » |
| préférence limitée à un projet | foyer du projet, pas le profil global |
| santé, finance, secret, localisation précise, nouvelle donnée familiale | ne pas écrire sans « mémorise ceci » |

Une occurrence explicite suffit pour un fait sur soi. Une correction remplace
l'état actif ; elle ne s'empile pas comme un addendum. Conserver une provenance
courte, sans extrait intime du chat.

## Projets

Lire `docs/second-brain/project-capture.md` et charger `project-memory` quand
Raphaël demande explicitement de créer/démarrer un projet ou de conserver ses
choix. Le foyer projet porte le stable ; `memory/project_*.md` ne porte que la
phase active et doit annoncer son expiration.

## Fin de session

`/done` est le writer de consolidation. Il peut enrichir les foyers existants et
créer un foyer non sensible clairement autorisé par la conversation. Les hooks
peuvent seulement détecter des signaux déterministes et rappeler `/done` ; ils
ne choisissent jamais ce qu'il faut apprendre.

## Anti-patterns

- Créer une note par message ou par fait.
- Dupliquer une doctrine du vault dans `memory/`.
- Garder un choix projet uniquement dans un transcript ou le recall natif.
- Transformer une hypothèse sur Raphaël en fait.
- Conserver du contexte stable dans un fichier projet temporaire.
- Marquer une source « à jour » après une écriture échouée.
