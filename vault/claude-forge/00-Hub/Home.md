---
titre: "Forge Brain — Home"
resume: "Vault forge-brain — 340+ notes pattern Karpathy 3-layers, MCP forge-brain port 8091, 8 canoniques chantier 22 mai + doctrine 22 mai (hooks lint/security/scope, JAMAIS workflow)"
aliases:
  - "home"
  - "accueil"
  - "forge brain"
  - "vault home"
  - "knowledge base"
  - "index principal"
type: index
derniere-maj: 2026-05-24
auteur: claude
sources: []
tags:
  - "#type/index"
  - "#domaine/vault"
  - "#domaine/meta"
---

# Forge Brain

Vault Karpathy LLM Wiki pour claude-forge. Pour trouver une note en 1 saut → **[[index]]** (content-oriented). Pour les conventions → **[[SCHEMA]]**. Pour les opérations → **[[log]]** + **[[CHANGELOG]]**.

## Si tu cherches "comment faire X" — canoniques chantier 22 mai

- [[comment-ecrire-claudemd]] — 200L, anti-patterns
- [[comment-creer-skill]] — 9 catégories Thariq, < 500L
- [[comment-creer-agent]] — Sonnet/Opus split, 8 couleurs
- [[comment-creer-hook]] — 29 events, doctrine 22 mai
- [[workflow-claude-code-optimal]] — routines Boris, advisor Brad Abrams
- [[methode-analyser-repo]] — META 6 étapes
- [[methode-pivoter-doctrine]] — checklist anti-drift résiduel
- [[mcp-vs-skills-doctrine]] — MCP data / Skills how-to
- [[pattern-vault-llm-karpathy]] — 3-layers + index.md + log.md

## Navigation par MOC

| Section | Contenu |
|---------|---------|
| [[MOC-Claude-Code]] | Features, changelog, hooks, skills, agents, best practices |
| [[MOC-Outils-IA]] | Gemini CLI, Codex, Copilot, Cursor, xAI |
| [[MOC-Modeles]] | Specs, benchmarks, migrations |
| [[MOC-Techniques]] | Prompt eng, context eng, RAG, agents, fine-tuning, patterns |
| [[MOC-Leaders]] | 79 fiches : CC team, agents, RAG, fine-tuning, prompt, industrie |
| [[MOC-Industrie]] | Market, funding, événements |
| [[MOC-Prompts]] | System prompts, techniques prompting |

## Doctrine 22 mai 2026 (active)

- **Hooks** : lint / security / scope UNIQUEMENT. JAMAIS workflow agentique. Voir [[raisonnement-22mai-doctrine-vs-enforcement]]
- **Modèles** : Sonnet exécution, Opus jugement
- **DA conditionnel ciblé** : livrables majeurs (skill cross-repo, agent orchestrant, archi). Pas systématique
- **Advisor AVANT travail substantiel**, après exploration

## Conventions

- 1 concept = 1 note atomique
- Frontmatter obligatoire (4-6 aliases, `resume` spécifique, `derniere-maj` ISO, ≥ 2 tags)
- Wikilinks `[[Note]]` pour tout cross-référencement
- MCP forge-brain uniquement (jamais Grep/Read brut sur vault)

## Liens

- [[index]] — index content-oriented Karpathy
- [[SCHEMA]] — conventions self-describing
- [[log]] — log append-only
- [[CHANGELOG]] — narration mensuelle
