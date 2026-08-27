---
name: done
description: ALWAYS invoke when Raphaël types /done, asks to finish/capitalise a session, or explicitly asks to remember what was learned. Updates existing memory, vault context, and Raphaël's profile; proposes hypotheses and new notes in one batch. NOT for recalling prior context at session start (recap).
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, mcp__forge-brain__*
---

# done — capitalisation de session

Lire entièrement `docs/second-brain/session-capture.md` et
`.claude/rules/memory-discipline.md` avant d'écrire. La conversation courante
est la source ; ne pas chercher un transcript externe.

## 1. Extraire sans inventer

Produire des candidats seulement pour :

- décisions et pivots réellement actés ;
- faits techniques vérifiés ;
- corrections ou erreurs qui éviteraient une récidive ;
- faits personnels et préférences explicitement formulés par Raphaël ;
- contexte de projet réellement changé.

Écarter le banal, l'historique Git, les recettes déjà visibles dans le code, les
versions volatiles et toute généralisation tirée d'un seul signal ambigu.

## 2. Router chaque candidat

| Candidat | Foyer |
|---|---|
| fait/préférence explicite durable sur Raphaël | `memory/user_raphael_profile.md` |
| hypothèse sur Raphaël | batch `À confirmer`, aucune écriture |
| donnée sensible | aucune, sauf « mémorise ceci » explicite |
| feedback relationnel ou incident précis | `memory/feedback_*.md` existant, sinon proposition |
| savoir technique réutilisable | canonique vault existante, sinon proposition de note |
| décision structurante | ADR vault existante ou proposition |
| contexte projet stable | `vault/1-Projets/` via MCP |
| phase temporaire | `memory/project_*.md` |

Avant une création : chercher le concept seul dans forge-brain et scanner
`memory/`. Enrichir le foyer existant ; ne jamais créer un doublon.

## 3. Capacités accordées par `/done`

L'invocation explicite autorise :

- `profile-apply` pour un fait ou une préférence explicite, durable et non
  sensible ;
- `repo-apply` pour corriger/enrichir un fichier mémoire existant ;
- `vault-apply` pour enrichir une note ou un contexte existant via MCP.

Restent proposés dans un batch unique : nouvelle note vault, nouveau fichier
mémoire, hypothèse personnelle et donnée sensible. Une suppression demande une
autorisation explicite séparée.

## 4. Appliquer des deltas minimaux

### Profil Raphaël

Relire `memory/user_raphael_profile.md`. Corriger ou enrichir la bonne puce au
lieu d'ajouter un journal de conversation. Ajouter une provenance courte sous
`## Provenance des mises à jour` : date, prédicat, `explicit` ou `confirmed`.
Une préférence plus récente contradictoire remplace l'ancienne formulation.

### Mémoire repo

Conserver `MEMORY.md` comme index court. Mettre à jour le fichier existant et
son pointeur ; une doctrine appartient au vault, pas à un feedback verbeux.

### Vault

Utiliser exclusivement MCP forge-brain. Lire la note entière, capturer la
préimage, relire avant mutation, écrire le delta dans le bon foyer, mettre
`derniere-maj`, puis relire. Ne jamais écrire le vault par le filesystem.

### Contexte

Mettre à jour `context-actuel` et les notes des projets substantiellement
touchés. Ne rien écrire pour une session purement exploratoire sans changement.

## 5. Vérifier et rapporter

Relire chaque cible, vérifier doublons et contradictions, puis rendre :

```markdown
## Session done — YYYY-MM-DD

### Appliqué
- [cible] — [delta]

### À valider en batch
- [type + cible + contenu court]

### Ignoré
- [candidat] — [raison]

### Conflits ou révocations
- [élément] — [action]
```

« Rien à capitaliser » est valide. Ne jamais créer de matière pour remplir le
rapport.

## Near misses

- Reprendre le contexte en début de session → `recap`.
- Sauvegarder un raisonnement complexe précis → `reasoning-cache`.
- Nettoyer les doublons/dormants du corpus → `clean-memory`.
