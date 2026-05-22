---
titre: "Thariq Shihipar"
resume: "Skills author Claude Code, 9 catégories skills LinkedIn mars 2026, Agent SDK Workshop 3-way trade-offs, 'HTML is the new markdown' Code with Claude SF"
aliases:
  - "thariq"
  - "@trq212"
  - "thariq shihipar"
  - "thariq skills"
  - "Thariq Anthropic"
  - "skills author claude code"
  - "9 categories skills"
  - "compute allocator"
  - "HTML is the new markdown"
role: "Skills Author, Claude Code team"
affiliation: "Anthropic"
derniere-maj: 2026-05-22
auteur: claude
sources:
  - "https://x.com/trq212"
  - "https://linkedin.com/in/thariq — post 17 mars 2026"
  - "Code with Claude SF, 6-7 mai 2026 — Agent SDK Workshop"
  - "Code with Claude SF, 6-7 mai 2026 — talk 'How I AI: HTML is the new markdown'"
type: leader
tags:
  - "#type/leader"
  - "#domaine/claude-code"
  - "#org/anthropic"
---

## QUI

Thariq Shihipar — auteur du système de **skills** Claude Code, équipe Anthropic Claude Code. Présent partout où la doctrine skills/SDK est formalisée : LinkedIn (post 9 catégories, 17 mars 2026), Code with Claude SF mai 2026 (Agent SDK Workshop + talk "HTML is the new markdown").

Twitter/X : [@trq212](https://x.com/trq212).

## POURQUOI EST PERTINENT

Thariq est **le référent doctrinal du système skills** — sa parole prime sur celle d'observateurs externes quand il s'agit de "qu'est-ce qu'une skill bien faite". Trois apports majeurs en 2026 :

1. **9 catégories skills** (LinkedIn, 17 mars 2026) — taxonomie complète, ordre verbatim.
2. **Agent SDK Workshop** (Code with Claude SF, mai 2026) — 3-way trade-offs Tools/Bash/Code gen, Swiss cheese defense, anti-pattern "50-100 tools".
3. **"HTML is the new markdown"** (Code with Claude SF) — doctrine "compute allocator" : 99% des tokens à la planification.

Il porte aussi la formulation "lethal trifecta" en pratique Anthropic — terme **forgé par Simon Willison juin 2025**, repris/diffusé par Thariq mais pas inventé par lui.

## CONTRIBUTIONS CLÉS

### Les 9 catégories de skills (LinkedIn, 17 mars 2026) — ORDRE VERBATIM

Verbatim exact, dans l'ordre publié :

1. **Library & API Reference**
2. **Product Verification**
3. **Data Fetching & Analysis**
4. **Business Process & Team Automation**
5. **Code Scaffolding & Templates**
6. **Code Quality & Review**
7. **CI/CD & Deployment**
8. **Runbooks**
9. **Infrastructure Operations**

L'ordre n'est pas arbitraire : il va de la couche **référence/savoir** (1-2) vers la couche **action/exécution** (8-9), avec dev/qualité au milieu (5-7). Une skill bien rangée trouve une de ces catégories sans tordre la définition.

### Agent SDK Workshop — 3-way trade-offs (Code with Claude SF, 6-7 mai 2026)

La décision **comment exposer une capacité à l'agent** :

| Voie | Caractère | Bon pour |
|------|-----------|----------|
| **Tools (MCP)** | atomic, non-reversible | actions discrètes à effet de bord clair (créer ticket, envoyer mail) |
| **Bash** | composable, exploratoire | exploration d'un système, chaînage ad hoc, débug |
| **Code gen** | dynamique | data analysis, transformation, calcul non-trivial |

Pas "MCP partout" — chaque voie a son créneau. Anti-pattern explicite : enfiler 50-100 tools MCP → **"le modèle se perd"**.

### Swiss cheese defense

Doctrine sécurité agents : **plusieurs couches de défense imparfaites** > une seule couche parfaite. Comme le fromage suisse, les trous d'une couche sont couverts par la couche suivante. Implication concrète : combiner permissions + hooks + classifier + sandbox, pas miser sur un seul mécanisme.

### Talk "How I AI: HTML is the new markdown" — Code with Claude SF

Verbatim :

> "99% of your AI-generated tokens should go to planning, interfaces, and communication — not production code."

> "We're all becoming 'compute allocators,' and our main job is to decide what's worth spending compute on."

Doctrine **compute allocator** : la valeur humaine n'est plus dans l'écriture du code, mais dans le **choix de l'allocation compute**. Quel projet mérite quoi, quand, à quel modèle, sur quel chemin. Le code n'est qu'un sous-produit de l'allocation.

### Lethal trifecta — attribution correcte

Thariq diffuse et applique le concept, mais le **terme "lethal trifecta" a été forgé par Simon Willison en juin 2025** (private data access + untrusted content + external communication = exfiltration). À citer comme "lethal trifecta (Simon Willison, repris par Thariq Shihipar dans la doctrine skills Anthropic)".

## VERBATIM NOTABLES

> "99% of your AI-generated tokens should go to planning, interfaces, and communication — not production code."

> "We're all becoming 'compute allocators,' and our main job is to decide what's worth spending compute on."

> "Le modèle se perd quand on lui donne 50-100 tools."
— Agent SDK Workshop, paraphrase fidèle.

> "Gotchas = highest-signal content in a skill."
— Doctrine skills antérieure, reprise depuis l'article LinkedIn "Lessons from Building Claude Code: How We Use Skills".

## WIKILINKS

- [[comment-ecrire-claudemd]]
- [[comment-creer-skill]]
- [[mcp-vs-skills-doctrine]]
- [[workflow-claude-code-optimal]]
- [[methode-analyser-repo]]
- [[comment-creer-skill|Skills Best Practices]]
- [[Boris Cherny]] — co-doctrine Claude Code
- [[Erik Schluntz]] — co-architecture agents
- [[MOC-Leaders]]

## SOURCES

- Twitter : https://x.com/trq212
- LinkedIn post "Lessons from Building Claude Code: How We Use Skills" + post 9 catégories (17 mars 2026)
- Code with Claude SF, 6-7 mai 2026 — Agent SDK Workshop (3-way trade-offs, Swiss cheese, anti-pattern 50-100 tools)
- Code with Claude SF, 6-7 mai 2026 — talk "How I AI: HTML is the new markdown"
- Simon Willison, juin 2025 — terme original "lethal trifecta"
- Recherche vault : `0-Inbox/_chantier-22mai/recherche-youtube-talks.md`
- Recherche vault : `0-Inbox/_chantier-22mai/recherche-x-twitter-leaders.md`
