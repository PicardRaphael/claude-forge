---
name: git-multi-repo
description: ALWAYS invoke when running git across multiple repos (forge + ia_back + neo_ia + lojii). DO NOT use cd <path> && git -- CWD persists between Bash calls and silently targets the wrong repo. Use git -C <path> exclusively.
allowed-tools: Bash
effort: high
user-invokable: true
---

## Role

Garantir que chaque commande git cible le bon repo dans un contexte multi-repo (forge, ia_back, neo_ia, lojii). Le CWD persiste entre les Bash calls -- cd repo && git cible le mauvais repo silencieusement.

## Pattern canonique

Correct:
  git -C C:/Users/raphael.picard_neote/Documents/claude-forge status
  git -C C:/Users/raphael.picard_neote/Documents/ia_back log --oneline -5

Faux (CWD persiste):
  cd C:/Users/raphael.picard_neote/Documents/ia_back && git status
  git log --oneline -5   # toujours dans ia_back apres cd

## Chemins des repos

| Alias  | Chemin absolu |
|--------|--------------|
| forge  | C:/Users/raphael.picard_neote/Documents/claude-forge |
| ia_back | C:/Users/raphael.picard_neote/Documents/ia_back |
| neo_ia | C:/Users/raphael.picard_neote/Documents/neot-v2 |
| lojii  | C:/Users/raphael.picard_neote/Documents/lojii |

## Etapes

1. Identifier les repos concernes
2. Pour chaque repo : git -C "<chemin absolu>" <commande>
3. Paralleliser les git read-only (status, log, diff) en 1 Bash call
4. Sequencer les git write (add, commit, push) par repo

## Gotchas

- CWD persiste entre Bash calls : cd dans un call modifie le CWD pour TOUS les appels suivants
- Backslashes Windows : preferer les forward slashes C:/Users/... -- plus robuste
- Ne PAS paralleliser git commit sur le meme repo -- race condition sur l index
- Toujours quoter les chemins avec espaces : git -C "C:/path with spaces/repo"
- Apres batch git : git -C <repo> log --oneline -1 pour confirmer le repo cible

## Exemples

  git -C C:/Users/raphael.picard_neote/Documents/claude-forge status --short
  git -C C:/Users/raphael.picard_neote/Documents/ia_back status --short
  git -C C:/Users/raphael.picard_neote/Documents/neot-v2 status --short

## Apprentissage

Feedback source : feedback_git_C_pas_cd_multi_repo.md
Valide lors d operations cross-repo forge/ia_back/neo_ia.
Si nouveau pattern multi-repo decouvert en session, stocker en memoire projet.
