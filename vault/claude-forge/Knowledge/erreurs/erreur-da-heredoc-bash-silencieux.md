---
titre: "Devil's advocate heredoc Bash échoue silencieusement"
resume: "Le DA avait disallowedTools: Write, Edit mais utilisait Bash cat > pour sauvegarder les critiques — écriture déguisée qui échouait silencieusement. Seulement 2/4+ critiques sauvegardées. Fix : MCP create_note"
aliases:
  - "erreur DA heredoc"
  - "erreur devil's advocate sauvegarde"
  - "bash cat write déguisé"
  - "critique non sauvegardée"
type: knowledge
derniere-maj: 2026-06-05
auteur: claude
tags:
  - "#type/erreur"
  - "#erreur/agent"
  - "#domaine/claude-code"
---
## Ce qui s'est passé

Session 11 mai 2026. Audit du devil's advocate révèle que seulement 2 critiques sur 4+ runs étaient sauvegardées dans `Knowledge/critiques/`. Le DA avait `disallowedTools: Write, Edit` dans son frontmatter mais utilisait un heredoc Bash (`cat > vault/.../critique-*.md`) pour écrire — un write déguisé qui passait ou non selon les permissions, sans erreur visible.

## Pourquoi c'était une erreur

Le compounding effect promis (chaque critique alimente les suivantes via MCP search) ne fonctionnait pas. Les `search_brain("critique ...")` retournaient quasi-vide → 3 appels MCP pour du signal nul à chaque run.

## Fix appliqué

Remplacé le heredoc Bash par `mcp__forge-brain__create_note` dans le prompt de l'agent. Le MCP n'est pas dans `disallowedTools` → la sauvegarde passe toujours. Marquée OBLIGATOIRE.

## Règle générale

**Ne jamais utiliser Bash pour écrire des fichiers quand `Write`/`Edit` sont interdits** — `cat >`, `echo >`, heredoc = des writes déguisés qui peuvent être bloqués silencieusement. Utiliser le MCP ou un autre canal autorisé.

## Scope exact — le HEREDOC n'échoue PAS partout (vérifié empiriquement 5 juin 2026)

Le HEREDOC Bash (`cat <<'EOF' > file`) **fonctionne** en commande Bash directe sur la machine forge — test 5 juin 2026 : fichier avec accents, `$var`, backticks, `@` écrit correctement (exit 0, contenu intact), et 2 commits du 4 juin créés via `cat <<'EOF'`. La doctrine « HEREDOC Windows à éviter » est donc **trop large si énoncée sans scope**.

Les DEUX cas réels où il casse :
1. **Sous `disallowedTools: Write, Edit`** (cette note) — write déguisé bloqué silencieusement.
2. **Dans un hook** (Git Bash, `bash -c '...$()...'`) — boucle quoting, cf [[erreur-hooks-bash-quoting-windows]].

Hors de ces deux contextes, le HEREDOC est utilisable. La prudence « préférer un fichier message / MCP » reste un bon défaut (comportement parfois inconstant selon le quoting), mais ne pas affirmer qu'il « échoue toujours sur Windows ».

## Piège connexe — here-string PowerShell `@'...'@` dans le tool Bash (5 juin 2026)

Distinct du HEREDOC bash. Un `git commit -m @'...message...'@` (here-string **PowerShell**) lancé via le tool **Bash** ne casse pas l'écriture — il pollue le contenu : `@'` et `'@` sont une syntaxe PowerShell que bash ne parse pas, donc le `@` de tête survit comme **premier caractère littéral** du message → sujet de commit `@ docs(...)`. Corrigé par `git commit --amend` avec des `-m` multiples (un par paragraphe).

**Règle :** ne pas mélanger les syntaxes de shell. Pour un message multi-ligne dans le tool **Bash**, utiliser plusieurs `-m`. Le here-string `@'...'@` n'est valide que dans le tool **PowerShell**. Symétrique du HEREDOC bash qui n'est valide que côté Bash.

## Liens

- [[erreur-devils-advocate-tronque]] — Autre erreur DA (troncation)
- [[MOC-Techniques]]
