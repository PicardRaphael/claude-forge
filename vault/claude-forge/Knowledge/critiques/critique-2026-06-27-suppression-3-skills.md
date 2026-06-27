---
titre: "Critique DA — plan de suppression/reclassement de 3 skills forge (27 juin 2026)"
resume: "Devils-advocate sur le plan destructif issu de l'audit utilité skills : KILL self-check / merge da-blocking-arbitrage / convert auditor-empirical-verify. 2 BLOCKING + 1 PARTIAL. Plan corrigé zéro-perte à exécuter en session fraîche."
aliases:
  - "critique suppression 3 skills 27 juin"
  - "DA reclassement skills forge"
  - "plan corrige self-check da-blocking auditor-verify"
type: knowledge
domaine: claude-code
status: active
derniere-maj: 2026-06-27
auteur: claude
tags:
  - "#type/critique"
  - "#domaine/claude-code"
---

## Contexte

Audit utilité/reclassement des 45 skills forge (workflow, 27 juin) → corpus LEAN (42/45 KEEP). 3 skills à toucher, arbitrées par Raphael : KILL `self-check`, merge `da-blocking-arbitrage`, convert `auditor-empirical-verify` → rule. Devils-advocate lancé AVANT exécution (doctrine : plan destructif issu d'audit → DA obligatoire). Verdict : **ne PAS exécuter tel quel** (2 BLOCKING + 1 PARTIAL).

## Verdicts

### Action 1 — KILL `self-check` → BLOCKING
- **2 checks uniques non couverts** par repo-inspector : (a) validation JSON de `settings.json`/`settings.local.json` (`self-check` SKILL.md:31-32) ; (b) détection du chemin obsolète `agent-memory/` dans les agents (SKILL.md:27). repo-inspector n'a aucun équivalent (grep exhaustif). `config-guardian` cible les *autres* repos, pas forge.
- **3 références entrantes orphelinées** : `forge-review/SKILL.md:29` + `:214-217` + `references/baseline.md:15` délèguent explicitement la conformité config à self-check. La prémisse « zéro câblage » du scan était fausse.
- **Plan corrigé (zéro-perte) AVANT `git rm`** : (a) porter les 2 checks dans repo-inspector (section Checks settings/skills) ; (b) réécrire les 3 réfs forge-review → repo-inspector mode=audit ; (c) régénérer INDEX.md + skill-triggers.json.

### Action 2 — Merge `da-blocking-arbitrage` dans l'agent devils-advocate → BLOCKING
- La cible (agent = sous-agent) ne peut exécuter ni l'arbitrage user (`AskUserQuestion` filtré) ni l'écriture dette (`create_note` indispo en sous-agent, cf devils-advocate.md:56). La skill tourne aujourd'hui en **session principale** (`user-invocable: true`) — c'est pour ça qu'elle PEUT arbitrer + écrire la dette.
- **Plan corrigé (split par foyer)** : scoring 0-100 + filtres faux-positifs (SKILL.md:39-69) → agent `devils-advocate.md` (raffine BLOQUANT/AVERTISSEMENT) ; procédure arbitrage A/B + attente décision + création `Knowledge/dettes/` (SKILL.md:31-37,90-93) → rule `devils-advocate-pipeline.md` (foyer arbitrage session principale). PUIS supprimer la skill.

### Action 3 — Convert `auditor-empirical-verify` → rule `post-dispatch-verify.md` → PARTIAL (PASS sous conditions)
- Traduction sans perte (checklist post-dispatch consultée par la session principale ; always-on = ne peut pas être oubliée, meilleur que trigger faible).
- **Conditions PASS** : (1) frontmatter `description:` obligatoire (sinon rule non chargée, cf repo-inspector.md:102) ; (2) retirer `INDEX.md:13` ; (3) rester concis (~60 lignes, coût token continu).

## Décision

Plan corrigé à exécuter en **session fraîche** (la session d'origine était trop longue ; opérations destructives = contexte propre requis). Aucune suppression sans avoir porté/réécrit les dépendances d'abord. Barre : un `git rm` n'est sûr qu'après portage complet des checks + réécriture des références entrantes.

## Items additifs liés (non destructifs, indépendants)

- **arxiv-verification** : câbler dans cc-news / rag-design Étape 6 / deep-research (dormante, besoin réel).
- **python-script-refactor-masse** : ⚠️ bug ROOT codé en dur `raphael.picard_neote` → cassé sur poste perso RAPHAEL-LENOVO. Fixer + raccourcir description + câbler.
- **Trous dispatch** : `evolve` + `loop-forge` absents de `comportement-proactif.md` ; `config-guardian` bypassé.
- **Drift contenu** : `cc-features-ref` dit « DÉFAUT Opus 4.7 » (vs 4.8) ; `cc-cowork-ref` daté 14 mai.
- **2 skills à créer** : `roadmap-projet-ia` (cadrage→roadmap), `deconstruction-maieutique` (livre/podcast→notes-concepts).

## Liens

- [[methode-monter-systeme-workflow]] — grille capabilities source du chantier
- [[devils-advocate-pipeline]] · [[da-blocking-arbitrage]] — doctrine arbitrage BLOCKING

## MAJ 27 juin — exécution (3 actions DONE, zéro-perte)

Plan corrigé exécuté en session (pas reportée — Raphael ne pouvait pas switcher) :
- ✅ **Action 3** : `auditor-empirical-verify` → rule `.claude/rules/post-dispatch-verify.md` (path hardcodé corrigé en `git rev-parse`). Skill supprimée, INDEX retiré.
- ✅ **Action 2** : `da-blocking-arbitrage` splittée — scoring 0-100 + faux-positifs → agent `devils-advocate` ; protocole arbitrage A/B + dette → rule `devils-advocate-pipeline`. Skill supprimée.
- ✅ **Action 1** : `self-check` KILL — 2 checks uniques (validité JSON settings + détection `agent-memory/`) portés dans `repo-inspector` mode=audit ; 5 réfs réécrites (forge-review SKILL.md ×4, baseline.md, INDEX, 2× skill-triggers) ; JSON validés. Skill supprimée.
- ✅ Trous dispatch comblés : `evolve` + `loop-forge` ajoutés à `comportement-proactif`.

Le grep a révélé +réfs que le DA listait (forge-review:13 + 2× skill-triggers) — vérification exhaustive faite avant `git rm`.

**Reste (additif, non destructif)** : câbler `arxiv-verification` (cc-news/rag-design/deep-research) · fix bug path `python-script-refactor-masse` (raphael.picard_neote) · drift contenu cc-features-ref (Opus 4.7→4.8) + cc-cowork-ref · créer `roadmap-projet-ia` + `deconstruction-maieutique`.
