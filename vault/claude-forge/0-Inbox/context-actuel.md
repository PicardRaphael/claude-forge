---
titre: Context Actuel
resume: Working memory dynamique — mis à jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, memoire de travail, etat actuel]
type: context
status: active
derniere-maj: 2026-05-25
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---

## Phase actuelle

Capitalisation post chantier ia_back 25 mai (commit `fdeee72` develop). Pattern quartet forge validé sur 2e repo (après neo_ia matin). 2 nouveaux feedbacks mémoire capitalisés (script Python refactor masse + Edit Read obligatoire).

## Dernière session (2026-05-25 — tour 2 ia_back)

### Décisions prises
- Pattern quartet forge appliqué en production sur ia_back (5 sub-agents audit en // + 4 vagues fix en //)
- Refactor 18 agents via script Python regex (308L économisées) plutôt que 18 Edit séquentiels
- 2 rules canoniques créées ia_back : `mcp-brief-then-direct.md` + `escalade-sub-agent.md`
- P0 secrets GCHAT/PG laissés de côté (rotation manuelle séparée par Raphael)
- 2 nouveaux hooks ia_back : `guard-di-registration.ts` + `bash-permission-syntax.ts`
- 1 nouvelle skill métier ia_back : `add-filter` (pattern récurrent ~30 occurrences SQL dynamique)
- Skill `testing-patterns` alignée sur le code (`__tests__/`) plutôt que l'inverse

### En cours
- Rien — chantier ia_back clôt et pushed
- ia_back develop à jour origin `fdeee72`
- claude-forge main à jour origin `6121fb6`

### Prochaines étapes (suggestions)
- Capitaliser pattern `script-python-refactor-masse` dans `04-Techniques/patterns/` (technique réutilisable cross-repos, pas juste mémoire)
- Considérer audit quartet sur neoteem-brain (3e repo, valider pattern sur vault Obsidian, pas codebase classique)
- Rotation manuelle webhook GChat ia_back + password PG (côté Google Cloud, hors Claude)
- Refactor identique 13+5 agents sur neo_ia ? À vérifier si les mêmes doublons existent

## Fils ouverts

- Pattern script-python-refactor-masse → vault `04-Techniques/patterns/` (non créé cette session)
- Audit neoteem-brain quartet (jamais fait, vault Obsidian = stack différente)
- P0 secrets historique git ia_back (rotation manuelle hors Claude)

## Liens

- [[Raphael-Picard]]
- [[Claude-Forge]]
- [[audit-ia-back-25mai-quartet]] — synthèse complète du chantier
- [[quartet-analyse-multi-repo]] — pattern parent
- [[ia-back-project]] — fiche projet
