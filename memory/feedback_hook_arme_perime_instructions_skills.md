---
name: hook-arme-perime-instructions-skills
description: "Armer un hook PreToolUse peut périmer au runtime des instructions de skills existantes — grep le verbe bloqué"
metadata:
  type: feedback
---

Quand on arme un hook PreToolUse qui bloque un outil (ex. `vault-write-guard` matche `Write|Edit|MultiEdit` sur le vault), les instructions de skills écrites AVANT le hook qui prescrivent cet outil deviennent **cassées au runtime**, pas seulement obsolètes : une skill qui suit l'instruction déclenche un blocage. Le drift est silencieux — rien ne signale qu'une skill prêche désormais un outil interdit.

**Why:** 7 juin 2026, tâche rules post-6-B. `done/SKILL.md` (L222+L301) prêchait « `Write` la note vault » ; `vault-write-guard` (armé pièce 2 du 6-B) matche `Write` aussi (pas que `Edit`) → un `/done` qui suivait l'instruction aurait été bloqué. Le seul laggard : toutes les autres skills capitalisantes (`reasoning-cache`, `methode-pivoter-doctrine`, `da-blocking-arbitrage`…) étaient déjà MCP-only.

**How to apply:** après avoir armé un hook PreToolUse qui bloque un outil/verbe (Write/Edit/Bash/MCP), grep les SKILL.md + rules pour ce verbe dans le périmètre gardé. Toute instruction qui le prescrit encore est cassée au runtime → corriger vers l'alternative sanctionnée. Distinguer périmètre exact : `vault-write-guard` ne matche que `vault/claude-forge/` → `Write` dans `memory/` reste valide (ne pas sur-corriger). Cf [[feedback_mcp_alias_ambigu_chemin_exact]] (drift jumeau côté outils MCP `file=`).
