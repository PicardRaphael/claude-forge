---
titre: Context Actuel
resume: Working memory dynamique — mis à jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, memoire de travail, etat actuel]
type: context
status: active
derniere-maj: 2026-05-27
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---

## Phase actuelle
Consolidation du workflow Spec-Driven Development Neoteem (ia_back + neo_ia) : de l'idée au code shippé, avec checkpoint humain.

## Dernière session (2026-05-27)
### Décisions prises
- **Split `/go` + `/ship`** sur ia_back + neo_ia : `/go` = typecheck/lint + tests + review + changelog (STOP) ; `/ship` = commit + push. Checkpoint humain pour test manuel entre les deux.
- **Pas de skill `/dev`** : le routing existant (agent-delegation ia_back / agent-routing neo_ia) orchestre déjà architect → test-writer → dev → reviewer.
- **Gherkin DANS le BRIEF** (source unique) — le ticket Jira le copie. BRIEF enrichi de 4 sections : Gherkin, recherche préalable, implémentations de référence, comment vérifier.
- **Spec NON systématique** : grosse feature = /spec obligatoire ; petit truc = ticket Jira direct sans spec (architect produit les contrats à la volée).
- **Nettoyage dette `architect-quick`** : ce n'est PAS un agent, c'est la skill `architect-sanity-check` (ou mode S de architect-deep). Corrigé dans toutes les rules vivantes des 2 repos.

### En cours
- Rien en cours — tous les commits poussés (ia_back develop 30f9fc4, neo_ia develop fe04e9b).

### Prochaines étapes
- Mettre à jour 2 notes vault : `workflow-claude-code-optimal` (go monolithique → go+ship) et `ia_back.md`/`neo_ia.md` (désync architect-quick agent → skill). Non bloquant.
- Lancer le prompt d'audit `claude-forge/PROMPT-audit-vault-jamais-consulte.md` en session fraîche (corrige l'erreur "vault jamais consulté en premier").
- Première vraie feature test du workflow complet : `feature-jira-ticket-from-neochat` (spec + 3 tickets prêts dans ia_back/TODO/).

## Fils ouverts
- Notes vault à synchroniser avec le split go/ship (workflow-claude-code-optimal documente encore /go monolithique).
- Audit "vault jamais consulté" (prompt écrit, pas encore lancé).

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
