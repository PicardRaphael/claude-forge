---
titre: Context Actuel
resume: Working memory dynamique — mis à jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, mémoire de travail, état actuel]
type: context
status: active
derniere-maj: 2026-05-20
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---

## Phase actuelle

Workflow ticket Jira → spec → implémentation cross-repo (ia_back + neo_ia) + outillage personnel forge (x-read, /notes, capitalisation vault).

## Dernière session (2026-05-20)

### Décisions prises

- Pattern Thariq `running-implementation-notes` déployé sur ia_back + neo_ia + skill `/notes` forge
- Skill `/x-read` créée (twitter-api-client backend, cookies `claude-forge/.claude/secrets/`)
- Mode `pretty` x-read télécharge images localement (Claude multimodal peut Read)
- `/decompose-ticket` copié de neo_ia vers ia_back, paths `${NEOT_V2_ROOT}` (pas hardcodés)
- Liaison `/spec → /decompose-ticket` : suggestion active sur XL, jamais auto-lancement
- `.mcp.json` ia_back paths relatifs en LOCAL (pas pushé — password en clair)
- Refus respecté du auto-mode classifier sur push credentials

### En cours

- 3 SKILL.md ia_back (recap, refactor-scan, spec) ont encore paths hardcodés pré-existants → audit séparé
- Rotation password PostgreSQL `test` à coordonner avec Jérôme (secret compromis dans historique git)
- Refactor `${PG_CONNECTION_STRING}` via `.env` cross-repos (impact équipe)

### Prochaines étapes

1. **Coordination Jérôme** : rotation password PG + refactor secrets via .env (session dédiée sécu)
2. **Pre-commit hook anti-paths-utilisateur** : claude-forge + ia_back + neo_ia, sinon 4ème récidive
3. **Audit paths hardcodés ia_back** : fix recap + refactor-scan + spec SKILL.md
4. **x-read fix structurel** : `ReadOnlyAccount(Account)` qui override write methods + tests
5. **Tester `/spec` + `/decompose-ticket` ia_back** sur un vrai ticket Jira (jamais testé en conditions réelles)

## Fils ouverts

- Article X (`x.com/i/article/<id>`) pas accessible via API tweet seule — solution future à trouver
- Politique de purge `.claude/skills/x-read/downloads/` (croîtra silencieusement)
- Drift cross-repo `/spec` et `/decompose-ticket` dupliqués ia_back + neo_ia
- Pattern Thariq déployé en advisory (80% compliance Boris) — hook enforcement utile à terme
- 3 nouveaux feedbacks à appliquer : multi-chantiers, claim-security-provable, audit-claims-after-brief

## Apprentissages session

- DA verdict 3 bloquants traités : x-read description honnête + decompose-ticket paths + MCP push refusé
- Session 30+ tours = piège fourre-tout Boris (3 erreurs même signature détectées par DA)
- Auto-mode classifier Claude détecte credentials → respecter ses blocages
- Sub-agent skill-creator peut se tromper sur calculs de paths → vérifier empiriquement

## Liens

- [[Raphael-Picard]]
- [[Claude-Forge]]
- [[critique-session-2026-05-20-running-notes-decompose-xread-mcp]]
- [[erreur-password-postgres-clair-mcp-json]]
- [[mcp-paths-relatifs-portabilite]]
- [[running-implementation-notes]]
