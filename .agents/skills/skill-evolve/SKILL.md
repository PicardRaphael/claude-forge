---
name: skill-evolve
description: ALWAYS invoke when user says "evolve skill", "ameliore la skill", "skill-evolve", or "sweep skills". Scans skills to spot which ones need attention (maturity score) and surfaces cross-pollination opportunities between skills. Delegates the deep per-skill audit + fixes to skill-creator. NOT for project architecture (use /evolve), NOT for Claude Code config audit (use repo-inspector mode=audit).
argument-hint: "[skill-name | all]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, mcp__forge-brain__*
model: sonnet
effort: high
---

# skill-evolve — Repérage stratégique + cross-pollination des skills

Deux rôles UNIQUES que `skill-creator` ne couvre pas :
1. **Sweep** — vue d'ensemble : quelles skills méritent attention (score de maturité, signaux rapides).
2. **Cross-pollination** — quels patterns d'une skill gagneraient à être transférés à une autre.

**L'audit profond d'UNE skill (6 dimensions, frontmatter, conformité standard, fixes) appartient à `skill-creator`** (qui a le GATE 0). skill-evolve ne le refait PAS — il REPÈRE et DÉLÈGUE.

**Ce n'est PAS `/evolve`** — `/evolve` analyse l'architecture produit d'un projet.
**Ce n'est PAS `repo-inspector (mode=audit)`** — qui audite la config `.claude/` entière.
**skill-evolve PROPOSE et PRIORISE. Il n'applique jamais.** Les corrections passent par `skill-creator`.

## Validation préalable

Vérifier que `$ARGUMENTS` est fourni. Si absent, afficher et stopper :
```
Usage : /skill-evolve <skill-name>   → repérage + cross-pollination d'une skill
        /skill-evolve all            → sweep de toutes les skills
```
Ne pas deviner une skill par défaut.

---

## Mode 1 — Repérage ciblé (skill-name)

Objectif : situer la skill (maturité, stabilité) et trouver les patterns transférables — PAS refaire l'audit conformité de skill-creator.

### Étape 1 — Charger la skill cible
- Glob `.claude/skills/<skill-name>/SKILL.md` (+ `~/.claude/skills/` si absente localement)
- Compter les lignes ; `git log --oneline -- <fichier> | head -10` (stabilité : <2 jeune, >10 dette potentielle ; skip si échec)

### Étape 2 — Score de maturité
Appliquer `references/scoring-rubric.md` (grille 1-5). Le score est un thermomètre, pas un audit complet.

### Étape 3 — Cross-pollination (le cœur unique de cette skill)
Comparer la skill cible aux autres skills forge. Pour chaque pattern de `references/cross-pollination-patterns.md`, vérifier s'il est pertinent ET absent de la cible :
- Lister les skills au workflow similaire (`ls .claude/skills/`)
- Identifier un pattern présent ailleurs et utile ici (fallback vault, validation $ARGUMENTS, scripts déterministes, progressive disclosure, format tableau sweep…)
- Pour chaque : « skill X fait Y mieux → applicable ici parce que Z »

### Étape 4 — Rapport de repérage
```
# Repérage skill — <skill-name>
**Maturité :** X/5 — [label]  ·  **Lignes :** X  ·  **Stabilité git :** X commits

## Cross-pollination (patterns transférables)
> Skill X fait Y mieux → appliquer ici parce que…  [Effort S/M/L]

## Signaux pour l'audit profond
[2-4 points qui méritent que skill-creator regarde de près — SANS faire l'audit ici]

## Ce qui est bien — ne pas toucher
[2-4 points forts. Obligatoire : une skill qui n'a que des défauts = analyse paresseuse]

## Prochaine étape
Pour l'audit profond + corrections → invoquer skill-creator sur <skill-name>
(skill-creator applique le GATE 0 : 6 dimensions, frontmatter, fixes).
```

### Étape 5 — Confirmation
- Lancer l'audit profond + fixes ? → invoquer `skill-creator` sur cette skill.
- Juste le repérage ? → OK, rien d'autre.
Ne jamais auto-appliquer. Ne jamais invoquer skill-creator sans confirmation.

---

## Mode 2 — Sweep (all)

Vue d'ensemble de TOUTES les skills pour prioriser. C'est l'usage le plus précieux : « lesquelles regarder en premier ».

### Étape 1 — Lister
```
ls .claude/skills/
ls ~/.claude/skills/ 2>/dev/null
```

### Étape 2 — Scan rapide par skill (léger, jamais profond)
Pour chaque skill, vérifier UNIQUEMENT :
1. Description présente + directive + triggers ?
2. SKILL.md > 500 lignes ?
3. Section Gotchas présente ?
4. Skill externe (kepano) ? → marquer "externe, ne pas toucher"

Ne PAS faire en sweep : recherche vault, git log, cross-pollination, audit 6 dimensions. Ça alourdirait un sweep de 25+ skills.

### Étape 3 — Output sweep
```
# Sweep skills — résultats
| Skill | Maturité | Signal principal | Type |
|-------|----------|------------------|------|
| forge-brain | 4/5 | OK | interne |
| obsidian-bases | — | externe, ne pas toucher | externe |

## Top 3 à traiter en priorité
1. <skill> — [raison] → `/skill-evolve <skill>` puis skill-creator
2. …
```
Le sweep PRIORISE ; il ne corrige rien. Chaque skill prioritaire part ensuite vers skill-creator.

---

## Gotchas

- **Ne refait PAS l'audit profond** — depuis le GATE 0 de skill-creator, l'audit 6-dimensions + frontmatter + fixes appartient à skill-creator. skill-evolve REPÈRE (maturité, cross-pollination) et DÉLÈGUE. Dupliquer l'audit = doublon à éviter.
- **Ne pas confondre avec `/evolve`** — `/evolve` = architecture produit projet. Rediriger si besoin.
- **Ne pas confondre avec `repo-inspector mode=audit`** — lui audite toute la config `.claude/`. skill-evolve = les skills uniquement, angle stratégique.
- **Ne jamais auto-appliquer** — propositions seulement. L'application passe par skill-creator (+ delegate-guard bloque les edits directs de toute façon).
- **Sweep = scan léger** — en mode `all`, pas de vault/git/cross-pollination par skill. Sinon inutilisable sur 25+ skills.
- **Skills externes (kepano)** — les marquer "ne pas toucher" dans le sweep ; ne jamais proposer de les réécrire (casse la synchro amont).
- **Pas de $ARGUMENTS dans backticks shell** — extraire dans une variable d'abord.
- **Section "Ce qui est bien" obligatoire** — équilibrer les propositions avec les points forts.
- **Skills dans ~/.claude/skills/** — ne pas oublier les skills globales.

## Références

- `references/scoring-rubric.md` — grille de maturité 1-5
- `references/cross-pollination-patterns.md` — patterns transférables entre skills (grandit à chaque analyse)
- `references/analyse-axes.md` — critères détaillés (le détail conformité est surtout couvert par skill-creator + checklist-skill-parfaite)

## Apprentissage

Après chaque usage : skills repérées + scores, patterns de cross-pollination identifiés et transférés, skills déléguées à skill-creator.

*Aucun apprentissage enregistré pour l'instant.*
