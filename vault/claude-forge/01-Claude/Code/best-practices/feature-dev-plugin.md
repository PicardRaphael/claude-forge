---
titre: "feature-dev — Plugin officiel Anthropic pour le développement de features"
resume: "Plugin 7 phases avec 3 types d'agents spécialisés (explorer, architect, reviewer) en parallèle. Fait exploration + implémentation + review en une session. Auteur : Sid Bidasaria (Anthropic)"
aliases:
  - feature-dev
  - feature-dev plugin
  - plugin feature-dev
  - Sid Bidasaria plugin
  - claude code feature development
  - development plugin anthropic
domaine: claude-code
type: reference
derniere-maj: 2026-05-12
tags:
  - "#type/reference"
  - "#domaine/claude-code"
  - "#domaine/plugin"
auteur: claude
---

## Installation

```
/plugin install feature-dev@claude-plugins-official
```

## Pipeline 7 phases

| Phase | Action | Agents |
|-------|--------|--------|
| 1. Discovery | Clarifie la demande, identifie contraintes | — |
| 2. Codebase Exploration | Mappe le code existant | 2-3 `code-explorer` en // |
| 3. Clarifying Questions | Pose les questions APRÈS exploration | — |
| 4. Architecture Design | Propose 2-3 approches avec tradeoffs | 2-3 `code-architect` en // |
| 5. Implementation | Attend approbation explicite, code | — |
| 6. Quality Review | Review confidence-based (≥80%) | 3 `code-reviewer` en // |
| 7. Summary | Documente décisions, fichiers modifiés | — |

## 3 agents spécialisés

- **code-explorer** — trace les chemins d'exécution, mappe les layers d'architecture
- **code-architect** — propose des approches (minimal, clean, pragmatic) avec tradeoffs
- **code-reviewer** — findings confidence-scored, ne rapporte que les ≥80%

## Principes clés

- Understand before changing (phase 2 empêche l'implémentation aveugle)
- Eliminate ambiguity early (phase 3 empêche le rework)
- Design before building (phase 4 empêche les erreurs d'architecture)
- Exécution parallèle en phases 2, 4 et 6

## Différence avec /spec

feature-dev = explore + code + review **en une session** (dev solo).
/spec = produit des **artefacts collaboratifs persistants** (dossier TODO/) pour exécution multi-dev, multi-repo, multi-session.

Les deux sont complémentaires : /spec pour planifier → feature-dev ou /go pour exécuter.

## Ce qu'on a copié pour /spec

- Agents explorateurs en parallèle (phase 2)
- Questions APRÈS exploration (phase 3)
- Multi-approches architecture (phase 4)
- Filtrage confiance pour les recommandations

## Liens

- [[pattern-spec-driven-development]] — Pattern SDD complet
- [[methode-analyser-repo]] — Plugin dans le setup standard
- [[workflow-claude-code-optimal]] — Pipeline implémentation