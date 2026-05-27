---
aliases: ["renforcements différés phase 3", "P2 P3 phase 3", "decision differer renforcements forge", "pourquoi pas linux mac forge", "pourquoi pas tags vault", "deferred hardening claude-forge"]
resume: "ADR : pourquoi 5 renforcements claude-forge (portabilité, versioning vault, README Mermaid, tests infra MCP, ADR pivots) sont DIFFÉRÉS après la phase 3, avec leurs déclencheurs de réactivation."
derniere-maj: 2026-05-27
type: knowledge
domaine: claude-code
tags: ["#type/raisonnement", "#projet/claude-forge"]
sources: ["Phase 3 renforcement 2026-05-27", "advisor consultation 2026-05-27"]
---

# Décision : renforcements différés (phase 3)

Lors de la phase 3 (renforcement absolu de claude-forge, 2026-05-27), 5 axes ont été audités. Un seul P0 exécuté (tests cœur MCP `search`/`resolve`), un P1 (tests hooks skill-activation + session-health). Les autres sont **différés volontairement** — pas oubliés. Cette note évite de reposer la question dans 3 mois.

Principe directeur (advisor) : ne pas distribuer du P0/P1 sur tous les axes pour la symétrie. Le besoin doit être réel et présent, pas théorique. Même piège que le "3:1 artificiel" de la phase 2.

## Ce qui est différé et pourquoi

### Portabilité Linux/Mac — P3
- **État** : `install.bat` Windows-only ; `mcp-autostart.py` utilise des flags Windows (`DETACHED_PROCESS`, `CREATE_NO_WINDOW`, `CREATE_NEW_PROCESS_GROUP`).
- **Pourquoi différé** : la cible déclarée est Windows. Faire du cross-OS par anticipation = code spéculatif non testé sur une plateforme qu'on n'utilise pas.
- **Déclencheur de réactivation** : un collaborateur non-Windows veut forker, OU intégration au partner network Anthropic exige du multi-OS. À ce moment : `install.sh` équivalent + branche `os.name`/`sys.platform` dans mcp-autostart pour les flags subprocess.

### Versioning du vault (snapshot daté) — P3
- **État** : aucun git tag, aucun snapshot. `log.md` (append-only) + `CHANGELOG.md` (narratif) tracent l'historique. Reconstruction d'un état à une date = uniquement via `git log --before=` manuel.
- **Pourquoi différé** : git versionne déjà tout. "Reconstruire l'état au 2026-05-01" est un besoin théorique aujourd'hui.
- **Déclencheur** : besoin de mesurer le compounding dans le temps (comparer état T0 vs T1) OU exigence de reproductibilité. Solution légère alors : `git tag vault-YYYY-MM` à chaque pivot doctrinal majeur (30s), pas de mécanisme lourd.

### README + schéma Mermaid — P3
- **État** : README clair, à jour, avec install + usage. Pas de schéma d'archi visuel.
- **Pourquoi différé** : cosmétique tant que personne d'externe ne consulte le repo.
- **Déclencheur** : présentation à un tiers (recruteur, partenaire Anthropic, contributeur).

### Tests infra MCP (watcher / server / git_sync) — P2
- **État** : `watcher.py`, `server.py`, `git_sync.py` = zéro test. I/O fichiers + subprocess git + boucles background.
- **Pourquoi différé** : ces modules font de l'I/O et du subprocess — tests fragiles à mocker, ratio coût/valeur défavorable tant qu'aucun bug n'est observé. Le cœur logique (`search`/`resolve`) était le vrai risque et il est désormais couvert.
- **Déclencheur** : un bug watcher (note non réindexée) ou git_sync (push silencieusement raté) observé en production.

### ADR dédiés pour les pivots structurants — P2
- **État** : la doctrine 22 mai a une note complète ([[raisonnement-22mai-doctrine-vs-enforcement]]). Les autres pivots (Jarvis/Tony Stark, séquence [[methode-analyser-repo|A→B→C→D→E]], délégation forcée, MCP vs RAG passif) sont tracés mais éparpillés (rules, techniques, casquette).
- **Pourquoi différé** : ces pivots SONT tracés (rule `sequence-canonique-modification.md`, `mcp-vs-skills-doctrine`, CLAUDE.md contrat Jarvis). Formaliser chacun en ADR = bureaucratie tant qu'aucun tiers n'a besoin du "pourquoi".
- **Déclencheur** : onboarding d'un contributeur tiers qui doit comprendre les choix de conception. Priorité alors : la délégation forcée (seule sans foyer canonique unique).

## Reminders (×3) non testés — P3
`session-reminder`, `learning-reminder`, `proactivity-reminder` : side-effects fail-open simples. Les tester = gonfler la couverture sans valeur (même piège que tester les reminders pour le ratio). Différé sauf bug observé.

## Lien

Matrice complète : [[phase-3-renforcement-audit]] (0-Inbox). Pivot doctrinal parent : [[raisonnement-22mai-doctrine-vs-enforcement]]. Pattern décisionnel : [[bug-caracterise-fix-trivial-vs-couteux]] (trivial = fix now, coûteux = phase dédiée — appliqué ici à l'échelle d'un axe entier).
