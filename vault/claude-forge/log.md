---
titre: "Log vault forge-brain — append-only Karpathy"
resume: "Log append-only format Karpathy strict ## [YYYY-MM-DD] action | titre. Trace atomique des operations Ingest / Query / Lint sur le vault. JAMAIS modifie retroactivement."
aliases:
  - "log vault"
  - "log karpathy"
  - "log append-only"
  - "trace vault forge"
  - "vault operations log"
derniere-maj: 2026-05-27
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

## [2026-05-27] chantier | Étape 3 — durcissement hooks (faux positif chaînage + angle mort PowerShell)
- Corrigé `vault-cat-guard.py` : segmentation sur &&/||/;/| avant détection — read-command + marker vault doivent co-occurrer dans le MÊME segment. Faux positif `git add "vault/..." && git push | tail` résolu (découvert en commitant l'étape 2b)
- Corrigé `security-guard.py` : matcher `Bash` → `Bash|PowerShell` (angle mort — git push --force via PowerShell contournait le garde). Code is_dangerous déjà cross-shell, fix = routing
- Audit transverse PowerShell sur hooks PreToolUse Bash-only : seul security-guard vulnérable (vault-cat-guard fermé 2b ; delegate-guard/meta = Edit|Write|MultiEdit hors sujet ; mcp-alias = MCP)
- note-updated `hook-intercepte-mcp-et-read-tools` : settings.json relu à chaud confirmé empiriquement
- Tests : 180 verts (170 + 7 chaînage + 3 cross-shell). Dette tracée : cmdlets PS-natifs destructeurs (Remove-Item) non couverts
- Méta : 2 failles de vault-cat-guard découvertes par usage réel (sur-blocage Read main en 2b + faux positif chaînage en 3). Pattern « les vrais faux positifs émergent à l'usage »
- Méthode : A→B→C→D→E + advisor + 2 AskUserQuestion (fix security-guard + verdict /probe-tool)

## [2026-05-27] chantier | Étape 2b — fix structurel MCP décoratif sub-agent
- Créé hook `.claude/hooks/vault-cat-guard.py` : bloque accès brut vault (cat/grep/find/Get-Content/Read). Bash/PowerShell 2 contextes, Read sub-agent only, exempt vault-maintainer. 46 tests
- Créé hook `.claude/hooks/mcp-alias-guard.py` : bloque `append_note(file=<stem ambigu>)` (log/index/CHANGELOG multi-dossiers). 23 tests
- Enregistré les 2 hooks dans `settings.json` (matchers `Bash|Read|PowerShell` et `mcp__forge-brain__append_note`)
- Durci 6 creators (`agent-creator` édit direct via bypass `.new`+`mv`, puis `skill-creator`/`hook-creator`/`claudemd-optimizer`/`repo-inspector`/`responsable-ia` en cascade via agent-creator) : directive « lire EN ENTIER via MCP » → brief inline + ESCALADE + interdiction accès vault brut
- note-created `01-Claude/Code/best-practices/hook-intercepte-mcp-et-read-tools.md` (preuve PreToolUse intercepte MCP/Read/PowerShell + méthode probe + exceptions delegate-guard)
- note-updated `comment-creer-skill` / `comment-creer-agent` / `comment-creer-hook` : section Brief sub-agent et accès vault ; + section bypass self-modification dans comment-creer-agent
- Empirique : 3 probes (matcher MCP, Read, PowerShell tous interceptés) ; vault-cat-guard a bloqué mes propres Read/PowerShell sur le vault en conditions réelles (preuve fonctionnelle)
- Tests : 170 verts (101 baseline + 69 nouveaux). Zéro régression
- Dette résiduelle : cas spéciaux vault-maintainer + devils-advocate (métier = écrire le vault) reportés
- Méthode : A→B→C→D→E + advisor (4 appels) + AskUserQuestion (2 STOP arbitrage). Commits non lancés, validation groupée demandée

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

## [2026-05-23] audit-thematique-fine-tuning | 22 corrections sur 87 claims (9 notes patchees)

- 7 sub-agents paralleles WebFetch direct : PEFT / Alignment / Frameworks / Infra / Models / Privacy+RAG / Datasets+Eval
- Type 1 (8 cas) : venues inventees (intruder dimensions arXiv 2410.21228 sans NeurIPS), SimPO/KTO auteurs, Gemma 3 tailles+license, TrueFoundry Medtronic->ResMed
- Type 2 (10 cas) : stars GitHub drift x3-x6 (DeepEval 5K->15.6K, MLX 4K->26K, Unsloth 54K->65K), chiffres -36
## [2026-05-23] audit-thematique-fine-tuning | 22 corrections sur 87 claims (9 notes patchees)
- 7 sub-agents paralleles WebFetch direct : PEFT / Alignment / Frameworks / Infra / Models / Privacy+RAG / Datasets+Eval
- Type 1 (8 cas) : venues inventees (intruder dimensions arXiv 2410.21228 sans NeurIPS), SimPO/KTO auteurs, Gemma 3 tailles+license, TrueFoundry Medtronic vers ResMed
- Type 2 (10 cas) : stars GitHub drift x3-x6 (DeepEval 5K vers 15.6K, MLX 4K vers 26K, Unsloth 54K vers 65K), chiffres -36%/-50%/5x retires, pricing precise
- Type 3 (4 cas) : torchtune no longer maintained, TGI archive 21 mars 2026, EU AI Act delay mai 2026, Lamini scoping case study
- Creee : [[erreur-audit-fine-tuning-2026-05-23]]
- Liens : [[fine-tuning-techniques-peft]] [[fine-tuning-alignment]] [[fine-tuning-frameworks]] [[fine-tuning-infrastructure]] [[fine-tuning-models]] [[fine-tuning-privacy]] [[fine-tuning-datasets]] [[fine-tuning-evaluation]] [[rag-vs-fine-tuning]]

## [2026-05-27] cleanup | Phase 1 forge (DA effort, EXAMPLES upstream, settings, doc, tests)
- Fix effort devils-advocate : body xhigh supprime, frontmatter high fait foi
- Capitalisation [[comment-creer-agent]] section "Frontmatter vs body : alignement obligatoire"
- Restauration json-canvas/references/EXAMPLES.md verbatim depuis upstream kepano/obsidian-skills (pas de fabrication)
- Coquille settings.json Bash(taskkill *) + bloc ask operations destructives
- Decision P2.6 : skills cc-*-ref user-invokable:false = MAINTENIR (non orphelines, referencees body createurs)
- Tests pytest 90/90 PASSED (69 MCP + 21 hooks, 0 echec)
- Creee : [[erreur-deny-global-ecrase-allow-projet]]

## [2026-05-27] tests-adverses | Phase 2 hooks critiques (security-guard + delegate-guard)
- test_security_guard.py : 26 tests, ratio adverse/happy 5.3:1 (in-scope bypass + 5 false-negatives prouves : uppercase/tilde/$HOME/glob/relatif)
- test_delegate_guard.py : 28 tests, ratio 8:1 (path tricks, impostors agent_type/agent_id, smuggle typo)
- Refactor security-guard : main() garde (testabilite, comportement detection inchange)
- Bug caracterise : delegate-guard L143-145 substring match agent_id = bypass indu (surface faible, agent_id fixe harness)
- Capitalisation [[comment-creer-hook]] etape 5 : regle ratio >=3:1 + piege 3:1 artificiel + caracterisation bug
- Tests repo : 90 -> 122 PASSED

## [2026-05-27] fix | delegate-guard substring agent_id durci + pattern fix-trivial
- Fix delegate-guard via hook-creator : suppression substring match agent_id (L143-145), exact-match conserve
- Test caracterise inverse en regression guard (test_agent_id_substring_does_not_grant_bypass), pas supprime
- E2E verifie : faux bypass substring -> bloque (exit 2), bypass legit -> passe (exit 0)
- Creee : [[bug-caracterise-fix-trivial-vs-couteux]] (pattern decisionnel fix immediat vs phase dediee)
- Tests repo : 122 -> 123 PASSED

## [2026-05-27] chantier | Phase 3 renforcement (audit 5 axes + tests coeur)
- Audit 5 axes (vitrine, tests, portabilite, versioning, ADR). Advisor : 1 seul P0 reel.
- P0 : tests coeur MCP search() 4 strategies + resolve 3 tiers + suggest/tags/property (test_search 18, test_resolve 19). MCP 69 -> 106.
- P1 : tests logique hooks session-health (seuils 2/20/40) + skill-activation (word-boundary). Hooks 76 -> 101.
- Caracterise : resolve_note tier 2 substring bat tier 3 prefixe (pinne, pas un bug).
- Creees : [[phase-3-renforcement-audit]] (0-Inbox, matrice) + [[decision-renforcements-differes-phase-3]] (ADR P2/P3 + declencheurs).
- Tests repo : 145 -> 207 PASSED. 0 regression.

## [2026-05-27] note-updated | audit-puis-vagues-paralleles : section Phase 3bis symetrie artificielle
- Ajout section "Phase 3bis — Pas de symetrie artificielle entre axes" dans la canonique audit/priorisation
- Pattern meta observe 2x (Phase 2 ratio 3:1 artificiel, Phase 3 advisor 1 P0 / 5 axes)
- Test de discrimination : risque reel/present vs theorique, impact maximal vs cosmetique
- Capitalise aussi en feedback memoire [[feedback_pas_de_symetrie_artificielle_priorisation]]

## [2026-05-27] note-updated | comment-creer-skill : pattern skill propose un diff a valider (A3)
- Ajout section "Pattern skill qui propose un diff a valider" + corollaire skill de jugement LLM non testable unitairement
- Skill done enrichie via skill-creator (304->310L) : generation de blocs + boucle validation [v]/[m]/[i]
- Roadmap Phase 4 : A3 marque FAIT (statut d'implementation)
- Capitalise en feedback memoire [[capitalisation-proposee-pas-auto]]

## [2026-05-27] Ingest | Phase 4 A1 — MCP search_sessions (recherche transcripts session)
- 22e outil forge-brain : `search_sessions(query, limit, project, role, since)` — FTS5 sur ~/.claude/projects/*.jsonl bruts non capitalises
- Code : mcp-forge-brain/src/sessions_indexer.py + sessions_db.py + sessions_watcher.py ; methode + @_tool dans src/tools/brain.py ; config sessions.{enabled,path,include_subagents}
- Table FTS5 separee session_messages (concerns vs notes_fts), watcher incremental mtime, eager au boot mesure 2.68s (243 transcripts, 15858 messages, subagents exclus configurables)
- Tests : test_sessions_indexer.py (18) + test_sessions_search.py (19) = 37, ~60% adverse, 0 regression (244 verts : 101 hooks + 143 MCP)
- Capitalise note canonique [[ajouter-source-donnees-mcp-forge-brain]] ; roadmap A1 FAIT ; CLAUDE.md + forge-brain-proactive + skill forge-brain MAJ 22 outils

## [2026-05-27] Ingest | Mémoire portable — claude-forge self-contained
- Migration mémoire ~/.claude/projects/<repo>/memory/ -> <repo>/memory/ (240 fichiers versionnés). Mécanisme : autoMemoryDirectory (user-scope, par machine) ; contenu suit le clone, pointeur local
- ADR actée [[decision-memoire-dans-le-repo]] (remplace l'ADR en attente) ; [[decision-settings-global-modification-manuelle]]
- Audit confidentialité empirique : mdp PostgreSQL prod + IP serveur committés en clair (GitHub claude-forge + Bitbucket ia_back). Redactés de HEAD dans 5 fichiers (2 memory + 3 vault). TODO P0 [[todo-rotation-password-postgres-prod]] (rotation = seul fix réel)
- Réconcilié dossier résiduel .claude/projects/ (3 fichiers obsolètes d'essai antérieur, git rm)
- Feedback [[claude-forge-self-contained-rien-hors-clone]] ; baseline tests vérifié empiriquement 244 (143 MCP + 101 hooks)
- EN ATTENTE test natif (autoMemoryDirectory appliqué à la main) avant adaptation /done /recap session-reminder.py install-forge

## [2026-05-27] Build | Mémoire portable étape 7-9 — composants adaptés + doctrine path
- Pivot du mécanisme : autoMemoryDirectory (cassé en multi-repos) -> `@memory/MEMORY.md` dans CLAUDE.md versionné (L100). Test @import validé empiriquement (231 lignes chargées depuis `<repo>/memory/`)
- Découverte non anticipée : l'@import AJOUTE une source, ne remplace pas l'auto-memory native. Double-source transitoire (231L repo vs 229L native tronquée) acceptée comme dette tracée. Feedback [[import-ajoute-pas-remplace-automemory]]
- 5 composants adaptés : /done (bloc PROJECT_ID supprimé, dédup+écriture via git rev-parse), /recap (dépendance $(claude-project-id) éliminée), session-reminder.py (glob ~/.claude/projects/* -> chemin déterministe __file__), install-forge (section Mémoire portable), CLAUDE.md (session précédente)
- Doctrine 4-contextes de résolution de path capitalisée : note canonique [[resolution-path-3-contextes]] (skill=git rev-parse, hook=__file__, settings=${CLAUDE_PROJECT_DIR} expansion harness, .mcp.json=relatif) + amendements [[comment-creer-skill]] et [[comment-creer-hook]] wikilinkés
- Test cross-machine probant (clone C:\temp\forge-test lit sa propre mémoire via __file__ et git rev-parse, pas l'origine). 244 tests verts, 0 régression
- Raisonnement [[architecture-decision-memoire-portable-import]] enrichi du résultat de test. Suivant = DA sur A1×A3 en session dédiée

## [2026-05-27] Query | DA compounding rétroactif (A1×A3) — idée tuée par probe empirique
- Devils-advocate sur le croisement A1×A3 (scanner les transcripts passés à /done). Méthode A→B→C→D→E + probe empirique sur 123 transcripts / 9631 messages via parseur réel `sessions_indexer`
- Donnée décisive : échantillon 12 hits sur la slice la plus chargée (`erreur|decision|pivot`) = 0/12 capitalisable-ET-nouveau (~8 bruit, ~4 déjà capitalisé). Verdict (c) tuer — échec de prémisse, pas de calibration
- Risque structurel n°1 = circularité C5 : l'indexeur garde les messages /done en clair (135 msg / 1,4% citent déjà un feedback_*.md) → ils remontent comme faux apprentissages. By-design
- Pivot retenu : `/recall-uncaptured <topic>` on-demand (design différent, pas garde-fou), à valider empiriquement. Note [[critique-2026-05-27-compounding-retroactif]], idée [[idee-compounding-retroactif]] amendée, feedback [[da-probe-empirique-avant-verdict]]

## [2026-05-27] audit | Audit transverse conformité doctrinale claude-forge
- 78 composants audités sur 9 critères (mémoire, path resolution, dépendances fragiles, meta-commentaire, frontmatter↔body, doctrine, code mort, wikilinks, chemins portables) : 11 agents, 47 skills, 9 hooks, 10 rules, CLAUDE.md. 94% conformes d'emblée — 5 résidus isolés, aucun pattern systémique
- Méthode A→B→C→D→E avec STOP étape D. Oracle de classification meta-commentaire = le hook [[meta-commentary-detector]] lui-même passé en scan sur tout son scope (`check_content`) → 2 hits réels. pyflakes sur hooks → 1 hit. Croisement wikilinks ⨯ existence vault MCP → 1 hit. Couleurs vs convention → 1 hit
- 5 corrections déléguées + vérifiées empiriquement : [[agent-creator]] wikilink mort `[[agents-orchestration]]`→`[[agents-architecture]]` ; responsable-ia `pink`→`purple` ; notes/SKILL `Source :`→`Référence :` ; mcp-brief-then-direct/SKILL retrait `(validé 26 mai 2026)` ; mcp-autostart.py imports orphelins `json`/`os`. 244 tests verts, 0 régression
- Cas ambigus tranchés = garder : `~/.claude/projects/` dans [[cc-features-ref]] (doc feature native CC, fait exact), `tip #1` dans skills cc-*-ref (documentaires, hook exempte), `(Boris)`/`(Anthropic)` ≤3 mots (tolérés)
- Capitalisation : feedback mémoire `audit-transverse-periodique-hooks-gardes-ecriture` (hooks = gardes en écriture, pas scanners périodiques). Cf [[erreur-meta-commentaires-composants]], [[resolution-path-3-contextes]]. Pas de commit (Raphael décide)
## [2026-05-27] note-updated | SELF_PORTRAIT régénéré + context-actuel + CHANGELOG
- `CLAUDE_FORGE_SELF_PORTRAIT.md` (racine repo, hors vault) régénéré 630L en update chirurgical par delta de section (pas rewrite). Ancien portrait (commit `4332182`, même jour) périmé : 262 commits/207 tests + 3 valeurs de notes divergentes (412/412/417)
- Métriques remesurées et unifiées sur source unique `vault_stats` : 302 commits, 244 tests (101 hooks + 143 MCP), 22 outils MCP, 430 notes vault, 193 feedbacks memory
- Nouvelle section 8bis "Système de veille" : cc-news (Tier 0 + 11 agents / 6 spécialités) + 80 fiches leaders + 3 chantiers (A pont veille→doctrine P-haute, B checklist vendredi P-basse, C sync leaders P-moyenne)
- Section Hermes déplacée du corps vers annexe B condensée (choix Raphael) : corps décrit forge en lui-même, pointeur [[phase-4-comparaison-hermes-roadmap]]
- Dette double-source mémoire tracée (section 12, déclencheur explicite) ; A3/A1 livrés + A1×A3 tué reflétés section 8 ; doctrine 4-contextes [[resolution-path-3-contextes]] + mémoire portable [[decision-memoire-dans-le-repo]] section 9
- Méthode A→B→C→D→E avec STOP étape D + advisor() avant écriture. Mis à jour [[context-actuel]] + [[CHANGELOG]]. Pas de commit (Raphael décide du découpage)

## [2026-05-27] chantier | Pont veille→doctrine Paquet 1 livré (Chantier A)
- Créé note canonique [[doctrine-vivante]] (04-Techniques/claude-code) — moteur externe d'évolution doctrinale (signal externe, pas seulement erreur interne), 3 verdicts (INFO/DOCTRINE_PIVOT_CANDIDATE/DOCTRINE_REINFORCE), gate humaine non négociable, scan aveugle interdit (lien probe 0/12 [[critique-2026-05-27-compounding-retroactif]])
- Créé skill `doctrine-impact-check` (156L, opus) — opérationnalise [[doctrine-vivante]] : croise un finding dirigé avec les canoniques, brouillon argumenté + gate [v]/[m]/[i], n'appelle jamais [[methode-pivoter-doctrine]] directement. 3 TODO différés (C5/C6/C7)
- Ajouté étape 8 à skill `cc-news` : invoque doctrine-impact-check sur findings MAJEURS (leader/Anthropic) only, anti-cascade
- Bug découvert en cours : MCP forge-brain décoratif en sub-agent (`No such tool available`, confirmé 2 agents skill-creator + hook-creator) → dette étape 2b (fix briefs 6 creators + hook vault-cat-guard + note canonique subagent-mcp-non-herite). Workaround appliqué = mcp-brief-then-direct inline
- Méthode A→B→C→D→E + advisor avant conception, 2 paquets (Core livré, C4-C7 différés). Pas de commit auto (Raphael décide)