# claude-forge — adaptateur Claude Code

**Dernière mise à jour : 2026-08-28 | Version : 5.0**

@AGENTS.md
@memory/MEMORY.md

## Particularités Claude Code

- `.claude/settings.json` est protégé contre l'auto-modification. Toute évolution hooks/permissions est préparée dans `.claude/settings.json.proposed`, puis appliquée manuellement par Raphaël.
- Hooks Windows : launcher `py`, chemins via `${CLAUDE_PROJECT_DIR}`, jamais `C:\Users\...`.
- Création de composants : utiliser `skill-creator`, `subagent-creator`, `hook-creator` ou `claudemd-creator` ; ne pas écrire leurs fichiers à la main sans avoir chargé la skill propriétaire.
- Description YAML : une seule ligne. Une skill reste sous 500 lignes ; un CLAUDE.md sous 200 lignes.
- Agents : `memory: project` et `permissionMode` obligatoires ; `disallowedTools: Write, Edit` sur les agents read-only.
- Modèles : `sonnet` pour exécution, `opus` pour jugement. Effort `high` par défaut ; `medium/low` pour mécanique ; `xhigh` seulement après gain mesuré ; `max` jamais en frontmatter.
- Source de vérité Claude Code : docs et changelog Anthropic actuels, puis `cc-news`. Toute information potentiellement datée est re-vérifiée.

Les rules détaillées sous `.claude/rules/` sont chargées automatiquement. Ne pas
dupliquer ici leurs workflows.
