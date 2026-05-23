# Audit Vault — Thème : Patterns + Context Engineering + Stacks

> **Lire d'abord** : `output/audit-vault-thematique/00-TEMPLATE-COMMUN.md`
>
> **Méthode validée à appliquer impérativement** (cf audit Claude Code 23 mai 2026, 95 claims auditées, 22 erreurs corrigées) :
> 1. Lecture parallèle des N notes via `mcp__forge-brain__read_note` SANS max_lines (session principale, pas sub-agents)
> 2. Inventaire claims dédupliqué → **checkpoint write `A-inventaire-claims.md` AVANT lancer phase B**
> 3. **Sub-agents parallèles par CLUSTER thématique** (5-7 clusters, PAS par note) avec brief structuré : claim verbatim + URLs candidates + format imposé
> 4. **Self-verify FAUX fort impact AVANT phase D** : refetch direct WebFetch les fondations doctrinales avant réécriture
> 5. **Distinguer Type 1 (citation/source fausse, principe juste) / Type 2 (chiffre inventé) / Type 3 (doctrine fausse au fond)** dans plan correction
> 6. **Hiérarchie sources** (thème mixte — Anthropic forte sur context engineering Claude, mais patterns plus larges) :
>    - **Sources primaires** (les meilleurs du domaine, single source acceptable) : **Andrej Karpathy (LLM Wiki, prompt as program)**, **Boris Cherny (Claude Code compounding)**, **Erik Schluntz (Vibe Coding, leaf nodes)**, **Thariq Shihipar (compute allocators)**, **Birgitta Böckeler (Thoughtworks, harness)**, **Martin Fowler (Guides+Sensors)**, **Mitchell Hashimoto (harness engineering)**, **Addy Osmani (harness)**, **Simon Willison (LLM patterns)**, **Tobi Lütke (qmd)**
>    - **Anthropic docs context engineering / memory / compaction** = single source canonique (verbatim docs)
>    - **Papers académiques** sur context windows, memory architectures = single source acceptable
>    - **Autres sources** (blogs, Medium, vidéos tierces) = 4+ sources convergentes obligatoire
> 7. Validation Raphael par vague (Type 2 safe → Type 1 source → Type 3 réécriture)
> 8. advisor() AVANT vague 3 ET AVANT rapport final
>
> **⚠️ Risque spécifique ce thème** : patterns "context engineering" récents (memory, compaction, context windows) évoluent vite — vérifier dates de validité contre features Anthropic actuelles. Pattern Karpathy LLM Wiki + pattern Boris compounding = sources canoniques à recroiser.
>
> **Mémoire forge à consulter avant lancer** : `feedback_audit_thematique_methode`, `feedback_anthropic_single_source`, `feedback_regle_scope_pas_universelle`, `Knowledge/erreurs/erreur-22-claims-fausses-vault-claude-code-2026-05-23`

## Navigation vault — où lire selon le cas

| Si tu cherches... | Lire EN ENTIER via `mcp__forge-brain__read_note` SANS max_lines |
|-------------------|------------------------------------------------------------------|
| Méthode d'audit thématique générale | `[[methode-analyser-repo]]` (section ORDRE CANONIQUE A→B→C→D→E) |
| Pattern Karpathy LLM Wiki (3-layers, index.md, log.md, qmd) | `[[pattern-vault-llm-karpathy]]` |
| Compounding error-driven (Boris) | `[[comment-ecrire-claudemd]]` + `[[workflow-claude-code-optimal]]` |
| Context engineering Claude (memory, compaction, context windows) | `[[Context Management]]` + docs Anthropic features |
| Harness engineering (Agent = Model + Harness) | `[[harness-engineering]]` + `[[comment-creer-agent]]` |
| Patterns vault (architecture-cerveau-obsidian-mcp, fts5-aliases-vs-embeddings) | Notes `04-Techniques/patterns/*` |
| Routines higher-order (Boris) | `[[workflow-claude-code-optimal]]` |
| Compute allocator mindset (Thariq) | `[[mcp-vs-skills-doctrine]]` + `[[workflow-claude-code-optimal]]` |
| Lethal trifecta + Swiss cheese defense | `[[mcp-vs-skills-doctrine]]` section "Anti-pattern transversal" |

**N'oublie pas de regarder aussi** :
- `05-Leaders/claude-code/*` (Boris, Erik, Thariq, Cat Wu) et `05-Leaders/agents/*` (Karpathy, Fowler, Hashimoto)
- `Knowledge/erreurs/*` pour pièges patterns
- `01-Claude/Code/features/*` pour features context (Dreaming, Memory Managed Agents)

## Scope

**Dossiers** : `04-Techniques/patterns/` + `04-Techniques/context-engineering/` + `04-Techniques/stacks/`

**Notes à auditer (~22)** :

`04-Techniques/patterns/` :
1. `LLM Wiki`
2. `Silent Assumptions`
3. `architecture-cerveau-obsidian-mcp`
4. `audit-claude-folder-pattern`
5. `codebase-maps-pattern`
6. `config-guardian-pattern`
7. `mcp-paths-relatifs-portabilite`
8. `pattern-behavioral-dispatch-test`
9. `pattern-figma-mcp-claude-code`
10. `pattern-fts5-aliases-vs-embeddings`
11. `pattern-github-spec-kit`
12. `pattern-gsd-framework`
13. `pattern-sdd-triangle`
14. `pattern-spec-driven-development`
15. `pattern-spec-skill-deployment`
16. `pattern-vault-query-guard`
17. `running-implementation-notes`

`04-Techniques/context-engineering/` :
18. `Context Engineering`
19. `Context Management`

`04-Techniques/stacks/` :
20. `stack-python-ia`
21. `stack-typescript-ia`

## Hiérarchie experts (priorité ce thème)

### Liste actuelle forge

**Context engineering** (P1) :
- Andrej Karpathy (LLM Wiki, Software 3.0, context management)
- Anthropic team (Memory, Compaction features Claude Code)
- Thariq Shihipar (compute allocator)
- Hashimoto (AGENTS.md compounding)

**Patterns / spec-driven development** (P2) :
- Tobi Lütke (Shopify CEO, qmd tooling, spec-driven)
- GitHub Spec Kit team
- Boris Cherny (Plan Mode, /spec)
- Erik Schluntz (leaf nodes, verifiable checkpoints)

**Software architecture patterns** (P3) :
- Martin Fowler (patterns reconnu)
- Eric Evans (DDD)
- Vaughn Vernon

**Stacks IA** :
- Communauté Python AI (HF, LangChain, LlamaIndex)
- Communauté TypeScript AI (Vercel AI SDK, LangChain.js)

### Étape 0 — Valider/étendre

WebSearch : "context engineering 2026", "spec-driven development experts", "AGENTS.md pattern authors", "Karpathy LLM Wiki", "Tobi Lutke spec qmd", "GitHub Spec Kit creators".

## Sources spécifiques

### Context Engineering
- Karpathy gist LLM Wiki (canonical)
- karpathy tweets / talks
- Anthropic Claude Code Memory + Compaction docs
- Lenny's Newsletter posts sur context

### Spec-driven development
- Tobi Lütke qmd / spec tooling
- GitHub Spec Kit repo
- pattern-spec-driven-development referenced sources
- pattern-sdd-triangle / pattern-gsd-framework — sources originales

### Patterns spécifiques
- pattern-figma-mcp-claude-code — vérifier MCP Figma docs
- pattern-fts5-aliases-vs-embeddings — décision techno forge ou pattern général ?
- audit-claude-folder-pattern — Anthropic ou forge ?
- codebase-maps-pattern — source ? (sourcegraph ? aider ?)

### Stacks
- huggingface.co (Python AI stack)
- vercel.com/ai (Vercel AI SDK)
- langchain.com python vs js
- platform.openai.com SDKs

### Vidéos YouTube
- Karpathy YC AI Startup School "Software 3.0" (context, memory, compaction)
- Tobi Lutke spec talks
- Anthropic Memory + Compaction walkthroughs

## Claims à vérifier (priorité)

### Patterns forge custom
- `architecture-cerveau-obsidian-mcp` — pattern forge unique ou inspiré ?
- `pattern-vault-query-guard` — source ?
- `pattern-behavioral-dispatch-test` — source ?
- `running-implementation-notes` — Thariq ou autre ?

### Spec-driven
- pattern-sdd-triangle — vérifier sources originales
- pattern-gsd-framework — Getting Stuff Done framework, qui ?
- pattern-spec-driven-development — convergence experts ?
- pattern-github-spec-kit — vérifier repo GitHub officiel
- pattern-spec-skill-deployment — pattern forge ou général ?

### Context Engineering
- Notes citent souvent Anthropic features → vérifier docs.claude.com
- Karpathy LLM Wiki → vérifier gist + tweets convergent

### Stacks IA
- Recommandations Python : huggingface, langchain, llamaindex — convergence ?
- Recommandations TypeScript : Vercel AI SDK 2026 état ?

### Silent Assumptions
- Pattern Karpathy ? Anthropic ? Source ?

## Étape F — Propagation

Si modifs :

**Forge** :
- Skill `obsidian-markdown`, `forge-brain` (architecture vault)
- MCP forge-brain (utilise FTS5 aliases pattern)
- Rules sur patterns (running-implementation-notes utilisée dans ia_back)

**Repos applicatifs** :
- ia_back : utilise running-implementation-notes (docs/implementation-notes/)
- ia_back : spec-brief-boundary-guard implémente spec-driven pattern
- neoteem-brain : architecture vault MCP

**Backlinks** :
- Notes patterns sont **très référencées** ailleurs (impact propagation important)

## Output

`output/audit-vault-thematique/06-patterns-context/`

---

**Commence par étape 0. advisor() aux transitions.**
