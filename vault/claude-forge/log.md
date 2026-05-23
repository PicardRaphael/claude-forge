---
titre: "Log vault forge-brain — append-only Karpathy"
resume: "Log append-only format Karpathy strict ## [YYYY-MM-DD] action | titre. Trace atomique des operations Ingest / Query / Lint sur le vault. JAMAIS modifie retroactivement."
aliases:
  - "log vault"
  - "log karpathy"
  - "log append-only"
  - "trace vault forge"
  - "vault operations log"
derniere-maj: 2026-05-22
auteur: claude
type: log
tags:
  - "#type/log"
  - "#karpathy/log"
---

# Log vault forge-brain

> Pattern Karpathy LLM Wiki : log **append-only** format strict `## [YYYY-MM-DD] action | titre`. Trace atomique des Ingest / Query / Lint. Pour la narration prosaique → voir [[CHANGELOG]].

**Format strict** (Karpathy Gist 4 avril 2026) :
```
## [YYYY-MM-DD] action | titre
- detail 1
- detail 2
```

**Actions canoniques** :
- `note-created` — nouvelle note ajoutee
- `note-updated` — note modifiee
- `note-deleted` — note supprimee
- `ingest` — capture source externe vers wiki
- `lint` — operation maintenance/cleanup
- `refonte` — refonte structurelle majeure
- `chantier` — chantier nomme (multi-actions groupees)

---

## [2026-05-23] chantier | Audit dogfooding forge — propagation pivot doctrinal 23 mai
- Détecté : forge ne respectait pas sa propre doctrine canonique vault sur 9 points (Type 1 doctrinal + 1 Type 3 structurel)
- Corrigé `CLAUDE.md` : 25+ → 29 events, Angela Jiang → Brad Abrams, max non déprécié, + 3 canoniques 23 mai ajoutées (methode-pivoter-doctrine + comparaison-skill-anthropic + anti-reentrance-sub-agents)
- Corrigé `vault/index.md` : mêmes 2 drifts doctrinaux + 3 canoniques 23 mai ajoutées
- Corrigé `vault/05-Leaders/claude-code/angela-jiang.md` : retiré attribution Advisor Strategy (revient à Brad Abrams)
- Corrigé `vault/1-Projets/Neoteem/ia_back/analyse-2026-05-22.md` : Angela Jiang → Brad Abrams
- Corrigé `.claude/skills/cc-hooks-ref/SKILL.md` : 25+ → 29 events
- Corrigé `.claude/agents/hook-creator.md` : 25+ → 29 events
- Corrigé `.claude/agents/devils-advocate.md` : effort xhigh → high (DA = jugement, pas architect)
- Ajouté frontmatter `description:` manquant sur `.claude/rules/sequence-canonique-modification.md` (rule MORTE silencieusement)
- Réduit `.claude/rules/check-before-create.md` en rappel court qui pointe vers sequence-canonique-modification.md (single source of truth)
- Cross-repo : corrigé `../neot-v2/ia_back/.claude/rules/quality-gates.md` (Angela → Brad Abrams)
- Drafté skill `/pivot-check` v1 (121L) pour automatiser détection drifts post-pivot (méta-insight feedback_doctrine_drift_pattern) — DA verdict GO-WITH-FIXES (B1 BLOQUANT sur agent-memory/), skill déplacée vers `vault/Knowledge/drafts/pivot-check-skill/` (hors scan CC), application manuelle Raphael requise
- Documenté pattern sub-agent bypass dans `Knowledge/erreurs/erreur-subagent-bypass-delegate-guard.md` : 3 couches protection (delegate-guard + sub-agent detection + auto-mode classifier) ont tenu
- Méthode : A→B→C→D→E + advisor() + DA, validation Raphael carte blanche

## [2026-05-22] chantier | Karpathy strict + composants refonte
- Cree dossier `raw/2026-05-22-chantier/` (Karpathy layer 1)
- Deplace 8 sources immuables : `recherche-*.md` vers `raw/`
- Cree `index.md` content-oriented (orientation LLM)
- Cree `log.md` append-only format Karpathy strict
- Cree `SCHEMA.md` self-describing (conventions vault)
- Supprime 9 hooks workflow (vault-query-guard, vault-query-tracker, vault-write-tracker, session-reset-vault-marker, vault-before-specialist, devil-advocate-stop, devil-advocate-tracker, devil-advocate-guard, reasoning-cache-reminder) — coherent doctrine 22 mai
- Genere `.claude/settings.json.proposed` (Python paths absolus + MultiEdit triplet + retrait hooks workflow). User doit appliquer manuellement (auto-mode classifier hard block self-modification)

## [2026-05-22] refonte | Chantier 8 canoniques + 14 leaders
- Cree 8 notes canoniques dans `04-Techniques/claude-code/` : [[comment-ecrire-claudemd]] + [[mcp-vs-skills-doctrine]] + [[comment-creer-skill]] + [[comment-creer-agent]] + [[comment-creer-hook]] + [[workflow-claude-code-optimal]] + [[methode-analyser-repo]] + [[pattern-vault-llm-karpathy]] + [[trail-of-bits-config]]
- Cree 14 fiches leaders : [[cat-wu]] + [[lisa-crofoot]] + [[angela-jiang]] + [[daisy-hollman]] + [[jeremy-hadfield]] + [[justin-young]] + [[Noah Zweben]] + [[addy-osmani]] + [[martin-fowler]] + [[hashimoto]] + [[tobi-lutke]] + reecrits [[Erik Schluntz]] + [[Thariq Shihipar]]
- Critique DA appliquee : 1 bloquant (events hooks inventes) + 5 forts (attribution lethal trifecta, aliases automatiser, DA conditionnel, metriques non sourcees, forrestchang→multica-ai)
- Nice-to-have DA N1-N5 traites (factoring wontfix, harness +21.8 pts etaye, isolation pattern vs stats forge, advisory 80% nuance, 7 anti-patterns ajoutes)

## [2026-05-22] note-deleted | 28 notes obsoletes cleanup
- 6 remplacees par canoniques : [[skills-guide]] [[agents-orchestration]] [[hooks-guide]] [[claudemd-guide]] [[claudemd-maintenance]] [[karpathy-llm-wiki-pattern]]
- 11 obsoletes doctrine 22 mai : [[Workflow Boris]] [[boris-workflow-2026-may]] [[pattern-architect-first-pipeline]] [[setup-project-complet]] [[kit-rules-standard]] [[vibe-coding-setup-complet]] [[best-practices-claude-code-leaders]] [[pipeline-boris-adapte-neoteem]] [[pattern-agentic-engineering]] [[agentic-engineering-karpathy]] [[Karpathy Dev Discipline]]
- 11 Knowledge obsoletes (markers TTL, dispatch-guard, architect-guard, TDD strict critiques)
- 64 fichiers vault wikilinks rediriges (~106 redirections)
- 0 wikilink residuel verifie empiriquement

## [2026-05-22] note-updated | Index + MOCs + CHANGELOG
- Cree section "Notes canoniques chantier 22 mai" en tete [[MOC-Claude-Code]]
- Mis a jour [[MOC-Leaders]] : section claude-code completee + agents enrichie + industrie creee
- Cree section "2026-05-22 — Chantier refonte canonique" dans [[CHANGELOG]]

## [2026-05-22] ingest | 16 rapports recherche web Anthropic
- Web research : blog Anthropic, GitHub Karpathy, X Twitter, YouTube SF/London, MCP vs Skills, Karpathy vault canonique
- 8 rapports recherche deposes (deplaces vers raw/ depuis _chantier-22mai/)
- 5 rapports verification (CLAUDE.md 200L, 9 categories Thariq, hooks officiels, 14 claims arbitres)
- 3 audits internes (MCP forge-brain, notes existantes, qualite rapports)

## [2026-05-21] refonte | Doctrine 22 mai pivot
- Cree [[raisonnement-22mai-doctrine-vs-enforcement]] — pivot doctrinal
- Cree [[raisonnement-kill-tdd-strict-hooks-mai-2026]]
- Cree [[raisonnement-revirement-pipeline-mai-2026]]
- Cree [[erreur-hooks-workflow-enforcement]]
- Cree [[erreur-pipeline-trop-long-frustration]]
- Pivot : hooks lint/security/scope, JAMAIS workflow agentique

---

## Conventions log

1. **Append-only** : on n'edite JAMAIS retroactivement. Si on s'est trompe, on ajoute une action `correction` qui referencee l'entree initiale.
2. **Format strict** : `## [YYYY-MM-DD] action | titre` exact. Pas de variations.
3. **Bullet points** : details en bullets dessous, wikilinks vers notes concernees.
4. **Une action = une entree** : pas de fusion. Si 5 actions dans la journee, 5 entrees.
5. **Cite les notes** : chaque action referencie les notes touchees via [[wikilink]].

## Voir aussi

- [[CHANGELOG]] — narration prosaique des changements
- [[SCHEMA]] — conventions du vault
- [[index]] — index content-oriented
- [[pattern-vault-llm-karpathy]] — pattern complet


## [2026-05-22] refonte | Composants .claude/ post-pivot 22 mai
- CLAUDE.md refondu (v3.0, 91 lignes < 100L sweet spot) : retire effort xhigh par defaut + hook critique double + architect-first obligatoire + DA systematique
- [[hook-creator]] agent : retire "Pattern marker + guard" du body, ajoute doctrine 22 mai + path Python absolu + triplet matcher Write|Edit|MultiEdit
- [[python-dev]] agent : opus+xhigh -> sonnet+high (effort xhigh reserve architect/dev-lead/refactor-pg) + matcher Write|Edit -> Write|Edit|MultiEdit
- [[project-analyzer]] agent : ajoute permissionMode plan + effort xhigh -> high
- [[project-auditor]] agent : effort xhigh -> high
- [[devils-advocate-pipeline]] rule reecrite : DA OBLIGATOIRE -> CONDITIONNEL cible
- 3 rules sans frontmatter description (agents-color-convention, changelog-vault, vault-consultation-protocol) : ajout description ligne 2 (etaient mortes silencieusement)
- [[python-ref]] skill : user-invokable true -> false (skill reference chargee par python-dev, comme cc-*-ref)
- Supprime 9 hooks workflow obsoletes : vault-query-guard, vault-query-tracker, vault-write-tracker, session-reset-vault-marker, vault-before-specialist, devil-advocate-stop, devil-advocate-tracker, devil-advocate-guard, reasoning-cache-reminder
- Genere .claude/settings.json.proposed (Python paths absolus Python313 + triplet MultiEdit + retrait hooks workflow). User doit appliquer manuellement (auto-mode classifier hard block self-modification)
- Audit complet : `vault/claude-forge/0-Inbox/_chantier-22mai/audit-gap-composants-canoniques.md`

## [2026-05-22] refonte | Cran 1 strict P1/P2 restants (6 items)
- devils-advocate agent : ajoute skills forge-brain + obsidian-markdown au frontmatter (ne lit plus vault via Grep/Read brut)
- cc-cowork-ref orpheline -> referencee dans project-analyzer skills
- CLAUDE.md gotchas critiques deplaces ligne 5 (etaient en bas, post v3.0 refactor restaient en fin) — auto-mode classifier + $ARGUMENTS + MCP forge-brain UNIQUEMENT
- claudemd-optimizer body : wikilink casse [[claudemd-guide]] -> [[comment-ecrire-claudemd]], ajout reference [[obsidian-markdown]]
- 3 skills allowed-tools ajoute : defuddle (Bash/WebFetch/Read), obsidian-markdown (Read/Write/Edit/MCP forge-brain), forge-brain (tous outils MCP forge-brain)
- .claude/settings.local.json.proposed genere : retire Bash(cat > *) overly broad (user applique manuellement, classifier bloque)
- 4 skills sans allowed-tools restent : configure-claude-desktop, expand, json-canvas, obsidian-bases (skills de reference sans outil critique, defaut OK)

## [2026-05-22] note-updated | context-actuel + memoire py launcher
- Cree memoire reference_python_windows_cross_machine.md (pattern py cross-machine)
- Update MEMORY.md avec entree py launcher
- Commit e80972a : python-dev.md ligne 19 corrige (python -m py_compile -> py -m py_compile)
- 19 commits chantier total : bb9e66e -> e80972a
## [2026-05-23] audit-thematique-claude-code | 12 notes corrigées + 2 leaders créés

Audit profond thème Claude Code (95 claims, 6 sub-agents parallèles).

- **Notes réécrites** (`update_note` complète) : [[comment-creer-hook]] [[comment-creer-agent]] [[comment-creer-skill]] [[comment-ecrire-claudemd]] [[workflow-claude-code-optimal]] [[methode-analyser-repo]] [[mcp-vs-skills-doctrine]]
- **Notes append** (compléments) : [[pattern-vault-llm-karpathy]] [[trail-of-bits-config]] [[methode-pivoter-doctrine]] [[raisonnement-22mai-doctrine-vs-enforcement]] [[critique-2026-05-22-8-canoniques-chantier]]
- **Notes créées** : [[Brad-Abrams]] (Product Lead Anthropic, Advisor Strategy) + [[Mitchell-Hashimoto]] (popularisateur harness engineering)
- **22 erreurs corrigées** : Justin Young split, Brad Abrams vs Angela Jiang, lethal trifecta = Willison, max non déprécié, 29 events hooks, timeouts par type, once:true skill only, 174L vs 130L, etc.
- **Nouvelles règles** : 250 chars description SKILL.md auto-trigger, pipeline architect→dev→reviewer→test ajouté à [[methode-analyser-repo]]
- **Source audit** : `output/audit-vault-thematique/01-claude-code/`

## [2026-05-23] behavioral-test-pass | doctrine audit 23 mai

Test comportemental session fraîche sur 6 corrections doctrinales audit thématique vault Claude Code → **6/6 PASS**. Validation : Brad Abrams Advisor Strategy (pas Angela Jiang), 29 events hooks (pas 25+), effort max toujours disponible (pas déprécié), Justin Young sans split modèles, Simon Willison lethal trifecta (pas Thariq), séquence A→B→C→D→E + pipeline conditionnel. Toutes notes canoniques contiennent ancrage anti-régression "⚠️ Avant 23 mai 2026…". Capitalisation : [[test-comportemental-audit-23mai]]. Audit thématique = **livré et validé**.

## [2026-05-23] done-session | audit thematique CC + forge dogfooding + meta-prompt + 6 prompts thematiques enrichis

Session longue (50+ échanges).

- **Audit thématique vault Claude Code** : 95 claims, 6 sub-agents par cluster, **22 erreurs corrigées**, 2 leaders créés ([[Brad-Abrams]], [[Mitchell-Hashimoto]]), 1 rule transverse ([[sequence-canonique-modification]])
- **Audit forge dogfooding** : 11 drifts corrigés (CLAUDE.md, vault/index.md, cc-hooks-ref, hook-creator, etc.). Skill `/pivot-check` draftée (4 fixes DA pending)
- **Méta-prompt bibliothèque** écrit dans `output/meta-prompt-generer-bibliotheque-analyse.md` — à exécuter en session fraîche pour générer ~25 prompts dans `vault/07-Prompts/analyse/`
- **6 prompts thématiques (02-07) enrichis** avec table "Navigation vault — où lire selon le cas"
- **2 nouveaux feedbacks mémoire** : `feedback_session_fatigue_decision`, `feedback_doctrine_drift_pattern` enrichi avec 3e incident
- **5 commits poussés** sur main : 9530458, cd058cc, 4aee799, c8ef44b, 3c55d94, 7b9f46c, bbe0311, b45d922

Pattern récurrent détecté : drift propagation aval (MOCs, CLAUDE.md, index.md) après pivot doctrinal canonique. 3 incidents en 3 jours.

## [2026-05-23] notes-creees | PTC + Google eng-practices

Suite tweet @_vmlops sur "/workflows shipped" (single source externe, slug non vérifié 404).

**Vérification** : feature canonique côté docs Anthropic = **Programmatic Tool Calling (PTC)**, pas `/workflows`. Pattern d'erreur identique à "Claude decides when to parallelize" hier (paraphrase tweet présentée comme verbatim Anthropic).

- **Note canonique créée** : [[programmatic-tool-calling]] (orchestration code Python, sandbox Anthropic, principe "code orchestre / modèle juge", comparaison sub-agents Justin Young, métriques verbatim docs)
- **Note référence créée** : [[google-eng-practices]] (4 docs Google CL/small-CLs/handling-comments, applicabilité forge calibrée — Small CLs principle convergent, handling reviewer comments peu applicable forge perso)
- **Append [[workflow-claude-code-optimal]]** : section PTC + lien vers note canonique
- **Append [[comment-creer-agent]]** : section PTC alternative aux sub-agents

Méta-prompt bibliothèque non touché — il prendra automatiquement les nouvelles notes au prochain run (read vault entier).

## [2026-05-23] audit | thème prompt engineering — 14 notes corrigées, 24 modifs

Audit méthodique 17 notes thème prompt-engineering (`04-Techniques/prompt-engineering/` + `07-Prompts/`). 57 claims auditées, 6 sub-agents parallèles par cluster + 4 self-verify WebFetch direct.

- **Notes modifiées (14)** : Adaptive Thinking, Effort Levels Guide, System Prompt Design, amanda-askell-prompt-engineering, deprecated-techniques-2026, forge-prompt-machine, opus-47-design-defaults, outcome-first-prompting, over-specification-paradox, prompting-chat-cowork-code, System Prompt Amanda Askell, System Prompt Claude Code, chain-of-thought, few-shot-prompting
- **Drifts Type 1/2 corrigés** : verbatim OpenAI fabriqué (cité 2× dans vault), Sculpting paper attribution Khan PAS Mikinka, "30 000 mots" → "35 000+ tokens", "157 versions" → "186+", "Let's think step by step" sourcé Kojima 2022, ALL-CAPS exception inversée vs verbatim Anthropic
- **Outputs** : `output/audit-vault-thematique/02-prompt-engineering/` (A-inventaire + 6 rapports clusters + C-croisement + D-plan + 0-experts)

## [2026-05-23] add | 11 nouvelles fiches leaders (prompt + industrie)

Suite à phase 0 audit prompt engineering : création fiches leaders identifiés mais absents du vault.

- **05-Leaders/prompt/** : Sander Schulhoff, Riley Goodside, Elvis Saravia, Jason Wei, Denny Zhou, Takeshi Kojima, Imran Khan, Anthony Mikinka, Yann LeCun, Ethan Mollick
- **05-Leaders/industrie/** : Geoffrey Hinton, Yoshua Bengio, Demis Hassabis, Ilya Sutskever, Reid Hoffman, Allie K. Miller

Yann LeCun en `prompt/` malgré position critique LLM (essentiel pour balance idéologique). Karpathy / Willison / Mollick déjà ailleurs — cross-référence via wikilinks.

## [2026-05-23] audit-thematique | 03-rag — 78 claims, 11 ❌ + 34 ⚠️ corrigées

- Méthode 6 étapes audit Claude Code 23 mai appliquée (sub-agents par cluster, checkpoint, self-verify, Type 1/2/3)
- 10 notes modifiées + 3 squelettes enrichis (rag-evaluation, rag-production, ColPali)
- Corrections critiques : TOOLQP date 2026 (pas 2025), MCP-Zero URL corrigée, Gemini 1.5 Pro NIAH multi-fact (inversion), Karpathy verbatim canonique, cache cosine 0.80 (pas 0.95)
- Liens : [[RAG]] [[rag-architecture]] [[tool-retrieval-query-expansion]] [[pattern-vault-llm-karpathy]]
- Output : `output/audit-vault-thematique/03-rag/`

## [2026-05-23] post-audit-rag | fiches leaders + capitalisation erreurs

- Créées : [[Jerry Liu]] (LlamaIndex CEO) et [[Harrison Chase]] (LangChain CEO) dans 05-Leaders/rag/
- Créée : [[erreur-audit-rag-11-faux-2026-05-23]] synthèse 11 FAUX + 6 patterns récurrents
- Mémoire forge : 2 nouveaux feedbacks (arxiv-id-yymm-format, arxiv-url-swap)
- Liens : [[RAG]] [[Jerry Liu]] [[Harrison Chase]] [[erreur-audit-rag-11-faux-2026-05-23]]
