---
titre: "Claude Code v2.1.113 — Breaking"
resume: "CLI natif binaire, sandbox security renforcée, find -exec plus auto-approuvé"
aliases:
  - "v2.1.113"
  - "2.1.113"
  - "CC 2.1.113"
  - "CLI native binary"
  - "breaking change avril 2026"
  - "sandbox security CC"
  - "binaire natif CLI"
domaine: claude-code
type: changelog
derniere-maj: 2026-04-21
auteur: claude
sources: ["https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md"]
tags: ["#type/changelog", "#domaine/claude-code"]
---

## Changements
- **CLI spawn binary natif per-platform** au lieu de bundled JS (npm path = deprecation notice)
- `sandbox.network.deniedDomains` setting
- Shift+Up/Down scroll fullscreen
- Ctrl+A/Ctrl+E = début/fin ligne logique (readline)
- Windows: Ctrl+Backspace = delete mot précédent
- URLs longues restent cliquables quand elles wrappent
- `/loop` Esc annule les wakeups
- `/extra-usage` fonctionne depuis Remote Control
- Remote Control supporte `@`-file autocomplete
- `/ultrareview` plus rapide (checks parallélisés, diffstat, animation)
- Subagents qui stall = fail après 10 min au lieu de hang

## Breaking changes
- CLI natif binaire = défaut. npm path affiche deprecation notice

## Sécurité
- macOS /private/* traités comme dangerous pour rm
- Bash deny rules matchent `env`/`sudo`/`watch`/`setsid` wrappers
- `find -exec`/`-delete` ne sont plus auto-approuvés
- 22 bug fixes

## Liens
- Precedent : [[CC v2.1.111]]
- Suivant : [[CC v2.1.114]]
- [[MOC-Claude-Code]]
