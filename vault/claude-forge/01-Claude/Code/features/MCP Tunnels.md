---
titre: "MCP Tunnels — Accès sécurisé aux MCP servers privés"
resume: "Tunnel sécurisé permettant aux Managed Agents d'accéder aux MCP servers derrière un firewall sans exposition publique. Research preview London 19 mai 2026."
aliases:
  - "MCP tunnels"
  - "tunnels MCP"
  - "MCP private access"
  - "MCP tunnel sécurisé"
  - "managed agents MCP privé"
  - "tunnel outbound MCP"
type: feature
derniere-maj: 2026-05-21
auteur: claude
sources:
  - "https://dev.to/devtoolpicks/anthropic-launches-self-hosted-claude-agents-what-indie-hackers-need-to-know-1nee"
  - "https://inaiwetrust.com/p/16-claude-features-that-change-how-you-build-ai"
tags:
  - "#type/feature"
  - "#domaine/claude-code"
  - "#domaine/mcp"
  - "#domaine/infrastructure"
  - "#domaine/securite"
---

## Principe

Permet aux Claude Managed Agents d'accéder aux MCP servers hébergés derrière le firewall de l'entreprise, sans les exposer sur internet public.

## Fonctionnement

1. Proxy léger déployé dans le réseau privé
2. Connexion outbound unique vers l'infrastructure de routage Anthropic
3. Les agents requêtent les outils internes de façon transparente
4. Pas de firewall rules inbound, pas d'endpoints publics
5. Chiffré end-to-end

## Scope

- Fonctionne avec Claude Managed Agents et Messages API
- Pas encore pour Claude Code CLI (au lancement)

## Use cases concrets

- Data warehouses internes
- Feature flag services
- Systèmes de ticketing (Jira, Linear)
- Bases de connaissances privées
- APIs internes

## Intérêt pour Neoteem

Potentiellement intéressant pour connecter les agents au brain Neoteem (MCP obsidian-brain) sans exposer le serveur MCP sur internet. À évaluer quand passage en GA.

## Statut

Research preview — annoncé Code with Claude London, 19 mai 2026. Nécessite demande d'accès, pas production-ready.

## Liens

- [[Self-Hosted Sandboxes]]
- [[Managed Agents]]
- [[Code with Claude 2026]]
- [[mcp-obsidian-brain-v2]]
- [[MOC-Claude-Code]]
