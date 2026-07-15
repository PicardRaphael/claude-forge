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

Commits `9466b0a`→`aeb5d4a`, branche `us/RPI/PP-N2-111820-claude-skills`. Suite de la critique du PLAN (13 juil., SHIP WITH FIXES) — vérifie si l'exécution répond aux 4 avertissements. **6/6 angles vérifiés empiriquement (les 2 diffs originaux fournis par la session principale).**

Note jumelle (contenu identique, chemin conventionnel demandé par le protocole) : [[critique-2026-07-15-execution-modernisation-bdd-claude]].

---

## Verdict

**Bloquants :** 0 | **Avertissements :** 1 | **Nitpicks :** 2

**Décision recommandée :** SHIP. L'unique avertissement (/ticket auto-invocable) est hérité du plan, connu, mitigé par rollback + critère de validation ; non ship-blocking.

Exécution nettement au-dessus de la moyenne. Les 6 angles passent (détail par angle ci-dessous).

---

## Si je devais le faire marcher malgré mes objections

1. **`/ticket` sans `disable-model-invocation`** (AVERTISSEMENT hérité, score 70) — `.claude/skills/ticket/SKILL.md:1-9` (frontmatter sans `disable-model-invocation`) : la skill peut être auto-déclenchée par le modèle, qui peut sauter une phase ou contourner un checkpoint humain (`SKILL.md:88`, `:108` = les 2 checkpoints). Perte du déterminisme d'une slash command. Mitigation en place : rollback `git revert aeb5d4af0` + critère de validation exécutable (`.claude/todo/2026-07-13-modernisation-claude.md:92-101`). **Chemin propre : sur le 1er ticket réel post-merge, vérifier les 6 points du critère ; si un checkpoint saute → ajouter `disable-model-invocation: true` OU rollback. Ne PAS considérer /ticket validé avant ce test.**
2. **Suppression commands/ avant validation /ticket** : commit isolé droppable (`aeb5d4a`), rollback 5 s documenté (todo:101-103). Suffisant SI la review Bastien est la porte de sortie. **Renforcement : garder `aeb5d4a` en dernier de la PR (ou non-mergé) jusqu'à ce que le critère /ticket passe.**
3. **settings.json.proposed** (`.claude/settings.json.proposed:1-16`) : contenu correct (`py` launcher, timeout 10, `${CLAUDE_PROJECT_DIR}`). Rien à corriger — ne pas oublier l'action humaine (rename → settings.json), sinon le hook ne s'active pas.

---

## Angle Technique — Qu'est-ce qui se casse ?

**Hook skill-activation.py : PROPRE.** `.claude/hooks/skill-activation.py` — fail-open absolu (2 `except → sys.exit(0)`, lignes 59-60 et 100-101), bypass `/ # !` (ligne 64), dédup session par tracker temp (`_tracker_path` L27-29), cap 2 suggestions/prompt (`MAX_SUGGESTIONS_PER_PROMPT` L16), word-boundary intelligent (`_kw_pattern` L48-53 gère `fetch(` et `NEO-`). Advisory pur, aucun `exit 2`. Aucun spam ni blocage dev possible.

**triggers.json : PROPRE, sans clé morte.** `.claude/.skill-triggers.json` — 30 clés vérifiées une à une contre 33 dossiers `skills/*/SKILL.md` : chaque clé correspond à un dossier réel. Le lead « drift auto-infligé » (analyse-ps réaligné en analyse-fonction-sql) NE se matérialise pas : `.claude/skills/analyse-ps/SKILL.md:2` → `name: analyse-ps`, identique dossier ET clé triggers.json:28. Les 3 skills sans clé (capitalise/summarize/package) sont à invocation manuelle — cohérent. Le hook ne suggérera jamais un `Skill(<inexistant>)`.

**AVERTISSEMENT (70) — /ticket auto-invocable.** Cf « Si je devais le faire marcher » §1.

**NITPICK (30) — package/SKILL.md référence commands/ et agents/ disparus.** `.claude/skills/package/SKILL.md:53,65` (mapping type→dossier) et `:136-137` (patterns de détection de dépendances) listent `.claude/commands/` et `.claude/agents/`. Ces dossiers n'existent plus (commands supprimé, agents→roles). MAIS c'est la doc générique de la mécanique de packaging (outil transverse, tout type CC) — pas une référence morte fonctionnelle. Cosmétique, inoffensif.

---

## Angle Stratégique — Est-ce le bon problème ?

**Skills proprietaire/suivicopro : HONNÊTES, zéro hallucination.** Les 13 procédures asserées existent dans `.claude/knowledge/index/index_sql_functions.txt` :
- proprietaire (`SKILL.md:51-58`) : `p_adf_calcul` (idx:1101), `p_budget_valide` (1118), `p_crg_valide` (1140), `p_acompte_valide` (1096), `p_corrige_crg` (1132), `p_reddition_valide_crg` (1202), `p_calcul_fiscal_preparatoire` (1120).
- suivicopro (`SKILL.md:49-56`) : `p_adf_calcul` (idx:2196), `p_budget_approbation` (2210), `p_dossier_creation` (2215), `p_exercice_ouvreferme` (2217), `p_copro_change_cle_generale` (2213), `p_adf_regul_coproprietaire_edition` (2198), `p_maj_data_cop` (2232).
Bonne pratique : les skills DÉFÈRENT colonnes/FK vers l'index (`proprietaire/SKILL.md:45`, `suivicopro/SKILL.md:43`) au lieu de les asserer. Risque d'hallucination concentré sur 2 claims comportementaux (`suivicopro/SKILL.md:31` trigger acteur type 9 ; `:62` trigger AFTER t_role → P_MAJ_DATA_COP), non vérifiables par l'index seul mais prudemment formulés. Les « à compléter » posés au BON endroit (glossaire `:32` + règles métier fines `:64` = savoir exigeant du vécu).

**Compression descriptions = GAIN NET (pas une perte).** Diff quotepart 1239→388 chars : l'original (`base_quotepart_frontmatter.md:8-14`) listait 2× une liste exhaustive keyword-stuffée (QP/QPTOT/QPSU, colonnes quotepart_valeur/quotepart_roleid/quoteparttotal_aid/quoteparttotal_ctrid, ~10 procs). La version actuelle (`.claude/skills/quotepart/SKILL.md:3`) garde tables primaires + p_quotepart_create/f_quotepart_check + colocation/SCI/indivision/nue-propriété + 4 anti-triggers. Le matching CC est sémantique (LLM), pas keyword ([[comment-creer-skill]]) → lister des colonnes n'aide pas le trigger et augmente le risque de drop du listing. Le filet `.skill-triggers.json:11` porte en plus le keyword-match (quote-part/quotepart/t_quote_part/colocation/indivision/indivisaire). Net positif.

---

## Angle Pratique — Combien de temps avant l'abandon ?

**Doctrine repo d'équipe : PROPRE.** [[config-repo-equipe-vs-forge]] appliquée : hook non-bloquant fail-open, pas de delegate-guard, skills auto-portantes (`{{PATH_*}}` + index du repo, zéro wikilink vault ni MCP forge-brain — vérifié sur proprietaire/suivicopro/quotepart), settings en .proposed (validation humaine), gouvernance Bastien (trigramme, branche, `todo:112-116`). README index inversé (CLAUDE.md résumé / README détail, `knowledge/index/README.md:9`) cohérent.

**NITPICK (20) — CLAUDE.md 248→131 L : slim sain.** Diff vérifié (`base_CLAUDE.md` 248 L vs `CLAUDE.md` 131 L) : le volume retiré (~128 L, L105-233 de l'original) est le guide index détaillé (formats btree/gin, décomposition des 7 champs FK, exemples perf) déporté au README chargeable `@.claude/knowledge/index/README.md` (intégralement présent). Les recettes Grep canoniques + table des 9 index RESTENT en contexte permanent (`CLAUDE.md:94-111`). Project structure enrichie (schémas proprietaire/suivicopro détaillés `:56-60`). Section Custom Agents → Rôles de session compacte (`:41-49`). Aucune perte fonctionnelle — le nitpick « sur-slim » posé initialement se dégonfle.

---

## Diffs vérifiés (angles #1 et #5 complétés)

- **#1 quotepart 1239→388 chars** : retrait = keyword stuffing (QP/QPTOT/QPSU, 4 colonnes, procs secondaires listées 2×). Conservé = tables primaires + procs clés + termes métier + 4 anti-triggers. Matching sémantique → gain net. Filet triggers.json couvre le keyword-match.
- **#5 CLAUDE.md 248→131** : retrait = guide index détaillé (déporté README, intégral). Conservé + enrichi = project structure, recettes Grep, table 9 index, workflow, capitalise. Zéro perte fonctionnelle.

---

## Vault — Historique pertinent

- [[critique-plan-modernisation-bdd-claude]] (13 juil.) : critique du PLAN, SHIP WITH FIXES, 4 avertissements. Bilan : budget Phase2↔4 (72) → RÉSOLU par `skillListingBudgetFraction: 0.03` ; /ticket déterminisme (68) → CONFIRMÉ ouvert, mitigé ; conversion perd des deux côtés (66) → RÉSOLU (bénéfice réel + réversibilité) ; Phase 3 démolit archi-rôles (58) → RÉSOLU (fix minimal git mv vers roles/, muscle memory @ intacte).
- [[config-repo-equipe-vs-forge]] : doctrine correctement appliquée, aucun écart.
- [[comment-creer-skill]] : matching sémantique (pas keyword) + `skillListingBudgetFraction` (paramètre CC réel, sourcé code.claude.com/docs + claudefa.st) — fondent le verdict « compression = gain net ».
