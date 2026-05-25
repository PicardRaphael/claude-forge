---
titre: Context Actuel
resume: "Working memory dynamique — mis à jour par /done, lu par /recap. Session 2026-05-25 : audit poussé neo_ia (15 tâches, -660 LOC) + naissance agent forge codebase-scanner + 2 notes canoniques patterns (quartet + vagues parallèles)."
aliases:
  - "context actuel"
  - "contexte courant"
  - "working memory"
  - "memoire de travail"
  - "etat actuel"
type: context
status: active
derniere-maj: 2026-05-25
auteur: claude
tags:
  - "#type/context"
  - "#meta/working-memory"
---

## Phase actuelle

Capitalisation patterns multi-repo après audit massif neo_ia 25 mai. Quartet forge `project-analyzer + project-auditor + codebase-scanner + devils-advocate` désormais opérationnel et documenté.

## Dernière session (2026-05-25)

### Décisions prises
- Créer agent forge **`codebase-scanner`** (Sonnet purple read-only) pour étape 1b/1c/1d/5 méthode-analyser-repo — complète le quartet d'analyse
- Méthode audit poussé = **5 axes parallèles + 4 vagues P0/P1/P2/P3** avec vérif empirique entre vagues
- Naming skills neo_ia uniforme : `neoia-*` (compact, majoritaire) — 3 skills renommées
- `.proposed` files transitoires : NE PAS commit (cf feedback antipattern existant)

### En cours
- neo_ia commit `7b86ea5` poussé sur develop : -660 LOC dedup + 4 skills code-gen + 3 hooks lint + purge méta-commentaires + sécu webhook
- forge commit `11f5610` poussé sur main : agent codebase-scanner + 2 notes vault patterns

### Actions manuelles en attente Raphael
1. **🚨 CRITIQUE** : révoquer + régénérer webhook GCHAT (l'ancien était dans git history avant commit) + mettre nouvelle valeur dans `neo_ia/.env`
2. Appliquer `mv neo_ia/.claude/settings.local.json.proposed neo_ia/.claude/settings.local.json` (classifier auto-mode bloque l'édition directe)
3. Tester comportementalement les 3 nouveaux hooks lint neo_ia + agent codebase-scanner forge

### Prochaines étapes (suggestions)
- **Porter le quartet d'analyse sur ia_back** (même méthode 5 axes + 4 vagues) — patterns prêts à réutiliser
- **Porter le quartet sur lojii** (Vue 3 / Vuetify 3, 634 composants — scan code via codebase-scanner serait riche en patterns)
- **Auditer claude-forge lui-même** avec le quartet (sauf codebase-scanner qui n'a pas de code applicatif Python à scanner)
- Tester si le pattern AMBIGU ESCALADE introduit dans `architect-deep` neo_ia fonctionne en conditions réelles

## Fils ouverts

- Webhook GCHAT à révoquer (sécu)
- `.proposed` à appliquer manuellement
- Compounding patterns : skills code-gen `create-fastapi-endpoint` / `create-sqlalchemy-repo` / `create-langgraph-agent` — premier vrai test d'usage à venir
- Test comportemental hooks `guard-asyncpg-direct` / `guard-cross-app-imports` / `guard-conftest-autouse`
- Question latente : faut-il un hook `delegate-guard` sur neo_ia ? (advisory pour l'instant)
- Mythes audités 22 mai (seuils canoniques) — peut-être étendre la note `reference_seuils_canoniques_agents_mythes` avec les seuils observés empiriquement sur neo_ia

## Liens

[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
[[1-Projets/neo_ia|neo_ia]]
[[quartet-analyse-multi-repo]]
[[audit-puis-vagues-paralleles]]
[[methode-analyser-repo]]
[[codebase-scanner]]
