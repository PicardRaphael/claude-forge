---
titre: "Limite connue MCP forge-brain — pas de lock inter-écritures (race théorique)"
resume: "Le serveur MCP forge-brain ne sérialise pas les écritures concurrentes : race théorique sur deux écritures simultanées sur la même note. Non codé car jamais déclenché (usage solo, écritures séquentielles), géré par discipline. À coder seulement si passage en multi-agent parallèle réel écrivant le vault."
aliases:
  - "limite lock MCP forge-brain"
  - "race condition écritures vault"
  - "pas de lock inter-écritures MCP"
  - "MCP write concurrency limit"
  - "vault write race theorique"
  - "chantier 5 limite 3"
type: technique
domaine: claude-code
derniere-maj: 2026-06-07
auteur: claude
tags:
  - "#type/technique"
  - "#domaine/claude-code"
---

## Symptôme

Le serveur MCP forge-brain (FastMCP HTTP, port 8091) n'a **aucun verrou** sérialisant les écritures concurrentes. Deux opérations d'écriture quasi simultanées sur la **même note** (ex. `update_property` + `append_note`, ou deux `update_property`) pourraient en théorie se chevaucher : la seconde lit l'état disque avant que la première ait écrit, puis écrase → perte de la première écriture (last-write-wins silencieux).

## Pourquoi non codé (chantier 5)

**Race jamais déclenchée en pratique.** L'usage est **solo** (une seule session principale Claude Code écrit le vault à la fois) et les écritures sont **séquentielles** (un tool MCP par tour, attendu avant le suivant). La fenêtre de course n'existe pas dans le workflow réel. Coder un lock (fichier, mutex, file d'attente) ajouterait de la surface et de la latence pour un problème qui **n'arrive pas** — exactement l'anti-pattern « fix pour un problème théorique » écarté au chantier 4. Géré par **discipline** : ne pas lancer deux écritures vault concurrentes sur la même note.

## Déclencheur qui justifierait de coder

Passage à un **usage multi-agent parallèle réel** où plusieurs agents/sessions écrivent le vault simultanément (ex. workflow fan-out avec plusieurs sous-agents en `create_note`/`update_property` concurrents sur des notes potentiellement identiques). À ce moment : sérialiser les écritures (lock par chemin de note, ou file d'attente côté serveur). Tant que l'écriture vault reste le fait de la session principale seule, inutile.

## Liens

- [[mcp-vault-llm-design]] — doctrine et matrice des outils MCP forge-brain
- [[architecture-cerveau-obsidian-mcp]] — architecture du serveur (FastMCP HTTP + watcher)
- [[erreur-mcp-yaml-dump-corruption]] — autre limite MCP, celle-ci RÉSOLUE (écriture array-safe)
