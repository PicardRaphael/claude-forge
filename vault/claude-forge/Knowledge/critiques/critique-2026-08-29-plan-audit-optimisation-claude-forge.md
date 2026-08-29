---
titre: "Critique — plan d'audit et d'optimisation claude-forge"
type: knowledge
domaine: Codex
derniere-maj: 2026-08-29
auteur: Codex
---

## Devils Advocate — Plan d’audit et d’optimisation claude-forge

**Intention déclarée :** Réduire la dette de contexte, la sur-rétention mémoire et la surface de sécurité de forge sans big-bang, tout en réalignant doctrine, skills, agents, règles et hooks.

### Verdict

**Bloquants :** 4 | **Avertissements :** 8 | **Nitpicks :** 2

**Décision recommandée :** BLOQUER le plan dans cet ordre; livrer seulement après correction de la séquence et réouverture explicite des ADR concernées.

### Bloquants scorés

- **99/100 — Contradiction silencieuse avec une décision acceptée.** Retirer `@memory/MEMORY.md` contredit [[decision-memoire-dans-le-repo]] (2026-05-27, statut accepté). Soit le plan a tort, soit il doit ROUVRIR formellement la décision; la contourner en silence n’est pas une option.
- **95/100 — Les évaluations arrivent après les mutations qui ont besoin d’elles.** Le rappel actuel produit déjà des hors-sujet et manque un project file. Retirer l’import puis mesurer rend impossible une comparaison fiable et crée un risque de perte de rappel utile.
- **88/100 — Transformer des règles globales en skills/path-scoped peut supprimer des garanties déterministes.** Une skill se déclenche probabilistiquement; une règle path-scoped ne couvre pas nécessairement les prompts, MCP et actions sans fichier. La taille ou le zéro-référence ne prouve pas qu’une règle est inutile.
- **86/100 — “Corriger les canoniques” sans registre de claims et pivot formel ne résout pas la dérive.** On risque de remplacer un millefeuille contradictoire par un nouvel instantané bientôt obsolète, sans propager la décision aux règles, templates, adapters et tests.

### Corrections nécessaires

1. Mettre les evals et la baseline avant toute suppression ou désactivation.
2. Rouvrir formellement [[decision-memoire-dans-le-repo]] avant toute suppression de l’import; documenter portabilité, rappel, coût contexte et rollback.
3. Classer chaque règle par propriété à préserver: invariant global déterministe, garde de sécurité, contexte path-scoped, ou workflow optionnel.
4. Définir le scope des settings: repo modifiable; toute mutation de `~/.claude/settings.json` doit respecter [[decision-settings-global-modification-manuelle]] et être fournie comme bloc parent complet à appliquer manuellement.
5. Pour les canoniques, construire une matrice claim -> source officielle actuelle -> décision -> surfaces dérivées; exécuter le pivot et son check de propagation.
6. Ne retirer la mémoire d’un agent qu’après inventaire des apprentissages utiles et extraction vers la bonne autorité.
7. Mettre les métriques `last_used` dans une télémétrie ignorée ou agrégée; ne pas salir git à chaque rappel.
8. Partager entre Claude/Codex les politiques et fixtures de tests, pas forcément un runtime hook commun.

### Version corrigée du plan

- **Gate 0 — Baseline et décisions.** Geler les suppressions. Construire 30–50 prompts-oracles couvrant mémoire, projets, vault, règles et sécurité. Mesurer hit-rate, precision@3, faux rappels, rappel périmé, contexte chargé, latence, prompts de permission et faux blocages. Lister les ADR acceptées touchées et les critères de rollback.
- **Wave 1 — Doctrine et sécurité, séparées.** Corriger les canoniques par registre de claims et pivot formel, puis seulement les creator skills. Côté sécurité, produire un diff par outil/commande et un ACL MCP explicite: chercheurs read-only, writer unique en session principale, avec tests adverses. Toute modification globale reste manuelle selon l’ADR.
- **Wave 2 — Retrieval canary.** Améliorer `memory-recall` pour hydrater un ou deux extraits pertinents avec provenance, au lieu de simples pointeurs. Introduire statut, dernière validation et expiry uniquement pour les mémoires temporaires. Garder l’import pendant le canary et comparer à la baseline.
- **Wave 3 — Rétention.** Retirer d’abord `session-reminder`, clairement redondant. Remplacer les watchers par âge, utilité, expiry et rappels réellement observés. Réduire ou retirer l’import seulement si les evals passent et après réouverture de l’ADR. Nettoyage exclusivement sous validation humaine, avec archive/rollback.
- **Wave 4 — Agents et règles.** Décider la mémoire agent par besoin: grader/self-updater probablement aucune après extraction; DA et inspector à justifier; code-dev local ou project avec cap/TTL. Pour les règles, conserver les invariants globaux et gardes, path-scoper le contexte réellement lié aux fichiers, convertir en skills uniquement les workflows optionnels. Aucun quota arbitraire et aucune suppression fondée sur “zéro référence”.
- **Wave 5 — Simplification plateforme.** Partager un corpus de politiques, fixtures et tests entre Claude/Codex; conserver des adaptateurs d’exécution séparés tant que les schémas diffèrent. A/B tester `skill-activation` contre les descriptions natives corrigées avant suppression.
- **Gate de sortie par wave.** Tests unitaires + evals comportementales + diff de contexte + test de rollback; une seule variable architecturale changée à la fois.

### Vault — Historique pertinent

[[decision-memoire-dans-le-repo]] est directement contredite et non adressée.
[[decision-settings-global-modification-manuelle]] est compatible uniquement si le plan distingue clairement settings projet et settings global.
