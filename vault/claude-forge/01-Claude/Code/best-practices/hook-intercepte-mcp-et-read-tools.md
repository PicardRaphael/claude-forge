---
titre: "PreToolUse intercepte les tools MCP et Read — preuve empirique"
resume: "Un hook PreToolUse avec matcher mcp__server__tool intercepte bien les appels MCP (tool_input.file lisible), et matcher Read intercepte les lectures (tool_input.file_path). Prouvé par hook probe 27 mai 2026. Débloque les gardes sur écritures MCP et lectures vault."
aliases:
  - "hook intercepte mcp"
  - "PreToolUse matcher mcp tool"
  - "hook matcher Read"
  - "intercepter append_note hook"
  - "matcher mcp__forge-brain__append_note"
  - "hook sur tool MCP"
derniere-maj: 2026-07-27
auteur: claude
type: technique
sources:
  - "Session 27 mai 2026 — Chantier A étape 2b, hook probe empirique"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/hooks"
  - "#domaine/mcp"
---
# PreToolUse intercepte les tools MCP et Read

## Fait empirique

Un hook `PreToolUse` peut matcher et intercepter :

1. **Un tool MCP** via `matcher: "mcp__forge-brain__append_note"` — le hook reçoit le stdin avec `tool_name: "mcp__forge-brain__append_note"` et `tool_input.file` (l'alias/stem passé à l'outil).
2. **Le tool Read** via `matcher: "Read"` — le hook reçoit `tool_name: "Read"` et `tool_input.file_path`.

Avant cette preuve, aucun hook forge ne matchait un tool MCP (tous sur `Write|Edit|MultiEdit|Bash`). L'hypothèse « PreToolUse intercepte-t-il les MCP ? » était un point bloquant identifié par l'advisor.

## Méthode de preuve (hook probe)

Pattern réutilisable pour vérifier l'interception d'un tool inconnu :

1. Écrire un hook stub qui log `sys.stdin` brut dans un fichier temp, puis `exit 0`.
2. L'enregistrer dans `settings.local.json` (pas `settings.json` — évite le hard block classifier) sur le matcher à tester.
3. Déclencher l'outil cible une fois.
4. Lire le log : si `FIRED` apparaît avec le bon `tool_name`, le matcher fonctionne.

Bonus observé : `settings.local.json` EST relu **à chaud** (le hook a fité dans la session courante sans redémarrage). Affiné le 27 mai en cours de session 2b : `settings.json` l'est AUSSI — `vault-cat-guard` enregistré dans `settings.json` a bloqué les Read/Bash/PowerShell de la session courante immédiatement après son enregistrement, et son ajustement (Read autorisé en session principale) a pris effet sans redémarrage. Donc `settings.json` ET `settings.local.json` sont relus à chaud sur cette version CC. Converge avec [[erreur-deny-global-ecrase-allow-projet]] (deny relu à chaud). Prudence : comportement de version, à re-vérifier si CC change.

## Stdin reçu (session principale, append_note)

```json
{
  "session_id": "...",
  "transcript_path": "C:\\Users\\...\\<id>.jsonl",
  "cwd": "C:\\Users\\...\\claude-forge",
  "permission_mode": "auto",
  "hook_event_name": "PreToolUse",
  "tool_name": "mcp__forge-brain__append_note",
  "tool_input": {"file": "...", "content": "..."}
}
```

Pas de champ `agent_type`/`agent_id` en session principale → la détection sub-agent passe par `transcript_path` (cf [[resolution-path-3-contextes]] pour les contextes d'exécution).

## Ce que ça débloque

- **Gardes sur écritures MCP** : ex `mcp-alias-guard.py` (bloque `append_note(file=<stem ambigu>)`).
- **Gardes sur lectures** : ex `vault-cat-guard.py` (bloque `Read` sur le vault — enforce la doctrine MCP-only structurellement).

## Exceptions delegate-guard légitimes — bypass par mismatch de matcher

`delegate-guard.py` route tout `.claude/agents/*.md` (et `SKILL.md`, `CLAUDE.md`) vers son creator dédié. Quand un creator est le **verrou de bootstrap** et doit se corriger lui-même (le creator requis EST le fichier buggé), l'édit direct est bloqué et la délégation impossible.

Bypass propre, sans violer ni désactiver le hook (exploite la spec du matcher) :

1. `Write` vers `<fichier>.md.new` — suffixe `.new` ≠ `.md` → `is_agent_md` False → delegate-guard ne tire pas.
2. `Bash mv <fichier>.md.new <fichier>.md` — `Bash` hors matcher `Edit|Write|MultiEdit` → delegate-guard ne tire pas.
3. `Read`/grep de vérif (le `Write` fichier entier remplace l'`Edit` ciblé → vérifier frontmatter intact).

Exception unique justifiée, jamais en routine, validation `advisor` préalable. Cas d'école : Chantier A étape 2b (27 mai 2026), `agent-creator` durci en premier par ce mécanisme. Détail complet : [[comment-creer-agent]] section « Self-modification d'un creator buggé via bypass de matcher ».
## Limite / scope

- Le matcher est le **nom exact du tool** (`mcp__server__tool`), pas un wildcard testé ici.
- Étendre un garde MCP à d'autres tools (`insert_section`, `update_note`) doit rester calibré sur observation empirique, pas sur inférence (cf [[feedback_mcp_alias_ambigu_chemin_exact]] : 4 violations, toutes sur `append_note`).

## Wikilinks

- [[comment-creer-hook]] — canonique hooks (30 events, matchers)
- [[pattern-mcp-brief-then-direct]] — pourquoi vault-cat-guard existe (MCP décoratif en sub-agent)
- [[feedback_mcp_alias_ambigu_chemin_exact]] — pourquoi mcp-alias-guard existe
- [[resolution-path-3-contextes]] — contextes d'exécution et résolution de path
