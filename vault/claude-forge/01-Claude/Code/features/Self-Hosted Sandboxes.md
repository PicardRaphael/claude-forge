---
titre: "Self-Hosted Sandboxes — Managed Agents sur votre infra"
resume: "Exécution du code des Managed Agents dans votre propre infrastructure au lieu des containers Anthropic. Public beta London 19 mai 2026."
aliases:
  - "self-hosted sandboxes"
  - "sandboxes auto-hébergées"
  - "managed agents self-hosted"
  - "custom sandboxes"
  - "self-hosted execution"
  - "sandboxes sur infra"
type: feature
derniere-maj: 2026-05-21
auteur: claude
sources:
  - "https://dev.to/devtoolpicks/anthropic-launches-self-hosted-claude-agents-what-indie-hackers-need-to-know-1nee"
  - "https://inaiwetrust.com/p/16-claude-features-that-change-how-you-build-ai"
tags:
  - "#type/feature"
  - "#domaine/claude-code"
  - "#domaine/agents"
  - "#domaine/infrastructure"
---

## Principe

Déplace l'exécution du code des agents de l'infra Anthropic vers l'infra du client. Les fichiers, le code, et le trafic réseau restent dans l'environnement du client.

## Architecture

Système de queue : les agents placent des work items, l'infra client les exécute. L'orchestration (context management, error handling) reste chez Anthropic — ce n'est **pas** du full on-premise.

## Providers au lancement

| Provider | Profil |
|----------|--------|
| **Cloudflare** | microVMs stateless |
| **Modal** | GPU-ready, compute-heavy |
| **Vercel** | Low-latency VM sandboxes |
| **Daytona** | Long-lived VMs, sessions étendues |
| **Custom** | Containers configurables |

## Limitations

- L'orchestration reste chez Anthropic (pas full on-premise)
- Pas disponible sur Claude Platform on AWS (au lancement)
- Memory non supportée dans les sessions self-hosted
- Network policies et audit logs configurables

## Use cases

- Compliance / données régulées
- VPC restrictions bloquant Managed Agents
- Healthcare / finance / government
- Clients enterprise avec security reviews strictes

Probablement ce qui bloquait l'adoption Managed Agents en entreprise.

## Statut

Public beta — annoncé Code with Claude London, 19 mai 2026.

## Liens

- [[Managed Agents]]
- [[MCP Tunnels]]
- [[Code with Claude 2026]]
- [[MOC-Claude-Code]]
