---
titre: "Critique — Exécution 2e moitié modernisation .claude/ repo bdd"
type: knowledge
domaine: claude-code
derniere-maj: 2026-07-15
auteur: claude
aliases:
  - "critique execution modernisation bdd"
  - "DA exécution claude bdd"
  - "critique compression descriptions skills bdd"
  - "critique hook skill-activation bdd"
tags:
  - "#type/critique"
  - "#domaine/claude-code"
  - "#domaine/skills"
---
# Devils Advocate — Exécution 2e moitié modernisation `.claude/` repo bdd

**Intention déclarée :** exécuter la 2e moitié du plan de modernisation `.claude/` du repo d'équipe PostgreSQL bdd (compression 19 descriptions, création skills proprietaire/suivicopro, déplacement rôles + slim CLAUDE.md, hook skill-activation + settings.proposed, suppression commands/) sans casser les workflows de l'équipe.

Commits `9466b0a`→`aeb5d4a`, branche `us/RPI/PP-N2-111820-claude-skills`. Fait suite à la critique du PLAN (13 juil., SHIP WITH FIXES, 4 avertissements) — cette critique vérifie si l'exécution a répondu aux avertissements ou les a matérialisés. **6/6 angles vérifiés empiriquement (les 2 diffs originaux fournis par la session principale).**

---

## Verdict

**Bloquants :** 0 | **Avertissements :** 1 | **Nitpicks :** 2

**Décision recommandée :** SHIP (exécution propre). L'unique avertissement (/ticket auto-invocable) est hérité du plan, connu, mitigé par rollback + critère de validation ; non ship-blocking.

Exécution nettement au-dessus de la moyenne. Les 6 angles passent :
- **Procs des 2 nouvelles skills : zéro hallucination** — les 13 procédures asserées existent dans `index_sql_functions.txt`.
- **triggers.json sans clé morte** — 30 clés = 30 dossiers skills réels ; le lead « drift analyse-ps » ne se matérialise pas (`name:` resté `analyse-ps`).
- **`skillListingBudgetFraction` = vrai paramètre CC** (sourcé code.claude.com/docs + claudefa.st), valeur 0.03 répond à l'avertissement budget du plan.
- **Compression descriptions = GAIN net** — quotepart 1239→388 chars : retire du keyword stuffing (QP/QPTOT/QPSU, colonnes, procs secondaires re-listées 2×), garde tables/procs primaires + anti-triggers. Le matching CC est sémantique (pas keyword) → lister des colonnes n'aidait pas le trigger. Le filet triggers.json couvre en plus le keyword-match.
- **CLAUDE.md 248→131 = sain** — le volume retiré (~128 L) est le guide détaillé des index déporté au README (formats btree/gin, décomposition FK) ; les recettes Grep canoniques + table des 9 index restent en contexte permanent. Rien de fonctionnel perdu.
- **Hook fail-open propre**, doctrine repo d'équipe respectée.

---

## Si je devais le faire marcher malgré mes objections

1. **`/ticket` sans `disable-model-invocation`** (AVERTISSEMENT hérité, score 70) : la skill peut être auto-déclenchée par le modèle, qui peut sauter une phase ou contourner un checkpoint humain — perte du déterminisme d'une slash command. Mitigation en place : rollback écrit (`git revert aeb5d4af0`) + critère de validation exécutable dans le todo. **Chemin propre : sur le 1er ticket réel post-merge, vérifier les 6 points du critère ; si un checkpoint saute → ajouter `disable-model-invocation: true` (slash-only) OU rollback. Ne PAS considérer /ticket validé avant ce test.**
2. **Suppression commands/ avant validation /ticket** : commit isolé droppable, rollback 5 s documenté — suffisant SI la review Bastien est la porte de sortie. **Renforcement : garder `aeb5d4a` en dernier de la PR (ou non-mergé) jusqu'à ce que le critère /ticket passe.**
3. **settings.json.proposed** : contenu correct (`py` launcher, timeout 10, `${CLAUDE_PROJECT_DIR}`). Rien à corriger — juste ne pas oublier l'action humaine (rename → settings.json), sinon le hook ne s'active pas.

---

## Angle Technique — Qu'est-ce qui se casse ?

**Hook skill-activation.py : PROPRE.** Fail-open absolu (2 `except → exit 0`), bypass `/ # !`, dédup session par tracker temp, cap 2 suggestions/prompt, word-boundary intelligent (`_kw_pattern` gère `fetch(` et `NEO-`). Advisory pur, aucun `exit 2`. Aucun spam ni blocage dev possible.

**triggers.json : PROPRE.** 30 clés = 30 dossiers skills réels. Le lead « drift auto-infligé » (analyse-ps réaligné) NE se matérialise pas : `name:` resté `analyse-ps`, identique dossier ET clé. Les 3 skills sans clé (capitalise/summarize/package) sont à invocation manuelle — cohérent qu'elles ne soient pas auto-suggérées. Le hook ne suggérera jamais un `Skill(<inexistant>)`.

**AVERTISSEMENT (70) — /ticket auto-invocable.** Cf « Si je devais le faire marcher » §1. Défaut réel mais mitigé, hérité du plan (score 68→70).

**NITPICK (30) — package/SKILL.md référence commands/ et agents/ disparus.** Mapping type→dossier (L47-67, L136-137) liste `.claude/commands/` et `.claude/agents/`. Ces dossiers n'existent plus. MAIS c'est la doc générique de la mécanique de packaging (outil transverse, tout type CC) — pas une référence morte fonctionnelle, package peut légitimement cibler ces dossiers dans un autre contexte. Cosmétique, inoffensif.

**Objections :**
- BLOQUANT : aucun
- AVERTISSEMENT : /ticket auto-invocable (perte déterminisme phases/checkpoints) — mitigé rollback + critère validation
- NITPICK : package/SKILL.md liste commands/+agents/ disparus (doc générique, inoffensif)

---

## Angle Stratégique — Est-ce le bon problème ?

**Skills proprietaire/suivicopro : HONNÊTES.** Toutes les procs asserées existent dans `index_sql_functions.txt` : `p_adf_calcul`, `p_crg_valide`, `p_budget_valide`, `p_acompte_valide`, `p_corrige_crg`, `p_reddition_valide_crg`, `p_calcul_fiscal_preparatoire` (proprietaire) ; `p_dossier_creation`, `p_budget_approbation`, `p_exercice_ouvreferme`, `p_copro_change_cle_generale`, `p_adf_regul_coproprietaire_edition`, `p_maj_data_cop` (suivicopro). Bonne pratique : les skills DÉFÈRENT colonnes/FK vers l'index au lieu de les asserer — risque d'hallucination concentré sur 2 claims comportementaux (trigger acteur type 9 → p_dossier_creation ; trigger AFTER t_role → P_MAJ_DATA_COP), non vérifiables par l'index seul mais prudemment formulés. Les « à compléter » posés au BON endroit (glossaire + règles métier fines = savoir exigeant du vécu, pas de l'index).

**Compression descriptions = bon problème bien résolu.** Le diff quotepart (1239→388) montre que l'original était du keyword stuffing (liste exhaustive répétée 2× : QP/QPTOT/QPSU, quotepart_valeur, quoteparttotal_aid/ctrid, ~10 procs). La doctrine CC (matching sémantique LLM, pas keyword — [[comment-creer-skill]]) rend cette liste inutile au déclenchement et même contre-productive (chaque char superflu augmente le risque de drop du listing entier). La compression garde les triggers primaires (tables/procs/termes métier + anti-triggers) et déporte le reste au body/index. Net positif.

**Objections :**
- BLOQUANT : aucun
- AVERTISSEMENT : aucun (l'avertissement plan « conversion perd des deux côtés » se résout : le bénéfice auto-trigger est réel pour analyse/verif ; marginal pour /ticket mais réversible)
- NITPICK : aucun

---

## Angle Pratique — Combien de temps avant l'abandon ?

**Doctrine repo d'équipe : PROPRE.** [[config-repo-equipe-vs-forge]] appliquée : hook non-bloquant fail-open, pas de delegate-guard, skills auto-portantes (`{{PATH_*}}` + index du repo, zéro wikilink vault ni MCP forge-brain), settings en .proposed (validation humaine), gouvernance Bastien (trigramme, branche). README index inversé (CLAUDE.md résumé / README détail) cohérent et documenté.

**NITPICK (20) — CLAUDE.md 131 L.** Diff vérifié : le volume retiré (~128 L de l'original L105-233) est le guide détaillé des index (formats btree/gin, décomposition des 7 champs FK, exemples perf) déporté au README chargeable `@.claude/knowledge/index/README.md`. Les recettes Grep canoniques (les plus utilisées) + la table des 9 index RESTENT en contexte permanent (L94-111). La section Custom Agents → Rôles de session compacte. Rien de fonctionnel perdu ; le nitpick « sur-slim » posé initialement se dégonfle — c'est un slim discipliné, pas une amputation.

**Objections :**
- BLOQUANT : aucun
- AVERTISSEMENT : aucun
- NITPICK : CLAUDE.md slim agressif mais sain (détail index au README, recettes canoniques préservées)

---

## Diffs vérifiés (angles #1 et #5 complétés)

- **#1 quotepart 1239→388 chars** : retrait = keyword stuffing (abréviations QP/QPTOT/QPSU, colonnes quotepart_valeur/quotepart_roleid/quoteparttotal_aid/quoteparttotal_ctrid, procs secondaires listées 2×). Conservé = tables primaires + p_quotepart_create/f_quotepart_check + colocation/SCI/indivision/nue-propriété + 4 anti-triggers. Matching CC sémantique → gain net, pas de perte de trigger. Filet triggers.json couvre le keyword-match.
- **#5 CLAUDE.md 248→131** : retrait = guide index détaillé (déporté README, intégralement présent). Conservé + ENRICHI = project structure (schémas proprietaire/suivicopro détaillés), recettes Grep canoniques, table 9 index, workflow, capitalise. Aucune perte fonctionnelle.

---

## Vault — Historique pertinent

- [[critique-plan-modernisation-bdd-claude]] (13 juil.) : critique du PLAN, SHIP WITH FIXES, 4 avertissements. Cette critique-ci vérifie l'exécution. Bilan des 4 avertissements du plan : budget Phase2↔4 (72) → RÉSOLU par `skillListingBudgetFraction: 0.03` ; /ticket déterminisme (68) → CONFIRMÉ ouvert, mitigé ; conversion perd des deux côtés (66) → RÉSOLU (bénéfice réel + réversibilité) ; Phase 3 démolit archi-rôles (58) → RÉSOLU (fix minimal git mv vers roles/, muscle memory @ intacte).
- [[config-repo-equipe-vs-forge]] : doctrine correctement appliquée, aucun écart.
- [[comment-creer-skill]] : matching sémantique (pas keyword) + `skillListingBudgetFraction` confirmés — fondent le verdict « compression = gain net » de l'angle #1.
