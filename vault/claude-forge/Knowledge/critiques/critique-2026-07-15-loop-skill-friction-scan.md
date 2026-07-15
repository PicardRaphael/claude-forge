---
titre: "Critique — SPEC loop skill-friction-scan"
resume: "DA adversarial sur la SPEC d'inner-loop skill-friction-scan : les 4 signaux de détection ne sont pas également détectables (signaux 1/2 = wishful thinking counterfactuel), doublon infra avec search_sessions (signal 3) et candidat mode sur skill-evolve plutôt que 3e skill. Verdict FIX-AVANT-SHIP dérivant vers KILL si signaux 1/2 non opérationnalisables."
aliases:
  - "critique skill-friction-scan"
  - "DA loop friction skills"
  - "critique loop auto-amélioration forge"
  - "friction scan transcripts verdict"
type: knowledge
domaine: claude-code
derniere-maj: 2026-07-15
auteur: claude
tags:
  - "#type/knowledge"
  - "#domaine/claude-code"
sources:
  - "[[loop-apprentissage-codex]]"
  - "[[ajouter-source-donnees-mcp-forge-brain]]"
---

## Devils Advocate — SPEC loop skill-friction-scan

**Intention déclarée :** inner-loop `/skill-friction-scan` qui lit les transcripts de session forge, détecte via 4 signaux les skills ayant « frotté » en usage réel, et produit un rapport d'amendements validés item par item par Raphael avant délégation à skill-evolve→skill-creator.

---

### Verdict

**Bloquants :** 2 | **Avertissements :** 3 | **Nitpicks :** 1

**Décision recommandée :** FIX-AVANT-SHIP — avec dérive explicite vers KILL si les signaux 1 et 2 ne peuvent PAS être transformés en règle de détection à vérité-terrain. Le résidu (signal 3) est largement couvert par search_sessions + skill-evolve.

---

### Si je devais le faire marcher malgré mes objections

1. **Scinder les 4 signaux par détectabilité, pas les traiter en bloc.**
   - GARDER signal 3 (erreur récurrente ≥2 sessions) : pattern/string match cross-session, vraie vérité-terrain. MAIS le router vers search_sessions existant, pas un parser neuf.
   - GARDER signal 4 (collision) : détectable via events `tool_use` Skill concurrents dans une fenêtre — nécessite tool_use, donc parser dédié.
   - METTRE EN QUARANTAINE signaux 1 (auto-invoke raté) et 2 (résultat corrigé) : jugements counterfactuels/sémantiques sans vérité-terrain dans le transcript. Ne les shipper QUE si on les opérationnalise en règle concrète (ex signal 1 = « Raphael a tapé `/skill-X` explicitement dans le tour N alors qu'aucune skill n'était active au tour N-1 » — vérifiable via tool_use, PAS « le sujet correspondait à une skill »).
2. **Réutiliser l'infra indexée existante.** Pour signal 3 : `search_sessions` couvre déjà. Pour signaux 4 (et 1/2 opérationnalisés) qui exigent les events `tool_use` : suivre le pattern canonique [[ajouter-source-donnees-mcp-forge-brain]] — ajouter une table FTS5 `skill_invocations` indexée + watcher incrémental mtime, PAS un script Python ad-hoc qui reparse 159 fichiers à chaque run.
3. **Faire de ce loop un `mode=friction` de skill-evolve, pas une 3e skill.** L'axe « comportement observé » est un vrai gap (skill-evolve = maturité statique), mais un gap justifie un mode sur la skill existante, pas un composant standalone à coût de listing permanent.
4. **Requalifier le PASS/FAIL preuve** : de « filtre automatique » à « aide à la falsifiabilité pour Raphael ». Ne pas le vendre comme garde-fou indépendant.

---

### Angle Technique — Qu'est-ce qui se casse ?

**Le cœur : les 4 signaux ne sont PAS également détectables** (§4.3). La SPEC les liste comme équivalents ; ils ne le sont pas.

- **Signal 3 (erreur récurrente)** — le plus solide. Match de motif d'erreur répété sur ≥2 sessions = vérité-terrain réelle dans le texte.
- **Signal 4 (collision)** — détectable-ish : deux events `tool_use` Skill en concurrence dans une fenêtre. Nécessite de lire les blocks tool_use.
- **Signaux 1 et 2 = le noyau wishful thinking.** « Une skill aurait dû se déclencher mais ne l'a pas » n'a AUCUNE vérité-terrain dans le transcript : ça exige de re-rejouer la décision de routing, et ça hallucine des matchs sur mots-clés. « Raphael a corrigé le résultat » est indistinguable d'un raffinement normal ou d'un changement de sujet. Or §8.2 déclare « le LLM juge les frictions » : toute la détection repose sur le jugement LLM SANS règle opérationnelle pour les signaux 1/2. Ironie : ce sont les signaux qui SONNENT le plus utiles et les MOINS détectables.

- **Contradiction infra silencieuse (search_sessions).** La note [[ajouter-source-donnees-mcp-forge-brain]] confirme que l'indexer `search_sessions` **strippe les blocks tool_use/thinking**. Donc search_sessions ne voit PAS les invocations de skill — inutile pour signaux 1/2/4. MAIS il couvre proprement le signal 3 (erreur récurrente via FTS), ce que la SPEC ignore totalement. Et pour ce qui exige les tool_use, la SPEC réinvente un parsing ad-hoc au lieu du pattern canonique d'ajout de source indexée.

**Objections :**
- BLOQUANT (score 85) : Signaux 1 et 2 non opérationnalisables depuis le .jsonl — jugement counterfactuel/sémantique sans vérité-terrain, générateur garanti de faux positifs. Ce sont pourtant les 2 signaux vendeurs de la SPEC.
- AVERTISSEMENT (score 70) : Réinvention d'un parser .jsonl ad-hoc alors que le pattern canonique est l'ajout d'une source MCP indexée (table FTS5 + watcher), et que search_sessions couvre déjà le signal 3.
- NITPICK (score 40) : §3.2 « ~159 fichiers/14j, lisibles » — « lisibles » ≠ « judgeables à coût raisonnable ». Confusion accès/coût.

---

### Angle Stratégique — Est-ce le bon problème ?

Le problème (frictions skills perdues entre sessions) est réel. Mais l'instrumentation choisie est disproportionnée et mal placée dans la topologie des composants forge.

- **Doublon partiel non défendu (§9).** L'anti-doublon argumente contre align-vault-skills (source=vault) et skill-evolve statique (source=skill) — mais ne défend JAMAIS contre « pourquoi pas `skill-evolve --mode=friction` ». C'est le vrai gap de la défense. L'axe transcript est un gap authentique (donc pas un pur doublon), mais un gap authentique justifie un MODE sur skill-evolve, pas une 3e skill standalone à coût de listing permanent. Doctrine forge = routing/fusion-first (forge-review : 0 KILL, 2 fusions).
- **Chevauchement /done.** `/done` fait déjà la métacognition fin-de-session et extrait les erreurs. Une partie du signal 3 est peut-être déjà capturée là — le rapport risque de re-surfacer ce que /done a déjà traité.

**Objections :**
- BLOQUANT (score 82) : Candidat fusion évident (mode friction de skill-evolve) non écarté par la SPEC. Créer une 3e skill quand un mode suffit = anti-doctrine perf-déclenchement/routing-avant-budget.
- AVERTISSEMENT (score 55) : Chevauchement avec /done (extraction erreurs fin-de-session) non adressé.
- NITPICK : aucun.

---

### Angle Pratique — Combien de temps avant l'abandon ?

- **Coût par run réel.** 159 fichiers .jsonl bruts, même à ~50KB moyen = ~8MB ≈ plusieurs millions de tokens juste pour LIRE une fois, avant tout jugement. Le chunking sous-agents (§7.2) ne réduit PAS l'agrégat — il le parallélise. Pour un payoff « skills légèrement mieux », risque orphelin élevé (lancé 2 fois puis mort).
- **Cercle vicieux faux positifs → fatigue → abandon.** Les signaux 1/2 produisent des claims plausibles-mais-faux. Chaque claim exige une revue humaine item par item (§7.1). Rapport bruité = revue coûteuse = Raphael arrête de lancer la commande = orpheline. Le mécanisme même qui devait aider (validation humaine) devient le goulot qui tue le loop.
- **État spéculatif.** `.skill-friction-state.json` + dédoublonnage par hash pour une commande **à la demande** : la reprise-depuis-dernier-run et le dédoublonnage supposent des runs fréquents et réguliers. Pour un usage « à la demande » solo, c'est de la complexité anticipée. Utile SEULEMENT si la commande devient récurrente (ce que la SPEC exclut en §2).

**Objections :**
- AVERTISSEMENT (score 65) : Coût token par run non chiffré dans la SPEC (millions de tokens/run) vs valeur floue → profil d'orpheline.
- NITPICK (score 45) : État JSON + hash = complexité spéculative pour une commande à la demande non planifiée.

---

### Vault — Historique pertinent

- **[[loop-apprentissage-codex]]** (source doctrinale, décision #3) : le pattern est réel et actionnable, MAIS la note insiste — « ni Willison ni OpenAI ne décrivent un loop auto-édition, le compounding reste jugement-piloté ». La SPEC respecte ce garde-fou (humain sur validation). Cependant la note recommande explicitement « à passer par loop-forge (SPEC) avant implémentation » ET la recette 5 étapes cite AWM/ACE dont le point 4 (validation) est un **evaluator module** ou **confidence score** — pas une simple citation de preuve auto-fournie par le même LLM juge.
- **[[ajouter-source-donnees-mcp-forge-brain]]** : pattern canonique d'ajout de source (search_sessions, validé 27 mai). Confirme que l'indexer strippe tool_use → search_sessions aveugle aux invocations skill. Contredit directement l'approche parser-ad-hoc de la SPEC : la bonne voie est une source MCP indexée.
- **synthese-audit-coherence-neo-ia-ia-back** : pattern « skills orphelines » déjà identifié comme problème récurrent en audit → renforce le risque orphelin (point 4).
