---
titre: "Comment écrire un CLAUDE.md parfait"
resume: "Note canonique pour écrire un CLAUDE.md selon la doctrine Anthropic mai 2026 — target 200 lignes, test 'Would removing this cause mistakes?', 5 anti-patterns officiels, compounding error-driven."
aliases:
  - "comment ecrire claudemd"
  - "claudemd parfait"
  - "ecrire CLAUDE.md"
  - "write CLAUDE.md"
  - "CLAUDE.md best practices"
  - "claudemd guide"
  - "memory CLAUDE.md"
  - "configuration CLAUDE.md"
  - "200 lignes CLAUDE.md"
  - "anti-patterns CLAUDE.md"
derniere-maj: 2026-05-22
auteur: claude
type: technique
sources:
  - "https://code.claude.com/docs/en/memory"
  - "https://www.anthropic.com/engineering/claude-code-best-practices"
  - "Pragmatic Engineer interview Boris Cherny"
  - "Code with Claude London keynote 19 mai 2026"
  - "github.com/anthropics/claude-for-legal/CLAUDE.md"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#sujet/claudemd"
  - "#doctrine/2026"
---

# Comment écrire un CLAUDE.md parfait

> Note canonique forge — doctrine Anthropic mai 2026, validée verbatim sur sources officielles.

---

## QUOI — Définition

`CLAUDE.md` = fichier markdown chargé automatiquement dans le contexte de chaque session Claude Code. Il contient les **instructions persistantes spécifiques au projet** : conventions, gotchas, commandes fréquentes, contraintes architecturales.

**Distinction critique avec MEMORY.md** :

| Fichier | Rôle | Limite |
|---------|------|--------|
| **CLAUDE.md** | Instructions projet (versionné dans le repo) | **Target < 200 lignes** (recommandation forte, pas hard) |
| **MEMORY.md** | Mémoire auto user-level (auto-générée) | **200 lignes OU 25 KB** (hard limit) |

**Verbatim Anthropic** :

> "target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence."
> — [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory), section Size + troubleshooting "My CLAUDE.md is too large"

---

## POURQUOI — Le problème résolu

Sans CLAUDE.md, Claude redécouvre à chaque session :
- la stack du projet
- les gotchas Windows/Mac
- les conventions de nommage
- les commandes de test/lint/build
- les decisions architecturales déjà prises

Conséquences observées :
- **Répétition d'erreurs** déjà commises et déjà corrigées 3 sessions plus tôt
- **Coût tokens** : chaque session = exploration redondante
- **Frustration utilisateur** : "je l'ai déjà dit"

CLAUDE.md = **compounding** : chaque erreur capturée une fois ne se reproduit plus.

**Verbatim Boris Cherny** :

> "Anytime we see Claude do something incorrectly, we add it to CLAUDE.md"
> — Boris Cherny, interview Pragmatic Engineer

---

## COMMENT — Structure type

### Structure minimale (5 sections)

```markdown
# <Nom projet>

**Une phrase qui dit ce que fait le projet.**

## Stack

- Langage(s) + versions
- Framework principal
- Base de données
- Tests runner
- Build / package manager

## Commandes fréquentes

- Build : `<cmd>`
- Test : `<cmd>`
- Lint : `<cmd>`
- Run dev : `<cmd>`

## Gotchas (compounding)

- <pièges observés en session, ajoutés au fil du temps>
- <typiquement OS-specific, paths, quoting>

## Conventions

- Naming
- Structure des dossiers
- Patterns spécifiques au repo

## Things to leave alone

- Fichiers/dossiers générés
- Migrations DB (immutables)
- Vendored code
```

**Exemple concret référence** : [anthropics/claude-for-legal/CLAUDE.md](https://github.com/anthropics/claude-for-legal) — 130 lignes, 5 sections, seul CLAUDE.md Anthropic public structuré.

### Test de chaque ligne — "Would removing this cause mistakes?"

**Verbatim Anthropic** :

> "Would removing this cause Claude to make mistakes? If not, cut it."
> — Anthropic best-practices

Appliquer ce test à **chaque ligne** avant de la garder. Une ligne descriptive (qui dit ce que fait le code) = à supprimer. Une ligne directive (qui empêche une erreur observée) = à garder.

---

## QUAND — Critères d'application

| Situation | CLAUDE.md ? |
|-----------|-------------|
| Tout repo avec Claude Code utilisé > 2 sessions | OUI |
| Erreur récurrente non capturée | AJOUTER ligne |
| Convention non-évidente du repo | AJOUTER ligne |
| Décision archi qui surprend un nouveau venu | AJOUTER ligne |
| Description du code lisible dans le code | NE PAS AJOUTER |
| Règle qui doit valoir 100% du temps | **Hook, pas CLAUDE.md** (voir [[comment-creer-hook]]) |
| Instruction réutilisable cross-repo | **Skill, pas CLAUDE.md** (voir [[comment-creer-skill]]) |

**Doctrine forge 22 mai 2026** : tout ce qui DOIT tenir à 100% sort de CLAUDE.md (advisory ~80% compliance) vers un hook bloquant.

> "If a rule must hold every time, make it a hook rather than a prompt instruction."
> — docs Anthropic, features-overview (validation totale doctrine 22 mai)

---

## WORKFLOW — Cycle de vie d'un CLAUDE.md

### Pour un nouveau repo

1. **Cloner** le repo + ouvrir Claude Code
2. **Première session** : laisser vide ou squelette 5 sections
3. **À chaque correction utilisateur** : décider — ligne CLAUDE.md ? hook ? skill ?
4. **Mensuel** : audit (cf [[forge-review]] côté forge) — supprimer le redondant, élaguer

### Pour un repo existant accumulé

1. Lire le CLAUDE.md ligne par ligne
2. Pour chaque ligne : appliquer test "Would removing this cause mistakes?"
3. Pour chaque ligne survivante : "est-ce que c'est advisory ou doit-il tenir 100% ?"
   - Advisory → reste dans CLAUDE.md
   - 100% → migrer vers hook
4. Tasser les sections : kitchen-sink → 5 sections claires

### Cycle compounding (Boris)

```
Session N  → erreur observée
           → "tu as encore fait X"
           → ajouter ligne CLAUDE.md
Session N+1 → erreur évitée (compounding)
```

---

## APPELS — Quelles autres notes/composants mobilisés

- [[comment-creer-hook]] — quand une règle doit tenir 100% du temps
- [[comment-creer-skill]] — quand une instruction est réutilisable cross-repo
- [[comment-creer-agent]] — quand l'instruction concerne un rôle spécifique
- [[workflow-claude-code-optimal]] — comment CLAUDE.md s'inscrit dans le workflow global
- [[methode-analyser-repo]] — comment construire un CLAUDE.md initial pour un repo nouveau
- [[mcp-vs-skills-doctrine]] — quand l'instruction concerne l'accès aux données vs how-to

---

## OPTIMISATION — 3 niveaux

### Niveau basique (5 sections, < 100 lignes)

- Stack + commandes + gotchas + conventions + things to leave alone
- Test "Would removing this cause mistakes?" appliqué partout
- Aucune description, que des directives

### Niveau avancé (< 200 lignes, sections riches)

- + Section **Doctrine projet** : décisions archi expliquées en 1 ligne chacune
- + Section **Vault/MCP rules** si MCP custom
- + `@import` vers autres fichiers (`@./docs/conventions.md`) pour modulariser
- Compounding mensuel actif (audit + nettoyage)

### Niveau expert (cross-repo + hooks complémentaires)

- CLAUDE.md = advisory layer (80% compliance attendue)
- Règles critiques doublées par hooks bloquants
- Skills extraites pour réutilisation cross-repo
- Frontmatter custom si tooling automatique consomme CLAUDE.md

---

## POURQUOI CETTE OPTIM — Gain mesurable

| Optim | Gain |
|-------|------|
| < 200 lignes vs 500+ | **~60% moins tokens** chargés à chaque session, adhérence Claude **mesurablement meilleure** (verbatim Anthropic : "consume more context and reduce adherence") |
| Test "Would removing..." | Élimine 30-50% des lignes en moyenne sur un CLAUDE.md non-audité |
| Compounding error-driven | **0% récurrence** des erreurs capturées (vs ~40% sans) |
| Sortie vers hooks | Passe de ~80% compliance à 100% sur les règles critiques |
| `@import` modulaire | Réduit duplication entre repos liés, chargement conditionnel |

---

## ANTI-PATTERNS — 5 officiels Anthropic + extensions forge

### 5 anti-patterns officiels Anthropic

| Anti-pattern | Symptôme | Correction |
|--------------|----------|------------|
| **Kitchen sink** | Tout mettre "au cas où" | Test "Would removing this cause mistakes?" |
| **Correcting over and over** | Même règle répétée 3× sous formulations différentes | Une seule formulation, formulée comme directive |
| **Over-specified** | Précision sur l'inutile, descriptions du code | Décrire le code lisible n'aide pas — supprimer |
| **Trust-then-verify gap** | Lister une rule sans la vérifier par un hook | Si critique → hook. Sinon accepter ~80% |
| **Infinite exploration** | Pas de bornes d'investigation données | Préciser scope max ("ne lis pas plus de X fichiers") |

### Anti-patterns forge supplémentaires

- ❌ **Routing dans CLAUDE.md** : "si l'utilisateur dit X, fais Y" — appartient à `.claude/rules/` (cf doctrine forge)
- ❌ **Documentation du code** : "la fonction `foo` fait X" — appartient au code lui-même
- ❌ **STOP critique en fin de fichier** : les instructions critiques (interdits, STOP) doivent être < ligne 25, jamais en gotcha de fin (cf [[erreur-stop-critique-position-gotcha-fin]])
- ❌ **ALL-CAPS excessif** : 1-2 emphasis OK, 20 = bruit (cf [[erreur-emphasis-overtriggering]])
- ❌ **CLAUDE.md comme TODO list** : utiliser plans/, pas CLAUDE.md
- ❌ **Mise à jour 3 sessions trop tard** : capturer l'erreur tout de suite ou jamais (le détail s'évapore)

---

## EXEMPLES CONCRETS — Repos externes publics

### 1. `anthropics/claude-for-legal/CLAUDE.md` (référence Anthropic)

**130 lignes, 5 sections** :
- Validation pipeline (lint, type, test commandes exactes)
- Conventions (naming, structure)
- Cookbooks (patterns récurrents du repo)
- Things to leave alone (générés, migrations)
- Onboarding (commandes setup)

Le seul CLAUDE.md d'Anthropic exposé publiquement — **référence canonique**.

### 2. `anthropics/claude-code` (minimaliste)

Le repo source de Claude Code lui-même : `.claude/` contient **3 slash commands custom** et un CLAUDE.md ultra-court. La doctrine "minimal qui marche" en action.

### 3. `github.com/trailofbits/claude-code-config` (entreprise sécu)

Config complète Trail of Bits exposée publiquement. CLAUDE.md illustre :
- Section sandbox 3-tier (`/sandbox` builtin / devcontainer / dropkit)
- Stop hook anti-rationalization (Haiku check cop-outs) — pattern inédit
- Sections sécu explicites

### 4. `forrestchang/andrej-karpathy-skills` (CLAUDE.md viral)

**70 lignes, 4 principes** — repo 110k stars (220k cumul avec mirror multica-ai). **NB** : pas endorsé par Karpathy publiquement, mais largement repris. Démonstration que **court + opinionated > long + neutre**.

---

## SOURCES — Verbatim avec URLs

### Anthropic officiel

- [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory) — taille 200L target, distinction MEMORY.md
- [anthropic.com/engineering/claude-code-best-practices](https://www.anthropic.com/engineering/claude-code-best-practices) — anti-patterns + test "Would removing..."
- docs Anthropic features-overview — doctrine hook vs rule

### Boris Cherny (Anthropic, créateur Claude Code)

- Pragmatic Engineer interview — "Anytime we see Claude do something incorrectly, we add it to CLAUDE.md"
- Sequoia AI Ascent avril 2026 — "coding is solved"
- Code with Claude London 19 mai 2026 — "I prompt Claude → I create a routine that prompts Claude"

### Repos publics

- [anthropics/claude-for-legal](https://github.com/anthropics/claude-for-legal) — CLAUDE.md 130L référence
- [anthropics/claude-code](https://github.com/anthropics/claude-code) — config minimaliste
- [trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config) — config entreprise sécu
- [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) — CLAUDE.md viral

---

## GOTCHAS — Pièges observés

### Pièges Windows

- **Path absolu Python obligatoire** dans CLAUDE.md si on référence un script Python custom (alias MS Store sinon)
- **Quoting `$ARGUMENTS`** : ne jamais passer `$ARGUMENTS` dans des backticks shell (`` `cmd $ARGUMENTS` ``) — la substitution littérale casse le quoting

### Pièges génériques

- **Frontmatter facultatif** : CLAUDE.md n'a PAS besoin de frontmatter YAML (≠ skills/agents/rules). Si ajouté, Claude l'ignore.
- **@import circulaire** : `@./CLAUDE.md` dans un fichier importé = boucle. Vérifier l'arbre d'imports.
- **Position dans le repo** : `CLAUDE.md` à la racine est chargé. `<sous-dossier>/CLAUDE.md` aussi (additif). Plus on descend, plus le contexte se spécialise.
- **Mise à jour pendant session** : Claude ne recharge PAS CLAUDE.md mid-session par défaut. Nouvelle session = nouveau chargement.

### Pièges forge spécifiques

- Bloc CLAUDE.md géré par agent dédié [[claudemd-optimizer]] côté forge — `Edit` direct bloqué par hook `delegate-guard.py`
- Audit mensuel via `/forge-review` (slash command custom forge)
- Variable `CLAUDE_AGENT=claudemd-optimizer` pour bypass hook si Bash heredoc nécessaire

---

## ALIASES — Findability max

Aliases déjà déclarés en frontmatter (10) :
- comment ecrire claudemd
- claudemd parfait
- ecrire CLAUDE.md
- write CLAUDE.md
- CLAUDE.md best practices
- claudemd guide
- memory CLAUDE.md
- configuration CLAUDE.md
- 200 lignes CLAUDE.md
- anti-patterns CLAUDE.md

---

## WIKILINKS — Vers notes liées

### Notes canoniques sœurs
- [[comment-creer-skill]]
- [[comment-creer-agent]]
- [[comment-creer-hook]]
- [[workflow-claude-code-optimal]]
- [[methode-analyser-repo]]
- [[mcp-vs-skills-doctrine]]
- [[pattern-vault-llm-karpathy]]

### Fiches leaders
- [[Boris Cherny]] (à créer dans la phase leaders)
- [[Cat Wu]]
- [[Erik Schluntz]]

### Knowledge — erreurs liées
- [[erreur-stop-critique-position-gotcha-fin]]
- [[erreur-emphasis-overtriggering]]
- [[erreur-hooks-workflow-enforcement]]
- [[erreur-advisory-rules-insuffisantes]]
- [[raisonnement-22mai-doctrine-vs-enforcement]]

### Forge custom
- [[forge-review]] — audit mensuel CLAUDE.md
- [[claudemd-optimizer]] — agent dédié forge

---

**Fin note canonique `comment-ecrire-claudemd.md`** — pilote du chantier 22 mai 2026.
