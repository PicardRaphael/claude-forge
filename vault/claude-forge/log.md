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