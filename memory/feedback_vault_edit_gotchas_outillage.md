---
name: vault-edit-gotchas-outillage
description: Deux gotchas outillage à l'écriture vault — delegate-guard faux positif sur note nommée agents-*.md, et insert_section qui misparente après un header de section nu
metadata:
  type: reference
---

Deux gotchas découverts en capitalisant une note vault (7 juin 2026), tous deux liés à l'outillage d'écriture, pas au contenu.

**Why:** chacun a coûté un détour ; ils sont invisibles tant qu'on ne les a pas rencontrés et re-mordront sur toute édition vault future.

**How to apply:**

1. **delegate-guard faux positif sur notes vault `agents-*.md`** — le hook `delegate-guard.py` matche `agents/*.md` PAR NOM. Une note vault `04-Techniques/agents/agents-architecture.md` se fait bloquer en Edit direct comme si c'était un sous-agent `.claude/agents/`. → Pour modifier le CONTENU d'une note vault, utiliser les outils MCP forge-brain (`insert_section`, `update_note`, `append_note`) qui ne passent pas par le hook PreToolUse Edit. Réserver Edit/Write aux notes dont le nom ne déclenche pas le pattern (ex. `index.md`, `stack-*.md`, `economie-*.md` passent). Ne JAMAIS contourner le hook par env var/script (cf [[delegate-guard-env-var-blocked]]).

2. **`insert_section` misparente après un header de section nu** — `mcp__forge-brain__insert_section(marker="## Section", position="after")` insère juste APRÈS la ligne du header, pas après la section entière. Si la section commence par un header `##` suivi directement de sous-sections `###` ou d'une table, le contenu inséré se loge AVANT le corps existant → la table/le bloc d'origine se retrouve reparenté sous la dernière sous-section insérée. → Pour insérer en FIN de section, viser un marker précis (dernière phrase de la section, en gras si possible) plutôt que le header nu. Vérifier le placement avec `read_section(file, heading="## Section")` (le param s'appelle `heading` et DOIT commencer par `#`). Correction = `update_note` (réécriture complète) si le bloc est déjà mal parenté.

Contexte : capitalisation rapport « Stack IA en production 2026 » → vault. Cf [[stack-ia-production-2026]], [[delegate-guard-pattern]].
