---
titre: "Critique — Plan uniformisation /spec + hook Jira ×3 repos"
resume: "DA sur le plan hook jira-format-guard + tickets + SKILL : classification couloir sur champ non lu, attachements non vérifiables, sync écrase les templates"
aliases:
  - "critique-spec-3-repos"
  - "critique-jira-format-guard-couloirs"
  - "DA-uniformisation-spec-2026-06-26"
  - "critique-hook-couloir-summary"
type: knowledge
domaine: claude-code
derniere-maj: 2026-06-26
auteur: claude
tags:
  - "#type/knowledge"
  - "#domaine/claude-code"
---

# Critique — Plan uniformisation /spec + hook jira-ticket-format-guard ×3 repos

**Intention déclarée** : aligner hook Jira + 29 tickets + SKILL/templates /spec sur 3 repos d'équipe (neo_ia, ia-workbench, neoteem-back-ts), source ia-wb puis sync.

## Verdict : 3 BLOCKING, 4 CONCERN, 2 OK

### BLOCKING

1. **Classification couloir sur `summary` = champ JAMAIS lu par le hook.** Le hook n'extrait QUE `description` + `issuetype` (`_extract_description`, `_extract_issuetype`). Volet 1.b veut détecter `[devops]/[qa]/[ux]` dans le `summary` → field absent du code. Les 2 seuls payloads observés (`.jira-payload-debug.log`) sont synthétiques (X/Y/Z/W/V) et n'ont PAS de `summary`. Résolution : supprimer les 2 logs synthétiques trompeurs, laisser le guard relogguer, lancer UN vrai `editJiraIssue`, choisir le discriminant parmi les champs prouvés présents (summary ? labels ?). Concevoir le classifier APRÈS avoir vu un payload réel.

2. **Option B rend la présence Gherkin INVÉRIFIABLE par le hook.** Les attachements (PJ BRIEF) ne sont pas dans le payload create/edit `description`. Le hook ne peut donc PAS vérifier la PJ. Retirer 🧪 du ticket + ne pas pouvoir checker la PJ = Gherkin non gardé NULLE PART. À accepter explicitement, ou garder un check pointeur faible (description contient la phrase pointeur "BRIEF"/"PJ").

3. **La sync ÉCRASE les templates — la prémisse du plan est fausse.** `apply-sync-spec.sh` FILES inclut `template-neo_ia.md`, `template-back-ts.md`, `output-templates.md` copiés entiers (`cp`). Le plan (Volet 2.d-e + RISK #3) affirme "template-*.md per-repo, PAS sync" → FAUX. Seul `stack-conventions.md` est per-repo. Le dirty-check du script ne protège que les modifs NON commitées. Résolution : éditer les templates DANS ia-wb (source), pas dans les cibles ; toute divergence committée par-repo dans ces 3 fichiers sera silencieusement perdue au prochain sync.

### CONCERN

4. **Parité .py ↔ .ts** : les 2 .py byte-identiques ; matchers IDENTIQUES ×3 (`(create|edit)JiraIssue|...NEOTEEM__.*`). Mais la modif touche 2 langages à la main → divergence future. Fix : porter ET re-tester les 2 ; tests adverses identiques dans chaque langage.

5. **Scope NON étanche /spec** : le matcher fire sur `(create|edit)JiraIssue` ET sur TOUT outil `mcp__claude_ai_MCP_JIRA_-_NEOTEEM__.*`. N'importe quelle story/module/sous-tâche avec description ≥20 chars est validée contre le template /spec → un dev d'équipe éditant un ticket Jira normal mange un deny. Anti-pattern [[config-repo-equipe-vs-forge]]. Fail-open couvre les reads, pas les writes. Vrai fix = discriminant /spec (marqueur que le hook check AVANT de valider).

6. **Docstring .py périmé** : dit "createJiraIssue only" alors que le matcher = create|edit. Désync doc/comportement à corriger pendant la modif.

7. **editJiraIssue ne renvoie pas toujours issuetype** : un edit partiel (description seule) → `_classify` retourne None → fallback "au moins 1 emoji". Comportement différent create vs edit, à expliciter dans les tests.

### OK
- Exclusion des 16 conformes : le plan liste explicitement les CONFORMES NE PAS TOUCHER (IA-7/10/11/.../32). Diff minimal respecté SI on s'y tient.
- Retrait 🧪 du set Story : cohérent avec Option B (le ticket ne porte plus le bloc).

## Prior art
- [[critique-2026-05-24-regex-source-faux-positifs]] — faux positifs de détection par pattern (mappe sur #1/#5)
- [[erreur-hook-garde-hors-vault-bloque-plan-file]] — faux positif team-scope d'un hook bloquant (mappe sur #5)
