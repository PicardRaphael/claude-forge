---
name: auditor-empirical-verify
description: ALWAYS invoke after a sub-agent or a creator skill reports having created, modified or deleted files. Runs the post-dispatch checklist — files exist, content conforms, diff confirms, size is realistic, no stray commit. DO NOT relay a sub-agent summary without invoking first. NOT for judging code quality (code-dev) or auditing a config (repo-inspector).
allowed-tools: Read, Glob, Grep, Bash
user-invocable: true
effort: high
---

# auditor-empirical-verify

Checklist de vérification empirique après un dispatch. Un sous-agent qui rend
« done » a pu échouer silencieusement — vérifier avant de relayer son résumé.

## Ce qui rend la vérification nécessaire

Un `exit 0` ne prouve rien. Un Write refusé rend la main sans erreur visible, et
le sous-agent affiche alors le contenu qu'il *comptait* écrire : la conversation
montre un livrable qui n'existe nulle part sur le disque. Aucune de ces défaillances
ne produit de message d'erreur. Seul le disque et le diff font foi.

Résoudre la racine du repo dans un bloc shell avec `$(git rev-parse --show-toplevel)`.
Ne jamais écrire de chemin absolu commençant par un nom d'utilisateur — Raphaël
travaille sur deux machines aux arborescences différentes, et un tel chemin échoue
silencieusement sur l'autre.

## Checklist post-dispatch (5 points)

```bash
REPO="$(git rev-parse --show-toplevel)"
```

1. **Le fichier existe.** `ls -la "$REPO/.claude/skills/<nom>/SKILL.md"` ou un
   `Glob` sur le motif attendu. Aucun résultat = fichier absent, pas un bug de Glob.
2. **Le contenu est conforme.** Lire les 20 premières lignes — frontmatter complet,
   `name` égal au dossier, description sur une seule ligne.
3. **Le diff confirme.** `git -C "$REPO" status --short` et `git -C "$REPO" diff --stat`.
   Un diff vide signifie soit rien fait, soit changements déjà stagés — regarder les deux.
4. **La taille est réaliste.** `wc -l` sur le livrable. Un `SKILL.md` de 5 lignes ou
   un hook sans `exit 2` est un échec silencieux, pas une livraison minimaliste.
5. **Aucun commit parasite.** `git -C "$REPO" log --oneline -3`. Les sous-agents
   committent malgré une consigne contraire placée en fin de prompt ; le vérifier
   coûte une commande et évite un commit de nettoyage séparé.

## Ce qu'on vérifie selon le dispatch

| Dispatch | Vérifier |
|---|---|
| `skill-creator` | `.claude/skills/<nom>/SKILL.md` existe, > 20 lignes, frontmatter parsable |
| `subagent-creator` | `.claude/agents/<nom>.md` existe, `tools` explicite, description une ligne |
| `hook-creator` | `.claude/hooks/<nom>.py` existe, contient `exit 2`, branché dans `settings.json` |
| `claudemd-creator` | diff avant/après sur le fichier ciblé, taille toujours sous la limite |
| `code-dev` | diff attendu, suite de tests relancée |
| `repo-inspector`, `devils-advocate`, `outcomes-grader` | read-only — un diff non vide est l'anomalie |
| tout dispatch | `git status --short` et `git log --oneline -3` |

Les trois agents read-only méritent l'inversion du test : chez eux, c'est la
présence d'un changement qui signale le problème.

## Anti-patterns

- « L'agent a dit done » — `exit 0` n'est pas un succès. Vérifier sur le disque.
- Relayer le résumé du sous-agent sans `ls` ni `diff` — c'est ainsi qu'une
  régression passe pour une livraison.
- « Je vois le résultat dans la conversation » — le contenu affiché peut n'avoir
  jamais été écrit.
- Sauter la vérification sur un agent réputé fiable — l'échec est silencieux,
  donc indépendant de la qualité de l'agent.
- Vérifier seulement ce que l'agent annonce avoir touché — comparer aussi à ce
  qui était demandé, sans quoi un livrable dilué passe inaperçu.

## Gotchas

- **Write refusé rend `exit 0`** côté Bash : le code de retour ne distingue pas
  le refus de la réussite.
- **Contenu affiché ≠ contenu écrit** : un sous-agent peut générer un fichier
  entier dans sa sortie sans avoir obtenu le droit de l'écrire.
- **Glob sans résultat = fichier absent** : ne pas conclure à un problème d'outil.
- **Diff vide après un agent** : rien fait, ou déjà stagé. Vérifier les deux.
- **Cross-repo** : passer par `git -C <chemin>` ; un `cd` en chaîne shell laisse
  le répertoire de travail déplacé pour les appels suivants.
- **Un sous-agent éditeur ne peut pas écrire un `SKILL.md`, un agent, un hook ou
  un `CLAUDE.md` sous forge** — `delegate-guard` le bloque. Un rapport de succès
  sur un de ces fichiers est donc à vérifier en priorité.

## Apprentissage

Incidents sources : `memory/feedback_subagent_autocommit.md` (un sous-agent a
committé dans un repo externe malgré la consigne) et
`memory/feedback_subagent_audit_category_error.md`.

Noter ici tout nouveau mode d'échec silencieux observé, et l'ajouter aux
anti-patterns quand il se répète.
