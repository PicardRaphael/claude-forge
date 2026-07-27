---
aliases:
  - effort Opus 4.7 doctrine
  - xhigh default Anthropic
  - effort level Claude Code 2026
  - adaptive thinking Opus 4.7
  - low medium high xhigh max
  - effort recommandation officielle
resume: "Doctrine officielle Anthropic Opus 4.7 (2026) — xhigh = default Claude Code tous plans. Scale low→medium→high→xhigh→max. xhigh 71% @ 100k vs max 74.5% @ 200k. Trivial = medium/low."
derniere-maj: 2026-07-27
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#statut/canonique"
---
# Effort Opus 4.7 — doctrine officielle Anthropic 2026

## Default = xhigh

Depuis Opus 4.7, Anthropic a **fait monter le default de Claude Code à `xhigh` sur tous les plans**. Le scale complet :

**low → medium → high → xhigh → max**

`xhigh` est un nouveau niveau introduit entre `high` et `max`.

## Recommandation officielle Anthropic

- **Coding / agentic** : start `xhigh`
- **Intelligence-sensitive** : minimum `high`
- **Trivial** (classification, extraction, formatting, summaries) : `medium` ou `low`

## Données chiffrées (Anthropic Agentic Coding benchmark)

| Effort | Score | Tokens consommés |
|--------|-------|------------------|
| `xhigh` | ~71% | ~100k |
| `max` | ~74.5% | >200k |

**Gain max vs xhigh** : +3% pour 2x tokens. Rarement justifié.

`max` n'est plus le default. **Adaptive thinking + xhigh ≈ max sans le coût**.

## Adaptive thinking

Opus 4.7 utilise `thinking: {type: "adaptive"}`. Effort = contrôle recommandé pour profondeur de réflexion.

Niveaux et thinking depth :
- `high`, `xhigh`, `max` : Claude pense profondément quasi toujours
- `medium`, `low` : peut skip thinking pour problèmes simples

**Important** : manual extended thinking (`thinking: {type: "enabled", budget_tokens: N}`) **n'est plus supporté** sur Opus 4.7. Utiliser adaptive thinking + effort.

## Pratique

- `max_tokens` : start 64k pour laisser room pour thinking + tool calls
- `xhigh` sur trivial = waste (adaptive thinking tourne longtemps sur prompts ambigus)
- Toggle effort dynamique OK : start xhigh, mur → bump max 1 step → revert xhigh
- Beaucoup de workloads `max` peuvent passer `xhigh` sans perte qualité

## Performance Opus 4.7

`low` Opus 4.7 ≈ `medium` Opus 4.6. À chaque niveau, 4.7 > 4.6.

## Implications forge

### Doctrine forge actualisée (réalignée 26 mai 2026)

Remplace l'ancien pivot 22 mai ("high partout, xhigh réservé 3 rôles") par :

| Agent forge type | Effort recommandé |
|------------------|-------------------|
| Créateurs (skill-creator, agent-creator, hook-creator, claudemd-optimizer) | **xhigh** |
| Analyseurs (project-auditor, project-analyzer, codebase-scanner) | **xhigh** |
| Reviewers (devils-advocate, outcomes-grader) | **xhigh** |
| Conseil stratégique (responsable-ia) | **xhigh** ou `max` ponctuel sur décisions majeures |
| Exécutants pure (python-dev) | **high** (intelligence-sensitive) |
| Workers triviaux | **medium** |

### Anciens fichiers à mettre à jour

> ⚠️ **Mis à jour 6 juin 2026** — Tableau effort révisé après pivot agents → skills :

| Composant forge | Effort recommandé |
|---|---|
| Skills créatrices (skill-creator, subagent-creator, hook-creator, claudemd-creator) | **high** (thread principal, pas agent Opus) |
| repo-inspector (audit/analyze/scan) | **xhigh** |
| devils-advocate | **xhigh** |
| outcomes-grader | **high** |
| code-dev | **high** |
| self-updater | **high** |
| responsable-ia (skill) | **xhigh** ou `max` ponctuel |

python-dev → code-dev. agent-creator / hook-creator / claudemd-optimizer → skills (pas d'effort frontmatter agent).


- `CLAUDE.md` forge (ligne effort)
- `feedback_opus47_workflow` mémoire
- `vault/04-Techniques/claude-code/workflow-claude-code-optimal.md`
- `vault/04-Techniques/claude-code/comment-creer-agent.md`

## Anti-pattern : double thinking archi → dev

**Jamais deux Opus xhigh en chaîne** sur la même feature (architect → dev). Si l'architecte (Opus xhigh) produit un plan détaillé, le dev qui re-raisonne profondément refait un travail déjà fait → double facturation thinking, redondant.

**Règles vérifiées empiriquement (ia_back, neo_ia)** :
1. Archi Opus xhigh → plan/spec/contrats. Dev **Sonnet high** → exécution du plan.
2. Si trop complexe pour Sonnet → **1 SEUL agent Opus xhigh** (archi + code, pattern dev-lead). Pas de délégation Opus→Opus.
3. **Anti-pattern à détecter** : `dev-*.md` avec `model: opus` + `effort: xhigh` appelé après un `architect-*.md` Opus → revoir.

- [[workflow-claude-code-optimal]] — patterns chain architect/dev
## Liens

- [[conflit-effort-xhigh-anthropic-vs-pivot-22mai]] — résolution du conflit
- [[methode-pivoter-doctrine]] — méthode pour propager le pivot
- [[workflow-claude-code-optimal]] — à mettre à jour
- [[comment-creer-agent]] — à mettre à jour

## Référence

- [Anthropic news Opus 4.7](https://www.anthropic.com/news/claude-opus-4-7)
- [Claude API effort docs](https://platform.claude.com/docs/en/build-with-claude/effort)
- [Claude Code model config](https://code.claude.com/docs/en/model-config)
- [Apiyi xhigh practical guide](https://help.apiyi.com/en/claude-opus-4-7-xhigh-effort-mode-explained-en.html)
- [ClaudeFast Opus 4.7 best practices](https://claudefa.st/blog/guide/development/opus-4-7-best-practices)

## Challengée + confirmée (2026-07-02)

Un scan cc-news a remonté une controverse : effort par défaut de Claude Code silencieusement baissé (high→medium, ~3 mars 2026), réponses superficielles (SHAs de commit et noms de packages fabriqués). **Boris Cherny (Anthropic, crédit MAX) a confirmé que certains tours allouaient ZÉRO token de raisonnement.**

**Verdict `doctrine-impact-check` : DOCTRINE_REINFORCE.** La controverse porte sur le fait de SUBIR le default adaptatif (Opus 4.6, medium implicite), pas sur `xhigh` demandé explicitement. Elle valide donc la doctrine forge : **forcer un effort explicite calibré par type plutôt que subir l'adaptatif silencieux**. Les chiffres « Opus 4.6 pense 67 % moins / analyse 6852 sessions » viennent d'agrégateurs (pasqualepillitteri.it, medium) — non vérifiés en primaire, **ne pas citer**. Seul le point Boris Cherny (zéro token) est de crédit MAX.


---

## AJOUT 27 juillet 2026 — Opus 5 : thinking ON par défaut, ladder effort inchangé

[[Opus 5]] (24 juil. 2026, `claude-opus-5`, nouveau défaut Opus dans CC v2.1.219 et défaut Claude Max) reconduit le ladder **low / medium / high / xhigh / max** sans changement de sémantique. Deux points neufs :

- **Thinking ON par défaut** (comme la lignée adaptive thinking 4.7/4.8) ; ⚠️ breaking migration : `thinking: disabled` combiné à effort **xhigh/max** → **erreur 400** (source secondaire, à re-vérifier docs plateforme avant de câbler en prod).
- **Fast mode** : Opus 5 à $10/$50 par MTok (~2,5× la vitesse) ; **Opus 4.7 retiré du fast mode** (`speed: "fast"` → erreur, pas de fallback) — fast = Opus 5 + Opus 4.8 uniquement.

La doctrine forge « effort calibré par TYPE de tâche » (xhigh agentique profond, high comparatif/jugement, medium mécanique) reste valide telle quelle pour Opus 5.
