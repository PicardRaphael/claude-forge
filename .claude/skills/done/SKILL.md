---
name: done
description: ALWAYS invoke when Raphaël types /done, asks to finish/capitalise a session, or explicitly asks to remember what was learned. Consolidates profile, projects, decisions, knowledge and temporary context. NOT for session recall (recap).
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, mcp__forge-brain__search_brain, mcp__forge-brain__read_note, mcp__forge-brain__read_note_by_path, mcp__forge-brain__read_section, mcp__forge-brain__list_notes
---

# done — capitalisation de session

Lire entièrement `docs/second-brain/session-capture.md` et
`.claude/rules/memory-discipline.md`. Lire aussi
`docs/second-brain/project-capture.md` si un projet ou un choix a changé. La
conversation courante est la source ; ne pas chercher un transcript externe.

## 1. Extraire sans inventer

Retenir seulement : décisions réellement actées, faits techniques vérifiés,
corrections utiles, faits/préférences explicitement formulés par Raphaël et
contexte projet réellement changé. Écarter le banal, les recettes visibles dans
le code, les versions volatiles non vérifiées et les généralisations ambiguës.

## 2. Router

| Candidat | Foyer |
|---|---|
| identité, objectif ou préférence personnelle durable | `Raphael-Picard` |
| détail propre à un domaine de vie/responsabilité | casquette existante |
| hypothèse sur Raphaël | batch `À confirmer`, aucune écriture |
| donnée sensible | aucune sans « mémorise ceci » explicite |
| feedback relationnel ou incident précis | `memory/feedback_*.md` existant, sinon nouveau si non couvert |
| savoir technique réutilisable | canonique vault existante, sinon note autonome si justifiée |
| contexte projet stable | foyer sous `1-Projets/` |
| choix projet réversible | section `Choix actifs` du foyer projet |
| décision structurante | note `Knowledge/decisions/` reliée au projet |
| phase temporaire | `memory/project_*.md` avec expiration |

Avant toute création, chercher le concept seul et lire les foyers candidats.
Enrichir avant de créer. Une nouvelle note personnelle exige un domaine durable
autonome ; une nouvelle décision exige les critères du contrat projet.

## 3. Autorisation

L'invocation explicite autorise les deltas non sensibles dans les foyers
existants et la création d'un foyer clairement requis par les faits explicites
de la session. Une suppression de note entière, une hypothèse et une nouvelle
donnée sensible restent soumises à validation.

## 4. Appliquer

### Profil et casquettes

Lire `Raphael-Picard`, puis la casquette pertinente. Corriger/enrichir la bonne
section et mettre `derniere-maj`. Garder une provenance concise dans la note
concernée. Ne pas recopier le contenu dans `memory/user_raphael_profile.md` : ce
fichier reste un adaptateur.

### Projet et décisions

Appliquer `docs/second-brain/project-capture.md`. Si la session a explicitement
créé un projet sans foyer, le créer. Relier les décisions structurantes au foyer
et garder l'état temporaire hors du vault.

### Mémoire repo

Conserver `memory/MEMORY.md` comme index court. Les feedbacks portent uniquement
un incident empirique non absorbable par la doctrine du vault.

### Vault

Utiliser exclusivement MCP forge-brain. Lire la cible entière, capturer la
préimage, appliquer le delta minimal, mettre `derniere-maj`, puis relire. La
session principale reste l'unique writer.

## 5. Vérifier et rendre

Relire chaque cible et vérifier doublons, contradictions, liens et ancienne
valeur remplacée. Rendre :

```markdown
## Session done — YYYY-MM-DD

### Appliqué
- [cible] — [delta]

### À confirmer
- [hypothèse ou donnée sensible]

### Ignoré
- [candidat] — [raison]

### Révoqué ou remplacé
- [élément] — [nouvel état]
```

« Rien à capitaliser » est valide.

## Gotchas

- Une préférence de projet n'est pas automatiquement une préférence globale.
- Un vault write quelconque ne prouve pas que le profil a été mis à jour :
  relire la cible exacte.
- Une décision remplacée garde sa trace et pointe vers la nouvelle.
- Ne pas créer une note pour remplir le rapport.

## Near misses

- Reprendre le contexte → `recap`.
- Créer/démarrer un projet pendant la session → `project-memory`.
- Sauvegarder un raisonnement complexe → `reasoning-cache`.
- Nettoyer doublons/dormants → `clean-memory`.

## Apprentissage

Si un routage échoue de façon répétée, corriger le contrat partagé avant
d'ajouter une exception locale.
