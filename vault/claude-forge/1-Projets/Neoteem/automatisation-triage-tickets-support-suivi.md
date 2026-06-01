---
aliases:
  - suivi automatisation triage tickets
  - projet triage support Cowork
  - support-lojii v3 suivi
  - deploiement MCP support local
  - skills triage analyse-qualification
resume: "Suivi du projet d'automatisation du triage des tickets support LOJII (SC/SD) via Claude Cowork. État 1er juin 2026 — v3 corrigée (régression mémoire vault vers local), déploiement local poste unique (Valéry), transition VM + partage Cowork entreprise à venir."
derniere-maj: 2026-06-01
auteur: claude
tags:
  - "#type/knowledge"
  - "#projet/neoteem"
  - "#casquette/responsable-ia"
  - "#domaine/support"
  - "#statut/en-cours"
---
# Suivi — Automatisation triage tickets support LOJII (Cowork)

> Note de SUIVI projet (côté forge). Objectif : retrouver l'état du déploiement à chaque session et savoir quoi vérifier au passage VM. État au **1er juin 2026**.

## Objectif

Automatisation Claude Cowork (tous les matins 7h) : lit les tickets clients SC/SD (Jira), les **classe** (Bug / Support / Service Request), écrit une **note interne** de proposition, pose le label `À_valider`. Le support reprend via `/analyse` pour valider/corriger. Les corrections alimentent une mémoire + une rétrospective = boucle d'apprentissage.

## Diagnostic de la régression (résolu)

- ~70 % de réussite avec la version d'origine (fichiers locaux bundlés).
- **Réécriture du 13 mai 2026** → forte dégradation. Hypothèse « skill trop gros » **écartée** (tailles ~identiques, logique de classif identique).
- **Cause-racine vérifiée** : la réécriture a migré la mémoire (learnings + retro-done) vers des **notes vault via MCP**. Or **Cowork ne peut PAS écrire le vault en run planifié** → notes jamais créées (`read_note("learnings-triage")` introuvable) → classification sans corrections passées + boucle morte.
- **Bug secondaire** : JQL rétro `comment ~ "Classification"` inopérante car les titres de note sont en **gras Unicode mathématique** (non cherchable JQL) → 0 ticket chaque matin. Corrigé via le label `À_valider`.

## Architecture v3.0.0 (corrigée le 1er juin)

- **2 skills** : `triage-tickets` (batch 7h + revue `/analyse`) + `analyse-qualification-tickets` (création N2 dev). Décision : NE PAS découper davantage (best practice triage IA 2026 : raisonnement de classification cohérent dans un prompt).
- **Mémoire LOCALE** : `support-memory/` (learnings.md, retro-done.txt, retro/) auto-créé par convention, zéro config. Vault en LECTURE seule en batch.
- **Enrichissement vault gardé UNIQUEMENT en `/analyse`** (interactif → écriture vault OK).
- **Run 7h** : Phase C (rétro, apprend de la veille) PUIS Phase A (triage, lit learnings frais).
- **2 plugins brain lecture seule** (pas admin) : `neoteem-brain-support` + `neoteem-brain-dev`. Les deux skills les appellent (support = répondre/FAQ/lexique ; dev = technique/Bugs/N2).
- **MCP `obsidian-brain`** : accès vault. Fallback CLI Obsidian si MCP absent.

## État au 1er juin 2026

- **Déploiement LOCAL, poste unique** : seul Valéry exécute, sur sa machine. Pas encore de partage org Cowork (Team/Enterprise « Share ») — on déploie proprement sur 1 poste d'abord.
- **MCP installé en local** sur le poste (pas de VM encore). Repo `mcp-obsidian-brain` : ajout `start-mcp-portable.bat` (lanceur sans chemin en dur) + `INSTALL-LOCAL-WINDOWS.md`. Commit `ce00a62` sur `master` Bitbucket (1er juin).
- **Livrables** : `claude-forge/output/support-lojii-plugin-v3/` — 4 zips importables (triage-tickets, analyse-qualification-tickets, neoteem-brain-support, neoteem-brain-dev) + `promt-automatision-7h.txt` + `CHECKLIST-INSTALL-COLLEGUE.md` + `INSTALL-MCP-COLLEGUE.md`.

## À VÉRIFIER au passage VM (futur — le cœur de cette note)

Quand la VM centrale du MCP sera en place :
1. **Plus d'install MCP locale** par poste → supprimer la tâche planifiée locale + `config.local.yaml` des postes.
2. **Rebrancher Claude** vers l'URL serveur central (HTTPS) au lieu de `localhost:8090`.
3. **Vérifier accès vault** via MCP distant (read_note, search_brain OK depuis Cowork).
4. **Mémoire locale** : `support-memory/` reste local au poste/VM qui exécute (JAMAIS dans le vault).
5. **Partage Cowork entreprise** : passer du poste-par-poste au « Share » natif org (Team/Enterprise) pour diffuser skills + plugins proprement à toute l'équipe.
6. **Étendre à l'équipe N1** : dé-commenter Marianne, Sonia, Margaux dans le prompt 7h (1 JQL par agent en parallèle).

## Validation fonctionnelle (à re-tester à chaque jalon)

- Run 7h classe + pose `À_valider`.
- `/analyse` + correction → ligne écrite dans `support-memory/learnings.md`.
- Rétro du lendemain trouve des tickets (pas « 0 à analyser »).
- Bug validé → N2 correct (preuve que `neo-brain` dev est branché).

## Inconnus à lever (au 1er juin)

- **Branchement MCP HTTP dans Cowork** : config Desktop `mcpServers` vide chez Raphaël → mécanisme exact à confirmer (sinon fallback CLI, non bloquant).
- **JQL rétro corrigée non testée** contre le vrai Jira (pas d'accès Atlassian en session forge) → vérifier au 1er run réel.

## Liens

- [[idees-agents-ia-issues-tickets-support]] — idées d'agents dérivées des 250 tickets support réels
- [[comprendre-neoteem-vue-responsable-ia]] — contexte Neoteem
- [[lojii]] — l'ERP concerné
