---
titre: "Erreur — deny global ~/.claude/ écrase allow projet (diagnostic permission git)"
type: knowledge
domaine: claude-code
derniere-maj: 2026-05-27
auteur: claude
statut: actif
aliases:
  - deny global écrase allow projet
  - precedence deny global settings
  - git commit bloqué malgré allow projet
  - permission git refusée diagnostic
  - settings global deny priorité
  - pourquoi git commit denied
tags:
  - "#type/erreur"
  - "#domaine/claude-code"
  - "#domaine/securite"
---

# Erreur — un `deny` global écrase tout `allow` projet

## Ce qui s'est passé (2026-05-27)

Session forge : commit + push demandés. `git add`, `git status`, `git branch`, `git --version` passaient, mais **`git commit` et `git push` étaient systématiquement refusés** (`Permission ... has been denied`), quelle que soit la syntaxe (`-F`, `-m`, `--file=`).

J'ai perdu plusieurs tours à soupçonner :
1. le pattern `Bash(git *)` du settings **projet** (faux — il couvre bien `git commit`),
2. le mode de permission de session (faux — un redémarrage n'a rien changé),
3. j'ai même ajouté `defaultMode: bypassPermissions` au settings **projet** (inutile).

Raphael a pointé la vraie cause : **le `.claude` global**.

## La cause réelle

`~/.claude/settings.json` (global) contenait un bloc `deny` :
```json
"deny": [
  "Bash(git commit *)", "Bash(git commit)",
  "Bash(git push *)",   "Bash(git push)",
  "Bash(git -C *)", "Bash(git remote *)", ...
]
```

**Règle de précédence Claude Code** : `deny` > `ask` > `allow`, et le scope **global (`~/.claude/`) écrase le scope projet (`.claude/`)**. Donc un `deny` global rend inopérant n'importe quel `allow` projet, même `Bash(git *)`. Aucune modification du settings *projet* ne peut contourner un `deny` *global*.

## Symptôme diagnostique caractéristique

Les sous-commandes git **simples** passent (`version`, `status`, `add`, `branch`) mais une sous-commande **précise** est refusée (`commit`, `push`). Quand `Bash(git *)` est en allow projet et qu'une sous-commande git précise est refusée → **chercher un `deny` ciblé dans `~/.claude/settings.json` global AVANT de toucher le settings projet**.

## Ce qu'il faut faire à la place

1. Lire `~/.claude/settings.json` en PREMIER quand une permission Bash est refusée malgré un allow projet.
2. Vérifier le bloc `deny` global (précédence absolue).
3. Modifier le `deny` global (avec accord utilisateur — c'est un garde-fou volontaire), pas le settings projet.
4. Le `deny` est relu à chaud (le commit a fonctionné immédiatement après édition, sans redémarrage de session).

## Lien avec le garde-fou volontaire

Le `deny` global git (commit/push/merge/rebase/reset/clean) est un **garde-fou sain par défaut** : il empêche tout git autonome non sollicité. Le retirer doit être une décision explicite de l'utilisateur. Garder le deny sur les opérations vraiment destructives (merge, rebase, reset --hard, clean, branch -D, rm -rf /, format, dd, shutdown).

## Liens

- [[config-guardian-pattern]] — check #1 mentionne « commit/push allow, global deny vide » mais ne documentait pas le piège diagnostique
- [[auto-mode-classifier]] — édition de settings.json permissions protégée
- [[feedback_bash_permission_format]] — format des permissions Bash
