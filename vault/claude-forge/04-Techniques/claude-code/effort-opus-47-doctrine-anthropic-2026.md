---
aliases:
  - effort Opus 4.7 doctrine
  - xhigh default Anthropic
  - effort level Claude Code 2026
  - adaptive thinking Opus 4.7
  - low medium high xhigh max
  - effort recommandation officielle
resume: "Doctrine effort Anthropic 2026 — scale low→medium→high→xhigh→max. La recommandation de DÉPART dépend du modèle : xhigh pour Opus 4.7/4.8 coding-agentic, high pour Opus 5 / Fable 5.1 / Sonnet 5, et AUCUNE pour Opus 5.5 (alias opus depuis le 22 sept. 2026, défaut API medium, « run an effort sweep »). Pivot 25 sept. : forge garde high explicite comme choix délibéré, sweep Opus 5.5 à n=3 avant de bouger un frontmatter."
derniere-maj: 2026-09-25
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

## Recommandation officielle Anthropic — DÉPEND DU MODÈLE (corrigé 29 juil. 2026)

⚠️ Il n'y a **pas** de recommandation unique : la page officielle [Effort](https://platform.claude.com/docs/en/build-with-claude/effort) donne une consigne **par modèle**, et elle a changé avec Opus 5. La version précédente de cette section affirmait « Coding / agentic : start `xhigh` » sans distinction de modèle — **c'était faux depuis le 24 juillet 2026**.

| Modèle | Point de départ officiel | Verbatim |
|--------|--------------------------|----------|
| Opus 4.7 **et** 4.8 | **`xhigh`** pour coding/agentic | « **Start with `xhigh` for coding and agentic use cases**, use `high` for most other intelligence-sensitive workloads » |
| **Opus 5** (défaut CC depuis 24 juil. 2026) | **`high`** (le défaut) | « **Start with `high`, the default**, and adjust based on your evals: step up to `xhigh` for demanding coding and agentic work, or to `max` when a task justifies unconstrained token spending, and use `low` and `medium` **liberally as your primary control** for token cost and response time wherever your evals show quality holds. » |
| Fable 5 (+ Mythos 5) | **`high`** | « Start with `high`, the default, for most tasks » · « Lower effort settings on Claude Fable 5 still perform well and often exceed `xhigh` performance on prior models. » |
| Sonnet 5 | **`high`** (défaut) | `xhigh` réservé « for the hardest coding and agentic tasks » |

**La phrase qui vise directement forge** :

> « **If you carried effort settings over from an earlier model, run a fresh effort sweep on your evals rather than reusing them.** »

C'est littéralement la situation de forge : la grille Option C a été calibrée à l'ère Opus 4.7/4.8, puis reconduite sur Opus 5 sans re-mesure.

**Ce qui change / ce qui ne change pas** :
- ❌ **Périmé** : `xhigh` comme *point de départ* de l'agentique/coding sur Opus 5.
- ✅ **Toujours valide** : calibrer par TYPE de tâche, et forcer un effort explicite plutôt que subir l'adaptatif. `xhigh` reste un **step-up mesuré** (« demanding coding and agentic work »), pas un défaut.
- 🔎 **Levier neuf non exploité par forge** : `low`/`medium` sont désignés « primary control » du coût sur Opus 5.

Autres faits de la même page, spécifiques à Opus 5 : **thinking non désactivable** à `xhigh`/`max` (requête `thinking: disabled` → **erreur 400**, ce qui confirme en primaire le point marqué « à re-vérifier » plus bas) ; `max_tokens` ≥ 64k à `xhigh`/`max` ; l'effort **ne raccourcit pas** la réponse visible (« changing effort does not reliably shorten responses, so prompt for length instead »).

Vérifié en session principale le 29 juil. 2026 par lecture directe de la page officielle (`platform.claude.com/docs/en/build-with-claude/effort`).

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

### ⚠️ Ligne `repo-inspector` du tableau ci-dessus : **`xhigh` est MESURÉ FAUX** (5 sept. 2026)

La cellule « repo-inspector (audit/analyze/scan) | **xhigh** » est **périmée** : elle date de la
grille Opus 4.7 et a été reconduite sur Opus 5 sans re-mesure — exactement ce qu'Anthropic
interdit. Valeur en vigueur : **`high`**. Le fichier `.claude/agents/repo-inspector.md` porte
désormais `effort: high`.

## ⚠️ Opus 5.5 (22 sept. 2026) — plus de point de départ officiel, `high` devient un choix (pivot du 25 sept.)

L'alias `opus` résout vers [[Opus 5.5]] depuis CC v2.1.280. Verbatim page Effort : *« `medium` is the default (Claude Opus 5 and earlier Opus models default to `high`, so a request that omits `effort` runs one level lower than it did on Claude Opus 5) … Run an effort sweep on your own evals rather than carrying settings over from an earlier model »*. Aucune phrase « Start with … » pour ce modèle.

| Modèle | Défaut API | Point de départ officiel |
|---|---|---|
| **Opus 5.5** (alias `opus` depuis 22 sept.) | **`medium`** | **aucun** — sweep sur ses évals |
| Opus 5 (legacy) | `high` | `high` |
| Fable 5.1 | `high` | `high` |
| Sonnet 5 | `high` | `high` |

Doctrine forge après pivot (validé par Raphaël le 25 sept.) : les frontmatters **gardent `effort: high` explicite**, comme **choix délibéré** et non plus comme « défaut officiel » ; un composant sans `effort:` tourne en `medium` sur Opus ; **aucun frontmatter ne bouge avant un sweep Opus 5.5 à n=3 runs par niveau** (`medium` vs `high`), même protocole que ci-dessous. Les phrases de cette note qui disent « `high` est le point de départ officiel » valent pour Opus 5, Fable 5.1 et Sonnet 5, **plus pour l'alias `opus`**. Raisonnement : [[raisonnement-2026-09-25-effort-opus-5-5]].

## Sweep Opus 5 — 5 septembre 2026 (mesuré, n=1 par niveau)

Premier sweep exécuté depuis l'avertissement « run a fresh effort sweep ». Répond au manque
signalé depuis le 29 juillet.

### Protocole reproductible

Une seule variable change : l'effort. Même agent, même cible, même prompt, trois niveaux.

1. **Véhicule** : un agent read-only (`disallowedTools: Write, Edit`) — rejouable sans risque.
2. **Cible fixe et bornée**, identique aux trois runs. Consistance > étendue.
3. **Sortie imposée** : écarts `fichier:ligne`, total par sévérité, et surtout **la liste des
   fichiers lus EN ENTIER vs partiellement** — c'est cette colonne qui discrimine l'effort,
   pas le nombre de findings.
4. **Prompt gelé, erreurs comprises** : le brief annonçait « 9 fichiers » pour 12 réels. Ne pas
   le corriger entre deux runs — l'erreur conservée devient un discriminant (repérer et corriger
   le périmètre annoncé est un comportement d'effort élevé).
5. **Critère de décision** : un fichier lu en plus qui **change la conclusion**, pas une réponse
   plus longue.

### Résultats — audit de `.claude/rules/` (12 fichiers, 710 lignes)

| Effort | Écarts (C/I/S) | Cibles lues en entier | Tokens | Durée |
|---|---|---|---|---|
| `xhigh` | 19 (1/10/8) | 12/12 | 154 773 | 9,3 min |
| `high` | 13 (1/7/5) | 12/12 | 136 135 | 6,7 min |
| `medium` | 11 (1/5/5) | 12/12 | 123 917 | 12,1 min |

**Les trois niveaux tiennent la couverture de lecture, et les trois repèrent l'erreur de périmètre
du brief.** Aucun fichier lu en plus à `xhigh`, aucune conclusion changée par le surcoût.

**Le résultat le plus solide n'est pas le classement, c'est la variance** : chaque niveau trouve un
CRITIQUE *différent* et les trois ne se recouvrent qu'à moitié. `xhigh` remonte les rules eager ;
`high` une contradiction entre deux rules ; `medium` l'écart doctrine↔code le plus actionnable.
Le nombre d'écarts décroît avec l'effort mais **la gravité, non** — l'effort supplémentaire achète
du volume de suggestions de style, pas de la profondeur de jugement.

### Verdict et sa limite

`repo-inspector` passe à **`high`**, pas à `medium` : n=1 par niveau avec une variance inter-runs
élevée ne suffit pas à descendre de deux crans sur un agent de **jugement**, l'Option C réserve
`medium`/`low` au mécanique, et `high` est le point de départ officiel Opus 5. Bouger un réglage
sur une observation unique serait le raisonnement même que ce sweep discipline.

Ce sweep **ne dit pas** que `medium` serait insuffisant — il dit que rien ne prouve qu'il soit
meilleur. Une descente reste ouverte contre 3 runs par niveau.

Les 27 autres composants à `high` restent inchangés : déjà au point de départ recommandé, donc
aucun écart à corriger. `python-ref` et `vault-health` restent à `medium` (inspection mécanique).

**Axe Fable 5.1 : sans objet** — aucun composant du parc ne déclare ce modèle (10 `opus`,
12 `sonnet`). Le sweep n'étant pas transférable entre modèles, il devra être refait si un
composant y bascule.

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
⚠️ **Correction 29 juil. 2026** — cette section concluait « la doctrine forge *effort calibré par TYPE* reste valide telle quelle pour Opus 5 ». **Partiellement faux** : le *principe* de calibrage par type reste valide, mais son **point de départ** ne l'est plus. La page officielle Effort recommande pour Opus 5 « Start with `high`, the default » (et non `xhigh`), et ajoute « If you carried effort settings over from an earlier model, run a fresh effort sweep on your evals rather than reusing them » — ce qui décrit exactement la grille Option C reconduite sans re-mesure. Le point « thinking disabled + xhigh/max → 400 », marqué ici comme source secondaire à re-vérifier, est **confirmé en primaire**. Voir la section « Recommandation officielle Anthropic — DÉPEND DU MODÈLE » en haut de cette note.

## Formalisation OFFICIELLE de la doctrine effort × modèle (Lydia Hallie, 7 juillet 2026)

Post « Claude Code effort level and model selection » — **Lydia Hallie (MTS équipe CC), claude.com/blog** (source primaire, crédit MAX ; antérieur à Opus 5, cite Opus 4.7/4.8). Première formalisation officielle de ce que forge maintenait empiriquement :

- **Modèle = plafond de capacité** (swap de poids gelés) ; **effort = quantité de travail par tour** — verbatim : « how much work Claude does on your request overall » (fichiers lus, outils, étapes avant de rendre la main — pas seulement la profondeur de thinking).
- **Grille modèles** : « Fable is a specialist… Opus is the expert… Sonnet is a really good generalist. » (Fable = problèmes inédits/tâches longues multi-étapes ; Opus = tâches ambiguës/domaines inconnus ; Sonnet = travail routinier précisément décrit.)
- **Règle de troubleshooting** : « **did it not try hard enough, or did it not know enough?** » — erreur par fichiers sautés/vérification manquante → monter l'**effort** ; erreur malgré contexte complet et vraie tentative → monter de **modèle**. « Start with the defaults, then reach for the dials. » Effort = préférence générale, pas toggle par tâche.

**Verdict doctrine : REINFORCE** — valide « Sonnet exécution / Opus jugement » + « effort calibré par TYPE ». La règle try-vs-know est le critère officiel pour arbitrer bump d'effort vs bump de modèle avant toute modification de frontmatter agent.

Source : https://claude.com/blog/claude-model-and-effort-level-in-claude-code · Fiche [[Lydia Hallie]].
