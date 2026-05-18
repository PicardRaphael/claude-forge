---
titre: Context Actuel
<<<<<<< Updated upstream
resume: Working memory dynamique — mis à jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, mémoire de travail, état actuel]
type: context
status: active
derniere-maj: 2026-05-15
=======
resume: Working memory dynamique -- mis a jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, memoire de travail, etat actuel]
type: context
status: active
derniere-maj: 2026-05-13
>>>>>>> Stashed changes
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---

## Phase actuelle
Setup Claude Code complet deploye sur lojii (frontend Vue 3 gestion immobiliere) — pret a utiliser.

<<<<<<< Updated upstream
Vault forge-brain nettoyé et skills fiabilisées. Prêt pour du travail produit ou de nouvelles explorations.

## Dernière session (2026-05-15)

### Décisions prises
- Vault audit complet : 231→251 notes, 100% grade A (98.9/100)
- 37 wikilinks à chemin normalisés (path/note → note)
- 20 notes vault créées (4 leaders, 4 features CC, 6 techniques, 3 _index, 2 ref/industrie, 1 erreur)
- cowork-skills-reliability.md réalisé : 8 descriptions directives, .skill-triggers.json 7→24
- Bug fixes audit.py (inline arrays YAML, resume list crash) et fix.py (normalisation wikilinks auto)

### En cours
- Rien en cours — session clôturée proprement.

### Prochaines étapes
1. Fusionner `claudemd-maintenance.md` dans `claudemd-guide.md` (DA bloquant identifié session 2026-05-14)
2. Renommer `0-Inbox`, `1-Projets`, `2-Casquettes` en format `0X-` (session dédiée)
3. Tests architecture multi-agents : `0-Inbox/tests-architecture-repos.md`
4. cc-news post-Google I/O (19-20 mai) — Gemini Omni attendu
5. Tester skill-activation.py en conditions réelles sur sessions variées

## Fils ouverts
- Google I/O le 19-20 mai — Gemini Omni attendu, relancer cc-news après
- Deprecation Sonnet 4 / Opus 4 le 15 juin — vérifier aucun code ne référence les anciens IDs
- Notes cc-news non-capitalisées : xAI→SpaceXAI, Kimi K2.6, Copilot REST API
- Forge = PRIVÉ, jamais d'open-source (feedback explicite Raphael)
- Cowork n'a PAS de hooks — checklist harness engineering uniquement
- ~18 red links vault restants (notes à créer au fil de l'eau : Amanda Askell déjà fait, restent Agent Teams features CC etc.)
- Audit script ne résout pas les aliases Obsidian ([[Cowork]] → cowork-architecture via alias)

## Liens
[[Claude-Forge|Claude-Forge]]
=======
## Derniere session (2026-05-13)
### Decisions prises
- Setup Claude Code lojii deploye : 4 agents, 8 skills, 10 rules, 7 hooks, MCP context7
- `.claude/` retire du .gitignore (partage equipe, seul settings.local.json ignore)
- CLAUDE.md optimise 330L → 87L (composants fantomes supprimes)
- Parite adaptee (pas forcee) : 4 agents au lieu de 12, adapte au contexte frontend
- vue-dev multi-mode (dev, migration-composition, migration-vue3, migration-windev)
- Pipeline markers complet : guard + writer + reset (bug corrige apres detection advisor)
- 51 micro-apps Vue 2 decouvertes dans neofront/ (scope migration reel)

### En cours
- MCP Figma a evaluer/configurer pour pixel-perfect
- Skill `audit-health`, `evolve`, `refactor-scan` non deployees (Phase 2 selon besoin)
- Hooks/settings non testes en conditions reelles
- Pas de commit/push sur lojii (en attente validation Raphael)

### Prochaines etapes
- Configurer MCP Figma pour le workflow design pixel-perfect
- Tester le setup en conditions reelles (premier ticket, premiere migration)
- Evaluer si skills supplementaires necessaires apres 2 semaines d'usage
- commit-push skill a adapter pour Bitbucket (pas de gh CLI)

## Fils ouverts
- deploy skill-evolve all sur neo_ia (27 skills) et ia_back (28 skills) — en attente
- /spec a tester en conditions reelles
- MCP postgres ia_back path casse chez Raphael
- lojii : tester hooks en conditions reelles avant d'ajuster

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
[[1-Projets/lojii/lojii|lojii]]
>>>>>>> Stashed changes
