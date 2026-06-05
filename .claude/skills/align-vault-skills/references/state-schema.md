# Schéma de l'état `.claude/_alignment-state.json`

Journal d'idempotence. Maintenu par `scripts/alignment_state.py`, jamais édité à la main pendant un cycle.

## Forme

```json
{
  "resolved": ["cc-features-ref::goal::descendant", "..."],
  "ignored":  ["devils-advocate::pattern-X::montant", "..."]
}
```

- **`resolved`** — écarts déjà corrigés (le dispatch a été fait, le composant reflète maintenant le vault). Ne plus signaler.
- **`ignored`** — écarts vus et écartés volontairement par Raphaël (faux positif accepté, ou écart montant légitime « le composant a raison, pas le vault »). Ne plus signaler.

Tout écart dont la clé n'est dans NI `resolved` NI `ignored` est un **nouvel écart** → il apparaît dans le rapport.

## Clé d'idempotence — composite lisible, PAS un hash

```
<composant>::<note-vault>::<sens>
```

- `<composant>` : nom du fichier sans extension (`cc-features-ref`, `devils-advocate`).
- `<note-vault>` : slug ou titre de la note canonique concernée (`goal`, `comment-creer-hook`).
- `<sens>` : `descendant` (vault → composant manquant) ou `montant` (composant → vault, à arbitrer).

Exemple : `cc-features-ref::goal::descendant`.

**Pourquoi pas un hash** : la SPEC §4 parlait de « hash composant+note+type », mais un LLM ne calcule pas un hash stable — deux passes produiraient des clés différentes, ce qui casserait le critère de reproductibilité (Bloc 5.2) par construction. Une clé composite lisible est déterministe, auditable à l'œil, et stable. `make_key()` dans le script est la seule source de clés.

## Cycle de vie

1. `check` — crée le fichier vide `{"resolved":[],"ignored":[]}` au 1er run si absent.
2. `filter` — lit l'état, retire les écarts dont la clé est déjà connue.
3. `resolve` / `ignore` — après validation Raphaël, ajoute les clés traitées. **Déclenché par Raphaël en session interactive, pas par le loop** : le loop ne fait que LIRE l'état et écrire le rapport. C'est le passage de relais humain qui marque resolved/ignored, sinon un écart réel disparaîtrait du rapport sans avoir été corrigé.

## Anti-fatigue

L'état est la mémoire qui empêche le re-signalement. Le cas test de la SPEC (§9) : une fois `/goal` + Agent View corrigés et leurs clés dans `resolved`, ils ne doivent JAMAIS réapparaître dans un rapport ultérieur.
