---
titre: "ia-workbench — repo de management des chantiers IA"
resume: "Repo frère vierge (zéro code applicatif) qui prépare les chantiers IA en amont du dev via des loupes (skills). 1re loupe = /spec : LE spec unique cross-repo, source du référentiel Jira (mono-repo → consommateurs sync). Décisions figées 18 juin 2026."
aliases:
  - "ia-workbench"
  - "ia workbench repo management"
  - "spec unique cross-repo"
  - "loupe spec discovery"
  - "repo preparation chantiers IA"
derniere-maj: 2026-06-18
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

LE `/spec` unique, **destiné à remplacer** les `/spec` mono-repo (neo_ia + back-ts). Flux : idée → discovery (NeoBrain carte → agent repo-explorer lit le code réel → conclure) → présenter → rédiger stories/US (template du repo cible) → créer Jira (parent d'abord) + BRIEF en PJ.

- **10 references** : epics-jira (source unique, marqueurs SYNC), interview-bank, output-templates, template-neo_ia (+ QA française), template-back-ts (pas de QA), matrice-tests, stack-conventions, contradiction-prompt, cross-validation, decompose-waves.
- **Tests par type, chiffrés** (taxonomie réelle cartographiée) : back-ts par suffixe (use-case/parité/contrat/mutation) ; neo_ia par dossier+marker (unit/integration/functional-DeepEval). **Pas de e2e** (pas de front dans ces repos ; bout-en-bout couvert par DeepEval + contrat/parité).

## Décisions FIGÉES (18 juin 2026)

- **Repo frère vierge**, read-only strict sur les repos produit (settings n'accorde que Read/Grep/Glob sur neot-v2/** + neofront/** ; l'absence de Write/Bash large FAIT le read-only).
- **BRIEF .md** vit dans `ia-workbench/stories/`, voyage en PJ Jira, **jamais committé dans un repo produit**.
- **ia-workbench = source unique du référentiel Jira** (epics-jira + templates) ; les mono-repo deviennent consommateurs régénérés par sync mécanique (marqueurs `<!-- SYNC -->`). Résout le TROU 2 de la critique DA. Pattern : [[pattern-vault-source-unique-sync-mecanique]].
- **Jamais inventer le contrat d'API** (placeholder + question) ; jamais décider seul (l'humain tranche) ; jamais de SQL.
- **ia_back décommissionné (N2-111278)** — jamais cible de travail neuf.
- **effort** : `xhigh` sur la skill /spec (agentique, option C), `high` sur repo-explorer (lecture).

## Reste à faire

- Script de sync epics-jira → mono-repo (marqueurs posés, script non écrit).
- MCP NEOTEEM exposé en HTTP + `add_attachment` (Jérôme) → débloque l'attache PJ.
- **TROU 1 de la critique DA (oracle/rubrique de ticket parfait)** : à traiter AVANT d'allumer un loop d'exécution — pas requis pour /spec seul.
- Dry-run réel du /spec sur un vrai besoin (validation comportementale).

## Liens

- [[critique-2026-06-18-ia-workbench-spec-discovery]] — devil's advocate (2 BLOCKING, dont TROU 1 oracle encore ouvert)
- [[pattern-vault-source-unique-sync-mecanique]] — mécanisme source unique → consommateurs sync
- [[pre-compute-vs-inference-loops-boris]] — fondement (fiabiliser l'entrée avant le loop)
- [[concevoir-loops-travail]] — niveaux de loops Boris
