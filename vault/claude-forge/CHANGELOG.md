---
titre: "Changelog vault forge-brain"
resume: "Historique des ajouts et modifications du vault forge-brain"
aliases:
  - changelog vault
  - historique vault
  - changelog forge-brain
  - historique notes vault
type: index
derniere-maj: 2026-07-27
auteur: claude
tags:
  - "#type/index"
  - "#domaine/claude-code"
---

## 2026-07-27 (4) — sweep anti-drift post-pivots (pivot-check sur les 9 pivots du jour)

- **Modifiées** : `index.md` + `00-Hub/Home` + `00-Hub/MOC-Claude-Code` (29→30 events, changelogs juillet ajoutés, gloss workflows/research-preview corrigé, How we contain Claude + steps-of-ai-adoption + fireside référencés) ; `00-Hub/MOC-Industrie` (retrait mythos-preview, graph-engineering-buzz) ; `01-Claude/models/claude-mythos-preview` (bannière RETIRÉ 21 juil.) ; `04-Techniques/claude-code/architecture-claude-folder` (gotcha nesting → depth 3, dossier workflows/ ajouté à la structure) ; `04-Techniques/agents/limites-subagents-claude-code` (AJOUT depth 3 + caps v2.1.217-219) ; `effort-opus-47-doctrine` (borne temporelle « xhigh = default » = ère 4.7, high depuis 4.8)
- **Source** : demande Raphael « regarde toutes les notes du vault à mettre à jour » → /pivot-check sur les 9 pivots du 27 juil. (Opus 5, mythos-preview retiré, fast mode 4.7, nesting depth 3, effort reviewers, 30 events, workflows nommés, date cc-news, MCP RC). Côté repo : cc-features-ref (Opus 5 + date réf. 25 juil.), subagent-creator (2 claims nesting), craft-prompt ref, hook-creator (30 events), pivot-check (exclusion .agents/+AGENTS.md = miroir ChatGPT, décision Raphael), CLAUDE.md l.53, memory feedback_major_mistakes #1 amendé + reference_agents_dir_chatgpt_mirror créée
- **Exclusions respectées** : CHANGELOG, log, Knowledge/erreurs|critiques|tests, notes changelog datées, fiches leaders (historique)

## 2026-07-27 (3) — chantier audit règles forge : correction drift tableau effort (catch DA)

- **Modifiées** : `04-Techniques/claude-code/effort-opus-47-doctrine-anthropic-2026` — cellules « Reviewers/devils-advocate → xhigh » corrigées → **high** (drift vs décision Option C du 18 juin, détecté par le devils-advocate qui a refusé son propre bump ; l'audit s'appuyait sur la cellule outlier) + callout de correction daté
- **Leaders** : critique DA sauvegardée par l'agent : `Knowledge/critiques/critique-2026-07-27-plan-audit-regles-forge.md`
- **Source** : chantier audit `.claude/` forge (repo-inspector lentille frontière + 3 tripartites → devils-advocate PASS-avec-réserves, 1 BLOQUANT inversé → arbitrage Raphael 4 questions). Côté repo : code-dev TDD reformulé 100 %-accurate, dédup comportement-proactif, descriptions codex-ref/rag-design < 250, CLAUDE.md S2/S4, settings.json.proposed (retrait hook fantôme notify-discord)

## 2026-07-27 (2) — analyse approfondie : interviews équipe CC + deep-dive graph engineering

- **Ajoutées** : `04-Techniques/claude-code/steps-of-ai-adoption-boris` (framework 0-4 Boris 16 juil., source primaire X retrouvée — les blogs tiers disaient anthropic.com, faux) ; `04-Techniques/claude-code/fireside-cat-wu-thariq-aiewf-2026` (Willison 21 juil. : system prompt −80 %, fewer constraints/tools, Claude prompting Claude all the way down, auto mode quasi universel, mémoire Tag = markdown/canal) ; `01-Claude/Code/features/How we contain Claude` (article 28 mai manquant au vault — 93 % approbation, sandbox −84 % prompts, deterministic boundary)
- **Modifiées** : `06-Industrie/graph-engineering-buzz` (analyse de fond : fausse attribution « ingénieur Anthropic » → Andrew Ng non vérifié, doctrine loop-d'abord/graphe-si-séparable, benchmarks knowledge graph, heuristique entity resolution pro-wikilinks) ; `effort-opus-47-doctrine-anthropic-2026` (post officiel Lydia Hallie 7 juil. : try-vs-know, REINFORCE allocation forge) ; `workflow-claude-code-optimal` + `concevoir-loops-travail` (AMENDE claim périmée nesting + addenda) ; `mcp-vs-skills-doctrine` (fewer tools + hooks coût contexte nul, crédit MOYEN Daisy) ; `comment-ecrire-claudemd` (doctrine prompting frontière) ; `Opus 5` (claims sécu Boris launch)
- **Leaders** : Boris Cherny (Odd Lots « It's almost entirely the model », série 15-24 juil.), Lydia Hallie (post effort×modèle), cat-wu + Thariq Shihipar (fireside), daisy-hollman (talk NDC 3 juin, VOD à surveiller)
- **Source** : run cc-news approfondi 27 juil. (4 agents : deep-dive graph engineering, fireside Willison, source primaire Steps of AI Adoption via x-read, balayage équipe 1-27 juil.)

## 2026-07-27 — cc-news 16-27 juillet : Opus 5, CC v2.1.212-220, buzz Graph Engineering, RC MCP détaillée

- **Ajoutées** : `01-Claude/models/Opus 5` (lancé 24 juil., $5/$25, 1M ctx, thinking ON, défaut Opus CC + Claude Max) ; `01-Claude/Code/changelog/CC juillet 2026 - Opus 5 + v2.1.212-220` (8 versions 17-25 juil. : /fork background, EndConversation, patch sécu PowerShell 5.1, flip-flop nesting subagents depth 3, skills fork→background) ; `06-Industrie/graph-engineering-buzz` (buzz Steinberger 18 juil., PAS une feature Anthropic, fake « étude Stanford+Anthropic $3,1M » débunké)
- **Modifiées** : `00-Hub/MOC-Modeles` (Opus 5, recadrage Fable, retraits) ; `01-Claude/models/Fable 5` (AJOUT recadrage accès 20 juil. : 50 % limites Max/Team Premium, -33 % limites, Pro→credits) ; `04-Techniques/claude-code/comment-creer-hook` (callout 30 events : +DirectoryAdded v2.1.219, source 'fork' SessionStart) ; `comment-creer-agent` + `anti-reentrance-sub-agents-pattern-escalade` (AJOUT nesting depth 3 + caps 200/20 + dépréciation param mode Task) ; `comment-creer-skill` (AJOUT context:fork background par défaut, /verify //code-review plus auto) ; `effort-opus-47-doctrine-anthropic-2026` (AJOUT Opus 5 thinking ON, erreur 400 thinking disabled+xhigh/max, Opus 4.7 hors fast mode) ; `mcp-vs-skills-doctrine` (AJOUT détails RC 2026-07-28 : core stateless, FastMCP→MCPServer, MCP Apps, dépréciation 12 mois)
- **Source** : run cc-news 27 juillet (fenêtre 16-27 juil.) — changelog officiel CC, annonce Anthropic « Introducing Claude Opus 5 » (24 juil.), blog officiel MCP (RC 2026-07-28), 5 agents de veille sources croisées

## 2026-07-21 — 2 vidéos X transcrites : talk AI DevCon memory/dreaming (Lamis) + talk Boris 2025 recyclé

- **Modifiées** : `01-Claude/Code/features/Memory Managed Agents` (AJOUT talk AI DevCon by Tessl — évolution mémoire 4 stades, 3 bottlenecks production, boucle hash-retry, memory poisoning par prompt injection, slide 97%/27%/34%, Q&A « deterministic harness ») ; `01-Claude/Code/features/Dreaming Managed Agents` (AJOUT intérieur d'un dreaming pass — orchestrateur + 1 subagent/transcript, stats de prévalence, steering, analogie école) ; `04-Techniques/agents/technique-dreaming-cross-session` (statut « 97% » upgradé : slide officielle Anthropic anonymisée) ; `04-Techniques/patterns/verification-sources-canoniques` (patterns 5-6 : quote inventée par tweet d'engagement + contenu vidéo recyclé non daté).
- **Leaders** : `05-Leaders/claude-code/Boris Cherny` (section talk fondateur « pro tips » Code with Claude mai 2025 — onboarding 2-3 sem→2-3 j, 80% staff quotidien, sécurité bash, pourquoi CLI).
- **Source** : 2 vidéos natives X partagées par Raphael (tweets @cyrilXBT 20 juil. + @hrswatigupta 19 juil.), pipeline x-read → curl MP4 → ffmpeg → faster-whisper + analyse frames (28+31 screenshots). Les 2 hooks viraux se sont révélés faux (citation inventée ; talk de mai 2025 présenté comme neuf).

## 2026-07-16 — Arbitrage v : traces DOCTRINE_REINFORCE + 6 enrichissements + MAJ skills réf

- **Modifiées (traces doctrine)** : `outcome-first-prompting` + `deprecated-techniques-2026` — challengées + confirmées 16 juil. par guide GPT-5.6 (9 juil.) + Mollick/Wharton (7 juil.), chiffres neufs (leaner prompts = +10-15 % score, -41-66 % tokens).
- **Modifiées (enrichissements)** : `Cowork GA` (web/mobile 7 juil., sessions remote, >90 % non-coding) ; `MOC-Codex` (CLI 0.144.5, Atlas à confirmer) ; `05-Leaders/prompt/Ethan Mollick` (post 7 juil.) ; `05-Leaders/industrie/Demis Hassabis` (manifesto watchdog 14 juil.) ; `08-xAI/products/xAI Grok` (Grok 4.5 + SpaceXAI + scandale Grok Build) ; `05-Leaders/rag/Jerry Liu` (Retrieval Harness).
- **Skills réf MAJ via self-updater** : cc-cowork-ref, codex-ref, cc-features-ref (findings post-7 juil.).
- *(rectif : MAJ appliquées par la session principale — sub-agent self-updater bloqué par delegate-guard, gap capitalisé dans `delegate-guard-pattern` ; codex-ref finalement inchangé, design single-source vers MOC-Codex déjà à jour)*
- **Source** : arbitrage Raphael `v` sur le rapport cc-news du 16 juillet.
## 2026-07-16 — Run cc-news : GPT-5.6, Grok 4.5, CC v2.1.203-211

- **Ajoutées** : `01-Claude/Code/changelog/CC juillet 2026 - v2.1.203-211.md` (9 versions 7-15 juil. : auto mode défaut gateways, screen reader, hardening injection Agent tool, fix billing caching) ; `02-OpenAI/models/GPT-5.6.md` (Sol/Terra/Luna, gating gouvernemental, Programmatic Tool Calling, scheming METR) ; `08-xAI/models/Grok 4.5.md` (SpaceXAI, token efficiency 4.2x, leak Cursor) ; `01-Claude/Code/features/Claude Reflect.md` (dashboard usage 9 juil.) ; `06-Industrie/industrie-juillet-2026.md` (Hassabis watchdog, Nous 1.5Md$, DeepSeek IPO, MS Frontier Company).
- **Modifiées** : `00-Hub/MOC-Modeles.md` (+ GPT-5.6, Grok 4.5, MAJ ligne Fable 5 redéployé).
- **Modifiée (learning post-run)** : `04-Techniques/claude-code/comment-creer-skill.md` — AJOUT 13 juillet nuancé : le ScannerError ` : ` venait du validateur PyYAML (borne conservatrice), pas d'un échec de chargement CC observé — datapoint cc-news charge avec ` : ` sur CC 2.1.211.
- **Source** : run `/cc-news` complet 16 juillet (Tier 0 + 16 agents), référence précédente 7 juillet (v2.1.202).
## 2026-07-16 — Premier run /vault-health (PASS)

- **Ajoutées** : `Knowledge/reviews/vault-health-2026-07-16.md` (rapport hebdo 4 sections — lint 11→9 low_aliases, consultation 7j saine ratio create/search 1,08×, adoption cross-repo 0 = baseline J0, inbox 1 note).
- **Modifiées** : `critique-plan-modernisation-bdd-claude` (aliases 0→4) + `delegate-guard-pattern` (aliases 3→4) — micro-fixes liste fermée (b).
- **Source** : premier run manuel de la routine `/vault-health` (SPEC TODO/SPEC-loop-vault-health.md), triple check PASS.
## 2026-07-16 — Analyse Karpathy/vague virale + extension cerveau user-scope + boucle refile

- **Ajoutées** : `Knowledge/critiques/critique-2026-07-16-vault-global-user-scope.md` (verdict DA sur le plan d'extension — 1 BLOCKING 82 arbitré).
- **Modifiées** : `pattern-vault-llm-karpathy` (section VAGUE VIRALE JUILLET 2026 — généalogie 8-15 juil., modes d'échec documentés, consensus « gouvernance > infrastructure », application forge) ; `decision-vault-agent-first` (§ Validation externe + extension user-scope machine actée) ; `mcp-vault-llm-design` (purge lien mort `old` dans exemple code) ; `Simon Willison` + `dette-detection-signaux-friction-skills` (liens vers non-notes réécrits en texte nu — lint 0 wikilink brisé).
- **Source** : article X @chesny 15 juil. (reprise ES du guide viral @kirillk_web3) → recherche 15+ sources ; diagnostic stagnation mesuré (consultation −80 %/30j, 65 % des sessions de juin hors forge sans MCP) ; arbitrage Raphael + DA : config MCP user-scope (Part A appliquée), `~/.claude/CLAUDE.md` global (Part C), hook SessionStart user en diff manuel (Part B), convention single-writer append-only hors forge, mesure J+14 (2026-07-30), P2b débundlé. Hors vault : rule forge-brain-proactive (refile + fausse-absence), skill x-read (fix users_by_login + gotcha article X), SPEC-loop-vault-health (draft).

## 2026-07-15 — Gotcha boot lent MCP (Gotcha #4) après RUN de vérif tool_events

- **Modifiée** : `04-Techniques/claude-code/ajouter-source-donnees-mcp-forge-brain.md` — nouveau **Gotcha #4** (section Cycle de vie) : premier boot LENT (rebuild DB + gros scan initial) → handshake MCP de la nouvelle session expire → TOUS les outils forge-brain absents (pas seulement le nouveau). Distinguer de l'échec d'enregistrement ; fix = 2e nouvelle session serveur chaud. Diagnostic PowerShell (Invoke-WebRequest 404 = vivant, db-wal figé = scan fini).
- **Source** : chantier `tool_events` (15 juil.). RUN de vérification du mode `skill-evolve friction` réussi : `search_tool_events(is_error=true)` remonte les vraies frictions récurrentes cross-session (schémas MCP read_section/update_property, delegate-guard, mcp-alias-guard). Finding : heuristique `is_error` a des faux positifs (AskUserQuestion/Read marqués [ERROR] sur « error » cosmétique) → à filtrer au regroupement (noté dans l'Apprentissage de skill-evolve, hors vault). TODO de capture supprimé après intégration.
## 2026-07-15 — Enrichissement mémoire Codex avancée (couche gérée + pattern auto-améliorant)

- **Modifiées** : `04-Techniques/codex/memoire-optimale-codex-chatgpt.md` (nouvelle section « Mémoire GÉRÉE par l'utilisateur » : native [memories] non-éditable → couche externe possédée ; 2 couches instruction/learned ; options MCP mem0/Basic Memory/Letta ; arbitrages portabilité/staleness/versioned-reads) ; `04-Techniques/codex/loop-apprentissage-codex.md` (section « pattern auto-améliorant » : squelette convergent 5 étapes, artefacts praticiens ECC/Dimillian/chatprd/Kulaxyz, 5 archétypes arXiv vérifiés ExpeL/Voyager/MemGPT/AWM/ACE).
- **Source** : recherche mémoire Codex avancée (demande Raphael, 2 agents read-only). Axe A tranché à la source : mémoire native Codex délibérément non pilotable à la main (« treat these files as generated state »). Axe B : le pattern « l'agent se forme seul » converge vers Trigger→Source→Extraction→VALIDATION→append-incrémental. 5 IDs arXiv vérifiés (arxiv-verification, agents ayant tourné sans classifieur sécu). Willison silencieux sur mémoire Codex (foyer = Jesse Vincent/Superpowers côté CC) ; OpenAI interne = compounding humain-piloté. Décision : capitaliser (fait) + amorcer un /loop forge d'auto-amélioration skills (recette ECC+ACE+validation gate, via loop-forge, SPEC avant impl).
## 2026-07-15 — Doctrine Codex : corpus 04-Techniques/codex/ + doctrine ChatGPT-seul + MOC-Codex

- **Ajoutées** (10, `04-Techniques/codex/`) : `workflow-codex-optimal.md` (note maître — Surface Map des 8 leviers, multitasking Sottiaux, séquence S/M/L/XL), `agents-md-codex.md` (cap 32 KiB `project_doc_max_bytes`, nesting, `AGENTS.override.md`), `config-toml-profils-codex.md` (rupture profils 0.134.0 = crash boot, précédence, requirements.toml), `comment-creer-skill-codex.md` (divergences vs standard Agent Skills : `.agents/skills`, sidecar `openai.yaml`, 4 scopes, portabilité NON byte-identique), `comment-creer-hook-codex.md` (stable v0.124.0, 10 events, piège `Stop` inversé, gap `additionalContext`/PreToolUse, trust model par hash), `subagents-cloud-codex.md` (TOML `developer_instructions`, max_threads=6/max_depth=1, CSV batch, automations RRULE), `loops-codex.md` (`codex exec`, automations, CI `openai/codex-action`), `loop-apprentissage-codex.md` (compounding `[memories]` + « scan sessions → update skills »), `memoire-optimale-codex-chatgpt.md` (montage mémoire cross-tool), `codex-vs-chatgpt-seul.md` (arbitrage produit).
- **Ajoutée** (1, `04-Techniques/chatgpt/`, nouveau dossier) : `personnalisation-chatgpt-app.md` (custom instructions, Projects, mémoire native, GPTs, connectors, Assistants API sunset 26 août 2026 → Responses API ; provenance dégradée signalée : help.openai.com 403 → paraphrase WebSearch).
- **Ajoutée** (1, `00-Hub/`) : `MOC-Codex.md` (index Codex, miroir de MOC-Claude-Code).
- **Modifiées** : `00-Hub/MOC-Techniques.md` (section « OpenAI Codex » → MOC-Codex) ; `02-OpenAI/products/OpenAI Codex.md` (section « MàJ 15 juil. 2026 » : état verrouillé GPT-5.6 Sol/Terra/Luna + pointeur doctrine).
- **Source** : chantier doctrine Codex (mission analyste 15 juil.). Recherche = sonde de sources (gate) + 6 agents read-only en parallèle sur sources primaires (`learn.chatgpt.com/docs/*`, repo `openai/codex` releases, Pragmatic Engineer, Willison), retour structuré par claim (verbatim + URL + date + confiance). Trois prémisses du brief corrigées à la source : hooks **stables** (pas expérimentaux) depuis v0.124.0 ; `on-failure` **déprécié** ; défaut CLI = **gpt-5.6-sol** (pas GPT-5-Codex). Doc officielle a migré (`developers.openai.com/codex/*` → `learn.chatgpt.com/docs/*` ; `docs/config.md` repo = stub). Chaque note distingue certain/probable/à-vérifier et date les données volatiles.
## 2026-07-15 — Base 05-Leaders/codex : 7 pointures OpenAI Codex
## 2026-07-15 — Audit couche-2 config .claude/ du repo bdd

- **Modifiées** : `04-Techniques/patterns/audit-claude-folder-pattern.md` — nouvelle section « Variante — audit COUCHE 2 quand un plan de modernisation existe déjà » (détecter un plan `.claude/todo/` récent → vérifier les `[x]` empiriquement, drift plan↔réel dans les deux sens, angles morts ; gotcha propagation incomplète d'un `git mv agents/→roles/` ; piège de brief « grep nom du dev courant » qui manque le chemin d'un autre dev).
- **Source** : audit du `.claude/` de bdd (15 juil.) — 3 agents parallèles + vérif empirique. Le repo avait déjà un plan de modernisation du 13 juil. exécuté à ~80 % → bascule en audit couche-2. Rapport archivé `claude-forge/output/audit-bdd-claude-2026-07-15.md`.


- **Ajoutées** : `05-Leaders/codex/Thibault Sottiaux.md` (head/eng lead Codex → GM core product), `Michael Bolin.md` (tech lead dépôt OSS openai/codex), `Fouad Matin.md` (release initiale CLI, sécu/sandbox), `Gabriel Peal.md` (ext VS Code + desktop), `Josh McKinney.md` (mainteneur Ratatui recruté full-time), `Andrew Ambrosino.md` (lead desktop app, doctrine taste>implementation), `Shao-Qian Mah.md` (researcher modèles). Nouveau dossier `05-Leaders/codex/`.
- **Modifiées** : `00-Hub/MOC-Leaders.md` — nouvelle section "Codex / OpenAI" (7 fiches).
- **Leaders** : 7 fiches Codex, chacune vérifiée sur ≥2 sources primaires (Pragmatic Engineer "How Codex is built" de Gergely Orosz + API GitHub openai/codex contributors + X/blogs). Doublons ignorés : Sam Altman, Simon Willison, Andrej Karpathy, Lilian Weng, Jason Wei (déjà présents, aucun fond Codex spécifique à ajouter).
- **Source** : phase veille Codex (mission analyste 15 juil.). Contributeurs semi-anonymes (jif-oai #1, pakrym-oai) écartés faute de nom vérifiable. Greg Brockman / Nick Turley = figures org, pas fiche (Brockman ⊂ industrie, proche Sam Altman existant).
- **Enrichie** : `05-Leaders/agents/Simon Willison.md` — section "Angle Codex" (praticien externe de référence : reverse-engineering Codex CLI, Codex + modèles self-hosted, lethal trifecta appliqué à Codex). Cercle A bullet 3 (praticiens externes) et Cercle B (usage pro ChatGPT/API) cherchés puis constatés MAIGRES : paysage dominé par contenu SEO/agrégateur et blogs d'entreprise, aucune pointure individuelle passant la barre reconnaissance+fond+≥2 sources primaires hormis Willison (déjà fiché, enrichi).

## 2026-07-15 — Pattern personas session principale (chantier bdd, demande Raphael)

- **Ajoutées** : `04-Techniques/claude-code/pattern-personas-session-principale.md` — canonique du pattern rôles/personas chargés en conversation principale (convention @dev via CLAUDE.md) vs subagents (AskUserQuestion officiellement indisponible, vérifié doc 15 juil.) vs Agent Teams ; grille de décision, piège namespace .claude/agents/, 6 best practices, cas réel bdd. `Knowledge/critiques/critique-execution-modernisation-bdd.md` — verdict DA SHIP (0 bloquant) sur l'exécution complète du chantier bdd.
- **Modifiées** : `04-Techniques/claude-code/comment-creer-agent.md` — AJOUT 15 juillet : persona de dialogue ≠ subagent, pointeur vers la nouvelle canonique.
- **Source** : chantier modernisation bdd (§4 roles/) + recherches web 15 juil. (doc officielle sub-agents/agent-teams, claude-personas, persona-generator, ultimate-guide).

## 2026-07-13 — Gotcha YAML descriptions une-ligne (chantier bdd)

- **Modifiées** : `04-Techniques/claude-code/comment-creer-skill.md` — AJOUT 13 juillet : `deux-points + espace` dans une description une-ligne non quotée = ScannerError → skill silencieusement non chargée. Remplacer ` : ` par ` — `, options `[sujet:{texte}]` sans espace, re-valider le parsing à toute migration `>-` → une-ligne.
- **Source** : chantier modernisation `.claude/` repo bdd (13 juil., branche us/RPI/PP-N2-111820-claude-skills) — 13 descriptions touchées, attrapé par validation PyYAML avant livraison.

## 2026-07-09 — Fusions skills forge-review : verification-sources-canoniques créée

- **Ajoutées** : `04-Techniques/patterns/verification-sources-canoniques.md` — matrice provider single-source + pattern vérification verbatim + 4 patterns d'erreur, promue depuis l'ex-skill `web-search-canonical-source` (foldée dans la rule `contenu-externe-non-fiable`, verdict forge-review + DA SHIP, arbitrage Raphael)
- **Modifiées** : `Knowledge/erreurs/erreur-vault-jamais-consulte-session-principale.md` — récidive 9 juil. (arbitrage DA sans lecture des précédents cités) + règle durcie « lire EN ENTIER les notes citées par un agent avant de relayer son verdict »
- **Source** : forge-review scope skills (fusions/kills) — F1 cc-rag-ref→rag-design/references/ appliquée, F2 trio doctrine en measure-first (critique DA `Knowledge/critiques/critique-2026-07-09-fusions-skills-forge.md`)
## 2026-07-09 — /done : raisonnement debug delegate-guard + contextes projet

- **Ajoutées** : `Knowledge/raisonnements/raisonnement-debug-delegate-guard-empilement.md` — chaîne de diagnostic du double bug d'attribution (fenêtre 15 lignes + estampille figée sur la première skill du tour), fix 39/39 validé en réel.
- **Modifiées** : `1-Projets/Claude-Forge/Claude-Forge.md` (état récent 9 juil.) ; `0-Inbox/context-actuel.md` (working memory).
- **Source** : /done fin de session forge-review + fix guard.
## 2026-07-09 — Nuance keyword stuffing : cross-lingue confirmé, 1-2 phrases FR tolérées

- **Modifiées** : `Knowledge/erreurs/e-descriptions-keyword-stuffing.md` — nouvelle section « Nuance 9 juillet 2026 » : routing skills = matching sémantique LLM pur (cross-lingue natif, vérifié web), 1-2 phrases FR exactes acceptables comme ancres, seule la liste exhaustive entre guillemets reste du stuffing. Aligné [[comment-creer-skill]].
- **Source** : sweep /skill-evolve descriptions (21 skills raccourcies ≤ 250 chars) — tension résolue entre cette note d'erreur (avril) et la canonique (mai/juin).
## 2026-07-03 — Pattern brouillon Confluence natif comme gate de validation (enrichissement)

- **Modifiées** : `04-Techniques/chatbot/rovo-agent-automation-confluence.md` — nouvelle section « Le gate de validation = brouillon Confluence NATIF (pas un dossier custom) » : `createConfluencePage(status="draft")` non indexé tant que draft, validation humaine = bouton « Publier », jamais `updateConfluencePage` (brouillon « [remplace] X »). Affine l'« Option B » (gate custom « À valider ») avec le mécanisme natif.
- **Source** : chantier refonte suite skills `neodoc` (Cowork, écriture par skill) — décision d'archi Raphael de remplacer le dossier Brouillon par le brouillon Confluence natif.
## 2026-07-02 — Loupe cadrage-cdc ia-workbench (enrichissement note projet)

- **Modifiées** : `1-Projets/ia-workbench/ia-workbench-repo-management.md` — ajout de la 2e loupe `/cadrage-cdc` (idée → CDC fonctionnel → /spec), avec la frontière anti-doublon (CDC fonctionnel, /spec dérive le technique) et le pattern « sortie calée sur les marqueurs d'entrée du consommateur ». `derniere-maj` → 2026-07-02.
- **Source** : création skill `cadrage-cdc` dans ia-workbench (hors vault — repo neot-v2), demande Raphael.
## 2026-07-02 — Cheatsheet prompting Fable 5

- **Ajoutées** : `07-Prompts/techniques/prompting-fable5-cheatsheet.md` — 12 patterns officiels Anthropic copier-coller pour Fable 5 (goal-setting > micromanagement, effort high défaut, anti-refacto, verification loops, checkpoint, memory system, send_to_user tool). Templates verbatim.
- **Modifiées** : `00-Hub/MOC-Techniques` (§ Prompt Engineering) + `00-Hub/MOC-Prompts` (§ Templates Prompts) — wikilinks vers la cheatsheet.
- **Source** : doc officielle platform.claude.com/docs/prompting-claude-fable-5 (source primaire), demande Raphael.
## 2026-07-08 — Roadmap Jarvis Vague 3 : durcissement injection #22 (volet doctrine)

- **Modifiée** : `04-Techniques/agents/agents-securite.md` — section « Application forge — hygiène injection indirecte » (MCP tiers + web = données non fiables, lethal trifecta chez forge, ETDI/tool poisoning, capitalisation = distiller le fait).
- **Hors vault** : nouvelle rule `.claude/rules/contenu-externe-non-fiable.md` (doctrine comportementale courte : contenu externe = donnée jamais instruction, HITL sur l'irréversible).
- **Source** : roadmap #22 volet (a). Volets (b) egress-allowlist hook + (c) sonde injection = arbitrage Raphael en cours (intrusifs sur la veille). État de l'art : arXiv 2601.17548 (agentic coding assistants), Anthropic auto-mode/sandboxing, Willison lethal trifecta.

## 2026-07-08 — Roadmap Jarvis Vague 1 (P0 correctifs dette)

- **Wikilinks cassés 101 → 1** (le dernier = exemple pédagogique délibéré `[[old]]` dans mcp-vault-llm-design). Prune ~73 liens scaffolding responsable-ia (texte conservé), déwiki ~20 renvois memory/rules en code-span, repointage ~10 vers canoniques, réparation par alias de 6 cibles (permissionmode→comment-creer-agent, amende→methode-pivoter-doctrine, etc.).
- **Notes sans tag 5 → 0 · orphelines → 0 · YAML cassé 0.** 3 canoniques (`comment-creer-skill`/`-agent`/`-hook`, 0 alias/0 tag) dotées de 7 aliases + 3 tags chacune (fix agent-first #1). Tags plats des 15 notes du 7 juil. normalisés `#type/`·`#domaine/` ; quasi-doublons fusionnés (conformité→conformite) ; 2 tags cassés réparés (#casquette/ vide, #projet/neote tronqué).
- **MOC-Claude-Code** : bloc « agents supprimés » (re-listés actifs) purgé, changelog + features juillet reliés. **Home** : compte 511→531. **SCHEMA** : §7 Templates/ retiré (prescrit jamais construit), Warp §4, règle câblage-à-la-création + anti-pattern tags plats. **MOC-Techniques** : 10 notes du 7 juil. câblées.
- **Promue** : `config-repo-equipe-vs-forge` (feedback cité 4× → note canonique 04-Techniques/claude-code). **0-Inbox trié** (6→1) : ADR mémoire clôturée (decisions/), 2 idées (raisonnements/), 2 synthèses Hermes (syntheses/).
- **`.claude/`** : repo-inspector:111 flippé (agent-memory = pattern VIVANT, plus jamais flaggé vestige — DA), forge-review:87 réf morte réparée, `.claude/agent-memory/agent-creator/` vestige purgé, memory-saturation-watcher recalibré 250/290→180/220 (+ tests), trigger-map 28→38 skills, 2 stubs rules supprimés.
- **Source** : roadmap `docs/roadmap-jarvis-2026-07.md` P0. Confirme 3× le pattern « les agents sur-classent » (audit-vault proposait 2 fusions de tags qui étaient des axes sémantiques légitimes).

## 2026-07-07 — Audit complet forge + roadmap Jarvis (4 agents + DA)

- **Ajoutées** : `Knowledge/critiques/critique-2026-07-07-roadmap-jarvis.md` (par l'agent devils-advocate — 2 bloquants : #7 agent-memory flippé, #20 rules conditionnelles re-scopé)
- **Livrable repo** : `docs/roadmap-jarvis-2026-07.md` — 35 items P0→P3 (correctifs dette vault/.claude/, quick wins CC v2.1.202, chantiers sécurité MCP + proactivité Jarvis, arbitrages)
- **Source** : audit 4 agents parallèles (config .claude/ 3 lentilles, vault structurel, gap features CC, état de l'art web) + vérif empirique session principale + verdict DA intégré

## 2026-07-07 — Migration memory→vault (triage 247 fichiers, workflow)

- **Ajoutées (14 notes)** : `04-Techniques/patterns/` audit-thematique-claims-vault, refactor-masse-script-python-regex, verifier-audit-deja-fait-avant-relancer, verify-empirique-avant-affirmation-session ; `04-Techniques/claude-code/` architecture-claude-folder, enableallprojectmcp-permissions-allow, skills-externes-upstream-sync, skills-metadata-tokens-load, worktrees-sessions-paralleles ; `04-Techniques/mcp/mcp-tool-prefix-serveur-wiring` ; `04-Techniques/outils/pdf-chrome-headless` ; `Knowledge/erreurs/` changer-mecanisme-lire-tests-qui-verrouillent, llm-deep-research-version-numbers-hallucinated ; `Knowledge/raisonnements/raisonnement-da-probe-empirique-avant-verdict`
- **Enrichies (33 notes)** : comment-creer-skill/-agent/-hook, auto-mode-classifier, methode-pivoter-doctrine, workflow-claude-code-optimal, plugin-vs-skill-anatomie, architecture-cerveau-obsidian-mcp, methode-analyser-repo, etc. (49 insertions, 478 lignes ajoutées, 0 écrasée)
- **Source** : triage read-only de 247 fichiers `memory/` (feedback+reference) vs vault via 3 workflows (50 agents triage + 53 prep + 48 apply). Contenu doctrinal doublon/absent migré, puis 114 fichiers memory supprimés (259→145). MEMORY.md 162→89 lignes. Re-tri session principale : 2 faux DELETE + 13 faux ENRICH corrigés (agents sur-classent).
## 2026-07-07 — Scan cc-news : CC v2.1.199→202 (source primaire)

- **Modifiées** : `01-Claude/Code/changelog/CC juillet 2026 - Sonnet 5 + v2.1.198.md` étendue à v2.1.202 (ajout sections 199/200/201/202, titre + resume + aliases + derniere-maj)
- **Findings CC** : Dynamic workflow size dans `/config` + OTel workflow (202) ; fix re-invoke skill dupliquée (202) ; `AskUserQuestion` no auto-continue + mode « default »→« Manual » non-breaking (200) ; slash-skills empilées jusqu'à 5 + sous-agents remontent erreurs API/partiels au parent + hooks stderr exit 2 affiché (199)
- **Impact forge signalé (pas de modif)** : renommage `default`→`Manual` non-breaking pour `permissionMode` ; fix « sous-agent erreur=succès » atténue partiellement `post-dispatch-verify` (pas le Write-denied exit 0)
- **Non capitalisé** : Fable 5 redéploiement 1er juillet (déjà dans [[Fable 5]]) ; Gemini 3.5 Pro encore en preview (pas de GA daté)
- **Source** : https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md

## 2026-07-02 — Scan cc-news complet : Sonnet 5 + CC v2.1.198 + vérifs primaires

- **Ajoutées** : `01-Claude/models/Sonnet 5.md` (modèle défaut CC v2.1.197, 1M natif, nouveau tokenizer ~1.0-1.35× tokens, pricing promo $2/$10 jusqu'au 31 août) ; `01-Claude/Code/changelog/CC juillet 2026 - Sonnet 5 + v2.1.198.md` (v2.1.191→198 vérifié CHANGELOG primaire : /dataviz, Claude in Chrome GA, background agents auto-PR, Explore hérite modèle session cap Opus, hook matchers hyphénés exact-match, sécu spawn MCP non approuvés)
- **Modifiées** : `Tim Dettmers` (correctif attribution SERA → papier AI2/Shen et al., Dettmers senior author ; claims 26×/57×/Devstral sourcés arXiv 2601.20789 + blog AI2, pas le blog perso)
- **Source** : scan cc-news 16 agents. Vérifs source primaire : CC CHANGELOG, MCP spec 2026-07-28 (stateless final), Sonnet 5 (anthropic.com, 30 juin), Karpathy→Anthropic (déjà au vault), LeCun/AMI Labs (déjà au vault), FlashAttention-4 (déjà au vault, Tri Dao), SERA. Rejetés comme non-nouveaux/hors-périmètre : Cohere Rerank 4 (11 déc 2025), OpenClaw (assistant messagerie, hors veille), AI Scientist-v2 (mars 2025). Découverte méthode : 4/6 candidats déjà à jour au vault → confirmation, pas révélation.
- **Doctrine (en attente gate)** : 2 traces REINFORCE proposées — controverse Adaptive-Thinking/effort sur `effort-opus-47-doctrine-anthropic-2026`, MCP stateless final sur `construire-mcp-production`.
- **Maintenance skill cc-news** : query morte `paperswithcode.com` repointée (HF Papers + CodeSOTA) ; Gemini CLI→Antigravity noté (migration forcée 18 juin) ; date de référence SKILL.md → 2 juillet 2026 / v2.1.198.

## 2026-06-30 — Hooks : OBLIGER vs RECOMMANDER + pattern routeur skill-trigger (recalibrage confiance Anthropic/forge)

- **Modifiées** : `comment-creer-hook` (AJOUT 30 juin : 2 modes d'action OBLIGER/RECOMMANDER, niveau de confiance Anthropic-literal vs doctrine forge, pattern routeur skill-trigger + gotchas) ; `cowork-skills-reliability` (section Skill Activation Hook étoffée : keyword vs forced-eval, sources communautaires) ; `anti-pattern-hookify-workflow-hooks` (ligne recalibrage : frontière no-workflow = doctrine forge, PAS règle Anthropic).
- **Hors vault** : `.claude/skills/hook-creator/references/checklist-hook-parfait.md` (1 ligne étape 0 : mode OBLIGER/RECOMMANDER) ; doublon `.claude/skill-triggers.json` (sans point, orphelin périmé) supprimé via git rm.
- **Source** : correction Raphael en session — j'avais aplati « hooks = lint/sécu/scope uniquement, jamais obliger ». Faux : exit 2 bloque (verbatim Anthropic vérifié code.claude.com/docs/en/hooks 30 juin), et le couple `.skill-triggers.json` + `skill-activation.py` route déjà vers les bonnes skills sur forge/neo_ia/back-ts. Vérif source primaire : la frontière no-workflow n'est PAS une règle Anthropic (doc muette) mais une doctrine forge (Boris thinnest wrapper). Pas de pivot — la doctrine vault était déjà correcte (AJOUT 18 juin + critère ACTION/SÉQUENCE 9 juin), c'était l'aplatissement de session qui était l'erreur.

## 2026-06-27 — Pivot doctrinal vault agent-first INSTRUIT (émancipation de Karpathy)

- **Ajoutées** : `Knowledge/raisonnements/raisonnement-2026-06-27-vault-agent-first.md` (instruction du pivot via methode-pivoter-doctrine).
- **Modifiées** : `SCHEMA.md` (raw/ retiré des couches, ontologie, ingest, anti-patterns, bandeau STATUT), `pattern-vault-llm-karpathy` (bandeau STATUT en tête chapeautant DRIFT/REQUALIF = trace), `architecture-cerveau-obsidian-mcp` + `mcp-vault-llm-design` + `LLM Wiki` (caveats forge-brain exception), `index.md` (raw/ + métadonnées Karpathy → agent-first, stats 480→511), `00-Hub/Home.md` (resume + lien Karpathy + derniere-maj). Hors vault : rule `forge-brain-proactive.md`, skill `pivot-check/SKILL.md` (exclusion raw/ morte retirée), `memory/feedback_drift_implementation_karpathy_organes_morts.md`.
- **Source** : décision [[decision-vault-agent-first]] (acceptée 2026-06-27) — forge-brain = cerveau d'agent piloté via MCP, Karpathy = échafaudage dépassé. raw/ supprimé, index/log/MOC = couche humaine optionnelle. Plan validé par advisor + devils-advocate (critique-2026-06-27-pivot-vault-agent-first), périmètre étendu 6→11 foyers après détection de foyers manqués. RESTE (ÉTAPE B) : alléger FOLDER_TO_MOC dans vault-audit.

## 2026-06-27 — Pivot agent-first + /done étape 6-bis (capitalisation session)

- **Ajoutées** : `Knowledge/decisions/decision-vault-agent-first.md` — ADR : forge = cerveau d'agent, Karpathy = échafaudage dépassé (raw/ tué, MOCs = couche humaine optionnelle, SCHEMA à refondre). Pivot à instruire via `methode-pivoter-doctrine`.
- **Modifiées** : `0-Inbox/context-actuel.md` (working memory) ; `1-Projets/Claude-Forge/Claude-Forge.md` (état récent + `derniere-maj` 2026-06-27) — via la nouvelle étape 6-bis de `/done`.
- **Outillage (.claude, hors vault)** : `skills/done/SKILL.md` étape 6-bis (maj notes contexte projet) ; mémoire — `feedback_pas-dogmatique-patterns-externes` (tier-2) + amendement `feedback_vault_edit_gotchas_outillage` (gotcha delete_note).
- **Source** : `/done` de fin de session (audit outillage vault + vision agent-first de Raphael).

## 2026-06-27 — Nettoyage vault : suppression raw/ (8 notes) + audit outillage (hub, MCP)

- **Supprimées** : `raw/2026-05-22-chantier/` — 8 notes `recherche-*` (bruts d'un chantier déjà distillés en canoniques). Pattern « pureté du contexte » : un brut = variable jetable. 1 wikilink mort résiduel dans [[pattern-vault-llm-karpathy]] (~L514) — à nettoyer (révèle une limitation MCP : pas d'édition ciblée).
- **Analysé, non modifié** : `00-Hub/` MOCs — suppression **écartée** (`MOC-Techniques` = ~95 backlinks ; casser les liens = dette nette pour bénéfice nul). Vrai défaut = `FOLDER_TO_MOC` de `vault-audit` pointe vers dossiers périmés (`02-Concurrents`/`03-Modeles`, provider drift 14 juin).
- **Source** : demande Raphael — hygiène vault + question outillage MCP/skills.

## 2026-06-27 — Second Cerveau IA (cours Eliott Meunier) : CMA + n8n + idée inbox

- **Ajoutées** :
  - `04-Techniques/patterns/cartographier-process-cma.md` — méthode CMA (Clarifier/Mapper/Amplifier), fiche process, mapping par fréquence, arbre agent-vs-automatisation, anatomie statique/dynamique/méthode, routage vers `loop-forge` (boucle CC) ou n8n (externe). Amont de [[methode-monter-systeme-workflow]].
  - `04-Techniques/claude-code/n8n-self-host-mcp-claude.md` — recette self-host n8n (Hostinger+Dokploy) + MCP n8n czlonkowski piloté par Claude, point RGPD, spec future skill `/n8n-automate`.
  - `0-Inbox/workflow-inbox-capture-vrac.md` — idée dormante : inbox capture-vrac → tri auto ; diagnostic « pourquoi dormant dans forge » + condition de viabilité (flux entrant).
- **Modifiées** : `04-Techniques/agents/agents-automation.md` — AJOUT callout « Choix forge/Neoteem : n8n en priorité » (Zapier/Make conservés pour la veille, écartés par défaut). Aucune suppression.
- **Source** : vidéo YouTube IubQUC9TL2w (Eliott Meunier — L'IA devient simple avec un Second Cerveau IA, cours complet). Le vault couvrait déjà ~80 % (IPCRA, `architecture-cerveau-obsidian-mcp`, `methode-monter-systeme-workflow`) → capitalisation du delta neuf uniquement, zéro doublon, zéro nouvelle skill.

## 2026-06-26 — Correction note ADF Jira + critique DA chantier /spec

## 2026-06-26 — Pattern footer-gate hook repo d'équipe (canonique hook)

- **Modifiées** : `04-Techniques/claude-code/comment-creer-hook.md` — AJOUT « Hook de validation sur repo d'ÉQUIPE : un marqueur dans l'artefact = gate d'étanchéité » (prolonge l'AJOUT 18 juin hook-de-structure). `derniere-maj` → 2026-06-26.
- **Source** : déblocage DA+advisor du chantier /spec — résout l'anti-pattern « hook bloquant large sur repo d'équipe » via discriminant footer écrit par l'outil producteur, lu comme gate d'entrée (pas de marqueur → SKIP).

- **Modifiées** : `Knowledge/questions/jira-rendu-adf-mcp-atlassian.md` — AJOUT corrigeant le gotcha #1 (le read MCP `responseContentFormat:"adf"` renvoie BIEN l'ADF structuré, vérifié 26 juin ; l'ancien « toujours markdown au read » était faux/périmé). `derniere-maj` → 2026-06-26.
- **Ajoutées** : `Knowledge/critiques/critique-2026-06-26-uniformisation-spec-3-repos.md` — verdict devil's advocate sur le plan hook+skill+cosmétique (3 BLOCKING résolus via marqueur footer /spec).
- **Source** : chantier normalisation tickets /spec 3 repos (option B Gherkin en PJ, hook footer-gate, retrait lignes parasites IA-27/28/33/34).

## 2026-06-24 — Correction drift : MCP local stdio MARCHE en Cowork (retour terrain)

- **Modifiées** : `01-Claude/Cowork/mcp-local-cowork-vs-claude-code.md` — amendement daté : la prémisse « localhost impossible en Cowork » est FAUSSE pour le transport **stdio**. Cowork lance le process en local (comme Desktop Chat) → stdio marche, pas besoin de tunnel HTTPS. La vraie distinction est le TRANSPORT (stdio ✅ / HTTP-localhost ❌ / HTTPS public ✅), pas local-vs-cloud. `titre`/`resume`/`derniere-maj` corrigés pour que le faux claim ne sorte plus en tête de search_brain.
- **Source** : retour terrain Raphael — forge-brain MCP testé en stdio sur le Cowork d'un PO puis le sien (launcher `mcp-forge-brain/start_stdio.py` créé, `transport="stdio"`). Infirme la note du 1er juin qui sur-généralisait depuis le seul cas HTTP-localhost.
## 2026-06-24 — Veille CC v2.1.179→190 + amendement Agent Teams (équipe implicite)

- **Modifiées** : `01-Claude/Code/changelog/CC juin 2026 - v2.1.160 ultracode.md` — section « AJOUT 24 juin 2026 — v2.1.179 → v2.1.190 » : auto mode bloque git destructif + `terraform/pulumi/cdk destroy` (2.1.183), `sandbox.credentials` (2.1.187), `!` bash auto-respond + `claude mcp login/logout` (2.1.186), foreground subagents plafonnés 5 niveaux (2.1.181), `/config key=value` (2.1.181). Constat loops : aucune nouveauté structurante depuis le 5 juin (que des fixes), [[concevoir-loops-travail]] reste à jour. `derniere-maj` → 2026-06-24.
- **Modifiées** : `04-Techniques/claude-code/agent-teams-natif-anthropic.md` + `01-Claude/Code/features/Agent Teams.md` — amendement v2.1.178 : `TeamCreate`/`TeamDelete` supprimés → équipe implicite (spawn teammate via paramètre `name` du tool `Agent`, `team_name` ignoré). Amendement de la couche mécanisme, pas pivot.
- **Source** : run `cc-news` (veille Claude Code + loops, demande Raphael) — changelog officiel source primaire vérifié (code.claude.com/docs/en/changelog, fetch 24 juin). Chiffres d'aggregateurs écartés (Salesforce 231j→13j, `/loop` 7 jours — non confirmés source primaire).
## 2026-06-24 — Audit ia-workbench post-refonte workflow /spec (modèle Module)
- **Modifiées** : `04-Techniques/patterns/audit-claude-folder-pattern.md` — nouveau Gotcha « refonte interne d'une feature casse l'index de recâblage » (checklist des arêtes : table de routage SKILL.md, préfixe MCP mort, `.mcp.json` résiduel, hook tracker sans cleaner, doc feature périmée). Capitalise les 4 casses trouvées sur ia-workbench.

- **Modifiées** : `1-Projets/ia-workbench/ia-workbench-repo-management.md` — alignée sur le nouveau modèle Jira **Module → 4 familles de Stories (REPO/UX/DevOps/QA) → Sous-tâches** (remplace epic-thème figé) ; references à jour (modules-jira source unique + templates ux/devops/qa) ; décision MCP figée (brain NeoTeem = connector claude.ai, `.mcp.json` ne déclare aucun forge-brain). `derniere-maj` → 2026-06-24.
- **Source** : audit du `.claude/` d'ia-workbench (repo de management hors forge) après refonte du workflow /spec — réparation de 4 casses introduites par l'update : `.mcp.json` (résidu forge-brain), SKILL.md (préfixe MCP mort + table de routage incomplète), hook tracker jamais reset (/spec ne se recommandait plus), doc feature périmée. Détail dans le CHANGELOG d'ia-workbench.

## 2026-06-23 — Cause RÉELLE du faux « pas trouvé » : synonymie marque NEOTEEM=Lojii (fix livré)

- **Modifiées** : `Knowledge/explorations/rag-qualite-source-documentaire-neoia-2026-06-19.md` — Gotcha 7 RÉÉCRIT : la piste « métadonnée pauvre » (écrite le 22) est INFIRMÉE par le diagnostic (summary+keywords contenaient « vote »). Vraie cause prouvée par test discriminant : le grader traite NEOTEEM ≠ Lojii comme deux produits et rejette (même produit). Fix livré documenté : single-source `PRODUCT_NAME_SYNONYMS` (parser+grader+génération), 2 foyers (grep obligatoire), garde-fou 0/N RETIRÉ (inverserait la doctrine d'abstention anti-hallucination), DeepEval double test anti-faux-vert « sur lojii », observabilité avec masquage PII obligatoire (`redact_for_observability`, flag OFF = champ omis, 5 foyers dont error). + Gotcha 6 complété (allowlist PII finale exclut PERSON, pas que MONEY). `derniere-maj` → 2026-06-23.
- **Source** : chantier fix grading agent support neo_ia (PR bug/support-grading-marque-synonymie, 2× APPROVE). Connaissance métier clé : NEOTEEM = Lojii = Vorio = même produit, que tout composant LLM du pipeline doit savoir.

## 2026-06-22 — Gotcha grading faux négatif + trace Langfuse aveugle (RAG support)

- **Modifiées** : `Knowledge/explorations/rag-qualite-source-documentaire-neoia-2026-06-19.md` — « Gotcha 7 — Faux négatif du grading LLM (juge sur métadonnée) + trace Langfuse aveugle » : query « vote extranet » → faux « pas trouvé » alors que la bonne page est au rang 4 ; le grader juge sur métadonnée (pas le contenu) et rejette ; correctifs priorisés (garde-fou anti-0/N > escalade contenu ciblée > revoir exemple canonique) + DeepEval double test ; sous-gotcha = la trace Langfuse a tous les I/O des nodes à null → prouve le chemin pas la cause, reproduire en local.
- **Source** : diagnostic session neo_ia + lecture `grading.py` + trace Langfuse réelle (I/O vides confirmés) — chantier agent support, échéance prod fin juillet.

## 2026-06-22 — Veille LangGraph/LangChain 1.0 + purge chiffres fabriqués

- **Modifiées** :
  - `04-Techniques/chatbot/index-architectures.md` — PURGE des métriques fabriquées rescapées de l'audit 23 mai (routing 94%/91%, latence 4.2s/2.8s, tokens 2800/1900, -33% latence) dans le decision tree ET la matrice par pattern → remplacées par du qualitatif + disclaimer + renvoi [[agents-ia-22-claims-fausses-2026-05-23]]. Règle d'or reformulée (verbatim « is usually enough »). `derniere-maj` → 2026-06-22.
  - `04-Techniques/chatbot/architecture-langgraph.md` — nouvelle section « LangGraph / LangChain 1.0 (GA 22 oct. 2025) — idiome 2026 » : `create_agent` (namespace `langchain.agents`, `langgraph.prebuilt` déprécié) + Agent Middleware (hooks before/after model, HITL/summarization/prompt-caching/retry) + durable execution (label canonique du checkpointing, idempotence, graceful shutdown ≥1.2). `derniere-maj` → 2026-06-22.
  - `04-Techniques/agents/agents-architecture.md` — section dédiée « Deep Agents (Harrison Chase) » (4 piliers : planning-as-tool, subagents isolation contexte, file-system memory, system prompt riche + mise en garde « subagents too soon »). `derniere-maj` → 2026-06-22.
- **Source** : veille `cc-news` ciblée LangGraph/LangChain/agents (confrontée à l'existant forge) avant de figer les références d'un futur skill `document-agent` (neo_ia). Seul angle mort réel = la GA 1.0 d'oct. 2025 ; le reste du corpus agents/RAG/eval/sécu est sain.

## 2026-06-21 — RAG eval : faible rescue ≠ boost inutile
## 2026-06-21 — Chantier couverture RAG support : bilan + pattern re-sync ciblé

- **Modifiées (suite, soir)** : `Knowledge/explorations/rag-qualite-source-documentaire-neoia-2026-06-19.md` — « Gotcha 6 — "C'est déjà neutralisé en amont" ne dispense PAS du filet aval » (critère structurel défense en profondeur : lister ce que la couche amont ne peut PAS couvrir par construction — source Confluence hors contrôle éditorial, entrée utilisateur non filtrée, écritures futures non disciplinées ; allowlist support sans MONEY factorisée dans le package via `mask_pii_entities`).
- **Source (suite)** : arbitrage axe D anti-PII du prompt de génération de l'agent support (chantier dev neo_ia) — décision « filet aval P0 malgré corps de note neutralisés ».

- **Modifiées** : `Knowledge/explorations/rag-qualite-source-documentaire-neoia-2026-06-19.md` — section « Suite empirique — bilan mesuré du chantier » (routing sain/marginal, restitution saine, seul levier = couverture, lexique→Confluence rejeté) + « Gotcha 5 — Re-sync ciblé d'UNE note sans flag dédié » (mini-vault temp + UPSERT idempotent, pas de rebuild).
- **Source** : chantier couverture neo_ia/neoteem-brain (3 trous comblés, lettrage TVA SC-101822 miss→rang 2). Clôture du diagnostic RAG ; reste = audit prompt génération + tests + mesure prod.


- **Modifiées** : `04-Techniques/rag/rag-evaluation.md` — nouvelle section « Faible rescue ≠ boost inutile — séparer les trois causes du no-gain » (gap sémantique / redondance / trou de contenu) ; enrichit le paragraphe « Verdict = rescues vs régressions ».
- **Source** : Bloc 1 du bilan routing support neo_ia (1 rescue / 0 régression sur 7 paires, baseline déjà forte sur les codes d'erreur explicites) → diagnostic = enrichir la couverture, pas toucher au boost.

## 2026-06-20 — Golden set RAG : composition deux familles + anti-fuite in-sample

- **Modifiées** :
  - [[rag-evaluation]] (`04-Techniques/rag/`) — section « Golden set frozen » enrichie : composition deux familles (pannes via tickets hors-sample / usage normal via contenu de pages indexées, mesurées séparément), garde anti-fuite in-sample (`assert lexical_index.match(q) is None` + sourcing hors-sample), verdict rescues vs régressions plutôt que hit@1 quand un boost sature le ranking. 2 pitfalls ajoutés (monoculture pannes, set in-sample tautologique).
- **Source** : chantier RAG Support neo_ia — cadrage du golden set pilote après re-chunk full. Réflexe Raphael « tester aussi l'usage normal, pas que les pannes » (le bot vise un rôle formateur, pas que le SAV).

## 2026-06-19 — Optimisations LLM par provider + dispositif d'agents Neoteem

- **Ajoutées** :
  - [[parametres-echantillonnage-llm]] (`04-Techniques/prompt-engineering/`) — réglages de sampling (temperature/top_p/top_k/penalties/seed) par cas d'usage, qualifiés par provider. 5 gotchas anti-folklore (non-portabilité plage, temp XOR top_p, reasoning verrouille la temp, penalties=0, seed≠déterminisme).
  - [[modes-service-debit-cout-latence-providers]] (`04-Techniques/serving/`) — Batch/Priority/Flex/Scale + provisioned throughput par provider (OpenAI/Azure, Anthropic, Vertex, Bedrock, vLLM). Discriminant : unités de réservation distinctes (Scale units/PTU/GSU+burndown/MU). Gotcha Vertex PT ≈8× on-demand sauf saturation.
- **Modifiées** :
  - [[reference-technique-stack-ia]] — 2 pointeurs vers les deltas NEUFS ci-dessus (comblent le trou « sampling » + « modes de service »).
  - [[Neoteem]] — chiffres agents corrigés (14/14/5 vs 15/11), nouvelle section « Dispositif d'agents Claude Code » (inventaire vérifié des 33 agents des 3 repos : rôle/modèle/effort + patterns transverses), alias `neoyah` ajouté.
- **Source** : demande Raphael — capitaliser les optimisations de réglages IA (sampling) puis les patterns provider (Vertex/OpenAI/Claude/Gemini/Bedrock, provisioning). Recherche web sources primaires (Anthropic/OpenAI/Google/AWS docs), tag VÉRIFIÉ/RAPPORTÉ sur pricing volatil. + note ombrelle Neoteem enrichie depuis l'inventaire disque des agents.

## 2026-06-18 — Critique DA : ia-workbench / spec discovery cross-repo
## 2026-06-18 — Amende limite description skill (modèle troncature CC 2.1.129+)
## 2026-06-18 — Doctrine effort : conflit xhigh résolu (option C)
## 2026-06-18 — Note projet ia-workbench (repo de management + loupe /spec)

- **Ajoutées** : [[ia-workbench-repo-management]] (`1-Projets/ia-workbench/`) — design + décisions figées du repo de management et de sa 1re loupe /spec (source unique du référentiel Jira, read-only strict, taxonomie tests réelle, e2e écarté, effort option C). Complète la critique DA du même jour.
- **Source** : chantier de construction d'ia-workbench (squelette + skill /spec + agent repo-explorer + système mémoire/changelog).

- **Modifiées** : [[conflit-effort-xhigh-anthropic-vs-pivot-22mai]] (QUESTION → résolue, option C) · [[workflow-claude-code-optimal]] (amende « xhigh réservé » périmé).
- **Décision** : xhigh = défaut agentique/coding ; high = comparatif/jugement ; medium/low = extraction ; max = ponctuel. Aligné sur reco Anthropic 2026 (vérif web Opus 4.8) + vécu chantier ia-workbench.
- **Source** : arbitrage Raphael 18 juin, ferme une question ouverte depuis le 26 mai. Canonique = [[effort-opus-47-doctrine-anthropic-2026]].

- **Modifiées** : [[comment-creer-skill]] — AJOUT 18 juin résolvant la contradiction interne (250 vs 1024/1536). Le mécanisme actuel = drop de descriptions entières par récence/fréquence (`skillListingMaxDescChars` + `skillListingBudgetFraction`), plus de troncature uniforme à 250. Viser 200-400 chars trigger-dense.
- **Source** : vérif web MANDATORY pendant la conception du squelette ia-workbench (skill /spec) — docs Anthropic skills + claudefa.st skill-listing-budget.

- **Ajoutées** :
  - [[critique-2026-06-18-ia-workbench-spec-discovery]] (`Knowledge/critiques/`) — verdict devil's advocate sur le repo de management `ia-workbench` et son skill `/spec` cross-repo. 2 BLOCKING (trou d'oracle « 80-90% parfait » sans métrique ; 4e copie du référentiel Jira qui dérive) + 4 IMPORTANT (brain périmé, découpage cross-repo = contrat hallucinable, coût tokens discovery par ticket, dérive orchestrateur). Patterns de fix : oracle binaire + capture verdict humain, source-unique-sync vault.
- **Source** : chantier loop / fiabilisation entrée tickets (session 18 juin). Note : prémisse « on part de rien » de la critique amendée ensuite par Raphael (les `/spec` mono-repo existent déjà et sont finis) → séquence oracle A→B→C abandonnée, mais les angles tests/coût/brain-périmé restent valides pour la conception du `/spec`.

## 2026-06-18 — Doctrine hook : structure d'artefact ≠ workflow agentique

- **Modifiées** :
  - [[comment-creer-hook]] (`04-Techniques/claude-code/`) — AJOUT 18 juin : clarification doctrine 22 mai. Un hook qui vérifie la STRUCTURE d'un artefact (sections d'une PR, frontmatter, message de commit) = quality gate de format AUTORISÉ ; seul le hook qui dicte le DÉROULÉ agentique reste interdit. + corollaire structure (hook) vs contenu (LLM) + gotcha robustesse encodage (normaliser NFKD, pas l'octet emoji).
- **Source** : chantier template de PR neoteem-back-ts + neo_ia (hook `pr-template-guard` déployé sur les 2 repos). J'avais mal appliqué la doctrine en rangeant ce hook côté « workflow » ; vérif état de l'art 2026 (consensus « hooks enforce structure, LLM generates content ») a confirmé qu'il s'agit d'un format gate.

## 2026-06-18 — Warp / Zach Lloyd (analyse 3 tweets X)

- **Ajoutées** :
  - [[Warp]] (`11-Warp/products/`) — ADE Warp 2.0 (4 piliers Code/Agents/Terminal/Drive), Oz (orchestration cloud multi-agents pilotant aussi Claude Code/Codex), benchmarks vérifiés source primaire warp.dev (71% SWE-bench Verified, #1 Terminal-Bench 52%), 3 stades du coding IA, terminal-as-workbench. Nouveau dossier fournisseur `11-Warp`.
  - [[Zach Lloyd]] (`05-Leaders/claude-code/`) — fondateur Warp (ex-Google Docs), thèses « terminal as AI workbench », « coding will be solved → intention humaine = prochain goulot », 3 stades du coding.
- **Source** : analyse de 3 tweets X (0xMorlex sur Agent Skills Anthropic ; addyosmani sur harness/loop engineering ; zachlloydtweets sur Warp). Tweets 1 et 2 déjà couverts (recherche-x-twitter-leaders + AJOUT 16 juin harness-engineering) → aucune action. Tweet 3 = seul vrai gap → 2 notes neuves. Corps des articles X (tweets 2-3) inaccessibles (402) : synthèse basée sur écrits publics des auteurs + vérif primaire warp.dev/Sequoia.

## 2026-06-17 — Gotcha lecture grosse note (read_note_by_path déborde aussi)

- **Modifiées** :
  - [[mcp-vault-llm-design]] (`04-Techniques/patterns/`) — § Lecture grosse note : le débordement tokens vaut aussi pour `read_note_by_path` ; relire le fichier de résultat via `Read` déborde car JSON une ligne ; fallback `head -c` pour le format de tête.
- **Source** : découverte empirique en mettant à jour ce CHANGELOG (~200k chars) pendant le chantier DPO.

## 2026-06-17 — DPO / preference tuning : dérivation + variantes 2026

- **Ajoutées** :
  - [[dpo-derivation]] (`04-Techniques/fine-tuning/`) — dérivation mathématique complète de la loss DPO : objectif RLHF KL-régularisé → Bradley-Terry → reward implicite → annulation de Z(x) → loss sigmoïde. Explique « Your Language Model is Secretly a Reward Model ».
- **Modifiées** :
  - [[fine-tuning-alignment]] (`04-Techniques/fine-tuning/`) — AJOUT 3 sections : variantes DPO 2026 (TDPO 2404.11999, R-DPO 2403.19159, Iterative/Step-wise), nouveautés GRPO 2026 (Dr.GRPO 2503.20783, 2-GRPO 2510.00977, λ-GRPO 2510.06870, GRPO-λ 2510.00194, RLOO 2402.14740), problème du Length Bias (transversal). Warning explicite λ-GRPO ≠ GRPO-λ (papiers distincts).
  - [[fine-tuning-datasets]] (`04-Techniques/fine-tuning/`) — AJOUT section dataset de préférence DPO : construction on-policy (sampling SFT, contrastive selection), pitfalls (skip SFT, LR, epochs, ref model), TRL DPOTrainer.
  - [[MOC-Fine-Tuning]] — pointeur vers dpo-derivation.
- **Source** : recherche web 3 angles (théorie/maths, pratique/production, nouveautés 2026). Tous les arXiv IDs nouveaux vérifiés en source primaire (WebFetch abstracts). Doctrine forge : enrichir l'existant (cluster fine-tuning) plutôt que dupliquer.

## 2026-06-17 — Audit global `.claude/` + enrichissement delegate-guard

- **Modifiées** :
  - [[erreur-subagent-bypass-delegate-guard]] (`Knowledge/erreurs/`) — AJOUT « le bypass n'est plus une env var, c'est `attributionSkill` (session principale UNIQUEMENT) ». Mécanisme delegate-guard changé : sub-agent/teammate insatisfiable, écriture des fichiers protégés en session principale après invocation de la skill créatrice.
- **Source** : audit global config `.claude/` (4 agents parallèles, 0 P0). Découverte empirique pendant l'application des fixes (agents fix-agents/fix-skills bloqués depuis leur position de teammate).

## 2026-06-17 — Doctrine skill de référence (embed-vs-pointer) + critique 4 skills RAG/outils

- **Modifiées** :
  - [[comment-creer-skill]] (`04-Techniques/claude-code/`) — AJOUT « Skill de référence : embarquer le stable, déléguer le volatil ». Arbitrage embed-vs-pointer par volatilité du fait (stable embarqué + tag source ; volatil pointé vers vault, rafraîchi par skill de veille dédiée). Corollaire : séparer référence (consomme) de veille (maintient).
- **Ajoutées** :
  - [[critique-2026-06-17-4-skills-rag-outils-ia]] (`Knowledge/critiques/`) — verdict DA SHIP des skills `cc-rag-ref`/`rag-design`/`choix-outils-ia`/`veille-outils-ia` (0 bloquant ; fix-first collision routage responsable-ia appliqué).
- **Source** : chantier création 4 skills RAG/outils + enrichissement responsable-ia (forge `.claude/skills/`). Tension embed-vs-pointer résolue avec l'advisor, validée par DA.

## 2026-06-17 — Chaîne de conception RAG : data models par cas + audit data amont
- **Ajoutées** :
  - [[rag-data-models-par-cas-usage]] (`04-Techniques/rag/`) — le data model optimal d'un chunk dépend du cas d'usage. Pattern transverse 3 couches (texte embeddé / scalaires pre-filter / payload citation) + 6 patterns de structuration + **8 schémas concrets avec JSON** (maintenance, immobilier/Loji, support FAQ, juridique, e-commerce, médical, code, financier). Le modèle Symptôme→Remède de Raphael confirmé + affiné
  - [[rag-data-audit-discovery]] (`04-Techniques/rag/`) — méthodologie d'audit data EN AMONT : commencer par les QUESTIONS (golden dataset), pas les documents ; grille d'inventaire des sources ; modélisation entités (flat vs graph) ; audit qualité (OCR/dédup/PII/**ACL filtrable**) ; table finding→décision d'architecture. Cadre CODIR = Azure CAF 4-level data-readiness
- **Source** : demande Raphael — (1) data models par type de RAG (exemple maintenance Symptôme→Cause→Diagnostic→Remède) ; (2) « comment fait-on un audit de data » → la chaîne audit→data model→ingestion→récupération→UX. Fan-out de 3 agents. Honnêteté capitalisée : AUCUN « modèle de maturité data-readiness propre au RAG » n'existe (toujours une dimension d'un cadre AI large). 5 IDs arXiv hallucinés par les agents écartés (chiffres supprimés avec leur source non vérifiable) ; les % Anthropic Contextual Retrieval (35/49/67) conservés car primaire vérifié

## 2026-06-17 — Intelligence de code + corrections RAG avancé (vérifiées arXiv)
- **Ajoutée** : [[intelligence-de-code-build-vs-buy]] (`04-Techniques/agents/`) — context engines (SocratiCode, CodeGraph 50k★, Serena, Augment) + revue de code IA (CodeRabbit, SonarQube/Semgrep). Verdict : OSS local gagne sur l'indexation, buy sur la revue, gate déterministe non négociable
- **Modifiées** :
  - [[rag-architecture]] — **4 chiffres corrigés, vérifiés full-text arXiv** (`/html/`) : CRAG (PubHealth 39→75,6 = +36,6 ; le « 78,1% » n'existe pas) · Self-RAG (PubHealth 72,4/74,5, FactScore Bio 81,2/80,2 ; confusion de métriques corrigée) · Adaptive-RAG (3,60× temps vs multi-step 8,81× = ~59% ; classifieur T5-Large 770M ; « 30-50% » pas dans le paper) · GraphRAG (win-rates comprehensiveness 72-83%, PAS « 86% vs 32% multi-hop » = fabrication tierce). + sections LightRAG/nano-graphrag/Neo4j + grille ColBERT-vs-dense
  - [[codebase-maps-pattern]] (section « au-delà de la map statique → context engines ») · [[MOC-paysage-outils-ia-marche-2026]] (catégorie 6) · [[MOC-Techniques]]
- **Source** : demande Raphael — domaine « intelligence de code » (outils qui analysent un repo pour que Claude Code code mieux), SocratiCode cité nommément + RAG avancé (suite). Fan-out de 3 agents. Découvertes : CodeGraph/Serena (leaders OSS que SocratiCode ne dominait pas), 4 chiffres faux dans rag-architecture corrigés à la source. Méthode capitalisable : `arxiv.org/html/<id>` est parsable (tables vérifiables), contrairement à `/abs/`.

## 2026-06-17 — Paysage outils IA marché : voix, briques produit (build-vs-buy)
- **Ajoutées** :
  - [[MOC-paysage-outils-ia-marche-2026]] (`00-Hub/`) — MOC parent : cartographie marché 5 catégories (voix, briques, productivité, infra/LLMOps, plateformes), angle build-vs-buy + adoption
  - [[outils-voix-ia-build-vs-buy]] (`04-Techniques/voix/`) — TTS/STT/agents vocaux ; build-vs-buy par brique (TTS=buy, STT=build viable, agents=buy-POC-puis-build) ; flags PlayHT mort + XTTS piège licence + EU AI Act
  - [[briques-produit-ia-build-vs-buy]] (`04-Techniques/rag/`) — OCR/embeddings/reranking/modération/RAG-aaS/extraction ; 2 piles Loji (buy rapide vs souveraineté FR self-host)
- **Modifiées** :
  - [[rag-embeddings]] — **2 corrections de pricing vérifiées source primaire** : voyage-3-large $0,18/M (pas $0,06 — le $0,06 est le nouveau voyage-4) ; Gemini embedding-001 $0,15/M (pas $0,006, erreur ×25). + ajout voyage-4
  - [[MOC-Techniques]] (section « Paysage outils IA marché ») · [[outils-memoire-rag-gouvernance-juin-2026]] (lien vers le MOC parent)
- **Source** : demande Raphael — outils IA du marché (gratuits ou payants-très-forts), voix (TTS/robots vocaux) cité comme exemple phare, angle « mieux que développer à la main ». Fan-out de 5 agents web. M&A vérifiés relevés : Humanloop MORT (Anthropic, sept. 2025), Langfuse→ClickHouse, Promptfoo→OpenAI, Portkey→Palo Alto.

## 2026-06-17 — Recherche 5 outils : mémoire agent, vector DB, RAG entreprise, gouvernance contexte
- **Ajoutées** :
  - [[memoire-agent-mem0]] (`04-Techniques/agents/`) — couche mémoire universelle ; flag du pivot v3 (avril 2026, OSS sans graphe traversable vs Platform)
  - [[memoire-agent-langmem]] (`04-Techniques/agents/`) — SDK LangChain-native, mémoire procédurale ; statut 0.0.30 figé
  - [[onyx-enterprise-search]] (`04-Techniques/rag/`) — plateforme RAG entreprise open-source ; flag Vespa→OpenSearch v4.0 (mai 2026)
  - [[pinecone-vector-database]] (`04-Techniques/rag/`) — vector DB serverless en profondeur (RU/WU, Inference, Assistant)
  - [[packmind-context-governance]] (`04-Techniques/agents/`) — gouvernance de contexte agents de code (ex-Promyze) + croisement doctrine cross-repo forge
  - [[outils-memoire-rag-gouvernance-juin-2026]] (`00-Hub/`) — note-hub d'orientation (3 catégories, pas un versus)
- **Modifiées** : [[rag-vector-databases]] (ligne Pinecone rafraîchie + liens) · [[agents-architecture]] (§ Memory : frameworks mem0/LangMem) · [[MOC-Techniques]] (entrées RAG & Agents)
- **Source** : demande Raphael — recherche approfondie sur mem0, LangMem, Onyx (onyx.app), Pinecone, Packmind (packmind.com). Fan-out de 5 agents web (site officiel + GitHub + retours d'usage), sources primaires distinguées du rapporté, faits volatils horodatés.

## 2026-06-16 — Veille cc-news + amende doctrinale sous-agents imbriqués (v2.1.172) + mémoire CC/Cowork
- **Modifiée** : [[relais-inter-agents-fiable]] — ajout de DEUX sections actionnables pour les futurs repos : (1) « Le maillon read-only : contrat de sortie de l'architect » (fuite « plan dans message intermédiaire → dev re-décide », parade « dernier message = livrable » + dispatch, sans jamais ouvrir Write ; déployé architect-deep neo_ia + architect back-ts) ; (2) « Déployer le relais /feature sur un NOUVEAU repo — méthode » (recette 6 étapes éprouvée : lire les formats réels avant de trancher / vérifier l'état git + .gitignore / grep REPO-WIDE / adapter pas copier / read-only préservé / cleanup sélectif). **Source** : demande Raphael « tout est-il dans tes notes pour qu'un futur repo soit top ». Le design était capitalisé, la MÉTHODE de déploiement ne l'était pas — manque comblé (search-then-enrich, foyer = le hub, pas de note orpheline). Lien croisé ajouté vers [[pattern-spec-skill-deployment]] (méthode sœur).
- **Modifiée** : [[relais-inter-agents-fiable]] — statut du registre léger passé de « hypothèse non éprouvée » à **« déployé sur neo_ia + neoteem-back-ts, à observer avant promotion canonique »** (≠ validé). Ajout d'une section « Relais intra-/feature » documentant le déploiement : fichier-relais unique sectionné `.tmpclaude/feature-notes/<slug>.md` (gitignoré, éphémère, 6 sections Objectif/Déjà fait/Décisions/Déviations/État/Next), persisté par la SESSION (read-only jamais touchés ; dev/test-writer déjà-writer peut écrire sa section), lecture ciblée par section, frontière cross-repo = ticket Jira, cleanup sélectif au /ship. **Source** : chantier « relais inter-agents /feature » (neo_ia 10 fichiers + neoteem-back-ts 11 fichiers, sur develop ; aucun frontmatter agent touché ; 0 pointeur-relais résiduel repo-wide vérifié).
- **Ajoutée** : [[relais-inter-agents-fiable]] (`04-Techniques/agents/`) — note-hub MINCE sur le relais inter-agents (3 fuites : perte verticale / redondance horizontale / coût de relecture). Ne re-rédige rien : pointe vers les 4 foyers existants ([[multi-agent-handoff-loss-pattern]], [[pattern-mcp-brief-then-direct]], [[software-factory-pattern-2026]] + skill `/spec` TODO/, [[workflow-claude-code-optimal]]). Verdict ÉTAPE 2 : forge ne fuit PAS matériellement (fan-out parallèle = 0 handoff chemin critique ; escalade-vers-central ; brief-then-direct couvre la transmission) → doctrine générale, pas correctif. Seul net-neuf = le **registre léger**, sorti en hypothèse `memory/feedback_registre-relais-agents` (non éprouvé → pas canonisé, à valider 2-3 cas). 8/8 wikilinks vérifiés avant création (zéro lien mort).
- **Enrichissement [[mcp-alias-ambigu-chemin-exact]]** (gotchas outillage vécus en session) : workaround écriture corrigé « Read+Edit disque » → variantes `*_by_path` (l'Edit disque désync l'index SQLite, cf [[vault-edit-gotchas-outillage]]) ; nouveau gotcha **`read_note_by_path` n'a PAS de pagination** (`offset`/`limit_chars` seulement sur `read_note`) → mur sur note massive à stem ambigu (CHANGELOG 190k chars) + 3 workarounds (alias unique paginé / marker + `insert_section_by_path` / parse du tool-result `.txt` avec `reconfigure utf-8`).
- **Audit `.claude/` forge (3 lentilles : sous-agents imbriqués / mémoire / contexte)** : enrichissement de [[technique-shared-agent-memory]] avec un volet **Cowork** (project Instructions ≠ CLAUDE.md, zéro hooks → MCP remote HTTPS, écriture vault headless impossible — ponts vers [[cowork-skills-reliability]] et [[cowork-write-vault-headless-impossible]]). Côté `.claude/` (non-vault, hors CHANGELOG) : correction de cibles mémoire mortes (`≤100 fichiers` → plancher ~240 / WARNING 250 / CRITICAL 290 du hook `memory-saturation-watcher`) dans `skills/done` + `rules/memory-discipline` ; prémisse sous-agent périmée corrigée dans `skills/loop-forge` ; références mortes `vault-consultation-protocol`→`forge-brain-proactive` et `agent-creator`→`subagent-creator` dans `agents/code-dev` + `agents/self-updater`.
- **Complétude drift résiduel (16 juin, suite)** : correction des « vitrines » qui portaient encore la prémisse périmée malgré les amendes en bas de note — gloses index [[MOC-Techniques]] et [[pattern-mcp-brief-then-direct]] (analogie « ne peut pas invoquer Agent » cassée) + corps amont de [[anti-reentrance-sub-agents-pattern-escalade]] (bandeau de tête + sections QUOI/WORKFLOW nuancées : « interdit » → « déconseillé par défaut, possible depuis v2.1.172 »). Discriminant appliqué : une glose qui *asserte* l'impossibilité = drift à corriger ; une glose qui *décrit* une « limitation contextuelle » (MCP décoratif, coût) = vraie, laissée intacte.

- **Ajoutées** : `04-Techniques/claude-code/recursive-language-models-rlm.md` (RLMs, arXiv 2512.24601) ; `01-Claude/models/Fable 5.md` (modèle classe Mythos, suspendu export-control 12 juin).
- **Modifiées (amende doctrinale — prémisse « sous-agents ne peuvent pas s'imbriquer » périmée depuis CC v2.1.172)** : `anti-reentrance-sub-agents-pattern-escalade` (AJOUT 16 juin : possible mais escalade reste défaut + section opérationnelle « ce qu'on peut faire ») ; `limites-subagents-claude-code` (méthode d'audit `grep ^tools:` corrigée — un agent qui omet `tools:` hérite Agent et nest) ; `comment-creer-agent` (table de capacités corrigée, source amont du claim).
- **Modifiées (mémoire CC + Cowork)** : `technique-shared-agent-memory` (section `memory:` frontmatter agent 3 scopes + diagnostic « CC ne retient rien » + recette repos) ; `technique-dreaming-cross-session` (3 modèles supportés, « 97% Rakuten » flaggé non confirmé → 79% TTM primaire) ; `Memory Managed Agents` (`/mnt/memory/`, read_write/read_only, caps, 30j version history, Vaults ≠ memory).
- **Enrichie** : `04-Techniques/agents/harness-engineering.md` (carte diagnostic Osmani, coût primaire 4×/15× Anthropic, Loop Engineering, lien pivot 22 mai). Doublon `04-Techniques/claude-code/harness-engineering.md` créé par erreur puis supprimé (search_brain initial trop étroit).
- **Changelog CC** : `CC juin 2026 - v2.1.160 ultracode` enrichi (v2.1.161→178 : Fable 5, sous-agents imbriqués, `Tool(param:value)`, `--safe-mode`/`/cd`, Stop hook additionalContext).
- **Composant `.claude/`** : `subagent-creator` SKILL.md L278 corrigée (nesting possible, via skill-creator). Memory : feedbacks `amende-vs-pivot-couche-factuelle-design`, `ccnews-structure-vault-provider-drift`, MAJ `anti_reentrance_sub_agents`.
- **Source** : run cc-news 16 juin 2026 (16 agents parallèles + Tier 0), sources primaires code.claude.com / platform.claude.com / anthropic.com vérifiées ; chiffres d'agrégateurs flaggés non confirmés.
## 2026-06-11 — Gotcha SubagentStop transcript (comment-creer-hook)

- **Modifiées** : [[comment-creer-hook]] — AJOUT « SubagentStop : scanner le TRANSCRIPT, jamais les champs du payload » (escalade-detector neo_ia n'a jamais rien détecté du 24 mai au 11 juin : il scannait les champs payload et le CHEMIN du transcript au lieu de son contenu ; fix porté py + ts, test = faux transcript avec marqueur).
- **Source** : chantier alignement neo_ia ↔ neoteem-back-ts (vagues 1-3).

## 2026-06-10 — Audit complet neoteem-back-ts 18/20 + état projet rafraîchi

- **Modifiées** : [[neoteem-back-ts]] — section « État (2026-06-10 soir) » : audit 7 axes noté 18/20 (plafond = preuve par l'exécution), optimisations livrées toutes branches (afae512 : /go+pnpm audit, ADR-002 RFC 9457, CDC §13 brouillard comptable, @AGENTS.md standalone, compteurs README), résidu branche US1 (relations.ts symboles inexistants), dettes P2.
- **Source** : audit 3 agents (repo-inspector .claude/ ; vérif empirique code develop+us ; recherche web état de l'art Drizzle/TS6/Stryker/supply-chain) croisé CDC v5.0 + NeoBrain (glossaire, ADR-001→005, conventions BDD) + canoniques forge.

## 2026-06-10 — Organisation par domaine métier + limite 1000 lignes (suite incident US1)

- **Modifiées** : [[conventions-naming-typescript]] — AJOUT « Organisation par DOMAINE métier + limites de taille » (vertical slice × hexagonal vérifié web ; domaines issus du métier RÉEL via neoteem-brain : Damier Lojii + 01-Domaines + MOC-BDD → commun/syndic/gerance/comptabilite/reporting ; limite stricte 1000 lignes triple capteur ; méthode réutilisable : interroger le brain AVANT d'inventer une taxonomie).
- **Source** : arbitrages Raphael post-US1 (granularité, pas réduction de périmètre ; fichiers logiques ; « mass tables » à venir) + recherches NeoBrain (glossaire, MOC-Domaines, MOC-BDD). Déployé : back-ts 59ee16c (conventions § 2bis, CDC §6.1+§7.3, rule file-size-limit, hooks file-size-guard + guard-ts-nocheck, architect/skills câblés).
## 2026-06-10 — Incident US1 artefacts générés : Default-FAIL ne prouve que les critères écrits

- **Modifiées** : [[workflow-claude-code-optimal]] — AJOUT « Incident US1 : le Default-FAIL ne prouve que les critères ÉCRITS » (37 tables générées pour 17 attendues, pipeline vert contre un contrat troué ; règles : liste fermée + assertion de comptage = critère de done standard des artefacts générés, review du GÉNÉRATEUR, @ts-nocheck = hook bloquant allowlisté).
- **Source** : 1er /feature réel neoteem-back-ts (us/N2-111279), diagnostic empirique (schema.test.ts n'assertait que G4). Déployé : back-ts a21dbc8 (hook guard-ts-nocheck testé 8/8 + 6 composants) + templates ×3 repos.
## 2026-06-10 — Placement des checks par event + vérifs par lots (incident lenteur US1)

- **Modifiées** : [[comment-creer-hook]] — AJOUT « Répartition des checks par event » (PostToolUse = format rapide < 500 ms ; typecheck/tests = Stop UNIQUEMENT avec decision:block ; coûts spawn interpréteur mesurés python 236 ms / py 454 ms / uv run 450-640 ms, additifs sur matchers larges ; gotcha git diff rate les untracked) ; [[comment-creer-agent]] — AJOUT « Agents dev : vérifications par LOTS » (jamais après chaque fichier, jamais de lint manuel si hook PostToolUse formate).
- **Source** : incident US1 neoteem-back-ts (~1h30, relances en boucle) + audits 3 repos + vérification web (Boris howborisusesclaudecode.com, Wiegold hooks, Pixelmojo). Appliqué : back-ts d3b4e20, neo_ia 17fa987.
## 2026-06-10 — Relance sub-agent après escalade (resume ou re-brief)

- **Modifiées** : [[anti-reentrance-sub-agents-pattern-escalade]] — AJOUT « La RELANCE après escalade : resume ou re-brief, jamais un prompt nu » (resume officiel CC ≥ 2.0.28 + bugs #11712/#33651, re-brief riche en filet, principe « la session principale injecte le contexte, l'agent ne le re-cherche pas »). Déployé : rule `agent-relaunch-context` (forge + neoteem-back-ts), § Relance dans `sub-agent-patterns` (neo_ia), formats d'escalade des 6 agents back-ts enrichis (État actuel + Suite recommandée).
- **Source** : observation production US1 neoteem-back-ts (le dev refaisait toutes ses recherches à chaque aller-retour escalade) + recherche web (docs Agent SDK subagents, issues GitHub #11712/#33651, PubNub best practices).
## 2026-06-10 — Harness design long-running apps (2e article Anthropic)

- **Modifiées** : [[workflow-claude-code-optimal]] — AJOUT 10 juin : Planner/Generator/Evaluator (GAN), Default-FAIL contract, sprint contracts, context anxiety vs resets, principe de simplification itérative du harness, evaluator tuning loop + application neoteem-back-ts (audit harness ~85 % conforme, 4 manques nocturne)
- **Source** : recherche harness agents autonomes pour neoteem-back-ts (demande Raphael confiance 80-90 %) — anthropic.com/engineering/harness-design-long-running-apps + effective-harnesses + Fowler/Osmani/Trail of Bits
## 2026-06-10 — Conventions nommage TS + patterns (chantier conventions neoteem-back-ts)

- **Ajoutées** : [[conventions-naming-typescript]] (`04-Techniques/stacks/`) — table canonique Google/typescript-eslint/Biome, enforcement mécanique `useNamingConvention`+`useFilenamingConvention` (vérifié positif ET négatif), verdict patterns hexagonal (CDC §6ter conforme Sairyss/Stemmler, GoF adaptés anti-cérémonie : static factory method, Strategy = map de fonctions).
- **Modifiées** : [[neoteem-back-ts]] — resume corrigé (« un MCP par domaine déployé une fois par client », jamais « un MCP par client » — correction Raphael).
- **Source** : chantier conventions + design patterns neoteem-back-ts (doc/conventions.md créé, biome.json enforce, rule + reviewer câblés).
## 2026-06-10 — AGENTS.md verbatim officiel (audit 200% neoteem-back-ts)

- **Modifiées** : [[comment-ecrire-claudemd]] — sous-section « AGENTS.md — précision officielle » : « Claude Code reads CLAUDE.md, not AGENTS.md » + 3 intégrations (import @AGENTS.md recommandé Windows, symlink, /init) + commentaires HTML block-level strippés avant injection.
- **Source** : audit 200 % du `.claude/` neoteem-back-ts par les skills créatrices, croisé doc officielle code.claude.com/docs/en/memory. Cas réel : AGENTS.md du repo seulement mentionné en texte → jamais chargé, corrigé par import.
## 2026-06-09 — Note projet neoteem-back-ts (E0 livré, E1 proposé)

- **Ajoutées** : [[neoteem-back-ts]] (`1-Projets/Neoteem/neoteem-back-ts/`) — folder-note projet : stack monorepo TS, décisions gravées (règle de tri PG §7.2, moteur `requete.*` 4 fonctions raw définitif, parité stricte, ia_back = comportement jamais modèle, scope étanche ws/WinDev), outillage `.claude/` complet (hooks `agent_id`, skill-activation porté, /go miroir CI), état E0 livré + E1 en attente OK parent.
- **Modifiées** : [[ia_back]] — section « Migration vers le monorepo TS » (source de la migration, chiffres réels, repo à terme archivé).
- **Source** : livraison E0 + perfection `.claude/` neoteem-back-ts (session 9 juin 2026).
## 2026-06-09 — Méthode de chasse aux méta-notes (livrable « au présent pur »)

- **Modifiées** : [[critique-2026-05-24-meta-commentaires-doctrine]] — ajout section « Méthode de chasse aux méta-notes ». Confirme empiriquement l'AVERTISSEMENT 1 de la note (« test lexical rate les méta-cachés ») : un grep prouve l'orientation, jamais l'absence de méta-note. Les méta-notes se cachent dans les sections RÉDIGÉES pendant la session courante → relecture sémantique obligatoire. 4 patterns à traquer + frontière méta-note vs justification-au-présent.
- **Source** : finalisation du CDC `neoteem-back-ts`. Un advisor a pointé 2 sections (propres) ; la lecture sémantique guidée a trouvé 2 vraies méta-notes ailleurs (§7.2 « Cible reformulée X→Y », « ancienne doctrine PG-first ») ratées par le grep ET par l'advisor.

## 2026-06-09 — Affinage anti-pattern hooks (action vs séquence) — projet neoteem-back-ts

- **Modifiées** : [[anti-pattern-hookify-workflow-hooks]] — ajout section « Critère discriminant net : ACTION ponctuelle vs SÉQUENCE d'étapes ». Explicite pourquoi `delegate-guard` (bloque une écriture) est conforme alors qu'un `architect-first` ne l'est pas — la frontière « sécurité/destructif » seule ne classait pas ce cas. Reformulation : hooks = déterministe (blocage d'action), skills+agents = probabiliste (jugement).
- **Source** : session de spec du monorepo `neoteem-back-ts` (epic Fondation E0). Raphael a challengé la formulation « hooks jamais de workflow agentique » → affinage du critère. Confirmé par état de l'art hooks 2026 + lecture `delegate-guard.py`.

## 2026-06-09 — Dossier MCP « construire des serveurs MCP parfaits » (recherche source-primaire)

- **Ajoutées (5 notes, nouveau sous-dossier `04-Techniques/mcp/`)** :
  - [[MOC-MCP]] — point d'entrée du dossier (5 décisions structurantes, gotcha sujet volatile).
  - [[mcp-tool-design-scaling]] — **note cœur** : design des tools (JSON Schema, annotations readOnly/destructive/idempotent/openWorld, descriptions = 3-4× moins d'échecs) + les 4 réponses 2026 au problème « trop de tools » (Code Execution -98,7 %, Tool Search Tool -85 %, Dynamic Tool Discovery GitHub, Codemode Cloudflare).
  - [[construire-mcp-production]] — recipe TS + Python à parité (protocole, 3 primitives, transports, SDK FastMCP 3.0 GA / @modelcontextprotocol/sdk, structure projet, maintenance/debug MCP Inspector + OpenTelemetry + versioning). Snippets = pattern durable + lien doc canonique.
  - [[mcp-securite-oauth-remote]] — OAuth 2.1 Resource Server, confused deputy, token passthrough INTERDIT, RFC 8707, lethal trifecta (Willison), patterns Cloudflare (workers-oauth-provider, Access, portals).
  - [[mcp-multi-client-claude-chatgpt-gemini]] — support réel Claude/ChatGPT/Gemini juin 2026 (ChatGPT remote-only pas de localhost, Streamable HTTP commun, MCP vs A2A Google).
- **Modifiées (2 notes, enrichies sans réécriture)** :
  - [[mcp-vs-skills-doctrine]] — section « AJOUT 9 juin 2026 » : statuts à jour (spec 2025-11-25, RC 2026-07-28, FastMCP 3.0 GA, gouvernance Linux Foundation) + pointeurs vers le nouveau dossier.
  - [[reference-technique-stack-ia]] — section 4.6 enrichie : RC 2026-07-28 (stateless, JSON Schema 2020-12), FastMCP 3.0 GA, renvoi [[MOC-MCP]].
- **Source** : demande Raphael « recherches ultra poussées sur les MCP — comment les meilleures entreprises créent des MCP ». Recherche vérifiée sur sources primaires (état juin 2026, post-cutoff) : modelcontextprotocol.io/specification/2025-11-25, blog Anthropic Code execution with MCP, docs Cloudflare/OpenAI/Google, github.com/github/github-mcp-server, github.com/PrefectHQ/fastmcp. Cible = référence générale réutilisable, TS+Python à parité.

## 2026-06-07 — Chantier 6-B pièce 1 (DEV MCP) — write-by-path + gotchas cycle de vie

- **Modifiées** : `04-Techniques/claude-code/ajouter-source-donnees-mcp-forge-brain.md` — section Tests enrichie d'un gotcha « couche wrapper `register_tools` non exercée si tests appellent `BrainTools` direct » (renvoi `memory/reference_mcp_forge_brain_lifecycle_gotchas.md`).
- **Source** : ajout des 4 outils `*_by_path` au serveur MCP forge-brain (Chantier 6-B pièce 1, commits `e50031d` + `fb69441`). Refactor en cœur partagé `_*_core(path,...)` → la variante by-path hérite du fix EOL 6-A. 205 tests verts. Le reste du chantier (preuve-prod live + hook anti-contournement + réécriture des 2 messages-pièges) est tracé dans `context-actuel` pour une session de reprise (restart MCP = kill port 8091 + nouvelle session).

## 2026-06-07 — Chantier 6-A & 6-C (DEV MCP) — écriture vault conforme par construction

- **6-A — fix EOL `newline=""` étendu aux 4 outils restants** (commit `63a8f66`). Le fix #2 n'avait couvert que `update_property`/`bulk` ; `update_note`/`insert_section`/`append_note`/`move_note` traduisaient encore LF→CRLF à l'écriture (166 notes LF du vault exposées au diff full-file). `insert_section` : 2 corrections induites (rstrip `\r\n` du marker, EOL aligné du content inséré) sinon le matching cassait sur les 301 notes CRLF. Doctrine EOL unifiée : l'appelant est seule autorité EOL, la couche IO ne traduit jamais. 11 tests régression EOL live byte-exact.
- **6-C — validation `create_note` (partition block-dur / warn-only)** (commit `4758671`). Conformité du contenu validée côté serveur MCP (source unique), AVANT écriture (refus = rien sur disque). BLOCK : frontmatter absent · BOM en tête · YAML invalide · double clé `aliases` (regex dédié importé de l'indexer — `yaml.safe_load` est aveugle, PyYAML garde le dernier en silence). WARN-ONLY : aliases<4 · aucun tag · wikilink→inexistant (forward-refs roadmap G1 sains, jamais bloqués ; tolérance memory/ `feedback_`/`reference_` gardée). 16 tests. Le block BOM attrape `bom-skillmd` à la source.
- **Bilan** : 188/188 tests verts, zéro régression. Trou B (write-by-path + hook anti-contournement) tracé séparé (changement d'archi, pas ce soir).
- **Modifiée (1 note)** : [[erreur-mcp-yaml-dump-corruption]] — addendum inventaire EOL complet des 4 outils (6-A) + statut BOM désormais exploité comme garde (6-C).
- **Source** : Chantier 6 du plan vault forge-brain (garantir l'écriture vault conforme).

## 2026-06-07 — Chantier 5/5 (DEV MCP) — CLOS

- **Limite #1 RÉSOLUE** (besoin prouvé) : `lint_vault` accepte `limit=0` (illimité) + sélecteur `category`. Validé en prod (89 wikilinks brisés en entier vs 50 tronqués). Commit `490d9fa`.
- **Limites #3 et #4 DOCUMENTÉES** comme limites connues (théoriques, non codées — doctrine « coder les besoins prouvés, documenter les théoriques », leçon Ch.4) :
  - **Créées (2 notes)** : [[limite-mcp-lock-inter-ecritures]] (race théorique sur écritures concurrentes — non codé car usage solo séquentiel ; déclencheur = multi-agent parallèle) et [[limite-mcp-lag-reindexation-agregats]] (lag agrégats poll 30s, non lié aux edits prouvé Ch.3 — géré par git diff pas compteur ; déclencheur = usage compteur temps-réel).
  - **Modifiée** : `00-Hub/MOC-Techniques.md` — section « Limites connues MCP forge-brain » ajoutée.
- **Bilan Chantier 5** : 2 besoins prouvés traités (#1 pagination, #2 array-safe) + 2 théoriques documentés (#3 lock, #4 lag) + multi-hop `traverse_graph` écarté (pas de consommateur). Pas « 6/6 codés pour le principe ».
- **Source** : clôture du Chantier 5/5 du plan vault.

## 2026-06-07 — Test de prod du fix array-safe (serveur MCP redémarré)

- **Serveur MCP redémarré** sur le code à jour (commit `2ff0538`) → 1er test de `update_property` array-safe en production réelle (client MCP → serveur → splice → disque).
- **Modifiées (2 notes)** : [[decision-byte-for-byte-splice-test-live]] — `aliases` étendu via array MCP (7 items, **zéro orphelin**, champs voisins intacts) = preuve de prod du splice array. [[erreur-mcp-yaml-dump-corruption]] — `resume` corrigé (scalaire) : l'ancien « update_property/bulk inutilisables sur array » devenu faux → acte la résolution.
- **Validé** : splice array-safe + scalaire fonctionnent de bout en bout en prod, sans corruption ni reformatage collatéral.

## 2026-06-07 — Raisonnement caché : écriture byte-for-byte (splice + test live)

- **Créée (1 raisonnement)** : [[decision-byte-for-byte-splice-test-live]] (Knowledge/raisonnements/) — chaîne décisionnelle réutilisable issue du fix limite #2 : (1) splice > re-dump (toute ré-sérialisation globale viole le byte-for-byte par construction → disqualifiée a priori) ; (2) insight méta : un diff mémoire « chirurgical » ment sur l'IO, `splitlines()`+`difflib` aveugle aux conversions EOL → test live byte-exact non négociable.
- **Modifiée** : `00-Hub/MOC-Techniques.md` — wikilink ajouté sous « Raisonnements cachés ».
- **Source** : /reasoning-cache post-fix chantier 5 limite #2. Détails du bug → [[erreur-mcp-yaml-dump-corruption]].

## 2026-06-07 — Chantier 5/5 (DEV MCP) — limite #2 RÉSOLUE : `update_property` array-safe

- **Modifiée (1 note Knowledge)** : [[erreur-mcp-yaml-dump-corruption]] — section « RÉSOLU 2026-06-07 » ajoutée. Les sections « NON corrigé côté outil » / contournement script Python obligatoire sont actées **périmées** à partir du commit `2ff0538`. `update_property`/`bulk_update_property` sont maintenant utilisables sur les arrays (tags/aliases/sources).
- **Code serveur MCP** (hors vault, commit `2ff0538`) : `update_property` réécrit en **splice chirurgical** (helper pur `_set_property_in_frontmatter`, remplace le span complet de la propriété, jamais `yaml.safe_dump`) + **IO byte-exact** (`read_text`/`write_text` `newline=""`). 2e bug découvert au test live : `write_text` convertissait les **166 notes LF** du vault en CRLF (diff full-file) → bug **actif**, corrigé. Signature `value: str | list[str]` (FastMCP transmet les list nativement, prouvé). 17 tests dédiés, 155/155 suite complète verte. Gate Raphael « zéro diff collatéral » respecté.
- **Découvertes annexes hors-scope** (notées, non corrigées) : `parse_note` ignore le frontmatter d'une note à BOM-en-tête (0 note affectée) ; `append_note` partage le pattern de traduction EOL.
- **Statut Ch.5** : limite #2 close. Restent #1 `lint_vault` non paginé, #3 lock inter-écritures MCP, #4 lag réindexation agrégats.
- **Source** : Chantier 5/5, limite #2 (3 incidents corruption YAML subis).

## 2026-06-07 — Système de coaching Lead IA — structure légère (2 notes vides)

- **Créées (2 notes, vides de contenu)** : `2-Casquettes/responsable-ia/coaching/index.md` (pilote de la boucle : conseil → terrain → capture, règle de capture des boucles complètes uniquement, double axe de tags `#theme` × `#boite`, apprentissage à 2 niveaux contextuel/transférable) et `2-Casquettes/responsable-ia/coaching/retours.md` (journal append-only, format en en-tête, zéro entrée).
- **Objectif** : remplacer un dump théorique de 41 notes par un système de coaching dont le vault est la mémoire — les notes se remplissent du vécu terrain réel de Raphael au fil des boucles, recentré « parcours de carrière Lead IA » (pas seulement la boîte actuelle).
- **Wikilinks vérifiés avant écriture** (anti lien-cassé) : hubs `management/index`, `communication/index`, `strategie/index` confirmés existants ; lien vers la casquette désambiguïsé en `responsable-ia` (stem `index` partagé 13×) ; résolution validée par get_backlinks (0 lien cassé).
- **Source** : demande Raphael — système de coaching collaboratif plutôt que rédaction théorique anticipée.

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


## 2026-06-08 — Drift d'implémentation Karpathy constaté (vérif empirique)

- **Modifiées** : `04-Techniques/claude-code/pattern-vault-llm-karpathy.md` — nouvelle section « DRIFT D'IMPLÉMENTATION CONSTATÉ — 8 juin 2026 ». Documente l'écart doctrine↔réel : `raw/` abandonné depuis le 22 mai (8 notes figées), `index.md` stale +51% (annonce 318 notes vs 480 réelles), Query keyword-only (search_brain BM25 pur, 0 vectoriel/rerank, 1237 appels/30j = outil n°1). Réparations par ROI + méta-leçon « un système qui marche malgré un organe mort cache son drift ».
- **Source** : comparaison forge-brain vs pattern Karpathy LLM Wiki (demande Raphael). Vérif empirique via `vault_stats`, `usage_stats(30j)`, `list_notes("raw")`, lecture `index.md`/`log.md` racine.


## 2026-06-08 (suite) — Requalification post-mesure des écarts Karpathy

- **Modifiées** : `04-Techniques/claude-code/pattern-vault-llm-karpathy.md` — section « REQUALIFICATION POST-MESURE » (append, analyse d'origine conservée). Diagnostic de décision sur critère tokens/perf réelle (mesures `usage.jsonl` 30j) : ② retrieval vectoriel = bilan tokens NÉGATIF, vrai ratage BM25 0,89% non-sémantique → écart assumé ; ① raw/ = 0 accès/30j, besoin fiabilité non matérialisé → écart assumé. Les deux avec trigger de réouverture. #3 index.md hors périmètre (non mesuré).
- **Source** : demande Raphael — décider chaque écart sur tokens/perf, pas conformité au pattern. Méta-leçon : « dévier du pattern ≠ avoir un problème » (symétrique de « valoriser ≠ consommer »).


## 2026-06-09 — Régénération index.md racine (organe Karpathy "lu en premier")

- **Modifiées** : `index.md` (racine) — régénéré depuis l'inventaire réel du vault. Corrige le stale +51% (annonçait 318 notes, en compte 480). Reste content-oriented (par « si tu cherches X »), pas un dump : l'exhaustif est délégué aux `_index` de sous-dossiers (erreurs/raisonnements/critiques). Ajouts : section PATTERNS technique (27 patterns + claude-code), doctrine post-22mai enrichie, 80 leaders par sous-domaine, features/changelog `01-Claude/` à jour, métadonnées réelles + mention du drift arbitré le 8 juin.
- **Source** : geste #3 du diagnostic drift Karpathy (8 juin) — le seul des 3 écarts qui était un geste mécanique légitime (les 2 autres requalifiés en écarts assumés).

## 2026-06-14 — Déclencheur ré-audit BM25-vs-embeddings (analyse vidéo Obsidian+Claude)

- **Modifiées** : [[pattern-fts5-aliases-vs-embeddings]] — section « Trajectoire & déclencheur de ré-audit » (vault 187→487 notes, seuil 1000 ; déclencheur = 1000 notes OU 2-3 ratés synonyme récurrents ; drop-in pré-conçu = `synonyms.yaml` query-time ~40L sans réindexation, embeddings en dernier recours)
- **Source** : croisement de la vidéo « Obsidian + Claude 4.7 » (IA Talkshow) avec le setup vault+MCP. Verdict : forge fait déjà l'essentiel (BM25 FTS5 + retrieval-as-tool + payload court) ; fossé sémantique latent non actif → capitalisation du déclencheur plutôt que feature spéculative (measure-before-optimize).

## 2026-06-14 — Réorg vault : fournisseurs IA en dossiers premier niveau (dissout Concurrents + Modeles)

- **Déplacées** (12 notes, via `git mv` — renames, historique préservé, wikilinks intacts car résolus par nom) :
  - Modèles Anthropic (Opus 4.7, Sonnet 4.6, Haiku 4.5, claude-mythos-preview) → `01-Claude/models/`
  - OpenAI : GPT-5.5 → `02-OpenAI/models/`, Codex → `02-OpenAI/products/`
  - Google : Gemma 4 → `03-Google/models/`, Gemini CLI → `03-Google/products/`
  - xAI : grok-code-fast-1 → `08-xAI/models/`, Grok → `08-xAI/products/`
  - Cursor → `09-Anysphere/products/`, GitHub Copilot → `10-Microsoft/products/`
- **Supprimés** : dossiers `02-Concurrents/` et `03-Modeles/` (dissous)
- **Architecture** : squelette par fournisseur = `models/` + `products/` (créés à la demande). 2 axes : ACTEUR (par fournisseur) × THÈME (transverse : 04-Techniques, 05-Leaders, 06-Industrie, 07-Prompts). Thématiques non renumérotés (chemins en dur préservés).
- **Suite (drift doc à corriger)** : SCHEMA.md §4, Home.md, MOC-Concurrents, MOC-Modeles décrivent encore l'ancienne structure.
- **Source** : décision Raphael 14 juin — les fournisseurs IA ne sont pas des « concurrents » mais des acteurs suivis, symétrie avec 01-Claude.

## 2026-06-14 — MOC-Concurrents renommé en MOC-Outils-IA

- **Renommée** : `MOC-Concurrents` → `MOC-Outils-IA` (00-Hub), via `move_note` (wikilinks réécrits automatiquement dans 7 backlinks : Home, MOC-Industrie, Gemini CLI, OpenAI Codex, GitHub Copilot, Cursor, xAI Grok).
- **Contenu neutralisé** : titre « MOC — Outils AI coding », H1 « Outils AI coding (cross-fournisseurs) », resume + tag `#domaine/outils-ia`. La note reste un index thématique transverse (les fiches vivent dans les dossiers fournisseurs `products/`).
- **Source** : préférence Raphael — dissolution du concept « Concurrents » (les fournisseurs sont des acteurs suivis).


## 2026-06-22 — Switcher credentials Claude Code

- **Ajoutées** : [[switcher-credentials-claude-code]] (Knowledge/explorations) — mécanisme copie + re-capture qui dure des mois, pourquoi NeoBoard a cassé (refresh maison + client_id invalidé par Anthropic février 2026), vérités contre-intuitives (expiresAt=accessToken, refreshToken présent≠vivant), pièges d'implémentation.
- **Source** : enquête + résolution panne switcher Neoteem (front web local `Documents/credential-claude/switch-web.mjs`).
## 2026-06-24 — Kit de base setup repo (chantier migration_script)

- **Modifiées** : [[methode-analyser-repo]] — section « KIT DE BASE — composants systématiques vs selon-repo » (memory/ + learning-reminder non-bloquant + skill-triggers/skill-activation + README/workflow/astuces = systématique ; pipeline agents / TDD / hooks lint = selon-repo).
- **Source** : chantier setup `.claude/` complet sur migration_script (repo équipe PostgreSQL). Gotchas capitalisés : trigger `_` mort (word-boundary), reset `.skill-recommendations-session` au SessionStart (bug latent neo_ia), erreur de catégorie « workflow dev app sur repo SQL ».
- **Mémoire** : feedback [[config-repo-equipe-vs-forge]] (déjà créé).

## 2026-06-24 — Correction bypass périmé delegate-guard-pattern

- **Modifiées** : `delegate-guard-pattern` — section 3 (bypass) corrigée : `CLAUDE_AGENT`/`CLAUDE_DELEGATE_BYPASS` PÉRIMÉS (retirés du hook réel car spoofables) → mécanisme réel = `attributionSkill` lu dans le transcript, bypass STRICT par type de fichier. Ajout section 4 « scope forge-only + engagement cross-repo » + alignement runner `py` Windows + matcher `Write|Edit|MultiEdit`.
- **Source** : incident 24 juin (9 SKILL.md écrits à la main dans migration_script hors forge → guard ne fire pas). Drift résiduel entre la note canonique et l'implémentation `delegate-guard.py` réelle.
## 2026-06-27 — Méthode « monter un système de workflow » (capabilities)

- **Ajoutées** : `04-Techniques/patterns/methode-monter-systeme-workflow.md` — grille de dispatch besoin → Skill/Workflow/Agent/Framework/Hook/MCP, 4 patterns de robustesse, 3 archétypes. Méthode transverse (cœur stack-agnostique, colonne « créer via » = instanciation forge/CC).
- **Source** : podcast YouTube agence/bootcamp IA (Eliott Meunier & associés, https://www.youtube.com/watch?v=5WiuP81OVJo) — taxonomie « capabilities », validateur embarqué Sierra-style, provenance draft→approved + jauge %draftia.

## 2026-06-27 (suite) — Audit utilité skills + critique DA suppression 3 skills

- **Ajoutées** : `Knowledge/critiques/critique-2026-06-27-suppression-3-skills.md` — verdict DA (2 BLOCKING + 1 PARTIAL) sur le plan KILL self-check / merge da-blocking-arbitrage / convert auditor-empirical-verify, avec plan corrigé zéro-perte + items additifs.
- **Source** : 3 workflows d'audit skills (classification, amélioration, utilité/reclassement) + devils-advocate. Corpus jugé LEAN (42/45 KEEP). Chantier destructif reporté en session fraîche.

## 2026-06-27 (suite 2) — Reclassement 3 skills exécuté (zéro-perte)

- **Composants `.claude/`** : `auditor-empirical-verify` → rule `post-dispatch-verify` ; `da-blocking-arbitrage` splittée (agent devils-advocate + rule pipeline) ; `self-check` KILL (checks portés dans repo-inspector). + trous dispatch evolve/loop-forge comblés. 3 commits (ce64a76, fa65282, ce32bd3).
- **Modifiées** : `Knowledge/critiques/critique-2026-06-27-suppression-3-skills.md` — section MAJ exécution (3 actions DONE + reste additif).
- **Source** : audit utilité skills + DA (2 BLOCKING corrigés zéro-perte avant suppression).

## 2026-07-16 — Gotcha permissions : Write/MultiEdit(path) inertes

- **Ajoutées** : `Knowledge/erreurs/erreur-write-multiedit-regles-permission-fichier-inertes.md` — seul `Edit(path)` est évalué par le contrôle de permission fichier (il couvre Write/Edit/MultiEdit) ; `Write(path)` et `MultiEdit(path)` sont des règles mortes. À NE PAS confondre avec le matcher de hook `Write|Edit|MultiEdit` (triplet explicite obligatoire, convention opposée).
- **Source** : message de correction Claude Code sur les settings forge — même pattern inerte trouvé dans les 4 repos (forge, ia_back, neo_ia, neoteem-brain). Nettoyage settings forge appliqué. Note reliée à [[erreur-deny-global-ecrase-allow-projet]], [[enableallprojectmcp-permissions-allow]], [[comment-creer-hook]].
