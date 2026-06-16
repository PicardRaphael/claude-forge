---
titre: Context Actuel
resume: Working memory dynamique -- mis a jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, memoire de travail, etat actuel]
type: context
status: active
derniere-maj: 2026-06-11
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---

## Phase actuelle
Outillage workflow IA cross-repo (neo_ia + neoteem-back-ts + skill forge) : /spec classe désormais les tickets par TYPE (FEATURE/BUG/OPTIMISATION) et route vers les 6 epics. Prochain gros chantier annoncé : CDC NeoMail.

## Derniere session (2026-06-11)
### Decisions prises
- Classification de ticket à 3 catégories (FEATURE/BUG/OPTIMISATION) gravée dans les 3 /spec jumeaux + `references/epics-jira.md` partagé (byte-identique ×3).
- 6e epic ajouté (NeoDoc N2-103047) — le référentiel disait « 5 epics » à tort.
- `refactor-scan` (neo_ia) corrigée : `user-invocable` (bug `user-invokable`), méta frontmatter retirée, densifiée 208→75L, périmètre d'audit complet préservé. Pas de renommage (référencée 11 fichiers).
- N2-111316 (durcissement SQL shared_utils) créé en `[IA] BUG`, parent N2-68082 (Chatbots), assigné Raphael — à rebasculer en `[IA] Optimisation` quand le type existera.
- Ordre validé : durcissement SQL shared_utils AVANT le CDC NeoMail (reuse-first : assainir le socle partagé avant de bâtir dessus).
- Plans nettoyés : `harnais-repo-parfait.md` supprimé (notes de session livrées) ; `docs/futur/` GARDÉ (visions différées, pas des plans terminés).

### En cours
- Rien d'ouvert techniquement — les 3 repos sont commités/poussés (neo_ia 55cd899, back-ts 4653f40, forge 96e2b37 + 4b5d627).

### Prochaines etapes
- **CDC NeoMail** (gros chantier de cadrage) — y intégrer l'exigence « zéro S608 » (les 6 S608 NeoMail hors-prod absorbées par le refacto).
- Lancer la story durcissement SQL N2-111316 via `/feature` quand souhaité (one-shot, parité).
- Quand le PM aura créé `[IA] Optimisation` dans Jira : rebasculer N2-111316.

## Fils ouverts
- Type Jira `[IA] Optimisation` : création déléguée au PM (action humaine). Mapping skills déjà prêt (résolution par nom).
- Une autre session Claude tournait en parallèle sur neo_ia (story SQL + gate mypy) — branches `us/N2-111316` et `chore/mypy-gate-vert` côté autre session, ne pas marcher dessus.
- P1 différés neo_ia (promptfoo, Presidio AI Act 2 août, DeepEval, Langfuse budgets) — stories /spec à venir.

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
