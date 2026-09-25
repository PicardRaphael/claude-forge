---
titre: "forge-review 2026-07-09 — fusions et kills de skills"
resume: "Review stratégique forge du 9 juillet 2026 sur les skills — 0 KILL, 2 fusions appliquées, 1 en measure-first (F2 trio doctrine), 2 rejetées après DA ; le levier forge est la collision de descriptions, pas la désuétude."
aliases:
  - forge-review-2026-07-09
  - forge review juillet 2026
  - journal forge-review
  - review fusions skills forge
  - verdicts KILL EVOLVE FUSION
derniere-maj: 2026-09-25
auteur: claude
type: review
tags:
  - "#type/review"
  - "#domaine/claude-code"
  - "#projet/claude-forge"
---
# forge-review — 9 juillet 2026 (scope skills)

Contrainte posée par Raphaël : perf-first. Journal promu depuis `memory/project_forge_review.md` le 25 sept. 2026 ; les forge-review suivantes s'ajoutent comme notes sœurs de ce dossier.

## Verdicts

- **KILL : 0.** Aucun poids mort. Le levier de forge est la collision de descriptions entre skills, pas leur désuétude.
- **FUSIONS appliquées (2)** :
  - F1 `cc-rag-ref` → `rag-design/references/` ;
  - F3 `web-search-canonical-source` → rule `contenu-externe-non-fiable`.
- **FUSION en measure-first (1)** : F2, le trio doctrine. L'hôte imposé est `methode-pivoter-doctrine` (34 backlinks). Le protocole de mesure est dans `output/mesure-F2-fusion-doctrine.md`.
- **FUSIONS rejetées après DA (2)** :
  - F4 `python-script-refactor-masse` : KEEP, trigger resserré ;
  - F5 `cc-prompt-ref` : KEEP, parce que c'est l'infrastructure des créateurs.
- **DA** : un BLOCKING sur F2 (réversibilité). Voir [[critique-2026-07-09-fusions-skills-forge]].

## Pattern retenu

Raisonner par budget (« passer de N à M skills ») au lieu de juger la friction et la valeur item par item est un anti-pattern (cf [[critique-2026-05-21-refonte-hooks-16-vers-6]]). Chaque fusion se juge seule.

Les skills peu utilisées sont justement celles dont Claude Code retire la description du listing. Ranger leur contenu dans `references/` le protège.

## Suivi (ouvert au 9 juillet, non revérifié depuis)

- A/B de déclenchement de F2, selon le protocole de `output/mesure-F2-fusion-doctrine.md`.
- Application de `delegate-guard.py.proposed`, qui attend une validation manuelle de Raphaël.

## Liens

- [[forge-review]]
- [[comment-creer-skill]]
- [[methode-pivoter-doctrine]]
