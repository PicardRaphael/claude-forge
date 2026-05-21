---
titre: "Synthèse audit cohérence neo_ia + ia_back — Mai 2026"
resume: "Audit cross-référence complet des 2 repos : 67 problèmes trouvés (9 critiques), pattern skills orphelines dans frontmatter, rules mortes sans frontmatter, credentials trackés"
aliases:
  - "audit coherence neo_ia ia_back"
  - "audit skills agents cross-reference"
  - "audit TDD repos 2026"
  - "coherence audit mai 2026"
  - "audit skills orphelines"
type: knowledge
domaine: claude-code
derniere-maj: 2026-05-21
auteur: claude
tags:
  - "#type/synthese"
  - "#domaine/claude-code"
  - "#projet/neo_ia"
  - "#projet/ia_back"
sources:
  - "Session 2026-05-21 — audit cohérence post-TDD"
---

## Patterns découverts (réutilisables sur tout repo)

### 1. Skills frontmatter orphelines (WARNING le plus fréquent)

**Pattern** : skill listée dans `skills:` du frontmatter d'un agent mais JAMAIS mentionnée dans le body.
**Impact** : la skill est injectée en contexte (consomme du budget tokens) mais l'agent ne sait pas quand/comment l'utiliser → injection inutile.
**Fréquence** : 11/16 agents ia_back, 6/12 agents neo_ia.
**Fix** : ajouter une instruction d'usage par skill dans le body ("Consulter `neo-brain-dev-ia` pour le contexte métier avant toute opération touchant un domaine fonctionnel").
**Checklist** : `skills-referenced-in-body` feedback déjà documenté, mais pas systématiquement appliqué.

### 2. Rules mortes (sans frontmatter `description:`)

**Pattern** : fichier `.md` dans `.claude/rules/` sans bloc `---\ndescription: ...\n---`. Claude Code ne charge pas la rule → morte silencieusement.
**Fréquence** : 2 rules identiques sur les 2 repos (`agents-color-convention`, `outcomes-after-architect`).
**Fix** : toujours vérifier que chaque rule a un frontmatter avec `description:`.
**Checklist** : ajouter dans le pipeline de création de rules.

### 3. Fichiers sensibles trackés malgré .gitignore

**Pattern** : fichier ajouté au .gitignore APRÈS avoir été commité. Git continue de le tracker.
**Fréquence** : `settings.local.json` (2 repos), `.mcp.json` (ia_back).
**Fix** : `git rm --cached <fichier>` pour untracker, puis commit.

### 4. Hook orphelin (existe mais pas dans settings.json)

**Pattern** : fichier dans `.claude/hooks/` qui n'est référencé par aucun événement dans `settings.json`.
**Fréquence** : `pipeline-reset` sur les 2 repos.
**Fix** : soit ajouter dans settings.json, soit supprimer.

## Résultats chiffrés

| Repo | Agents | Skills | Rules | Hooks | Critiques | Warnings |
|------|--------|--------|-------|-------|-----------|----------|
| ia_back | 16 | 26 | 16 | 14 | 4 | 14 |
| neo_ia | 12 | 25 | 16 | 12 | 5 | 19 |

## Ce qui est solide (les deux repos)

- 100% `memory: project` sur tous les agents
- 100% `permissionMode` configuré
- 0 agent orchestrateur (pas d'outil Agent dans les subagents)
- Read-only agents ont `disallowedTools: Write, Edit`
- Pipeline TDD cohérent entre rules/agents/CLAUDE.md
- Skills < 500L, kebab-case, pas de README.md

## Liens

- [[critique-2026-05-21-tdd-optimizations-handshake]] — critique DA des optimisations TDD
- [[erreur-claude-agent-env-var-dead-code]] — erreur dispatch-guard associée
- [[raisonnement-hook-agent-detection-method]] — raisonnement agent_type confirmé
