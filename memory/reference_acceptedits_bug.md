---
name: acceptedits-bug-anthropic-since-v2179
description: "Bug Anthropic confirmé acceptEdits (Shift+Tab) prompte quand même à chaque Edit/Write depuis v2.1.79 mars 2026, non fixé v2.1.139 mai 2026. Workaround = Auto mode"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 659a145e-76a1-4fd2-a7c7-a7ee10f7dbc3
---

# Bug acceptEdits Claude Code (mars-mai 2026)

## Symptôme
Status bar affiche "Accept edits on" mais prompt "Do you want to make this edit?" apparaît à chaque tool call Edit/Write/MultiEdit. Raphael l'a signalé le 2026-05-22 sur v2.1.138 Windows.

## Root cause
- VSCode extension : `requestToolPermission` dans extension.js route vers UI sans checker `permissionMode`
- CLI Windows 11 : régression v1.0.103 puis v2.1.79+

## Issues GitHub
- #58504 (v2.1.139, mai 2026) — non fixé
- #47571 — worktree bug
- #7113 — Windows 11 regression
- #31827, #11870, #7662 — duplicates fermés

## Workarounds (ordre préférence Raphael)
1. **Auto mode** (Anthropic, sorti 2026-03-24) — Classifier évalue risque par tool call. Safe + autonome. Cf [[auto-mode-classifier]]
2. `"defaultMode": "bypassPermissions"` dans .claude/settings.json — plus large blast radius
3. `permissions.allow` allow-list explicite Edit/Write/MultiEdit

## Pertinence forge
Raphael en Auto mode actuellement (cf CLAUDE.md ligne 7 "Auto-mode classifier hard block"). Le bug acceptEdits n'est PAS sa config — c'est un bug Anthropic. Ne pas chercher à debugger ses settings.

Liens : [[auto-mode-classifier]], [[reference_cc_updates_april2026]]
