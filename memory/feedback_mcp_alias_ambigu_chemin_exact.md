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

**How to apply:** RÈGLE FERME (re-violée 2× : 27 mai session A1 PUIS 27 mai session audit transverse — 3 violations totales malgré ce feedback) : pour `log.md` / `index.md` / `CHANGELOG.md` (stems présents dans plusieurs dossiers du vault), NE JAMAIS appeler `append_note(file="log")` NI `append_note(file="log vault")` NI aucun alias. Aller DIRECTEMENT en Edit chemin exact (`vault/claude-forge/log.md`) — l'édition vault directe n'est PAS bloquée par hook. `append_note` n'est sûr que pour un stem unique.

**Réflexe correct dès le départ** : ouvrir le fichier par chemin exact (Read sur `vault/claude-forge/log.md` ou `read_note_by_path`), repérer le dernier bloc, puis Edit pour insérer le nouveau bloc avant la section finale. Zéro appel `append_note` sur un stem multi-dossier.

**Nettoyage d'un append parasite** : un `append_note` au mauvais fichier laisse DEUX dégâts — (1) le bloc parasite, (2) un résidu cosmétique (newline final perdu, `\ No newline at end of file` au `git diff`). L'Edit pour retirer le bloc ne restaure PAS le newline. Restaurer à l'identique de HEAD via `git checkout -- <fichier>` (le fichier non encore commité revient propre). Vérifier `git diff --stat` vide après.

Toujours lire le chemin réel retourné par l'écriture MCP et corriger immédiatement si faux. Cf [[deny-global-ecrase-allow-projet]] (autre cas de résolution implicite trompeuse).

**4e violation 27 mai (Chantier A /done)** : `append_note(file="log vault")` utilisé — exactement l'alias que la RÈGLE FERME ci-dessus interdit nommément. La règle écrite a maintenant échoué 4×. Conclusion (cf [[feedback_feedback_reviole_3x_regle_insuffisante]]) : l'enrichissement textuel ne suffit plus, garde-fou structurel requis. **À traiter en étape 2b / session future** : hook PreToolUse sur `mcp__forge-brain__append_note` qui vérifie l'unicité du stem dans le vault avant écriture, erreur si stem multi-dossiers (log/index/CHANGELOG). Ne pas se contenter d'enrichir ce feedback une 5e fois.
