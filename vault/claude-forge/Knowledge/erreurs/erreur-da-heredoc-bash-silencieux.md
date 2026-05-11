---
titre: "Devil's advocate heredoc Bash échoue silencieusement"
resume: "Le DA avait disallowedTools: Write, Edit mais utilisait Bash cat > pour sauvegarder les critiques — écriture déguisée qui échouait silencieusement. Seulement 2/4+ critiques sauvegardées. Fix : MCP create_note"
aliases:
  - "erreur DA heredoc"
  - "erreur devil's advocate sauvegarde"
  - "bash cat write déguisé"
  - "critique non sauvegardée"
type: knowledge
derniere-maj: 2026-05-11
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

## Liens

- [[erreur-devils-advocate-tronque]] — Autre erreur DA (troncation)
- [[MOC-Techniques]]
