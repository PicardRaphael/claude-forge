---
titre: "Agents Sécurité — OWASP, sandboxing, guardrails"
resume: "Sécurité agents IA 2026 : OWASP top 10 agentic, prompt injection, sandboxing, dual-LLM, permissions, audit trails"
aliases:
  - agent security
  - sécurité agents
  - OWASP agentic
  - prompt injection defense
  - agent sandboxing
  - agent guardrails
domaine: ia
type: technique
derniere-maj: 2026-05-08
auteur: claude
sources:
  - "https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html"
  - "https://rapidclaw.dev/blog/prompt-injection-defense-production-agents-2026"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/agents"
---

## OWASP Top 10 for Agentic Applications (2026)

Premier framework peer-reviewed pour agents autonomes tool-using.

- **ASI01 — Agent Goal Hijack** : input manipulé redirige goals, planning, multi-step behavior
- **LLM01 — Prompt Injection** : #1 menace. Présent dans **73% des déploiements prod**. Pas de solution propre — analogie avec SQL injection avant parameterized queries
- **LLM06 — Excessive Agency** : accès tools trop permissif

Menaces additionnelles : **memory poisoning** (données malveillantes persistées), **data exfiltration** via tool calls, **supply chain attacks** sur outils découverts dynamiquement.

## Défense en profondeur (7 couches)

1. **Input handling** — séparation trusted/untrusted
2. **Output filtering** — validation des sorties agent
3. **Capability sandboxing** — limiter les outils disponibles
4. **Privilege separation** — least-authority tools, JIT ephemeral tokens
5. **Canary tokens** — détection d'exfiltration
6. **Policy engines** — règles au niveau gateway
7. **Continuous red teaming** — tests adversarial réguliers

## Pattern Dual-LLM

- **LLM privilégié** : a accès aux tools, ne lit JAMAIS de contenu non-fiable
- **LLM quarantainé** : lit le contenu non-fiable, ne peut PAS agir
- Le privilégié reçoit uniquement des résumés structurés du quarantainé

Casse la chaîne injection → action. Une couche dans defense-in-depth, pas une solution complète.

## Sandboxing

La plupart des agents exécutent du code non-sandboxé. Production :
- **Docker** pour outils standard
- **gVisor / Kata / Firecracker MicroVMs** pour code à haut risque
- Limites strictes : mémoire, CPU, réseau, filesystem allowlists
- Software-only sandboxing = insuffisant → isolation hardware recommandée

Claude Code : système de permissions 7 modes + classifieur ML.

## Permissions tools

- Définir permissions explicites par tool : rate limits, valeurs params autorisées/bloquées
- MCP permissions model = granulaire
- Vérification signature + checking pour composants externes
- **HITL** reste la défense la plus efficace pour actions high-stakes

## Audit trails

OpenTelemetry agent identity schema : `gen_ai.agent.id`, `gen_ai.agent.name`, `gen_ai.agent.version`.

Chaque invocation tool, décision permission, et output = loggé immutablement. EU AI Act Article 15, NIST AI RMF.

## Liens

- [[Agents IA]] — Index principal
- [[agents-evaluation]] — Testing et benchmarks
- [[agents-architecture]] — Patterns architecture
