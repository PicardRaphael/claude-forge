---
name: audit-thematique-06-patterns-findings-cles
description: "Findings clés audit thème 06 patterns/context/stacks 23 mai 2026 — fondations canoniques confirmées, 4 attributions corrigées, méthode validée"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 8fa91757-f7b7-4aca-8e12-6bce6d8e70c2
---

Audit thème 06 vault forge-brain (21 notes, ~92 claims, 28 corrections) — findings à retenir pour audits futurs et propositions Jarvis.

## Fondations canoniques confirmées (utiliser librement)

- **Karpathy gist LLM Wiki** (`gist.github.com/karpathy/442a6bf555914893e9891c11519de94f`, 4 avril 2026, 5K+ stars) :
  - Verbatim : *"Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."* (point-virgules)
  - "~100 sources, ~hundreds of pages" (PAS "100 articles, 400K mots")
  - **Pas de chiffre 70x RAG dans le gist** — c'est de MindStudio blog tiers
- **Anthropic blog 15 mai 2026 "Claude Code at Scale"** (`claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start`) : verbatim codebase-maps "lightweight markdown file at the repo root..."
- **Tweet Thariq Running Implementation Notes — 19 mai 2026** (pas 18 mai). 4 sections finales : Design decisions / Deviations / Tradeoffs / Open questions. Métriques réelles : 951 likes / 44 RT (PAS 758k vues)
- **Leak Claude Code 31 mars 2026** : v2.1.88 npm `cli.js.map` 59.8 MB / 512K+ lignes / 1900 TypeScript files — découvreur Chaofan Shou (Solayer Labs)

## Attributions corrigées (ne plus se tromper)

- **3 niveaux SDD (spec-first / spec-anchored / spec-as-source)** = **Birgitta Böckeler (Thoughtworks/martinfowler.com)** — PAS Drew Breunig, PAS Heeki Park (Park utilise les termes en référençant Böckeler)
- **Drew Breunig SDD Triangle** = Spec/Tests/Code (3 sommets feedback loop) + outil Plumb pre-commit (`github.com/dbreunig/plumb`)
- **4 piliers Context Engineering (Composition/Ranking/Optimization/Orchestration)** = formalisation communauté (keyvalue.systems + davidkimai/Context-Engineering "inspired by Karpathy") — PAS Karpathy direct (lui a juste tweeté "+1 for context engineering")
- **Karpathy 4 anti-patterns** = silent assumptions, overcomplexity, scope creep, vague execution — listés **sans hiérarchie** ("#1" = lecture interprétative forge)
- **"Document & Clear" pattern** = communauté / Manus AI ("Markdown is my working memory on disk") / sshh.io — PAS Boris
- **`/compact` seuils** = sous 40-60% (Thariq via howborisusesclaudecode.com), auto-fire ~83.5%. PAS 70%.

## Frameworks SDD chiffres mai 2026

- **GitHub Spec Kit** (`github/spec-kit`) : ~105K stars (croissance rapide depuis 93K), 7 fichiers per spec dir (pas 8), 6 commandes core + 3 optionnelles (= 9), 40+ extensions community (pas 80+)
- **GSD** (`gsd-build/get-shit-done`) : ~59K stars, créé par Lex Christopherson (glittercowboy, TACHES org, music producer Costa Rica), 29 Skills + 12 Custom Agents, 200K tokens contexte frais par subagent, plans ~50% contexte frais
- **BMAD** (`bmad-code-org/BMAD-METHOD`) : 46,700+ stars v6.6.0 (29 avr 2026), **21 agents spécialisés** (pas 12+), 50+ workflows, Scale-Adaptive Intelligence
- **Plugin feature-dev Anthropic** : auteur Sid Bidasaria, 7 phases, 3 agents nommés (code-explorer / code-architect / code-reviewer), 89K+ installs vérifiés

## Skills Figma officielles (vérifié help.figma.com)

**8 skills réelles** :
1. figma-use
2. figma-use-figjam
3. figma-use-slides
4. figma-code-connect
5. figma-create-new-file
6. figma-generate-diagram
7. figma-generate-library
8. figma-generate-design

**Noms inventés à éviter** : figma-implement-design, figma-create-design-system-rules, figma-code-connect-components.

## Claude Code MCP limits

- Warning à 10k tokens output, max default **25k tokens** (`MAX_MCP_OUTPUT_TOKENS` env var override possible, `anthropic/maxResultSizeChars` annotation pour texte)
- Rate limits Figma MCP : Starter/View/Collab 6 calls/mois (écriture exemptée), Org Dev/Full 200/jour, Enterprise Dev/Full 600/jour

## Stacks IA chiffres (mai 2026)

- **uv 10-100x plus rapide que pip** (Astral BENCHMARKS officiel, 8-10x sans cache, 80-115x warm)
- **DSPy +10-40% qualité** (arXiv 2310.03714 paper original)
- **MCP 97M downloads SDK/mois** (mars 2026, Digital Applied)
- **Pydantic AI 25+ providers** (pas 20+)
- **Prompt caching Claude -90%** (cache read 0.1× base)
- **Batch API -50%** OpenAI/Anthropic/Google
- **Reranking +15-25% précision** (T2-RAGBench, FinDER)
- **Modal cold start ~1s container, GPU warm secs→mins** (pas <1s GPU)
- **OpenAI strict + parallel tool calls** : fix annoncé (compatibilité restaurée snapshots récents)
- **Mastra** = Kepler Software (Sam Bhagwat, Abhi Aiyer, Shane Thomas, ex-Gatsby, YC W25)

## How to use

- Avant de citer un de ces chiffres/verbatim dans une réponse à Raphael : vérifier que la source est toujours valide (>7 jours = re-vérifier)
- Les claims listés ci-dessus sont la **source canonique** pour le thème patterns/context/stacks — privilégier sur les autres mentions dans le vault si conflit
