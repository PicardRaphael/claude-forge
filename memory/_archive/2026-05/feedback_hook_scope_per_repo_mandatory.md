---
name: hook-scope-per-repo-mandatory
description: Tout hook avec scope par chemin (SCOPED_PATTERNS) DOIT aussi vérifier le scope par repo via is_inside_<project>. Sinon pollution cross-repo garantie.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 72a20014-5e49-4c73-a59e-6512f642233a
---

Quand un hook claude-forge utilise des patterns de chemin pour décider quoi scanner (ex : `CLAUDE.md`, `.claude/agents/*.md`), il scanne par défaut TOUS les fichiers matchant ces patterns, peu importe le repo où l'écriture a lieu.

**Cas concret 24 mai 2026** : le hook `meta-commentary-detector.py` de claude-forge a bloqué une tentative de `Write` dans `neot-v2/ia_back/.claude/hooks/meta-commentary-detector.ts` depuis la session claude-forge — alors qu'il devrait n'enforcer QUE dans claude-forge.

**Why :** quand la session Claude principale (claude-forge) écrit dans un autre repo (cross-repo write), les hooks claude-forge s'exécutent toujours. Le pattern `[/\\]\.claude[/\\]hooks[/\\][^/\\]+$` match aussi dans `neot-v2/ia_back/.claude/hooks/`. Sans guard `is_inside_forge`, le hook pollue.

**How to apply :**

Tout nouveau hook avec `SCOPED_PATTERNS` (chemin) doit AUSSI implémenter :

```python
FORGE_PROJECT_DIR = str(Path(__file__).resolve().parent.parent.parent).replace("\\", "/").lower()

def is_inside_forge(path: str) -> bool:
    return path.replace("\\", "/").lower().startswith(FORGE_PROJECT_DIR)

# Dans main(), AVANT toute autre vérif :
if not is_inside_forge(file_path):
    sys.exit(0)  # fail-open hors du repo
```

**Précédent canonique** : `delegate-guard.py` claude-forge a cette logique depuis le début. Quand on copie un hook depuis delegate-guard pour en créer un nouveau, garder cette structure.

**Check audit** : grep tous les hooks claude-forge pour `is_inside_` — si un hook a `SCOPED_PATTERNS` sans `is_inside_forge`, c'est un bug latent à fixer.

**Port cross-repo (ia_back, neo_ia)** : la version dans chaque repo doit utiliser `CLAUDE_PROJECT_DIR` env var ou `process.cwd()` comme racine, pas un path hardcodé vers claude-forge.
