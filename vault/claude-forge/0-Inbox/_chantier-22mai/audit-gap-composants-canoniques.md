---
titre: "Audit gap composants .claude/ vs 8 canoniques 22 mai 2026"
resume: "Audit read-only des 11 agents, 34 skills, 19 hooks, 9 rules, CLAUDE.md, settings.json du repo claude-forge confrontés aux 8 notes canoniques produites le 22 mai 2026."
aliases:
  - "audit gap canoniques 22 mai"
  - "audit composants forge 22 mai"
  - "gap analysis claude-forge"
derniere-maj: 2026-05-22
auteur: claude
type: audit
tags:
  - "#type/audit"
  - "#domaine/claude-code"
  - "#chantier/22mai"
---

# Audit gap composants `.claude/` vs 8 canoniques

**Repo** : `C:\Users\raphael.picard_neote\Documents\claude-forge\`
**Date** : 2026-05-22
**Périmètre** : 11 agents, 34 skills, 19 hooks Python, 9 rules, CLAUDE.md (84L), settings.json + settings.local.json
**Méthode** : read-only, confrontation aux 8 canoniques (comment-creer-skill, comment-creer-agent, comment-creer-hook, comment-ecrire-claudemd, workflow-claude-code-optimal, methode-analyser-repo, mcp-vs-skills-doctrine, pattern-vault-llm-karpathy)

Priorités : **P0** = bloquant doctrinal/sécurité · **P1** = écart majeur · **P2** = polish

---

## 1. Agents (`.claude/agents/*.md`) — 11 fichiers

| Agent | model | effort | color | memory | permMode | Gaps détectés | P |
|-------|-------|--------|-------|--------|----------|---------------|---|
| **agent-creator** | sonnet | high | pink | project | acceptEdits | RAS — conforme canonique | — |
| **skill-creator** | sonnet | high | pink | project | acceptEdits | RAS | — |
| **hook-creator** | sonnet | high | pink | project | acceptEdits | **Body référence "Pattern marker + guard" comme bonne pratique** (l. 13) — contredit doctrine 22 mai (anti-pattern) | **P0** |
| **claudemd-optimizer** | sonnet | high | pink | project | acceptEdits | Ne référence pas `obsidian-markdown` dans son body alors qu'elle est en `skills:` (3 refs au lieu de 4 attendues) | P2 |
| **devils-advocate** | opus | xhigh | red | project | acceptEdits | `effort: xhigh` cohérent (jugement) mais hors liste restreinte (architect/dev-lead/refactor-pg) — canonique autorise pour DA implicitement. RAS | — |
| **outcomes-grader** | opus | high | yellow | project | plan | `permissionMode: plan` rare mais légitime (read-only grader). `disallowedTools` complet (Write/Edit/Bash/Agent). Conforme | — |
| **project-analyzer** | opus | xhigh | purple | project | (manque !) | **`permissionMode` absent du frontmatter** — viole canonique "OBLIGATOIRE". `effort: xhigh` sur purple analyzer hors liste restreinte (canonique : architect/dev-lead/refactor-pg) | **P0** + P1 |
| **project-auditor** | opus | xhigh | purple | project | plan | Idem : `effort: xhigh` non listé pour purple analyzer. Sinon conforme | P1 |
| **python-dev** | opus | xhigh | green | project | acceptEdits | **`effort: xhigh` non justifié** — canonique réserve xhigh à architect/dev-lead/refactor-pg. Devrait être `sonnet`+`high` (exécution) ou `opus`+`high`. Sur-coût + over-thinking risk | **P0** |
| **self-updater** | sonnet | high | cyan | project | acceptEdits | RAS | — |
| **vault-maintainer** | sonnet | high | cyan | project | acceptEdits | RAS — 12 refs skills dans body | — |

**Observation transverse** :
- Tous les agents ont `memory: project` ✅
- Tous les agents ont `color` ✅
- 10/11 ont `permissionMode` ✅ — `project-analyzer` manquant
- Skills frontmatter cohérent avec body (sauf claudemd-optimizer mineur)
- Aucun agent CTO orchestrateur ✅ (anti-pattern absent)

---

## 2. Skills (`.claude/skills/*/SKILL.md`) — 34 fichiers

| Skill | Lignes | user-invokable | Gaps | P |
|-------|--------|----------------|------|---|
| analyze-project | 91 | true | RAS | — |
| cc-advisor | 96 | true | RAS | — |
| cc-agents-ref | 117 | false | Référencé dans agent-creator body ✅ | — |
| cc-cowork-ref | 298 | false | **Pas référencé dans le body d'un agent parent** (skills:) → orpheline potentielle (cf feedback_non_invokable_skills_orphan) | P1 |
| cc-features-ref | 251 | false | Référencé via claudemd-optimizer / project-analyzer ✅ | — |
| cc-hooks-ref | 216 | false | Référencé dans hook-creator ✅ | — |
| cc-news | 144 | true | `skills: [x-read]` et `x-read` est référencé dans body ✅ | — |
| cc-prompt-ref | 197 | false | Référencé dans project-auditor ✅ | — |
| cc-skills-ref | 154 | false | Référencé dans skill-creator ✅ | — |
| config-guardian | 98 | true | Pas de `model`/`effort` → mais skill, optionnel | — |
| configure-claude-desktop | 87 | (manque) | `user-invokable` non spécifié — défaut OK | P2 |
| craft-prompt | 148 | true | RAS | — |
| defuddle | 41 | (manque) | Pas de `user-invokable` — comportement par défaut | P2 |
| done | 288 | true | RAS | — |
| evolve | 227 | true | RAS | — |
| expand | 48 | (manque) | Pas de `user-invokable`, pas d'`allowed-tools` | P2 |
| forge-brain | 141 | (manque) | Pas de frontmatter `user-invokable` ni `allowed-tools` | P2 |
| forge-review | 240 | true | RAS | — |
| forge-status | 42 | true | RAS | — |
| install-forge | 50 | true | RAS | — |
| json-canvas | 244 | (manque) | Pas de `user-invokable`/`allowed-tools` | P2 |
| notes | 134 | true | RAS | — |
| obsidian-bases | **376** | (manque) | Body conséquent — proche limite 500L mais OK. Pas de `references/` extraite (à surveiller) | P2 |
| obsidian-markdown | 197 | (manque) | OK (skill standard portée Obsidian) | — |
| outcomes-test | 138 | true | RAS | — |
| python-ref | 183 | **true** | **Incohérence** : skill de référence chargée par agent `python-dev` (skills frontmatter), devrait être `user-invokable: false` comme cc-*-ref | P1 |
| reasoning-cache | 171 | true | RAS | — |
| recap | 165 | true | RAS | — |
| self-check | 45 | true | RAS | — |
| skill-evolve | 230 | true | RAS | — |
| spec | 147 | true | Référence `neo-brain-dev-ia` (skill projet externe) dans `skills:` — référence cross-repo, OK | — |
| vault-audit | 163 | true | RAS | — |
| watch | 205 | true | RAS | — |
| x-read | 134 | true | RAS | — |

**Aucune SKILL.md > 500L** ✅ (max 376 sur obsidian-bases)
**Catégories Thariq** : forge a beaucoup de skills méta (création, audit, veille) — entrent dans Cat. 4 (Process), Cat. 6 (Quality), Cat. 5 (Scaffolding). Légitime.

---

## 3. Hooks (`.claude/hooks/*.py` + settings.json) — 19 scripts

| Hook | Event | Matcher | Gap | P |
|------|-------|---------|-----|---|
| **delegate-guard** | PreToolUse | `Edit\|Write` | **Manque `MultiEdit`** — trou architectural canonique | **P0** |
| **vault-query-guard** | PreToolUse | `Write` | **Manque `Edit` + `MultiEdit`** — trou double | **P0** |
| security-guard | PreToolUse | `Bash` | OK (security/scope) | — |
| vault-before-specialist | PreToolUse | `Agent` | OK | — |
| vault-write-tracker | PostToolUse | `Write\|Edit\|MultiEdit` | ✅ triplet complet | — |
| vault-query-tracker | PostToolUse | `Read\|Grep\|Glob\|Skill\|mcp__...` | OK | — |
| devil-advocate-tracker | PostToolUse | `Agent` | OK | — |
| devil-advocate-guard | PostToolUse | `Agent` | OK | — |
| reasoning-cache-reminder | PostToolUse | `Agent` | OK | — |
| learning-reminder | Stop | — | `once:true` ✅ | — |
| devil-advocate-stop | Stop | — | `once:true` ✅. **Cependant : workflow agentique (gate DA en fin de session)** — canonique 22 mai classe DA pipeline comme advisory CONDITIONNEL, pas systématique. Hook qui force DA sur tout = anti-pattern doctrinal | **P1** |
| proactivity-reminder | Stop | — | `once:true` ✅ | — |
| session-health | UserPromptSubmit | — | OK | — |
| skill-activation | UserPromptSubmit | — | OK | — |
| session-reminder | SessionStart | — | OK | — |
| mcp-autostart | SessionStart | — | `async:true` ✅ | — |
| session-reset-vault-marker | SessionStart | — | **Marker pipeline pour workflow vault** — canonique 22 mai (feedback_marker_ttl_pattern, raisonnement-22mai-doctrine-vs-enforcement) déconseille markers de workflow. Légitime ici (security/scope vault) mais à challenger | P2 |

**Sous-pipeline vault `marker+guard`** : session-reset-vault-marker (SessionStart) → vault-query-tracker (PostToolUse marker write) → vault-query-guard (PreToolUse exit 2 si marker absent). **Architecture identique au pattern markers banni d'ia_back/neo_ia le 22 mai**. À évaluer : est-ce security (légitime) ou workflow (anti-pattern) ? La canonique permet hooks vault PreToolUse pour scope/security — mais imposer "tu DOIS avoir consulté le vault avant d'écrire" = workflow agentique, pas security. **P0 doctrinal**.

**Hook qui pourrait être problématique** :
- `devil-advocate-guard` + `devil-advocate-stop` = pipeline DA-systématique, alors que canonique dit DA CONDITIONNEL. P1.
- Pas d'`asyncRewake` détecté (cohérent — pas utilisé)
- Pas de `PreEdit/PostEdit/PreWrite/PostWrite` inventés ✅ — tous via PreToolUse/PostToolUse matcher
- Chemins Python : `python "$(git rev-parse --show-toplevel)/.claude/hooks/X.py"` — **chemin relatif via PATH** : sur Windows, alias MS Store → bug potentiel (cf feedback_python_path_windows). Canonique exige path absolu. **P0 Windows**.

---

## 4. Rules (`.claude/rules/*.md`) — 9 fichiers

| Rule | Frontmatter `description:` | Cohérence doctrine 22 mai | P |
|------|---------------------------|---------------------------|---|
| agents-color-convention.md | **MANQUANT** | OK | **P1** |
| changelog-vault.md | **MANQUANT** | OK | **P1** |
| check-before-create.md | ✅ | OK | — |
| comportement-proactif.md | ✅ | OK | — |
| delegate-to-specialists.md | ✅ | OK | — |
| devils-advocate-pipeline.md | ✅ | **DA présenté comme OBLIGATOIRE** sur livrables majeurs → canonique 22 mai dit CONDITIONNEL. Section "Pipeline complet" inclut DA en gate systématique = anti-pattern doctrinal | **P0** |
| forge-brain-proactive.md | ✅ | OK | — |
| memory-discipline.md | ✅ | OK | — |
| vault-consultation-protocol.md | **MANQUANT** | OK | **P1** |

**3 rules sans frontmatter** = mortes silencieusement (cf feedback_rules_frontmatter_mandatory). Critique car ce sont des règles utilisées (agents-color-convention notamment).

---

## 5. CLAUDE.md (racine)

**Taille : 84 lignes** ✅ (target < 200, recommandation Boris ~100)

**Anti-patterns vérifiés** :
- ❌ Kitchen sink : non, sections claires
- ❌ Correcting over and over : risque modéré — sections "Devil's advocate" répétée 3× (gotchas l.77/78/79)
- ❌ Over-specified : OK
- ❌ Trust-then-verify gap : section "Hooks > Rules" cite ~80% advisory mais ne précise pas quelles règles critiques sont doublées par hook
- ❌ Infinite exploration : OK
- ❌ Routing dans CLAUDE.md : OK — délégué à `.claude/rules/comportement-proactif.md`
- ❌ STOP critique en gotchas fin : oui — règles Devil's advocate critiques (l.77-80) en gotchas fin, devraient être < ligne 25. **P1**

**Gaps doctrine 22 mai** :
- l.31 "règle advisory = ~80% compliance. Chaque règle critique DOIT être doublée d'un hook exit 2" — **contredit pivot 22 mai** : hooks workflow agentique sont anti-pattern. Phrase doit être nuancée : hooks pour lint/security/scope, PAS pour workflow. **P0**
- l.35 "Rules : architect-first OBLIGATOIRE (même taille S). Gates : test-writer → code-reviewer" — pipeline systématique anti-pattern doctrine 22 mai. **P0**
- l.36 "CLAUDE.md : ~100L max" : cohérent avec canonique ✅
- l.26 `effort: xhigh = défaut Opus 4.7` — canonique 22 mai a révisé : xhigh RÉSERVÉ architect/dev-lead/refactor-pg, high partout ailleurs. **P0**

**Sections additionnelles attendues canonique CLAUDE.md** :
- Stack ❌ absent (forge = méta-repo, légitime mais à mentionner)
- Commandes fréquentes ❌ absent
- Things to leave alone ❌ absent

---

## 6. Settings.json + settings.local.json

**settings.json (project, versionné)** :
- Permissions Bash format correct : `Bash(git *)`, `Bash(ls *)` avec espace ✅
- Pas de chemins absolus user-specific dans le project settings ✅
- Hooks chemins : `$(git rev-parse --show-toplevel)` — **astuce portable** mais résout `python` via PATH (Windows alias MS Store risk). **P0** (cf section hooks).

**settings.local.json** :
- 4 permissions PowerShell hardcodées avec path absolu `C:\Users\raphael.picard_neote\...` — légitime (settings.local non-versionné par défaut)
- Permission `Bash(cat > *)` — overly broad, à surveiller (peut bypasser delegate-guard via cat redir) **P1**
- Permission cross-repo `Bash(cd C:/Users/raphael.picard_neote/Documents/neot-v2/* && git *)` — scope élargi, intentionnel ?

**enabledMcpjsonServers: ["forge-brain"]** ✅
**enableAllProjectMcpServers: true** ✅

---

## 7. Utilisation MCP forge-brain

**Agents qui utilisent MCP forge-brain dans body** :
- `vault-maintainer` ✅ (Etape 0 — MCP forge-brain obligatoire)
- `agent-creator`, `skill-creator`, `hook-creator`, `claudemd-optimizer` : `forge-brain` en `skills:` frontmatter, référencée dans body via skill `forge-brain` (qui sait utiliser MCP)
- `project-auditor`, `project-analyzer`, `self-updater` : idem

**Skill `forge-brain`** : utilisée comme proxy d'accès au MCP par tous les agents. Cohérent.

**Agents sans MCP forge-brain** :
- `devils-advocate` : `tools: Read, Grep, Glob, Bash` — peut accéder au vault via Read direct = **anti-pattern** (cf rule forge-brain-proactive : "Ne JAMAIS utiliser CLI Obsidian, Grep ou Read brut sur le vault"). Devrait avoir MCP tools. **P1**
- `outcomes-grader` : read-only, n'a pas besoin du vault sauf si rubrique vaultée — OK
- `python-dev` : pas de vault accès, légitime

**Rule `forge-brain-proactive.md`** : référencée ✅ (par claude-md / agents).

---

## 8. VERDICT GLOBAL — Top 10 gaps prioritaires

| # | Gap | Niveau | Effort | Composant |
|---|-----|--------|--------|-----------|
| 1 | **Hooks matcher `Edit\|Write` sans `MultiEdit`** sur `delegate-guard` et `vault-query-guard` — trou architectural canonique | **P0** | S | `.claude/settings.json` |
| 2 | **Chemins Python `python` (PATH) au lieu de chemin absolu** dans tous les hooks settings.json — risque Windows MS Store alias | **P0** | S | `.claude/settings.json` (19 entrées) |
| 3 | **CLAUDE.md contredit doctrine 22 mai** : promeut "chaque règle critique DOIT être doublée d'un hook exit 2" + "architect-first OBLIGATOIRE" + "effort xhigh par défaut" | **P0** | M | `CLAUDE.md` l.31/35/26 |
| 4 | **`hook-creator` body** référence "Pattern marker + guard" comme bonne pratique alors que doctrine 22 mai le classe anti-pattern | **P0** | S | `.claude/agents/hook-creator.md` |
| 5 | **`python-dev` en opus+xhigh** alors que canonique réserve xhigh à architect/dev-lead/refactor-pg — sur-coût + over-thinking | **P0** | S | `.claude/agents/python-dev.md` |
| 6 | **`project-analyzer` sans `permissionMode`** dans frontmatter — viole canonique "OBLIGATOIRE" | **P0** | S | `.claude/agents/project-analyzer.md` |
| 7 | **Pipeline vault marker+guard** (vault-query-guard + tracker + reset) replique l'archi markers bannie 22 mai pour ia_back/neo_ia — à justifier (security) ou démanteler | **P0** | L | 4 hooks vault-* |
| 8 | **`devils-advocate-pipeline.md`** présente DA comme OBLIGATOIRE systématique — canonique 22 mai dit CONDITIONNEL. Idem hook `devil-advocate-stop` qui force DA en fin de session | **P0** | M | rule + hook |
| 9 | **3 rules sans frontmatter `description:`** — mortes silencieusement : `agents-color-convention.md`, `changelog-vault.md`, `vault-consultation-protocol.md` | **P1** | S | 3 fichiers rules |
| 10 | **`python-ref` en `user-invokable: true`** alors qu'elle est skill de référence chargée par `python-dev` — devrait être `false` comme `cc-*-ref` | **P1** | S | `.claude/skills/python-ref/SKILL.md` |

### Gaps secondaires (P1/P2) hors top 10

- `cc-cowork-ref` orpheline potentielle (pas référencée dans body d'agent parent)
- `claudemd-optimizer` ne réf. pas `obsidian-markdown` dans body
- `devils-advocate` accède au vault via Grep/Read brut sans MCP forge-brain
- 7 skills sans `allowed-tools` explicit (P2 cosmétique)
- CLAUDE.md gotchas DA en fin de fichier (devrait être en haut < l.25)
- `project-analyzer` + `project-auditor` en `effort: xhigh` sur purple analyzer (hors liste restreinte)
- Permission `Bash(cat > *)` overly broad dans settings.local.json

---

## Résumé exécutif

Le repo forge présente une **maturité structurelle élevée** (architecture 3-layers, color convention, memory project généralisé, MCP forge-brain centralisé, CLAUDE.md sous limite 200L) mais souffre de **drift doctrinal post-pivot 22 mai** : plusieurs composants (CLAUDE.md, hook-creator, devils-advocate-pipeline, devil-advocate-stop, pipeline vault marker+guard, python-dev xhigh) reflètent encore la doctrine PRE-22mai (workflow agentique enforced, xhigh par défaut, DA systématique, markers pipelines).

**5 gaps majeurs** = pipeline vault marker+guard à réévaluer (security vs workflow), hooks matcher MultiEdit absent, Python path Windows risk, CLAUDE.md doctrine obsolète, `python-dev` xhigh non justifié.

**Effort total estimé** : 4-6h pour résoudre les 10 P0/P1 — majoritairement des modifications ciblées de quelques lignes par fichier, la décision la plus lourde étant le sort du pipeline vault marker+guard (refonte L).
