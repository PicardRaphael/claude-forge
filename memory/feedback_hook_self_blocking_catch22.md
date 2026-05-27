---
name: hook-self-blocking-catch22
description: "Un hook qui détecte des patterns interdits se bloquera lui-même s'il contient ces patterns en tant que data (regex, tests). Exclure le hook + ses tests dans EXCLUDED_SUFFIXES."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 72a20014-5e49-4c73-a59e-6512f642233a
---

Catch-22 récurrent : un hook PreToolUse Write|Edit|MultiEdit qui détecte des patterns interdits (regex de meta-commentaires, secrets, etc.) contient légitimement ces patterns dans son CODE pour les matcher. Quand on tente de l'éditer, le hook scanne son propre contenu et bloque.

**Cas concret 24 mai 2026** : `meta-commentary-detector.py` contenait `Cf doctrine` et `Source:` comme strings de patterns. Toute édition via Edit/Write s'auto-bloquait.

**Fix appliqué** :

```python
EXCLUDED_SUFFIXES = (
    "RECAP.md", "recap.md", "CHANGELOG.md", "changelog.md",
    # Self-exclusion: detector + tests contiennent les patterns comme data
    "meta-commentary-detector.py",
    "meta-commentary-detector.ts",  # version port TS
    "test_meta_commentary_detector.py",
)
```

**Why :** sans self-exclusion, la seule façon de modifier le hook est via `Bash + Python` (le hook ne couvre que Edit/Write, pas Bash). C'est un contournement non-discipliné qui peut masquer d'autres bugs et viole l'esprit de la doctrine "hook bloque tout".

**How to apply :**
- Tout hook qui contient ses propres patterns en data DOIT s'auto-exclure
- Idem pour les fichiers de tests qui contiennent des cas adverses (par construction des violations)
- Réflexe : quand on crée un hook, immédiatement ajouter à EXCLUDED_SUFFIXES :
  - Le hook lui-même (variantes .py, .ts, .sh)
  - Les fichiers de tests associés
  - Tout fichier `tests/test_<hook>.<ext>`

**Pattern méta :** "tout système d'enforcement qui scanne du contenu doit prévoir le cas où il scanne SA PROPRE définition". Sinon impossible à maintenir.
