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
derniere-maj: 2026-06-07
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

## Lethal trifecta (Simon Willison, juin 2025)

La combinaison de trois capacités = **vulnérabilité grave** :

1. **Accès aux données privées**
2. **Exposition au contenu non fiable** (web, emails, documents externes)
3. **Capacité de communication externe** (exfiltration possible)

> « MCP makes it very easy for people to glue lots of tools together… so you can accidentally do the trifecta. » — Simon Willison

Willison insiste : **pas de mitigation statistique** — « You can't have security mitigations that work on statistics » et « You can't patch your way out of prompt injection ». Défense **en profondeur obligatoire**, jamais un seul filtre probabiliste.

**Défenses** : least-privilege tooling, input/output filtering, **human-in-the-loop pour actions irréversibles**, **tokenisation des données sensibles**. Outils/patterns : Llama Guard 3, Azure Prompt Shields, Google DeepMind **CaMeL**, le paper *Design Patterns for Securing LLM Agents against Prompt Injections* (IBM/Invariant/ETH/Google/Microsoft).

## Sécurité MCP — failles documentées

MCP a gagné la guerre des interfaces mais sa sécurité est immature. Traiter **tout serveur MCP tiers comme du code non fiable** ; auditer avec `mcp-scan`.

| Faille | Détail | Source |
|---|---|---|
| **Tool poisoning** | Instructions malveillantes cachées dans les descriptions d'outils (PoC exfiltrant `~/.ssh/id_rsa` via Cursor) | Invariant Labs, avril 2025 |
| **CVE-2025-49596** | RCE critique CVSS 9.4 dans MCP Inspector (corrigé v0.14.1, 13 juin 2025) | NVD |
| **CVE-2025-6514** | mcp-remote, 437k+ environnements affectés | Oligo Security |
| **ToolHijacker** | 96,7% succès d'attaque par injection de description d'outil malveillante | NDSS 2026, cf [[tool-retrieval-query-expansion]] |

Cf [[agents-architecture]] section MCP (réconciliation servers + code execution).

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

- [[MOC-Techniques]]
- [[Agents IA]] — Index principal
- [[agents-evaluation]] — Testing et benchmarks
- [[agents-architecture]] — Patterns architecture
