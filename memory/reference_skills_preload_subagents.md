---
name: skills-preload-subagents
description: "skills: frontmatter d'un agent PROJET = préchargement du CONTENU COMPLET des skills dans son contexte au démarrage (doc officielle 9 juin 2026). Ne PAS lister Skill dans tools pour ça. references/ non préchargés"
metadata:
  type: reference
---

# skills: frontmatter agent = préchargement RÉEL (doc officielle)

Doc officielle sub-agents (code.claude.com/docs/en/sub-agents, vérifiée 9 juin 2026) :

- **`skills:` d'un agent précharge le CONTENU COMPLET** de chaque skill listée dans le contexte du sub-agent au démarrage — « The full skill content is injected, not just the description ».
- **« To preload Skills into context, use the `skills` field rather than listing `Skill` here »** (champ tools) — l'outil `Skill` dans tools n'est utile que si l'agent doit invoquer d'AUTRES skills à la demande.
- Les **`references/` ne sont PAS préchargés** — seuls les SKILL.md. Pointer les references/ in-body reste nécessaire.
- Skills avec `disable-model-invocation: true` non préchargeables ; skill manquante = warning debug log, skip silencieux.
- Sens inverse : `context: fork` + `agent:` dans une SKILL = la skill s'exécute DANS un subagent.

## Périmètre de validité — ne pas sur-généraliser

Ceci vaut pour les **agents project-scope du repo courant**. Les limitations forge documentées restent vraies dans LEURS contextes : Agent Teams teammates (skills frontmatter ignorées) et agents user-scope invoqués cross-repo (skills non résolues) — cf [[pattern-mcp-brief-then-direct]]. Le MCP d'un `tools:`/`allowed-tools:` de sub-agent reste décoratif (serveur non connecté).

**Why:** Audit neoteem-back-ts 9 juin 2026 : les agents du repo disaient in-body « les skills ne se déclenchent pas ici — lis leurs SKILL.md » → double chargement (contenu déjà injecté + relecture). Corrigé : « skills préchargées (frontmatter) — applique-les ; lire seulement references/ ».

**How to apply:** Agent project-scope avec `skills:` → body dit « préchargées, applique » + pointe uniquement les references/ non préchargés. Ne pas ajouter `Skill` aux tools sauf besoin d'invoquer d'autres skills.
