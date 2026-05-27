---
titre: "Changelog vault forge-brain"
resume: "Historique des ajouts et modifications du vault forge-brain"
aliases:
  - changelog vault
  - historique vault
  - changelog forge-brain
  - historique notes vault
type: index
derniere-maj: 2026-05-27
auteur: claude
tags:
  - "#type/index"
  - "#domaine/claude-code"
---
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
  - [[da-blocking-arbitrage]] (skill) — confidence scoring 0-100 + seuil 80 (emprunté code-review Boris Cherny)
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
- **3 wikilinks morts fixés** : `[[skills-guide]]` → `[[comment-creer-skill]]`, `[[agents-orchestration]]` → `[[comment-creer-agent]]`, `[[hooks-guide]]` → `[[comment-creer-hook]]` dans cc-*-ref/SKILL.md.
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
