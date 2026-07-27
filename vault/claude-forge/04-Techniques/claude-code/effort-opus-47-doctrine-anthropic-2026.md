---
aliases:
  - effort Opus 4.7 doctrine
  - xhigh default Anthropic
  - effort level Claude Code 2026
  - adaptive thinking Opus 4.7
  - low medium high xhigh max
  - effort recommandation officielle
resume: "Doctrine effort Anthropic 2026 — scale low→medium→high→xhigh→max. xhigh = défaut CC à l'ère Opus 4.7 ; high = défaut recommandé depuis Opus 4.8 (reconduit par Opus 5). xhigh 71% @ 100k vs max 74.5% @ 200k. Doctrine forge Option C : effort explicite calibré par TYPE (xhigh agentique, high jugement, medium/low mécanique)."
derniere-maj: 2026-07-27
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#statut/canonique"
---
# Effort — doctrine officielle Anthropic 2026 (lignée Opus 4.7 → 4.8 → 5)

## Le défaut effort par ère

Le scale complet, introduit avec Opus 4.7 : **low → medium → high → xhigh → max** (`xhigh` = niveau ajouté entre `high` et `max`).

| Ère | Défaut Claude Code | Source |
|-----|--------------------|--------|
| Opus 4.7 (avril-mai 2026) | **xhigh** (monté sur tous les plans) | annonce Opus 4.7 |
| Opus 4.8 (depuis 28 mai 2026) | **high** (recommandé) | annonce Opus 4.8, cf [[CC 28 mai 2026 - Opus 4.8 + Dynamic Workflows]] |
| [[Opus 5]] (depuis 24 juil. 2026) | **high** — ladder reconduit sans changement de sémantique | annonce Opus 5 |

La doctrine forge (Option C, ci-dessous) est indépendante de ce défaut : elle **force un effort explicite calibré par type de tâche** au lieu de subir le défaut adaptatif.

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

`max` n'est pas un défaut. **Adaptive thinking + xhigh ≈ max sans le coût**.

## Adaptive thinking

Depuis Opus 4.7 : `thinking: {type: "adaptive"}`. Effort = contrôle recommandé pour la profondeur de réflexion.

Niveaux et thinking depth :
- `high`, `xhigh`, `max` : Claude pense profondément quasi toujours
- `medium`, `low` : peut skip thinking pour problèmes simples

**Important** : manual extended thinking (`thinking: {type: "enabled", budget_tokens: N}`) **n'est plus supporté** depuis Opus 4.7. Utiliser adaptive thinking + effort.

## Pratique

- `max_tokens` : start 64k pour laisser room pour thinking + tool calls
- `xhigh` sur trivial = waste (adaptive thinking tourne longtemps sur prompts ambigus)
- Toggle effort dynamique OK : start xhigh, mur → bump max 1 step → revert xhigh
- Beaucoup de workloads `max` peuvent passer `xhigh` sans perte qualité

## Performance Opus 4.7

`low` Opus 4.7 ≈ `medium` Opus 4.6. À chaque niveau, 4.7 > 4.6.

## Implications forge

### Doctrine forge actualisée — Option C (arbitrée 18 juin 2026)

`xhigh` = agentique/coding multi-tool long-horizon · `high` = jugement/comparatif structuré · `medium`/`low` = scan/extraction · `max` = ponctuel, jamais en frontmatter. Source de la décision : [[conflit-effort-xhigh-anthropic-vs-pivot-22mai]] (résolue).

| Agent forge type | Effort recommandé |
|------------------|-------------------|
| Créateurs (skill-creator, agent-creator, hook-creator, claudemd-optimizer) | **xhigh** |
| Analyseurs (project-auditor, project-analyzer, codebase-scanner) | **xhigh** |
| Reviewers (devils-advocate, outcomes-grader) | **high** (Option C — jugement structuré) |
| Conseil stratégique (responsable-ia) | **xhigh** ou `max` ponctuel sur décisions majeures |
| Exécutants pure (python-dev) | **high** (intelligence-sensitive) |
| Workers triviaux | **medium** |

### Composants forge actuels (post-pivot agents → skills, 6 juin 2026)

| Composant forge | Effort recommandé |
|---|---|
| Skills créatrices (skill-creator, subagent-creator, hook-creator, claudemd-creator) | **high** (thread principal, pas agent Opus) |
| repo-inspector (audit/analyze/scan) | **xhigh** |
| devils-advocate | **high** (Option C — reviewer) |
| outcomes-grader | **high** |
| code-dev | **high** |
| self-updater | **high** |
| responsable-ia (skill) | **xhigh** ou `max` ponctuel |

python-dev → code-dev. agent-creator / hook-creator / claudemd-optimizer → skills (pas d'effort frontmatter agent).

Fichiers alignés sur cette grille : `CLAUDE.md` forge (ligne effort) · `feedback_allocation_modele_effort` mémoire · [[workflow-claude-code-optimal]] · [[comment-creer-agent]].

## Anti-pattern : double thinking archi → dev

**Jamais deux Opus xhigh en chaîne** sur la même feature (architect → dev). Si l'architecte (Opus xhigh) produit un plan détaillé, le dev qui re-raisonne profondément refait un travail déjà fait → double facturation thinking, redondant.

**Règles vérifiées empiriquement (ia_back, neo_ia)** :
1. Archi Opus xhigh → plan/spec/contrats. Dev **Sonnet high** → exécution du plan.
2. Si trop complexe pour Sonnet → **1 SEUL agent Opus xhigh** (archi + code, pattern dev-lead). Pas de délégation Opus→Opus.
3. **Anti-pattern à détecter** : `dev-*.md` avec `model: opus` + `effort: xhigh` appelé après un `architect-*.md` Opus → revoir.

- [[workflow-claude-code-optimal]] — patterns chain architect/dev

## Liens

- [[conflit-effort-xhigh-anthropic-vs-pivot-22mai]] — décision Option C (résolue 18 juin, arbitrage Raphael)
- [[critique-2026-07-27-plan-audit-regles-forge]] — le DA qui a détecté le drift des cellules Reviewers (corrigées 27 juil.)
- [[methode-pivoter-doctrine]] — méthode pour propager un pivot
- [[workflow-claude-code-optimal]] · [[comment-creer-agent]]

## Référence

- [Anthropic news Opus 4.7](https://www.anthropic.com/news/claude-opus-4-7)
- [Claude API effort docs](https://platform.claude.com/docs/en/build-with-claude/effort)
- [Claude Code model config](https://code.claude.com/docs/en/model-config)
- [Apiyi xhigh practical guide](https://help.apiyi.com/en/claude-opus-4-7-xhigh-effort-mode-explained-en.html)
- [ClaudeFast Opus 4.7 best practices](https://claudefa.st/blog/guide/development/opus-4-7-best-practices)

## Challengée + confirmée (2026-07-02)

Un scan cc-news a remonté une controverse : effort par défaut de Claude Code silencieusement baissé (high→medium, ~3 mars 2026), réponses superficielles (SHAs de commit et noms de packages fabriqués). **Boris Cherny (Anthropic, crédit MAX) a confirmé que certains tours allouaient ZÉRO token de raisonnement.**

**Verdict `doctrine-impact-check` : DOCTRINE_REINFORCE.** La controverse porte sur le fait de SUBIR le default adaptatif (Opus 4.6, medium implicite), pas sur `xhigh` demandé explicitement. Elle valide donc la doctrine forge : **forcer un effort explicite calibré par type plutôt que subir l'adaptatif silencieux**. Les chiffres « Opus 4.6 pense 67 % moins / analyse 6852 sessions » viennent d'agrégateurs (pasqualepillitteri.it, medium) — non vérifiés en primaire, **ne pas citer**. Seul le point Boris Cherny (zéro token) est de crédit MAX.

## Opus 5 (24 juillet 2026) — ladder inchangé, thinking ON par défaut

[[Opus 5]] (`claude-opus-5`, nouveau défaut Opus dans CC v2.1.219 et défaut Claude Max) reconduit le ladder **low / medium / high / xhigh / max** sans changement de sémantique. Deux points neufs :

- **Thinking ON par défaut** (comme la lignée adaptive thinking 4.7/4.8) ; ⚠️ breaking migration : `thinking: disabled` combiné à effort **xhigh/max** → **erreur 400** (source secondaire, à re-vérifier docs plateforme avant de câbler en prod).
- **Fast mode** : Opus 5 à $10/$50 par MTok (~2,5× la vitesse) ; **Opus 4.7 retiré du fast mode** (`speed: "fast"` → erreur, pas de fallback) — fast = Opus 5 + Opus 4.8 uniquement.

La doctrine forge « effort calibré par TYPE de tâche » reste valide telle quelle pour Opus 5.

## Formalisation OFFICIELLE de la doctrine effort × modèle (Lydia Hallie, 7 juillet 2026)

Post « Claude Code effort level and model selection » — **Lydia Hallie (MTS équipe CC), claude.com/blog** (source primaire, crédit MAX ; antérieur à Opus 5, cite Opus 4.7/4.8). Première formalisation officielle de ce que forge maintenait empiriquement :

- **Modèle = plafond de capacité** (swap de poids gelés) ; **effort = quantité de travail par tour** — verbatim : « how much work Claude does on your request overall » (fichiers lus, outils, étapes avant de rendre la main — pas seulement la profondeur de thinking).
- **Grille modèles** : « Fable is a specialist… Opus is the expert… Sonnet is a really good generalist. » (Fable = problèmes inédits/tâches longues multi-étapes ; Opus = tâches ambiguës/domaines inconnus ; Sonnet = travail routinier précisément décrit.)
- **Règle de troubleshooting** : « **did it not try hard enough, or did it not know enough?** » — erreur par fichiers sautés/vérification manquante → monter l'**effort** ; erreur malgré contexte complet et vraie tentative → monter de **modèle**. « Start with the defaults, then reach for the dials. » Effort = préférence générale, pas toggle par tâche.

**Verdict doctrine : REINFORCE** — valide « Sonnet exécution / Opus jugement » + « effort calibré par TYPE ». La règle try-vs-know est le critère officiel pour arbitrer bump d'effort vs bump de modèle avant toute modification de frontmatter agent.

Source : https://claude.com/blog/claude-model-and-effort-level-in-claude-code · Fiche [[Lydia Hallie]].
