---
name: config-guardian-audit-pattern
description: Pattern complet pour auditer les repos Neoteem — 5 checks baseline, corrections par stack, mémoire compounding Boris. Reproduire ce workflow à chaque audit.
type: feedback
originSessionId: fdb162f8-52a4-438b-a60a-c8e2ce6e37cf
---
Quand on audite un repo Neoteem, toujours suivre ces 5 checks dans cet ordre :

1. **Permissions git** — commit/push allow dans settings.json + settings.local.json + vérifier global deny
2. **Hooks cohérence stack** — tous les hooks doivent utiliser le même langage que le projet. Détecter orphelins + fantômes
3. **Rules obligatoires** — check-before-create, learn-from-mistakes, quality-gates
4. **MCP tools dans agents** — chaque agent doit déclarer les MCP tools dont il a besoin selon son rôle (pas de liste universelle — dépend du projet et de l'agent)
5. **Mémoire compounding** — memory: project sur tous agents, Gotchas dans CLAUDE.md, section Mémoire dans CLAUDE.md, feedback rules réelles

**Why:** Session du 4 mai 2026 — audit complet des 3 repos a révélé des agents sans MCP déclarés, un hook dans le mauvais langage, un fichier orphelin, des sections Mémoire manquantes. Tout corrigé en une session.

**How to apply:** Utiliser `/config-guardian` depuis forge (la baseline par repo est dans references/baseline-rules.md de la skill). Chaque repo a sa propre architecture — ne pas copier-coller les MCP d'un repo à l'autre.
