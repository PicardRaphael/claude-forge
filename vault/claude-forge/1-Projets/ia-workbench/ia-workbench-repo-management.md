---
titre: "ia-workbench — repo de management des chantiers IA"
resume: "Repo frère vierge (zéro code applicatif) qui prépare les chantiers IA en amont du dev via des loupes (skills). 1re loupe = /spec : LE spec unique cross-repo, source du référentiel Jira (mono-repo → consommateurs sync). Modèle Jira = Module → 4 familles de Stories → Sous-tâches (révisé 24 juin 2026)."
aliases:
  - "ia-workbench"
  - "ia workbench repo management"
  - "spec unique cross-repo"
  - "loupe spec discovery"
  - "repo preparation chantiers IA"
derniere-maj: 2026-06-24
auteur: claude
type: projet
tags:
  - "#type/projet"
  - "#domaine/claude-code"
  - "#projet/ia-workbench"
---

# ia-workbench — repo de management des chantiers IA

> Repo : `Documents/neot-v2/ia-workbench` (local, pas de remote au 18 juin). Frère de neo_ia / neoteem-back-ts / bdd / neofront, jamais parent.

## Raison d'être

Repo de **management**, zéro code applicatif. Il porte l'outillage `.claude/` qui PRÉPARE les chantiers IA en amont du dev. Principe fondateur (loops Boris Cherny) : **un loop amplifie son entrée** → on fiabilise l'ENTRÉE (tickets parfaits) avant d'automatiser l'exécution. Le repo grandit par ajout de **loupes** (features = skills), jamais par ajout de code produit.

## Architecture — socle + features

- **Socle** : `doc/architecture-ia-workbench.md` (stable, commun à toutes les loupes).
- **Feature** : `doc/features/<nom>.md` (le spécifique). 1re = `spec-discovery.md`.
- Composants : connaissance = skill · exploration lourde = agent (repo-explorer) · comportement transverse = rule · fiabilité déclenchement = hook skill-activation (UserPromptSubmit).

## 1re loupe — /spec (discovery cross-repo → tickets parfaits)

LE `/spec` unique, **destiné à remplacer** les `/spec` mono-repo (neo_ia + back-ts). Flux : idée → discovery (NeoBrain carte → agent repo-explorer lit le code réel → conclure) → présenter → rédiger Module + Stories (template du repo cible) → créer Jira (Module d'abord, puis Stories, puis Sous-tâches) + BRIEF en PJ.

- **Modèle Jira (révisé 24 juin 2026) : Module → 4 familles de Stories → Sous-tâches.** Le Module (type Jira « Module », hierarchyLevel 1) est CRÉÉ à chaque chantier — il remplace l'ancien epic-thème permanent figé et voyage dans le pipeline « IA - Pipeline ». Sous lui : **STORY-REPO** (une par repo touché, cas par défaut) + **STORY-UX / STORY-DEVOPS / STORY-QA** conditionnelles (couloirs de responsabilité, assignées à l'acteur). Projet **IA** (`projectKey` IA, id 10319), plus jamais N2.
- **references de la skill** : `modules-jira.md` (SOURCE UNIQUE du référentiel Jira, marqueurs SYNC ; remplace l'ex-`epics-jira.md` supprimé), interview-bank, output-templates, template-neo_ia (+ QA française), template-back-ts (pas de QA), **template-ux / template-devops / template-qa** (les 3 couloirs conditionnels), matrice-tests, stack-conventions, contradiction-prompt, cross-validation, decompose-waves.
- **Tests par type, chiffrés** (taxonomie réelle cartographiée) : back-ts par suffixe (use-case/parité/contrat/mutation) ; neo_ia par dossier+marker (unit/integration/functional-DeepEval). **Pas de e2e** (pas de front dans ces repos ; bout-en-bout couvert par DeepEval + contrat/parité + la STORY-QA conditionnelle pour la surface IA testable par un humain).

## Décisions FIGÉES (18 juin 2026, modèle Jira révisé 24 juin)

- **Modèle Jira = Module par chantier → 4 familles de Stories → Sous-tâches** (24 juin). On CRÉE un Module à chaque `/spec` (plus de référentiel d'epics-thèmes à choisir ni à rattacher). Détail figé : `references/modules-jira.md`.
- **Repo frère vierge**, read-only strict sur les repos produit (settings n'accorde que Read/Grep/Glob sur neot-v2/** + neofront/** ; l'absence de Write/Bash large FAIT le read-only).
- **BRIEF .md** vit dans `ia-workbench/stories/`, voyage en PJ Jira, **jamais committé dans un repo produit**.
- **ia-workbench = source unique du référentiel Jira** (modules-jira + templates) ; les mono-repo deviennent consommateurs régénérés par sync mécanique (marqueurs `<!-- SYNC -->`). Résout le TROU 2 de la critique DA. Pattern : [[pattern-vault-source-unique-sync-mecanique]].
- **Jamais inventer le contrat d'API** (placeholder + question) ; jamais décider seul (l'humain tranche) ; jamais de SQL.
- **ia_back décommissionné (N2-111278)** — jamais cible de travail neuf.
- **Brain NeoTeem = connector claude.ai** (`mcp__claude_ai_MCP_NeoBrain_-_NEOTEEM__*`), PAS `.mcp.json`. Le `.mcp.json` ne doit déclarer aucun brain forge-brain (résidu copié de claude-forge, corrigé 24 juin). MCP Jira = `plugin:atlassian:atlassian` (création) + `MCP JIRA - NEOTEEM` (Service Desk).
- **effort** : `xhigh` sur la skill /spec (agentique, option C), `high` sur repo-explorer (lecture).

## Reste à faire

- Script de sync modules-jira → mono-repo (marqueurs posés, script non écrit).
- MCP NEOTEEM exposé en HTTP + `add_attachment` (Jérôme) → débloque l'attache PJ.
- **TROU 1 de la critique DA (oracle/rubrique de ticket parfait)** : à traiter AVANT d'allumer un loop d'exécution — pas requis pour /spec seul.
- Dry-run réel du /spec sur un vrai besoin (validation comportementale).

## Liens

- [[critique-2026-06-18-ia-workbench-spec-discovery]] — devil's advocate (2 BLOCKING, dont TROU 1 oracle encore ouvert)
- [[pattern-vault-source-unique-sync-mecanique]] — mécanisme source unique → consommateurs sync
- [[pre-compute-vs-inference-loops-boris]] — fondement (fiabiliser l'entrée avant le loop)
- [[concevoir-loops-travail]] — niveaux de loops Boris
