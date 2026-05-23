---
titre: Context Actuel
resume: Working memory dynamique -- mis a jour par /done, lu par /recap. Session 2026-05-23 : neo_ia session 3 complete (15 commits) + pattern anti-reentrance + instrumentation Niveau 3 + 5 notes vault.
aliases:
  - "context actuel"
  - "contexte courant"
  - "working memory"
  - "memoire de travail"
  - "etat actuel"
type: context
status: active
derniere-maj: 2026-05-23
auteur: claude
tags:
  - "#type/context"
  - "#meta/working-memory"
---

## Phase actuelle

neo_ia session 3 complete et pushed (15 commits ahead origin/develop integres). Instrumentation Niveau 3 deployee (hook PostSubagentStop CSV), pattern anti-reentrance documente, dette F1+F2 corrigee. Reanalyse Niveau 3 prevue dans 1-2 semaines avec n>>30 invocations.

## Derniere session (2026-05-23)

### Decisions prises

- **Refactor dev-neochat** A+B+C+scope : 158L->131L (-39%), 11 tools->6 (verif empirique 0% usage WebSearch/WebFetch/3MCP/MultiEdit), 8 skills->5, scope clarifie (apps/neochat 93% primaire, shared_* 32%+19% secondaire avec consultation Things to leave alone)
- **Pattern anti-reentrance** : sub-agent ne peut PAS invoquer Agent. Format ESCALADE REQUISE markdown 5 champs (Detection, Raison, Agent recommande, Etat actuel, Suite recommandee). Corrige dev-neochat + dev-shared-utils.
- **packages/CLAUDE.md complete** : NeoMail ajoute (3e app), 8 modules shared_utils detailles, Things to leave alone exhaustif, routing agents table + note anti-reentrance
- **Niveau 3 instrumentation deployee** : hook agent-metrics-logger.py PostSubagentStop -> .claude/agent-metrics.csv (append-only, gitignored). Rule scope invocations dev-* (option b advisor).
- **architect-deep PAS touche** : Niveau 1 flag 5/5 seuils MAIS Niveau 2 = 6 ops typique (faux positif Niveau 1, validation Cat Wu canonique max 6-8 ops)
- **guard-ddl-ban hook security** : DA verdict KEEP avec 3 corrections appliquees (bypass env var, retrait alembic, message clarifie). 20 tests adverses passent.
- **CHANGELOG.md** : 6 entrees groupees session 3 sous section 2026-05-22

### En cours

- (rien -- chantier session 3 termine, push reussi sur 2 repos bitbucket+github)

### Prochaines etapes

- **Dans 1-2 semaines** : reanalyser `.claude/agent-metrics.csv` neo_ia avec n>>30 invocations distribuees. Critere statistique : si p50 > 8 ops sur > 20 invocations dev-* malgre rule scope -> split confirme. Sinon -> rule scope suffit.
- Skill `/check-agent-metrics` forge pas creee finalement. Analyse manuelle quand pret via script `output/analyse-dev-neochat-empirique.py` adapte.

## Fils ouverts

- **dev-neodoc (n=2) et dev-neomail (n=1)** : verdict reporte faute donnees suffisantes. Attendre Niveau 3 mature.
- **Cleanup claude-forge** : beaucoup de deletions output/ et modifs canoniques non-committees (hors scope session 3). A trier par Raphael quand il veut.
- **architect-deep audit ligne par ligne "Would removing this cause mistakes?"** : jamais execute (preference Raphael = pas le faire sans donnees). A reconsiderer si patterns Niveau 3 le confirment.

## Capitalisation session

### Memoire projet (4 nouveaux feedback)

- [[feedback_methode_abcde_carte_pas_verdict]] -- Niveau 1 = carte, pas verdict
- [[feedback_gotchas_line_numbers_verifies]] -- Tout claim fichier.py:N = grep -n verif AVANT relayage
- [[feedback_anti_reentrance_sub_agents]] -- Eviter "deleguer/rediriger" dans Hors scope sub-agent
- [[feedback_couper_loops_perfectionnisme]] -- Couper loops "es-tu parfait" apres ABCDE+advisor valide

### Vault forge (5 notes + 1 MOC update)

- [[critique-2026-05-22-guard-ddl-ban]] -- DA verdict KEEP avec 3 corrections
- [[erreur-gotchas-line-numbers-non-verifies-claudemd]] -- Incident F1+F2 session 3
- [[niveau-1-static-mesure-agents-neo-ia-2026-05-22]] -- Mesure 14 agents Niveau 1 + UPDATE Niveau 2
- [[architecture-decision-niveaux-mesure-agents]] -- Raisonnement direction inversee Niveau 1/2/3
- [[anti-reentrance-sub-agents-pattern-escalade]] -- Doctrine + pattern ESCALADE REQUISE
- [[MOC-Techniques]] -- 2 wikilinks ajoutes section Agents & Harness Engineering

## Liens

[[Raphael-Picard]]
[[Claude-Forge]]
[[anti-reentrance-sub-agents-pattern-escalade]]
[[architecture-decision-niveaux-mesure-agents]]
