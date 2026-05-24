---
titre: "Doctrine vs enforcement — refonte hooks workflow ia_back + neo_ia"
type: knowledge
domaine: claude-code
derniere-maj: 2026-05-24
aliases:
  - "doctrine vs enforcement 22 mai"
  - "refonte hooks workflow mai 2026"
  - "suppression architect-guard commit-guard dispatch-guard"
  - "Claude decides when to invoke"
  - "thinnest wrapper Boris Cherny appliqué"
  - "suppression hooks workflow ia_back neo_ia"
resume: "Suppression de 7 hooks workflow (architect-guard, commit-guard, dispatch-guard, marker-protect, agent-marker-writer, pipeline-reset, session-reset-markers) sur ia_back + neo_ia le 22 mai 2026. Doctrine Anthropic 2026 (Boris, Thariq, Agent SDK) : la session principale décide quand invoquer les sub-agents, pas un hook."
tags:
  - "#type/raisonnement"
  - "#domaine/claude-code"
  - "#projet/ia_back"
  - "#projet/neo_ia"
  - "#technique/hooks"
  - "#technique/agents"
sources:
  - "Session 22 mai 2026 — friction 6× développement feature"
  - "[[Boris Cherny]] — Latent Space podcast, Pragmatic Engineer"
  - "[[Thariq]] — Anthropic skills/sessions"
  - "Anthropic Agent SDK overview (Sep 2025)"
  - "[[critique-2026-05-21-refonte-hooks-16-vers-6]]"
  - "[[raisonnement-kill-tdd-strict-hooks-mai-2026]]"
  - "[[erreur-pipeline-trop-long-frustration]]"
---
# Doctrine vs enforcement — refonte hooks workflow 22 mai 2026

## Contexte

Sessions du 21-22 mai : friction 6× sur le développement feature côté ia_back et neo_ia. L'utilisateur dit "stop, vos hooks c'est de la merde, ce n'est pas scalable". Diagnostic préalable (déjà commité 21 mai) avait tué `tdd-guard`. Mais le problème persistait : architect-guard, commit-guard, dispatch-guard, marker-protect, agent-marker-writer, pipeline-reset, session-reset-markers continuaient à forcer un pipeline trop large.

## Le déclic — recherche web doctrine Anthropic 2026

3 sources convergent :

### Boris Cherny — "thinnest wrapper"

> "All the secret sauce — it's all in the model." (Latent Space)
> "Complex scaffolding is often rendered obsolete by the next model generation."

Boris investit dans l'**infrastructure déterministe** (context, tool routing), **PAS** dans des "decision scaffoldings" (planners explicites, state graphs, pipelines forcés). Architect-guard path-based qui force architect-first sur src/** = exactement le decision scaffolding qu'il évite.

### Doctrine Agent SDK — "Claude decides when to invoke"

> "Claude decides when to parallelize — you're defining the capability, not the scheduling."

C'est mot-pour-mot ce que l'utilisateur a dit : *"peut-être que c'est à la session principale de dire tiens là, il faut que j'appelle l'architecte"*. Doctrine officielle Anthropic.

### Hooks = pour quoi exactement ?

> "Hooks are deterministic and are recommended for **lint, test, and security**."

Exemples Anthropic : `rm -rf`, `--no-verify`, force-push, secret leak, lint blocant. **Pas** "forcer architect-first sur src/**". Donc les hooks workflow = **misuse** du pattern selon la doctrine.

### CLAUDE.md / rules = pour la doctrine

> "CLAUDE.md is advisory — use it for guidelines, coding preferences, architectural decisions."

La doctrine "appelle architect quand X" va dans CLAUDE.md / rules. Pas dans un hook.

## Décisions prises (22 mai 2026)

### 1. Suppression des hooks workflow (7 hooks × 2 repos = 14 fichiers)

Sur ia_back + neo_ia :
- `architect-guard.{ts,py}` — force architect avant Write/Edit dans `src/**` ou `apps/**`
- `commit-guard.{ts,py}` — force code-reviewer marker avant `git commit`
- `dispatch-guard.{ts,py}` — bloque la session principale d'écrire dans `src/`
- `marker-protect.{ts,py}` — empêche écriture directe des markers
- `agent-marker-writer.{ts,py}` — crée les markers après chaque Task agent
- `pipeline-reset.{ts,py}` — reset des markers après push
- `session-reset-markers.{ts,py}` — reset au SessionStart

Plus markers `.architect-marker` et `.code-reviewer-marker` supprimés.

### 2. Split architect en quick + deep

- `architect-quick.md` : sonnet, effort high, 2 skills max, pas plan mode, output 5 lignes max
- `architect-deep.md` : config existante (opus xhigh, 5-8 skills, plan mode)

Raison : Opus 4.7 xhigh ne respecte pas le mode S "30 secondes" du fichier architect.md (prone overthinking, documenté). Pour avoir un vrai sanity check rapide, il faut un agent séparé avec contraintes dures.

### 3. Doctrine encodée dans rules

- Nouvelle rule `when-to-architect.md` (chaque repo) — matrice de décision quick/deep/skip
- Réécriture complète `quality-gates.md` — passage de "TOUJOURS" à "SELON CRITÈRES"
- Update `orchestrator-mindset.md` — retrait "ne codes pas, hook bloque"

### 4. Update CLAUDE.md des 2 repos

- Section TDD : "convention agent, pas obligation"
- Section Gotchas : note explicite "hooks workflow supprimés 22 mai 2026"
- Stack .claude : compteurs hooks à jour (14 → 7 sur ia_back, 12 → 5 sur neo_ia approximativement)

## Hooks gardés (légitimes selon doctrine Anthropic)

| Repo | Hook | Pourquoi gardé |
|------|------|----------------|
| ia_back | `typecheck.ts` | Qualité — bun tsc --noEmit après edit |
| ia_back | `guard-core-imports.ts` | Architecture — empêche src/core d'importer @infra |
| ia_back | `guard-pg-repo-readonly.ts` | Sécurité — repo PG immutable |
| ia_back | `guard-test-scope.ts` | Qualité — pas de `bun test` global |
| ia_back | `on-push-notify.ts` | Observabilité — webhook gchat |
| ia_back | `session-health.ts` | UX — session-reminder |
| ia_back | `spec-brief-boundary-guard.ts` | Architecture — BRIEF distant scope |
| neo_ia | `repo-scope-guard.py` | Sécurité — pas d'accès repos voisins |
| neo_ia | `guard-pytest-scope.py` | Qualité — pas de `pytest` global |
| neo_ia | `auth-detector.py` / `auth-cleanup.py` | Sécurité — auth temp |
| neo_ia | `on-push-notify.py` | Observabilité |
| neo_ia | `session-health.py` | UX |
| neo_ia | `spec-brief-boundary-guard.py` | Architecture |

Tous = lint/test/security/observabilité. Aucun ne force un workflow agentique.

## Anti-patterns identifiés rétrospectivement

1. **Hook qui force architect-first** = decision scaffolding (Boris dit non)
2. **Path-based blocklist `src/**`** = non scalable (refactor → hooks obsolètes)
3. **Markers `.architect-marker` + `.code-reviewer-marker`** = couche de complexité sans valeur ajoutée vs doctrine
4. **`/go` qui reset les markers après push** = paradoxal, Boris cherche minimal pas couplage
5. **`dispatch-guard` qui bloque la session principale** = inverse de "Claude decides when to invoke"
6. **`commit-guard` qui force code-reviewer marker** = idem, doctrine dans rules suffit

## Risque accepté

~20% des cas où la session skip architect sur du vrai architectural. Pari : `architect-quick` cheap + doctrine claire dans CLAUDE.md/rules > friction 6× actuelle qui fait abandonner l'utilisateur.

Mesure de succès : développer une feature M doit prendre < 30 min (vs ~3h aujourd'hui d'après le chiffre 6× donné par Raphael).

## Conflit avec mémoire forge — résolution

`feedback_enforce_not_advise` disait : "advisory = 80% compliance, hook = 100%, transformer immédiatement tout advisory skippé en hook bloquant".

**Résolution** : cette règle s'applique quand **l'advisory est skippé** (compliance miss). PAS quand **la sur-conformité existe déjà** (sur-enforcement). La sur-enforcement est son propre mode de défaillance.

Le feedback est donc révisé (pas supprimé) avec ce scope. Sans cette révision, la prochaine session re-créera un hook au premier skip.

## Liens

- [[Boris Cherny]] — créateur Claude Code, doctrine thinnest wrapper
- [[Thariq]] — Anthropic, skills et sessions
- [[critique-2026-05-21-refonte-hooks-16-vers-6]] — étape précédente (16→6 hooks)
- [[raisonnement-kill-tdd-strict-hooks-mai-2026]] — kill TDD strict 21 mai
- [[erreur-pipeline-trop-long-frustration]] — symptôme côté utilisateur
- [[workflow-claude-code-optimal]] — pipeline pratique post-refonte
- [[comment-creer-hook]] — guide hooks
- [[agents-color-convention]] — architect-quick + architect-deep = blue

## Sources web (recherche 22 mai 2026)

- [Anthropic Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview) — "Claude decides when to invoke"
- [Building agents with Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
- [Hooks reference Claude Code](https://code.claude.com/docs/en/hooks) — lint/security examples
- [Building Claude Code with Boris Cherny, Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/building-claude-code-with-boris-cherny) — "thinnest wrapper"
- [Inside Claude Code, Medium](https://medium.com/@Coda./inside-claude-code-engineering-the-future-of-agentic-development-508050bf37a2) — bitter lesson appliqué
- [How Boris Uses Claude Code](https://howborisusesclaudecode.com/) — workflow officiel

---

## CORRECTION CITATION POST-AUDIT 23 MAI 2026

La citation Agent SDK utilisée dans ce raisonnement :
> "Claude decides when to parallelize — you're defining the capability, not the scheduling."

n'apparaît pas verbatim sur [code.claude.com/docs/en/agent-sdk/overview](https://code.claude.com/docs/en/agent-sdk/overview) (vérifié 23 mai 2026).

**Verbatim réels Anthropic** (à utiliser à la place) :
- *"Claude decides when to call a tool based on the user's request"*
- *"Skills are model-invoked: Claude autonomously chooses when to use them based on context"*
- *"Claude autonomously invokes when relevant"*

**Le pivot doctrinal 22 mai reste 100% valide** — il repose sur de multiples sources convergentes :
1. Boris "thinnest wrapper" (Latent Space, Pragmatic Engineer)
2. Boris "All the secret sauce — it's all in the model" (Latent Space verbatim)
3. Docs Anthropic Agent SDK : Claude decides / autonomously invokes
4. Doctrine Anthropic hooks recommandés pour lint/test/security (cf [[comment-creer-hook]])
5. Skills = model-invoked (docs Anthropic)

La formule exacte citée était une paraphrase pédagogique, pas un verbatim. Le **principe** "la session principale décide quand invoquer, pas un hook" reste pleinement attesté.

---

Source audit : `output/audit-vault-thematique/01-claude-code/C-croisement-revise.md`
