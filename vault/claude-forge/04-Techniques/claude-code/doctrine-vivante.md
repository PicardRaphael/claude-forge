---
titre: "Doctrine vivante — la doctrine forge doit être challengée par le monde extérieur"
resume: "Principe canonique : la doctrine forge évolue non seulement par l'erreur interne (CLAUDE.md DOIT évoluer) mais par le signal externe à fort crédit (Anthropic officiel, leaders reconnus du vault). Un finding dirigé produit un de trois verdicts — INFO, DOCTRINE_PIVOT_CANDIDATE, DOCTRINE_REINFORCE — avec gate humaine systématique. Scan aveugle interdit (puits sec mesuré 0/12)."
aliases:
  - "doctrine vivante"
  - "living doctrine"
  - "doctrine challengée externe"
  - "pont veille doctrine"
  - "doctrine challenge externe leaders"
  - "doctrine évolutive forge"
domaine: claude-code
type: technique
derniere-maj: 2026-05-28
auteur: claude
sources:
  - "Chantier A — pont veille → doctrine (27 mai 2026)"
  - "[[critique-2026-05-27-compounding-retroactif]]"
  - "[[methode-pivoter-doctrine]]"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/doctrine"
  - "#doctrine/2026"
---
# Doctrine vivante

La doctrine forge n'est pas un socle figé. Elle évolue. Jusqu'ici, le moteur d'évolution documenté était **interne** : « CLAUDE.md DOIT évoluer » (ajouter après chaque erreur, supprimer le redondant). Cette note pose le moteur **externe** : la doctrine doit aussi être challengée par le monde extérieur, et Claude doit proposer des pivots de façon proactive quand il observe une contradiction avec une source à fort crédit.

C'est l'extension du local (l'erreur que JE commets) au global (ce que le monde apprend avant moi).

## Principe

Une doctrine non challengée se sédimente. Le risque n'est pas qu'elle soit fausse au moment où on l'écrit — c'est qu'elle reste en place après que le terrain a bougé (nouveau modèle qui rend obsolète un scaffolding, best practice publiée qui contredit un pattern forge, mesure empirique qui invalide une prémisse). Le moteur interne ne capte pas ces dérives : on ne fait pas l'erreur soi-même, donc rien ne se déclenche.

Le moteur externe comble ce trou : un signal à fort crédit qui contredit ou renforce une note canonique déclenche une **proposition** de mise à jour doctrinale, soumise à arbitrage humain.

## Sources de challenge légitimes

| Source | Crédit | Exemple |
|--------|--------|---------|
| Anthropic officiel | Maximal sur Claude / Claude Code | docs, changelog, blog research, équipe (Boris Cherny, Thariq, Lisa Crofoot) |
| Leaders reconnus du vault | Élevé sur leur domaine | `05-Leaders/` — Karpathy, Hashimoto, Böckeler, Simon Willison, etc. |
| Mesure empirique forge | Décisive | probe sur transcripts, audit, test adverse |

**Pas une source légitime** : tweet random, article tiers paraphrasant Anthropic sans lien primaire, hype non vérifiée (cf [[feedback_tweet_hype_paraphrase_pattern]]). Le crédit se vérifie : sur Claude, Anthropic est single source ([[feedback_anthropic_single_source]]) ; sur un domaine large, consensus multi-sources (skill `web-search-canonical-source`).

## Mécanisme — trois verdicts

Un finding dirigé (URL d'un leader, conclusion d'un run `cc-news`, mesure) est croisé avec les notes canoniques `04-Techniques/claude-code/`. Il produit **un** de trois verdicts :

| Verdict | Signification | Action |
|---------|---------------|--------|
| `INFO` | Fait nouveau, sans impact doctrinal | Capitaliser comme note de fait (comportement `cc-news` actuel). Aucun pivot. |
| `DOCTRINE_PIVOT_CANDIDATE` | Le finding **contredit** une doctrine canonique | Pré-remplir un brouillon argumenté (doctrine actuelle, source externe, position proposée) → gate `[v]alider / [m]odifier / [i]gnorer`. `[v]` lance [[methode-pivoter-doctrine]]. |
| `DOCTRINE_REINFORCE` | Le finding **confirme** une doctrine canonique | Tracer « challengée + confirmée le {date} par {source} ». Renforce la confiance, pas de pivot. |

Implémentation : skill `doctrine-impact-check`.

## Anti-pattern cardinal — modification automatique interdite

Aucun mécanisme ne modifie une note de doctrine canonique sans validation humaine explicite. Même sur un signal Anthropic officiel fort, la gate `[v]/[m]/[i]` est non négociable. La doctrine appartient à Raphaël ; le mécanisme propose, l'humain tranche.

Le verdict `DOCTRINE_PIVOT_CANDIDATE` produit un **brouillon à lire**, jamais un pivot enclenché. [[methode-pivoter-doctrine]] (5 étapes, structurante) n'est lancée qu'après `[v]`.

## Anti-pattern — scan aveugle

Le challenge est **dirigé**, jamais aveugle. Un finding précis entre ; le mécanisme le croise avec les canoniques. Il n'existe pas de scan systématique de l'historique « au cas où » : la prémisse « les transcripts contiennent un gisement d'apprentissages dormants » a été mesurée fausse (probe 0/12 sur la slice la plus chargée en signal, [[critique-2026-05-27-compounding-retroactif]]). Le puits est sec ; aucun resserrement d'heuristique ne ramène du contenu qui n'existe pas. Et un scan rétroactif aveugle ressusciterait de la doctrine périmée (risque d'obsolescence temporelle).

Déclenchement légitime : URL collée par Raphaël, finding majeur d'un run `cc-news`, mesure empirique. Toujours un signal explicite, jamais un balayage.

## Cadence

Continu et événementiel — à chaque `cc-news` (étape 8 sur les findings majeurs), à chaque input externe d'une source à fort crédit. Pas de scan périodique programmé.

## Lien avec l'existant

- Étend « CLAUDE.md DOIT évoluer » (moteur interne, erreur) au moteur externe (signal du monde).
- S'appuie sur [[methode-pivoter-doctrine]] pour exécuter un pivot validé sans drift résiduel (5 étapes).
- Complémentaire de la skill `pivot-check` (détecte le drift résiduel **après** un pivot) — ici on est **avant** : détecter qu'un pivot est *nécessaire*.

## Wikilinks

- [[methode-pivoter-doctrine]] — exécute un pivot validé (5 étapes, anti-drift)
- skill `pivot-check` — détecte le drift résiduel post-pivot (aval ; ici = amont)
- [[critique-2026-05-27-compounding-retroactif]] — pourquoi le scan aveugle est interdit (0/12)
- [[raisonnement-22mai-doctrine-vs-enforcement]] — exemple de pivot déclenché par signal externe (Boris, Agent SDK)
- [[comment-ecrire-claudemd]] — « CLAUDE.md DOIT évoluer » (moteur interne étendu ici)
- [[methode-analyser-repo]] — séquence A→B→C→D→E (croiser réel ⨯ canoniques)


## Sources d'inspiration

Le pattern doctrine vivante (signal externe → verdict {INFO, DOCTRINE_PIVOT_CANDIDATE, DOCTRINE_REINFORCE} → gate humaine) ne sort pas du néant. Il transpose deux corpus académiques et industriels établis en doctrine personnelle opérationnelle :

- **PIVOT: Bridging Planning and Execution in LLM Agents via Trajectory Refinement** — Tuo Zhang, Alin-Ionut Popa, Yan Xu, Rui Song, Dimitrios Dimitriadis (arXiv:2605.11225, mai 2026). Framework PLAN → INSPECT → EVOLVE → VERIFY pour corriger les écarts entre planification et exécution dans les agents LLM. Trajectoires traitées comme objets optimisables, raffinées par interaction avec l'environnement. Le mécanisme INSPECT (détecter un écart entre prévu et observé) → EVOLVE (proposer un ajustement) → VERIFY (valider avant intégration) inspire directement le pipeline `finding externe → verdict → gate`.

- **Architecture Decision Records (ADR)** — Michael Nygard, *Documenting Architecture Decisions* (2011). Capture les décisions structurantes avec leur contexte, leurs alternatives écartées, et le verdict. L'ADR introduit la notion qu'une décision peut être *superseded* par une décision ultérieure traçable. La doctrine vivante applique le même principe au corpus canonique forge : une note canonique peut être pivotée, et le pivot trace contexte + source + verdict.

**Transposition opérationnelle (adaptation Raphaël)** :
- Le gate humain typé `[v]alider / [m]odifier / [i]gnorer` (vs choix binaire accept/reject) est forge-spécifique.
- Le triplet de verdicts INFO / PIVOT_CANDIDATE / REINFORCE (vs binaire pertinent/non) est forge-spécifique.
- L'interdiction du scan aveugle (puits sec mesuré 0/12, [[critique-2026-05-27-compounding-retroactif]]) est une contribution empirique forge non présente dans les deux sources.
- L'intégration avec [[methode-pivoter-doctrine]] (5 étapes anti-drift résiduel) ne figure dans aucune source externe.

Le pattern forge = PIVOT (mécanisme inspect/evolve) + ADR (traçabilité décision) + contraintes empiriques internes (anti-scan-aveugle, gate typé, méthode anti-drift).
