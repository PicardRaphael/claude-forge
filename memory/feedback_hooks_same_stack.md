---
name: hooks-same-stack
description: Les hooks doivent utiliser le même langage/runtime que le projet (pas Python dans un projet TypeScript/Bun).
type: feedback
---

Toujours écrire les hooks dans le même stack que le projet.

**Why:** L'utilisateur a corrigé un hook Python dans un projet Bun/TypeScript. Cohérence du stack, pas de dépendance externe inutile (python3).

**How to apply:** Projet Bun → hooks en `.ts` avec `#!/usr/bin/env bun`. Projet Python → hooks en `.py`. Ne jamais mélanger.
