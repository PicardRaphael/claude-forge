---
name: mcp-running-pas-connected-transport
description: "MCP 'running' = process vivant, PAS connecté. Vérifier le transport (stdio vs http)"
metadata:
  type: feedback
---

Quand un MCP affiche **"running"** mais ne répond pas : vérifier le **transport**. Un serveur
lancé via `command`/`args` (Claude attend du **stdio**) mais qui démarre en **HTTP** (port) est
"running" (process lancé) sans être **connecté** (Claude lui parle en stdio, lui écoute en HTTP).
Le vrai test = `claude mcp list` → **"Connected"**, pas "running".

**Why:** Session 1er juin 2026 — config `command`/`args` de Valéry pointait un serveur démarré
en streamable-http → "running" mais outils morts. Fix = aligner transport (ajout mode stdio au serveur).
**How to apply:** tout debug MCP qui semble "lancé mais inactif" → checker stdio vs http AVANT tout.
