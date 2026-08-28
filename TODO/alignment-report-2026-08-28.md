# Alignment report — 2026-08-28

> Généré par la skill `align-vault-skills` (loop hebdo). Lecture seule : aucun composant modifié. Raphaël déclenche les dispatches.

## Vérification

- **Verdict global :** PASS
- **Couverture :** 8/8 composants scannés (OK)
- **Reproductibilité :** Deux passes concordantes : recherche globale puis lecture integrale des huit foyers
- **Échantillon (0 faux positif) :** 5/5 ecarts relus, 0 faux positif
- **Notes :** Scan cible second cerveau : profil Raphael, projets stables, decisions et adaptateurs Claude/Codex.

## Écarts détectés (5, résolus le 2026-08-28)

Les cinq corrections ont été appliquées puis leurs clés enregistrées dans
`.claude/_alignment-state.json`. Le prochain scan ne doit pas les re-signaler.

| # | Composant cible | Sens | Note vault | Action suggérée |
|---|---|---|---|---|
| 1 | memory-discipline | montant | Raphael-Picard | **RÉSOLU** — vault canonique, profil local réduit à un adaptateur |
| 2 | done-claude | descendant | Raphael-Picard | **RÉSOLU** — faits personnels routés vers le profil et les casquettes vault |
| 3 | done-codex | descendant | Raphael-Picard | **RÉSOLU** — adaptateur Codex aligné sur le profil vault |
| 4 | forge-brain-claude | montant | Claude-Forge | **RÉSOLU** — enrichissement avant création et projets stables canoniques |
| 5 | AGENTS.md | descendant | Claude-Forge | **RÉSOLU** — création projet et choix routés vers `project-memory` |

### Clés d'idempotence archivées dans l'état

- `memory-discipline::Raphael-Picard::montant`
- `done-claude::Raphael-Picard::descendant`
- `done-codex::Raphael-Picard::descendant`
- `forge-brain-claude::Claude-Forge::montant`
- `AGENTS.md::Claude-Forge::descendant`
