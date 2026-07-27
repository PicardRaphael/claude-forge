---
description: "Vérification empirique obligatoire après tout dispatch d'un sub-agent qui clame avoir créé/modifié/supprimé des fichiers — ne jamais relayer le résumé sans grep/ls/diff"
---

# Vérification empirique post-dispatch — OBLIGATOIRE

Les sub-agents retournent « done » même en cas d'échec silencieux (Write denied retourne exit 0 côté Bash mais le fichier n'existe pas). La session principale DOIT vérifier empiriquement avant de relayer un résultat à Raphael.

## Checklist post-dispatch (4 points)

1. **Fichiers existent ?** — `ls -la <chemin attendu>` ou `Glob .claude/skills/<nom>/**`
2. **Contenu conforme ?** — `head -20 <fichier>` (frontmatter complet ?)
3. **Git diff confirme ?** — `git -C <repo> diff --stat` + `git -C <repo> status --short` (résoudre `<repo>` via `git rev-parse --show-toplevel`, jamais de path en dur OS-spécifique)
4. **Taille réaliste ?** — `wc -l <fichier>` (SKILL.md < 5 lignes = échec silencieux)

## Par type d'agent

| Agent | Vérifier |
|---|---|
| skill-creator | `ls .claude/skills/<nom>/SKILL.md` + `wc -l > 20` |
| subagent-creator | `ls .claude/agents/<nom>.md` + frontmatter complet |
| hook-creator | `ls .claude/hooks/<nom>.py` + `grep exit 2` |
| claudemd-creator | `wc -l CLAUDE.md` + diff avant/après |
| tout agent | `git diff --stat` pour confirmer les fichiers touchés |

## Anti-patterns

- « Le sub-agent a dit done » → non. exit 0 ≠ succès. Vérifier empiriquement.
- Relayer le résumé sub-agent sans grep/ls → régression silencieuse.
- « Je vois le résultat dans la conversation » → le sub-agent peut avoir affiché le PRÉVU sans avoir écrit.
- Skipper la vérif sur agents « fiables » → tous échouent silencieusement sur Write denied.
- Relayer un finding d'AUDIT sans Read direct du fichier incriminé → un agent peut lire une liste YAML multi-lignes (`tools:` suivi de `- Read`) comme « champ vide » et rapporter un CRITIQUE faux (audit neo_ia 27 juil. : 2 faux positifs frontmatter). Contre-vérifier chaque finding bloquant par Read avant de le relayer ou d'agir.

## Gotchas

- Exit 0 ≠ succès : Write denied retourne exit 0 côté Bash mais le fichier n'existe pas.
- Contenu affiché ≠ contenu écrit : le sub-agent peut générer le contenu dans son output sans avoir pu le Write.
- Glob sans résultat = fichier absent (ne pas interpréter comme un bug Glob).
- `git diff` vide après agent : soit rien fait, soit changements non stagés — vérifier les deux.
- Nouvel anti-pattern de sub-agent découvert → l'ajouter dans la section Anti-patterns.
