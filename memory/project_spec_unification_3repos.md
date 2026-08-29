---
name: spec-unification-3repos
description: Chantier en cours (26 juin 2026) — uniformiser /spec dans neo_ia/neoteem-back-ts/ia-workbench. Phase 1+2 livrées+poussées ; reste l'audit/normalisation des 23 tickets Jira existants.
type: project
status: review-required
expires: 2026-09-15
metadata:
  type: project
---

Chantier démarré 26 juin 2026 : rendre la skill `/spec` IDENTIQUE et fiable dans les 3 repos (neo_ia, neoteem-back-ts, ia-workbench), pour que `/feature` exécute des specs parfaites. Déclencheur : IA-16 (emoji, pas Gherkin) vs IA-27 (Gherkin, pas emoji au 1er jet) — sorties divergentes faute de skill alignée + de garde déterministe.

## Décisions actées (Raphael)
- SKILL.md **strictement identique** ×3 (répétition assumée), `effort: xhigh`, chemin `docs/stories/` partout.
- **Source = ia-workbench** ; sync par script `tools/apply-sync-spec.sh` (copie fichiers entiers vers `../neo_ia`+`../neoteem-back-ts`, dry-run par défaut, garde dirty). `modules-jira.md` garde son script à marqueurs séparé.
- Stack-spécifique reste par-repo : `template-*.md`, `stack-conventions.md`, section « read-only » d'ia-wb.
- Discovery **code-d'abord** (agent `repo-explorer` opus/xhigh), MCP NeoBrain en complément. MCP BDD gardé.
- Ticket = **résumé scannable** ; détail lourd (recherche §0, contrat verbatim, Gherkin complet) en **PJ**. Gherkin **littéral au niveau Story** (section 🧪).
- Nettoyage PJ → `.spec-archive/` (gitignored) après attachement confirmé.
- **Hook `jira-ticket-format-guard`** (py neo_ia+ia-wb, TS/bun neoteem-back-ts) : bloque create/editJiraIssue si sections obligatoires du template manquantes par type (Module/Story/Sous-tâche) ou Story sans Gherkin rempli. Gère ADF objet réel. Fail-open. Scopé Jira (repos d'équipe → jamais exit 2 large).

## État (fin session 26 juin) — COMMITÉ + POUSSÉ sur les 3 repos
Phase 1+2 done : SKILL.md unifié, repo-explorer, 3 rules (discovery-workflow code-first, jamais-decider-seul, spec-vault-mandatory révisée), references (modules-jira réconcilié, Gherkin Story), hook durci, script sync, docs/stories migré. 2 commits/repo poussés (neo_ia+back-ts sur develop, ia-wb sur master).

## Session 26 juin (suite) — normalisation tickets FAITE + pivot doctrine « option B »
PRÉMISSE FAUSSE corrigée : les tickets n'étaient PAS à l'ancien format. (Re)créés par /spec unifié les 25-26 juin → déjà conformes (ADF #00b8d9, PJ BRIEF, étiquettes). 29 tickets (pas 23). Audit complet : 16 conformes, écarts réels = (1) Stories sans 🧪, (2) couloirs vs hook, (3) cosmétique. Cf [[brief-premisse-fausse-verifier-avant-executer]] (cas « ma propre mémoire projet est une prémisse faillible »).

DÉCISIONS Raphael :
- **Couloirs** : le hook avait tort de leur imposer le set complet → ALLÉGÉ.
- **Gherkin = OPTION B** : le BRIEF en PJ est la SOURCE UNIQUE ; le ticket NE recopie PLUS le Gherkin (pointeur au plus). Trou de vérif PJ par le hook = ASSUMÉ.
- **Marqueur footer /spec** = nouveau contrat de sortie de /spec (étanchéité repo d'équipe + routage rôle).

LIVRÉ (DA + advisor passés, tests verts) :
- **Hook `jira-ticket-format-guard`** réécrit (.py ia-wb+neo_ia, .ts back-ts) : GATE footer `/spec · rôle:` (pas de footer→SKIP, fix étanchéité team-repo, vrai problème de fond trouvé par DA) ; classement par RÔLE lu dans footer (module/story-repo/devops/qa/ux/sous-tache-repo/sous-tache-couloir) ; couloirs allégés (🎯✅) ; 🧪 Gherkin RETIRÉ partout. Tests adverses 24/24 .py ET .ts.
- **SKILL.md /spec + templates** (source ia-wb + sync ×3) : footer sur chaque ticket (étape 6), gate format = footer au lieu de Gherkin-inline, 🧪 Story = pointeur PJ, drift « ticket copie verbatim » nettoyé dans output-templates.md (×3) + matrice-tests.md.
- **Cosmétique tickets** (editJiraIssue ADF, rendu coloré préservé via getJiraIssue responseContentFormat:adf qui renvoie BIEN l'ADF — la note vault [[jira-rendu-adf-mcp-atlassian]] disait read=markdown, FAUX ici) : ligne parasite 🏷️ retirée + footer ajouté sur IA-27 (module), IA-28 (story-repo), IA-33/34 (sous-tache-repo). Glyphe 🗚️ IA-8/9 et labels one-shot : Raphael a choisi de NE PAS les faire.

PROPRIÉTÉ CLÉ : les 25 autres tickets restent SANS footer → le hook les skip (déjà relus = correct). Pas de rétrofit, diff minimal.

## RESTE éventuel (non bloquant)
- Les 25 tickets sans footer ne sont pas validés par le hook (volontaire). Si un jour on veut qu'ils le soient → ajouter le footer (edit ADF). Pas nécessaire.
- À CAPITALISER vault (fin de chantier) : pattern « marqueur footer = gate d'étanchéité d'un hook de validation sur repo d'équipe » + « getJiraIssue responseContentFormat:adf renvoie l'ADF réel » (corrige la note jira-rendu-adf). Cf section capitalisation ci-dessous.

## À capitaliser en fin de chantier (vault, pas encore fait)
Pattern « skill identique ×N repos + script sync fichiers-entiers + hook validation format déterministe » = réponse au drift multi-copies. Lié à [[pattern-vault-source-unique-sync-mecanique]] et critique DA `critique-2026-06-26-uniformisation-spec-3-repos`. Gotcha encodage hook déjà couvert ([[comment-creer-hook]] + [[decision-byte-for-byte-splice-test-live]] pour l'audit CRLF).
