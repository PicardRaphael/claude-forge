---
titre: "Critique — Convention couleurs + hooks TDD + cto-mindset renforce"
resume: "2 bloquants : hooks TDD orthogonaux au probleme stated (main session code directement), seul fix pertinent (cto-mindset) est advisory (~80% compliance). Fix propose : dispatch-guard base sur CLAUDE_AGENT."
aliases:
  - "critique color tdd hooks"
  - "critique tdd-guard ia_back"
  - "critique cto-mindset advisory"
  - "DA color convention tdd hooks"
  - "devil advocate session 21 mai hooks"
type: knowledge
domaine: claude-code
derniere-maj: 2026-05-21
auteur: devils-advocate
tags:
  - "#type/knowledge"
  - "#type/critique"
  - "#projet/ia-back"
  - "#projet/neo-ia"
  - "#domaine/claude-code"
sources:
  - "Session 2026-05-21 — color convention + TDD hooks + cto-mindset"
---

## Verdict

**LIVRER AVEC CORRECTIONS** — 2 bloquants, 4 avertissements, 2 nitpicks.

Les hooks TDD et guard-test-scope ont une valeur propre reelle (enforcement TDD + scope de tests), mais le framing "ca fixe le probleme screenshot" est faux.

## 2 Bloquants

### 1. Hooks TDD orthogonaux au probleme stated

Le probleme observe : main session neo_ia code `ia_back_client.py` au lieu de re-dispatcher un dev agent. Le `tdd-guard` verifie "existe-t-il un test correspondant" — il ne verifie PAS "est-ce la main session ou un subagent qui ecrit". Si le test existe deja (probable apres un pipeline partiel), le hook laisse passer la main session.

Le discriminant technique existe : `CLAUDE_AGENT` est vide pour la main session, rempli pour les subagents. Le hook l'utilise deja (bypass test-writer). Un `dispatch-guard` qui whitelist les agents dev resolverait le vrai probleme.

### 2. Seul fix pertinent est advisory (~80% compliance)

La phrase ajoutee en haut de `cto-mindset.md` ("RE-DISPATCHER, JAMAIS coder directement") est le seul livrable qui adresse le probleme. Mais la main session avait DEJA la rule "Tu ne codes JAMAIS directement" — elle l'a ignoree quand le dev a echoue. 3 incidents documentes dans [[erreur-advisory-rules-insuffisantes]] prouvent ce pattern.

## 4 Avertissements

1. `.tdd-bypass` marker set-and-forget — critique deja identifiee dans [[critique-tdd-neo-ia-proposal]]
2. Exemptions incompletes tdd-guard.ts (index.ts, *.d.ts, config dans src/) — pas bloquant aujourd'hui, le sera quand ia_back grandit
3. Probleme le plus important le moins bien adresse — 80% effort sur couleurs + TDD, 2% sur le vrai fix
4. Session-reset-markers vs .tdd-bypass — dilemme structurel du bypass marker

## 2 Nitpicks

1. Convention couleurs sans enforcement dans agent-creator — drift lent garanti
2. 39 agents modifies pour couleurs = commit bruyant dans git log

## Chemin recommande

1. Creer `dispatch-guard.ts` (ia_back) et `dispatch-guard.py` (neo_ia) : PreToolUse Write|Edit sur src/, verifie CLAUDE_AGENT dans whitelist dev agents, bloque si vide
2. Garder tdd-guard tel quel mais le presenter comme enforcement TDD, pas fix du dispatch
3. Ajouter convention couleurs dans checklist agent-creator
4. Ajouter exemptions previsibles dans tdd-guard.ts (index.ts, *.d.ts, types/)

## Liens

- [[erreur-advisory-rules-insuffisantes]] — rules advisory = ~80% compliance
- [[critique-tdd-neo-ia-proposal]] — analyse detaillee du TDD strict
- [[critique-2026-05-21-outcomes-test-deploy]] — meme session, meme pattern advisory
- [[critique-2026-05-13-setup-lojii]] — parite forcee cross-repo precedent
