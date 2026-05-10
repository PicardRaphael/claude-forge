---
titre: "Best Practices Claude Code — Synthese Leaders"
resume: "Recap consolide Boris, Erik Schluntz, Thariq, Cat Wu, Karpathy : planification, contexte, parallelisme, skills, effort, agentic engineering"
aliases:
  - "best practices CC"
  - "recap bonnes pratiques"
  - "boris erik thariq best practices"
  - "best practices claude code leaders"
  - "synthese leaders claude code"
  - "reference_boris_thariq_bestpractices"
domaine: claude-code
type: technique
derniere-maj: 2026-05-10
auteur: claude
sources:
  - "https://howborisusesclaudecode.com"
  - "https://youtube.com/watch?v=fHWFF_pnqDk"
  - "https://www.linkedin.com/pulse/lessons-from-building-claude-code-how-we-use-skills-thariq-shihipar-iclmc"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/agents"
---

## 1. Ne plus ecrire de code — devenir PM de Claude

**Erik Schluntz** + **Boris Cherny** : meme posture
- Tu ne codes plus, tu diriges Claude
- "Forget the code, focus on the product" (Erik)
- 100% du code ecrit par Claude (Boris : nov. 2025, Erik : fev. 2025)
- 22 000 lignes mergees en prod par Erik — 2 semaines compressees en 1 jour
- CC = 4% des commits GitHub publics (Boris, CNBC mai 2026)

## 2. Planifier AVANT de lancer

**Erik** : 15-20 min de planification par tache
- Explorer le codebase d'abord
- Creer un plan detaille
- Merger tout le contexte dans un seul prompt
- **"Leaf nodes"** : donner a Claude les features isolees, garder le controle sur le core/design system

**Boris** : Plan Mode → iterer → auto-accept → one-shot
- Fichier plan dans un .md, /clear, nouvelle session qui lit le plan
- "Give Claude a way to verify its output" = tip #1

## 3. Gestion du contexte = competence #1

**Boris** — les 3 pieges :
- `/clear` entre taches non liees — sessions "fourre-tout" = piege #1
- `/compact "garder le plan"` proactif a 70% — pas attendre l'auto-compact
- `/btw` pour questions sans polluer le contexte
- Deleguer la recherche aux subagents

**Pattern "Document & Clear"** :
1. Dump le plan dans un .md
2. /clear
3. Nouvelle session qui lit le .md

## 4. Paralleliser comme un "Fleet Commander"

**Boris** : 5 terminaux + 5-10 sessions cloud en parallele
- Chaque session dans son worktree git
- Ne code pas lui-meme, orchestre
- `/batch` pour centaines d'agents paralleles

**Pattern anti-crash agents** :
- Max 6-8 operations par agent
- Decouper par theme/repo/phase
- Paralleliser ce qui est independant
- Voir [[decoupe-agents-anti-crash]]

## 5. CLAUDE.md = concis et compounding

**Boris** + **Karpathy** :
- ~100 lignes max — "si je l'enleve, Claude fait des erreurs ?" sinon couper
- CLAUDE.md = advisory (~80% compliance). Hooks = deterministe (100%)
- Compounding : apres chaque erreur → ajouter au CLAUDE.md pour ne pas refaire
- Erreurs dans Auto Memory, pas dans CLAUDE.md

## 6. Skills = composabilite

**Thariq** :
- Dossiers avec scripts/assets, pas juste du markdown
- Section Gotchas = contenu le plus important (highest-signal)
- Progressive disclosure — pointer vers des fichiers, Claude lit a la demande
- Ne pas etre trop specifique — laisser de la flexibilite
- Prompt caching = architecture de base, pas une optimisation optionnelle

## 7. Effort et modeles

**Cat Wu** + **Boris** :
- Opus 4.7 = modele "delegation" — contexte complet upfront
- `effort: xhigh` = defaut Opus 4.7
- `effort: high` sur TOUS les sonnet — jamais medium
- Adaptive thinking = seul mode sur Opus 4.7 (plus de budget_tokens)
- "Step by step" desormais inutile voire contre-productif sur modeles frontier

## 8. La lecture de code va devenir un bottleneck

**Erik Schluntz** :
> "In a year or two, demanding to read every line of code will make you the bottleneck"

Analogie : LLM = compilateur. Comme on a arrete d'ecrire de l'assembly, on va arreter de lire chaque ligne.

## 9. Agentic Engineering

**Karpathy** (Sequoia AI Ascent, mai 2026) :
- "Vibe coding" c'est fini → "Agentic engineering"
- 80% de son code = AI-generated
- Software 3.0 : programmer par contexte, pas par instructions
- "Jagged intelligence" : l'IA excelle ou elle a des feedback loops, echoue sur l'ambigu
- 4 principes : Simplicity, Surgical changes, No Silent Assumptions, Verifiable Steps

## Liens

- [[Workflow Boris]]
- [[Erik Schluntz]]
- [[Boris Cherny]]
- [[Thariq Shihipar]]
- [[Andrej Karpathy]]
- [[agentic-engineering-karpathy]]
- [[decoupe-agents-anti-crash]]
- [[MOC-Techniques]]
