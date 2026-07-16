---
titre: "Claude Cowork — GA"
resume: "Cowork GA 9 avril 2026, tous plans payés, RBAC, OpenTelemetry, Analytics API, SCIM"
aliases:
  - "cowork"
  - "claude cowork"
  - "cowork GA"
  - "claude desktop pro"
  - "cowork enterprise"
type: feature
derniere-maj: 2026-07-16
auteur: claude
sources:
  - "https://9to5mac.com/2026/04/09/anthropic-scales-up-with-enterprise-features-for-claude-cowork-and-managed-agents/"
tags:
  - "#type/feature"
  - "#domaine/industrie"
---

## Contexte

Claude Cowork (ex-Claude Desktop Pro) en disponibilité générale depuis le 9 avril 2026.

## Découvertes

- Disponible macOS + Windows, tous plans payés
- RBAC enterprise, OpenTelemetry, Analytics API
- Groupes SCIM
- Computer Use disponible Pro + Max
- [[Claude Design]] = premier plugin Anthropic Labs

## Update mai 2026

- Connecteur Zoom, add-ins Microsoft 365 (Excel, PowerPoint, Word)
- 10 templates agents services financiers
- Microsoft Copilot Cowork (Frontier) integre Opus 4.7
- Controles organisation : group spend limits, usage analytics

## Liens

- [[MOC-Claude-Code]]
- [[Managed Agents]]
- [[Dispatch]]
- [[Claude Design]]
- [[Code with Claude Conference]]
- [[MOC-Industrie]]

## AJOUT 2026-07-16 — Web + mobile, sessions remote (7 juillet 2026)

- Cowork étendu au **web (claude.ai) et mobile (iOS/Android)** en beta — Max d'abord, rollout progressif sur plusieurs semaines. Chat et Cowork partagent désormais un home unifié.
- Nouveau modèle d'exécution : **sessions remote hébergées sur les serveurs Anthropic** (inverse du modèle Dispatch local) — sessions/fichiers sauvegardés sur le compte Claude, accessibles depuis n'importe quel device, le travail continue laptop fermé, les tâches planifiées tournent sans device allumé. Usage limits doublées prolongées jusqu'au 5 août 2026.
- ⚠️ Implication MCP : une session remote serveur n'atteint PAS un MCP localhost — renforce [[mcp-local-cowork-vs-claude-code]] et [[cowork-write-vault-headless-impossible]].
- Datapoint usage (1,2M sessions anonymisées, 600k+ orgs, échantillon mai 2026) : **> 90 % de l'usage Cowork est non-coding** — 33,4 % business process/ops, 16,4 % content creation, 8,7 % dev logiciel.
- Sources : claude.com/blog/cowork-web-mobile + TechCrunch (7 juil. 2026). Cf [[industrie-juillet-2026]].
