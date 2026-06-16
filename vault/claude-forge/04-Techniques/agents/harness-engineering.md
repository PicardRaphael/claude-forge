---
titre: "Harness Engineering"
resume: "Discipline 2026 formalisee par Birgitta Bockeler (Thoughtworks, mars 2026) : tout ce qui entoure le modele LLM (state, tools, feedback loops, contraintes, orchestration). Reconnu 4e paradigme AI Engineering par TechTimes (13 mai 2026)"
aliases:
  - "harness engineering"
  - "agent harness"
  - "model harness"
  - "agentic harness"
  - "everything around the model"
  - "agent infrastructure"
domaine: technique
type: technique
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://martinfowler.com/articles/harness-engineering.html"
  - "https://www.techtimes.com/articles/313524/20260513/harness-engineering-rises-4th-paradigm-ai-engineering.htm"
tags:
  - "#type/technique"
  - "#domaine/agents"
---

## Description

Discipline formalisee par **Birgitta Bockeler** (Distinguished Engineer, Thoughtworks) dans son article hebergé sur martinfowler.com (mars 2026). Reconnue comme **4e paradigme de l'AI Engineering** par TechTimes (13 mai 2026), apres Prompt Engineering (2022-24) et Context Engineering (2025).

**Formule centrale (citee par Bockeler, attribuee a LangChain)** :

> Agent = Model + Harness

Le harness = tout ce qui **entoure** le modele et qui n'est pas le modele lui-meme.

> [!note] Audit 23 mai 2026
> Cette note a ete reattribuee a Bockeler (auteure reelle, single source primaire). Les versions anterieures citaient a tort Fowler / Addy Osmani / Simon Willison comme co-auteurs. Voir [[Knowledge/erreurs/agents-ia-22-claims-fausses-2026-05-23]].

## Composants du Harness

| Composant | Description |
|---|---|
| **State management** | Persistance de l'etat entre les appels (memoire, contexte) |
| **Tool execution** | Couche d'execution et validation des tool calls |
| **Feedback loops** | Signaux de succes/echec retournes au modele |
| **Enforceable constraints** | Contraintes deterministes (linters, guards, hooks) |
| **Context management** | Assemblage dynamique du contexte par tache |
| **Sub-agent orchestration** | Coordination d'agents specialises |

## Feedforward vs Feedback (verbatim Bockeler)

Distinction structurante :

| Type | Quand | Exemples |
|------|-------|----------|
| **Guides (feedforward controls)** | AVANT action — anticipation | CLAUDE.md, SKILL.md contraintes, architecture docs |
| **Sensors (feedback controls)** | APRES action — correction | Hooks exit 2, linters, tests, type checkers |

Bockeler verbatim : "Guides (feedforward controls)" / "Sensors (feedback controls)". **Feedforward > Feedback** en general — mieux vaut anticiper que corriger. Mais les deux sont necessaires.

## Computational vs Inferential (verbatim Bockeler)

> "Computational — deterministic and fast, run by the CPU"
> "Inferential — Semantic analysis, AI code review, 'LLM as judge'"

| | Computational | Inferential |
|---|---|---|
| Vitesse | ms-sec | sec-min |
| Fiabilite | Deterministe, 100% | Probabiliste, ~95% |
| Exemples | Linters, hooks, tests | AI code review, semantic analysis |
| Cout | CPU, quasi gratuit | GPU/API, cher |

**Priorite : Computational d'abord, Inferential en complement.**

## Ashby's Law of Requisite Variety (verbatim Bockeler)

> "A regulator must have at least as much variety as the system it governs"

Reduire la variete que l'agent doit gerer → reduire le scope → harness plus complet possible. 1 skill = 1 responsabilite.

## Insight cle : deterministe > suggestif

Un prompt disant "ne modifie pas les fichiers de configuration" sera ignore une partie du temps. Un hook qui `exit(2)` quand un fichier de config est modifie = enforcement total.

C'est le passage de l'**advisory** (instructions) au **deterministe** (contraintes executables).

> Note : la formule "Linters qui bloquent > Prompts qui suggerent" presente dans les versions anterieures de cette note **n'apparait PAS verbatim** dans l'article de Bockeler. Elle est une synthese forge du principe deterministe > suggestif, pas une citation.

## Relation avec le vault forge

Le vault forge-brain applique deja ce principe :
- `delegate-guard.py` — bloque les edits directs de skills/agents
- `devil-advocate-guard.py` — pattern feedback control sur livrables majeurs
- `vault-query-guard.py` — bloque les writes sans consultation vault prealable

Ces hooks = harness engineering applique a Claude Code.

## Couches du Harness (architecture)

```
┌─────────────────────────────────┐
│  Orchestration (subagents)      │
├─────────────────────────────────┤
│  Context Assembly               │
├─────────────────────────────────┤
│  Enforceable Constraints/Hooks  │
├─────────────────────────────────┤
│  Tool Execution Layer           │
├─────────────────────────────────┤
│  State Management               │
└─────────────────────────────────┘
         ↕ modele LLM ↕
```

## Stat marche

**65% des echecs d'agents** tracent a des defauts de harness, PAS a des limitations du modele — TechTimes (13 mai 2026), source primaire confirmee audit 23 mai.

## Ressources

- awesome-harness-engineering (GitHub ai-boost) — catalogue patterns/outils
- Article Bockeler sur martinfowler.com — reference canonique
- Augment Code Guide — application au coding

## Quand utiliser

- Design d'un systeme multi-agent
- Audit d'un agent existant qui a des comportements imprevisibles
- **Diagnostic de skill Cowork qui ne suit pas les instructions** — c'est un probleme de harness
- Decider entre "prompt instruction" et "hook deterministe"
- Evaluation de la robustesse d'un pipeline agentic

## Liens

- [[Context Engineering]] — Composant "orchestration" du harness
- [[workflow-claude-code-optimal]] — Patterns de harness appliques (Boris, Karpathy)
- [[agents-securite]] — Sandboxing et permissions = couches du harness
- [[mass-multi-agent-system-search]] — Optimisation automatisee du harness multi-agent
- [[MOC-Techniques]]

---

## AJOUT 16 juin 2026 — Compléments (carte de diagnostic Osmani, coût primaire, Loop Engineering)

> Veille cc-news 16 juin. Compléments à la note existante (qui couvre déjà Guides/Sensors, Computational/Inferential, Ashby). Sources primaires : [addyosmani.com](https://addyosmani.com/blog/agent-harness-engineering/), [mitchellh.com](https://mitchellh.com/writing/my-ai-adoption-journey), [anthropic.com/engineering/multi-agent-research-system](https://www.anthropic.com/engineering/multi-agent-research-system).

### Carte de diagnostic des défaillances (Addy Osmani)

Réflexe « ratchet » : à chaque erreur d'agent, mapper le symptôme vers le bon fix de harness (pas corriger l'output).

| Symptôme | Fix harness |
|---|---|
| Règle inconnue de l'agent | CLAUDE.md / AGENTS.md (guide) |
| Règle violée | hook (sensor/enforcement) |
| Info manquante | skill / MCP |
| Outil dangereux | restreindre permissions |
| Contexte pollué | isolation sub-agent |
| Crash silencieux | monitoring / sensor |

### Loop Engineering (Osmani) + origine du terme

« Loop Engineering » = remplacer le prompteur humain par un système qui prompte l'agent. Boris Cherny (verbatim) : *« I don't prompt Claude anymore. I have loops running that prompt Claude »*. **Origine du terme** : Mitchell Hashimoto, *my-ai-adoption-journey* (5 fév 2026) — *« Each line in [AGENTS.md] is based on a bad agent behavior »* (antérieur à Böckeler/LangChain). Cf [[hashimoto]] / [[addy-osmani]] / [[martin-fowler]].

### Coût tokens — chiffre PRIMAIRE Anthropic

Agents ≈ **4× tokens** vs chat, multi-agent ≈ **15× tokens** vs chat ([engineering/multi-agent-research-system](https://www.anthropic.com/engineering/multi-agent-research-system)). À distinguer du « 65% des échecs = harness » (TechTimes, déjà dans le corps). Ces 4×/15× sont du multi-agent, PAS une métrique de profondeur de nesting (cf [[anti-reentrance-sub-agents-pattern-escalade]] § AJOUT 16 juin, sous-agents imbriqués v2.1.172).

### Lien doctrine forge

Le pivot 22 mai (hooks = lint/sécu/scope, JAMAIS workflow) = « sensors computationnels, pas guides déguisés en enforcement ». Cf [[raisonnement-22mai-doctrine-vs-enforcement]].

`derniere-maj` → 2026-06-16.
