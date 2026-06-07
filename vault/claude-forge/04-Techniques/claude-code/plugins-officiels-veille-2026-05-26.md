---
titre: "Veille plugins officiels Anthropic — 26 mai 2026 (11 plugins analysés)"
resume: "Analyse comparative de 11 plugins officiels (hookify, skill-creator, agent-sdk-dev, code-review, mcp-server-dev, remember, atomic-agents, pydantic-ai, sourcegraph, data-engineering, forge-skills) vs forge/neo_ia/ia_back. 2 ADAPT (eval pattern + confidence scoring), 4 REFERENCE, 5 SKIP."
aliases:
  - "veille plugins officiels 2026-05-26"
  - "plugins anthropic 11 analyses"
  - "hookify skill-creator code-review analyse"
  - "marketplace claude-plugins-official veille"
  - "plugins officiels vs forge"
derniere-maj: 2026-05-26
auteur: claude
type: veille
sources:
  - "https://github.com/anthropics/claude-plugins-official (203 plugins total marketplace.json)"
  - "WebFetch + gh CLI 26 mai 2026"
tags:
  - "#type/news"
  - "#domaine/claude-code"
  - "#meta"
---

# Veille plugins officiels Anthropic — 26 mai 2026

Demande Raphael : analyser 11 plugins officiels et juger pertinence vs forge / neo_ia / ia_back. Marketplace `anthropics/claude-plugins-official` compte 203 plugins au total au 26 mai 2026.

## Verdict global

- **ADAPT (2)** : skill-creator (eval pattern), code-review (confidence scoring)
- **REFERENCE (3)** : agent-sdk-dev, mcp-server-dev, pydantic-ai (watch-list)
- **SKIP (6)** : hookify, remember, atomic-agents, sourcegraph, data-engineering, forge-skills

## Tableau détaillé

| Plugin | Ce qu'il fait | Équivalent forge | Verdict | Action |
|--------|---------------|------------------|---------|--------|
| **hookify** | Hooks via markdown YAML (event/pattern/action) — bash, file, stop, prompt | `hook-creator` + `cc-hooks-ref` (29 events doctrine 22 mai) | ❌ SKIP + flag doctrinal | `event: stop` + transcript conditions = workflow hook = viole doctrine 22 mai. Voir [[anti-pattern-hookify-workflow-hooks]] |
| **skill-creator** Anthropic | Évals A/B `with_skill/baseline` + `run_loop.py` + benchmark viewer HTML + 3 agents (grader/comparator/analyzer) | `skill-creator` agent + `skill-evolve` + `outcomes-grader`/`outcomes-test` | ✅ ADAPT (gap mesurable) | Enrichir [[comment-creer-skill]] + note dédiée [[eval-pattern-anthropic-skill-creator]] |
| **agent-sdk-dev** | `/new-sdk-app` Python/TS Agent SDK scaffolding + 2 verifiers (py/ts) | Aucun (forge ne fait pas du SDK app dev) | ⚠️ REFERENCE | Note référence si construction app Agent SDK custom |
| **code-review** Boris | Pipeline 7 étapes, 4 agents //, **confidence scoring 0-100 + seuil 80** filtre faux positifs, post GitHub | `reviewer.md` neo_ia/ia_back + `da-blocking-arbitrage` + `auditor-empirical-verify` | ✅ ADAPT (1 idée à voler) | Enrichir la skill `da-blocking-arbitrage` avec scoring numérique |
| **mcp-server-dev** | 3 skills build-mcp-server / build-mcp-app / build-mcpb (auth flows, widgets, packaging) | Forge-brain MCP fonctionnel port 8091 | ⚠️ REFERENCE | Note référence si nouveau MCP futur |
| **remember** | Tiered memory now.md → today → recent → archive via Haiku compression | MEMORY.md natif + 200+ feedback files + vault forge-brain | ❌ SKIP — caveat bloquant | **Exige désactiver auto-compact CC** = casse workflow. Vault + MEMORY.md font mieux structurellement |
| **atomic-agents** | Framework Python concurrent LangGraph + skills framework/new-app + agents explorer/reviewer | neo_ia = LangGraph 1.0, pas atomic-agents | ❌ SKIP | Framework concurrent, ne switch pas la stack pour un plugin |
| **pydantic-ai** | Patterns agents/tools/structured output/streaming Pydantic AI | neo_ia = Pydantic 2.10 ✅ mais LangGraph (pas Pydantic AI) | ⚠️ REFERENCE watch-list | Watch si neo_ia introduit Pydantic AI futur |
| **sourcegraph** | MCP search code cross-repos via instance Sourcegraph | Grep/Glob local | ❌ SKIP | Neoteem n'a pas instance Sourcegraph. Reconsidérer si setup change |
| **data-engineering** (astronomer) | Airflow DAGs, dbt, MCP airflow, warehouse exploration | Aucun (pas d'Airflow chez Neoteem) | ❌ SKIP | Stack non match (postgres.js + LangGraph, pas Airflow/dbt) |
| **forge-skills** (Atlassian) | Apps Atlassian Forge (Jira/Confluence), Teamwork Graph, ADS lookup | Aucun (rien à voir avec ta forge — c'est Atlassian Forge) | ❌ SKIP | Confusion de nom : ce n'est pas claude-forge |

## Discriminateurs appliqués (advisor 26 mai)

1. **Forge a-t-il déjà absorbé l'équivalent ?** → Doctrine [[comparaison-skill-anthropic-claude-code-setup]] : on absorbe pas dans nouvelle skill forge
2. **Technique vs produit ?** → Technique → enrichir canonique. Produit → référence ou skip
3. **Stack-match ?** → neo_ia LangGraph (pas atomic-agents/Pydantic AI), ia_back postgres.js TS (pas Python deps)
4. **Conflit doctrinal ?** → hookify workflow hooks vs doctrine 22 mai

## Découvertes non-évidentes (advisor)

- **skill-creator vrai gap forge** : `evals.json` + `run_loop.py` + A/B `with_skill/baseline` + viewer HTML = infra mesure que forge n'a pas. `outcomes-grader` + `outcomes-test` ≠ benchmark itératif
- **code-review** : confidence scoring 0-100 + seuil 80 = pattern empruntable seul, pas tout le pipeline
- **remember caveat** : auto-compact CC doit être désactivé = bloquant
- **mcp-server-dev** : forge a déjà forge-brain MCP, donc utile en référence pas en skill
- **forge-skills naming confusion** : Atlassian Forge ≠ claude-forge perso

## Actions exécutées 26 mai

1. ✅ Note synthèse (ce fichier)
2. ✅ Note anti-pattern [[anti-pattern-hookify-workflow-hooks]]
3. ✅ Note technique [[eval-pattern-anthropic-skill-creator]]
4. ✅ Enrichissement [[comment-creer-skill]] section eval pattern
5. ✅ Enrichissement de la skill `da-blocking-arbitrage` confidence scoring 0-100
6. ✅ Update [[analyse-plugin-claude-code-setup]] + [[comparaison-skill-anthropic-claude-code-setup]]

## Wikilinks

- [[comparaison-skill-anthropic-claude-code-setup]] — pattern précédent (claude-code-setup 23 mai)
- [[analyse-plugin-claude-code-setup]] — analyse 26 avril
- [[anti-pattern-hookify-workflow-hooks]] — anti-pattern doctrinal
- [[eval-pattern-anthropic-skill-creator]] — technique eval A/B
- [[comment-creer-skill]] — canonique enrichie
- skill `da-blocking-arbitrage` — skill enrichie
- [[raisonnement-22mai-doctrine-vs-enforcement]] — doctrine hooks lint/sécu/scope only
- [[methode-analyser-repo]] — méthode 6 étapes appliquée
- rule `cross-repo-propagation` — propagation enrichissements neo_ia/ia_back

## Sources

- `anthropics/claude-plugins-official` marketplace.json (203 plugins)
- 11 WebFetch + gh CLI 26 mai 2026
- Advisor session forge 26 mai


## Méthode reproductible

La méthode 6 étapes appliquée cette session est capitalisée dans [[methode-veille-plugins-marketplace]] — pattern réutilisable pour la prochaine veille (marketplace continue de grossir : 203 → estimé 300+ d'ici août 2026).
