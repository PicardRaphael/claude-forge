---
titre: Context Actuel
resume: Working memory dynamique — mis à jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, mémoire de travail, état actuel]
type: context
status: active
derniere-maj: 2026-05-14
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---

## Phase actuelle

Session marathon de renforcement forge — cc-news, deep research, restructuration vault, mise à jour complète des agents/skills/hooks.

## Dernière session (2026-05-14)

### Décisions prises
- Vault restructuré : `01-Claude/Code/` + `01-Claude/Cowork/`
- 8 notes best-practices créées (skills-guide, hooks-guide, claudemd-guide, context-management, agents-orchestration, mcp-vs-cli-vs-skills, cowork-architecture, cowork-skills-reliability)
- 4 agents specialists enrichis (Ashby, Generator/Evaluator, PATH portable, descriptions directives)
- 3 reference skills mises à jour (cc-skills-ref, cc-agents-ref, cc-hooks-ref)
- 5 hooks créés/modifiés (skill-activation, vault-write-tracker, proactivity-reminder, apply-edit, hooks Python PATH fix)
- Skill `/expand` créée
- cc-news : v2.1.140, date de référence 14 mai 2026

### En cours
- **Demain : debug skill Cowork** qui ne suit pas les instructions — checklist 9 étapes dans `cowork-skills-reliability.md`
- Nouveau hook `skill-activation.py` à tester en conditions réelles

### Prochaines étapes
1. `/recap` + `/vault-audit` rapide pour vérifier cohérence post-restructuration
2. Debug skill Cowork avec la checklist harness engineering
3. Fusionner `claudemd-maintenance.md` dans `claudemd-guide.md` (DA bloquant)
4. Mettre à jour `MOC-Claude-Code.md` avec les 8 nouvelles notes
5. Renommer `0-Inbox`, `1-Projets`, `2-Casquettes` en format `0X-` (session dédiée)

## Fils ouverts
- Google I/O le 19-20 mai — Gemini Omni attendu, relancer cc-news après
- Deprecation Sonnet 4 / Opus 4 le 15 juin — vérifier aucun code ne référence les anciens IDs
- Notes cc-news non-capitalisées individuellement : xAI→SpaceXAI, Kimi K2.6, Copilot REST API
- Tester skill-activation.py en conditions réelles (1er fire confirmé cette session ✓)
- Forge = PRIVÉ, jamais d'open-source (feedback explicite Raphael)
- Cowork n'a PAS de hooks — impacte la stratégie debug skill Cowork demain
- Tests architecture multi-agents : note `0-Inbox/tests-architecture-repos.md` à exécuter
- Fusionner claudemd-maintenance.md dans claudemd-guide.md
- Renommer 0-Inbox, 1-Projets, 2-Casquettes en format 0X-
- MOC-Claude-Code.md à mettre à jour avec les 8 nouvelles notes

## Liens
[[Claude-Forge|Claude-Forge]]
