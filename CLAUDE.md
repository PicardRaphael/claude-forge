# claude-forge — adaptateur Claude Code

**Dernière mise à jour : 2026-09-30 | Version : 5.1**

@AGENTS.md
@memory/MEMORY.md

## Particularités Claude Code

- `.claude/settings.json` est une surface de sécurité protégée par `hook-creator`. Toute évolution est relue avec son diff et ses tests ; les réglages utilisateur globaux restent manuels.
- Hooks Windows : launcher `py`, chemins via `${CLAUDE_PROJECT_DIR}`, jamais `C:\Users\...`.
- Création de composants : utiliser `skill-creator`, `subagent-creator`, `hook-creator` ou `claudemd-creator` ; ne pas écrire leurs fichiers à la main sans avoir chargé la skill propriétaire.
- Description YAML : une seule ligne. Une skill reste sous 500 lignes ; un CLAUDE.md sous 200 lignes.
- Agents : mémoire persistante désactivée par défaut et activée seulement avec besoin, périmètre et révision explicites ; `disallowedTools: Write, Edit` sur les agents read-only.
- Modèles : jamais `sonnet` dans forge — `opus` + effort `medium` pour exécution et mécanique, `opus` + `high` pour jugement, `haiku` pour l'exploration rapide, parce qu'Opus 5.5 en `medium` égale Opus 5 en `high` (vault `raisonnement-2026-09-30-zero-sonnet`). Fable seulement en step-up mesuré ; `xhigh` seulement après gain mesuré ; `max` jamais en frontmatter.
- Source de vérité Claude Code : docs et changelog Anthropic actuels, puis `cc-news`. Toute information potentiellement datée est re-vérifiée.

Les rules détaillées sous `.claude/rules/` sont chargées automatiquement. Ne pas
dupliquer ici leurs workflows.
