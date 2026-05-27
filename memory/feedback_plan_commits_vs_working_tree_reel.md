---
name: plan-commits-vs-working-tree-reel
description: Plan de commits précis donné par Raphael ⨯ working tree contenant des fichiers hors-scope (résidus session antérieure, fichiers déjà M au démarrage) = vérifier git status AVANT, isoler le hors-scope dans un commit dédié, signaler l'écart. Jamais noyer un concern étranger dans un commit du plan ni exécuter le plan à l'aveugle.
metadata:
  type: feedback
---

Quand Raphael donne un plan de commits numéroté précis (N concerns, messages fournis) ET que le working tree contient des fichiers qui ne correspondent pas au plan (résidus d'une session antérieure, fichiers déjà `M` dans le git status initial, fichier attendu par le plan mais non modifié) : NE PAS exécuter le plan à la lettre. Vérifier `git status` AVANT de committer, croiser avec le plan, isoler le hors-scope dans un commit dédié supplémentaire, et signaler chaque écart dans le rapport.

**Why:** Session 27 mai (DA compounding rétroactif). Plan = 4 commits. Réalité : `context-actuel.md` + `feedback_cartographie_*` étaient des résidus d'une session précédente (déjà `M`/`??` au démarrage), et `log.md` — cité par le commit 4 — n'était PAS modifié. Exécuter le plan littéralement aurait noyé un concern étranger dans le commit 4 et oublié d'écrire le bloc log. Le découpage par concern n'a de sens que si chaque commit = UN concern réel.

**How to apply:**
- `git status --short` AVANT le premier commit, croiser ligne par ligne avec le plan.
- Fichier du plan non modifié (ex : "log append-only") = l'écrire d'abord si c'est l'intention, sinon le retirer du commit.
- Fichier modifié hors-plan (résidu) = commit dédié supplémentaire, jamais noyé dans un commit du plan.
- Pour isoler une partie d'un fichier multi-concerns (ex : 2 lignes dans MEMORY.md) : Edit temporaire (retirer la ligne hors-scope, committer, réinsérer) > `git apply --cached` avec patch inline (cassé par parenthèses/accents dans le texte via bash eval).
- Signaler chaque écart dans le rapport final, avec justification — c'est de la franchise Jarvis, pas de la désobéissance.

## Lien

- [[feedback_carte_blanche_commit_push]] — exécuter sans re-valider note par note (complémentaire : ici on ADAPTE un plan précis à la réalité du repo, on ne re-valide pas)
- [[feedback_commit_push_check]] — git status + diff avant push, jamais aveugle
- [[feedback_never_pure_executor]] — Jarvis actif même sur prompts directifs (signaler l'écart)
