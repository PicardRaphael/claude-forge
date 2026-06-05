---
titre: Context Actuel
resume: Working memory dynamique -- mis a jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, memoire de travail, etat actuel]
type: context
status: active
derniere-maj: 2026-06-05
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---

## Phase actuelle
Pipeline complet loop-forge → align-vault-skills dogfoodé de bout en bout et clos. Skill `align-vault-skills` armée en `/loop` hebdo via Task Scheduler local. 1er run de test a détecté 3 drifts réels sur `cc-features-ref` (Opus 4.8, Dynamic Workflows, ultracode) → corrigés et poussés (commits `7468860`, `82d762a`).

## Dernière session (2026-06-05)
### Décisions prises
- `/loop-forge` = SKILL (pas agent) ; 1 seule skill branche code/hors-code ; sortie = SPEC puis dispatch séparé ; checklist Tasks natif anti-oubli ; réflexe "enrichir avant créer" ancré 3 niveaux.
- 1er vrai loop conçu = `align-vault-skills` (scan bidirectionnel vault↔cc-*-ref+agents, idempotent par clé composite `component::note::direction`, kill-switch fichier).
- Infra = Task Scheduler Windows local (cloud écarté : besoin vault local + MCP port 8091 + fichiers locaux).
- État `_alignment-state.json` + rapport `TODO/` gitignored (runtime local, pas versionné).

### En cours
- Rien d'inachevé. Pipeline validé end-to-end : détection 3 drifts → délégation skill-creator → vérif empirique → commit → archivage 2 clés resolved.

### Prochaines étapes
- Laisser tourner le `/loop` hebdo (Task Scheduler). Au prochain run auto, l'état pré-rempli ne re-signalera pas les 3 drifts archivés.
- `/clean-memory` en session dédiée : alerte CRITICAL 243 fichiers memory/ (cible <100).
- Concevoir d'autres loops via `/loop-forge` quand un job répétitif émerge.

## Fils ouverts
- Saturation memory/ (243 fichiers) — chantier `/clean-memory` à part entière, non traité cette session.
- V2 `align-vault-skills` si faux positifs récurrents : 2e agent validateur (vote réel/faux).

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
[[concevoir-loops-travail]]
[[pre-compute-vs-inference-loops-boris]]
