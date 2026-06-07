---
titre: "Changelog vault forge-brain"
resume: "Historique des ajouts et modifications du vault forge-brain"
aliases:
  - changelog vault
  - historique vault
  - changelog forge-brain
  - historique notes vault
type: index
derniere-maj: 2026-06-07
auteur: claude
tags:
  - "#type/index"
  - "#domaine/claude-code"
---

## 2026-06-07 — Chantier 5/5 (DEV MCP) — ENTAMÉ : 2 des 6 limites MCP traitées (read_note_resolved + exclusion CHANGELOG)

- **Modifiée (1 canonique)** : [[mcp-vault-llm-design]] — outil `read_note_resolved` retiré de la matrice courante (sections 1-9 renumérotées 7→8, POURQUOI « embeds opaques » retiré) ; entrée **v1.4 (7 juin)** ajoutée au STATUT documentant le retrait (0 appel/365j, 0 MOC à embeds — dormant faute de matériau). Historique daté (MÉTRIQUES 24 mai, v1.3) **préservé** — vrai à sa date, non réécrit.
- **Code serveur MCP** (hors vault, commit `0b369b9`) : `read_note_resolved` + `_resolve_embeds` + wrapper + 6 tests embed supprimés ; `lint_vault` exclut `CHANGELOG.md` du scan source (précédent `log.md`). Doc skill `forge-brain/SKILL.md` nettoyée (3 lignes, via skill-creator). 138 tests passent.
- **Effet lint mesuré** : 98 → 90 wikilinks cassés (les 8 du CHANGELOG = noms morts narratifs entre backticks, 0 vrai lien réparable, vérifiés 1 par 1).
- **Statut Ch.5** : ENTAMÉ, **pas clos**. 4 limites MCP restantes (tracées dans `context-actuel`) : #1 `lint_vault` non paginé (plafond 50), #2 `rename_tag`/écriture array-safe (3 incidents corruption YAML), #3 lock inter-écritures MCP (race-condition), #4 lag réindexation agrégats. `traverse_graph` multi-hop = piste écartée (pas de consommateur — décision Raphael), ≠ une des 6 limites.
- **Source** : Chantier 5/5 du plan vault, 2 items à besoin immédiat (verdict `usage_stats` Ch.4).

## 2026-06-07 — Chantier 4/5 outils MCP dormants — CLÔTURE (« rien à réveiller », prouvé)

- **Modifiées (2 canoniques)** : [[comparaison-mcp-forge-brain-vs-mcp-brain-28mai2026]] reçoit une section « Vérification empirique d'usage (7 juin) » qui qualifie 2 de ses claims via `usage_stats(365j)` — A2 (« search_brain = dernier recours ») = anti-pattern réel mais MARGINAL (échantillon 20 requêtes : 80 % vraie exploration, 20 % = 2 notes re-cherchées intra-session) ; critère #5 (`read_note_resolved`) = supérieur en conception mais dormant en usage (0 MOC à embeds dans le vault). [[pattern-maintenance-hybride-corpus-accumulatif]] : critère « D — dormants » étendu des notes aux **outils** (rare-par-design / inutile-faute-de-matériau / redondant — 1 pointeur vers la comparaison).
- **Verdict Chantier 4** : 20/22 outils appelés, 2 zéro-appel. `move_note` → laissé dormant (rare par design, sûreté wikilinks, 0 bypass). `read_note_resolved` → arbitrage Ch.5 (PAS redondant, dormant faute de matériau ; tension #5/P3d à trancher). Aucune rule de ciblage créée : le sur-usage `search_brain` (1192) testé et INVALIDÉ.
- **Source** : Chantier 4/5 du plan vault, diagnostic lecture-seule prouvé par log `usage.jsonl`, hypothèse de départ (Note B sur-usage search_brain) cherchée à invalider plutôt qu'à confirmer.

## 2026-06-07 — Chantier 3/5 wikilinks — CLÔTURE G2 + bilan (103 → 96 liens brisés, chantier terminé)

- **Créées (4 notes, récurrence prouvée pour chacune)** : [[automemorydirectory-absolu-casse-multiprojet]] + [[import-ajoute-pas-remplace-automemory]] (paire mémoire portable, chacune citée par 2 ADR) ; [[erreur-emphasis-overtriggering]] (anti-pattern CLAUDE.md cité par la canonique [[comment-ecrire-claudemd]]) ; [[audit-tripartite-doctrinal-pattern]] (3 lentilles Boris/Will/ECC, ≥6 notes + opérationnel dans repo-inspector). Les liens entrants se résolvent automatiquement.
- **Retiré (1 lien, niche)** : `capitalisation-proposee-pas-auto` dans [[phase-4-comparaison-hermes-roadmap]] (concept d'une phase projet ponctuelle, pas réutilisable, visait un fichier `memory/`).
- **Laissés en roadmap G1 (intentionnel, pas un bug)** : `manager-seniors-plus-experimentes` et `lexique-expressions-clients` = contenu à écrire (management responsable-ia, lexique métier Neoteem) — s'auto-réparent au chantier CONTENU futur.
- **Bilan Chantier 3/5 wikilinks** : 133 → 96 liens brisés (−37). Tous les liens cassés par ERREUR (causes A casse-leader, B renommage, C typo, D composant `.claude/`, E fichier `memory/`, G2 concepts) traités. Reste 96 = sain : ~70 roadmap G1 (contenu à écrire), 8 noms morts narration CHANGELOG (exclusion `CHANGELOG.md` du lint tracée au Chantier 5, limite MCP #6), ~15 placeholders syntaxiques d'exemple (F, no-op). 0 YAML cassé, 0 régression.
- **Source** : chantier 3/5, GO dernier paquet G2 de Raphael, preuve de récurrence exigée avant chaque création.

## 2026-06-07 — Chantier 3/5 wikilinks — G2 créations + retraits sur preuve (107 → 103 liens brisés)

- **Créée (1 note)** : [[multi-agent-handoff-loss-pattern]] (04-Techniques/agents/) — synthèse doctrinale croisant le paper Google/MIT (chiffres) × pattern-swarm (mécanisme de la fuite) × comment-creer-agent (règle design). Thèse : le coût du multi-agent = le nombre de handoffs sur le chemin critique, pas le nombre d'agents ; le threshold 45 % est le seuil de rentabilité du handoff. Résout le lien posé par [[google-mit-scaling-agent-systems-2025]]. Backlink ajouté dans [[comment-creer-agent]] (section APPELS).
- **Repointé (1 lien)** : dans [[todo-rotation-password-postgres-prod]], le lien vers un fichier `memory/` jamais créé (`secret-management-never-commit-credentials`) → absorbé par [[erreur-password-postgres-clair-mcp-json]] (déjà citée dans la note, couvre l'anti-pattern + la règle + la réparation). Pas de note créée : la note d'erreur subsume le savoir, créer = doublon.
- **Régression auto-infligée corrigée** : l'exemple littéral du gotcha « lint parse les wikilinks même entre backticks » (note `mcp-vault-llm-design`, ajouté ce jour) s'était auto-compté comme 2 liens cassés — preuve par l'exemple du gotcha lui-même. Exemple réécrit en texte nu, gotcha renforcé.
- **Retraits sur preuve (2 cibles, 3 liens)** : #9 `plugin-structure-cowork-claude-code` (cité 2× par [[plugin-vs-skill-anatomie]]) → retiré : la note citante EST déjà la note d'anatomie plugin, aucune cible séparée n'existe. #10 `dossier-strategique-ia-neoteem` (cité par [[comprendre-neoteem-vue-responsable-ia]] annoté « mémoire forge ») → retiré : visait un fichier `memory/`, le dossier est un livrable CODIR externe, pas une note vault. Vérifiés via `read_note` avant verdict (jamais supposer renommage).
- **Source** : chantier 3/5, GO G2 item par item de Raphael, AskUserQuestion sur chaque candidat création.

## 2026-06-07 — Chantier 3/5 wikilinks — lots D + E (124 → 107 liens brisés)

- **Lot D — liens vers composant `.claude/` (19 liens)** : un skill/agent/rule/hook n'est PAS une note vault → retrait du wikilink, texte gardé visible en code-span (`nom-composant`) ou en prose (« la skill X », « cf rule Y »). Touche eval-pattern-anthropic-skill-creator, analyse-plugin-claude-code-setup, comparaison-skill-anthropic-claude-code-setup, context-drift-throw-vs-patch, pattern-vault-llm-karpathy, doctrine-vivante (×3), comment-creer-hook (×2), comment-creer-skill, hooks-conformite-audit-passif-continu (×2), pattern-maintenance-hybride-corpus-accumulatif, plugins-officiels-veille-2026-05-26 (×3).
- **Lot E — liens vers fichier `memory/` (5 cibles traitées)** : pas de règle unique, décision par cible. **Retraits (2)** : un lien pointant vers un fichier `memory/feedback_*` ou `memory/reference_*` n'est pas une note vault → retrait du wikilink, texte gardé (decision-settings-global-modification-manuelle, python-windows-tmp-msys-invisible — la rule windows-hooks couvre déjà ce savoir, promotion = doublon). **Promotions (3)** : gotchas MCP réutilisables et durables promus en vraies notes vault — [[mcp-alias-ambigu-chemin-exact]], [[vault-edit-gotchas-outillage]], [[workflow-args-array-gotcha]] (frontmatter complet, 5 aliases, tags convention, wikilinks corps vérifiés existants, créées via `create_note`).
- **Reste expliqué, pas un bug** : ~70 liens restants = roadmap responsable-ia (contenu à écrire, chantier dédié futur — les liens s'auto-réparent quand les notes existeront) ; 8 liens dont la source est le changelog = noms morts re-mentionnés dans la narration des réparations (le lint parse les wikilinks même entre backticks) → à éliminer au Chantier 5 via exclusion de `CHANGELOG.md` du lint (comme `log.md`/`raw/` déjà exclus, limite MCP #6) ; 15 placeholders syntaxiques d'exemple (no-op, exemples de doc).
- **Gotcha confirmé (renforce limite MCP #2)** : `update_property` sur un champ **array** (tags, aliases, sources) corrompt le YAML — même bug qu'au Chantier 2, élargi. Règle ferme : jamais `update_property` sur un array → `update_note` ou Edit disque + reindex.
- **Source** : chantier 3/5, GO lots D+E de Raphael, fork CHANGELOG tranché (option 1 tracée au Ch.5, pas de scrub).

## 2026-06-07 — Chantier 3/5 wikilinks — réparations sûres A+B+C (133 → 124 liens brisés)

- **Lot A — casse leader (3 liens)** : ajout de l'alias kebab sur [[Boris Cherny]] (`boris-cherny`), [[Erik Schluntz]] (`erik-schluntz`), [[Thariq Shihipar]] (`thariq-shihipar`). Répare les liens kebab→Title Case. **Gotcha rencontré** : `update_property` sur `aliases` insère une 2e clé YAML (double déclaration) → frontmatter cassé. Fix = Edit disque du bloc `aliases` en liste unique, puis `update_property` scalaire (`derniere-maj`) pour forcer le reindex MCP.
- **Lot B — renommage, cible existe (5 liens)** : `[[ia-back-project]]`→[[ia_back]], `[[neo-ia-project]]`→[[neo_ia]] ([[audit-ia-back-25mai-quartet]]) ; `[[architecture-rag-canonique]]`→[[rag-architecture]] ([[feedback-sbi-radical-candor]]) ; `[[critique-will-vs-ecc-deux-doctrines]]`→[[will-vs-ecc-deux-doctrines-anthropic]] ([[google-mit-scaling-agent-systems-2025]]) ; auto-lien `[[neoia-test-infrastructure]]` retiré ([[neo-ia-tests-lenteur-diagnostic]] pointait vers elle-même).
- **Lot C — typo (1 lien)** : `[[thariq-shihpar]]`→[[Thariq Shihipar]] (shihpar→shihipar, [[affaan-mustafa-ecc-hackathon-winner]]).
- **Découvertes opératoires** : (1) le lint résout par alias (prouvé : `[[Thariq]]` a re-cassé quand l'alias `thariq` a été corrompu, puis re-résolu après réparation) ; (2) **l'index aliases/links du lint se rebâtit sur écriture MCP, pas sur Edit disque brut** → règle du chantier : Edit disque → `update_property` scalaire (reindex) → lint ; (3) backticks ne neutralisent PAS le lint (un `[[X]]` en code-span reste compté → option code-span pour F = morte) ; (4) delegate-guard faux positif sur les notes `04-Techniques/agents/*.md` (match `agents/` trop large) → contournement légitime via MCP `update_note`.
- **Vérif** : `lint_vault` 133 → **124** (−9 exactement), YAML cassé 0, 0 régression. Reste 124 = D+E+F+G (non traités ce lot).
- **Source** : chantier 3/5, GO A+B+C de Raphael.

## 2026-06-07 — Chantier 3/5 wikilinks — DIAGNOSTIC Phase 1 (lecture seule) + gotcha résolution MCP

- **Modifiée** : [[mcp-vault-llm-design]] — section GOTCHAS enrichie : `read_note` ne fait PAS de case-folding kebab↔Title Case (`read_note("boris-cherny")` introuvable alors que `Boris Cherny.md` existe), asymétrie avec `get_backlinks`/`move_note` case-insensitive. Conséquence : un wikilink kebab→Title Case est réellement mort pour la navigation LLM (pas un faux positif lint). Réparation = alias kebab, PAS `move_note`.
- **Diagnostic (aucune réparation)** : `lint_vault` = 133 wikilinks brisés, ~55 cibles distinctes. Classés en 7 causes (casse leader, renommage, typo, lien→composant `.claude/`, lien→memory, placeholder syntaxique, roadmap responsable-ia jamais écrite). Grille + plan Phase 2 dans `TODO/chantier-3-wikilinks-diagnostic.md`. Arbitrage Raphael attendu sur causes D/E/G avant réparation.
- **Source** : chantier 3/5 plan vault. Test décisif `read_note` vs `lint_vault` (lint a raison ici).

## 2026-06-07 — Chantier 2/5 normalisation tags — E1 complétion (1 note format yaml.dump sautée)

- **Modifiée** : 1 note ([[MOC-Techniques]]) — `#type/techniques` → `#type/technique` (mapping G1 déjà validé, complétion de E1).
  - **Cause** : le script de rename suppose les guillemets DOUBLES (`"#tag"`). Cette note était au format **yaml.dump** (clés triées alpha + guillemets SIMPLES `'#tag'` + items non indentés) — cicatrice de l'ancien bug `update_property`. L'extraction `val.startswith('"')` rate l'apostrophe simple → tag non reconnu → note **sautée proprement** (jamais corrompue : le script n'écrit que si `changes` non vide).
  - **Détection** : `get_tags` réindexé après E2 = audit d'ampleur complet sur disque → seul résidu de TOUS les mappings = `#type/techniques (1)`. Blast radius prouvé = 1 note.
  - **Fix** : `update_note` (réécriture maîtrisée, format yaml.dump préservé à l'identique), pas de réouverture du script pour 1 note. git diff = 1 ligne. `find_by_property #type/techniques` = 0.
- **Enrichissement à venir** : [[erreur-mcp-yaml-dump-corruption]] — les notes single-quote/clés-alphabétiques (cicatrices `update_property`) sont sautées non-corruptivement par un rename qui suppose les guillemets doubles.
- **Source** : chantier 2/5. **Chantier 2/5 réellement terminé, 0 résidu** (vérifié get_tags). Reformatage global des notes yaml.dump = chantier futur potentiel (hors scope tags).

## 2026-06-07 — Chantier 2/5 normalisation tags — LOT E2 (retraits de tags décoratifs)

- **Modifiées** : 4 notes — retrait de 4 tags décoratifs (1 ligne par note), 0 renommage. Décision sur preuve read-only validée par Raphael (chaque retrait justifié note par note).
  - `#personne/raphael` (note [[Raphael-Picard]]) — redondant avec `#type/casquette` sur sa propre note-racine.
  - `#position/critique` (note [[Yann LeCun]]) — posture d'1 leader, n'aide aucune navigation de groupe ; `#type/critique` désigne le type de note (DA), pas une posture.
  - `#chantier/22mai2026` + `#chantier/23mai2026` (2 notes) — repères temporels morts, jamais utilisés en navigation ; date portée par `derniere-maj` + titre.
  - Critère respecté : aucun de ces 4 tags n'aidait à retrouver un GROUPE ; chaque note garde ≥ 2 tags (reste trouvable).
  - **Outillage** : nouvelle logique « retrait » ajoutée au script (`normalize-tags.py`, sentinelle mapping → `""` = drop de la ligne). TESTÉE avant apply : `--show` AVANT/APRÈS des 4 notes → seule la ligne du tag retiré disparaît, frontmatter intact.
  - Vérif : git diff **retrait-only** (4 notes + script, 0 wikilink, 0 ligne ajoutée, 0 ligne supprimée hors item tag). `lint_vault` : **0 frontmatter cassé**, 133 wikilinks (stable). `find_by_property` : les 4 tags = 0.
- **Source** : chantier « vault forge-brain parfait » 2/5, grille singletons validée par Raphael (7 juin 2026). **Chantier 2/5 terminé** (LOTS C, A, B, D, E1, E2). Bilan get_tags avant/après à suivre.

## 2026-06-07 — Chantier 2/5 normalisation tags — LOT E1 (singletons : renommages / re-préfixages)

- **Modifiées** : 40 notes — 43 renommages, **2 déduplications**. Traitement des singletons par GROUPE (grille validée par Raphael, jamais tag par tag).
  - **G4 (fin du LOT A)** : toute la traîne `#sujet/*` résiduelle → `#domaine/*` (`sujet/` n'est pas un axe canonique). `skill` + `skills` unifiés en `#domaine/skills`. Cibles existantes (securite, audit, testing, vault, prompt-engineering, patterns, harness-engineering, plugin) absorbent ; le reste crée le `#domaine/X` légitime (claudemd, llm-wiki, memoire, methode, canoniques, maintenance, portabilite, specs, tokens, validation-doctrine).
  - **G2 (hors-convention → axe canonique)** : `#audit/*` → `#domaine/audit` · `#composant/agent|hook` → `#domaine/agents|hooks` · `#doctrine` (nu) → `#doctrine/2026` · `#meta/{bilan,externe,lessons-learned,working-memory}` → `#meta`. GARDÉS : `#rituel/*` (cluster cohérent casquette responsable-ia) et `#karpathy/{index,log,schema}` (auto-tag des 3 fichiers schéma).
  - **G1 (typos/variantes → forme dominante)** : `frameworks`→`framework`, `techniques`→`technique` (pluriels), `ai-security`→`securite`, `ai-alignment`→`alignment` (EN/variante), `#pattern/prompt*`→`#domaine/prompt-engineering` (les 2 dédups), `type/test`→`#domaine/testing`, `domaine/llm`→`#domaine/ia` (LLM générique ; `llm-research`/`llm-reasoning`/`llm-wiki` préservés), trio veille `type/industrie`+`type/veille`→`#type/news` (type « brève d'actualité » commun, sujet porté par `domaine/`).
  - Vérif : git diff **100 % tag-only** (40 notes + script, 0 wikilink touché). `lint_vault` : **0 frontmatter cassé**, 133 wikilinks (stable). `find_by_property` : `#sujet/skills`/`memoire` = 0, `#composant/agent` = 0, `#domaine/skills` = 3, `#type/news` = 3, `#domaine/llm` nu = 0 (les `llm-*` restent). `get_tags` (agrégat) en lag de réindexation — vérité prise sur `find_by_property`.
- **Source** : chantier « vault forge-brain parfait » 2/5, grille singletons validée par Raphael (7 juin 2026). E2 (retraits des 4 tags décoratifs) à suivre, séparé.

## 2026-06-07 — Chantier 2/5 normalisation tags — LOT D (projet/anthropic → domaine/anthropic)

- **Modifiée** : 1 note ([[Brad-Abrams]]) — `#projet/anthropic` → `#domaine/anthropic` (Anthropic n'est pas un projet du repo mais un domaine de veille). 1 renommage, 0 dédup.
  - **NON touchés (gardés distincts, vérifiés)** : `#org/anthropic` = **9** inchangé (axe affiliation des leaders Claude Code) · `#projet/neoteem` + `#projet/neoteem-brain` + `#projet/neoteem-po` = **20** inchangé (3 réalités distinctes).
  - Vérif : git diff **100 % tag-only** (1 fichier, 0 wikilink touché). `lint_vault` : **0 frontmatter cassé**. `find_by_property` : `#projet/anthropic` = 0, `#org/anthropic` = 9 (stable), `#projet/neoteem*` = 20 (stable).
- **Source** : chantier « vault forge-brain parfait » 2/5, décisions tags validées par Raphael (7 juin 2026). LOT E (singletons résiduels) à suivre pour arbitrage.

## 2026-06-07 — Chantier 2/5 normalisation tags — LOT B (technique/ outil/ → domaine/)

- **Modifiées** : 16 notes — fusion des axes `#technique/*` et `#outil/*` (prouvés redondants avec `#type/` + `#domaine/`) vers `#domaine/*`.
  - `#technique/agents` → `#domaine/agents` · `#technique/hooks` → `#domaine/hooks` · `#technique/testing` → `#domaine/testing` · `#outil/claude-code` → `#domaine/claude-code` · `#outil/atlassian` → `#domaine/atlassian` · `#outil/figma` → `#domaine/figma`.
  - Bilan : 22 renommages, **0 déduplication** (les notes ayant déjà `#domaine/claude-code` ou autre cible n'ont pas collisionné).
  - Vérif : git diff **100 % tag-only** (16 fichiers, 0 wikilink touché, 0 ligne hors `- "#..."`). `lint_vault` : **0 frontmatter cassé**, compteur wikilinks stable à 133 (cette fois pas de dérive — conforte l'artefact de réindexation du LOT A). `find_by_property` : les 6 axes `#technique/*` + `#outil/*` = **0** partout (axes disparus du vault).
- **Source** : chantier « vault forge-brain parfait » 2/5, décisions tags validées par Raphael (7 juin 2026). LOT D à suivre.

## 2026-06-07 — Chantier 2/5 normalisation tags — LOT A (sujet/ → domaine/ + cibles tranchées)

- **Modifiées** : 30 notes — fusion des synonymes de préfixe `#sujet/*` vers `#domaine/*` + 2 fusions multi-cibles.
  - `#sujet/mcp` → `#domaine/mcp` · `#sujet/hooks` → `#domaine/hooks` · `#sujet/workflow` → `#domaine/workflow` · `#sujet/agents` → `#domaine/agents` · `#sujet/orchestration` → `#domaine/orchestration` · `#sujet/karpathy` → `#domaine/karpathy` (concept, PAS `leader/` — la veille cc-news se fait par le dossier `05-Leaders/`, pas par tag).
  - Multi-cibles : `#sujet/doctrine` + `#domaine/forge-doctrine` → `#domaine/doctrine` (5 notes, sources disjointes : 4 + 1) · `#sujet/audit-thematique` + `#domaine/audit-vault` → `#domaine/audit` (5 notes).
  - Bilan : 33 renommages, **0 déduplication** (aucune fusion n'a produit de doublon dans une même note).
  - Méthode : même script déterministe que LOT C, dry-run + `--show` multi-cible validés AVANT `--apply`.
  - Vérif : `find_by_property` confirme `#sujet/*` = 0 partout, `#domaine/doctrine` = 5, `#domaine/audit` = 5. `lint_vault` : **0 frontmatter cassé**. Diff git **100 % tag-only** (0 wikilink touché, 0 ligne hors `- "#..."`, ajout comme suppression) — un changement de tag ne peut par construction ni créer ni casser un wikilink. Compteur lint affiché 132→133 non stabilisé : artefact de réindexation de l'agrégat après écriture raw (même gotcha que `get_tags`), pas une régression de lien — preuve diff > proxy compteur.
- **Enrichie** : [[erreur-mcp-yaml-dump-corruption]] — la section « gotcha agrégats retardés » généralise de `get_tags` à `lint_vault` (compteur wikilinks fluctue 131/132/133 indépendamment des edits tag-only) + méta « face à une consigne chiffrée, la preuve git directe bat le proxy compteur agrégé tronqué ; ne pas `git stash` pour mesurer (CRLF) ».
- **Source** : chantier « vault forge-brain parfait » 2/5, décisions tags validées par Raphael (7 juin 2026). LOTS B/D à suivre.

## 2026-06-07 — Chantier 2/5 normalisation tags — LOT C (formes projet)

- **Modifiées** : 21 notes — fusion des formes projet vers le nom EXACT du repo (underscore / tiret canonique).
  - `#projet/neo-ia` → `#projet/neo_ia` (15 notes) · `#projet/ia-back` → `#projet/ia_back` (7) · `#projet/forge` → `#projet/claude-forge` (2) · `#claude-forge` (nu) → `#projet/claude-forge` (1).
  - Méthode : script déterministe `.claude/scripts/normalize-tags.py` (dry-run validé + `--show` avant/après intégral), gère les 2 formats frontmatter (liste YAML + inline array). Les 3 outils MCP `*update*property` corrompent les tags multi-valeurs (bulk écrase l'array, update_property duplique la déclaration) → script raw en session principale, doctrine MCP-only respectée (la garde vise les dumps de lecture sous-agent, cf [[pattern-mcp-brief-then-direct]]).
  - Vérif : lint_vault 132 wikilinks brisés INCHANGÉ, 0 frontmatter cassé. `find_by_property #projet/neo-ia` = 0, `#projet/neo_ia` = 24 ✓. CRLF préservé (diff `2 +-`/`4 +-` par note, pas de réécriture LF).
  - Gotcha outillage : `get_tags` (agrégat) retarde après écriture raw ; `find_by_property` / `get_property` fiables immédiatement.
- **Enrichie** : [[erreur-mcp-yaml-dump-corruption]] — section datée : le fix regex (cas scalaires) casse les propriétés MULTI-LIGNES/arrays (items orphelins, double déclaration) ; cas array NON corrigé côté outil ; contournement script + `update_note` ; gotcha délai reindex `get_tags`. Claims étiquetées observé/inféré.
- **Source** : chantier « vault forge-brain parfait » 2/5, décisions tags validées par Raphael (7 juin 2026). LOTS A/B/D à suivre.

## 2026-06-07 — Réconciliation Important/ #5 (dernier) : skill.md absorbé dans comment-creer-skill — dossier Important/ vidé

- **Modifiées** :
  - [[comment-creer-skill]] — AJOUT section datée « SkillsBench (chiffres vérifiés) ». Deltas vérifiés source primaire (arXiv:2602.12670, skill `arxiv-verification` : YYMM 2602=fév 2026 ✓, titre ✓, arXiv-only sans venue) : +16,2 pp skills curées (abstract verbatim) ; Haiku 4.5+Skills 27,7% > Opus 4.5 sans 22,0% (corps) ; –1,3 pp skills auto-générées (Opus 4.6 +1,4 / GPT-5.2 –5,6) ; résolution L2→L3 (scripts+references = leviers perf). Seleznov 650-trial gardé avec hedge community non-vérifié.
- **Supprimées (hors vault)** : `Important/skill.md` — ~85% subsumé (anatomie skill-creator, matrice 3 environnements, checklist 6 dimensions, question set 3 rounds déjà présents), absorbé après lecture EN ENTIER doc (190L) + canonique + vérif arXiv des chiffres neufs.
- **Dossier `Important/` : VIDÉ.** 5 docs réconciliés (1 déplacé+enrichi, 4 absorbés). Doctrine single-source rétablie : toute la connaissance vit dans le vault, cherchable MCP.
- **Source** : passe réconciliation Important/ terminée (#5/5). Méthode constante : lecture EN ENTIER doc + canonique → diff claim par claim → vérif source des deltas neufs → enrich-first → suppression.

## 2026-06-07 — Réconciliation Important/ #4 : Stack IA.md subsumé (dispatch vérifié) + nettoyage sources mortes

- **Modifiées** :
  - [[stack-ia-production-2026]] — 3 mentions du chemin mort `Important/Stack IA.md` remplacées (frontmatter `sources:` + 2 dans le body) par « synthèse forge interne capitalisée, doc source archivé ».
  - [[economie-agentique-pricing-2026]] — ligne `sources:` `Important/Stack IA.md` remplacée idem.
- **Supprimées (hors vault)** : `Important/Stack IA.md` — INTÉGRALEMENT subsumé. Dispatché ce matin (7 juin) vers la note-carte [[stack-ia-production-2026]] (3 thèses + 5 recos + caveats) + [[economie-agentique-pricing-2026]] (chiffres Menlo/Klarna/Ramp/Harvey VÉRIFIÉS source primaire + 1 erreur corrigée : 76% buy vs taux conversion pilote→prod) + [[agents-securite]] (OWASP/lethal trifecta Willison/CVE MCP) + enrichissements agents-architecture/frameworks/stack-*-ia. Couverture vault SUPÉRIEURE au doc source (vérifications + corrections). Vérifié EN ENTIER doc + note-carte + 2 canoniques filles avant verdict.
- **Source** : passe réconciliation Important/ (doc #4/4 — dernier rapport du dossier). Reste : `skill.md` (brouillon meta-skill, diff fin à part).

## 2026-06-07 — Réconciliation Important/ #3 : reference-claude-md intégralement subsumé (0 enrichissement)

- **Supprimées (hors vault)** : `Important/reference-claude-md.md` — INTÉGRALEMENT subsumé par [[comment-ecrire-claudemd]], aucun delta neuf. La canonique contient déjà MODE AUDIT (13 signaux + procédure 5 étapes), MODE OPTIMISATION (5 passes), MATRICE règle/mécanisme, CHECKLIST 4 dimensions, hiérarchie + 3 leviers modularisation — ET bien plus (5 lignes Karpathy obligatoires, 8 éléments avancés, exemples repos vérifiés). Lu EN ENTIER doc (238L) + canonique avant verdict. Cas inverse de #1/#2 : zéro enrichissement, la canonique domine strictement.
- **Source** : passe réconciliation Important/ (doc #3/4). Aucune modif vault hors suppression du doublon.

## 2026-06-07 — Réconciliation Important/ #2 : reference-subagents absorbé dans comment-creer-agent

- **Modifiées** :
  - [[comment-creer-agent]] — AJOUT section datée « Résolution modèle (ordre exact vérifié) + invocation explicite + champs frontmatter récents ». Deltas vérifiés source primaire (code.claude.com/docs/en/sub-agents, 7 juin) : ordre résolution modèle env>param>frontmatter>inherit (le doc source l'avait INVERSÉ param/frontmatter → corrigé) ; syntaxe @-mention exacte `@"name (agent)"` + `--agent` session-wide ; champs récents `isolation: worktree`/`background`/`initialPrompt` ; scoped identifier plugin `plugin:review:security`.
- **Supprimées (hors vault)** : `Important/reference-subagents-claude-code.md` — ~95% subsumé (6 niveaux enforcement, 3 causes, table héritage, issues #43630/#32910/#18721 déjà dans la canonique), absorbé après lecture EN ENTIER du doc ET de la canonique 49 KB + diff claim par claim. Pré-verdict « contenu neuf » infirmé par la lecture complète (garde-fou dans les deux sens, cf [[feedback_lire_fichier_entier_avant_verdict]]).
- **Source** : passe de réconciliation Important/ vs canoniques (doc #2/4). Enrich-first + vérif source primaire des affirmations avant propagation.

## 2026-06-07 — Réconciliation Important/ #1 : reference-hooks absorbé dans comment-creer-hook

- **Modifiées** :
  - [[comment-creer-hook]] — AJOUT section datée « Correction count events (30) + fiabilité handlers http/mcp + champ continue universel ». 3 deltas vérifiés source primaire (code.claude.com/docs/en/hooks, 7 juin) : count events 29→30 (ajout MessageDisplay) ; http/mcp_tool échouent OUVERT (non-bloquant sur panne → hard policy = command+exit2) ; `{continue:false}` universel précède tout champ event-spécifique.
- **Supprimées (hors vault)** : `Important/reference-hooks-claude-code.md` — doublon à ~90% de la canonique, absorbé après lecture EN ENTIER + diff fin claim par claim (garde-fou lecture-entière, cf [[feedback_lire_fichier_entier_avant_verdict]]).
- **Source** : passe de réconciliation des docs `Important/` vs canoniques vault (1 doc à la fois, validation par doc). Enrich-first : deltas neufs absorbés AVANT suppression du source.

## 2026-06-07 — Capitalisation rapport « Référence technique ingénierie LLM » (serving/inférence + déplacement vers vault)

- **Ajoutées** :
  - [[serving-inference-optimisation]] (04-Techniques/serving/) — note neuve : choix moteurs vLLM/SGLang/TensorRT, PagedAttention vs RadixAttention, params vLLM, quantification FP8/AWQ/GPTQ, speculative decoding EAGLE-3/MTP, désagrégation prefill/decode, métriques TTFT/TPOT. Foyer serving d'inférence générale manquant (distinct de fine-tuning-infrastructure).
  - [[prompt-caching-kv-cache]] (04-Techniques/serving/) — note neuve : mécanique exacte prompt caching Anthropic (multiplicateurs 1,25×/2×/0,1×, ordre tools→system→messages, breakpoints), relocation trick ProjectDiscovery (hit 7%→84%, économie 59-70%), OpenAI/Gemini, KV-cache serveur, Code Mode. Complémentaire de [[Context Management]] (doctrine d'usage).
  - [[reference-technique-stack-ia]] (04-Techniques/serving/) — DÉPLACÉE depuis Important/ vers le vault (cherchable MCP), frontmatter ajouté (type reference, 5 aliases, tags). Référence exhaustive 8 sections sourcée VÉRIFIÉ/RAPPORTÉ. Original Important/ supprimé (git rm) — pas de doublon.
- **Modifiées** :
  - [[agents-evaluation]] — delta daté Langfuse→ClickHouse (acquisition 16 janv. 2026, Série D 400M$ Dragoneer, valorisation 15 Md$, 20 470 stars) vérifié source primaire (blog ClickHouse + BusinessWire). Ligne tableau corrigée (19K → 20K+, racheté ClickHouse) + callout `[!info]` daté. Wikilink vers [[reference-technique-stack-ia]] §6.
- **Source** : rapport `Important/reference-technique-stack-ia.md` (niveau implémentation). Doctrine reference-grade (advisor) : doc source = référence exhaustive, notes atomiques = deltas décisionnels seulement. Enrich-first respecté (RAG embeddings/reranking déjà riches → non touchés). Contrôle lint_vault avant/après : 131 wikilinks brisés inchangés (delta 0), 0 YAML cassé.

## 2026-06-07 — Constat tension cible/mesure maintenance corpus (allègement contexte forge)

- **Modifiées** :
  - [[pattern-maintenance-hybride-corpus-accumulatif]] — AJOUT sous-section « Tension cible vs mesure (constat 2026-06-07) » après « Cibles empiriques mesurées ». Cible ≤50 INCHANGÉE. Constat : après tri critère cité-OU-stratégique sur les 38 non-cités, 137 tier-1 retenus. Les 59 cités gardés en KEEP automatique jamais examinés → ni 50 ni 137 prouvés. À trancher lors d'une passe dédiée auditant aussi les 59 cités (cité ≠ stratégique). `derniere-maj` → 2026-06-07.
- **Source** : session allègement contexte forge (démotion tier-1 MEMORY 154→137, commit 2b6bd03). Tension surfacée à Raphael qui a demandé de l'inscrire comme constat empirique daté sans modifier la cible.

## 2026-06-07 — Capitalisation rapport « Stack IA en production 2026 » (enrich-first + vérif source primaire)

- **Ajoutées** :
  - [[economie-agentique-pricing-2026]] (2-Casquettes/responsable-ia/strategie/) — économie agentique, fin du SaaS par siège, pricing à l'outcome, cas Klarna/Ramp/Harvey, chiffres Menlo Ventures vérifiés source primaire
  - [[stack-ia-production-2026]] (Knowledge/syntheses/) — synthèse transverse : 3 thèses (simple→workflows→multi-agent ; read vs write ; evals = moat) + carte vers les 8 canoniques + 5 étapes recommandées + caveats
- **Modifiées** :
  - [[agents-architecture]] — doctrine simple→workflow→multi-agent, verdict read/write, leçons Anthropic (50 sous-agents), réconciliation chiffre serveurs MCP (~10K public vs 308/2797 registre), code execution with MCP (-98,7%), sécurité MCP
  - [[agents-securite]] — lethal trifecta (Simon Willison), défenses CaMeL/Llama Guard, table CVE MCP (tool poisoning, CVE-2025-49596, CVE-2025-6514, ToolHijacker)
  - [[agents-evaluation]] — « evals = new unit tests », workflow error-analysis, mix scorers 60/30/10, LangChain State of Agent Engineering 2025 (vérifié source primaire, correction barrière≠cas d'usage)
  - [[agents-frameworks]] — fiches Vercel AI SDK 5 (31 juil 2025) + Mastra (seed 13 M$ oct 2025, YC W25)
  - [[stack-typescript-ia]] — inférence maison Cursor Composer 2/2.5 (Kimi K2.5 confirmé arXiv 2603.24477, scores vérifiés)
  - [[../strategie/index]] (responsable-ia) — section économie agentique + ligne table 14 sujets
  - [[rag-chunking]] — derniere-maj (Contextual Retrieval déjà présent mot pour mot, aucun ajout)
  - [[comment-creer-hook]] — nouvel anti-pattern « Faux positifs de scope — émergent à l'usage » : table de 5 incidents forge (vault-cat-guard, hook hors-vault/plan file, meta-commentary regex, vault-before-specialist, delegate-guard sur note vault agents-*.md) + leçons structurelles (matcher par chemin, tester adverse, exception en tête). Promotion vault du méta-pattern (récurrence ≥5 incidents, cf memory-discipline)
- **Source** : `Important/Stack IA.md` (synthèse forge interne) — capitalisation enrich-first ; 3 chiffres décisionnels vérifiés à la source primaire le 7 juin (Menlo Ventures, LangChain State, Cursor Composer) ; marqueurs épistémiques (estimation d'enquête / claim vendeur / vérifié) préservés ; 2 corrections vs synthèse (76% achetés up from 53% ≠ 47% ; barrière qualité ≠ cas d'usage customer service)

## 2026-06-06 — Doctrine skills/agents enrichie depuis research LLM (matrice CLI/Desktop/Cowork)

- **Modifiées** : [[cowork-skills-reliability]] — nouvelle section « Matrice enforcement par environnement » : table CLI/Desktop/Cowork pour chaque mécanisme (hooks, MCP, CLAUDE.md, skills scanning, context:fork) + stratégie d'enforcement recommandée par cible (CLI fort, Desktop best-effort, Cowork par discipline)
- **Modifiées** : [[comment-creer-agent]] — nouvelle section « Matrice enforcement par environnement » appliquée aux agents + gotcha `context: fork` ignoré via Skill tool + règle agent-creator Cowork (no hooks, no stdio MCP)
- **Source** : research LLM Claude.ai juin 2026 (Important/skill.md) — triage bucket A/B/C, seul bucket B enrichi (direction solide, chiffres non vérifiés omis, hedges préservés)

## 2026-06-06 — Régression intermittente Problème B (skill spec PO) + triptyque de fix

- **Modifiées** : [[cowork-skills-reliability]] — section « Cas empirique » : régression intermittente (émojis qui sautent, puces markdown, encadré 1/2) = fluency bias ; fix = consigne FERME + checklist pré-action + rule permanente > reference à la demande. Souvent une étape d'ENTRÉE sautée (question non posée) qui se propage en section manquante. **Complément** : (4) checklist passive → GATE impératif « à voix haute » avec point qui régresse traité en dernier ; (5) frontière de responsabilité — la garde anti-oubli va dans le skill PROPRIÉTAIRE de l'artefact, pas « partout » (erreur encadré dans `maquette` corrigée par Raphael) ; (6) garde transverse `verification-skill-avant-validation` = relire le SKILL.md invoqué et cocher ses obligations avant toute validation/création.
- **Source** : session skills PO Neoteem (spec + maquette + review-maquette) — renforcement phase 1 (questions obligatoires), GATE VÉRIFICATION AVANT CRÉATION JIRA, 3 rules pour le `.claude` de Marie-Laure (`tickets-conformite`, `maquettes-conformite`, `verification-skill-avant-validation`).

## 2026-06-06 — Gotcha BOM SKILL.md + compétence-vs-plugin pour /spec nu (cas PO Neoteem)

- **Modifiées** : [[plugin-vs-skill-anatomie]] — 2 anti-patterns ajoutés : (1) BOM UTF-8 en tête de SKILL.md casse le frontmatter → « plugin validation failed » Cowork ou skill non chargée ; (2) plugin force le préfixe `/<plugin>:<skill>`, pour `/spec` nu distribuer la compétence individuelle (zip `dist/chat/`, pas de manifest = pas de validation).
- **Source** : session debug plugin PO Marie-Laure (skills `spec`/`review-ticket`) — symptôme « validation failed » + ticket rédigé hors-template = skill non chargée (BOM + mauvaise commande `/spec` vs `/neoteem-po:spec`).

## 2026-06-06 — Mémoire Claude Code Desktop = identique CLI (anti-confusion deux « Desktop »)

- **Modifiées** : [[plugin-vs-skill-anatomie]] — ajout section mémoire dans la table comparative + encadré anti-confusion. Distinction vérifiée source primaire : **Claude Code Desktop** (IDE) partage strictement le mécanisme mémoire de la **CLI** (`~/.claude/projects/<repo>/memory/`, CLAUDE.md, `@import`, v2.1.59+), tandis que **Claude Desktop** (app Chat/Cowork) a son « Auto Memory » Settings > Features (≠). Setup PO recommandé : Auto-Memory + `CLAUDE.local.md` gitignored sur repo partagé.
- **Source** : analyse du CLAUDE.md d'une PO Neoteem (Marie-Laure) sur Claude Code Desktop — confirmation doc Anthropic via claude-code-guide ([code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory)).

## 2026-06-05 — Contraintes Rovo agent en automation Confluence

- **Ajoutées** : [[rovo-agent-automation-confluence]] (04-Techniques/chatbot/) — contraintes dures d'un agent Rovo invoqué par automation (texte-seul `{{agentResponse}}`, pas d'écriture native = REST obligatoire, dédup par grounding non fiable via indexing delays, branching Confluence cassé) + fork archi auto-merge vs gate "À valider" + point à tester empiriquement (grounding en automation).
- **Modifiées** : [[rovo-agent-automation-confluence]] — section « Format doc cible pensé POUR le chunking/embedding » : paramètres réels prod (`confluence_ingest_v2.py` : 2500 chars/300 overlap, titre injecté par chunk, dédup par `page_id` sans content_hash) + insight contre-intuitif « nombre de pages neutre pour le retrieval, vrai levier = qualité chunks + write-time scoring ».
- **Source** : chantier chatbot support NeoIA — recherche doc Atlassian + lecture des 3 scripts de sync Confluence (neo_ia, scripts/ racine, neoteem-brain) = tous lecture→embed, verdict « aucun script de réécriture/publication Confluence dans aucun repo » (clients read-only confirmés).

## 2026-06-05 — Pattern dédup multi-source (convergence amont) dans rag-architecture

- **Modifiées** : [[rag-architecture]] — nouvelle section « Dédup multi-source : convergence amont vs dédup retrieval » (stratégie source canonique unique embeddée vs dédup au retrieval, gotcha barrière de validation, anti-gaspillage content_hash). Issu du chantier spec chat support neo_ia (architecture « tout converge vers Confluence »).
- **Source** : raisonnement /spec chat support multi-source (Jira→brain→Confluence→embedding) — pivot d'archi 3-ingestors → convergence + 2 blockers découverts (barrière validation qui fuit, écriture Confluence inexistante).

## 2026-06-05 — Enrichissement RAG : 2 vidéos Jonas Roman (ZParse) + cc-news RAG

- **Modifiées** :
  - [[Jonas Roman]] — ajout de ZParse (son outil d'ingestion RAG FR/EU, ISO 27001), 2 vidéos mai 2026 (pipeline d'ingestion + Supabase/pgvector), méthodo production (Golden Dataset, scoring chunks write-time, éval Précision/Recall/Faithfulness, doctrine « bottleneck = ingestion »).
  - [[rag-chunking]] — nouvelle section « Scoring de pertinence à l'ingestion (write-time) » : LLM-as-judge `relevant_score` 1-10 + filtre seuil à l'ingestion, comparaison write-time vs retrieval-time reranking.
  - [[rag-architecture]] — nouvelle section « RAG souverain EU » : Cloud Act vs localisation, AI Act 2 août 2026, Mistral OCR 3 self-host, vector DB EU (Qdrant/Weaviate/pgvector), stack support EU type.
  - [[rag-embeddings]] — sections « Parsing OCR amont (Mistral OCR 3) » et « Génération groundée — Cohere Command A+ » (MoE Apache 2.0, citations natives) + maj rôles Cohere (Patrick Lewis Director Agentic AI, Nils Reimers Director ML).
- **Source** : analyse profonde de 2 vidéos YouTube RAG (phZ_iqu1gN0 20 mai + yEmVTVTjzag 31 mai, Jonas Roman/Lagentia) via transcription Whisper + run cc-news ciblé RAG (verdict : aucune nouveauté technique post-2 juin ; vault déjà à jour, seules pépites = scoring write-time + souveraineté EU).

## 2026-06-05 — Piège here-string PowerShell dans le tool Bash

- **Modifiées** : [[erreur-da-heredoc-bash-silencieux]] — section "Piège connexe — here-string PowerShell `@'...'@` dans le tool Bash" : `git commit -m @'...'@` (syntaxe PowerShell) lancé via le tool **Bash** laisse le `@` de tête comme premier caractère littéral du sujet de commit. Distinct du HEREDOC bash. Règle : multi-`-m` dans Bash, `@'...'@` réservé au tool PowerShell.
- **Source** : gotcha observé cette session lors du commit `cc-features-ref` (sujet pollué `@ docs(...)`, corrigé par `--amend`).

## 2026-06-05 — Audit drift C2 : scope HEREDOC précisé

- **Modifiées** : [[erreur-da-heredoc-bash-silencieux]] — section "Scope exact" : le HEREDOC Bash FONCTIONNE en commande directe (vérifié empiriquement 5 juin : accents/$var/backticks OK, exit 0 ; 2 commits du 4 juin via `cat <<'EOF'`). Ne casse QUE sous `disallowedTools` ou dans un hook Git Bash. La doctrine "HEREDOC Windows à éviter" était trop large.
- **Audit drift 30j (sessions ⨯ canoniques)** : un seul vrai écart (HEREDOC). BOM PS 5.1 + Compress-Archive backslash déjà capitalisés (commits 283593d, 2c35c08). Conclusion : capitalisation à jour sur 30 jours, pas de dérive systémique.

## 2026-06-05 — Pattern checklist Tasks natif propagé aux canoniques

- **Modifiées** : [[comment-creer-skill]] + [[comment-creer-agent]] — section "Étapes séquentielles obligatoires → checklist Tasks natif (anti-oubli)" : `TaskCreate`/`TaskUpdate` pending→in_progress→completed pour les skills-questionnaires et agents multi-phases. Justif : Opus 4.8 interprète littéralement, ne généralise pas seul, peut sauter une étape sur un long enchaînement. Consolide ce qui était dispersé (audit-puis-vagues-paralleles, cowork-skills-reliability principe #9, changelog Opus 4.8).
- **Source** : conception de la skill `loop-forge` (9 blocs pilotés Tasks). Recherche web Opus 4.8 prompting (TaskCreate/TaskUpdate, interprétation littérale).

## 2026-06-05 — Note socle "concevoir un loop de travail" (méthode universelle)

- **Ajoutées** : [[concevoir-loops-travail]] (04-Techniques/claude-code/) — socle doctrinal de la future skill `/loop-forge`. Méthode universelle code & hors-code : 3 types de loop (inner/`/loop`/`/goal`), 4 briques (déclencheur/source/jugement/action), vérification obligatoire (tip #1 Boris 2-3x quality), **READ vs WRITE cross-repo** + pattern fleet, 3 infra (serveur/local/Desktop) + incompatibilités, 4 garde-fous (validation humaine/plafond coût/log/kill-switch), sortie SPEC puis dispatch.
- **Source** : interview Boris Acquired + recherches web (VentureBeat workflow, Sunghyun Roh READ/WRITE split, Anthropic managed-agents 7-strategy). Complète [[pre-compute-vs-inference-loops-boris]] (le pourquoi) côté comment.

## 2026-06-05 — Boris Acquired : pre-compute vs inference / "my job is to write loops"

- **Ajoutées** : [[pre-compute-vs-inference-loops-boris]] (04-Techniques/claude-code/) — fondement théorique des routines/`/loop`/Dynamic Workflows. 3 niveaux d'abstraction (écrire code → prompter Claude → écrire des loops qui promptent Claude). Principe **pre-compute > inference** (= "pre-compiling" : raise upfront / decrease ongoing) + verbatims nets ("a couple hundred Claudes running", "under-fund everything", principes → skills, taste s'érode, valeurs = dernier rempart).
- **Modifiées** : [[Boris Cherny]] — section "Interview Acquired (juin 2026)" + derniere-maj.
- **Source** : transcription Whisper (forge) de la vidéo native X (podcast Acquired, 30 min) partagée par @0xCodez le 4 juin 2026. Le tweet survend ("daily setup / $500 course") alors que c'est une interview origin-story — pattern tweet-hype, transcription source primaire privilégiée.

## 2026-06-04 — Note canonique plugin vs skill (compétence)

- **Ajoutées** : [[plugin-vs-skill-anatomie]] (04-Techniques/claude-code/) — skill = unité atomique (`<nom>/SKILL.md`), plugin = conteneur distribuable (skills + agents + hooks + MCP + LSP + monitors + bin + settings). Point critique : **un CLAUDE.md à la racine d'un plugin est IGNORÉ** (verbatim Anthropic plugins-reference) → instructions persistantes via skill, pas via CLAUDE.md embarqué. Claude Code = directory-based ; Claude Desktop/Web = upload .zip (Connectors pour MCP distant). Arbre de décision skill/plugin + application cas po-lojii Neoteem.
- **Modifiées** : [[plugin-vs-skill-anatomie]] — ajout section « README.md dans un plugin = doc humaine, JAMAIS affiché par Claude ». Vérifié primaire : README ni requis ni affiché ; seuls `displayName`/`description` du plugin.json apparaissent dans `/plugin` et le marketplace. Décision Neoteem : pas de README dans les 4 plugins `output/lojii/`, plugin.json soigné à la place.
- **Source** : Découverte Raphael (compétence vs plugin dans Claude Desktop) + vérification source primaire docs Anthropic (plugins, plugins-reference, skills) le 4 juin 2026.

## 2026-06-02 — Note INFO split crédit programmatique 15 juin (à-vérifier)

- **Ajoutées** : [[split-credit-programmatique-15-juin-2026]] (06-Industrie/) — annonce multi-sources tierces (InfoWorld, it-connect) : usage programmatique (Agent SDK, GitHub Actions, claude -p) tirerait sur un crédit mensuel dédié séparé des limites chat dès le 15 juin. Statut `a-verifier` explicite : ABSENT de anthropic.com/news ET support.claude.com en primaire au 2 juin. Montants non confirmés. Miroir du changement Copilot (lui confirmé primaire github.blog 1er juin). TODO re-check après le 15 juin.
- **Source** : sweep cc-news global (16 agents). Seul item actionnable survivant au tri source-primaire — impacterait les setups forge consommant de l'API programmatique. Le reste du sweep = déjà-vault ou antérieur au 2 juin (2 doctrine-impact-check harness + emphase = REINFORCE, pas de pivot).

## 2026-06-02 — Veille CC v2.1.160 (workflow→ultracode) + tri source primaire

- **Ajoutées** : [[CC juin 2026 - v2.1.160 ultracode]] (01-Claude/Code/changelog/) — drop 2.1.155→2.1.160 vérifié source primaire (raw GitHub CHANGELOG + anthropic.com/news). Point critique : le mot-déclencheur des Dynamic Workflows passe de `workflow` à `ultracode` (2.1.160). Aussi : Claude in Chrome via `/chrome` (2.1.157), Auto Mode Bedrock/Vertex/Foundry (2.1.158), durcissements sécu écriture fichiers shell/git config (2.1.160), IPO S-1 confidentiel (1er juin).
- **Source** : run cc-news (focus « vidéos prompting équipe Anthropic »). Le concept visé (« Claude prompts itself / améliore ton prompt avant de bosser ») était DÉJÀ doublement capitalisé : philosophie dans [[Code with Claude 2026]] (Boris Cherny higher-order prompts) + implémentation tranchée dans [[prompt-rewriter-pattern]] (pas de hook systématique, préférer /expand). Aucune recréation.
- **Note** : claims aggregateurs ÉCARTÉS après vérif primaire (advisor block) — crédits programmatiques 15 juin (20$/100$/200$), `/powerup`, hook `PermissionDenied`, `CLAUDE_CODE_NO_FLICKER` absents du changelog réel ET de anthropic.com/news. Pattern hallucination chiffrée aggregateurs ([[feedback_llm_deep_research_version_numbers]]).

## 2026-06-01 — 2 méthodes responsable-ia : réunion kit-de-décision + grille priorisation IA

- **Ajoutées** : [[reunion-kit-de-decision-autonome]] (2-Casquettes/responsable-ia/reunions/) — pattern d'animation quand les docs sont déjà lus : poser LA fourche, laisser un kit de décisions que la direction emporte pour trancher sans toi (influence sans présence). Verbatim des phrases pivots, dissymétrie comme argument, reframe repli→stratégie.
- **Ajoutées** : [[grille-priorisation-ia-loji]] (2-Casquettes/responsable-ia/priorisation/) — scorer les opportunités IA sur Impact + Moat ×2 + Faisabilité. Le moat (donnée Loji) compte double : priorise l'inimitable sur le faisable. Item parké volontaire pour prouver la discipline.
- **Source** : session 1er juin — Raphael prépare une réunion direction sur la trilogie de dossiers stratégiques IA (fourche éditeur vs facilitateur). Les 2 méthodes extraites du travail d'animation.

## 2026-06-01 — Guide maîtrise NotebookLM 2026 (deep-research vérifié)

- **Ajoutées** : [[notebooklm-maitrise]] (04-Techniques/outils/) — guide power-user complet : Studio 4 tuiles, Audio Overviews (4 formats + option « personnalisé » + mode interactif), Video Overviews + Cinematic, Slides/PPTX, Configure Chat Custom (mode auditeur), living documents Drive, sync Gemini bidirectionnel, quotas vérifiés 6 tiers.
- **Source** : demande Raphael (« utiliser NotebookLM à la perfection »). Workflow `deep-research` (5 axes, 24 sources, 106 agents, vérification adversariale 3 votes/claim → 13 confirmés, 2 réfutés). Sources majoritairement primaires Google (blog.google, workspaceupdates, support.google.com). Aucune note vault préexistante (seule mention dans [[RAG]]).
- **Note** : 2 claims réfutés exclus (Cinematic réservé tiers payants ; « 5× » uniforme). Quotas flaggés volatils (split Ultra 20TB/30TB post-I/O mai 2026).

## 2026-06-01 — Réflexe consultation vault sur question substantielle (Option C)

- **Modifiées** : [[erreur-vault-jamais-consulte-session-principale]] (Knowledge/erreurs/) — ajout 3e occurrence (audit skills, doctrine consultée tardivement) + FIX Option C appliqué : `skill-activation.py` re-fire le rappel `forge-brain` par SUJET (skill/agent/hook/claudemd/general) au lieu de once-per-session global. Le cas skill→agent dans une même session déclenche désormais 2 rappels (canoniques vault différentes), anti-spam même sujet préservé. Gotcha encodage accents documenté (test via echo bash = faux négatif).
- **Source** : session 1er juin 2026 — Raphael constate qu'un audit skills n'a pas consulté la doctrine vault AVANT. Diagnostic : aucun mécanisme ne rappelle de consulter le MCP. Fix advisory (exit 0, conforme doctrine 22 mai non-workflow-hook). Fichiers `.claude/` : `.skill-triggers.json` (triggers_by_subject) + `hooks/skill-activation.py` (tracker clés composites). 8/8 tests + stdin réel UTF-8 vérifiés.
- **Note** : trou de routing tripartite (« analyse profonde » ne lance pas boris/ecc/will-auditor) gardé hors-scope, option prête-à-coller documentée dans la note.

## 2026-05-30 — Erreur hook garde hors-vault bloque le plan file

- **Ajoutées** : [[erreur-hook-garde-hors-vault-bloque-plan-file]] (Knowledge/erreurs/) — un hook PreToolUse bloquant toute écriture hors-périmètre strict attrape le plan file `~/.claude/plans/` en faux positif → plan mode cassé. Cartographie 4 repos (seul neoteem-brain touché) + fix exception explicite + blocage classifier auto-mode sur édition de hook sécu.
- **Source** : session 30 mai 2026 — plan mode cassé sur neoteem-brain (`guard-external-writes.py`).

## 2026-05-29 — clean-memory corpus complet (mesure + capitalisation)

- **Modifiées** : [[pattern-maintenance-hybride-corpus-accumulatif]] — ajout section "Mesure corpus complet — clean-memory 2026-05-29" (répartition 94 KEEP / 73 POINTEUR / 49 PURGE sur 216 feedbacks, couche déterministe inopérante confirmée, plancher structurel <100, garde-fous validés).
- **Source** : exécution skill /clean-memory sur corpus complet `memory/` (hook saturation CRITICAL 282 fichiers). 3 Dynamic Workflows croisés (235 agents). Mémoire projet : `memory/` 282→232 fichiers, 216→166 feedbacks, commits forge ef78c70 (PURGE) + 25281a0 (slim).
- **Note** : aucune note vault créée (doctrine déjà couverte). Nouveau gotcha workflow `args` → mémoire projet `reference_workflow_args_array_gotcha` (cas empirique outil, pas doctrine réutilisable).

## 2026-05-29 — Idées agents IA issues des tickets support Neoteem

- **Ajoutées** : `1-Projets/Neoteem/idees-agents-ia-issues-tickets-support.md` — nouvelles idées d'agents dérivées du lexique de 250 tickets support réels (auto-diagnostic N1, qualification/triage, pré-vol comptable régul/clôture, préparation révision loyers). Chaque idée fondée sur des tickets SC réels, pas inventée.
- **Source** : exploration approfondie neoteem-brain ([[lexique-expressions-clients]] = 250 tickets SC déc 2025-avr 2026, proc-charte-qualification-n2, problèmes connus). Pour enrichir le catalogue d'idées de la roadmap CODIR.

## 2026-05-29 — Synthèse stratégique Neoteem (vue Responsable IA)

- **Ajoutées** : `1-Projets/Neoteem/comprendre-neoteem-vue-responsable-ia.md` — synthèse stratégique de Neoteem/Loji depuis le vault neoteem-brain (MCP obsidian-brain) : architecture (Lojii→ws→PG, logique 100% PostgreSQL, 12 schémas), domaines métier (syndic/gérance/compta), le MOAT (base de données Loji inimitable, acteur universel 27 rôles × 98 fonctions), apps IA existantes (NeoChat/NeoMail/NeoDoc), concurrents, et où l'IA crée de la valeur.
- **Source** : exploration profonde neoteem-brain (e-architecture-globale, e-organisation-neoteem, overviews syndic/gérance, MOC-Domaines, e-database-manager, e-module-suivi-dossier, q-roles-tiers-complet) pour outiller la trilogie docs CODIR (Stratégique + Roadmap + Modèle éco). Distinction validée Raphael : base Loji = moat (clients) ; 682 notes vault = accélérateur interne.

## 2026-05-29 (suite) — Audit .claude/ multi-repo : fixes forge + décision learning-reminder

- **Ajoutées** :
  - `Knowledge/decisions/decision-garder-learning-reminder-hook.md` — décision : garder `learning-reminder` (filet /done non fiable, exception assumée doctrine 22 mai) ; supprimer `proactivity-reminder`. Discriminateur blocking/advisory + fait technique « Stop ne supporte pas additionalContext ».
- **Modifiées (forge .claude/)** :
  - `settings.json` (édit manuel Raphael) — retrait registration `proactivity-reminder` du Stop. `hooks/proactivity-reminder.py` supprimé.
  - `rules/comportement-proactif.md:61` — règle morte « CLI Obsidian » → MCP forge-brain.
  - `rules/memory-discipline.md` — section MCP dédupliquée → wikilink (single-source).
  - `agents/devils-advocate.md` — `permissionMode: acceptEdits` → `plan` (agent read-only).
- **Source** : Audit `.claude/` multi-repo (pilote Dynamic Workflows). Fixes neo_ia/ia_back faits en sessions dédiées (briefs séparés).

## 2026-05-29 — Veille cc-news : Opus 4.8 + Dynamic Workflows (drop 28 mai)

- **Ajoutées** :
  - `01-Claude/Code/changelog/CC 28 mai 2026 - Opus 4.8 + Dynamic Workflows.md` — note atomique : modèle `claude-opus-4-8` (28 mai, défaut effort high, fast mode 3× moins cher, ~4× plus honnête sur failles code) + feature **Dynamic Workflows** (script JS d'orchestration, ≤1000 sous-agents / 16 concurrents, coordination hors-contexte, déclenché par « workflow » ou réglage `ultracode`, v2.1.154+, plans Max/Team/Enterprise). Changelog CLI v2.1.141→156 (MessageDisplay hook, disallowed-tools frontmatter skills, lean system prompt, fixes PowerShell Windows). Sources primaires WebFetch anthropic.com + claude.com.
- **Modifiées** :
  - `04-Techniques/claude-code/workflow-claude-code-optimal.md` — section « AJOUT 29 mai 2026 — Dynamic Workflows » : continuité doctrinale avec PTC et `no-cto-orchestrator-agent` (orchestration native vs agent custom interdit).
  - `.claude/skills/cc-news/SKILL.md` (via skill-creator, delegate-guard OK) — date de référence 21 mai → **29 mai 2026 (v2.1.156)**.
- **Source** : Veille `cc-news` domaine claude-code (3 agents A/B/C parallèles + Tier 0). Finding majeur croisé doctrine via `doctrine-impact-check`.

## 2026-05-28 (suite 5) — AMEND CLAUDE.md L14 v3 : scope ouvert "toute réponse substantielle"

- **Modifiées** :
  - `CLAUDE.md` L14 (via claudemd-optimizer, delegate-guard OK) — scope élargi de "6 catégories" à "toute réponse substantielle à une question Raphael (proposition, rédaction d'un ticket/commentaire/spec/explication, refonte, audit, jugement, recommandation, recherche web)". Clause "si aucune note pertinente → répondre quand même" ajoutée. Anti-pattern 28 mai 2026 (14 itérations rédaction commentaire ticket) tracé. Wikilink `[[erreur-vault-jamais-consulte-session-principale]]` ajouté.
  - `Knowledge/erreurs/erreur-vault-jamais-consulte-session-principale.md` (vault) — AJOUT section "2e occurrence — 28 mai 2026 (rédaction commentaire ticket Neoteem)" : contexte, cause-racine (trou doctrinal scope L14), conséquences (14 itérations, notes ratées), fix appliqué (AMEND L14 + feedback memory), pattern transverse renforcé, déclencheur réactivation (3e occurrence → Option B/C). `derniere-maj` mise à jour.
- **Source** : Session 28 mai — Raphael remonte "dès que je te pose une question, il faudrait que tu vérifies si on a des notes". Diagnostic empirique : l'AMEND L14 v2 (28 mai matin) couvrait audit/jugement mais pas l'assistance rédactionnelle (création ticket, écriture commentaire, spec, explication). Trou doctrinal de scope confirmé par 2e occurrence en 4 jours.

## 2026-05-28 (suite 4) — Archi backs Neoteem + stockage fichiers + webservices Jérôme

- **Ajoutées** :
  - `1-Projets/Neoteem/archi-backs-neoteem.md` — Contrats d'exposition front : neo_ia front IA uniquement, ia_back jamais front, métier hors scope. Anti-patterns + 8 itérations V1→V14 source.
  - `1-Projets/Neoteem/stockage-fichiers-neoteem.md` — Pas de S3 chez Neoteem. 3 options persistance : BDD JSON, Drive client (via webservices Jérôme), combo. Exception GCS NeoDoc.
  - `1-Projets/Neoteem/webservices-jerome.md` — 3 webservices métier réutilisables (Correspondance / AG / Drive). Checklist intégration. Wikilinks vers archi-backs + stockage.
- **Modifiées** :
  - `0-Inbox/context-actuel.md` — append session post-/done + update derniere-maj.
- **Source** : Session rédaction commentaire ticket Jira "Comparatif devis" (14 itérations V1→V14 pour caler l'archi).

## 2026-05-28 (suite 3) — Doctrine architecture cognitive 3-acteurs + hook saturation + pilote 29 fichiers

- **Modifiées** :
  - `pattern-maintenance-hybride-corpus-accumulatif` (vault) — AJOUT section "Architecture cognitive — trois acteurs" (~85L) : triade MEMORY.md/vault/memory* + workflow décision 4 étapes + template pointeur + 4 exemples PASS/FAIL + cibles empiriques. 2 aliases + 2 wikilinks ajoutés. `derniere-maj` 2026-05-28.
  - `.claude/rules/memory-discipline.md` — AJOUT section "Triade memory/vault/memory-physique (3 acteurs)" (~22L) avec workflow 4 étapes inline + anti-patterns + pointeur vers pattern vault.
  - `.claude/skills/done/SKILL.md` — AMEND via skill-creator (~9L) : callout doctrinal 3-acteurs + workflow 4 étapes entre Etape 2 et 2a. delegate-guard hook bloqué Edit direct = conformité doctrine `delegate-to-specialists` respectée.
- **Créés** :
  - `.claude/hooks/memory-saturation-watcher.py` — Hook SessionStart advisory (~85L). WARNING 80 / CRITICAL 100. Exclut MEMORY.md + _index_archive.md. Fail-open.
  - `.claude/hooks/tests/test_memory_saturation_watcher.py` — 5 tests pytest (2 nominaux + 3 adverses) — 5/5 verts. Baseline hooks 186 → 191.
  - `.claude/_backups/memory-pilote-pre-purge-2026-05-28.tar.gz` (573 KB) — backup défensif avant pilote.
  - `memory/feedback_ratio_empirique_doublons_memory_vault.md` (tier-1) — mesure 38% doublons pilote ancre seuils hook + workflow.
- **Pilote memory/ — 29 fichiers (3 PURGE + 8 POINTEURS + 18 KEEP)** :
  - PURGE : `feedback_audit_coherence_pattern.md`, `feedback_audit_repo_method.md`, `feedback_auditor_false_positives.md` (doublons confirmés [[audit-claude-folder-pattern]])
  - POINTEUR (body réécrit 11-20L) : `claim_security_must_be_provable`, `gotchas_line_numbers_verifies`, `x_articles_inaccessibles_empirique`, `advisor_da_mandatory`, `da_bash_write`, `da_failure_options`, `audit_qualite_design_transverse`, `repo_audit_workflow`
  - Index `MEMORY.md` et `_index_archive.md` synchronisés (3 entrées retirées + 1 entrée ratio ajoutée tier-1)
  - Compte : 274 → 271 fichiers / MEMORY.md 161 → 158 tier-1 / _index_archive 103 → 102 tier-2
- **`settings.json`** : ajout 3e hook SessionStart `memory-saturation-watcher.py` (édit manuel Raphael — classifier hard-block sur project settings).
- **Source** : cartographie empirique 274 fichiers (orphelins, âge, citations, clusters, auto-obsolètes) + pilote 29 fichiers (clusters verify-empirique 13 + advisor-da 6 + audit-methode 11). Verdict 38% doublons = SATURATION APPARENTE mais réelle. Couverture vault existante mesurée 60% (pattern-maintenance-hybride couvrait déjà mécanisme + rule memory-discipline frontière) → AMEND chirurgical retenu vs création doublon (cohérent feedback tier-1 single-source-truth).
- **Dette curative tracée** : 242 fichiers memory/ restants à auditer + 18 KEEP pilote re-classification possible. Déclencheur réactivation : hook CRITICAL chaque session OU `/clean-memory` périodique OU plage tranquille weekend.

## 2026-05-28 — AMEND CLAUDE.md L14 doctrine read_note session principale

- **Modifiées** : `CLAUDE.md` projet L14 (élargissement scope vault consultation à "audit / jugement / recommandation" + prescription verbatim "search_brain → read_note EN ENTIER" + anti-pattern explicite + wikilink [[pattern-mcp-brief-then-direct]])
- **Vault** : `context-actuel` mise à jour (section AMEND L14 + sweep empirique)
- **Mémoire** : `feedback_brief_prescrit_travail_deja_fait.md` créé tier-1 (distinct de feedback_brief_premisse_fausse — obsolescence ≠ fausseté)
- **Source** : Vérification empirique sous-gap doctrinal session principale (3 read_note EN ENTIER) ce matin. Brief auto-mode prescrivait Phase 1 création note canonique déjà existante (`pattern-mcp-brief-then-direct` AJOUT 28 mai). Pivot vers AMEND L14 ciblé + sweep drift confirmé nul.

## 2026-05-28 (suite 2) — AMEND CLAUDE.md L14 v2 nuance contexte

- **Modifiées** : `CLAUDE.md` projet L14 v2 (ajout `**si pas déjà en contexte**` entre "canoniques pertinentes" et anti-pattern parenthèse)
- **Mémoire** : `feedback_read_note_conditionnel_si_pas_deja_contexte.md` créé tier-1 + indexé MEMORY.md
- **Source** : Raphael surface tension implicite L14 (read_note EN ENTIER) vs L19 (tokens/contexte ultra-précieux). Garde-fou anti-double-pay sans dérogation doctrine — canonique déjà chargée transcript = citer + wikilink, pas re-read_note.

## 2026-05-28 (post-OVERVIEW) — 3 capitalisations /done

- **Ajoutée** : note canonique [[bug-tools-array-first-last-drop]] (04-Techniques/claude-code) — bug GitHub `anthropics/claude-code#60237` documenté avec verbatim issue, workaround padding, lien symptôme MCP décoratif observé forge (cause-racine plausible, repro à faire). Évite que la découverte forensique 28 mai reste enterrée dans working memory uniquement
- **Modifiée** : `memory/feedback_mcp_alias_ambigu_chemin_exact.md` — extension "28 mai 2026 — `update_property` non couvert (6e violation)". `mcp-alias-guard.py` actuel ne matche que `append_note` ; 6 outils MCP forge-brain prenant `file=<alias>` restent à découvert. Règle de mesure ancrée : tout outil `file=` peut écrire silencieusement sur le mauvais fichier sur stem ambigu. Workaround définitif = `read_note_by_path` + `Read`/`Edit` filesystem direct
- **Ajoutée** : `memory/feedback_surface_plutot_que_padder_ou_tronquer.md` (tier-2) — variante longueur de [[feedback_ecart_consigne_chiffree_surfacer]]. Capture la préférence Raphael confirmée chantier OVERVIEW : 230L vs cible 280-320L assumé sans padding ni troncature
- **Source** : étape /done post-livrable OVERVIEW Anthropic, 3/3 blocs validés [v] item par item

## 2026-05-28 (soir) — OVERVIEW.md Anthropic externe + fix chiffre tests 324

- **Livrées** : `OVERVIEW.md` racine repo (230L, présentation externe destinée Anthropic / Boris Cherny — 9 sections cadrage / 3 axes innovation / architecture défensive avec snippet `vault-cat-guard.py` / mécanismes anti-drift / méthodologie / validations empiriques / limitations / travail-en-cours / contact)
- **Modifiées** : `README.md` (chiffres alignés 10/48/12/9/438, paragraphe 3 axes, double pointeur OVERVIEW externe + SELF_PORTRAIT interne), `SELF_PORTRAIT.md` (correction chiffre tests 181 → **324** = 143 mcp-forge-brain + 181 hooks, 3 occurrences)
- **Découverte forensique bug GitHub #60237** : closed, titre exact *"Sub-agent frontmatter `tools:` array silently drops first and last positions at spawn time"*. Ne concerne pas le frontmatter MCP/skills. **Cause-racine plausible** du symptôme MCP décoratif sub-agent observé empiriquement (corrélation forte : `mcp__forge-brain__*` en position 1 des `tools:` array de tous les sub-agents forge). Repro formel à faire — tracé §8 OVERVIEW
- **Correction chiffre tests (capté par advisor avant commit)** : SELF_PORTRAIT portait "181 verts (143+38)" depuis ≥1 session, brief Raphael relayait passivement. Mesure empirique = 143 + **181** (hooks, confusion fichiers vs cas de tests). Vrai total **324 verts**. Fix appliqué 5 occurrences (3 OVERVIEW + 2 SELF_PORTRAIT). Feedback `chiffre-baseline-brief-verifier-empiriquement` amendé section "Renforcement 2e occurrence"
- **Discipline mesurer-avant-proclamer jusqu'au bout** : 2 chiffres SELF_PORTRAIT non re-vérifiables (`2,68s eager-boot`, `4 attributions doctrinales fausses`) → généralisés dans OVERVIEW. Aucun chiffre précis non vérifié dans doc destiné Boris
- **Notes vault** : aucune note créée (canoniques existantes wikilinkées), `context-actuel.md` mis à jour entrée 28 mai soir
- **Source** : engagement Anthropic en préparation, méthode A→B→D→E→F appliquée

## 2026-05-28 — SELF_PORTRAIT régénéré condensé

- **Modifiées** : `SELF_PORTRAIT.md` (racine repo, renommé depuis `CLAUDE_FORGE_SELF_PORTRAIT.md`, 631L → 151L)
- **Source** : photographie technique fidèle post bilan 27-28 mai. Chiffres remesurés (361 commits, 48 skills, 10 agents forge + 3 user-scope, 12 hooks Python + 1 inline, 9 rules, 453 notes vault, 181 tests verts, MEMORY 24,6k + archive 16,6k)
- **Méthode** : A→B→D→E→F (cartographie empirique → wikilinks canoniques → plan d'écart STOP → rédaction → capitalisation)
- **Notes vault** : aucune note créée/modifiée — wikilinks vers canoniques existantes uniquement

## 2026-05-28 — Bilan global 27-28 + test oracle vault-first 3/3 CONFORME

Note synthèse `Knowledge/syntheses/journee-27-28-mai-2026.md` créée pour archiver la séquence de 2 jours (113 commits, 110 le 27 + 3 le 28) — chiffres bruts vérifiés empiriquement (48 skills + 10 agents + 9 rules + 12 hooks, baseline 181 tests PASS du début à la fin), architecture livrée (mémoire portable, search_sessions MCP, tests adverses 3:1, comparaison Hermes, audit context tokens -43%, audit lifecycle 3 KILL/2 AMEND), patterns méta capitalisés avec wikilinks, dette résiduelle tracée (comment-creer-rule absente P2, gotcha obsidian-skills marketplace, /context à valider).

Test empirique du comportement oracle vault-first sur 3 scénarios représentatifs (skill creation / prompt engineering audit multi-repos / capitalisation page Anthropic). **3/3 CONFORME** : aucune réponse depuis savoir interne sans consultation vault, canoniques lues EN ENTIER via `read_note` sans `max_lines`, vérification non-doublon AVANT capitalisation (S3 a amendé `CC mai 2026 - Code with Claude` au lieu de créer doublon). La canonique a gagné une section "AJOUT 28 mai 2026 — Champs settings.json avancés" documentant v2.1.128 (`disableRemoteControl`), v2.1.136 (`policyHelper`), v2.1.143 (`worktree.bgIsolation`), helpers auth (`apiKeyHelper`, `otelHeadersHelper`, `awsAuthRefresh`, `gcpAuthRefresh`), skills avancés (`maxSkillDescriptionChars`, `skillListingBudgetFraction`, `skillOverrides`, `disableSkillShellExecution`), drop-in `managed-settings.d/` et sandbox détaillé.

Verdict global : claude-forge oracle vault-first VALIDÉ empiriquement, top 1-3% mondial fonctionnel (mesuré, pas estimé).

## 2026-05-28 — Propagation post-clean-memory : 4 items doctrinaux + note canonique 3 axes

Session de propagation des décisions issues du chantier `/clean-memory` du 27 mai. Quatre composants `.claude/` modifiés en cohérence : la skill `clean-memory` gagne une Section E (promotion/rétrogradation tier-1↔tier-2) avec critère mécanique formalisé (citation ≥1 OU 3 axes stratégiques OU pinned), `CLAUDE.md` ancre une 8e puce critique sous L25 affirmant "Tokens/contexte = ressource ultra-précieuse" avec mention de l'architecture tier-1 visible / tier-2 dans `_index_archive.md`, la skill `done` impose désormais résumés <80 chars et propose le tier à la création (défaut tier-2, 0 citation à la naissance), et un nouveau hook `memory-size-watcher.py` (SessionStart, advisory, seuil 38k chars avec marge 2k sous seuil système 40k, fail-open) accompagné de 5 tests pytest (181/181 verts post-merge) alerte préventivement quand MEMORY.md approche le mur.

Une note canonique `Knowledge/syntheses/3-axes-strategiques-forge.md` créée pour combler un trou doctrinal : les "3 axes stratégiques forge" (MCP décoratif sub-agent, agent vs skill densité MCP vault, living doctrine) étaient mentionnés dans skills et briefs sans note unique définissant leur scope précis — désormais ancrés avec wikilinks vers les notes canoniques sources ([[mcp-vs-skills-doctrine]], [[anti-reentrance-sub-agents-pattern-escalade]], [[methode-pivoter-doctrine]], [[raisonnement-22mai-doctrine-vs-enforcement]]).

Apprentissage méta capitalisé en mémoire : `feedback_chiffre_baseline_brief_verifier_empiriquement` (variante chiffrée de brief-prémisse-fausse — la baseline tests annoncée "319 → 324" mesurée empiriquement à 176 → 181, écart 143 silencieusement absorbé sans mesure aurait pollué le bilan) et `feedback_auto_violation_doctrine_fraichement_inscrite` (résumé feedback à 92 chars créé tour suivant de l'inscription de la règle <80 chars dans `done` — pattern d'oubli en sortie de chantier qu'il faut traquer). Une proposition Jarvis `/clean-memory-archive-only` (variante allégée sans gate par item pour les rétrogradations triviales) tracée dans la note 3 axes avec déclencheur de réactivation explicite — non livrée par discipline anti-sur-engineering (1 occurrence ≠ build).

## 2026-05-27 — Mémoire : MEMORY.md hiérarchisé tier-1/tier-2, divisé par deux

L'index mémoire `MEMORY.md` a franchi le seuil empirique de 40k chars (mesuré à 42.5k) — le déclencheur du pattern de maintenance hybride canonisé le matin même s'est appliqué à lui-même. Plutôt qu'un nettoyage cosmétique réactif, deux leviers structurels. Levier A : les 112 résumés d'index dépassant 80 caractères raccourcis radicalement (le slug porte déjà le concept, le résumé ne fait que compléter l'actionnable, le détail vit dans le fichier feedback). Levier C : hiérarchisation à deux niveaux — les 97 feedbacks cités au moins une fois ou jugés stratégiques (axes innovation MCP, contrat Jarvis, méta-doctrines fraîches de la journée) restent visibles dans `MEMORY.md` ; les 96 non cités partent dans un nouveau `memory/_index_archive.md`, chargé uniquement si une recherche le déclenche, avec un pointeur explicite depuis l'index principal.

Le critère « créé depuis moins de 60 jours » du brief initial a été abandonné après mesure : le corpus entier datant d'une seule semaine, il classait 194 feedbacks sur 194 en tier-1 et ne triait rien — surfacé à Raphael avant exécution plutôt que d'appliquer une consigne inopérante. Le critère retenu est la citation entrante (mécanique, vérifiable par grep), 44 % des feedbacks étant cités. Résultat : `MEMORY.md` passe de 42470 à 21493 caractères (−49 %), soit environ 5 à 6k tokens économisés à chaque session puisqu'il est chargé via `@import`. Un feedback obsolète (`use-obsidian-cli`, qui prônait la CLI Obsidian là où la doctrine actuelle impose le MCP) archivé pour de bon, ses deux wikilinks corrigés dans la note canonique Karpathy. Propagation de l'outillage (skill `/clean-memory`, règle tokens dans CLAUDE.md, hook de surveillance de taille à 38k) tracée pour une session dédiée post-`/clear`.

## 2026-05-27 — Hygiène permissions : settings.local.json épuré de 48 à 11 entrées allow

Palier d'hygiène repo. Le brief visait `settings.json` (« ~66 lignes de permissions ad-hoc accumulées »), mais la cartographie empirique a renversé la prémisse : le fichier versionné est discipliné — 11 hooks tous vivants, chaque permission tracée en commit, seulement 23 lignes de permissions sur 163. La vraie dette ad-hoc vivait dans `settings.local.json` (gitignored, perso), que le brief ne mentionnait même pas. Arbitrage de périmètre via AskUserQuestion → on cible le local seul, on ne touche pas le versionné.

Sur 48 entrées allow réelles (le « 51 » initial était une estimation visuelle, corrigée par `comm` sur le backup) : 25 supprimées en SAFE remove (doublons du versionné, l'anti-pattern `cd && git` qui contredit la doctrine `git -C`, 18 commandes one-shot mortes dont les `cp outcomes-test` d'un déploiement déjà fait, et un `Read` à double-slash résiduel), puis 13 entrées MCP `mcp__forge-brain__*`. Ces dernières étaient en arbitrage : un test empirique (retirer `list_notes`, l'appeler, observer) a prouvé que `enableAllProjectMcpServers: true` couvre les outils au niveau tool sans prompt — donc redondantes. Nuance observée en direct : le harness re-persiste l'entrée tool dans le allow après chaque appel MCP (re-sédimentation cosmétique à re-nettoyer périodiquement, pas une régression).

Backup hors-versionné dans `.claude/_backups/` (ajouté au .gitignore). `settings.local.json` étant gitignored, aucun commit ne le concerne — seuls le .gitignore, le vault et la mémoire sont versionnés. Deux apprentissages capitalisés : un brief peut poser une prémisse factuelle fausse (vérifier le périmètre réel avant d'exécuter), et la couverture tool-level d'`enableAllProjectMcpServers`.

## 2026-05-27 — Doctrine git corrigée : le deny `git merge` global n'a jamais existé (hypothèse C)

- **Diagnostic empirique 5 couches** : aucun deny `git merge` nulle part. `~/.claude/settings.json` = 12 entrées deny toutes destructives OS (`rm -rf`, `format`, `mkfs`, `shutdown`, `taskkill`, `kill -9`), zéro git. `settings.local.json` global absent. Repo `.claude/settings.json` + `.local.json` = vides. `grep -i merge .claude/hooks/` = aucun match. Le « branch first » est NATIF au harness Claude Code, pas une permission.
- **Cause** : le claim « `git merge *` en deny global » écrit le matin même (commit `b6731d4`) était une rationalisation a posteriori sur un symptôme observé (agent sur branche par défaut), sans vérification du settings. Doctrine fausse documentée ~6h.
- **Correction** : section CLAUDE.md `## Workflow Git (intentionnel)` → `## Workflow Git (convention)` (via claudemd-optimizer). « Convention humaine de discipline, pas verrou technique » — preuve empirique citée dans la formulation.
- **Capitalisation** : feedback mémoire `diagnostic-empirique-avant-affirmer-une-garde` (vérifier matériellement une garde avant de l'écrire dans un artefact doctrinal + citer la preuve). Leçon méta dans [[context-actuel]] : l'inférence fausse a traversé agent + humain + advisor sans demande de preuve.
- **Source** : divergence détectée lors du merge agent de la session audit transverse (le merge a marché → rien à contourner → le deny n'existait pas).

## 2026-05-27 — Audit transverse densité MCP write des 10 agents (flotte saine confirmée)

- **Audit (lecture seule)** : les 10 agents restants (post-KILL `vault-maintainer`) classés selon densité d'écriture MCP vault. Résultat **0 candidat KILL/PIVOT** — `vault-maintainer` était bien le cas isolé. 5 rare (4 créateurs + responsable-ia), 4 spécial (repo-inspector/outcomes-grader read-only, python-dev/self-updater écriture filesystem), 1 rare/dégradé (devils-advocate, 1 `create_note` non bloquant).
- **Nuance révélée** : le critère cible l'**écriture MCP vault** seule (`No such tool available` en sous-agent), PAS l'écriture filesystem `.claude/` via Write/Edit (qui fonctionne). Les 4 créateurs écrivent beaucoup mais sur le filesystem, leur `mcp__forge-brain__*` sert à la lecture des canoniques. Confondre les deux aurait produit 4 faux candidats KILL.
- **Prévention structurelle** : ajout d'une question-réflexe dans `.claude/agents/agent-creator.md` (section « Avant de créer ») — « métier = N× écritures MCP vault en boucle ? → SKILL pas agent ». Ancre le critère en prévention plutôt qu'en audit récurrent (doctrine « gardes en écriture > scanners périodiques »).
- **Capitalisation** : note canonique [[pattern-mcp-brief-then-direct]] enrichie (tableau write MCP vault vs filesystem + résultat audit 0/10) ; feedback mémoire `densite-mcp-write-vs-filesystem`.
- **Source** : proposition Jarvis tracée au KILL vault-maintainer. Méthode A→B→C→D→E + advisor + STOP étape D. Merge agent (deny `git merge` absent des permissions globales, vérifié empiriquement).

## 2026-05-27 — Chantier C : sync leaders vault↔cc-news (single source of truth)

- **Ajoutées (1)** : [[pattern-vault-source-unique-sync-mecanique]] (04-Techniques/patterns) — pattern forge : quand une liste vit dans le vault ET dans une skill consommatrice, le dossier vault est la source unique et un script régénère le bloc consommateur à la maintenance (entre marqueurs, idempotent, report des écarts non couverts), jamais au runtime.
- **Hors vault (.claude/skills/cc-news/)** : script `scripts/sync-leaders.py` créé — régénère le bloc « Leaders canonisés » des 6 `references/domain-*.md` depuis `list_notes(05-Leaders/<domaine>)`. Les 6 domain-*.md migrés (table Leaders → marqueurs SYNC + section « Watchlist signaux non canonisés » pour les cibles chassées sans fiche vault). SKILL.md cc-news documenté (163→179L). Mapping concurrents→industrie acté.
- **Diagnostic** : divergence bidirectionnelle mesurée (~36 fiches vault hors plans de chasse, ~14 cibles chassées sans fiche). `find_by_property(type=leader)` cassé (63/80) → `list_notes(folder)` seul fiable.
- **Dette tracée** : queries cc-news non régénérées (~50 leaders synced sans query, listés par le report `[!]` du script) — à compléter à froid ; normalisation `handle_x` des 80 fiches (mode dégradé : seuls les handles `x.com/` explicites injectés, denylist orga pour Han Xiao).
- **Source** : Chantier C, méthode A→B→C→D→E + 3 AskUserQuestion (mécanisme sync / divergence / handles) + advisor (rattrape le gap visibilité≠chasse).

---
## 2026-05-27 — Étape 3 : durcissement hooks (faux positif chaînage + angle mort PowerShell)

- **Hooks `.claude/` (hors vault)** : `vault-cat-guard.py` corrigé — segmentation de la commande sur `&&`/`||`/`;`/`|` avant détection ; un read-command et le marker vault doivent co-occurrer dans le MÊME segment (faux positif `git add "vault/..." && git push | tail` résolu). `security-guard.py` matcher `Bash` → `Bash|PowerShell` (angle mort : git push --force via PowerShell contournait le garde). 180 tests verts.
- **Découverts par usage réel** : 2 failles de `vault-cat-guard` émergées en l'utilisant (sur-blocage Read main → corrigé 2b ; faux positif commandes chaînées → corrigé étape 3). Audit transverse PowerShell : seul `security-guard` vulnérable parmi les hooks Bash-only.
- **Dette tracée** : cmdlets PowerShell-natifs destructeurs (Remove-Item/Stop-Process) non couverts par security-guard — session sécu dédiée.
- **Source** : usage réel du hook 2b + proposition Jarvis audit PowerShell validée.

---
## 2026-05-27 — Chantier A étape 2b : fix structurel MCP décoratif sub-agent

- **Ajoutées (1)** : `01-Claude/Code/best-practices/hook-intercepte-mcp-et-read-tools.md` — preuve empirique que PreToolUse intercepte les tools MCP, Read et PowerShell ; méthode de probe ; section exceptions delegate-guard (bypass `.new`+`mv`).
- **Modifiées (3)** : `comment-creer-skill`, `comment-creer-agent`, `comment-creer-hook` — section « Brief sub-agent et accès vault » (cause-racine MCP décoratif + interdiction accès brut + wikilinks). `comment-creer-agent` reçoit en plus la section « Self-modification d'un creator buggé via bypass de matcher ».
- **Hooks `.claude/` (hors vault)** : 2 hooks de garde créés — `vault-cat-guard.py` (bloque cat/grep/Read brut du vault ; Bash/PowerShell 2 contextes, Read sub-agent only, exempt vault-maintainer) et `mcp-alias-guard.py` (bloque append_note sur stem ambigu). 6 creators durcis. 170 tests verts.
- **Source** : Chantier A étape 2b — bug MCP décoratif confirmé empiriquement, fix par enforcement structurel + briefs inline durcis.

---
## 2026-05-27 — Chantier A : pont veille→doctrine (Paquet 1 livré)

- **Ajoutées (1)** :
  - [[doctrine-vivante]] (04-Techniques/claude-code) — note canonique posant le principe : la doctrine forge évolue par signal externe à fort crédit (Anthropic, leaders), pas seulement par erreur interne. 3 verdicts (INFO / DOCTRINE_PIVOT_CANDIDATE / DOCTRINE_REINFORCE), gate humaine non négociable, scan aveugle interdit (lien probe 0/12).
- **Hors vault (.claude/skills/)** :
  - Skill `doctrine-impact-check` créée (156L, opus) — opérationnalise [[doctrine-vivante]] : croise un finding dirigé avec les canoniques, produit un verdict + brouillon argumenté + gate `[v]/[m]/[i]`. N'appelle jamais [[methode-pivoter-doctrine]] directement. 3 TODO différés (C5 fraîcheur triggered-by-event, C6 ligne méta-doctrine, C7 arbitrage conflits).
  - Skill `cc-news` — étape 8 ajoutée : invoque `doctrine-impact-check` sur les findings MAJEURS (leader/Anthropic) uniquement, anti-cascade.
- **Source** : Chantier A, méthode A→B→C→D→E, 2 paquets (Core C1+C2+C3 livré ; C4-C7 différés à évaluer après usage). Bug MCP décoratif sub-agent découvert en cours → dette étape 2b tracée dans [[context-actuel]].
## 2026-05-27 — SELF_PORTRAIT régénéré (post Mémoire Portable + DA + Audit transverse + Veille)

- **Modifiées (1)** :
  - [[context-actuel]] (0-Inbox) — phase actuelle = SELF_PORTRAIT régénéré, métriques unifiées, suivant = Chantier A pont veille→doctrine.
- **Hors vault (racine repo)** :
  - `CLAUDE_FORGE_SELF_PORTRAIT.md` régénéré (630L) en update chirurgical par delta de section (pas rewrite). Métriques remesurées et unifiées sur source unique (`vault_stats`) : 302 commits, 244 tests (101 hooks + 143 MCP), 22 outils MCP, 430 notes, 193 feedbacks. Nouvelle section 8bis "Système de veille" (cc-news + 80 leaders + 3 chantiers A/B/C). Section Hermes déplacée en annexe B condensée. Dette double-source mémoire tracée (section 12). A3/A1 livrés + A1×A3 tué reflétés en section 8.
- **Source** : session dédiée post-/clear, mission régénération SELF_PORTRAIT. Méthode A→B→C→D→E avec STOP étape D + advisor avant écriture. Ancien portrait (commit `4332182`, même jour) périmé sur métriques (262 commits/207 tests) et 3 valeurs de notes divergentes (412/412/417).

## 2026-05-27 — DA compounding rétroactif (A1×A3) : idée tuée par probe empirique

- **Ajoutées (1)** :
  - [[critique-2026-05-27-compounding-retroactif]] (Knowledge/critiques) — devils-advocate sur le croisement A1×A3 (scanner les transcripts passés à /done pour rattraper les apprentissages non capitalisés). Verdict (c) **tué** : probe empirique sur 123 transcripts / 9631 messages → échantillon 12 hits sur la slice la plus chargée (`erreur|decision|pivot`) = **0/12 capitalisable-ET-nouveau**. Risque structurel n°1 = circularité C5 (l'indexeur garde les messages /done en clair → ils remontent comme faux apprentissages). Pivot retenu : `/recall-uncaptured <topic>` on-demand, à valider empiriquement (27 mai).
- **Modifiées (1)** :
  - [[idee-compounding-retroactif]] (0-Inbox) — statut passé à TUÉE + verdict DA appendé (préserve le 0/12 pour ne pas réouvrir le sujet sans nouvelle donnée).
- **Source** : session DA Phase 4, mission "challenger A1×A3 avant tout build". Méthode A→B→C→D→E + probe empirique (parseur réel `sessions_indexer`).

## 2026-05-27 — Mémoire portable (étape 7-9) : composants adaptés + doctrine résolution de path

- **Ajoutées (1)** :
  - [[resolution-path-3-contextes]] (04-Techniques/patterns) — note canonique : table empirique des 4 contextes de résolution de path (skill = `git rev-parse`, hook = `__file__`, settings command = `${CLAUDE_PROJECT_DIR}` expansion harness, .mcp.json = paths relatifs), avec preuve par ligne (27 mai).
- **Modifiées (3, amendements wikilinkés)** :
  - [[comment-creer-skill]] — AJOUT 27 mai : résolution path skill = `git rev-parse`, jamais `${CLAUDE_PROJECT_DIR}` (vide en skill). Wikilink vers note canonique.
  - [[comment-creer-hook]] — AJOUT 27 mai : résolution path hook = `__file__`, jamais `os.environ["CLAUDE_PROJECT_DIR"]`. Robuste au cwd. Wikilink vers note canonique.
  - [[architecture-decision-memoire-portable-import]] — résultat du test de validation (@import OK + double-source native non anticipée).
- **Composants `.claude/` adaptés (hors vault)** : skills `/done` (bloc PROJECT_ID supprimé, dédup+écriture → `$(git rev-parse)/memory`), `/recap` (lecture feedbacks → repo, dépendance `$(claude-project-id)` éliminée), `/install-forge` (section "Mémoire portable"), hook `session-reminder.py` (`glob ~/.claude/projects/*` → chemin déterministe `__file__`).
- **Mémoire** : feedback `import-ajoute-pas-remplace-automemory` (double-source transitoire, divergence 231/229).
- **Source** : session Mémoire Portable étape 7-9 (relais). Asymétrie 3 contextes de résolution de path découverte et capitalisée. Double-source transitoire acceptée comme dette tracée.

---
## 2026-05-27 — Mémoire portable : claude-forge self-contained

- **Ajoutées (3)** :
  - [[decision-memoire-dans-le-repo]] (Knowledge/decisions) — ADR actée : mémoire versionnée dans `<repo>/memory/`, chargée nativement via `autoMemoryDirectory` (user-scope, par machine). Remplace l'ADR en attente.
  - [[todo-rotation-password-postgres-prod]] (Knowledge/decisions) — TODO P0 : mot de passe PostgreSQL prod committé en clair (GitHub claude-forge + Bitbucket ia_back), redacté de HEAD mais présent dans l'historique. Rotation = seul fix réel.
  - [[decision-settings-global-modification-manuelle]] (Knowledge/decisions) — ADR : modifs `~/.claude/settings.json` = manuelles via diff fourni (hard-block classifier).
- **Modifiées (3, redaction sécu)** : `critique-2026-05-22-audit-neo_ia`, `critique-session-2026-05-20-running-notes-decompose-xread-mcp`, `erreur-password-postgres-clair-mcp-json` — secret PostgreSQL prod + IP serveur remplacés par `[REDACTED]` + mention de nettoyage rétroactif.
- **Mémoire** : feedback `claude-forge-self-contained-rien-hors-clone` ; amendement `verify-exhaustive-claims` (validation empirique baseline tests 244). Migration de 240 fichiers mémoire vers `<repo>/memory/` (versionné).
- **Source** : session Mémoire Portable — dernière faille de portabilité de claude-forge fermée. Audit confidentialité empirique : 1 secret prod détecté + redacté. ADR en attente [[adr-memoire-hors-repo-non-portable]] transformée en décision actée.

## 2026-05-27 — Phase 4 A1 : recherche transcripts session (MCP search_sessions)

- **Ajoutées** : [[ajouter-source-donnees-mcp-forge-brain]] (04-Techniques/claude-code/) — pattern canonique pour brancher une nouvelle source de données indexable sur le MCP forge-brain.
- **Modifiées** : roadmap Phase 4 (A1 marqué FAIT). Rule `forge-brain-proactive.md` (22 outils, ajout search_sessions). CLAUDE.md (22 outils, via claudemd-optimizer). Skill `forge-brain` (allowed-tools + 2 matrices, via skill-creator).
- **Source** : implémentation A1 — 22e outil MCP `search_sessions`. Code : `mcp-forge-brain/src/sessions_{indexer,db,watcher}.py` + `tools/brain.py`. 37 tests (~60% adverse), 0 régression (244 verts). Scan initial mesuré 2.68s (243 transcripts, 15858 messages, subagents exclus configurables).

## 2026-05-27 — Phase 4 A3 : capitalisation proactive à /done

- **Modifiées (2)** :
  - [[comment-creer-skill]] (04-Techniques/claude-code) — ajout section "Pattern skill qui propose un diff à valider" + corollaire "skill de jugement LLM n'est pas testable unitairement".
  - [[phase-4-comparaison-hermes-roadmap]] (0-Inbox) — section Statut d'implémentation : A3 marqué FAIT, A1/A2 à faire.
- **Composant** : skill `.claude/skills/done/SKILL.md` enrichie via skill-creator (304→310L) — génération de blocs prêts-à-écrire (feedback/note vault/ADR) + boucle de validation `[v]/[m]/[i]`, aucune écriture sans validation.
- **Mémoire** : feedback `capitalisation-proposee-pas-auto` — proposer le diff, jamais auto-écrire.
- **Source** : implémentation gap A3 roadmap Phase 4 (croisement Jarvis : couverture Hermes + contrôle forge).

## 2026-05-27 — Phase 4 : comparaison Hermes Agent vs claude-forge

## 2026-05-27 — Phase 4 : capitalisation post-session

- **Ajoutées (1)** :
  - [[idee-compounding-retroactif]] (0-Inbox) — piste produit issue de Phase 4 : croisement A1×A3 (chercher les transcripts non capitalisés à /done et les proposer). Capacité qu'aucun agent (Hermes ni forge) n'a. Liée depuis la roadmap.
- **Mémoire** : feedback `comparaison-concurrentielle-code-vs-marketing` — comparer un concurrent = lire le code cloné, tester l'hypothèse de positionnement (souvent fausse).
- **Source** : Stop hook learning-reminder, métacognition fin de Phase 4.

- **Ajoutées (3)** :
  - [[phase-4-comparaison-hermes-roadmap]] (0-Inbox) — audit code source Hermes Agent (Nous Research, 169k stars), matrice comparative axes prioritaires + plan d'action 3 catégories (combler/décliner/acquis).
  - [[adr-gaps-hermes-declines-phase-4]] (Knowledge/raisonnements) — ADR consolidée des 6 gaps Hermes déclinés, chacun avec déclencheur de réactivation.
  - [[avantages-acquis-claude-forge-vs-hermes]] (Knowledge/syntheses) — selling points vérifiés (mémoire graphe, delegate-guard bloquant, doctrine versionnée, capitalisation tracée) pour comm externe.
- **Source** : Phase 4, lecture code source réel (chemins+lignes), critère de pertinence use case synchrone. Verdict : claude-forge strictement supérieur sur mémoire structurée / conformité / traçabilité ; Hermes supérieur sur recherche transcripts + lifecycle skills + vitesse capitalisation autonome.

## 2026-05-27 — Pattern méta : pas de symétrie artificielle en priorisation

- **Modifiées (1)** :
  - [[audit-puis-vagues-paralleles]] — ajout section "Phase 3bis — Pas de symétrie artificielle entre axes" : un audit de N axes peut n'avoir qu'un seul P0, prioriser sur l'impact réel sans forcer un P0/P1 par axe. Test de discrimination + 2 occurrences (Phase 2 ratio 3:1 artificiel, Phase 3 advisor 1 P0 / 5 axes).
- **Source** : pattern méta observé sur 2 phases consécutives (27 mai). Capitalisé aussi en mémoire feedback.

## 2026-05-27 — Phase 3 renforcement (audit 5 axes + tests cœur MCP/hooks)

- **Créées (2)** :
  - [[phase-3-renforcement-audit]] dans `0-Inbox/` — matrice de priorisation des 5 axes (source de vérité).
  - [[decision-renforcements-differes-phase-3]] dans `Knowledge/raisonnements/` — ADR des P2/P3 différés + déclencheurs de réactivation.
- **Code** : +37 tests MCP (`test_search.py` 18, `test_resolve.py` 19 — couvre `search` 4 stratégies FTS5/BM25, alias expansion, resolve 3 tiers, suggest/tags/property) ; +25 tests hooks (`test_session_health.py` 12, `test_skill_activation.py` 13). 69→106 MCP, 76→101 hooks. 0 régression.
- **Caractérisation** : `resolve_note` tier 2 (substring) bat tier 3 (préfixe) — pinné, pas un bug.
- **Source** : phase 3 renforcement absolu avant comparaison Hermes. Advisor : un seul P0 (cœur MCP non testé), reste P2/P3 capitalisé.

## 2026-05-27 — Phase 2 tests adverses hooks critiques + fix bugs

- **Créées (1)** :
  - [[bug-caracterise-fix-trivial-vs-couteux]] dans `04-Techniques/patterns/` — pattern décisionnel : fix trivial = immédiat, fix coûteux = feedback pour phase dédiée.
- **Modifiées (1)** :
  - [[comment-creer-hook]] — étape 5 enrichie : règle "ratio adverse/happy ≥ 3:1 pour hooks sécu/contrôle" + piège du 3:1 artificiel + caractérisation de bug + testabilité (main() gardé). Réf agent fantôme corrigée (project-auditor → repo-inspector).
- **Source** : Phase 2 forge — suites adverses test_security_guard.py (26 tests, 5.3:1) + test_delegate_guard.py (29 tests, 8:1). 2 bugs trouvés ET CORRIGÉS : security-guard non testable (refactor main()), delegate-guard substring match agent_id (durci en exact-match, test caractérisé inversé en regression guard). Tests hooks 21 → 76, total repo 123/123 PASSED.

## 2026-05-27 — Phase 1 nettoyage claude-forge

- **Ajoutées (1)** :
  - [[erreur-deny-global-ecrase-allow-projet]] dans `Knowledge/erreurs/` — deny global `~/.claude/settings.json` écrase allow projet (précédence + diagnostic)
- **Modifiées (1)** :
  - [[comment-creer-agent]] — section "Frontmatter vs body : alignement obligatoire" (le frontmatter fait foi, le body ne le contredit jamais)
- **Source** : Phase 1 nettoyage forge (fix effort devils-advocate, restauration EXAMPLES.md upstream, coquille settings, décision skills cc-*-ref, tests 90/90 PASSED)

## 2026-05-26 — Veille 11 plugins officiels Anthropic + enrichissements canoniques

- **Créées (3)** :
  - [[plugins-officiels-veille-2026-05-26]] dans `04-Techniques/claude-code/` — synthèse comparative 11 plugins (hookify, skill-creator, agent-sdk-dev, code-review, mcp-server-dev, remember, atomic-agents, pydantic-ai, sourcegraph, data-engineering, forge-skills). 2 ADAPT, 3 REFERENCE, 6 SKIP.
  - [[anti-pattern-hookify-workflow-hooks]] dans `04-Techniques/claude-code/` — documente violation doctrine 22 mai par patterns `event: stop` + transcript conditions
  - [[eval-pattern-anthropic-skill-creator]] dans `04-Techniques/claude-code/` — pattern A/B `with_skill/baseline` + `run_loop.py` + viewer HTML. Gap vs outcomes-grader documenté.
- **Modifiées (2)** :
  - [[analyse-plugin-claude-code-setup]] — section veille 26 mai
  - [[comparaison-skill-anthropic-claude-code-setup]] — confirmation doctrine "on absorbe pas dans skill forge"
- **Enrichies (2 canoniques via skill-creator)** :
  - [[comment-creer-skill]] — section pattern eval Anthropic
  - skill `da-blocking-arbitrage` — confidence scoring 0-100 + seuil 80 (emprunté code-review Boris Cherny)
- **Source** : Demande Raphael 26 mai, marketplace.json 203 plugins, advisor + AskUserQuestion arbitrages
- **Doctrine reconduite** : aucune nouvelle skill forge créée, single source of truth = vault canonique

## 2026-05-25 (tour 2) — Audit ia_back quartet forge + 4 vagues parallèles

- **Créée** : [[audit-ia-back-25mai-quartet]] dans `Knowledge/syntheses/` — synthèse complète (verdicts, 4 vagues, comparaison neo_ia, apprentissages pattern)
- **Source** : Session forge 25 mai 2026 — premier déploiement quartet sur ia_back après neo_ia matin
- **Résultats ia_back** : commit `fdeee72` pushed develop, -280 LOC, +5 fichiers, 0 régression, 18 agents refactored via wikilink rules (308L économisées via script Python ponctuel)
- **Apprentissages** : refactor masse via script Python > Edit séquentiels (10+ fichiers), false positives auditor nécessitent vérif empirique, codebase-scanner détecte drifts invisibles dans `.claude/`

## 2026-05-25 — Casquette responsable-ia : formation exhaustive 8 axes

- **Créée** : casquette complète `2-Casquettes/responsable-ia/` (11 sous-dossiers thématiques)
- **Hubs créés** (10 index.md riches) : index racine, log, reunions, management, strategie, communication, priorisation, tickets, documentation, gouvernance, veille, templates, frameworks
- **Notes atomiques réunions (7)** : stand-up walking-the-board, sprint planning IA spike, sprint review demo eval, retrospective formats rotation, post-mortem blameless SRE, CODIR 6-pager Bezos, réunion client hype management, techniques ADR/RFC, facilitation Liberating Structures, async-first GitLab/Basecamp
- **Source** : recherche web 8 sub-agents parallèles (3000-4000 mots chacun, sourcés URLs) sur management équipe IA, rituels agiles, rédaction tickets, stratégie IA/gouvernance, communication direction non-tech, priorisation roadmap, comptes rendus, veille
- **Cibles** : Raphael Lead IA Neoteem (proptech, équipe 1-5, première fois rôle) — douleurs comm direction + priorisation
- **Cheat sheet exhaustive** : 70+ frameworks référencés (Amazon 6-pager, PR-FAQ, SCQA, BLUF, ADR Nygard, DACI, RICE, WSJF, GIST, OKR, SBI, BICEPS, Crucial Conversations, Liberating Structures, AI Act EU, NIST RMF, OWASP LLM Top 10, etc.)
- **Templates prêts à coller** : 6-pager, weekly update BLUF, ADR Nygard, postmortem blameless, CR réunion, spike Jira, DACI, PR-FAQ
- **Plan apprentissage 90 jours** structuré dans index racine

## 2026-05-24 (tour 2) — Innovations doctrine meta + auto-injection canonique

- **Modifiée** : [[comment-ecrire-claudemd]] — section "Tradeoff Karpathy NON inclus" + "Coexistence avec Critiques < ligne 25" simplifiée. 8 éléments Karpathy avancés au lieu de 6 (+ senior engineer test, + seuil 200→50 lignes).
- **Modifiée** : [[comment-creer-hook]] — nouvelle section "HOOKS TRANSVERSAUX — Catalogue à proposer en audit repo" (6 hooks réutilisables avec cas d'usage).
- **Modifiée** : [[methode-analyser-repo]] — étape 7 "Proposer hooks transversaux applicables" ajoutée.
- **Ajoutée** : [[critique-2026-05-24-meta-commentaires-doctrine]] — verdict DA VALIDER AVEC AMENDEMENTS + 7 infractions documentées + 6 amendements.
- **claude-forge/CLAUDE.md** : 7 infractions meta-commentaires purgées (L3, L51, L54, L55, L74, L87, L99) en 2 passes. Version 3.2.
- **Hook créé** : `.claude/hooks/meta-commentary-detector.py` (PreToolUse Write|Edit|MultiEdit) — 9 patterns, exclusions vault, désambiguïsation ≤3 mots. Tests 15/15. Settings.json.proposed à coller manuellement par Raphael.
- **6 agents patchés** : skill-creator, agent-creator, hook-creator, claudemd-optimizer, project-auditor, project-analyzer reçoivent section "Lecture obligatoire au démarrage" avec `read_note` SANS max_lines des canoniques correspondantes (innovation #2 auto-injection).
- **3 wikilinks morts fixés** : `skills-guide` → [[comment-creer-skill]], `agents-orchestration` → [[comment-creer-agent]], `hooks-guide` → [[comment-creer-hook]] dans cc-*-ref/SKILL.md.
- **Anthropic vérifié** : `claude-for-legal/CLAUDE.md` zéro meta-commentaire → doctrine forge alignée.

## 2026-05-24 — 5 lignes Karpathy en ouverture + anti-pattern meta-commentaires

- **Modifiées** : [[comment-ecrire-claudemd]] — ajout section "5 LIGNES D'OUVERTURE OBLIGATOIRES" en tête + 8 éléments Karpathy additionnels au corps niveau avancé (match style, dead code orphelin vs unrelated, plan format `[Step] → verify`, transformations tâches→goals, senior engineer test, seuil 200→50 lignes, critère succès auto-évaluable).
- **Ajoutée** : [[erreur-meta-commentaires-composants]] (Knowledge/erreurs/) — anti-pattern de justification/source/meta dans le contenu directif d'un composant (hook, agent, skill, CLAUDE.md, rule). Le pourquoi vit dans le vault canonique.
- **Source** : verbatim [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) — 100K+ stars Q1 2026, distillation Karpathy 26 jan 2026 sur LLM coding pitfalls.
- **CLAUDE.md propagés** (5 lignes Karpathy en tête) :
  - `claude-forge/CLAUDE.md` (via sub-agent claudemd-optimizer)
  - `neot-v2/ia_back/CLAUDE.md`
  - `neot-v2/neo_ia/CLAUDE.md`
- **Non propagés** :
  - `neot-v2/neoteem-brain/CLAUDE.md` : vault Obsidian, principes "diff minimal / code minimum" peu pertinents pour un repo de notes.
  - `neot-v2/neo_ia/packages/CLAUDE.md` : sous-CLAUDE.md additif, esprit "5 lignes en tête" pour les CLAUDE.md racine uniquement.
- **Décision additionnelle** : PAS de ligne italique tradeoff sous les 5 lignes (bruit visuel, dilue le signal — anti-pattern formalisé dans [[erreur-meta-commentaires-composants]]).

## 2026-05-23 — Audit thématique 07 leaders/modèles/industrie/concurrents : ~40 notes patchées sur 98 auditées (135 claims)

**Méthode** : 7 sub-agents parallèles par cluster (affiliations+benchmarks / stars / verbatim Anthropic / papers arXiv / concurrents / industrie funding / attributions sensibles) + 3 self-verify WebFetch directs. Méthode validée 6× consécutivement.

**Patches majeurs** :
- **Karpathy → Anthropic 19 mai 2026** (rejoint équipe pre-training sous Nick Joseph). Fiche `Andrej Karpathy.md` updatée + verbatim X post + source TechCrunch
- **Sutskever CEO SSI depuis juillet 2025** (pas 2024, Daniel Gross était CEO initial)
- **Cat Wu Mercado Libre 23K/500K/9K + Oscar Mowen** : marqués ⚠️ "à confirmer livestream YouTube" — aucune source externe accessible ne mentionne ces chiffres (Every podcast, Lenny, TechCrunch, MIT Tech Review, Fortune London, Chris Ebert blog). Possible mais non vérifié à date 23 mai. Propagé dans `Code with Claude 2026.md` + `Managed Agents.md`
- **Jeremy Hadfield Dreaming specs** (`dreaming-2026-04-21` / max 100 sessions / restriction modèles) : marquées non vérifiées (WebFetch direct anthropic.com/news/dreaming = 404 au 23 mai)
- **Anthropic valorisation $380B fév 2026 (Series G post-money) vs $900B en négociation mai 2026** (Bloomberg 12 mai) — préciser dans `Dario Amodei.md` + `industrie-mai-2026.md` ($30Mds levée, pas $50Mds)
- **xAI 11 co-fondateurs** (pas 12). Merger SpaceX-xAI annoncé 2 février 2026 (pas mai)
- **Cursor $2B ARR fév 2026** (vs $500M juin 2025 obsolète). SpaceX/Cursor deal $60B + $10B breakup fee (CNBC + TechCrunch)
- **Stars GitHub drift x1.8-x4** corrigés : Karpathy AutoResearch 21K→82.9K, Ghostty 30K→55K, llama.cpp 150K→112K (sur-estimait), Unsloth 40K→65K + 10M downloads requalifié 2.19M PyPI, LLM Course 70K→79.6K, LLaMA-Factory 68K→71.5K, CrewAI 50.8K→52K, BabyAGI 20K→22.3K, sentence-transformers 15K→20.7K modèles HF
- **Papers premier-auteur vs senior** précisés : Self-Consistency (Wang premier, Zhou senior), SWE-agent (John Yang premier, Yao co-auteur), BEIR (Thakur premier, Reimers co-auteur), AWQ (Ji Lin premier, Song Han senior), FlashAttention-4 (Zadouri/Shah/Hohnerbach co-leads, Tri Dao senior)
- **Awards corrigés** : Schulhoff Prompt Report **PAS** EMNLP Best Theme (c'est HackAPrompt 2023). LlamaFactory = ACL 2024 System Demonstrations (pas main track). FlashAttention-4 = MLSys 2026 Best Paper Honorable Mention ajouté. Hassabis Nobel 1/4 + 1/4 + 1/2 Baker (pas 1/3-1/3-1/3)
- **Doublons fusionnés vers dossier primaire** (canoniques marquées) :
  - Harrison Chase canonique = `agents/`, doublon `rag/` marqué
  - Jerry Liu canonique = `rag/`, doublon `agents/` marqué
  - Ethan Mollick canonique = `industrie/`, doublon `prompt/` marqué
  - Hashimoto canonique = `claude-code/Mitchell-Hashimoto.md` (version "popularisé + hedge"), doublon `agents/hashimoto.md` corrigé "INVENTÉ" → "popularisé"
- **Lisa Crofoot** : verbatim "8 frontier models", "scaffolding holds Claude back", "Mythos OpenBSD 27 ans" — attributions à confirmer livestream (sources externes ne confirment pas l'attribution précise)
- **Mikinka UCL** retiré (non attesté arXiv), Dettmers "pause santé fév 2025" retiré (non sourcé)
- **Lilian Weng "46,900+ citations Scholar"** retiré (blog post sans entrée Scholar)
- **Daisy Hollman "red squigglies" / Alex Albert** : mention Albert retirée (non sourcée)
- **Boris Cherny "$1B ARR + Bun"** précisé : annonce corporate Anthropic 2 déc 2025 (pas verbatim Boris). "Coding solved" "late 2025/entering 2026" (pas spécifiquement "oct 2025")
- **Daniel Han Unsloth "10M downloads"** : requalifié comme cumulé multi-canaux ; PyPI réel = 2.19M/mois (mai 2026)

**Notes erreur** : pattern récurrent confirmé "venues conférence inventées" + "stars GitHub drift x3-x6 / 6 mois" + "specs techniques fabriquées sans source primaire" (Dreaming) + "chiffres clients fabriqués paraphrasés comme verbatim" (Mercado Libre/Oscar Mowen)

## 2026-05-23 — Audit thématique fine-tuning : 22 corrections sur 87 claims

- **Auditées** : 10 notes `04-Techniques/fine-tuning/*` via 7 sub-agents parallèles WebFetch direct
- **Corrigées** (9 notes patchées) :
  - `fine-tuning-techniques-peft` : intruder dimensions (FAUX NeurIPS 2025 → arXiv 2410.21228 sans venue), Spectrum -36% retiré, DoRA reformulé, QLoRA verbatim abstract, ajout sources auteurs (Hu/Dettmers/Liu/Hartford)
  - `fine-tuning-alignment` : SimPO (Princeton), KTO (Contextual AI), ORPO (KAIST), DAPO (50 pts AIME), GRPO chiffre -50% retiré, sources arXiv ajoutées
  - `fine-tuning-frameworks` : stars actualisées (Unsloth 65K, MLX 26K, LLaMA-Factory 71K), torchtune marqué "no longer maintained 2025", TRL v1.0 mars 2026 confirmé, FSDP 5x reformulé
  - `fine-tuning-infrastructure` : TGI archivé GitHub 21 mars 2026, neoclouds 40-85% (pas 40-70%), Together AI/AWS pricing précisé, Lambda RTX 4090 N/A, TCO seuil scoping
  - `fine-tuning-models` : Gemma 3 corrigé (1B/4B/12B/27B, Gemma Terms of Use pas Apache), Llama 88.4% précisé (3.3 70B Instruct), DeepSeek licenses nuancées, Qwen >50% sourcé HF Spring 2026
  - `fine-tuning-privacy` : VaultGemma ε+δ précisés, TEE benchmark ETH Zurich arXiv 2509.18886, TrueFoundry (ResMed pas Medtronic), EU AI Act delay mai 2026, FIT/LLMEraser sources arXiv
  - `fine-tuning-datasets` : LIMA sourcé (arXiv 2305.11206) au lieu de "200 vs 2000" non sourcé, stars Argilla/Label Studio actualisées
  - `fine-tuning-evaluation` : stars actualisées (lm-eval-harness 12.7K, DeepEval 15.6K x3), Skywork 57.43% précisé, JudgeBench ICLR 2025 **confirmé** (différent du pattern intruder dimensions)
  - `rag-vs-fine-tuning` : seuil "200K tokens" retiré (non sourcé), reformulé en doctrine corpus + caching
- **Créée** : `Knowledge/erreurs/erreur-audit-fine-tuning-2026-05-23.md`
- **Patterns capitalisés** : venues inventées (NeurIPS/ICLR), stars GitHub drift x3-x6, chiffres marketing à scoper case study, confusion training vs inference pricing
- **Source** : Audit thématique vault 05-fine-tuning (post-audit RAG + Claude Code 23 mai)

## 2026-05-23 — Post-audit RAG : fiches leaders manquantes + capitalisation erreurs

- **Ajoutées** :
  - `05-Leaders/rag/Jerry Liu.md` — co-fondateur CEO LlamaIndex, agentic RAG, LlamaParse
  - `05-Leaders/rag/Harrison Chase.md` — co-fondateur CEO LangChain, LangGraph, LangSmith
  - `Knowledge/erreurs/erreur-audit-rag-11-faux-2026-05-23.md` — synthèse 11 FAUX audit RAG + 6 patterns récurrents (arXiv YYMM, URL swap, paraphrase, inversion modèle, seuil inversé, chiffres fantômes)
- **Mémoire forge** :
  - `feedback_arxiv_id_yymm_format.md` — format YYMM doit matcher mois cité
  - `feedback_arxiv_url_swap_papers_similaires.md` — N papers domaine = URLs swapées
- **Modifiée** :
  - `04-Techniques/rag/RAG.md` — descriptions Jerry Liu / Harrison Chase enrichies

---

## 2026-05-23 — Audit thématique 03 RAG (~78 claims auditées)

- **Modifiées (10 notes + 3 enrichissements squelettes)** :
  - `04-Techniques/rag/RAG.md` (MOC) — retrait "73% retrieval" + "65%/85-90%" non sourcés, attribution Lewis et 11 co-auteurs Meta/FAIR/UCL/NYU, marché $11B avec source Grand View, Karpathy verbatim canonique
  - `04-Techniques/rag/rag-architecture.md` — Self-RAG arXiv 2023/ICLR 2024, RAPTOR Stanford (pas Stanford/Google), GraphRAG chiffres marqués "source secondaire", Gemini 1.5 Pro >99.7% multi-fact corrigé (inversion modèle), 200K seuil verbatim Anthropic, Lamini case study Fortune 500
  - `04-Techniques/rag/rag-chunking.md` — NAACL 2025 Vectara/UW-Madison auteurs, FloTorch source, overlap 10-20% (pas 50-100), Late Chunking inversion 0.8516/0.8590 corrigée, H-RAG 0.4271 (pas 0.4728), NMF 19.6-32.6x, NVIDIA tableau corrigé
  - `04-Techniques/rag/rag-embeddings.md` — Voyage 65.1 (pas 67.1), Cohere dims 1536 (pas 1024), Voyage "médical" retiré, NV-Embed-v2 marqué MTEB v1 EN, BBQ Elasticsearch 8.16 + Qdrant 1.5-bit, ColBERT 554% = FastPlaid attribution, quantization 96% (pas 99%+)
  - `04-Techniques/rag/rag-reranking.md` — tableau benchmark non traçable retiré, leaderboard ELO Agentset complet, Contextual Anthropic verbatim ($1.02/M)
  - `04-Techniques/rag/rag-vector-databases.md` — "70% workloads pgvector" retiré, bornes techniques vanilla <10-20M et pgvectorscale <50M+, Instacart blog source
  - `04-Techniques/rag/rag-metadata.md` — Qdrant 10-15 = règle empirique, Unstructured "75%" précisé "réduction erreurs préparation données", Markdown 20-40% HTML clean/68-87% réel, cache cosine 0.80 (pas 0.95), seuils RAGAS marqués "non canoniques", Crucible précisé
  - `04-Techniques/rag/tool-retrieval-query-expansion.md` — **TOOLQP date 2025→2026**, **MCP-Zero URL 2603.13426→2506.01056**, OATS clarifié 2603.13426, ToolHijacker contexte shadow/target, Lost-in-Middle dissocié Liu 2023 vs blog vLLM
  - `04-Techniques/fine-tuning/rag-vs-fine-tuning.md` — RAFT affiliations 100% UC Berkeley (Microsoft/Meta contributeurs blog seuls), ratio P=80% nuancé, Lamini case study Fortune 500
  - `04-Techniques/rag/rag-evaluation.md` — squelette 30L → enrichi avec RAGAS/DeepEval/LLM-as-judge, patterns d'évaluation, pitfalls
  - `04-Techniques/rag/rag-production.md` — squelette 30L → enrichi avec pipelines ingestion, retrieval multi-stage, drift detection, multi-tenancy, observabilité
  - `04-Techniques/rag/ColPali.md` — squelette 30L → enrichi avec architecture PaliGemma+ColBERT, ICLR 2025, ViDoRe benchmark, comparatif Jina v4

- **Bilan** : ~78 claims dont 11 ❌ (14.5%) + 34 ⚠️ (45%) → corrections appliquées en 1 session. Cluster 3 (embeddings) = 0 erreur (modèles Harrier-OSS-v1, Jina v5 confirmés réels). Cluster 6 (doctrine) = 30% erreurs (extrapolations forge).

- **Source audit** : `output/audit-vault-thematique/03-rag/` (A-inventaire + 6 rapports cluster + D-synthèse + F-rapport final)

---

## 2026-05-23 — Audit thématique 06 patterns + context + stacks (~92 claims auditées)

- **Modifiées (13 notes vault + 2 fichiers .claude)** :
  - `04-Techniques/patterns/LLM Wiki.md` — réécrite : sources Karpathy gist, retrait "70x RAG" non attesté, "400K mots" → verbatim "~100 sources, hundreds of pages"
  - `04-Techniques/patterns/Silent Assumptions.md` — Karpathy 4 anti-patterns sans hiérarchie (suppression "#1")
  - `04-Techniques/patterns/architecture-cerveau-obsidian-mcp.md` — ponctuation verbatim Karpathy `;` (point-virgules)
  - `04-Techniques/patterns/config-guardian-pattern.md` — ponctuation verbatim Karpathy
  - `04-Techniques/patterns/pattern-github-spec-kit.md` — Spec Kit 105K stars, 7 fichiers (pas 8), 40+ extensions (pas 80+)
  - `04-Techniques/patterns/pattern-gsd-framework.md` — Lex Christopherson / TACHES, ~59K stars, 29 skills (commandes exactes hors scope)
  - `04-Techniques/patterns/pattern-sdd-triangle.md` — 3 niveaux maturité = **Böckeler/Thoughtworks** (pas Breunig ni Park)
  - `04-Techniques/patterns/pattern-spec-driven-development.md` — chiffres stars actualisés, attribution 3 niveaux Böckeler, suppression S*=0.509, BMAD 21 agents
  - `04-Techniques/patterns/pattern-figma-mcp-claude-code.md` — 8 skills officielles (pas 7 inventés), env var MAX_MCP_OUTPUT_TOKENS, sources élargies
  - `04-Techniques/patterns/running-implementation-notes.md` — date 19 mai 2026, métriques 951 likes/44 RT, URL tweet à retrouver
  - `04-Techniques/context-engineering/Context Engineering.md` — réécrite : 4 piliers communauté pas Karpathy, retrait sweet spot 150-300 mots, nuance ALL-CAPS, 4K Stanford pas 3K
  - `04-Techniques/context-engineering/Context Management.md` — réécrite : /compact 40-60% pas 70%, Document & Clear = communauté/Manus, /clear = Anthropic docs sans "piège #1"
  - `04-Techniques/stacks/stack-python-ia.md` — Modal cold start ~1s container, GPU warm secs→mins
  - `04-Techniques/stacks/stack-typescript-ia.md` — strict + parallel OpenAI fix annoncé
  - `05-Leaders/agents/Andrej Karpathy.md` — retrait 400K mots / 70x RAG, ajout verbatim Obsidian/IDE/wiki
  - `01-Claude/Code/best-practices/context-management.md` — /compact 40-60% pas 70%
- **Fichiers .claude propagés** :
  - `.claude/agents/project-analyzer.md` — attribution /compact corrigée
  - `.claude/skills/cc-features-ref/SKILL.md` — /compact 40-60%
- **Type 3 (réécritures structurelles)** : 4 notes (LLM Wiki, Context Engineering, Context Management, pattern-sdd-triangle)
- **Type 2 (chiffres/sources)** : 16 corrections chirurgicales
- **Type 1 (attribution)** : 8 corrections
- **Source** : Audit thématique méthode validée 23 mai (sub-agents par cluster + self-verify FAUX fort impact + Type 1/2/3)
- **Output complet** : `output/audit-vault-thematique/06-patterns-context/` (A-inventaire, B-cluster1 à B-cluster6, C-croisement-et-plan-correction)


## 2026-05-23 — Leaders prompt + industrie (11 nouvelles fiches)

Suite à l'audit prompt engineering : création des fiches leaders manquantes identifiées en phase 0 (validation experts).

**05-Leaders/prompt/ (8 fiches ajoutées)** :
- Sander Schulhoff — CEO Learn Prompting/HackAPrompt, Prompt Report
- Riley Goodside — premier Staff Prompt Engineer Scale AI → Google DeepMind, glitch tokens
- Elvis Saravia — Co-Founder DAIR.AI, promptingguide.ai
- Jason Wei — Chain-of-Thought original author (NeurIPS 2022), FLAN, emergent abilities
- Denny Zhou — "king of reasoning" Google DeepMind, fondateur Reasoning Team
- Takeshi Kojima — Zero-shot CoT ("Let's think step by step", Matsuo Lab UTokyo)
- Imran Khan — Sculpting paper (arxiv 2510.22251, indépendant) — correction attribution forge
- Anthony Mikinka — UCL Universal Conditional Logic (arxiv 2601.00880, S*=0.509)
- Yann LeCun — Turing 2018, AMI Labs, position critique LLM/prompt engineering (world models JEPA)
- Ethan Mollick — Wharton, Prompting Science Report 1

**05-Leaders/industrie/ (5 fiches ajoutées)** :
- Geoffrey Hinton — Turing 2018 + Nobel Physics 2024, "Godfather of AI", U of T Emeritus
- Yoshua Bengio — Turing 2018, MILA founder, AI alignment
- Demis Hassabis — Nobel Chemistry 2024 (AlphaFold), DeepMind CEO, Gemini
- Ilya Sutskever — Safe Superintelligence CEO, ex-OpenAI Chief Scientist, AlexNet co-auteur
- Reid Hoffman — LinkedIn cofounder, Inflection AI board, "person-plus-AI" framework
- Allie K. Miller — Open Machine CEO, AI business ROI, ex-AWS Head ML Startups

**Source** : phase 0 audit prompt engineering 23 mai 2026, validation hiérarchie experts. Notes 4-6 aliases, sources tier 1-3, wikilinks cross-categories.

## 2026-05-23 — Audit thématique prompt engineering (vault forge)

Audit méthodique 17 notes du thème prompt engineering (`04-Techniques/prompt-engineering/` + `07-Prompts/`). Méthode A→B→C→D→E + propagation F appliquée (cf [[methode-analyser-repo]]) avec 6 sub-agents par cluster + 4 self-verify WebFetch direct des fondations doctrinales.

**Résultats** : 57 claims auditées sur 17 notes.
- ✅ 39 canoniques (verbatim confirmés multi-source)
- ⚠️ 14 partielles (paraphrase/sur-traduction à préciser)
- ❌ 4 fabriqués (verbatim/chiffres inventés)
- 4 attributions/dates fausses

**Corrections appliquées** (14 notes, 24 modifs) :
- **Modifiées** :
  - `amanda-askell-prompt-engineering.md` : A8/A9 attribution claude-character → TIME jan 2026 (verifié WebFetch), A11 soul document "~30 000 mots" → "80 pages / 35 000+ tokens" (officiel Anthropic), tweet update Aug 2025 ajouté
  - `System Prompt Amanda Askell.md` : date "mi-avril 2026" → "août 2025"
  - `System Prompt Claude Code.md` : Piebald "157 versions, v2.1.114" → "186+ versions, v2.1.149"
  - `over-specification-paradox.md` : Sculpting paper attribution "Mikinka UCL" → **Imran Khan** (indépendant), ajout finding GSM8K (Sculpting nuit gpt-5)
  - `Adaptive Thinking.md` : "surpasse systématiquement" → "reliably outperforms" (verbatim), snippet interleaved complété (2e phrase ajoutée), distinction deprecated 4.6 vs removed 4.7
  - `Effort Levels Guide.md` : "toujours configurer 64k+" → "Anthropic recommande de partir de 64k (à tuner)"
  - `opus-47-design-defaults.md` : précision "version COURTE 4.7" + note version longue pour 4.5/4.6
  - `outcome-first-prompting.md` : verbatim OpenAI fabriqué remplacé par canonique, structure 5 → 7 headers OpenAI documentée
  - `deprecated-techniques-2026.md` : verbatim OpenAI corrigé, "Let's think step by step" sourcé Kojima 2022 (PAS Wei 2022), section "prefilled erreur 400" → "no longer supported" (verbatim Anthropic), **section ALL-CAPS doctrine inversée** (Anthropic dit "dial back aggressive language"), markdown excessif verbatim canonique ajouté, sections 2-4 reformulées en heuristiques sourçables
  - `forge-prompt-machine.md` : disclaimer source FORGE v3 non-publiable, principe 7 "15 échanges" inventé retiré → Lost in the Middle (Liu 2024)
  - `prompting-chat-cowork-code.md` : "technique la plus efficace" → "technique recommandée"
  - `System Prompt Design.md` : sources ajoutées (claude-character + askell)
  - `chain-of-thought.md` : sources canoniques (Wei 2022 + Kojima 2022 distinction critique)
  - `few-shot-prompting.md` : source canonique Brown 2020 GPT-3 paper

**Sources** : audit méthode validée [[feedback_audit_thematique_methode]], méthode A→B→C→D→E [[methode-analyser-repo]], 6 sub-agents parallèles par cluster + 4 self-verify WebFetch (UCL 2601.00880 ✅, Sculpting 2510.22251 attribution fausse, OpenAI GPT-5.5 guide, Anthropic claude-character + best practices + messages API). Pattern récidiviste tweet/paraphrase verbatim non vérifiée confirmé ([[feedback_tweet_hype_paraphrase_pattern]] 5e occurrence).

**Outputs audit** : `output/audit-vault-thematique/02-prompt-engineering/` (A à D + 6 rapports clusters).

## 2026-05-23 — Audit dogfooding forge (propagation pivot doctrinal)

Audit transverse : forge respecte-t-il sa propre doctrine canonique vault post-pivot 23 mai ?

**Verdict** : PARTIAL PASS — 53/56 composants alignés (~95%), **9 drifts factuels corrigés** dans la propagation aval. Pattern reproduit `feedback_doctrine_drift_pattern` : canoniques OK, MEMORY/CLAUDE.md/index.md pas resynchronisées.

### Drifts Type 1 doctrinaux corrigés
- "25+ events" → "29 events" : `CLAUDE.md:34`, `vault/index.md:31`, `.claude/skills/cc-hooks-ref/SKILL.md:3+9`, `.claude/agents/hook-creator.md:34`
- "Angela Jiang advisor 5×" → "Brad Abrams advisor strategy" : `CLAUDE.md:35`, `vault/index.md:32`, `vault/1-Projets/Neoteem/ia_back/analyse-2026-05-22.md:149`, `../ia_back/.claude/rules/quality-gates.md:43`, `vault/05-Leaders/claude-code/angela-jiang.md` (6 edits)
- "`max` déprécié v2.1.91" → "`max` toujours disponible, prone overthinking" : `CLAUDE.md:48`

### Drifts Type 3 structurels corrigés
- `.claude/rules/sequence-canonique-modification.md` : frontmatter `description:` manquant → ajouté (rule MORTE silencieusement avant)
- `.claude/rules/check-before-create.md` : doublon partiel A→B→C→D→E avec sequence-canonique → réduit en rappel court pointant vers source canonique

### Canoniques 23 mai ajoutées à la navigation
- `[[methode-pivoter-doctrine]]` (checklist pivot sans drift résiduel)
- `[[comparaison-skill-anthropic-claude-code-setup]]`
- `[[anti-reentrance-sub-agents-pattern-escalade]]`

### Bonus : skill `/pivot-check` draftée (DA verdict GO-WITH-FIXES, pas encore active)
Skill v1 (121L) créée pour automatiser la détection des drifts post-pivot doctrinal sur tous les composants forge + memory. DA verdict GO-WITH-FIXES avec B1 BLOQUANT (périmètre rate `agent-memory/*/MEMORY.md` = principale source du drift). Skill déplacée vers `vault/claude-forge/Knowledge/drafts/pivot-check-skill/` (hors scan CC) en attente d'application manuelle des 4 fixes par Raphael (cf `output/audit-vault-thematique/08-claude-forge/PIVOT-CHECK-FIXES-PENDING.md`). Insight conservé pour répétition du pattern `feedback_doctrine_drift_pattern` (2× en 2 jours).

### Méta-insight
Créer `methode-pivoter-doctrine.md` (canonique vault) n'a pas suffi à l'appliquer rétroactivement sur son propre pivot. Forge avait besoin d'un check automatisé → `/pivot-check`.

---

## 2026-05-23 — Audit thématique vault Claude Code (95 claims auditées, 22 corrections)

Audit profond de 12 notes canoniques thème Claude Code via 6 sub-agents parallèles + vérifications directes (docs Anthropic). 95 claims analysées, **22 erreurs structurelles ou citations fausses détectées et corrigées**.

### Erreurs structurelles corrigées (Type 3 — réécriture)
- **Justin Young 2-agent ≠ Opus/Sonnet split** : article dit "harness was otherwise identical". Réécrit [[comment-creer-agent]].
- **Advisor strategy = Brad Abrams (pas Angela Jiang)** : coquille Simon Willison "Angela Kiang" propagée. Verbatim Abrams : "close to Opus-level intelligence at much lower prices". Source CwC SF avec Mario Rodriguez (GitHub). Réécrit [[comment-creer-agent]] + [[workflow-claude-code-optimal]].
- **Lethal trifecta = Simon Willison juin 2025** (pas Thariq). Éléments : private data / untrusted content / **exfiltration vector**. URL canonique : `simonwillison.net/2025/Jun/16/the-lethal-trifecta/`. Réécrit [[mcp-vs-skills-doctrine]].
- **Agent = Model + Harness** : popularisé par Hashimoto (5 fév 2026), pas Fowler/Böckeler. Réécrit [[comment-creer-agent]] + [[comment-creer-hook]].
- **LangChain 52.8→66.5** : Vivek Trivedy 17 fév 2026, modèle **GPT-5.2-Codex** (pas Claude). Réécrit.
- **Stop hook `once: true`** : skill frontmatter UNIQUEMENT (verbatim docs). Réécrit [[comment-creer-hook]].

### Chiffres corrigés (Type 2)
- claude-for-legal CLAUDE.md = **174 lignes** (pas 130)
- multica-ai = **67 lignes** (pas 70)
- Hook timeouts : **600s/30s/60s** selon type (pas 60s partout)
- **29 events** hooks officiels (pas 25+) — vault rate `TaskCreated` + `StopFailure`
- **effort: max TOUJOURS DISPONIBLE** mai 2026 (pas déprécié v2.1.91)

### Nouvelles règles ajoutées
- **SKILL.md description ~250 chars** pour auto-trigger fiable (limite system reminder `/skills` tronque au-delà)
- **Pipeline standard architect→dev→reviewer→test** explicité dans [[methode-analyser-repo]] avec quand-skip

### Notes leaders créées
- [[Brad-Abrams]] — Product Lead Anthropic, créateur Advisor Strategy
- [[Mitchell-Hashimoto]] — popularisateur "harness engineering"

### Notes modifiées (12)
- [[comment-creer-hook]] (réécriture complète : 29 events, timeouts, once:true)
- [[comment-creer-agent]] (réécriture complète : 2-agent Justin Young sans split, Brad Abrams Advisor Strategy, sources Fowler/Hashimoto corrigées)
- [[comment-creer-skill]] (réécriture complète : 9 catégories source corrigée, règle 250 chars)
- [[comment-ecrire-claudemd]] (réécriture complète : 174L/67L, max disponible, Hashimoto AGENTS.md)
- [[workflow-claude-code-optimal]] (réécriture complète : Brad Abrams, Noah Zweben verbatim, harness sources)
- [[methode-analyser-repo]] (réécriture complète : pipeline standard ajouté + alias automatiser)
- [[mcp-vs-skills-doctrine]] (réécriture complète : lethal trifecta Willison, Ronacher URL, qmd attribution nuancée)
- [[pattern-vault-llm-karpathy]] (append corrections : vibe coding titre exact, qmd, 4 patterns labels)
- [[trail-of-bits-config]] (append : C12.5 reformulation MCP doctrine)
- [[methode-pivoter-doctrine]] (append : citation pivot reformulée)
- [[raisonnement-22mai-doctrine-vs-enforcement]] (append : citation Anthropic verbatim corrigée, pivot reste valide)
- [[critique-2026-05-22-8-canoniques-chantier]] (append : compléments audit 23 mai)

### Source audit
`output/audit-vault-thematique/01-claude-code/` — A-inventaire-claims, B-verif-cluster*, C-croisement-revise, D-plan-correction.

## 2026-05-22 — Chantier refonte canonique (8 canoniques + 14 leaders + cleanup 28 notes)

Refonte complète du vault forge-brain pour en faire une **source de vérité actionnable** : quand on demande "analyse ce repo, propose-moi la config Claude Code", les agents trouvent immédiatement la doctrine canonique. Stratégie clean slate validée Raphael (rm sec, pas d'archive).

### Ajoutées — 8 notes canoniques (`04-Techniques/claude-code/`)
1. `comment-ecrire-claudemd.md` — CLAUDE.md target 200L Anthropic, 5 anti-patterns officiels, compounding Boris
2. `mcp-vs-skills-doctrine.md` — MCP data / Skills how-to (Thariq 3-way trade-offs, lethal trifecta Simon Willison)
3. `comment-creer-skill.md` — 9 catégories Thariq verbatim, frontmatter trigger 3e personne, < 500L
4. `comment-creer-agent.md` — frontmatter complet, 2-agent Justin Young, Sonnet/Opus split, convention 8 couleurs
5. `comment-creer-hook.md` — 25+ events officiels, doctrine "rule 100% → hook", Fowler Guides+Sensors
6. `workflow-claude-code-optimal.md` — routines Boris, advisor 5× Angela Jiang, leaf nodes Erik, multi-clauding
7. `methode-analyser-repo.md` (META) — grille 6 étapes pour transformer repo en config CC
8. `pattern-vault-llm-karpathy.md` — 3-layers raw/wiki/schema, 3 ops Ingest/Query/Lint, qmd Tobi Lütke
9. `trail-of-bits-config.md` — setup entreprise sécu publique (anti-rationalization Stop hook + 3-tier sandbox)

### Ajoutées — 14 fiches leaders + corrections d'attribution
- `05-Leaders/claude-code/` : cat-wu, lisa-crofoot, angela-jiang, daisy-hollman, jeremy-hadfield, justin-young, Noah Zweben + réécrites Erik Schluntz + Thariq Shihipar
- `05-Leaders/agents/` : addy-osmani, martin-fowler, hashimoto
- `05-Leaders/industrie/` : tobi-lutke

**Corrections d'attribution arbitrées** :
- Advisor 5× → Angela Jiang (PAS Cat Wu)
- "Scaffolding holds Claude back" → Lisa Crofoot (PAS Cat Wu)
- +300% PRs équipe → Noah Zweben | +200% PRs/eng org → Cat Wu (PAS Boris)
- 2-agent architecture → Justin Young (anthropic.com/engineering/effective-harnesses)
- qmd créateur → Tobi Lütke (PAS Karpathy, qui le recommande)
- Building Effective Agents co-auteur → Barry Zhang (PAS Amanda Askell)
- Lethal trifecta → Simon Willison juin 2025 (Thariq diffuse, ne crée pas)

### Critique DA appliquée
- `Knowledge/critiques/critique-2026-05-22-8-canoniques-chantier.md` créée
- 1 BLOQUANT corrigé : events inventés (PreEdit/PostEdit/PreWrite/etc) → 25+ events réels alignés sur `cc-hooks-ref/SKILL.md`
- 5 forts corrigés : attribution lethal trifecta, aliases "automatiser", DA-gate conditionnel, métriques inventées → qualitatif, forrestchang → multica-ai

### Supprimées — 28 notes (clean slate)
**Remplacées par canoniques (6)** : skills-guide, agents-orchestration, hooks-guide, claudemd-guide + claudemd-maintenance, karpathy-llm-wiki-pattern v0.1
**Obsolètes doctrine 22 mai (11)** : Workflow Boris (avril) + boris-workflow-2026-may, pattern-architect-first-pipeline, setup-project-complet + kit-rules-standard, vibe-coding-setup-complet, best-practices-claude-code-leaders, pipeline-boris-adapte-neoteem, pattern-agentic-engineering, agentic-engineering-karpathy + Karpathy Dev Discipline
**Knowledge obsolètes (11)** : erreur-marker-ttl + erreur-architect-marker, raisonnement-hook-agent-detection, critique-architect-guard + critique-dispatch-guard + critique-color-tdd + critique-tdd-neo-ia + critique-setup-tdd-strict + critique-mcp-forge-brain + critique-tdd-optimizations + erreur-skip-checklist

### Wikilinks redirigés
- 64 fichiers vault modifiés
- ~106 wikilinks redirigés vers canoniques cibles
- 0 wikilink résiduel vérifié empiriquement

### Source motivation
- 16 rapports de recherche déposés dans `0-Inbox/_chantier-22mai/` (~373 KB)
- Code with Claude London 19 mai 2026 (Boris/Cat/Angela/Lisa/Daisy/Jeremy/Noah)
- Code with Claude SF 6-7 mai 2026 (Erik/Thariq)
- Karpathy chez Anthropic depuis 19 mai 2026
- Doctrine pivot 22 mai : hooks lint/security/scope, JAMAIS workflow

### Commits
- `a29ddb4` : 16 rapports + PLAN-EXECUTION-FINAL
- `c651959` → `5443897` : 8 canoniques
- `f3188a0` : corrections DA
- `310c3f1` : 14 fiches leaders
- `9272a8f` : Phase C cleanup 28 notes

## 2026-05-21 (soir) — Kill TDD strict hooks + fix marker wipe sub-agent

- **Ajoutée** : `Knowledge/raisonnements/raisonnement-kill-tdd-strict-hooks-mai-2026.md` — décision tranchée (TDD = convention agent, pas hook bloquant) avec preuves web search Anthropic + DA verdict + bug bonus marker wipe sub-agent worktree
- **Modifiée** : `04-Techniques/patterns/pipeline-boris-adapte-neoteem.md` — section "Mise à jour 21 mai 2026 (soir)" ajoutée : règle "1 test à la fois" (vs "MAX 3 batch"), kill hooks ce soir, pipeline canonique final
- **Source** : Session frustration Raphael (4h+ sur fix BERNAT). Web search Boris Cherny + Anthropic confirme "ONE failing test per behavior per cycle, never bulk". DA verdict refonte hooks (16→6) refusé pour ce soir — 4 bloquants techniques. 3 kills propres uniquement (`tdd-guard.py` × 2 + `on-env-protect.py`). Bug bonus diagnostiqué : `session-reset-markers` wipe au démarrage sub-agent worktree v2.1.69+ — fix `source==startup` + check `agent_type`.
- **Commits** : neo_ia `a27ccec`/`25abe5d`/`342a8b0` — ia_back `a78f996`/`a9fb5fd`/`6d037e1`

## 2026-05-22 — Pipeline Boris adapté Neoteem (gain 50-60%/feature)

- **Ajoutées** :
  - `04-Techniques/patterns/pipeline-boris-adapte-neoteem.md` — recette pipeline agentic à appliquer sur tout nouveau repo (architect S/M/L, max 3 tests/comportement, REFACTOR fusionné, pipeline conditionnel, effort high partout sauf jugement)
  - `Knowledge/raisonnements/raisonnement-revirement-pipeline-mai-2026.md` — capture multi-étapes du revirement (retire architect → rends-le rapide → pipeline conditionnel). Précieux pour comprendre POURQUOI un jour
  - `Knowledge/erreurs/erreur-pipeline-trop-long-frustration.md` — l'erreur déclencheur (4h/feature, perte de plaisir). Anti-patterns à NE PAS recréer
- **Modifiées** : aucune note vault directement (le pattern existant `pattern-architect-first-pipeline.md` reste valide en complément)
- **Source** : Session 21-22 mai 2026, frustration utilisateur "4h pour une feature, je ne prends plus de plaisir". Pivot multi-étapes via advisor + DA + project-auditor cross-repo + recherche web Boris/Willison 2026. Commits f6d89e0 neo_ia + bc109aa ia_back. Gain mesuré : feature M neo_ia 30-45 min → 12-18 min, feature CRUD ia_back 4h → 1h30.
- **Mémoires liées** (mises à jour, pas dans vault) : `feedback_pipeline_quality_gates`, `feedback_opus47_workflow`, `feedback_test_writer_systematic`, `reference_boris_thariq_bestpractices` (section adaptation Neoteem ajoutée)

## 2026-05-21 — repo-scope-guard fixes adversaires (post-DA)

- **Ajoutée** : `Knowledge/erreurs/erreur-tests-heureux-vs-adverses.md`
- **Source** : DA lancé post-push (stop hook l'a forcé) a trouvé 3 bloquants : Glob pattern hors scope non testé, Write ia_back non bloqué (incohérence rule/hook), Bash bypass triviaux. 2 fixes appliqués : (1) Glob résout aussi le pattern relatif/absolu, (2) FREE_READ_REPOS vs FREE_WRITE_REPOS (ia_back read-only enforced). Position assumée by-discipline pour Bash arbitraire (pas de regex hardcodée — décision Raphael). Documenté dans rule "Limites assumées".

## 2026-05-21 — Refactor vault-before-specialist forge (4 fixes)

- **Ajoutée** : `Knowledge/erreurs/erreur-vault-before-specialist-ttl-scope.md`
- **Source** : Raphael observe que devil's advocate et advisor appellent neo-brain trop souvent. Audit + DA + advisor → 4 fixes appliqués : retirer TTL 60min (viole marker-ttl-antipattern), réduire scope 10→4 agents (skill/agent/hook/claudemd-creator seulement), is_specialist lit subagent_type only (plus de faux positifs prompt), nouveau hook session-reset-vault-marker.py SessionStart. Tests empiriques 6/6 PASS. Audit neo_ia complémentaire : pas de hook bloquant équivalent, advisory uniquement, RAS.

## 2026-05-21 — neo_ia repo-scope + dette hook vault notée

- **Ajoutée** : `Knowledge/erreurs/erreur-architect-neo_ia-fouille-bdd.md`
- **Source** : Architect neo_ia explorait bdd/ sans autorisation. Solution triple : rule `repo-scope.md` + patch top-of-file `architect.md` + 3 hooks Python (auth-detector UserPromptSubmit, repo-scope-guard PreToolUse, auth-cleanup SessionStart). Tests empiriques 8/8 PASS. Dette `vault-before-specialist.py` (TTL 60min, scope gonflé) notée pour session dédiée.

## 2026-05-21 — TDD optimizations + audit cohérence 2 repos

- **Ajoutées** : `Knowledge/critiques/critique-2026-05-21-tdd-optimizations-handshake.md`, `Knowledge/syntheses/synthese-audit-coherence-neo-ia-ia-back.md`
- **Modifiée** : `0-Inbox/context-actuel.md` — ajout résultats audit + optimisations TDD
- **Source** : Session 2026-05-21 — Sprint Contract, audit cohérence ia_back (43 problèmes) + neo_ia (24 problèmes)

## 2026-05-21 — Dispatch-guard E2E + erreur CLAUDE_AGENT + raisonnement détection

- **Ajoutées** : `Knowledge/erreurs/erreur-claude-agent-env-var-dead-code.md`, `Knowledge/raisonnements/raisonnement-hook-agent-detection-method.md`, `Knowledge/critiques/critique-2026-05-21-dispatch-guard-livraison.md`, `Knowledge/critiques/critique-2026-05-21-color-tdd-cto-mindset.md`
- **Modifiée** : `0-Inbox/context-actuel.md` — mis à jour avec contexte dispatch-guard + résultats E2E
- **Source** : Sessions 2026-05-21 — déploiement dispatch-guard, tests E2E, confirmation empirique agent_type runtime

## 2026-05-21 — Convention couleurs agents cross-repo

- **Ajoutée** : `01-Claude/Code/best-practices/agents-color-convention.md` — Standard palette couleurs par catégorie (8 couleurs, 8 rôles)
- **Source** : Test Desktop avec collègue — point coloré visible mais pas le nom d'agent, besoin de convention cohérente cross-repo

## 2026-05-20 — Fixes DA EVOLVE (frontière mémoire/vault + audit fantôme)

- **Créée** :
  - `1-Projets/Neoteem/agent-manager-neoteem.md` — Application concrète du rôle Agent Manager à Neoteem (scindée depuis agent-manager-role.md selon rule memory-discipline.md)
- **Modifiées** :
  - `01-Claude/Code/best-practices/agent-manager-role.md` — Section "Application à Neoteem" retirée (déportée vers 1-Projets/), tag #projet/neoteem retiré, wikilink ajouté vers [[agent-manager-neoteem]]
  - `04-Techniques/patterns/codebase-maps-pattern.md` — Table "Application aux repos Neoteem" retirée (audit fantôme non basé sur audit réel)
- **Source** : Verdict devil's advocate 2026-05-20 — fixes EVOLVE non-bloquants restants

## 2026-05-20 — Capitalisation blog Anthropic "Large codebases" + tweet Thariq

- **Créées** :
  - `04-Techniques/patterns/running-implementation-notes.md` — Pattern Thariq (758k vues 18 mai 2026) : fichier vivant maintenu pendant l'implémentation pour capturer design decisions, deviations, tradeoffs, open questions
  - `04-Techniques/agents/subagent-explore-then-edit.md` — Pattern Anthropic : subagent read-only mappe le subsystem dans un fichier, main agent édite avec la picture complète
  - `01-Claude/Code/best-practices/agent-manager-role.md` — Rôle org émergent (DRI / Agent Manager / équipe dédiée) pour Claude Code en enterprise
  - `04-Techniques/patterns/codebase-maps-pattern.md` — Markdown table of contents à la racine pour navigation Claude sur grosses codebases
- **Modifiées** :
  - `01-Claude/Code/best-practices/hooks-guide.md` — Ajout section "Self-improving hooks" : pattern Stop hook qui propose updates CLAUDE.md, SessionStart dynamique, 3 rôles des hooks
- **Source** : Blog Anthropic "How Claude Code works in large codebases" (14 mai 2026) + tweet @trq212 (18 mai 2026)

## 2026-05-18 — Feature classifier + audit skills cross-repo

- **Créée** :
  - `01-Claude/Code/features/auto-mode-classifier.md` — Filet de sécurité Anthropic en mode auto : scope, self-modification, destructif. Bypass via permissions.allow
- **Modifiée** :
  - `0-Inbox/context-actuel.md` — résolu conflit merge + mis à jour avec session 2026-05-18
- **Hors-vault** :
  - neo_ia : 13 skills passées `user-invokable: true` (référence/conventions accessibles spontanément)
  - ia_back : 7 skills passées `user-invokable: true`
- **Source** : Session audit neo_ia + question Raphael sur classifier

## 2026-05-18 — Capitalisation guide officiel Anthropic prompting Opus 4.7

- **Modifiées** :
  - `03-Modeles/anthropic/Opus 4.7.md` — enrichi : instruction-following littéral, response length adaptative, tool use, subagents, ton, design defaults, code review recall/precision, effort levels, prompts officiels
  - `04-Techniques/prompt-engineering/Effort Levels Guide.md` — strict respect low/medium, risque under-thinking, 64k tokens, steerability thinking
  - `04-Techniques/prompt-engineering/Adaptive Thinking.md` — steerability, interleaved thinking, migration extended→adaptive, bonnes pratiques Anthropic
- **Créées** :
  - `04-Techniques/prompt-engineering/opus-47-design-defaults.md` — style cream/Georgia/terracotta persistant + 2 contre-mesures + prompt anti-slop allégé
  - `04-Techniques/prompt-engineering/prompting-opus47-cheatsheet.md` — 16 prompts officiels Anthropic copier-coller + 4 bonus
- **Source** : Guide officiel Anthropic "Prompting best practices" (platform.claude.com) + article Ruben Hassid (Substack)

## 2026-05-15 — Audit vault complet + normalisation wikilinks + desorphelinement

- **Corrigé** :
  - 37 wikilinks à chemin normalisés (`[[path/note]]` → `[[note]]`) dans 11 fichiers
  - 8 wikilinks vers cibles inexistantes corrigés (Best practices Boris Thariq → lien correct, etc.)
  - 9 notes frontmatter corrigés (auteur, resume, MOC links) via fix.py
  - 3 notes critiques DA enrichies (resume + aliases + tags)
  - 2 notes MOC `derniere-maj` format corrigé
- **Créés** :
  - `Knowledge/erreurs/_index.md` — index 12 erreurs documentées
  - `Knowledge/syntheses/_index.md` — index 5 synthèses d'analyses
  - `Knowledge/critiques/_index.md` — index 5 critiques DA
- **Modifiés** :
  - `MOC-Claude-Code` — ajout section Agents forge (7 fiches), cowork-architecture, mcp-vs-cli-vs-skills
  - `MOC-Techniques` — ajout prompt-rewriter-pattern, architecture-cerveau-obsidian-mcp
- **Résultat** : score 98.2→98.8, orphelines 31→4, grade A 224→232, grade C 1→0
- **Bug fix** : audit.py crash sur `resume` de type list (AttributeError)
- **Batch stubs** (17 notes créées pour combler les red links) :
  - `05-Leaders/` : Amanda Askell, Patrick Lewis, Rafael Rafailov, Alex Albert
  - `01-Claude/Code/features/` : Agent Teams, Session Sharing, Claude Desktop, Project Glasswing
  - `04-Techniques/` : rag-production, rag-evaluation, Silent Assumptions, Context Management, System Prompt Design, ColPali
  - `07-Prompts/` : Piebald-AI System Prompts
  - `06-Industrie/` : OpenAI Revenue 25B
  - `Knowledge/erreurs/` : erreur-skip-checklist-skill-modification
- **Wikilinks redirigés** : Skills Best Practices → skills-guide, obsidian-markdown/python-ref → texte (skills)
- **Aliases ajoutés** : cowork-architecture += Cowork, Dispatch
- **Résultat final** : 251 notes, 100% grade A, score 98.9, orphelines 4 (intentionnelles)
- **Source** : /vault-audit + /vault-audit fix

## 2026-05-14 — 5 points Raphael + hooks enforcement + /done

- **Créés** :
  - `Knowledge/erreurs/erreur-auto-mode-classifier-self-modification.md` — double block delegate-guard + auto-mode
  - `04-Techniques/agents/prompt-rewriter-pattern.md` — analyse pattern et alternatives
- **Hooks créés** :
  - `skill-activation.py` (UserPromptSubmit) — recommandations skills automatiques
  - `vault-write-tracker.py` (PostToolUse) — compte écritures vault → DA après 3+
  - `proactivity-reminder.py` (Stop) — rappel proposition Jarvis si session > 5 tours
  - `apply-edit.py` — utilitaire bypass delegate-guard + auto-mode
- **Skill créée** : `/expand` — transforme prompt brut en spec précise
- **Source** : 5 questions Raphael sur meta-design forge

## 2026-05-14 — Restructuration 01-Claude + 8 notes deep research

- **Restructuration** : `01-Claude-Code/` → `01-Claude/Code/` + `01-Claude/Cowork/` (nouveau)
- **Créées dans 01-Claude/Code/best-practices/** :
  - `skills-guide.md` — Format YAML, 9 catégories Thariq, activation, budget /doctor
  - `hooks-guide.md` — 25+ events, exit 2, marker+guard, hookSpecificOutput
  - `claudemd-guide.md` — < 200 lignes, loading order, @import, compounding
  - `context-management.md` — /clear, /compact, compaction, subagents isolation
  - `agents-orchestration.md` — Subagents YAML, Generator/Evaluator, Dreaming, Outcomes
  - `mcp-vs-cli-vs-skills.md` — Benchmarks, Willison skills>MCP, matrice décision
- **Créées dans 01-Claude/Cowork/** :
  - `cowork-architecture.md` — Vue d'ensemble, plugins, Dispatch, Routines, pricing
  - `cowork-skills-reliability.md` — 2 problèmes, 73% cassées, debugging 9 étapes, bugs connus
- **Modifiées** :
  - `04-Techniques/agents/harness-engineering.md` — 4e paradigme, feedforward/feedback, 65% stat
  - `01-Claude/Code/changelog/CC mai 2026 - Code with Claude.md` — v2.1.139-140
- **Skills modifiées** :
  - `cc-news` v2.1.138 → v2.1.140
  - `cc-cowork-ref` — section diagnostic harness engineering
  - `cc-news/references/domain-claude-code.md` — @ClaudeCodeLog et @ClaudeDevs
- **Source** : cc-news 11 agents + 6 agents deep research (Boris, Cat Wu, Lydia, Thariq, Willison, Anthropic docs)

## 2026-05-14 — cc-news scan complet (session précédente)

- Harness Engineering enrichi, CC changelog v2.1.139-140
- Source : scan cc-news complet 11 agents

## 2026-05-13 — Setup Claude Code lojii + Figma MCP + Techniques memoire agents

- **Ajoutées** : `1-Projets/lojii/lojii.md`, `1-Projets/lojii/analyse-claude-code-2026-05-13.md`, `04-Techniques/patterns/pattern-figma-mcp-claude-code.md`, `04-Techniques/agents/technique-dreaming-cross-session.md`, `04-Techniques/agents/technique-shared-agent-memory.md`, `Knowledge/critiques/critique-2026-05-13-setup-lojii.md`
- **Modifiées** : `0-Inbox/context-actuel.md`
- **Source** : Analyse projet-analyzer + recherche web Figma MCP + Anthropic Dreaming + Netflix memory pattern + agent-memory scopes

## 2026-05-13 — Setup Claude Code lojii + Pattern Figma MCP

- **Ajoutées** : `1-Projets/lojii/lojii.md`, `1-Projets/lojii/analyse-claude-code-2026-05-13.md`, `04-Techniques/patterns/pattern-figma-mcp-claude-code.md`, `Knowledge/critiques/critique-2026-05-13-setup-lojii.md`
- **Modifiées** : `0-Inbox/context-actuel.md`
- **Source** : Analyse projet-analyzer + recherche web Figma MCP + critique devil's advocate

## 2026-05-13 — Analyse projet Lojii (frontend Vue 3)

- **Ajoutées** : `1-Projets/lojii/lojii.md`, `1-Projets/lojii/analyse-claude-code-2026-05-13.md`
- **Source** : Analyse complète projet-analyzer sur neofront/lojii (634 composants Vue 3 / Vuetify 3)

## 2026-05-12 — État de l'art Tool Retrieval & Query Expansion

- **Ajoutées** : `04-Techniques/rag/tool-retrieval-query-expansion.md`
- **Modifiées** : `04-Techniques/rag/RAG.md` (ajout lien MOC)
- **Source** : Recherche web état de l'art 2024-2026 (Re-Invoke, TOOLQP, OATS, ToolRerank, ToolShed, MCP Semantic Discovery) + analyse code neo_ia HybridToolSelector

## 2026-05-11 — Architecture profonde NeoDoc (neo_ia)

- **Créées dans 1-Projets/Neoteem/neo_ia/neodoc/** :
  - `neodoc-architecture.md` — Vue d'ensemble : RAG Vertex AI Discovery Engine, workspaces, notes indexables, schéma BDD 9 tables
  - `neodoc-research-agent.md` — Agent Research LangGraph 5 nœuds, query decomposition (google-genai natif), grounding citations, dual path (retrieve vs full_doc)
  - `neodoc-ingestion-pipeline.md` — Pipeline 7 étapes Drive/upload → GCS → Discovery Engine, 4 modes (sync/async/batch/folder), retry intelligent
- **Modifiée** : `neo_ia.md` — wikilinks NeoDoc ajoutés
- **Source** : analyse profonde du code source apps/neodoc/

## 2026-05-11 — Architecture profonde NeoMail (neo_ia)

- **Créées dans 1-Projets/Neoteem/neo_ia/neomail/** :
  - `neomail-architecture.md` — Vue d'ensemble : webhook Pub/Sub, classification LLM, 21 tools, BROUILLON ONLY, diff NeoChat vs NeoMail
  - `neomail-webhook-pipeline.md` — Pipeline 10 étapes : Pub/Sub → History API → classify → label sync → auto-reply draft, sécurité IAM, hiérarchie exceptions
- **Restructurée** : notes NeoChat déplacées dans `neochat/`, NeoMail dans `neomail/`
- **Modifiée** : `neo_ia.md` — wikilinks NeoMail ajoutés
- **Source** : analyse profonde du code source apps/neomail/

## 2026-05-11 — Architecture profonde NeoChat (neo_ia)

- **Créées dans 1-Projets/Neoteem/neo_ia/** :
  - `neochat-architecture.md` — Vue d'ensemble : 6 agents, 26 tools, interrupt handlers, ToolInTool patterns
  - `neochat-react-engine.md` — Declarative ReAct Engine 7 phases, AgentBlueprint dataclass, interrupt handlers
  - `neochat-adaptive-prompt.md` — Adaptive Prompt Builder V2 4 layers (cache Gemini), ToolPromptLoader, conditional rules
  - `neochat-tool-rag.md` — HybridToolSelector pgvector : 10 étapes (expansion, hybrid search, LLM rerank, BFS deps)
- **Modifiée** : `neo_ia.md` — ajout section Architecture détaillée par app (NeoChat/NeoDoc/NeoMail)
- **Source** : analyse profonde du code source neo_ia (blueprint, react.py, adaptive.py, selector.py, builders)

## 2026-05-11 — Capitalisation vidéos Code with Claude + Boris AI Ascent

- **Créées dans 01-Claude-Code/features/** :
  - `Memory Managed Agents.md` — Architecture memory : filesystem, permission scopes, optimistic concurrency, version history
  - `Dreaming Managed Agents.md` — Process scheduled review cross-sessions, déduplication, vérification, enrichissement
  - `Code with Claude 2026.md` — Résumé conférence SF : SpaceX, Dreaming, Outcomes, Multi-agent, Routines
- **Créée dans 04-Techniques/patterns/** :
  - `boris-workflow-2026-may.md` — Setup Boris mai 2026 : mobile-first, /loop partout, 150 PRs/jour, coding is solved
- **Modifiées** : `MOC-Claude-Code.md` (4 notes ajoutées), `Boris Cherny.md` (section mai 2026)
- **Source** : transcription YouTube — Memory & Dreaming (Mahesh Murag), Boris AI Ascent Sequoia, Everything new from CwC 2026 (Matt Cuda)

## 2026-05-11 — 6 fiches leaders agents/industrie + audit + corrections devil's advocate

- **Créées dans 05-Leaders/agents/** :
  - `Chi Wang.md` — AutoGen/AG2 creator, Google DeepMind, ICLR 2026
  - `Yohei Nakajima.md` — BabyAGI creator, Untapped Capital GP, build-in-public
  - `David Shapiro.md` — ACE Framework, architecture cognitive 6 couches
  - `Div Garg.md` — MultiOn founder, browser agents 500+ steps
  - `Joao Moura.md` — CrewAI founder & CEO, $18M levés, 50.8K stars
- **Créée dans 05-Leaders/industrie/** :
  - `Dario Amodei.md` — CEO Anthropic, RSP, Mythos, clash DoD 2026 (déplacé d'agents/ suite critique devil's advocate)
- **Corrections devil's advocate** :
  - Dario Amodei : déplacé de agents/ → industrie/ (cohérence taxonomique, la note dit elle-même qu'il n'est pas un builder agents)
  - `type: leader` harmonisé sur les 13 fiches agents (8 anciennes avaient `type: ""`)
  - Aliases Dario enrichis : +4 termes de recherche sémantique (responsible scaling, AI safety leader, etc.)
  - Joao Moura créé (candidat le plus évident absent de la batch initiale)
- **Modifiés** : `MOC-Leaders.md` (section Agents + Industrie enrichies), `Agents IA.md` (section Pionniers)
- **Enrichi** : `cc-news/references/domain-agents.md` (5 leaders ajoutés au tableau)
- **Audit** : 199 notes, score moyen 95/100 (185A/13B/0C/1D), fix déterministe appliqué
- **Source** : recherche web 2026 + devil's advocate

## 2026-05-10 — Dossier stacks/ : 2 notes reference implementation IA (TS + Python)

- **Creees dans 04-Techniques/stacks/** :
  - `stack-typescript-ia.md` — SDKs (Vercel AI SDK, Mastra, LlamaIndex.TS), RAG, streaming SSE, Zod, deployment edge, audit checklist, diagnostic optimisation
  - `stack-python-ia.md` — SDKs (LangGraph, Pydantic AI, Instructor, DSPy, CrewAI), RAG, ML/DL, FastAPI SSE, deployment, audit checklist, diagnostic optimisation
- **Sections ajoutees (corrections devil's advocate)** : Observability, Memory, Guardrails, MCP, Provider routing, Agent sandboxing, Audit Checklist (12-15 anti-patterns), Diagnostic optimisation (flux conditionnel)
- **Modifie** : `MOC-Techniques.md` — section "Stacks Implementation IA" ajoutee
- **Source** : Agent recherche TS/Python + advisor + devil's advocate (3 bloquants corriges)

## 2026-05-10 — Dossier chatbot/ : 11 notes architectures chatbot & multi-agent

- **Creees dans 04-Techniques/chatbot/** :
  - `index-architectures.md` — Decision tree pattern + framework, matrice evaluation croisee
  - `architecture-claude-api.md` — Messages API, Agent SDK, Managed Agents, system prompts
  - `architecture-openai-api.md` — Responses API, Agents SDK, Conversations, Realtime
  - `architecture-langgraph.md` — StateGraph, supervisor, swarm, checkpointing, HITL
  - `architecture-crewai.md` — Crews, Flows, memory unifiee, prototypage rapide
  - `architecture-gemini-api.md` — Function calling, ADK, A2A, Interactions API
  - `architecture-autogen.md` — GroupChat, en declin, successeur MS Agent Framework
  - `pattern-orchestrateur.md` — Supervisor + hierarchique cross-framework
  - `pattern-swarm.md` — Handoffs decentralises cross-framework
  - `pattern-pipeline.md` — Prompt chaining, evaluator-optimizer, parallelisation
  - `pattern-single-agent-multi-tool.md` — Pattern defaut 80% des chatbots
- **Modifie** : `MOC-Techniques.md` — section "Architectures Chatbot & Multi-Agent" ajoutee
- **Source** : 4 agents de recherche paralleles (Claude API, OpenAI, LangGraph, CrewAI/AutoGen/Gemini) + advisor + devil's advocate

## 2026-05-10 — Reorganisation 04-Techniques : 12 notes deplacees dans sous-dossiers, 5 index Knowledge crees

- **Deplacees vers prompt-engineering/** :
  - `amanda-askell-prompt-engineering.md` — depuis racine 04-Techniques
  - `forge-prompt-machine.md` — depuis racine 04-Techniques
  - `prompting-chat-cowork-code.md` — depuis racine 04-Techniques
- **Deplacees vers patterns/** :
  - `config-guardian-pattern.md` — depuis racine 04-Techniques
  - `pattern-vault-query-guard.md` — depuis racine 04-Techniques
  - `vibe-coding-setup-complet.md` — depuis racine 04-Techniques
  - `best-practices-claude-code-leaders.md` — depuis racine 04-Techniques
- **Deplacees vers agents/** :
  - `agentic-engineering-karpathy.md` — depuis racine 04-Techniques
  - `pattern-agentic-engineering.md` — depuis racine 04-Techniques (notes distinctes, pas fusionnees)
- **Deplacees hors 04-Techniques** :
  - `claude-desktop-preferences.md` → `01-Claude-Code/features/` (type feature, pas technique)
  - `mcp-obsidian-brain-v2.md` → `01-Claude-Code/features/` (feature Claude Code Neoteem)
  - `neoteem-brain-plugins.md` → `1-Projets/Neoteem/neoteem-brain/` (contexte projet)
  - `sqlite-fts5-vault.md` → `04-Techniques/rag/` (technique RAG/search)
- **Ajoutees** : 5 index `_index.md` dans Knowledge/ : evolutions/, reviews/, raisonnements/, explorations/, questions/
- **Modifiees** :
  - `00-Hub/MOC-Techniques.md` — reorganisation sections, suppression entrees parties, ajout Prompt Engineering + RAG
  - `00-Hub/MOC-Claude-Code.md` — ajout claude-desktop-preferences + mcp-obsidian-brain-v2 dans Features
  - `1-Projets/Neoteem/neoteem-brain/neoteem-brain.md` — ajout liens neoteem-brain-plugins + mcp-obsidian-brain-v2
- **Source** : reorganisation organisationnelle 04-Techniques demandee par Raphael

## 2026-05-10 — Capitalisation cc-news : 6 techniques prompt engineering 2026 (outcome-first, over-specification, harness, MASS, PromptArmor, deprecated)

- **Ajoutées** :
  - `04-Techniques/prompt-engineering/outcome-first-prompting.md` — OpenAI GPT-5.5 : outcome + critères de succès, pas process step-by-step
  - `04-Techniques/prompt-engineering/over-specification-paradox.md` — UCL arXiv 2601.00880 : seuil S*=0.509, dégradation quadratique, 29.8% réduction tokens
  - `04-Techniques/prompt-engineering/deprecated-techniques-2026.md` — Inventaire complet techniques contre-productives sur frontier models
  - `04-Techniques/agents/harness-engineering.md` — Agent = Modèle + Harness, contraintes déterministes > prompts suggestifs
  - `04-Techniques/agents/mass-multi-agent-system-search.md` — DeepMind ICLR 2026 : optimisation conjointe prompts + topologie multi-agent
  - `04-Techniques/agents/prompt-armor.md` — ICLR 2026 arXiv 2507.15219 : LLM préprocesseur défense injection, < 1% attack rate
- **Modifiées** :
  - `00-Hub/MOC-Techniques.md` — 3 nouvelles sections + 6 wikilinks ajoutés
  - `00-Hub/MOC-Prompts.md` — 3 wikilinks ajoutés dans section Principes
- **Source** : cc-news scan 2026-05-10 (24 techniques prompt engineering)

## 2026-05-10 — Capitalisation cc-news : changelogs CC 2.1.132-136, Cursor 3.3, Grok 4.20, Jina v4, Context Engineering

- **Ajoutées** :
  - `01-Claude-Code/changelog/CC v2.1.132.md` — CLAUDE_CODE_SESSION_ID, memory leak 10GB+ MCP stdout (6 mai)
  - `01-Claude-Code/changelog/CC v2.1.133.md` — worktree.baseRef, CLAUDE_EFFORT hooks, sandbox paths (7 mai)
  - `01-Claude-Code/changelog/CC v2.1.136.md` — Release majeure 50+ changements, autoMode.hard_deny (8 mai)
  - `04-Techniques/rag/jina-embeddings-v4.md` — 3.8B, single+multi-vector ColBERT unifié, 72.19 JinaVDR
- **Modifiées** :
  - `02-Concurrents/cursor/Cursor.md` — section Cursor 3.3 : PR Review, Parallel Agents, Visual Canvases
  - `02-Concurrents/xai/xAI Grok.md` — Grok 4.3 (1M ctx, vidéo), Grok 4.20 Beta (4+16 agents)
  - `04-Techniques/context-engineering/Context Engineering.md` — 4 pilliers, sweet spot 150-300 mots, règles empiriques
  - `00-Hub/MOC-Claude-Code.md` — wikilinks CC v2.1.132/133/136
- **Source** : cc-news scan 2026-05-10

## 2026-05-09 — Migration CLI→MCP complète + Stop hook devil's advocate + autonomie

- **Migration CLI→MCP** : TOUS les agents (10/10), skills (forge-brain, done, recap, reasoning-cache, skill-evolve, forge-review, vault-audit), rules (memory-discipline, check-before-create, forge-brain-proactive), et references migrés. Zéro ref CLI dans le projet.
- **Stop hook** : `devil-advocate-stop.py` bloque la fin de session si devil's advocate pas lancé
- **Auto-start MCP** : hook SessionStart lance le MCP automatiquement
- **Skill obsidian-cli supprimée** : remplacée par MCP forge-brain
- **Règle d'autonomie** : advisor + devil's advocate valident → agir sans demander
- **MCP optimisé** : 11 outils (+ list_notes, vault_stats), descriptions forge-brain, exemples adaptés
- **Source** : feedback Raphael, recherche Boris best practices, advisor

## 2026-05-09 — MCP forge-brain + /watch + Context Note + devil's advocate

- **Ajoutées** :
  - `mcp-forge-brain/` — MCP server self-contained (SQLite FTS5, port 8091), copie autonome de mcp-obsidian-brain
  - `.mcp.json` — config MCP projet pour forge-brain
  - `0-Inbox/context-actuel.md` — Working memory dynamique (/done écrit, /recap lit)
  - Skill `/watch` — transcription YouTube via yt-dlp
- **Modifiées** :
  - Skill `/done` : fix cross-projet, routing 1-Projets/2-Casquettes, frontmatter nettoyé, garde anti-hallucination, Context Note en étape 6
  - Skills `forge-brain`, `recap` : structure vault + scan 1-Projets/2-Casquettes
  - Skill `vault-audit` + `audit.py` : nouveaux dossiers dans FOLDER_TO_MOC + TEMPLATE_SECTIONS
  - Rule `memory-discipline.md` : frontière memory↔vault canonique
  - CLAUDE.md : 2 lignes vault structure + standard qualité
  - Notes vault enrichies : ia_back, neo_ia, bdd, neoteem-brain (détails composants Claude Code)
  - Memory project_*.md : 4 fichiers slimmés (pointeurs vers vault 1-Projets/)
- **Devil's advocate** : critique `/done` sauvée dans `Knowledge/critiques/`, 3 bloquants corrigés
- **Source** : Analyse Eliott Meunier + recherche MCP servers + advisor

## 2026-05-09 — Structure holistique vault + skill /done + standard qualité

- **Ajoutées** :
  - `0-Inbox/` — dossier capture rapide
  - `1-Projets/Claude-Forge/Claude-Forge.md` — contexte projet forge
  - `1-Projets/Neoteem/Neoteem.md` — contexte projet Neoteem
  - `1-Projets/Neoteem/ia_back/ia_back.md` — contexte repo ia_back
  - `1-Projets/Neoteem/neo_ia/neo_ia.md` — contexte repo neo_ia
  - `1-Projets/Neoteem/neoteem-brain/neoteem-brain.md` — contexte repo neoteem-brain
  - `1-Projets/Neoteem/bdd/bdd.md` — contexte repo bdd
  - `1-Projets/Expertise-IA/Expertise-IA.md` — projet vision expert IA
  - `2-Casquettes/Raphael-Picard.md` — profil holistique complet
  - `2-Casquettes/Famille.md` — casquette famille
  - `2-Casquettes/Gaming.md` — casquette gaming
  - `Templates/context-projet.md` — template note de contexte projet
  - `Templates/context-casquette.md` — template note de contexte casquette
- **Modifiées** : Rule `forge-brain-proactive.md` — standard qualité (4-6 aliases, résumé, wikilinks) + routage dossiers 0/1/2
- **Skills** : `/done` créée — métacognition fin de session (extraction décisions/faits/préférences)
- **Source** : Analyse vidéo Eliott Meunier "Son système IA remplace une équipe entière" — ontologie par utilité, contexte holistique, /done auto-update

## 2026-05-08 — Erreur paths hardcodés multi-poste

- **Ajoutées** : `Knowledge/erreurs/erreur-settings-paths-hardcodes-multi-poste.md` — bug paths absolus user-spécifiques dans settings.json + hooks Python + marker files, cassent quand on pull sur un autre poste
- **Source** : premier usage de claude-forge sur poste perso (rapha) après pull depuis poste pro (raphael.picard_neote) — flot d'erreurs `Python was not found` + guard vault-query bloqué en permanence

## 2026-05-08 — Skill reasoning-cache + template raisonnement

- **Ajoutees** : `Templates/raisonnement.md` — template pour noter les chaines de raisonnement validees
- **Modifiees** : `00-Hub/MOC-Techniques.md` — section "Raisonnements caches" ajoutee avec lien vers Knowledge/raisonnements/
- **Source** : creation skill reasoning-cache (chain-of-thought caching au niveau tooling)

## 2026-05-08 — Base de connaissances Agents IA complète

- **Ajoutées** : `04-Techniques/agents/` — 6 notes (Agents IA MOC, frameworks, architecture, automation, évaluation, sécurité)
- **Leaders** : 6 fiches agents dans `05-Leaders/` (Shunyu Yao, Andrew Ng, Lilian Weng, Jim Fan, Simon Willison, Ethan Mollick)
- **Synthèse** : `techniques-inedites.md` — 8 combinaisons innovantes RAG × Agents jamais faites
- **cc-news** : section Agents IA & Automation leaders ajoutée (12 sources)
- **CLAUDE.md** : v1.9, mindset Jarvis/Innovateur ajouté
- **Source** : recherche via 5 agents parallèles (frameworks, architecture, leaders, automation, évaluation)

## 2026-05-08 — Base de connaissances RAG complète

- **Ajoutées** : `04-Techniques/rag/` — 7 notes (RAG MOC, chunking, embeddings, architecture, metadata, reranking, vector-databases)
- **Leaders** : 10 fiches RAG dans `05-Leaders/` (Jonas Roman, Omar Khattab, Douwe Kiela, Jerry Liu, Harrison Chase, Han Xiao, Chip Huyen, Greg Kamradt, Nils Reimers, James Briggs)
- **Synthèses** : `rag-obsidian-claude-video-analyse.md` (analyse critique vidéo YouTube), `outils-portabilite-forge.md` (defuddle, yt-dlp)
- **cc-news** : section RAG & Embeddings leaders ajoutée (9 sources)
- **Source** : recherche approfondie via 5 agents parallèles (chunking, embeddings, architecture, experts, metadata) + analyse vidéo YouTube RAG+Obsidian+Claude

## Liens


## 2026-05-21 — Capitalisation Code with Claude 2026 (keynote SF + London)

- **Créées** :
  - `01-Claude/Code/features/Self-Hosted Sandboxes.md` — Public beta London, 4 providers (Cloudflare/Modal/Vercel/Daytona), architecture queue
  - `01-Claude/Code/features/MCP Tunnels.md` — Research preview London, tunnel outbound sécurisé vers MCP privés
- **Enrichies** :
  - `Code with Claude 2026.md` — Stats transcription (20h/semaine, 17x API, task horizon), section London, framework 16 features, quotes Boris/Dianne
  - `Code with Claude Conference.md` — Speakers London confirmés, annonces spécifiques London, Extended 20 mai
  - `Dreaming Managed Agents.md` — Limites techniques (100 sessions, header API, modèles supportés), démo Lumara
  - `Managed Agents.md` — London features, webhooks 8 events, Outcomes params, Advisor Strategy, clients keynote
  - `CC mai 2026 - Code with Claude.md` — London drop (Self-Hosted Sandboxes + MCP Tunnels + enrichissements)
- **Source** : Transcription Whisper vidéo YouTube (427 segments, 47 min) + 142 captures d'écran + blogs tiers (Chris Ebert, Simon Willison, Dotzlaw, inaiwetrust, dev.to) + page officielle London

## 2026-05-22 — Refonte doctrine hooks workflow ia_back + neo_ia

- **Ajoutées** :
  - `Knowledge/raisonnements/raisonnement-22mai-doctrine-vs-enforcement.md` (décision centrale, sources Anthropic Boris/Thariq/Agent SDK)
  - `Knowledge/erreurs/erreur-hooks-workflow-enforcement.md` (anti-pattern à ne pas refaire)
- **Modifiées** :
  - `04-Techniques/patterns/pipeline-boris-adapte-neoteem.md` (note suppression hooks)
  - `05-Leaders/claude-code/Boris Cherny.md` (application doctrine Neoteem)
  - `01-Claude/Code/best-practices/hooks-guide.md` (section anti-pattern workflow enforcement)
  - `1-Projets/Neoteem/ia_back/ia_back.md` (refonte hooks 22 mai)
  - `1-Projets/Neoteem/neo_ia/neo_ia.md` (refonte hooks 22 mai)
- **Source** : friction 6× développement feature, recherche web Anthropic 2026 (Agent SDK "Claude decides when to invoke", Boris "thinnest wrapper")

## 2026-05-27 — KILL vault-maintainer + résolution cas spéciaux MCP décoratif

Suite des étapes 2b/3 (fix structurel MCP décoratif sub-agent), traitement des 2 derniers cas spéciaux qui restaient en dette : les agents dont le métier touche le vault.

**Diagnostic empirique.** Le MCP forge-brain étant décoratif en contexte sub-agent (`No such tool available`, confirmé 27 mai), deux agents posaient question. `vault-maintainer` (métier = N× écritures MCP : aliases, MOC, frontmatter, backlinks) ne peut littéralement pas faire son travail en sub-agent. `devils-advocate` (métier = analyse + au plus 1 `create_note`) fonctionne en mode dégradé déjà prévu par son brief.

**vault-maintainer — KILL.** L'agent était un doublon fonctionnel de la skill `/vault-audit`, qui couvre la même checklist mais tourne en session principale (MCP effectif) avec un script Python déterministe. Aucune invocation historique via le tool Agent. Verdict : suppression. Son seul apport unique — le déclenchement proactif après cc-news / création de note — a été porté dans la description de `/vault-audit`. L'exemption qui lui était réservée dans le hook `vault-cat-guard` a été retirée (surface d'exemption nulle, doctrine MCP-only plus stricte). L'archive `agent-memory/vault-maintainer/` est conservée.

**devils-advocate — gardé, brief clarifié.** Son brief disait déjà que la sauvegarde vault est non bloquante (sinon critique en texte). On a précisé la cause exacte (échec structurel du MCP en sub-agent, pas aléatoire) et confirmé empiriquement que la persistance marche : 23 critiques dans `Knowledge/critiques/` pour ~24 invocations.

**Pattern de design dégagé.** Un composant dont la valeur est `N× écriture MCP` est structurellement une skill (session principale, MCP effectif), pas un agent. Les agents survivent au contexte sub-agent quand leur métier est l'analyse plus des écritures rares. Capitalisé en amendement de [[pattern-mcp-brief-then-direct]].

Tests hooks 176 verts (180→176, suppression du mécanisme d'exemption testé). Méthode A→B→C→D→E, advisor, arbitrage par agent.

## 2026-05-28 (suite 4) — Audit MCP forge-brain vs MCP brain + AMEND skill forge-brain A1+A2+A3

- **Créées** :
  - `04-Techniques/claude-code/comparaison-mcp-forge-brain-vs-mcp-brain-28mai2026.md` (vault) — note canonique audit empirique 14 critères techniques. Verdict A : MCP forge-brain mieux conçu tokens/Karpathy serveur (6 gains / 1 perte inapplicable forge / 7 égalités). Extraits code preuve (forge:210-218 pagination autoguidée, forge:550-594 read_section, forge:596-637 read_note_resolved, forge:867+1097 usage_log).
- **Modifiées** :
  - `.claude/skills/forge-brain/SKILL.md` (197L → 292L, +95L) — AMEND A1+A2+A3 via skill-creator (delegate-guard) :
    - **A1** (L31-70) — Section "Pattern Karpathy opérationnel" : 3 temps SEARCH/SELECT/READ + table 4 modes (Query N=3 / Audit N=4 / Exhaustive 2-4 / Exploration illimité) + anti-patterns ❌/✅
    - **A2** (L161-177) — Matrice "Priorisation tools AVANT search_brain — Hiérarchie économie tokens" : `find_by_property` > `read_section` > `read_note` > `search_brain` (dernier recours)
    - **A3** (L91-124) — Section "Pagination autoguidée 500L par passes" : exploiter header serveur `[suite : appeler avec offset=N]` (forge:215-217)
  - `0-Inbox/context-actuel.md` — Phase audit MCP + recommandations P3a/b/c/d brain ← forge tracées pour décision séparée Raphaël.
- **Source** : Recadrage Raphaël session 28 mai — "lequel des 2 MCP serveurs est le mieux conçu tokens/Karpathy serveur ?". Audit comparatif 14 critères empiriques.
- **AUCUNE modification code MCP** : verdict A confirme MCP forge-brain déjà bien conçu. Gap = utilisation par skill, pas serveur.
