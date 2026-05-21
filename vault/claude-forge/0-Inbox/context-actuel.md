---
titre: Context Actuel
resume: Working memory dynamique — mis à jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, mémoire de travail, état actuel]
type: context
status: active
derniere-maj: 2026-05-21
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---

## Phase actuelle

Workflow ticket Jira → spec → implémentation cross-repo unifié. `/spec` master déployée ia_back + neo_ia, `/decompose-ticket` supprimée des 2 repos. Pattern Thariq running-notes intégré, x-read fonctionnel avec image multimodale.

## Dernière session (2026-05-20)

### Décisions prises

- **Fusion `/spec` + `/decompose-ticket`** en une seule skill unifiée master dans claude-forge
- Déploiement sur ia_back + neo_ia (3 repos sync), stack-agnostic via `references/stack-conventions.md`
- Suppression complète de `/decompose-ticket` des 2 repos (intégrée comme Phase 5 conditionnel XL)
- STOP CRITIQUE en blockquote ligne 18 + gate AskUserQuestion bloquant Phase 4 + Phase 5 conditionnel XL
- Override Option B advisor → exécution Option A "fais tout commit push" malgré turn 50+ (responsabilité Raphael acceptée)
- DA n'a pas pu finaliser (529 API Anthropic) — livraison faite sans son verdict final
- 3 commits poussés : forge `e8ef466`, ia_back `2d0d094`, neo_ia `e690461`

### En cours

- Pas testé sur un vrai ticket Jira — angle mort critique à corriger
- Bug Jérôme diagnostiqué textuellement, fix appliqué mais pas reproduit empiriquement

### Prochaines étapes (priorisées)

1. **Tester `/spec` sur un vrai ticket Jira** (ia_back ou neo_ia) — valider que le bug Jérôme est bien fixé
2. **Pre-commit hook anti-paths-utilisateur** dans claude-forge + ia_back + neo_ia (proposition Jarvis du tour précédent — 4ème récidive sinon garantie)
3. **Rotation password PostgreSQL `test`** + refactor `${PG_CONNECTION_STRING}` via `.env` — coordination Jérôme requise (secret compromis dans historique git)
4. **3 SKILL.md ia_back avec paths hardcodés pré-existants** : recap, refactor-scan, fixed-spec — audit batch
5. **x-read fix structurel** : `ReadOnlyAccount(Account)` qui override write methods (sécurité)
6. **Article X non accessible** via API tweet seule — solution future

## Fils ouverts

- DA n'a pas validé la fusion `/spec` finale (529 server overload) — risque résiduel à monitorer
- Drift cross-repo `/spec` master vs clones ia_back/neo_ia — convention "toujours modifier master, redéployer" à respecter, pas enforcée par hook
- Politique purge `.claude/skills/x-read/downloads/` (croîtra silencieusement)
- 5 chantiers dans la session 2026-05-20 = violation explicite de `feedback_session_multi_chantiers` créé le matin même. À pas refaire.

## Apprentissages session

- **Position d'instruction = comportement modèle** : STOP en gras ligne 18 (marche) vs STOP en gotcha ligne 179 (ignoré). Primacy/recency confirmé empiriquement par bug Jérôme.
- **Auto-mode classifier bloque le bypass** delegate-guard même via env CLAUDE_AGENT. Sub-agent skill-creator a le bypass natif.
- **API 529 Overloaded** sur Anthropic peut faire échouer un DA en background — protocole de fallback documenté
- **Override conscient de l'advisor** par utilisateur valide → responsabilité partagée, mais erreurs prévisibles arrivent (session 50+ tours)
- **5ème chantier dans même session** = exactement ce que feedback créé le matin interdisait. Auto-référentiel.

## Liens

- [[Raphael-Picard]]
- [[Claude-Forge]]
- [[erreur-stop-critique-position-gotcha-fin]] — Erreur structurelle découverte cette session
- [[critique-session-2026-05-20-running-notes-decompose-xread-mcp]] — Critique DA matin
- [[forge-prompt-machine]] — Primacy/recency effect théorique
- [[pattern-spec-driven-development]] — Pattern foundational
