---
name: evolve
description: ALWAYS invoke when the user wants prioritized product/architecture evolution proposals for a project — what to build next (path via ARGUMENTS). NOT for config audit (repo-inspector), skill sweeps (skill-evolve) or code review.
argument-hint: "[/absolute/path/to/project]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Agent, mcp__forge-brain__*
model: sonnet
effort: high
---

# evolve — Propositions d’évolution produit et architecture

Analyse un projet et produit des propositions d’évolution priorisées, orientées **produit et architecture**.

**Ce n’est PAS un audit Claude Code** (repo-inspector (mode=analyze) fait ça).
**Ce n’est PAS une review de code existant** (/simplify fait ça).
C’est de la prospection : que manque-t-il pour que ce projet soit meilleur ?

## Phase 0 — Consulter canoniques forge (OBLIGATOIRE avant scan)

Avant tout scan, consulter via `mcp__forge-brain__read_note` (lecture EN ENTIER) :
- `methode-analyser-repo` — séquence A→B→C→D→E à appliquer
- `comment-ecrire-claudemd` — pour évaluer CLAUDE.md cible
- `mcp-vs-skills-doctrine` — pour évaluer composants stack-spécifiques

Plus tout pattern canonique ad-hoc pertinent à la stack détectée (Phase 1 → identifier stack → lire canoniques associées).

Anti-pattern : proposer évolutions sur savoir interne sans consulter forge-brain. La Phase 3 existante (cross-référence) ne suffit pas — elle arrive trop tard, après que le scan a déjà biaisé l'analyse.

Référence : [[pattern-mcp-brief-then-direct]] Règle 2.

## Validation préalable

Vérifier que $ARGUMENTS est fourni et que le chemin existe.

Si le chemin est absent ou invalide, afficher :

```
Usage : /evolve /chemin/absolu/du/projet
Exemple : /evolve <work-repos>/neo_ia
```

Ne pas continuer. Ne pas analyser le répertoire courant par défaut.

## Phase 1 — Scan structurel

Utiliser Glob et Read pour cartographier le projet. **Paralléliser les appels.**

### 1a. Architecture générale

```
Glob: **/*.py, **/*.ts, **/*.js, **/*.go, **/*.rs   (limiter à 200 résultats)
Glob: **/CLAUDE.md, **/.claude/agents/*.md, **/.claude/skills/*/SKILL.md
Glob: **/pyproject.toml, **/package.json, **/Cargo.toml, **/go.mod
Glob: **/docker-compose*.yml, **/Dockerfile, **/*.yaml (CI/CD)
Glob: **/pytest.ini, **/jest.config.*, **/vitest.config.*
```

Read les fichiers de config racine (pyproject.toml, package.json, Cargo.toml) pour extraire stack, dépendances, scripts.

### 1b. Tests

```
Glob: **/test_*.py, **/*_test.py, **/*.spec.ts, **/*.test.ts, **/*.spec.js
```

Comparer le nombre de fichiers tests vs fichiers source. Ratio < 0.3 = signal.

### 1c. Signaux de dette

```
Grep: TODO|FIXME|HACK|XXX|NOQA|type: ignore  (dans les sources)
Grep: NotImplementedError|raise NotImplementedError
Grep: except:|except Exception  (bare except = signal error handling faible)
Grep: print(  (debug prints laissés en prod = signal)
```

### 1d. Monitoring et observabilité

```
Grep: logging|logger|structlog|loguru
Grep: sentry|datadog|prometheus|opentelemetry|metrics
```

Absence de logging structuré ou de monitoring = signal.

### 1e. Documentation

```
Glob: **/README.md, **/docs/**/*.md, **/*.rst
Glob: **/.env.example, **/.env.template
```

Absence de README ou .env.example = signal.

## Phase 2 — Analyse des gaps

Sur la base du scan, identifier les gaps vs best practices.

Évaluer chaque dimension (OK / gap mineur / gap critique) :

| Dimension | Signaux négatifs |
|-----------|-----------------|
| Tests | ratio < 30%, absence de tests d’intégration, 0 fixture |
| Error handling | bare except, exceptions silencées, pas de retry |
| Observabilité | print debug, pas de logger structuré, pas de métriques |
| Typage | absence de type hints (Python), `any` omniprésent (TS) |
| Config | secrets hardcodés, pas de .env.example, pas de validation Pydantic/Zod |
| Documentation | README absent/vide, fonctions publiques sans docstring |
| Sécurité | dépendances non pincées, pas de scan deps |
| Patterns modernes | pas de retry/backoff, pas de circuit breaker si appels externes |
| DX | pas de makefile/scripts, pas de pre-commit, linter absent |
| Architecture | modules trop couplés, pas de séparation des concerns, god files |

## Phase 3 — Cross-référence contextuelle

**Interroger forge-brain avant de formuler les propositions :**

```
Skill: forge-brain
Query: "évolutions [nom du projet]" + "best practices [stack détectée]" + "erreurs passées [contexte]"
```

Objectif :
- Éviter de proposer quelque chose déjà tenté et abandonné
- S’appuyer sur les patterns documentés dans le vault
- Croiser avec les besoins utilisateurs si le vault les mentionne

Si le projet a un neoteem-brain accessible (MCP ou skill disponible), interroger également :
- Tickets ouverts pertinents
- Feedbacks utilisateurs sur les modules concernés

## Phase 4 — Synthèse et priorisation

Formuler **maximum 10-15 propositions**. Qualité > quantité.

Pour chaque proposition :
- **Titre court** (action + objet)
- **Pourquoi** : impact concret, ce qui se passe si on ne le fait pas
- **Effort estimé** : < 1h / 1-4h / > 4h
- **Fichiers concernés** : chemins relatifs au projet
- **Priorité** : basée sur impact × effort

### Buckets de priorisation

#### Quick Wins (effort < 1h, impact immédiat)
Ce qui se fait en une session et améliore significativement la base. Maximum 5.
Exemples typiques : ajouter .env.example, brancher un linter, corriger les bare except, ajouter un README.

#### Améliorations moyennes (effort 1-4h, améliore qualité/DX)
Ce qui demande une vraie session mais reste borné. Maximum 5.
Exemples : migrer vers logging structuré, ajouter des tests d’intégration sur les modules critiques, configurer pre-commit.

#### Features stratégiques (effort > 4h, valeur business/architecture)
Ce qui change la trajectoire du produit. Maximum 5. Être sélectif.
Exemples : ajouter un monitoring avec alertes, refactorer un module god, ajouter un pipeline CI/CD.

## Phase 5 — Output

Afficher dans la conversation (ne pas écrire dans le projet). Format :

```markdown
# Évolutions proposées — [nom du projet]

**Stack détectée :** [technologies principales]
**Signaux analysés :** [nb TODOs, ratio tests, gaps identifiés]
**Source forge-brain :** [note si vault consulté, insights trouvés]

---

## Quick Wins (< 1h)

### 1. [Titre]
**Pourquoi :** ...
**Effort :** ~Xmin
**Fichiers :** `path/relatif`

[2-5 items]

---

## Améliorations moyennes (1-4h)

### 1. [Titre]
**Pourquoi :** ...
**Effort :** ~Xh
**Fichiers :** `path/relatif`

[1-5 items]

---

## Features stratégiques (> 4h)

### 1. [Titre]
**Pourquoi :** ...
**Effort :** ~Xh
**Impact :** ...

[1-5 items]

---

## Ce qui a été écarté
[Lister 2-3 idées non retenues avec justification — montre que la sélection est intentionnelle]
```

La section **Ce qui a été écarté** est obligatoire. Elle prouve que la sélection est rigoureuse, pas un dump.

## Gotchas

- **$ARGUMENTS vide ou invalide** : ne jamais analyser `.` par défaut. Bail immédiat avec message d’usage.
- **Ne pas proposer de composants Claude Code** (skills, agents, hooks) — c’est repo-inspector (mode=analyze)/config-guardian. Rester sur le produit et l’architecture métier.
- **Read-only absolu** : aucun Write, Edit, ni Bash en écriture dans le chemin analysé. Jamais.
- **Cap strict à 15 propositions** : si on en trouve 20, garder les 15 avec le meilleur ratio impact/effort. L’exhaustivité est un anti-pattern.
- **Forge-brain en premier** : ne pas proposer une évolution que le vault mentionne comme abandonnée ou hors scope.
- **Ratio tests** : compter fichiers tests / fichiers source, pas les lignes. Ratio < 0.3 = signal, pas alerte critique automatique — contextualiser.
- **Chemins Windows/POSIX** : $ARGUMENTS peut être `C:\\path\\...` ou `/c/path/...`. Si Glob échoue avec un format, essayer l’autre.
- **Dead code vs dette** : un TODO seul n’est pas une proposition d’évolution. Grouper les TODOs thématiquement avant de proposer.
- **Ce qui a été écarté obligatoire** : si absent, la liste semble générée sans tri. Toujours inclure 2-3 items avec justification.
- **Ne pas dupliquer repo-inspector** : si l’utilisateur demande un audit setup CC, rediriger vers repo-inspector (mode=analyze). evolve = produit et architecture, pas la config .claude/.

## Exemples d’usage

```
/evolve <work-repos>/neo_ia
/evolve <work-repos>/ia_back
/evolve /home/user/projects/mon-api
```

## Apprentissage

Section pour capitaliser les découvertes entre sessions.
Après chaque usage significatif, sauvegarder en mémoire projet :

- Patterns récurrents détectés sur ce projet
- Propositions acceptées vs rejetées (et pourquoi)
- Gaps qui reviennent à chaque analyse (dette structurelle)

*Aucun apprentissage enregistré pour l’instant.*
