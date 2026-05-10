---
titre: "CLAUDE.md Maintenance — Best Practices Officielles et Communautaires"
resume: "Consensus Boris + Anthropic + communauté : 100-200L max, test 'Would removing this cause mistakes?', reactive not proactive, monthly audit, tools > prose."
aliases:
  - "CLAUDE.md maintenance"
  - "CLAUDE.md best practices"
  - "CLAUDE.md pruning"
  - "CLAUDE.md bloat"
  - "maintenir CLAUDE.md"
  - "optimiser CLAUDE.md"
domaine: claude-code
type: technique
derniere-maj: 2026-05-10
auteur: claude
sources:
  - "https://code.claude.com/docs/en/best-practices"
  - "https://howborisusesclaudecode.com/"
  - "https://claude.com/blog/using-claude-md-files"
tags:
  - "#type/technique"
  - "#type/best-practice"
  - "#domaine/claude-code"
---

## Tailles recommandées

| Source | Cible |
|---|---|
| Anthropic officiel | < 200 lignes |
| Boris Cherny (Claude Code team) | ~100 lignes, ~2.5k tokens |
| Communauté (alexop.dev, HumanLayer) | 40-60 lignes root, reste en skills/rules |

À 32K tokens (benchmark NoLiMa), les modèles tombent sous 50% de recall. Le CLAUDE.md est injecté à CHAQUE session → chaque token compte.

## Règle d'or — Boris

**"Anytime we see Claude do something incorrectly we add it to the CLAUDE.md."**
Mais aussi : **"Ruthlessly edit your CLAUDE.md over time."**

→ Le CLAUDE.md DOIT évoluer (add + prune), pas rester statique.

## Test de chaque ligne

**"Would removing this cause Claude to make mistakes? If not, cut it."**

## Quoi mettre où

| Contenu | Où | Pourquoi |
|---|---|---|
| Erreurs comportementales récurrentes de Claude | **CLAUDE.md gotchas** | Chargé à chaque session |
| Règles spécifiques à un type de fichier | **`.claude/rules/` avec `paths:`** | Chargé on-demand |
| Procédures multi-étapes | **Skills** | Chargé sur invocation |
| Erreurs techniques (skill config, RAG, prompt) | **Vault Knowledge/erreurs/** | Consulté via MCP |
| Formatting, linting, types | **Hooks + outils** | Enforcement > prose |

## Anti-patterns documentés

1. **Context Stuffing** — CLAUDE.md > 10K tokens = instructions ignorées
2. **Static Memory** — jamais mis à jour = drift avec la réalité
3. **Tools in prose** — écrire "use ruff format" au lieu de configurer un hook PostToolUse
4. **Over-specification** — au-delà S* = 0.509, dégradation quadratique (UCL 2601.00880)

## Mécanisme de maintenance

- **Ajout** : quand Claude fait la même erreur 2 fois, ou quand un code review attrape quelque chose
- **Suppression** : quand Claude fait déjà bien sans l'instruction, ou quand un hook/tool enforce la règle
- **Audit mensuel** : via `/forge-review` (tâche planifiée)
- **Claude écrit ses propres règles** : "Update your CLAUDE.md so you don't make that mistake again"
- **HTML comments `<!-- -->` = 0 tokens** : maintainer notes sans coût

## Liens

- [[over-specification-paradox]]
- [[harness-engineering]]
- [[best-practices-claude-code-leaders]]
- [[Workflow Boris]]
