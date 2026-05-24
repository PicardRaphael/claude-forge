---
name: skill-evolve
description: Analyzes a Claude Code SKILL.md effectiveness and proposes concrete improvements based on execution patterns, cross-pollination with other skills, and vault techniques. Use when optimizing a skill, running a maintenance sweep, or when the user says "evolve skill", "améliore la skill", "skill-evolve", or "sweep skills".
argument-hint: "[skill-name | all]"
user-invokable: true
allowed-tools: Read, Glob, Grep, Bash, mcp__forge-brain__*
model: sonnet
effort: high
---

# skill-evolve — Méta-analyse et amélioration des skills

Analyse une skill existante et produit des propositions d'amélioration concrètes.

**Ce n'est PAS `/evolve`** — `/evolve` analyse l'architecture produit d'un projet.
**Ce n'est PAS un audit de config Claude Code** — `project-auditor` fait ça.
C'est une analyse de l'efficacité d'une SKILL.md elle-même : est-elle bien structurée, bien déclenchée, exploite-t-elle les meilleures techniques disponibles ?

**Ce skill PROPOSE. Il n'applique jamais.** Les modifications passent par `skill-creator`.

## Validation préalable

Vérifier que `$ARGUMENTS` est fourni.

Si absent, afficher :
```
Usage : /skill-evolve <skill-name>
        /skill-evolve all
Exemple : /skill-evolve forge-brain
          /skill-evolve all
```
Ne pas continuer. Ne pas deviner une skill par défaut.

## Mode 1 — Analyse profonde (skill-name)

### Étape 1 — Charger la skill cible

Pour la skill nommée dans $ARGUMENTS :
- Glob `.claude/skills/<skill-name>/SKILL.md`
- Glob `.claude/skills/<skill-name>/references/*.md`
- Glob `~/.claude/skills/<skill-name>/SKILL.md` (si absente localement)

Si aucun fichier trouvé : afficher la liste des skills disponibles et bail.

Compter les lignes du SKILL.md.

### Étape 2 — Charger le contexte mémoire

- Read `.claude/agent-memory/skill-creator/MEMORY.md`

Chercher dans MEMORY.md les feedbacks mentionnant le nom de la skill ou sa catégorie.

### Étape 3 — Interroger le vault

Utiliser le MCP forge-brain (auto-start, port 8091) :

```
forge-brain:search_brain query="<skill-name> technique amélioration" limit=8
forge-brain:search_brain query="erreur skill <domaine>" limit=5
```

Si le MCP ne répond pas : fallback Glob sur `vault/claude-forge/04-Techniques/` et `vault/claude-forge/Knowledge/erreurs/`.

### Étape 4 — Vérifier l'historique git

```
git log --oneline -- .claude/skills/<skill-name>/SKILL.md | head -10
```

Nombre de commits = indicateur de stabilité. < 2 commits = jeune. > 10 commits = vieille dette potentielle.
Si git log échoue, skip sans erreur.

### Étape 5 — Analyser sur 4 axes

Voir `references/analyse-axes.md` pour les critères détaillés de chaque axe.

**Axe 1 — Efficacité**
- La description déclenche-t-elle correctement ? Contient-elle des triggers naturels ?
- Le workflow est-il complet ou s'arrête-t-il trop tôt ?
- Les Gotchas couvrent-ils les vraies erreurs (pas l'évident) ?

**Axe 2 — Évolution**
- Y a-t-il des techniques récentes dans le vault qui pourraient enrichir cette skill ?
- Le modèle/effort configuré est-il toujours optimal ?
- Des patterns documentés dans MEMORY.md s'appliquent-ils sans être encore intégrés ?

**Axe 3 — Cross-pollination**
- Quelles autres skills font quelque chose de similaire mieux ?
- Y a-t-il un pattern (progressive disclosure, checklist, script déterministe) présent ailleurs et absent ici ?
- Voir `references/cross-pollination-patterns.md` pour les exemples documentés.

**Axe 4 — Simplification**
- Peut-on supprimer des étapes sans perdre de valeur ?
- Y a-t-il des instructions qui énoncent l'évident (anti-pattern Thariq) ?
- Le SKILL.md est-il > 500 lignes ? Si oui, quoi déporter dans references/ ?

### Étape 6 — Produire le rapport

Format de sortie (dans la conversation, jamais dans un fichier) :

```
# Analyse skill — <skill-name>

**Score de maturité :** X/5 — [label]
**Lignes SKILL.md :** X [OK / DÉPASSE 500L -> à déporter]
**Stabilité git :** X commits [jeune / stable / ancienne dette]
**Sources consultées :** mémoire [oui/non] · vault [oui/non · N résultats]

---

## Propositions classées par impact

### Impact élevé

#### 1. [Titre court]
**Axe :** [Efficacité / Évolution / Cross-pollination / Simplification]
**Problème :** ...
**Proposition :** ...
**Effort :** S (< 30min) / M (1-2h) / L (> 2h)

[2-4 items]

### Impact moyen

[1-3 items, même format]

### Impact faible (nice-to-have)

[0-2 items]

---

## Cross-pollination

> Skill X fait Y mieux — appliquer le même pattern ici parce que...

---

## Ce qui est bien — ne pas toucher

[2-4 points forts à préserver]

---

## Prochaine étape

Pour appliquer ces changements : invoquer skill-creator avec ce brief.
```

La section **Ce qui est bien** est obligatoire — une skill qui n'a que des défauts est une analyse paresseuse.

### Étape 7 — Demander confirmation

Terminer par :
- Appliquer ces changements ? -> invoquer skill-creator avec ce brief.
- Prioriser autrement ? -> préciser et relancer l'analyse.
- Juste analyser pour l'instant ? -> OK, aucune modification faite.

Ne jamais auto-appliquer. Ne jamais invoquer skill-creator sans confirmation explicite.

---

## Mode 2 — Sweep (all)

Quand $ARGUMENTS = "all", analyse rapide sur TOUTES les skills.

### Étape 1 — Lister les skills

```
ls .claude/skills/
ls ~/.claude/skills/ 2>/dev/null
```

### Étape 2 — Analyse rapide par skill

Pour chaque skill, vérifier uniquement :
1. Axe Efficacité : description en anglais ? triggers présents ?
2. Axe Simplification : SKILL.md > 500 lignes ? Section Gotchas présente ?

Ne PAS faire en sweep : recherche vault, git log, cross-pollination.
Ces checks alourdiraient un sweep de 25+ skills.

### Étape 3 — Output sweep

```
# Sweep skills — résultats

| Skill | Score rapide | Signal principal |
|-------|-------------|-----------------|
| forge-brain | 4/5 | OK |
| cc-skills-ref | 3/5 | SKILL.md 612L -> déporter |
| evolve | 5/5 | OK |

## Top 3 à analyser en profondeur

1. <skill> — [raison principale]
2. <skill> — [raison principale]
3. <skill> — [raison principale]

Lancer /skill-evolve <skill-name> pour l'analyse complète.
```

---

## Gotchas

- **Ne pas confondre avec `/evolve`** — `/evolve` analyse l'architecture produit d'un projet. `/skill-evolve` analyse une SKILL.md elle-même. Si l'utilisateur veut analyser l'architecture d'un projet : rediriger vers `/evolve`.
- **Ne jamais auto-appliquer** — ce skill produit des propositions uniquement. L'application passe toujours par skill-creator avec confirmation explicite. Le hook delegate-guard bloque les edits directs de toute façon.
- **Sweep = analyse légère uniquement** — en mode "all", ne pas lancer de recherche vault ni git log pour chaque skill. Inutilisable sur > 15 skills.
- **Pas de $ARGUMENTS dans backticks shell** — si besoin d'utiliser le nom de la skill dans une commande bash, l'extraire dans une variable d'abord.
- **Section "Ce qui est bien" obligatoire** — proposer uniquement des défauts donne l'impression que la skill ne vaut rien. Équilibrer avec les points forts.
- **Score 5/5 = propositions quand même** — une skill mature a toujours des micro-améliorations. Score 5 = stable, pas parfaite.
- **Skill dans ~/.claude/skills/** — ne pas oublier les skills globales. Chercher dans les deux emplacements.
- **Vault non disponible** — si Obsidian CLI échoue au pré-check, fallback Glob sur vault/. Ne pas bloquer l'analyse.

## Références

- `references/analyse-axes.md` — critères détaillés des 4 axes d'analyse avec exemples
- `references/scoring-rubric.md` — grille de maturité 1-5 avec labels et exemples
- `references/cross-pollination-patterns.md` — patterns cross-skills documentés

## Apprentissage

Après chaque usage significatif, sauvegarder en mémoire projet :

- Skills analysées et scores obtenus
- Propositions acceptées vs rejetées (et pourquoi)
- Patterns récurrents identifiés

*Aucun apprentissage enregistré pour l'instant.*
