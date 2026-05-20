---
titre: "Subagent — Explore puis Edit (split read-only / write)"
resume: "Pattern officiel Anthropic large codebases : subagent read-only mappe le subsystem et écrit ses findings dans un fichier, puis le main agent édite avec le picture complète"
aliases:
  - "subagent explore then edit"
  - "split exploration editing"
  - "read-only subagent mapping"
  - "subagent two-phase"
  - "explore-edit split pattern"
  - "exploration findings file"
domaine: claude-code
type: technique
derniere-maj: 2026-05-20
auteur: claude
sources:
  - "https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start"
  - "Anthropic Applied AI — Claude Code at scale (14 mai 2026)"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/agents"
  - "#pattern/subagent"
---

## Le pattern

Sur une grosse codebase, ne pas faire explorer et éditer par la même session :

1. **Phase 1 — Explore (subagent read-only)** : un subagent isolé avec son propre context window mappe le subsystem, suit les références cross-fichiers, et **écrit ses findings dans un fichier markdown** (ex: `exploration-notes.md`)
2. **Phase 2 — Edit (main agent)** : le main agent lit le fichier de findings et édite avec la picture complète sans avoir consommé son contexte sur l'exploration

> [!quote] Anthropic (blog 14 mai 2026)
> "Once the harness is in place, some teams spin up a read-only subagent to map a subsystem and write findings to a file, then have the main agent edit with the full picture."

## Pourquoi

| Problème | Solution |
|----------|----------|
| Le contexte du main agent se sature en lisant 20 fichiers d'exploration | Le subagent isolé bouffe le contexte d'exploration, pas le main |
| Re-explorer à chaque session de coding | Le fichier de findings est persistant et réutilisable |
| Modifications accidentelles pendant l'exploration | Subagent en mode `disallowedTools: Write, Edit` → 100% read-only enforced |
| Confusion entre "comprendre" et "modifier" | Phase clairement séparées, livrable explicite |

## Configuration

### Subagent explorer

```yaml
---
name: codebase-explorer
description: Maps a subsystem read-only and writes findings to a file
model: opus
effort: high
disallowedTools:
  - Write
  - Edit
  - NotebookEdit
tools:
  - Read
  - Grep
  - Glob
  - Bash
---

Tu explores le subsystem demandé en read-only. À la fin, écris UN SEUL fichier
`exploration-notes.md` dans le répertoire de travail contenant :

- Architecture : composants principaux, leurs responsabilités
- Entry points : où on entre dans ce subsystem
- Dependencies : ce que ce code appelle et ce qui l'appelle
- Conventions : patterns observés, naming, gotchas
- Points d'attention : code suspect, TODOs, dette

Ne modifie rien d'autre. Ne tente pas d'éditer le code.
```

> [!warning] Gotcha critique — disallowedTools casse Bash heredoc
> `disallowedTools: Write, Edit, NotebookEdit` casse aussi `Bash` heredoc (`cat <<EOF > file.md`). Le shell échoue silencieusement, l'agent croit avoir écrit. Documenté dans [[erreur-da-heredoc-bash-silencieux]] (2/4+ critiques DA perdues en prod, 2026-05-11).
>
> **Fix #1 éprouvé (recommandé) : MCP `forge-brain:create_note`** — le MCP n'est pas affecté par `disallowedTools` qui ne couvre que les tools natifs. Pattern utilisé en prod par `devils-advocate.md` qui a `disallowedTools: Write, Edit` ET écrit ses critiques via MCP.
>
> **Fix #2 (fallback)** : retourner le contenu au main agent qui écrit le fichier lui-même.
>
> **Fix #3 (mauvais, ne fait pas)** : "autoriser uniquement Write" — perd l'enforcement read-only qui est tout l'intérêt du pattern.

### Workflow main agent

```
1. Lance le subagent explorer sur le subsystem cible
2. Lit exploration-notes.md
3. Implémente la feature en gardant exploration-notes.md référencé
4. Maintient en parallèle implementation-notes.md (voir [[running-implementation-notes]])
```

## Quand utiliser

- ✅ Codebase > 100k lignes
- ✅ Subsystem inconnu à toucher (ex: legacy module qu'on n'a jamais lu)
- ✅ Refactor qui demande une compréhension globale avant de toucher au code
- ✅ Audit de sécurité / dette technique
- ❌ Fix simple dans un fichier connu
- ❌ Feature isolée dans un module bien maîtrisé

## Combinaisons

| Combiner avec | Pourquoi |
|---------------|----------|
| [[running-implementation-notes]] | Explorer puis implémenter en notant les décisions live |
| [[pattern-spec-driven-development]] | Explorer → générer spec → implémenter dans session séparée |
| [[harness-engineering]] | Pattern foundational du harness Anthropic |
| LSP integrations | Le subagent explorer gagne énormément avec LSP (symbol-level vs string) |

## Gotcha — limites subagents

Voir [[limites-subagents-claude-code]] :
- Pas de parallélisme entre subagents (bugs confirmés)
- 200k context max, 32k output
- `maxTurns` cassé dans certaines versions

Pour cette raison : un seul subagent explorer à la fois, et bien borner sa tâche (max 30 tours).

## Anti-patterns

- ❌ Faire explorer ET éditer par le main agent → context saturé, perte de focus
- ❌ Plusieurs subagents en parallèle → bugs CC connus
- ❌ Subagent sans `disallowedTools` Write/Edit → peut modifier accidentellement
- ❌ Ne pas écrire les findings dans un fichier → tout est perdu à la fin du subagent

## Liens

- [[harness-engineering]] — Pattern foundational du harness
- [[running-implementation-notes]] — Phase 2 logique après exploration
- [[limites-subagents-claude-code]] — Limites techniques à connaître
- [[decoupe-agents-anti-crash]] — Découpage par phase
- [[claudemd-guide]] — Subagent doit hériter du CLAUDE.md
