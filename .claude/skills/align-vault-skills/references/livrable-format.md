# Format du livrable `TODO/alignment-report-<date>.md`

Écrit par `scripts/alignment_state.py write-report` à partir d'un payload JSON. La skill NE rédige PAS le markdown à la main (évite la casse heredoc Windows et garantit un format stable).

## Payload JSON attendu

```json
{
  "date": "2026-06-05",
  "coverage": {
    "expected": 19,
    "scanned": 19,
    "components": ["cc-features-ref", "cc-skills-ref", "...", "skill-creator", "..."]
  },
  "verdict": {
    "coverage": true,
    "reproducibility": "2 passes concordantes sur l'échantillon 06-05",
    "sample": "3/5 écarts relus, 0 faux positif",
    "pass": true,
    "notes": "optionnel"
  },
  "new_gaps": [
    {
      "component": "cc-features-ref",
      "direction": "descendant",
      "note": "goal",
      "action": "déléguer à skill-creator : ajouter la section /goal à cc-features-ref",
      "key": "cc-features-ref::goal::descendant"
    }
  ]
}
```

## Structure rendue

1. **Titre** + bannière « lecture seule, Raphaël déclenche ».
2. **## Vérification** — verdict global PASS/FAIL + 3 lignes (couverture chiffrée, reproductibilité, échantillon).
3. **## Nouveaux écarts (N)** — tableau `# | Composant cible | Sens | Note vault | Action suggérée`, puis la liste des clés d'idempotence à archiver. Si N=0 : phrase explicite « aucun nouvel écart ».

## Sens d'un écart

| Sens | Signification | Formulation de l'action |
|------|---------------|-------------------------|
| `descendant` | doctrine/feature présente au **vault**, absente d'un composant qui devrait la refléter | « ajouter X à \<composant\> » — à corriger |
| `montant` | affirmation d'un **composant** absente ou contredite par le vault | « **à arbitrer** : le composant dit X, le vault dit Y. Composant plus récent ? → mettre à jour le vault. Périmé ? → corriger le composant. » |

Un écart montant n'est JAMAIS formulé « corriger le composant » d'office : il peut être légitime (composant plus à jour que le vault). Cf SPEC §Notes.

## Action suggérée = commande de dispatch

Chaque écart porte une action exécutable par Raphaël, jamais auto-appliquée :
- composant = skill → `déléguer à skill-creator : ...`
- composant = agent → `déléguer à subagent-creator : ...`
- écart montant → `arbitrer puis dispatch vers vault (create_note/update) OU skill-creator/subagent-creator`

## Rétention

Livrables conservés 30 j (SPEC §3). Le nettoyage des vieux `alignment-report-*.md` n'est pas automatisé ici — purge manuelle ou tâche séparée.
