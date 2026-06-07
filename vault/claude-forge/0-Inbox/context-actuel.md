---
titre: Context Actuel
resume: Working memory dynamique -- mis a jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, memoire de travail, etat actuel]
type: context
status: active
derniere-maj: 2026-06-07
auteur: claude
tags: ["#type/context", "#meta"]
---
## Phase actuelle
Capitalisation de connaissances dans le vault terminée — dossier `Important/` entièrement réconcilié et vidé, doctrine single-source rétablie.

## Dernière session (2026-06-07)
### Décisions prises
- Sous-dossier `04-Techniques/serving/` créé (granularité validée vs stacks/) : serving-inference-optimisation + prompt-caching-kv-cache + reference-technique-stack-ia (déplacée d'Important/).
- Doctrine reference-grade : doc source = référence exhaustive cherchable MCP, notes atomiques = deltas décisionnels seulement.
- Réconciliation `Important/` menée 1 doc à la fois, 1 commit par doc, validation utilisateur par doc.
- Stack IA.md supprimé + 4 sources mortes nettoyées (pas gardé comme archive).

### En cours
- Rien de bloqué. 7 commits poussés sur main (c3a29b7 → 78f21ef). Working tree clean, branche synchro origin.

### Prochaines étapes
- **Chantier 3/5 wikilinks : CLÔTURÉ 7 juin** (133 → 96 liens brisés, −37). 0 lien cassé par ERREUR ; le résidu 96 est sain et expliqué : ~70 roadmap G1 (contenu à écrire), 8 narration CHANGELOG (→ exclusion Ch.5), ~15 placeholders syntaxiques (F). Voir CHANGELOG entrées 2026-06-07.
- Chantier CONTENU futur (roadmap G1 responsable-ia, ~52 cibles distinctes) — les liens s'auto-réparent à mesure que les notes sont écrites.
- **Chantier 4/5 outils MCP dormants : CLÔTURÉ 7 juin — « rien à réveiller » (résultat prouvé).** Diagnostic `usage_stats(365j)` : 20/22 outils appelés, 2 zéro-appel. `move_note` → LAISSÉ dormant (rare par design, capacité de sûreté réécriture wikilinks ; 0 rename en Ch.2+3 donc aucun bypass). `read_note_resolved` → CANDIDAT SUPPRESSION Ch.5 (cf Fils ouverts). Hypothèse « sur-usage `search_brain` » (1192 appels) testée et INVALIDÉE : échantillon 20 requêtes réelles = 80% vraie exploration / 20% ciblage déguisé (les 4 = 2 notes re-cherchées 2× intra-session, pas un défaut de ciblage). Sur-usage structurel non prouvé → AUCUNE rule de ciblage créée (nuirait à 80% de cas légitimes). `search_brain` à 1192 = sain pour un vault de concepts.

## Fils ouverts
- Le garde-fou lecture-entière (feedback + rule sequence-canonique renforcée) vient d'être posé — surveiller qu'il tient sur les prochains audits/comparaisons (ne plus juger « doublon/subsumé » sur 30 lignes).
- Les canoniques `comment-creer-hook`/`-agent`/`-skill` ont reçu des sections « AJOUT 7 juin » (deltas vérifiés source primaire) — si elles approchent une taille lourde, envisager déport en references/ à terme.
- **Bug frontmatter — `comment-creer-agent`/`-skill`/`-hook`** : double bloc YAML + BOM en tête (`derniere-maj:` seul, puis `﻿---`) → 0 alias / 0 tag au lint. 3 canoniques majeures. Réparation dédiée (retrait BOM + fusion des 2 blocs). Rejoint la tâche hygiène frontmatter du plan. Manip YAML délicate (le BOM casse le parsing) → session attentive, Obsidian fermé, séparée de toute autre écriture — PAS un coup de fin de journée.
- **Exclusion `CHANGELOG.md` du lint** (Chantier 5, limite MCP #6) : les 8 derniers liens « narration » du lint sont des noms morts re-mentionnés dans le CHANGELOG (le lint parse les `[[]]` même entre backticks, cf gotcha `mcp-vault-llm-design`). Fix = exclure `CHANGELOG.md` du scan comme `raw/`/`log.md`. DEV MCP, pas en chantier d'usage.
- **Arbitrer outil `read_note_resolved`** (Chantier 5, issu du diagnostic Ch.4 du 7 juin) : 0 appel sur 365j car sans matériau — son cas d'usage est « MOC à embeds `![[X]]` », or le vault n'a que 4 embeds dont 0 structurel (les 2 fichiers concernés *parlent* de la syntaxe, ne l'emploient pas). **PAS redondant** avec `read_note` (qui ne résout pas les embeds — c'est la fonction propre de l'outil). **Tension à trancher** : supprimer (allègement) vs garder (capacité latente si le vault adopte un jour des MOC à embeds) — car la canonique [[comparaison-mcp-forge-brain-vs-mcp-brain-28mai2026]] le valorise (critère #5 « forge MIEUX » + P3d « porter vers neoteem-brain »). Ne PAS graver « suppression » sans cet arbitrage explicite. Si suppression retenue : serveur MCP + `skills/forge-brain/SKILL.md` (L81/L152/L171) + rule si citée. DEV MCP. Ne PAS fabriquer de MOC à embeds pour le « justifier ».
- **Pistes externes à confronter à l'usage RÉEL au Chantier 5** (apportées par Raphael 7 juin — consigne : ne PAS copier, vérifier le besoin per-outil avant tout port). NE PAS migrer vers framework tiers (Cognee/Graphiti/Mem0) : l'espace se consolide H2 2026, le SQLite/FTS5 maison est plus durable.
  - **#1 Multi-hop / graphe (port depuis obsidian-brain)** — candidat annoncé « le plus solide » (gain tokens annoncé 6,8-49×, NON vérifié, à confirmer SEULEMENT si faisabilité prouvée). **Statut = à trancher PER-OUTIL, pas « bloqué »** : `find_by_symbol` est gated par la table `symbols(symbol, kind)` que forge n'a pas (cf critère #6 [[comparaison-mcp-forge-brain-vs-mcp-brain-28mai2026]], précondition `references-*` absente). MAIS `traverse_graph`/`find_concept_chain` parcourent peut-être le **graphe de wikilinks** — que forge a, riche (objet du Ch.3 : ~96 liens vivants + centaines résolus). **Discriminant à vérifier au Ch.5 = lire le code de `traverse_graph`/`find_concept_chain` dans obsidian-brain : parcourent-ils les wikilinks (forge a → matériau) ou la table symbols (forge n'a pas → bloqué) ?** Ne pas reporter le verdict #6 « bloqué » sur les 3 outils en bloc.
  - **#2 Temporal (Zep/Graphiti)** — raisonner sur « vrai à quelle date » (périmé, contradiction). **Question ouverte, NE PAS résoudre maintenant** : Jarvis en a-t-il besoin vu [[doctrine-vivante]] (verdicts INFO / PIVOT_CANDIDATE / REINFORCE + gate humaine) qui couvre déjà l'évolution doctrinale ? À confronter, pas à porter.
  - **#3 Grille d'éval 5 dimensions (mem0)** — contradiction / temporal / abstention / mise à jour. **Ce n'est PAS un outil mais une grille de MESURE** de la qualité du MCP. Candidate critère d'éval, hors scope « réveiller un outil ».
- **Lecture / positionnement Anthropic (PAS une piste outil)** : arxiv **2601.20404** « On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents » — fichier d'instructions structuré → −28,6 % runtime, −16,6 % tokens, complétion comparable. Conforte la discipline tokens. ⚠️ **Métadonnées du brief corrigées sur source primaire** : auteurs = Lulla/Mohsenimofidi/Galster/Zhang/Baltes/Treude (Canterbury NZ / Singapour / Adelaide), **PAS ETH Zurich** ; **1 papier, pas 2** ; sujet = `AGENTS.md`, pas « fichiers contexte » générique. Fait qualitatif vrai, attribution hallucinée (pattern [[feedback_llm_deep_research_version_numbers]]).

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
