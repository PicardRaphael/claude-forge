---
titre: "Critique DA — 8 canoniques chantier 22 mai 2026"
resume: "Devils-advocate sur les 8 notes canoniques produites en Phase B du chantier vault — 1 bloquant (events hooks inventés), 5 avertissements forts, 5 nice-to-have. Verdict : LIVRER AVEC CORRECTIONS."
aliases:
  - "critique 22 mai 8 canoniques"
  - "DA chantier 22 mai"
  - "critique notes canoniques vault"
  - "verdict 8 canoniques"
derniere-maj: 2026-05-22
auteur: claude (devils-advocate via session principale)
type: critique
sources:
  - "Agent devils-advocate session 2026-05-22 chantier vault"
  - ".claude/skills/cc-hooks-ref/SKILL.md (source de vérité events)"
tags:
  - "#type/critique"
  - "#chantier/22mai2026"
  - "#sujet/vault"
---

# Critique DA — 8 canoniques chantier 22 mai 2026

> Devils-advocate sur les 8 notes canoniques produites en Phase B du chantier vault forge-brain.

## Verdict global

**Bloquants : 1** | **Avertissements forts : 5** | **Nice-to-have : 5**

**Décision : LIVRER AVEC CORRECTIONS** — le bloquant `comment-creer-hook.md` invente des events qui n'existent pas. Corrections appliquées en session du 22 mai.

## BLOQUANT — `comment-creer-hook.md` invente des events ❌

### Problème

La table "29 events officiels (verbatim docs Anthropic)" listait `PreEdit`, `PostEdit`, `PreWrite`, `PostWrite`, `PreBash`, `PostBash`, `PreAgent`, `PostAgent`, `AgentResult`, `WorktreeDelete`. **Aucun n'existe.**

### Preuve empirique

`.claude/skills/cc-hooks-ref/SKILL.md` (skill forge à jour avril-mai 2026) liste 25+ events réels :
- `PreToolUse` (avec matcher), `PostToolUse`, `PostToolUseFailure`
- `Stop`, `SubagentStart`/`SubagentStop`
- `SessionStart`/`End`, `UserPromptSubmit`, `UserPromptExpansion`
- `PermissionRequest`, `PermissionDenied`, `Notification`
- `PreCompact`/`PostCompact`, `Setup`, `TeammateIdle`, `TaskCompleted`, `ConfigChange`
- `WorktreeCreate`/`WorktreeRemove`, `InstructionsLoaded`, `CwdChanged`, `FileChanged`
- `PostToolBatch`, `Elicitation`/`ElicitationResult`

Pour intercepter une écriture = `PreToolUse` avec `matcher: "Write|Edit|MultiEdit"`.

### Correction appliquée

- Table réécrite alignée sur `cc-hooks-ref/SKILL.md`
- Alias "29 events" → "25+ events" (frontmatter + bottom)
- Étape "Choisir l'event" précisée (matcher pour Write/Bash/etc.)
- `asyncRewake` clarifié : option de retour, PAS un event

## A1 — Attribution "lethal trifecta" → Simon Willison ⚠️

### Problème
`mcp-vs-skills-doctrine.md` attribuait le **lethal trifecta** à Thariq. C'est faux.

### Vérification
Terme forgé par **Simon Willison** ([simonwillison.net](https://simonwillison.net), juin 2025). Thariq l'a repris dans Agent SDK Workshop mai 2026 mais ne l'a pas créé.

### Correction appliquée
Section réécrite : "Lethal trifecta (Simon Willison) — repris par Thariq".

## A2 — Findability "automatiser X" ⚠️

### Problème
Aucune des 8 notes n'avait `automatiser`, `automate`, `automation` en alias. Le test "comment automatiser X" cité par Raphael ne matchait pas.

### Correction appliquée
- `methode-analyser-repo.md` : ajout aliases "comment automatiser un repo claude code", "automate repo setup", "automatiser projet claude code"
- `workflow-claude-code-optimal.md` : ajout aliases "comment automatiser claude code", "automation workflow"

## A3 — DA-gate résurgent contre doctrine 22 mai ⚠️

### Problème
3 notes (skill, agent, hook) prescrivaient DA systématique après création. Doctrine 22 mai a tué les gates systématiques (cf [[raisonnement-22mai-doctrine-vs-enforcement]] + [[feedback_pipeline_quality_gates]]).

### Correction appliquée
Reformulé en "Étape optionnelle CONDITIONNELLE — DA si livrable majeur, pas systématique" dans les 3 notes.

## A4 — Métriques non sourcées ⚠️

### Problème
`comment-ecrire-claudemd.md` claimait "~60% moins tokens", "0% récurrence vs ~40% sans", "30-50% lignes éliminées" — aucune source.

### Correction appliquée
Table reformulée en qualitatif + verbatim Anthropic et Boris cités au lieu de chiffres inventés.

### À faire ultérieurement
Vérifier ou retirer : "2-3× quality" Boris (URL ?), "259 PRs/30j Boris décembre 2025" (verbatim mais URL primaire absente).

## A5 — forrestchang URL obsolète ⚠️

### Problème
4 notes citaient `forrestchang/andrej-karpathy-skills`. L'URL redirige aujourd'hui vers `multica-ai/andrej-karpathy-skills`.

### Correction appliquée
Toutes occurrences mises à jour vers `multica-ai/andrej-karpathy-skills` avec mention "ex-forrestchang". Claim "110k + 220k cumul" retiré (non vérifié).

## Nice-to-have (NON appliqués session)

| # | Item | Statut |
|---|------|--------|
| N1 | Redondance Trail of Bits / claude-for-legal dans 5 notes — factoriser éventuel | Acceptable (self-contained) |
| N2 | "Harness > model +21.8 pts" suppose même modèle des deux côtés — étayer | À faire |
| N3 | `pattern-vault-llm-karpathy.md` mélange pattern + stats forge — isoler | À faire |
| N4 | "advisory 80% compliance" répété sans source | À étayer |
| N5 | Anti-patterns manqués (test chargement CLAUDE.md, description=body skill, agent invoque agent, hook race condition, MCP schema invalide, `permissionMode: plan`, `AGENTS.md` alternative) | À ajouter ultérieurement |

## Cohérence doctrine 22 mai — globalement OK

Les 8 notes répètent la doctrine "hooks lint/security/scope, JAMAIS workflow" avec wikilink vers `raisonnement-22mai-doctrine-vs-enforcement`. Pas de contradiction structurelle.

## Wikilinks
- [[raisonnement-22mai-doctrine-vs-enforcement]]
- [[feedback_pipeline_quality_gates]]
- [[critique-2026-05-21-refonte-hooks-16-vers-6]]
- [[comment-ecrire-claudemd]]
- [[mcp-vs-skills-doctrine]]
- [[comment-creer-skill]]
- [[comment-creer-agent]]
- [[comment-creer-hook]]
- [[workflow-claude-code-optimal]]
- [[methode-analyser-repo]]
- [[pattern-vault-llm-karpathy]]

---

**Fin critique DA chantier 22 mai 2026.**
