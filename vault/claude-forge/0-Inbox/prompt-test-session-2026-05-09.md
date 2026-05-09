---
titre: Prompt de test session 2026-05-09
resume: Prompt optimisé pour valider TOUTES les améliorations — MCP, /done, /watch, vault, devil's advocate, Stop hook, agents, skills
aliases:
  - prompt test
  - test session
  - validation session
type: context
status: active
derniere-maj: 2026-05-09
auteur: claude
tags:
  - "#type/context"
  - "#meta/test"
---

## Prompt à copier dans une nouvelle session Claude Code

```
Tu vas tester TOUTES les améliorations de la session 2026-05-09. Pour chaque test, rapporte OK/FAIL + détail si FAIL. Ne skip aucun test.

IMPORTANT : le MCP forge-brain doit tourner. Vérifie avec `netstat -an | grep 8091`. Si port fermé, lance : `python mcp-forge-brain/start.py` en background.

---

### BLOC 1 — MCP forge-brain (accès vault)

**Test 1.1 — vault_stats**
Appelle vault_stats() via MCP. Combien de notes, tags, wikilinks, aliases ?

**Test 1.2 — search_brain**
Appelle search_brain(query="Raphael Picard", limit=3). Quels résultats ?

**Test 1.3 — read_note par alias**
Appelle read_note(file="forge") — doit résoudre vers Claude-Forge.md via l'alias.

**Test 1.4 — list_notes par dossier**
Appelle list_notes(folder="1-Projets", limit=20). Combien de notes de contexte projet ?

**Test 1.5 — get_backlinks**
Appelle get_backlinks(file="Raphael-Picard"). Quelles notes pointent vers le profil ?

**Test 1.6 — get_tags**
Appelle get_tags(). Les tags #type/context et #type/projet existent-ils ?

**Test 1.7 — create_note + update_property**
Crée une note test : create_note(path="0-Inbox/test-mcp-2026-05-09.md", content="---\ntitre: Test MCP\nresume: Note de test\naliases: [test mcp, test]\ntype: context\nderniere-maj: 2026-05-09\ntags:\n  - '#meta/test'\n---\n\nCeci est un test MCP.\n"). Puis update_property(file="test-mcp-2026-05-09", name="derniere-maj", value="2026-05-09"). Puis supprime la note avec Bash (rm vault/claude-forge/0-Inbox/test-mcp-2026-05-09.md).

---

### BLOC 2 — Profil holistique (vault structure)

**Test 2.1 — Note Raphael Picard**
Appelle read_note(file="Raphael-Picard"). Confirme : date de naissance (23/01/1990), famille (Jennifer, Rose, Louis), gaming (Diablo 4, PoE2), vision (expert IA reconnu), parcours (moniteur d'équitation → dev → Lead IA).

**Test 2.2 — Projets Neoteem**
Appelle list_notes(folder="1-Projets/Neoteem"). Confirme : Neoteem.md, ia_back.md, neo_ia.md, neoteem-brain.md, bdd.md existent.

**Test 2.3 — Casquettes**
Appelle list_notes(folder="2-Casquettes"). Confirme : Raphael-Picard.md, Famille.md, Gaming.md existent.

**Test 2.4 — Context Note**
Lis vault/claude-forge/0-Inbox/context-actuel.md. Confirme : dernière session, décisions prises, prochaines étapes, fils ouverts.

---

### BLOC 3 — /watch (transcription YouTube)

**Test 3.1 — /watch fonctionne**
Lance /watch https://www.youtube.com/watch?v=dQw4w9WgXcQ
Confirme qu'une transcription est retournée (même partielle/courte).

---

### BLOC 4 — Devil's advocate pipeline

**Test 4.1 — État initial propre**
Vérifie que .claude/.devil-advocate-needed ET .claude/.devil-advocate-done n'existent PAS (reset par SessionStart).

**Test 4.2 — Guard PostToolUse crée le marker**
Lance un agent general-purpose avec une tâche simple (ex: "dis bonjour"). Ensuite vérifie que .claude/.devil-advocate-needed EXISTE maintenant.

**Test 4.3 — Stop hook bloque**
Essaie de terminer (dis "j'ai fini"). Le Stop hook DOIT bloquer avec "Devil's advocate non lancé". Rapporte si ça bloque ou pas.

**Test 4.4 — Devil's advocate résout**
Lance l'agent devils-advocate sur un sujet simple : "Critique rapide : est-ce que le MCP forge-brain est bien configuré ?". Vérifie que .claude/.devil-advocate-done EXISTE. Le devil's advocate DOIT chercher dans le vault via MCP (search_brain) — PAS via CLI.

**Test 4.5 — Stop hook laisse passer**
Après le devil's advocate, le Stop hook ne doit PLUS bloquer.

---

### BLOC 5 — CLAUDE.md + Rules

**Test 5.1 — CLAUDE.md vérifié**
Lis CLAUDE.md et confirme :
- Contrat Jarvis : règle autonomie (advisor + devil's → agir sans demander)
- Vault : MCP UNIQUEMENT mentionné (pas de CLI)
- Gotchas : devil's advocate obligatoire mentionné
- Zéro mention de "obsidian-cli" dans tout le fichier

**Test 5.2 — Zéro CLI dans le projet**
Lance : grep -r "obsidian-cli.sh" .claude/ --include="*.md" --include="*.py"
Le résultat DOIT être vide. Si des fichiers restent, liste-les.

**Test 5.3 — Rule forge-brain-proactive**
Lis .claude/rules/forge-brain-proactive.md. Confirme : MCP OBLIGATOIRE, pas de CLI.

---

### BLOC 6 — Skills + Agents cohérence

**Test 6.1 — forge-brain skill**
Lis .claude/skills/forge-brain/SKILL.md (30 premières lignes). Confirme : MCP en premier, pas de CLI.

**Test 6.2 — Agent devils-advocate**
Lis .claude/agents/devils-advocate.md. Confirme : utilise forge-brain:search_brain, PAS obsidian-cli.

**Test 6.3 — Agent skill-creator**
Lis .claude/agents/skill-creator.md (30 premières lignes). Confirme : skills: contient forge-brain (PAS obsidian-cli).

---

### BLOC 7 — /done (métacognition)

**Test 7.1 — /done fonctionne**
Lance /done. Confirme :
- Extraction (décisions, faits, préférences — même si peu de contenu dans cette session de test)
- Context Note (0-Inbox/context-actuel.md) est réécrite
- Rapport structuré affiché

---

## Résumé final

Affiche un tableau avec les 20 tests et leur statut :

| Test | Description | Statut |
|------|------------|--------|
| 1.1 | vault_stats | OK/FAIL |
| 1.2 | search_brain | OK/FAIL |
| ... | ... | ... |
| 7.1 | /done | OK/FAIL |

Score : X/20 tests passés.
Si score < 20 : liste les FAIL avec la cause probable.
```
