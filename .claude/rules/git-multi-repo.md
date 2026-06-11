---
description: Jamais cd <path> && git dans un contexte multi-repo — le CWD persiste entre Bash calls. TOUJOURS git -C <chemin-absolu>.
---

# Git multi-repo — Convention CWD

## Règle absolue

```bash
# CORRECT
git -C C:/Users/raphael.picard_neote/Documents/claude-forge status
git -C C:/Users/raphael.picard_neote/Documents/neot-v2/ia_back log --oneline -5

# FAUX — CWD persiste, le 2e git cible toujours ia_back
cd C:/Users/raphael.picard_neote/Documents/neot-v2/ia_back && git status
git log --oneline -5
```

## Chemins des repos

| Alias | Chemin absolu |
|-------|--------------|
| forge | `C:/Users/raphael.picard_neote/Documents/claude-forge` |
| ia_back | `C:/Users/raphael.picard_neote/Documents/neot-v2/ia_back` |
| neo_ia | `C:/Users/raphael.picard_neote/Documents/neot-v2/neo_ia` |
| lojii | `C:/Users/raphael.picard_neote/Documents/neofront` |
| neoteem-brain | `C:/Users/raphael.picard_neote/Documents/neot-v2/neoteem-brain` |

## Pratiques

- **Paralléliser** les `git read-only` (status, log, diff) en 1 Bash call via `&&`
- **Séquencer** les `git write` (add, commit, push) — jamais en parallel sur le même repo (race sur l'index)
- **Quoter** les chemins avec espaces : `git -C "C:/path with spaces/repo"`
- **Confirmer** le repo ciblé après batch : `git -C <repo> log --oneline -1`
- **Forward slashes** uniquement — backslashes moins robustes

## Gotchas

- CWD persiste entre Bash calls — `cd` dans un call affecte TOUS les appels suivants de la session
- Ne pas paralleliser `git commit` sur le même repo — race condition sur l'index
- Vérifier le repo cible après toute opération cross-repo

Source : `memory/feedback_git_C_pas_cd_multi_repo.md`
