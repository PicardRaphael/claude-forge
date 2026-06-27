---
name: pivot-check
description: Detects Type 1 doctrinal drift (residual obsolete claims) after correcting a canonical note. Invoke when the user types /pivot-check, or when starting a session that follows a vault canonical edit. Advisory only — reports drifts, never auto-applies fixes.
user-invocable: true
effort: high
memory: project
allowed-tools: Grep, Read, Bash
---

# /pivot-check — Audit post-pivot doctrinal

Verifie qu'un pivot doctrinal (correction d'une note canonique vault) a bien ete propage a CLAUDE.md, `.claude/` et memoire. Detecte les drifts residuels **Type 1** (claims obsoletes survivants).

## QUAND invoquer

- Apres avoir corrige une note dans `vault/claude-forge/04-Techniques/claude-code/`
- Apres un audit revelant un drift doctrinal dans le repo
- Avant un commit modifiant une note canonique
- Manuellement : `/pivot-check <terme-obsolete>` ou `/pivot-check` (mode interactif)

## METHODE

### Etape 1 — Identifier les termes

Si l'utilisateur n'a pas fourni de termes, demander :
- Terme(s) **obsoletes** a detecter (ex : "Angela Jiang", "max deprecie")
- Terme(s) **canoniques** attendus (ex : "Brad Abrams", "effort: high")
- Note(s) canonique(s) source (ex : `workflow-claude-code-optimal`)

### Etape 2 — Perimetre obligatoire (grep cross-fichiers)

Lancer Grep sur chaque terme obsolete dans ces cibles :

| Cible | Scope |
|---|---|
| `CLAUDE.md` | Racine du repo courant |
| `.claude/skills/*/SKILL.md` | Toutes les skills |
| `.claude/agents/*.md` | Tous les agents |
| `.claude/rules/*.md` | Toutes les rules |
| `.claude/hooks/*.py` | Hooks (rare mais possible) |
| `vault/claude-forge/index.md` | Navigation principale LLM |
| `vault/claude-forge/00-Hub/*.md` | MOCs thematiques |
| `vault/claude-forge/05-Leaders/**` | Fiches biographiques |
| `memory/MEMORY.md` | Index memoire |
| `memory/feedback_*.md` | Feedbacks archives |
| `**/RECAP.md` | Session recaps qui figent du contexte obsolete |
| `.claude/agent-memory/*/MEMORY.md` | Memoires per-agent — **principale source du drift** observe sur neo_ia 22 mai |

**Paralleliser les Grep** — lancer toutes les cibles en parallele, pas sequentiellement.

### Etape 3 — Exclusions legitimes (NE PAS flagger)

Ignorer les occurrences dans :
- `vault/claude-forge/CHANGELOG.md` — historique narratif
- `vault/claude-forge/Knowledge/erreurs/` — contexte archive
- `vault/claude-forge/Knowledge/critiques/` — DA passes
- `vault/claude-forge/0-Inbox/_chantier-*` — archives chantier
- Lignes contenant "avant le" ou "coquille corrigee" (meta-historique)

**Regle biographies** : `vault/claude-forge/05-Leaders/` peut legitimement nommer des personnes — ces notes SONT la source de verite biographique. Flagger uniquement si le terme obsolete apparait dans une **affirmation doctrinale** (ex : dans CLAUDE.md ou une rule).

### Etape 4 — Rapport

Pour chaque occurrence hors exclusions :

  Fichier : .claude/skills/hook-creator/SKILL.md:42
  Terme obsolete : "max (effort level)"
  Suggestion : remplacer par "effort: high (max deprecie v2.1.91)"

Si > 5 occurrences dans des clusters differents — recommander delegation sub-agents par cluster.

### Etape 5 — Application (opt-in uniquement)

Si l'utilisateur confirme les fixes, deleguer aux specialistes :

| Cible | Agent |
|---|---|
| `CLAUDE.md` | `claudemd-creator` |
| `.claude/skills/*/SKILL.md` | `skill-creator` |
| `.claude/agents/*.md` | `subagent-creator` |
| `.claude/rules/*.md` | Edit direct (pas de specialiste) |
| Notes vault | Edit direct ou `/vault-audit` |

Le hook `delegate-guard.py` bloque les edits directs sur SKILL.md, agents et CLAUDE.md — deleguer est obligatoire, pas optionnel.

### Etape 6 — Capitalisation vault (SUGGÉRÉE, pas automatique)

⚠️ **Doctrine 22 mai** : cette skill est ADVISORY pure. Elle ne capitalise PAS automatiquement — elle SUGGÈRE à l'utilisateur de :

1. Mettre a jour `vault/claude-forge/CHANGELOG.md` (cf `.claude/rules/changelog-vault.md`)
2. Append dans `vault/claude-forge/log.md` : `## [YYYY-MM-DD] pivot-check | <pivot-name>`
3. Si le drift s'est reproduit — creer/mettre a jour `Knowledge/erreurs/<pivot-name>.md`

C'est à l'utilisateur (ou la session principale) d'exécuter ces actions. La skill rapporte + recommande, ne fait pas.

### Etape 7 — Propagation cross-repo (recommandation)

Si le pivot concerne une note canonique qui peut être référencée dans `ia_back` ou `neo_ia`, recommander à l'utilisateur de relancer /pivot-check dans ces repos depuis leur racine respective. Cette skill ne peut PAS scanner cross-repo elle-même (scope local), mais elle DOIT le signaler.

## ANTI-PATTERNS

- **Ne pas lancer /pivot-check avant d'avoir corrige la canonique** — detecte les drifts POST-correction, pas les erreurs dans la source
- **Ne pas skip les exclusions** — CHANGELOG et archives contiennent l'historique, le reecrire detruit la tracabilite
- **Batch fix sans grep post-fix** — toujours relancer Grep sur les termes corriges pour confirmer
- **Oublier CHANGELOG vault** — sans log, le pivot est invisible pour la session suivante

## GOTCHAS

- **05-Leaders est ambigu** : une fiche biographique contient forcément le nom de la personne — faux positif structurel. Flagger uniquement les **affirmations doctrinales** hors biographies (ex : le nom dans CLAUDE.md ou une rule).
- **memory/MEMORY.md tronque a 200 lignes** — le fichier peut contenir des entrees obsoletes au-dela de la limite de lecture. Si un terme manque dans le rapport, signaler l'ambiguite.
- **delegate-guard.py bloque le path direct** — ne pas tenter d'editer SKILL.md directement meme pour un fix evident, exit 2. Toujours passer par skill-creator.
- **Grep sur vault via Grep natif CC** — justifie car le perimetre inclut `.claude/` et `memory/`, pas seulement le vault (qui serait MCP-only). Les deux scopes coexistent dans cette skill.
- **Termes partiels polluent** : chercher "max" retournera des faux positifs massifs — toujours utiliser des termes suffisamment specifiques (ex : "effort: max" ou "max deprecie").

## Reference canonique vault

- [[methode-pivoter-doctrine]] — checklist 5 etapes complete qui inspire cette skill
- [[feedback_doctrine_drift_pattern]] — pattern reproduit 2x en 2 jours (mai 2026), Type 1/2/3

## Apprentissage

Apres chaque invocation, noter dans la memoire projet :
- Quel pivot a declenche l'invocation ?
- Combien de drifts Type 1 detectes / corriges ?
- Y a-t-il des exclusions a coder en dur pour ce repo ?

Patterns observes a coder ici au fil des sessions :
- `05-Leaders/` = exclusion structurelle, ne flagger que les affirmations doctrinales
- `CHANGELOG.md` vault = archive narrative, ne jamais modifier
- **Pivot neo_ia 22 mai 2026** : doctrine pivotée dans rules MAIS pas dans `.claude/agent-memory/*/MEMORY.md` → drift silencieux. C'est CE cas qui motive la skill. Ne JAMAIS skipper `agent-memory/` du périmètre.
