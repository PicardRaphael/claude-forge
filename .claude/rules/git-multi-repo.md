---
description: Jamais cd <path> && git dans un contexte multi-repo — le CWD persiste entre Bash calls. TOUJOURS git -C <chemin-absolu>.
---

# Git multi-repo — Convention CWD

## Règle absolue

```bash
# CORRECT — git -C <chemin résolu>, jamais cd
git -C "$FORGE" status
git -C "$IA_BACK" log --oneline -5

# FAUX — CWD persiste, le 2e git cible toujours ia_back
cd "$IA_BACK" && git status
git log --oneline -5
```

## Chemins des repos — RÉSOUDRE, jamais recopier

⚠️ **Machines multiples** : Raphael travaille sur 2 PC avec des noms d'utilisateur et des arborescences différents, et tous les repos ne sont pas présents partout. Un chemin absolu écrit en dur ici est **faux sur l'autre machine** et échoue silencieusement (j'improvise, ou je conclus à tort que le repo n'existe pas).

**Résoudre en début de tâche multi-repo**, puis réutiliser les variables :

```bash
FORGE="$(git rev-parse --show-toplevel)"          # depuis une session forge
DOCS="$(dirname "$FORGE")"                         # dossier parent des repos
for r in "$DOCS"/neot-v2/ia_back "$DOCS"/neot-v2/neo_ia \
         "$DOCS"/neot-v2/neoteem-brain "$DOCS"/neofront; do
  [ -d "$r/.git" ] && echo "PRESENT $r" || echo "ABSENT  $r"
done
```

| Alias | Emplacement relatif au parent de forge | Note |
|-------|----------------------------------------|------|
| forge | `claude-forge` | `git rev-parse --show-toplevel` |
| ia_back | `neot-v2/ia_back` | repo git |
| neo_ia | `neot-v2/neo_ia` | repo git |
| neoteem-brain | `neot-v2/neoteem-brain` | repo git |
| lojii / neofront | `neofront/<sous-repo>` | ⚠️ **PAS un repo** — dossier conteneur (vérifié 29 juil. 2026). Chaque sous-dossier est un repo git indépendant : `admin_client`, `ag`, `back-office`, `budget-syndic`, `chatbot`, `banque`, `bibliotheque_composants`, `administration-extranet`, `administrations-neoteem`, `balance-globale`… `git -C .../neofront` **échoue** : cibler le sous-repo précis. Lister : `ls -d "$DOCS"/neofront/*/.git`. |

**Repo ABSENT = cas normal, pas une erreur** : annoncer le skip explicitement à Raphael (« ia_back absent sur cette machine, non audité »), jamais l'ignorer en silence ni improviser un chemin. Cf `memory/feedback_localiser_repos_avant_workflow_multi_repo.md` (localiser empiriquement avant tout fan-out).

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

Source : `memory/feedback_git_C_pas_cd.md`
