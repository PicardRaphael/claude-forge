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
derniere-maj: 2026-09-05
auteur: claude
type: technique
sources:
  - "Session 27 mai 2026 — Chantier A étape 2b, hook probe empirique"
  - "Audit de doctrine 5 septembre 2026 — retrait de la recette de contournement"
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

## ⛔ Trou connu de delegate-guard : le mismatch de matcher — exploitation INTERDITE

Le corollaire du fait empirique ci-dessus : un hook ne voit **que** ce que son matcher attrape. `delegate-guard.py` est enregistré sur `Write|Edit|MultiEdit` et teste le suffixe `.md`. Il en résulte deux angles morts réels :

- un `Write` vers `<fichier>.md.new` ne matche pas le test de suffixe ;
- un `Bash mv` n'est pas dans le matcher `Write|Edit|MultiEdit`.

**Ce constat sert à durcir le hook, jamais à passer à travers.** Enchaîner ces deux angles morts pour écrire un composant protégé est un contournement de garde-fou de scope — interdit sans exception, quelle que soit l'urgence et quel que soit le prétexte (« le creator est lui-même buggé », « c'est une exception unique », « c'est propre car ça respecte la spec du matcher »). La rule `delegate-to-specialists.md` est explicite : *si le hook bloque, la réponse n'est JAMAIS de le contourner.* Cf [[erreur-subagent-bypass-delegate-guard]] — un sub-agent a produit exactement ce raisonnement et il a été traité comme une faute.

### Que faire quand un creator doit se corriger lui-même

1. **Session principale + `Skill(<creator>)` frais**, puis les Edits enchaînés dans la fenêtre du transcript. C'est le chemin prouvé (16 juil. 2026) ; il couvre le cas « le creator requis est le fichier à modifier », le bypass `attributionSkill` étant strict par type de fichier et non par identité du fichier édité.
2. Si le creator est cassé au point d'être inutilisable : corriger **le hook** via `hook-creator`, ou remonter la décision à Raphaël. Modifier la garde est légitime ; la contourner ne l'est pas.
3. Sub-agent bloqué : STOP + ESCALADE avec le diff préparé (cf [[anti-reentrance-sub-agents-pattern-escalade]]), jamais d'auto-déblocage.

> **Correction du 5 septembre 2026.** Cette section prescrivait jusqu'ici la recette `.md.new` + `mv` comme un « bypass propre, sans violer ni désactiver le hook », validé par advisor et présenté comme exception légitime (cas d'école : durcissement d'`agent-creator`, 27 mai 2026). C'était une doctrine fausse, restée active plus de trois mois et relayée par [[comment-creer-agent]], qui portait une section jumelle — supprimée le même jour. Aucune formulation ne rend acceptable le franchissement d'un garde-fou de scope.

## Limite / scope

- Le matcher est le **nom exact du tool** (`mcp__server__tool`), pas un wildcard testé ici.
- Étendre un garde MCP à d'autres tools (`insert_section`, `update_note`) doit rester calibré sur observation empirique, pas sur inférence (cf [[feedback_mcp_alias_ambigu_chemin_exact]] : 4 violations, toutes sur `append_note`).

## Wikilinks

- [[comment-creer-hook]] — canonique hooks (30 events, matchers)
- [[delegate-guard-pattern]] — le hook protégé ici, son mécanisme `attributionSkill` et son scope forge-only
- [[erreur-subagent-bypass-delegate-guard]] — l'erreur fondatrice : contourner n'est jamais la réponse
- [[pattern-mcp-brief-then-direct]] — pourquoi vault-cat-guard existe (MCP décoratif en sub-agent)
- [[feedback_mcp_alias_ambigu_chemin_exact]] — pourquoi mcp-alias-guard existe
- [[resolution-path-3-contextes]] — contextes d'exécution et résolution de path
