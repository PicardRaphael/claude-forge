---
name: anthropic-skills-plugin-installed
description: Plugin anthropic-agent-skills installé dans claude-forge. 16 skills officielles disponibles (pdf, skill-creator, mcp-builder, claude-api, etc.). Les utiliser comme référence ou complément.
type: reference
---

## Plugin : anthropic-agent-skills (document-skills)

Installé dans le projet. 16 skills disponibles :

### Utiles pour claude-forge (référence + usage)

| Skill | Quand l'utiliser |
|-------|-----------------|
| **pdf** | Lire/traiter des PDF (complete-guide.pdf, docs projet) |
| **skill-creator** | Optimiser les descriptions de skills (boucle eval, run_loop.py) |
| **mcp-builder** | Guide MCP à jour spec 2026 (complémente plugin-dev:mcp-integration) |
| **claude-api** | Référence API Anthropic à jour (4.6 deprecations) |
| **doc-coauthoring** | Écriture collaborative de specs/docs (subagent fresh-eyes review) |
| **web-artifacts-builder** | Générer des dashboards/rapports HTML interactifs |
| **webapp-testing** | Tests Playwright pour apps web |

### Disponibles mais peu utilisées pour forge

| Skill | Usage |
|-------|-------|
| docx | Créer/éditer des Word |
| xlsx | Créer/éditer des Excel |
| pptx | Créer/éditer des PowerPoint |
| frontend-design | Design frontend distinctif (anti "AI slop") |
| brand-guidelines | Identité visuelle Anthropic |
| algorithmic-art | Art génératif P5.js |
| canvas-design | Art statique PNG/PDF |
| theme-factory | 10 thèmes visuels prédéfinis |
| slack-gif-creator | GIFs animés pour Slack |
| internal-comms | Communications internes entreprise |

### Comment les utiliser

- Invocables via `/pdf`, `/skill-creator`, `/mcp-builder`, etc.
- Ou Claude les charge automatiquement selon la description
- Peuvent servir de modèles de structure (references/, scripts/, assets/)
