---
name: plugins-officiels-anthropic-marketplace
description: Marketplace anthropics/claude-plugins-official compte 203 plugins (mai 2026). Doctrine forge = on absorbe pas dans skills forge — enrichissement canonique vault ou skip
metadata: 
  node_type: memory
  type: reference
  originSessionId: e91e446c-e32c-4517-ab41-e1e4c5555314
---

# Plugins officiels Anthropic — marketplace `claude-plugins-official`

**203 plugins** au 26 mai 2026 (marketplace.json). 11 analysés en profondeur lors de la veille 26 mai.

## Verdict pattern (à reconduire pour futures veilles)

- **ADAPT** = technique réutilisable manquante → enrichir canonique vault forge (PAS de nouvelle skill forge)
- **REFERENCE** = produit utile situationnellement → note vault, pas de skill
- **SKIP** = stack non-match OU anti-pattern doctrinal OU caveat bloquant

## 11 plugins analysés 26 mai 2026

| Plugin | Verdict | Raison |
|--------|---------|--------|
| skill-creator | ADAPT | Eval A/B pattern (gap mesurable vs outcomes-grader) |
| code-review | ADAPT | Confidence scoring 0-100 (emprunté à da-blocking-arbitrage) |
| agent-sdk-dev | REFERENCE | Si construction app Agent SDK custom futur |
| mcp-server-dev | REFERENCE | Forge a déjà forge-brain MCP fonctionnel |
| pydantic-ai | REFERENCE | Watch-list si neo_ia introduit Pydantic AI |
| hookify | SKIP | Workflow hooks violent doctrine 22 mai |
| remember | SKIP | Exige désactiver auto-compact CC = bloquant |
| atomic-agents | SKIP | Framework concurrent LangGraph (neo_ia stack) |
| sourcegraph | SKIP | Pas d'instance Sourcegraph Neoteem |
| data-engineering | SKIP | Pas d'Airflow/dbt chez Neoteem |
| forge-skills | SKIP | Atlassian Forge ≠ claude-forge (confusion de nom) |

## Discriminateurs pour future veille

1. **Forge a déjà absorbé l'équivalent ?** → doctrine [[comparaison-skill-anthropic-claude-code-setup]]
2. **Technique vs produit ?** → technique = enrichir canonique. produit = note référence ou skip
3. **Stack-match neo_ia/ia_back ?** → vérifier pyproject.toml/package.json empiriquement
4. **Conflit doctrinal ?** → notamment doctrine 22 mai (hooks workflow = NON)

## Notes vault canoniques

- [[plugins-officiels-veille-2026-05-26]] — synthèse complète 11 plugins
- [[anti-pattern-hookify-workflow-hooks]] — anti-pattern doctrinal documenté
- [[eval-pattern-anthropic-skill-creator]] — technique eval A/B Anthropic
- [[analyse-plugin-claude-code-setup]] — analyse claude-code-setup (avril)
- [[comparaison-skill-anthropic-claude-code-setup]] — doctrine "on absorbe pas"
