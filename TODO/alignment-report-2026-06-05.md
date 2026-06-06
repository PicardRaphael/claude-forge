# Alignment report — 2026-06-05

> Généré par la skill `align-vault-skills` (loop hebdo). Lecture seule : aucun composant modifié. Raphaël déclenche les dispatches.

## Vérification

- **Verdict global :** FAIL
- **Couverture :** 1/19 composants scannés (INCOMPLET)
- **Reproductibilité :** non vérifiée ce cycle (test 1 passe)
- **Échantillon (0 faux positif) :** 0 faux positif — les 3 notes vault citées existent
- **Notes :** Couverture partielle assumée (1/19) pour test bout-en-bout. PASS attendu au 1er run /loop complet.

## Nouveaux écarts (3)

| # | Composant cible | Sens | Note vault | Action suggérée |
|---|---|---|---|---|
| 1 | cc-features-ref | descendant | CC 28 mai 2026 - Opus 4.8 + Dynamic Workflows | Ajouter Dynamic Workflows (research preview, 28 mai, v2.1.154) à cc-features-ref. Déléguer à skill-creator. |
| 2 | cc-features-ref | descendant | CC juin 2026 - v2.1.160 ultracode | Ajouter le déclencheur ultracode (v2.1.160, 2 juin) à cc-features-ref. Déléguer à skill-creator. |
| 3 | cc-features-ref | descendant | CC 28 mai 2026 - Opus 4.8 + Dynamic Workflows | Mettre à jour section Effort/modèles : Opus 4.8 absent (cc-features-ref ne cite que 4.6/4.7). Déléguer à skill-creator. |

### Clés d'idempotence (à archiver dans l'état après traitement)

- `cc-features-ref::CC 28 mai 2026 - Opus 4.8 + Dynamic Workflows::descendant`
- `cc-features-ref::CC juin 2026 - v2.1.160 ultracode::descendant`
- `cc-features-ref::CC 28 mai 2026 - Opus 4.8 + Dynamic Workflows::descendant`

