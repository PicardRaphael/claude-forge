---
name: mcp-alias-ambigu-chemin-exact
description: "MCP forge-brain append_note/read avec un alias court (ex \"log\") résout vers le mauvais fichier quand plusieurs notes partagent le stem. Passer chemin exact ou alias unique."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f598fcbc-1e1f-4161-bd42-75eddf13fbdf
---

Les outils MCP forge-brain qui prennent un `file` par alias (`append_note`, `read_note`) résolvent par FTS et peuvent matcher le MAUVAIS fichier quand plusieurs notes partagent le même stem.

**Why:** Le 27 mai, `append_note(file="log", ...)` a écrit dans `2-Casquettes/responsable-ia/log.md` au lieu du `log.md` racine du vault. Cause : le log racine a l'alias `"log vault"` (pas `"log"` seul), donc l'alias court `log` a matché le log casquette. Résultat : entrée parasite à nettoyer + re-écriture au bon endroit (perte de temps).

**How to apply:** RÈGLE FERME (re-violée le 27 mai en session A1 malgré ce feedback) : pour `log.md` / `index.md` / `CHANGELOG.md` (stems présents dans plusieurs dossiers du vault), NE JAMAIS appeler `append_note(file="log")` ou alias court. Aller DIRECTEMENT en Edit chemin exact (`vault/claude-forge/log.md`) — l'édition vault directe n'est PAS bloquée par hook. `append_note` n'est sûr que pour un stem unique. Toujours lire le chemin réel retourné par l'écriture MCP et corriger immédiatement si faux (l'append parasite se nettoie par Edit, pas par MCP). Cf [[deny-global-ecrase-allow-projet]] (autre cas de résolution implicite trompeuse).
