---
titre: "Intelligence de code (context engines + revue IA) — build-vs-buy juin 2026"
resume: "Paysage des outils qui font coder MIEUX les agents IA : context engines / repository intelligence (SocratiCode, CodeGraph, Serena, Augment) qui indexent le repo pour l'agent, + revue de code IA et gates qualité (CodeRabbit, SonarQube, Semgrep). Verdict : OSS local gagne sur l'indexation, buy sur la revue."
aliases:
  - "intelligence de code"
  - "context engine code agent"
  - "repository intelligence"
  - "SocratiCode CodeGraph Serena"
  - "revue de code IA"
  - "faire coder mieux Claude Code"
domaine: ia
type: technique
derniere-maj: 2026-06-17
auteur: claude
sources:
  - "https://github.com/giancarloerra/socraticode"
  - "https://github.com/colbymchenry/codegraph"
  - "https://www.augmentcode.com/product/context-engine-mcp"
  - "https://coderabbit.ai/pricing"
  - "https://github.com/semgrep/semgrep"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/agents"
---

## Description

Outils qui rendent un agent de code (Claude Code, Cursor, Copilot) **meilleur** — deux familles : (A) **context engines / repository intelligence** qui indexent le repo et donnent ce contexte à l'agent ; (B) **revue de code IA + gates qualité** qui vérifient le code produit (par humains ET agents). Légende : `[v]` = source primaire vérifiée (GitHub API/site officiel, 17 juin 2026) · `[r]` = rapporté/benchmark-vendor non reproductible.

> [!warning] Tous les benchmarks de cette catégorie sont éditeur
> « 61% moins de tokens », « +80% qualité », « 82% bug catch »… = mesurés par le vendeur sur ses repos/prompts, sans tiers indépendant. `[v]` confirme que le chiffre EST annoncé là, **pas qu'il soit vrai sur VOTRE repo**. Directionnel, pas garanti.

## A. Context engines / repository intelligence

Indexent code + dépendances + schémas pour que l'agent **raisonne sur la structure** au lieu de lire fichier par fichier (recherche hybride sémantique+BM25, graphes de dépendances, analyse d'impact « blast radius »). Branchés via **MCP**.

> [!tip] Le constat qui tranche le build-vs-buy
> Les deux plus gros acteurs sont **OSS, gratuits, locaux** — et peu connus : **CodeGraph** (50,5k★ `[v]`, MIT) et **GitNexus** (42,3k★ `[v]`). **Builder l'indexation soi-même = non-sens** (sujet commodifié par la communauté). Le « buy » payant (Augment, Tabnine) se justifie surtout pour le **cross-repo hébergé + gouvernance entreprise**.

| Outil | ⭐ `[v]` | Licence | MCP Claude Code | Verdict |
|---|---|---|---|---|
| **CodeGraph** (colbymchenry) | 50 560 | MIT | natif (SQLite pré-indexé, 8 agents) | **Leader OSS** — le plus simple à adopter, 100% local |
| **GitNexus** (abhigyanpatwari) | 42 324 | non-commercial ⚠️ | natif (16 outils + skills + hooks) | Intégration CC la plus profonde, mais licence non-commerciale |
| **Serena** (oraios) | 25 450 | MIT | natif | Navigation symbolique via Language Server (LSP), **pas RAG** — précis sur gros repos |
| **Repomix** (yamadashy) | 26 333 | MIT | MCP ou CLI | Packe le repo en 1 fichier AI-friendly (dump structuré, pas de graphe) |
| **gitingest** (coderamp-labs) | 14 915 | MIT | CLI/web | Extrait prompt-friendly d'un repo distant (one-shot) |
| **SocratiCode** (giancarloerra) | 2 976 | **AGPL-3.0** ⚠️ | natif | Le déclencheur de la recherche — solide mais 17× moins d'étoiles |

### SocratiCode en détail (l'outil que tu citais)
MCP server zero-config, indexe **localement** : recherche hybride RRF, graphes de dépendances 18+ langages, analyse d'impact symbole-niveau, call-flow, cross-project/branch, + artefacts schémas DB/API/infra, viewer HTML. Stack Qdrant+Ollama (Docker), 100% local → privacy/air-gap. Benchmark `[vendor]` : sur VS Code (2,45M LOC) avec Opus 4.6 = 61% moins de tokens, 84% moins d'appels, 37× plus rapide vs grep. Hôtes : Claude Code, Cursor, Copilot, Windsurf, Cline, Codex, Gemini CLI. Cloud en beta (SSO/SAML, pricing non public). **⚠️ AGPL-3.0** : OK en interne dev, à faire valider juridiquement si embarqué dans un produit distribué (Loji).

### Buy managé (context engine hébergé)
- **Augment Code** : Context Engine exposé en MCP (GA fév 2026), mode local (Auggie CLI) ou remote (cross-repo hébergé = **code egress**, à valider souveraineté FR). Benchmark `[vendor]` : Claude Code + Opus = +80% qualité. **100$/mois** flat (≤50 seats). Le « 70,6% SWE-bench » NON confirmé en source primaire.
- **Tabnine Enterprise Context Engine** (GA fév 2026) : modèle continu de l'archi, marche avec Claude Code/Cursor/Copilot, déploiement **air-gapped** possible (angle régulé/souveraineté). Pricing non public.
- **Sourcegraph Cody/Amp** : code graph sémantique cross-repo, dès 59$/user/mo — surdimensionné pour une PME aujourd'hui.

### Le contre-pied : pas d'index du tout
**Cline** assume publiquement : pas d'index, pas de RAG — exploration agentique fichier-par-fichier (suit les imports) en pariant sur les grandes fenêtres de contexte. Valide que **sur repo moyen + fenêtre Opus 1M, l'exploration native peut suffire** (cf [[codebase-maps-pattern]]). La faiblesse : les requêtes « je ne connais pas le nom » (le code dit `throttleMiddleware`, tu cherches « rate limiting ») — là où le sémantique gagne.

## B. Revue de code IA + gates qualité

Vérifient le code produit (humains ET agents). **Doctrine forge clé** : un fichier de règles (CLAUDE.md/.cursorrules) est **advisory** ; seul un **linter/CI gate déterministe** est non négociable pour contraindre la sortie d'un agent (cf [[raisonnement-22mai-doctrine-vs-enforcement]], [[erreur-advisory-rules-insuffisantes]]).

### Revue de code IA (PR review) — BUY gagne
| Outil | Pricing `[v]` | OSS | Distinctif |
|---|---|---|---|
| **CodeRabbit** (leader) | Pro 24$ / Pro+ 48$ /dev/mo | Non | Bundle LLM + 30+ linters/SAST, 4 plateformes, autofix |
| **GitHub Copilot review** | inclus Business 19$/seat | Non | Natif flux PR GitHub (bascule usage-based juin 2026) |
| **Graphite Agent** (sur Claude) | Starter 20$ / Team 40$ | Non | Agit (fix/merge), pas que commenter ; stacked-PR |
| **Qodo Merge / PR-Agent** | PR-Agent **OSS gratuit** ; Merge ~30$/u `[r]` | **Oui** (Apache 2.0, 11,6k★) | Seul vrai OSS, multi-modèle, self-host |
| **Greptile** | Pro 30$/seat (puis 1$/review) | Non | Indexe tout le repo en graphe → bugs cross-fichiers |
| **Cursor BugBot** | usage-based `[r]` | Non | Bugs-only (faible bruit), GitHub only |

Builder un reviewer LLM maison = réinventer prompt+indexation+intégration pour un résultat inférieur → **buy gagne**. Seul cas OSS : PR-Agent self-hosted si confidentialité forte.

### Gates qualité & sécu — OSS-first puis upgrade
- **Qualité** : **SonarQube Community** (gratuit, LGPL-3.0, 10,7k★ ; + AI Code Assurance qui détecte le code IA et renforce le quality-gate) · DeepSource · Codacy Guardrails (scan IDE temps réel via MCP, pré-commit).
- **Sécu (buy/OSS gagne le plus nettement)** : **Semgrep** (moteur OSS LGPL-2.1, 15,5k★, SAST) · **Socket** (malware supply-chain, irréplicable en maison) · **GitGuardian** (secrets, 550+ types) · Snyk (SCA+SAST). Ces angles dépendent de **threat-intelligence vivante** → impossible à coder en CI maison.

### Rendre les agents IA meilleurs (guardrails)
3 familles : (a) **test-gen auto-vérifiants** (Qodo Cover OSS mais figé depuis juin 2025 ; Early) → gate sur exécution+couverture · (b) **enforceurs de standards** ([[packmind-context-governance|Packmind]], ESLint-en-CI) → gate sur conventions · (c) **gates sécu/qualité** (Meta CodeShield/LlamaFirewall MIT, filtrage inference-time du code LLM). Principe unificateur : **déplacer le check de la prose advisory vers un gate exécutable** — exactement la doctrine forge.

## Synthèse build-vs-buy pour Neoteem

| Besoin | Reco |
|---|---|
| Agent code mieux sur 1 gros repo, gratuit, local, souverain | **CodeGraph** (MIT, MCP natif, 50k★) ou **Serena** (LSP). Zéro code egress |
| Idem + artefacts DB/API/infra + air-gap | **SocratiCode** OSS (⚠️ AGPL-3.0 si distribution produit) |
| Context engine managé cross-repo + tribal knowledge | Augment (100$/mo, egress) ou Tabnine ECE (air-gap) |
| Reviewer PR IA | **BUY** — Copilot review (si déjà GitHub) ou CodeRabbit ; ne pas builder |
| Gate déterministe qualité+sécu | **OSS-first** : SonarQube Community + Semgrep, upgrade payant ensuite |
| Supply-chain / secrets | **BUY** (impossible en maison) : Socket + GitGuardian (free ≤25 devs) |
| Builder l'indexation soi-même | **Non** — commodité, pas un moat |

> [!warning] Morts / pièges
> **Bloop** (archivé 2024) et **code-graph-rag-mcp** (archivé) — ne pas adopter. **GitNexus** = licence non-commerciale. **SocratiCode** = AGPL-3.0.

## Liens

- [[MOC-paysage-outils-ia-marche-2026]] — cartographie marché parente
- [[codebase-maps-pattern]] — le tier-0 sans index (carte markdown du repo)
- [[packmind-context-governance]] — gouvernance standards de code pour agents
- [[briques-produit-ia-build-vs-buy]] — même doctrine OSS-local-quand-pas-un-moat
- [[harness-engineering]] — agent = modèle + harness (le contexte compte autant que le modèle)
- [[MOC-Techniques]]
