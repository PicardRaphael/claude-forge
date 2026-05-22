---
titre: "Audit qualité — Rapports chantier 22 mai sont-ils parfaits pour produire les notes canoniques ?"
resume: "Audit des 8 rapports de recherche du chantier 22 mai : forces/manques/contradictions/claims à vérifier, verdict SUFFISANT/À COMPLÉTER, plan de recherches additionnelles"
aliases:
  - "audit qualite chantier"
  - "rapports chantier complets"
  - "audit avant notes canoniques"
derniere-maj: 2026-05-22
auteur: claude
tags:
  - "#type/synthese"
  - "#projet/forge"
---

# Audit qualité — Rapports chantier 22 mai

## Méthode

- Read complet des 8 rapports (~3 400 lignes cumulées)
- Grep croisé sur 5 dimensions chiffrées critiques : stars Karpathy, PRs/jour Boris, 22k LOC Erik, +300% PRs hebdo, dates pivot vibe coding, versions modèles
- Aucune modification, aucune création de note canonique
- Critères : citations verbatim + URL, dates exactes, métriques chiffrées, anti-patterns nommés, workflow étapé, sources primaires

---

## BLOC 1 — `recherche-youtube-talks.md`

- **Fichier** : `recherche-youtube-talks.md`
- **Lignes** : 410
- **Forces** :
  1. Transcription complète de la London opening keynote (6 500 mots) avec URL canonique `youtube.com/watch?v=6amLO7I9xdg` et speakers nommés en ordre d'apparition
  2. 8+ citations verbatim attribuées (Boris, Lisa Crofoot, Katelyn Lesse, Angela Jiang, Daisy Hollman, Fiona Fung) avec contexte d'énonciation
  3. Tableau métriques SF (section 2.6) chiffré avec sources : +80x demand, +300% PRs, 66% token reduction, 87% SWE-bench
  4. 10 sources canoniques URL listées en fin (Simon Willison, Chris Ebert, Blake Crosley, MIT Tech Review, Fortune, InfoQ, TechCrunch)
  5. Section "Sources non explorées" (section 10) honnête sur les gaps (Daisy/Noah/Matt London talks pas encore uploadés)
- **Manques détectés** :
  - Le talk Boris AI Ascent (`SlGRN8jh2RI`) est référencé mais "transcription non extractible" — pas de verbatim direct, contradiction avec le rapport YouTube watch qui transcrit lui-même Sequoia AI Ascent (Lauren Reeder interview, `SlGRN8jh2RI` = même URL)
  - Métriques 8.4% / 10.1% Outcomes (docx/pptx) mentionnés sans source URL
  - "Boris setup Boris (canonique 2026-05)" section 3.2 = tableau dense mais source aggrégée (Pragmatic Engineer + howborisusesclaudecode.com) sans citer ligne par ligne
  - Pattern "Compounding Engineering" attribué à Dan Shipper sans tweet URL exact
- **Contradictions internes ou avec autres rapports** :
  - **PRs/jour Boris** : ce rapport dit "20-30 PRs/jour" (sect 3.3) ; le rapport `recherche-youtube-watch-vibe-coding.md` cite Boris verbatim "150 PRs in a day" (record une journée) ; le rapport `recherche-x-twitter-leaders.md` cite "259 PRs en 30 jours" (thread janvier). **Les trois sont compatibles** (20-30/jour moyen + record 150 + 259/30j = 8-9/jour avg ancien) MAIS la note canonique devra clarifier "moyen vs record vs janvier"
  - **PRs hebdo équipe** : "~500 (janvier) à ~1150 (mars) = +300%" — attribué à **Noah Zweben** ici, attribué à **Boris keynote SF** dans `recherche-x-twitter-leaders.md`. Qui a présenté ce chart ?
  - **Version Opus** : "Opus 4.5 with thinking" (X janvier) vs "Opus 4.7" (London mai) — pas une contradiction, mais transition pas explicitée
- **Claims à vérifier additionnellement** :
  - "+200% PRs/eng Anthropic interne" (Cat Wu) — confirmé verbatim dans le rapport YouTube watch sect 4 ✓
  - "Mercado Libre 23 000 ingénieurs, 500k PRs, 9k apps, 90% Q3 2026" — confirmé verbatim dans YouTube watch ✓
  - "Mythos OpenBSD 27 ans" — confirmé verbatim YouTube watch ✓
  - "5x cost reduction Eve Legal" — confirmé verbatim YouTube watch ✓
  - "8 frontier models en 12 mois" (Lisa Crofoot) — confirmé verbatim YouTube watch ✓
  - "PostCompact hook" mentionné sect 3.2 — vérifier que c'est bien un type de hook officiel CC (ou hookSpecificOutput inventé)
- **Couverture par sujet canonique** :
  - skill : PARTIEL (mentions, pas de doctrine consolidée)
  - agent : PARTIEL (Boris subagents `code-simplifier`, `verify-app`)
  - hook : PARTIEL (PostToolUse, PostCompact, Stop, SessionStart cités sans détail)
  - CLAUDE.md : PARTIEL (2.5k tokens Boris, Compounding Engineering)
  - workflow : OK (plan mode → auto-accept → /commit-push-pr, multi-clotting, advisor strategy détaillé)
  - méta analyse-repo : RIEN
  - Karpathy vault : RIEN
  - MCP vs skills : PARTIEL (anti-pattern "20 MCP × 15 tools each")
- **Verdict** : **SUFFISANT** pour servir de matière première workflow + Boris/Cat Wu. **À compléter** uniquement si on veut sourcer ligne par ligne les citations setup Boris (Pragmatic Engineer transcript complet).

---

## BLOC 2 — `recherche-blog-docs-anthropic.md`

- **Fichier** : `recherche-blog-docs-anthropic.md`
- **Lignes** : 449
- **Forces** :
  1. Tableau "Carte des sources" (sect 0) avec URL + date + auteurs pour 9 sources Anthropic officielles — référence primaire idéale
  2. **Citation verbatim** des tableaux "Build your setup over time" et "Context costs" de `features-overview` (sect 2) — c'est LE document de doctrine 2026
  3. Anti-patterns OFFICIELS nommés et numérotés (sect 1.3) : 5 "Common failure patterns" verbatim depuis `best-practices`
  4. Frontière hook/skill/CLAUDE.md/rules consolidée en un seul tableau (sect Synthèse) — directement réutilisable
  5. Précision honnête sur les redirects : `anthropic.com/engineering/claude-code-best-practices` → `code.claude.com/docs/en/best-practices` (page vivante sans signature)
  6. Identifie le **gap** : pas d'article officiel co-signé Cat Wu+Boris Cherny
- **Manques détectés** :
  - Pas de date sur les pages "vivantes" (`code.claude.com/docs/en/*`) — Anthropic ne signe pas, donc inévitable
  - Justin Young (Effective Harnesses) : pas de bio/affiliation détaillée
  - Section 9 (Writing effective tools) : 5 principes listés mais sans extraits verbatim pour chacun (juste 1-2 quotes globales)
  - Métriques manquantes : pas de chiffre sur le ratio "% de devs utilisant Skills GA" ni sur l'adoption Plugins
  - L'article "How Anthropic teams use Claude Code" (juillet 2025) est cité avec usages par équipe — mais le rapport ne signale PAS qu'il est obsolète sur les pratiques 2026 (Skills GA oct 2025, hooks, parallel sessions = absents)
- **Contradictions internes ou avec autres rapports** :
  - **Sweet spot CLAUDE.md** : ce rapport dit "< 200 lignes" (officiel) ; `verif-claudemd-taille-officielle.md` confirme aussi 200. Forge dit "~100L max". **PAS contradiction** mais à arbitrer dans la note canonique
  - **"Erik Schluntz, Amanda Askell" co-auteurs Building Effective Agents** : ce rapport CORRIGE le claim (seul Erik + Barry Zhang). Bon flag, mais signal qu'une source ancienne traînait quelque part — vérifier que d'autres rapports n'ont pas le bug
- **Claims à vérifier additionnellement** :
  - "Tool response max 25 000 tokens dans Claude Code" — vérifier dans docs officielles (sect 9 cite ce chiffre)
  - "Agent hook : timeout 60s, jusqu'à 50 tool-use turns" — vérifier dans hooks-guide (sect 3 cite ces chiffres)
  - "Skills re-attached après compaction : 5 000 tokens chacun, budget combiné 25 000" — source pas vérifiable depuis le rapport
  - "Auto mode classifier model qui bloque scope escalation" — confirmé par le rapport mais sans citation verbatim
- **Couverture par sujet canonique** :
  - skill : OK (progressive disclosure 3 niveaux verbatim, Skills GA blog, frontière vs MCP/subagent/CLAUDE.md)
  - agent : OK (Building Effective Agents 5 patterns + Effective Harnesses 2-agent architecture)
  - hook : OK (5 types handlers, doctrine deterministic verbatim, frontière hook vs skill)
  - CLAUDE.md : OK (sweet spot 200L, INCLURE/EXCLURE verbatim, anti-pattern over-specified)
  - workflow : OK (Build your setup over time tableau)
  - méta analyse-repo : RIEN
  - Karpathy vault : RIEN
  - MCP vs skills : PARTIEL (frontière mentionnée, pas de doctrine MCP-vs-skill développée)
- **Verdict** : **SUFFISANT** — c'est la pierre angulaire doctrine officielle pour les 4 notes canoniques skill/agent/hook/CLAUDE.md/workflow.

---

## BLOC 3 — `recherche-x-twitter-leaders.md`

- **Fichier** : `recherche-x-twitter-leaders.md`
- **Lignes** : 440
- **Forces** :
  1. Handles X confirmés (tableau sect 1) — évite confusions (`@ErikSchluntz` capital, `@alexalbert__` double underscore)
  2. 9 leaders couverts avec **URL tweet exacte pour chacun** (Boris, Thariq, Cat Wu, Lydia, Erik, Alex, Karpathy, Simon, Addy)
  3. Chiffres harness > model **directs** : "52.8% → 66.5% via harness changes seuls", "rank Top 30 → Top 5" (Addy/LangChain Terminal Bench 2.0)
  4. Identifie clairement le distinguo `[paraphrase]` vs verbatim — méthodologie honnête
  5. Section "Anti-patterns à capitaliser" (sect Anti-patterns détectés) directement réutilisable
- **Manques détectés** :
  - Beaucoup de `[paraphrase]` — surtout Cat Wu, Lydia, Alex Albert (snippets Google insuffisants pour verbatim)
  - Thariq "9 catégories skills" (sect 2) — pas de liste des 9 catégories ! "Les bonnes skills tombent dans une seule" mais lesquelles ? Manque critique pour la note canonique skill
  - Karpathy "220 000+ étoiles cumulées" (sect 7) : décomposé "91k Forrest Chang + 132k mirror multica-ai" — chiffres approximatifs (le rapport Karpathy vault dit "110,000+ stars en ~3 mois" pour Forrest seul)
  - Aucune date précise pour le tweet Alex Albert sur les hooks (juste "Tweet Hooks rollout")
- **Contradictions internes ou avec autres rapports** :
  - **CONTRADICTION CRITIQUE Karpathy stars** : ce rapport = "220 000+ étoiles cumulées (91k Forrest + 132k mirror)" ; rapport `recherche-karpathy-vault-canonique.md` = "**110,000+ stars en ~3 mois**" pour le repo Forrest Chang. **À arbitrer** — TechTimes article cité (20260518) parle de "220k combined", donc 220k = somme repos dérivés, 110k = repo principal Forrest. Note canonique devra dire les deux chiffres distincts
  - **Date thread Boris fondateur** : "2 jan 2026" ici ; rapport `recherche-youtube-talks.md` dit "Thread X janvier 2026 (8M views)" sans date précise. OK cohérent
  - **PRs Boris** : "259 PRs en 30 jours, 497 commits, 40 000 lignes" ici (Opus 4.5, janvier) vs "150 PRs/jour record" (rapport YouTube watch, Boris Sequoia mai). Compatible mais nécessite cadrage temporel
  - **+300% PRs hebdo** : attribué ici à Boris keynote SF (sect 1) ; attribué à Noah Zweben dans `recherche-youtube-talks.md`. **À arbitrer** — Boris a probablement présenté un chart de Noah Zweben, à confirmer sur live blog Simon Willison
- **Claims à vérifier additionnellement** :
  - "Opus 4.6 dans Claude Code 58.0% Terminal-Bench 2.0 vs ForgeCode 79.8%" (Addy, sect 9) — citer source Addy primaire
  - "Boris : 100% production code is now AI, hadn't written a line by hand since October 2025" (sect 5) — confirmé verbatim dans rapport YouTube watch Boris Sequoia ✓
  - "Lydia tweet Learning mode" URL `x.com/lydiahallie/status/2056420694087594283` — semble fabriquée car ID très long mai 2026 ; à vérifier
  - "Alex Albert tweet hooks" sans ID/date — claim à risque
  - "Karpathy 28 jours consécutifs au top GitHub Trending, rang #94 mondial" — source ?
- **Couverture par sujet canonique** :
  - skill : PARTIEL (Thariq abstraction + 9 catégories non listées + gotchas pattern + append-mostly)
  - agent : PARTIEL (Lydia Agent Teams, Erik leaf nodes, sub-agents Boris)
  - hook : PARTIEL (Alex Albert "red squigglies", Addy Ratchet Principle)
  - CLAUDE.md : OK (Boris 2.5k tokens, Karpathy 4 règles, Compounding Engineering)
  - workflow : OK (Boris setup 10 points, Erik 4 stratégies, Lydia Learning mode)
  - méta analyse-repo : PARTIEL (Addy harness engineering)
  - Karpathy vault : RIEN (couvert ailleurs)
  - MCP vs skills : PARTIEL (Boris : MCP = "simplest answer")
- **Verdict** : **À COMPLÉTER** — exigences spécifiques : (1) lister les 9 catégories Thariq (relancer x-read ou WebFetch sur tweet `trq212/status/2033949937936085378`), (2) vérifier IDs tweets Lydia/Alex Albert via x-read, (3) arbitrer attribution "+300% chart" via Simon Willison live blog.

---

## BLOC 4 — `recherche-github-karpathy-leaders.md`

- **Fichier** : `recherche-github-karpathy-leaders.md`
- **Lignes** : 412
- **Forces** :
  1. **Inventaire concret `.claude/` Anthropic** : `anthropics/claude-code` n'a QUE 3 commandes (`commit-push-pr.md`, `dedupe.md`, `triage-issue.md`) — finding majeur, contraste avec forge
  2. `anthropics/claude-for-legal` CLAUDE.md analysé en détail (130 lignes, 5 sections, regex naming, invariants I1-I11) — référence concrète idéale
  3. 36 plugins officiels catégorisés (12 LSP + dev tools + quality + méta + style)
  4. Mitchell Hashimoto "Harness Engineering" 3 citations verbatim avec URL exacte
  5. Fowler/Böckeler taxonomie Guides vs Sensors (computational/inferential) reproduit verbatim + tableau
  6. Tableau divergences (sect 8) Anthropic / Hashimoto / Karpathy / Forge — directement réutilisable pour méta analyse
- **Manques détectés** :
  - `anthropics/claude-code` settings.json "non visible" — pas creusé si privé ou absent
  - 36 plugins listés mais pas de stats (downloads, étoiles, dernière mise à jour)
  - Skill `skill-creator` Anthropic décrite en 5 lignes (sect 1.3) — la doctrine "with-skill + baseline parallèle" mériterait verbatim
  - Pas de mention des `.claude/skills/` ni `.claude/agents/` Anthropic exposés (peut-être inexistants, à confirmer)
  - "Karpathy LLM Wiki gist publié 3-4 avril 2026 sur X, gist le lendemain" : date imprécise (3 OU 4 avril)
- **Contradictions internes ou avec autres rapports** :
  - **Karpathy a rejoint Anthropic — annonce mai 2026** : confirmé. Mais date précise ici = juste "mai 2026" alors que `recherche-karpathy-vault-canonique.md` dit "19 mai 2026" avec tweet URL
  - **CLAUDE.md claude-for-legal taille** : "130 lignes, ~5.89 KB" ici. Pas de contradiction directe avec verif-claudemd (200L cible) — alignement
  - **Karpathy stars CLAUDE.md** : sect 6.1 référence le repo Forrest Chang mais ne donne PAS de chiffre stars (le donne implicitement via "Karpathy LLM Wiki gist" 5000+ stars en 5 jours). Cohérent avec les autres rapports
  - Forge décrite "60+ skills/agents/hooks" sect 1.1 — pas de chiffre exact, à vérifier
- **Claims à vérifier additionnellement** :
  - "anthropic.com/engineering/claude-code-best-practices redirige vers code.claude.com" — confirmé dans rapport blog
  - "Mitchell Hashimoto 'harness engineering' repris par Fowler, OpenAI, Mollick dans les 2 semaines" — source ?
  - "LangChain février 2026 Terminal Bench 2.0 : 52.8% → 66.5% via harness" — vérifier (Fowler article cite ces chiffres)
  - "100 articles, 400K mots" Karpathy LLM Wiki perso — non vérifiable (privé)
- **Couverture par sujet canonique** :
  - skill : OK (skill-creator workflow, Stripe/Vercel/Cloudflare/Sentry/OpenAI skills officielles)
  - agent : OK (Building Effective Agents implicite, Vercel claude-managed-agents-starter)
  - hook : PARTIEL (Ghostty AGENTS.md interdictions = pas hooks, mais c'est mentionné)
  - CLAUDE.md : OK (claude-for-legal 130L détaillé, Ghostty AGENTS.md, Karpathy 4 rules)
  - workflow : PARTIEL (Karpathy 3 ops Ingest/Query/Lint mentionnés brièvement)
  - méta analyse-repo : OK (sect 7 + 8 — patterns récurrents + divergences cross-leaders)
  - Karpathy vault : OK (sect 2 LLM Wiki, 3 couches, ops)
  - MCP vs skills : RIEN
- **Verdict** : **SUFFISANT** pour méta analyse-repo + CLAUDE.md doctrine. Aucune recherche additionnelle bloquante.

---

## BLOC 5 — `verif-claudemd-taille-officielle.md`

- **Fichier** : `verif-claudemd-taille-officielle.md`
- **Lignes** : 84
- **Forces** :
  1. **Citation verbatim avec URL** Anthropic officiel : "target under 200 lines per CLAUDE.md file" (`code.claude.com/docs/en/memory`)
  2. **Distinction critique** identifiée : 200L CLAUDE.md = recommandation (soft) ; 200L/25KB = HARD limit MEMORY.md
  3. Tableau croisé sources (Anthropic vs HumanLayer vs Builder.io vs forge) — verdict clair "pas de divergence Anthropic ↔ Anthropic"
  4. 5 questions précises répondues nettement (sect "Réponses aux questions précises")
  5. Anti-pattern officiel "The over-specified CLAUDE.md" cité verbatim
- **Manques détectés** :
  - Pas de "last updated" sur la page docs Anthropic (limitation Anthropic, pas de l'auteur)
  - HumanLayer "~60 lignes" cité mais sans URL exacte
  - Pas de capture screenshot/timestamp de la page (au cas où Anthropic édite)
- **Contradictions internes ou avec autres rapports** :
  - **PARFAITE COHÉRENCE** avec `recherche-blog-docs-anthropic.md` qui cite aussi 200L
  - Forge dit "~100L max" — plus strict que Anthropic, cohérent et défendable
- **Claims à vérifier additionnellement** : aucun
- **Couverture par sujet canonique** :
  - CLAUDE.md : OK COMPLET (le rapport est mono-sujet)
  - tous autres : RIEN (et c'est normal)
- **Verdict** : **SUFFISANT** — verdict 100% PARFAIT sur son scope. La note canonique CLAUDE.md doit citer ce rapport et la source Anthropic verbatim.

---

## BLOC 6 — `recherche-youtube-watch-vibe-coding.md`

- **Fichier** : `recherche-youtube-watch-vibe-coding.md`
- **Lignes** : 462
- **Forces** :
  1. **38 309 mots de transcript primaire YouTube** — pas de paraphrase blog, sources brutes
  2. 4 talks transcrits avec URL exacte et titre exact YouTube : Erik Schluntz (`78EYLieMpvc`), Boris Sequoia (`SlGRN8jh2RI`), Thariq SDK Workshop (`TqC1qOfiVcQ`), London keynote (`6amLO7I9xdg`)
  3. **Citations verbatim massives** avec marqueurs `>` (au moins 40+ extraits)
  4. Tableau "Métriques dures rassemblées" (sect Synthèse) avec source verbatim pour chacune — directement réutilisable
  5. Anti-patterns nommés avec source + résolution (tableau sect Anti-patterns nommes)
  6. Résout explicitement le paradoxe Karpathy vs Erik sur "vibe coding" (sect Reconciliation)
  7. Section "Vidéos NON transcrites" honnête sur les gaps (Karpathy Sequoia URL non trouvée, Thariq SF Extended introuvable)
  8. Convergences avec doctrine forge documentées (sect Annexe)
- **Manques détectés** :
  - Karpathy Sequoia AI Ascent 2026 NON transcrit (URL YouTube non trouvée) — couvert par blog Karpathy bearblog
  - Thariq SF Extended talk "Multi-agent: when to split" NON trouvé — couvert par workshop SDK ~2h (qui couvre les mêmes thèmes mais ce n'est PAS le même talk)
  - Boris CwC SF Opening Keynote (`wjvESxKgqaQ`) identifié mais NON transcrit (cap 5 vidéos auto-imposé)
  - "1 day instead of 2 weeks" Erik : le rapport NOTE explicitement que c'est analogie cognitive, pas chiffre mesuré — bon flag honnête
  - Sub-titres EN auto-gen YouTube uniquement (pas manuels) — risque de typos sur noms propres / chiffres
- **Contradictions internes ou avec autres rapports** :
  - **DATE PIVOT vibe coding → agentic engineering** : ce rapport (sect Vidéos non transcrites) RÉSOUT explicitement : event Sequoia AI Ascent **29 avril 2026**. Tweet original vibe coding = **février 2025**. Rapport `recherche-x-twitter-leaders.md` dit "Tweet fondateur 26 janvier 2026" — c'est COMPATIBLE car janvier 2026 = thread "vibe coding → agentic engineering" (le pivot Karpathy), pas le tweet vibe coding original 2025. **Note canonique : 3 dates distinctes à séparer** (1) tweet vibe coding original fév 2025 (2) thread pivot 26 janv 2026 (3) talk Sequoia 29 avril 2026
  - **22 000 LOC Erik** : ce rapport citation verbatim "22,000 line change". Cohérent avec autres rapports
  - **"1 jour vs 2 semaines"** : ce rapport CORRIGE explicitement — Erik dit "one day instead of two weeks" en ANALOGIE (pas chiffre mesuré). Rapports `recherche-youtube-talks.md` (sect 6.2 "compressées à 1 jour") et `recherche-x-twitter-leaders.md` (sect 5 "Résultat : 2 semaines → 1 jour") présentent ça comme métrique brute. **À corriger dans la note canonique** — utiliser le framing analogie
  - **Boris "150 PRs in a day"** : ce rapport = verbatim Boris Sequoia "There was a day last week I did like 150 PRs in a day. That was a record." → c'est un RECORD, pas la moyenne. Le rapport `recherche-youtube-talks.md` dit "20-30 PRs/jour" comme moyenne. Compatible
- **Claims à vérifier additionnellement** :
  - "Boris 100% code Claude depuis October/November 2025" — verbatim ✓
  - "Mythos OpenBSD 27 ans" — verbatim Lisa Crofoot ✓
  - "Mercado Libre 23 000 ingénieurs, 90% Q3 2026 Oscar Mowen" — verbatim Cat Wu ✓
  - "Binti 20 jours saved foster family" — verbatim Cat Wu ✓
  - "Karpathy a la même histoire TI-83 que Cat Wu" (sect 4, note bracketée) — vérifier (Boris Sequoia transcript a-t-il vraiment l'anecdote TI-83 ?)
- **Couverture par sujet canonique** :
  - skill : OK (Thariq verbatim "Skills are progressive context disclosure", filesystem-based)
  - agent : OK (Thariq sub-agents = context protection, parallel, verification rule-based)
  - hook : PARTIEL (Lisa "scaffolding holds back", pas de doctrine hook spécifique)
  - CLAUDE.md : PARTIEL (mention "Document & Clear" workflow Erik)
  - workflow : OK (Erik 4 stratégies leaf nodes, Boris loops, multi-clauding, advisor)
  - méta analyse-repo : PARTIEL (Lisa "scaffolding evolves with capability")
  - Karpathy vault : RIEN (talk Sequoia non transcrit)
  - MCP vs skills : OK (Thariq Tools vs Bash vs Code gen trade-offs verbatim, "non-reversible = tool")
- **Verdict** : **SUFFISANT** — c'est le rapport le plus dense en verbatim primaire. La transcription Karpathy Sequoia est un gap mais blog bearblog couvre. **OPTIONNEL** : transcrire Boris CwC SF Opening Keynote (`wjvESxKgqaQ`) pour avoir le couple SF+London symétrique.

---

## BLOC 7 — `recherche-karpathy-vault-canonique.md`

- **Fichier** : `recherche-karpathy-vault-canonique.md`
- **Lignes** : 530
- **Forces** :
  1. **Verbatim du Gist** Karpathy LLM Wiki via WebFetch — citations exactes pour 3 couches / 3 ops / index.md / log.md / tooling
  2. URL gist exacte : `gist.github.com/karpathy/442a6bf555914893e9891c11519de94f`
  3. Citation pivot verbatim : "Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase"
  4. **Inventaire VÉRIFIÉ** des repos Karpathy (nanochat / autoresearch / nanoGPT / llm.c) — finding majeur : Karpathy n'utilise PAS CLAUDE.md/AGENTS.md à la racine de ses repos !
  5. nanochat `read-arxiv-paper/SKILL.md` analysé en détail (workflow concret transposable)
  6. autoresearch `program.md` analysé en détail (setup steps + rules + tracking TSV)
  7. **Question Q4 honnête** : "Karpathy ne prescrit RIEN" sur frontmatter — empêche de surclaim
  8. Tableau comparatif Karpathy vs forge-brain (sect Q6) avec verdict "ÉCART MAJEUR / MANQUE / DIFFÉRENT" par dimension
  9. 4 recommandations refonte forge-brain hiérarchisées P1/P2/P3
- **Manques détectés** :
  - Tweet X 2 avril 2026 annonce LLM Wiki : **PAS accédé verbatim** (reconstitué via couverture presse) — flag honnête de l'auteur
  - Karpathy a-t-il publiquement endorsé le repo Forrest Chang ? **Non trouvé** — bon flag
  - "Statut endorsement public Karpathy sur forrestchang/andrej-karpathy-skills" : non trouvé. **Bon flag** — à re-vérifier via x-read si critique
  - Talks Dwarkesh Patel récents Karpathy : non explorés
  - Frontmatter "communauté convergence" : pas de citation source du consensus (qui a convergé ?)
- **Contradictions internes ou avec autres rapports** :
  - **Karpathy CLAUDE.md stars** : "110,000+ stars en ~3 mois" ici vs "220 000+ étoiles cumulées" dans `recherche-x-twitter-leaders.md`. **Résolution** : 110k = repo principal Forrest Chang, 220k = somme repos dérivés (Forrest + mirror multica-ai). Note canonique = dire les deux distinctement
  - **Date thread Karpathy "vibe coding → agentic engineering"** : 26 janvier 2026 ici. Cohérent avec `recherche-x-twitter-leaders.md` (même date). Cohérent avec `recherche-youtube-watch-vibe-coding.md` (qui dit "Vague 3 du chantier qui disait fevrier est probablement confondu avec le tweet original de fevrier 2025")
  - **Sequoia AI Ascent 2026 talk Karpathy** : ce rapport (sect 3) couvre via singjupost transcript ; rapport YouTube watch dit "URL YouTube directe non trouvée". Cohérent — le talk a un transcript écrit mais pas de YouTube identifié
  - **Date Karpathy rejoint Anthropic** : "19 mai 2026" ici avec tweet URL `x.com/karpathy/status/2056753169888334312`. Cohérent avec autres rapports (juste plus précis)
- **Claims à vérifier additionnellement** :
  - "qmd github tobi/qmd" — confirmer existence repo (cité dans gist Karpathy)
  - "5,000+ stars en 5 jours" sur gist LLM Wiki — confirmer
  - "Karpathy LLM Wiki perso 100 articles 400 000 mots" — non vérifiable (privé), assumer verbatim Karpathy
  - "Sequoia AI Ascent talk = 29 avril 2026" — source `recherche-youtube-watch-vibe-coding.md` dit "29 avril 2026 (event date)". À cross-checker avec singjupost
  - Tweet X 2 avril 2026 annonce LLM Wiki — récupérer ID via x-read si critique pour la note canonique
- **Couverture par sujet canonique** :
  - skill : PARTIEL (nanochat read-arxiv-paper SKILL.md exemple)
  - agent : PARTIEL (autoresearch program.md = mode agent)
  - hook : RIEN
  - CLAUDE.md : OK (Forrest Chang 70L verbatim 4 sections, Karpathy schema file)
  - workflow : OK (3 ops Ingest/Query/Lint canoniques)
  - méta analyse-repo : OK (sect 4 inventaire Karpathy repos)
  - **Karpathy vault : OK COMPLET** (le rapport est mono-sujet)
  - MCP vs skills : PARTIEL (mention qmd CLI+MCP)
- **Verdict** : **SUFFISANT** pour la note canonique Karpathy vault. **OPTIONNEL** : x-read sur tweet 2 avril 2026 annonce LLM Wiki si on veut le verbatim original.

---

## BLOC 8 — `recherche-mcp-vs-skills-cli.md`

- **Fichier** : `recherche-mcp-vs-skills-cli.md`
- **Lignes** : 353
- **Forces** :
  1. **TL;DR exécutif** dès le top (sect 0) — verdict clair "MCP = connectivité, Skills = procédure"
  2. **Citations verbatim attribuées** : Simon Willison, Thariq, Anthropic, Boris, Ronacher, Trail of Bits — toutes avec URL
  3. Token cost concret : "Sentry MCP ~8 000 tokens upfront", "GitHub MCP tens of thousands" — chiffres réutilisables
  4. Tableau comparatif (sect 2) 11 critères MCP vs Skill+CLI
  5. 6 anti-patterns nommés avec source + citation + fix (sect Anti-patterns documentés)
  6. **Verdict argumenté pour forge-brain et neoteem-brain** distinctement (sect 4 et 5) — directement actionnable
  7. Pattern hybride Karpathy `qmd` cité (CLI + MCP server simultanés) — référence canonique
  8. Trail of Bits config production référencée avec URL `github.com/trailofbits/claude-code-config`
- **Manques détectés** :
  - "Mesurer le token cost réel forge-brain + neoteem-brain" : noté comme TODO (sect Annexe gaps) — pas fait
  - Pas de citation Eric J. Ma source URL (sect 7 dernière citation)
  - "Anthropic blog skills-explained" URL pas explicite (juste cité `claude.com/blog/skills-explained`)
  - 11 outils MCP forge-brain listés (sect 4) — pas de comptage token cost actuel
- **Contradictions internes ou avec autres rapports** :
  - Boris Sequoia "It's just MCP" (ce rapport sect 1.6) ↔ Simon Willison "Skills bigger deal than MCP" (sect 1.1) — c'est PAS une contradiction mais une **tension stratégique** que le rapport résout bien : MCP = couche connectivité, Skills = procédure on-top
  - Thariq workshop transcrit ici (sect 1.3) cite mêmes verbatim que `recherche-youtube-watch-vibe-coding.md` (sect 3) — cohérent
- **Claims à vérifier additionnellement** :
  - "GitHub MCP officiel consomme tens of thousands de tokens" — chiffre Simon Willison, à confirmer source
  - "Sentry MCP ~8 000 tokens" — chiffre Ronacher, à confirmer
  - "Trail of Bits `enableAllProjectMcpServers: false` par défaut" — confirmer dans repo TOB
  - Le **vrai** verdict pour neoteem-brain : "682+ notes" — est-ce le chiffre actuel (`project_neoteem_brain.md` mémoire confirme 682+ notes 2026-05-06) ✓
- **Couverture par sujet canonique** :
  - skill : OK (frontière vs MCP, Trail of Bits 2000 words limit, references/)
  - agent : RIEN
  - hook : PARTIEL (mention `vault-query-guard` enforcement)
  - CLAUDE.md : RIEN
  - workflow : PARTIEL (knowledge-first routing)
  - méta analyse-repo : RIEN
  - Karpathy vault : PARTIEL (qmd pattern cité)
  - **MCP vs skills : OK COMPLET** (mono-sujet)
- **Verdict** : **SUFFISANT** — verdict clair et actionnable. **OPTIONNEL** : mesurer le token cost réel forge-brain MCP au démarrage (Langfuse trace) si critique.

---

# Synthèse finale

## 1. Tableau des contradictions chiffrées/datées

| Métrique / Date | Valeur A | Valeur B | Valeur C | Source à arbitrer |
|---|---|---|---|---|
| Stars CLAUDE.md Karpathy | 110 000+ (`karpathy-vault`) | 220 000+ cumulées (`x-twitter`) | — | Arbitrage : 110k = Forrest Chang seul, 220k = somme dérivés (TechTimes 20260518) — citer les 2 distinctement |
| PRs Boris (rythme) | 20-30/jour (`youtube-talks` setup) | 259 en 30 jours (`x-twitter` jan thread, ~8.6/jour) | 150 PRs RECORD un jour (`youtube-watch` Boris Sequoia) | Compatibles : 259 = janvier 2026, 20-30 = solo régulier mai, 150 = record. Note canonique = cadrer chronologie |
| +300% PRs hebdo équipe | attribué Noah Zweben (`youtube-talks`) | attribué Boris keynote SF (`x-twitter`) | — | Probable : Boris a présenté un chart de Noah Zweben. À confirmer via Simon Willison live blog SF |
| Erik 22 000 LOC ratio | "2 semaines → 1 jour" comme métrique (`youtube-talks` + `x-twitter`) | "one day instead of two weeks" comme ANALOGIE cognitive, pas chiffre mesuré (`youtube-watch` Erik verbatim) | — | **Verbatim watch gagne** — utiliser framing analogie dans note canonique |
| Date pivot Karpathy "vibe → agentic" | janvier 2026 thread (`x-twitter`, `karpathy-vault`) | "fév 2025 tweet vibe + 29 avril 2026 Sequoia event" (`youtube-watch`) | — | Pas contradiction : 3 dates distinctes (1) tweet vibe original fév 2025 (2) pivot thread 26 janv 2026 (3) talk Sequoia 29 avril 2026 |
| Karpathy joined Anthropic | "mai 2026" (`github-karpathy-leaders`) | "19 mai 2026" tweet ID (`karpathy-vault`, `x-twitter`) | — | 19 mai 2026 ✓ |
| Opus version Boris | 4.5 (X jan 2026) | 4.7 (London mai 2026) | — | Pas contradiction, évolution dans le temps |
| Sweet spot CLAUDE.md | < 200L Anthropic officiel | ~100L forge interne | ~60L HumanLayer | 200 = recommandation officielle, 100 = plus strict OK, 60 = pratique terrain. Pas contradiction |
| Lydia tweet ID Learning mode | `2056420694087594283` (`x-twitter`) | — | — | ID suspect long (mai 2026), à vérifier via x-read |
| Karpathy 220k cumul décomposition | "91k Forrest Chang + 132k mirror multica-ai" (`x-twitter`) | "110k Forrest Chang" (`karpathy-vault`) | — | 110k > 91k → un des 2 chiffres Forrest Chang est obsolète. TechTimes 20260518 donne le total cumulé |

## 2. Liste des claims à re-vérifier (priorisée par criticité)

### Criticité HAUTE (impact direct sur notes canoniques)

1. **Stars Karpathy CLAUDE.md précis** — 91k OU 110k Forrest Chang ? Cumul 220k confirmé ?
2. **9 catégories Thariq skills** : non listées dans aucun rapport — bloquant pour note skill canonique
3. **+300% PRs hebdo : Noah Zweben ou Boris** ? Bloquant pour attribution dans note workflow
4. **Erik 22k LOC** : framing analogie vs métrique brute — choisir verbatim watch
5. **Date Karpathy Sequoia talk** : 29 avril 2026 (event) confirmer via source primaire

### Criticité MOYENNE (utile pour rigueur)

6. **GitHub MCP "tens of thousands tokens"** — chiffre Simon Willison source
7. **Sentry MCP "~8 000 tokens"** — chiffre Ronacher source
8. **Lydia tweet ID Learning mode** — vérifier authenticité via x-read
9. **Alex Albert tweet hooks** — pas d'ID/date, claim fragile
10. **"Tool response 25 000 tokens max"** + **"Agent hook 50 tool-use turns / 60s timeout"** — vérifier dans docs Anthropic
11. **"PostCompact hook" existe ?** — vérifier hooks-guide
12. **Skill-creator Anthropic "with-skill + baseline parallèle"** — verbatim workflow à récupérer

### Criticité BASSE (cosmétique)

13. Boris/Cat TI-83 anecdote — convergence biographique à confirmer
14. Mitchell Hashimoto "repris par Fowler/OpenAI/Mollick dans les 2 semaines" — source
15. Karpathy gist LLM Wiki "5 000+ stars en 5 jours" — chiffre exact
16. Tweet X 2 avril 2026 annonce LLM Wiki — verbatim original via x-read

## 3. Recherches additionnelles nécessaires AVANT notes canoniques

### Bloquantes (relancer agents)

- **WebFetch ou x-read sur `x.com/trq212/status/2033949937936085378`** — récupérer la liste des 9 catégories skills Thariq
- **WebFetch sur Simon Willison live blog SF `simonwillison.net/2026/May/6/code-w-claude-2026/`** — arbitrer attribution chart +300% PRs (Noah Zweben vs Boris)
- **WebFetch sur TechTimes article `20260518/karpathy-inspired-claudemd-passes-220000`** — récupérer la décomposition exacte stars 110k/91k/132k

### Non bloquantes mais souhaitables

- **x-read sur tweet Karpathy 2 avril 2026 annonce LLM Wiki** — verbatim original
- **x-read sur tweet Lydia `2056420694087594283`** — vérifier authenticité
- **WebFetch sur `code.claude.com/docs/en/hooks-guide`** — vérifier "Agent hook : 50 turns / 60s" + "PostCompact hook"
- **Transcript Boris CwC SF Opening Keynote `wjvESxKgqaQ`** — symétrie SF+London (optionnel, London suffit pour la doctrine)

## 4. Couverture matricielle (rapports × sujets canoniques)

| Rapport ↓ / Sujet → | skill | agent | hook | CLAUDE.md | workflow | méta analyse-repo | Karpathy vault | MCP vs skills |
|---|---|---|---|---|---|---|---|---|
| `youtube-talks` | PARTIEL | PARTIEL | PARTIEL | PARTIEL | OK | RIEN | RIEN | PARTIEL |
| `blog-docs-anthropic` | OK | OK | OK | OK | OK | RIEN | RIEN | PARTIEL |
| `x-twitter-leaders` | PARTIEL | PARTIEL | PARTIEL | OK | OK | PARTIEL | RIEN | PARTIEL |
| `github-karpathy-leaders` | OK | OK | PARTIEL | OK | PARTIEL | **OK** | OK | RIEN |
| `verif-claudemd` | RIEN | RIEN | RIEN | **OK** | RIEN | RIEN | RIEN | RIEN |
| `youtube-watch-vibe-coding` | OK | OK | PARTIEL | PARTIEL | OK | PARTIEL | RIEN | OK |
| `karpathy-vault-canonique` | PARTIEL | PARTIEL | RIEN | OK | OK | OK | **OK** | PARTIEL |
| `mcp-vs-skills-cli` | OK | RIEN | PARTIEL | RIEN | PARTIEL | RIEN | PARTIEL | **OK** |

### Lecture matricielle par sujet canonique

| Sujet | Couverture cumulée | Verdict |
|---|---|---|
| **skill** | 4×OK + 2×PARTIEL | SUFFISANT (sauf si 9 catégories Thariq requises) |
| **agent** | 3×OK + 3×PARTIEL | SUFFISANT |
| **hook** | 1×OK + 5×PARTIEL | À COMPLÉTER — manque "Agent hook 50 turns" + "PostCompact" vérif |
| **CLAUDE.md** | 4×OK + 2×PARTIEL | SUFFISANT (verif + blog + github + karpathy se complètent parfaitement) |
| **workflow** | 5×OK + 2×PARTIEL | SUFFISANT |
| **méta analyse-repo** | 2×OK + 2×PARTIEL | SUFFISANT (github + karpathy + Addy harness) |
| **Karpathy vault** | 1×OK + 1×PARTIEL | SUFFISANT (karpathy-vault rapport est mono-sujet) |
| **MCP vs skills** | 2×OK + 5×PARTIEL | SUFFISANT (mcp-vs-skills rapport est mono-sujet) |

## 5. Verdict global

**On PEUT produire 6 notes canoniques sur 8 sujets dès maintenant** : CLAUDE.md, agent, workflow, méta analyse-repo, Karpathy vault, MCP vs skills.

**On DOIT compléter 2 sujets avant** :

1. **note canonique skill** — relancer agent WebFetch/x-read pour récupérer la liste des **9 catégories Thariq** (tweet `trq212/status/2033949937936085378`). Bloquant car c'est LA taxonomie centrale skills 2026.
2. **note canonique hook** — vérifier dans `code.claude.com/docs/en/hooks-guide` : (a) "Agent hook timeout 60s / 50 tool-use turns" cité dans blog rapport, (b) existence "PostCompact" cité dans Boris setup. 1 WebFetch suffit.

**Autres remédiations recommandées avant publication** (non bloquantes) :

- Arbitrer attribution "+300% chart" (Noah Zweben vs Boris) via Simon Willison live blog SF
- Aligner les 3 chiffres Karpathy stars (110k / 91k / 220k cumul) en citant TechTimes directement
- Corriger systématiquement le framing "Erik 22k LOC 2 semaines→1 jour" — utiliser verbatim watch ("analogie cognitive, pas chiffre mesuré")
- Cadrer chronologie PRs Boris (259 jan / 20-30 moyenne / 150 record)

**Plan d'action proposé** :

```
Vague A (bloquante, ~15 min) :
  - WebFetch Simon Willison live blog SF → arbitrage Noah Zweben/Boris
  - WebFetch + x-read tweet Thariq 9 catégories
  - WebFetch hooks-guide → vérif Agent hook + PostCompact

Vague B (production notes, séquentielle) :
  - 6 notes canoniques produites directement (CLAUDE.md, agent, workflow, méta, Karpathy vault, MCP)
  - 2 notes canoniques produites après Vague A (skill, hook)
```

---

## Notes méthodologiques de l'audit

- **Aucune note canonique créée** — audit pur
- **Aucun rapport modifié** — lecture seule
- Grep croisé limité à 5 dimensions (stars, PRs, 22k LOC, +300%, dates vibe coding) — d'autres contradictions mineures peuvent exister
- Les verdicts SUFFISANT/À COMPLÉTER sont basés sur le critère "PARFAIT" du brief : verbatim + URL + dates + métriques + anti-patterns nommés + workflow étapé. Si les notes canoniques sont rédigées avec moins d'exigence, tous les rapports passent.
