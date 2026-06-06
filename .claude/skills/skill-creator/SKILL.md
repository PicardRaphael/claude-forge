---
name: skill-creator
description: ALWAYS invoke when user wants to create, edit, audit, optimize, or benchmark a Claude Code skill / SKILL.md, or asks why a skill isn't triggering. Do not hand-write SKILL.md directly — use this skill first.
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, mcp__forge-brain__*
---

# skill-creator

Crée et optimise des skills Claude Code selon la doctrine forge + workflow Anthropic officiel.
Couvre : interview → draft → evals → optimization loop → packaging.

## Phase 0 — Détecter le point d'entrée

Extraire depuis l'historique AVANT d'interviewer :
- Nom / objectif si mentionné → skip question 1
- Environnement cible si évident → skip question 2
- Mode : création / optimisation / audit / benchmark

Vérifier qu'une skill similaire n'existe pas :

```bash
ls .claude/skills/ ~/.claude/skills/ 2>/dev/null
```

Si similaire → proposer modifier/optimiser plutôt que recréer.

---

## Phase 1 — Interview (AskUserQuestion, ≤ 4 questions/round)

Ne poser QUE ce qui n'est pas déductible du contexte. Stopper tôt si évident.
Extraire d'abord depuis l'historique de conversation, puis combler les trous.

**Round 1 — Intent (toujours)**
1. Que doit permettre cette skill à Claude ? (texte libre)
2. **Environnement cible ?** → CLI / Desktop / Cowork / Portable ← *question de branchement critique*
3. Créer nouvelle ou optimiser/auditer une existante ?

**Round 2 — Déclenchement & frontières**
4. Quand déclencher (phrases exactes utilisateur) ? Quand PAS (near-misses) ?
5. Side-effects ? (deploy/commit/send/delete) → si oui : `disable-model-invocation: true` + slash-only + AskUserQuestion gate (session principale uniquement — pas disponible en sub-agent)

**Round 3 — Forme & outillage**
6. SKILL.md unique ou dossier avec scripts + references ? (scripts si logique déterministe répétée ; references si doc > 300L)
7. Outils/MCP ? (stdio uniquement CLI/Desktop ; remote HTTPS pour Cowork)
8. Modèle cible ? (Haiku = plus de guidance ; Opus = moins ; Sonnet défaut)
9. Mettre en place des evals ? (recommandé OUI pour outputs objectivement vérifiables)

---

## Phase 2 — Recherche & edge cases (avant de rédiger)

- Probing proactif : edge cases, formats IO, fichiers exemples, critères de succès, dépendances
- Ne pas écrire les test prompts avant que tout soit clarifié
- Si skill complexe : recherche via MCP vault ou sub-agents en parallèle

---

## Phase 3 — Rédiger SKILL.md

### Frontmatter (règles absolues)

```yaml
---
name: <nom-exact-dossier-kebab-case>          # obligatoire = dossier
description: <TRIGGER directive 3e personne>  # UNE SEULE LIGNE, jamais >- ni |
user-invocable: true                          # si slash command souhaitée
allowed-tools: <liste ou mcp__server__*>      # wildcard préféré
model: sonnet | opus | haiku                  # optionnel
effort: high                                  # optionnel
disable-model-invocation: true                # si side-effects
---
```

**Description = trigger, pas résumé.** Template Seleznov (direction : 100% activation vs ~50% passive) :
```
ALWAYS invoke when [trigger concret]. <ce que fait la skill>. DO NOT [action concurrente] without invoking first.
```

Limites critiques :
- ≤ **250 chars** pratique — system reminder `/skills` tronque au-delà → auto-trigger défaillant
- ≤ **1024 chars** spec officielle
- description + `when_to_use` ≤ **1536 chars** combiné dans le listing
- Inclure **near-miss exclusions** (ce qui NE doit PAS déclencher)
- Pas de XML tags, pas de YAML multi-ligne (Prettier mangling casse la découverte)

### Corps SKILL.md (< 500 lignes — sinon déporter dans `references/`)

```markdown
# <Nom skill>

<1-2 phrases — quand utiliser, résultat attendu>

## Étapes
1. <étape concrète>
2. <étape concrète>

## Gotchas  ← section la plus importante
- <piège 1 avec pourquoi>

## Apprentissage  ← OBLIGATOIRE skills métier
<pattern ou découverte à noter après utilisation>
```

Principes rédaction :
- Voix impérative ; expliquer le *pourquoi* plutôt que ALL-CAPS MUST
- Réserver ALWAYS/NEVER/JAMAIS aux étapes vraiment fragiles/critiques
- Chemins forward-slash uniquement
- Si scripts/ : préciser EXÉCUTER vs LIRE dans le body
- Critique importante : < ligne 25, jamais en bas de fichier

### Structure dossier

```
.claude/skills/<nom>/
├── SKILL.md              # < 500 lignes
├── scripts/              # opérations déterministes (.py, .sh) — exécutables
└── references/           # doc longue, chargée à la demande, citée explicitement
```

### Enforcement selon environnement cible

| Cible | Ce qui marche | Ce qui NE marche PAS |
|-------|--------------|----------------------|
| **CLI** | Hooks PreToolUse/PostToolUse + description directive + CLAUDE.md routing | — |
| **Desktop** | Description directive + script-output gating + MCP local | Hooks peu fiables |
| **Cowork** | Description directive + script-output gating + remote HTTPS MCP + AskUserQuestion gate + project Instructions | **ZÉRO hooks**, pas de stdio MCP, CLAUDE.md non chargé |
| **Portable** | Description directive + script-output gating uniquement | Hooks, MCP stdio |

**Ne jamais émettre de hooks dans une skill ciblant Cowork.**
Routing : CLAUDE.md/.claude/rules (CLI/Desktop) ou project/folder Instructions (Cowork) — jamais dupliquer le contenu de la skill dans CLAUDE.md.

---

## Phase 4 — Écrire les test cases (2–3 prompts réalistes)

- Montrer à l'utilisateur pour validation avant d'enregistrer
- Sauvegarder dans `evals/evals.json` avec assertions laissées vides

---

## Phase 5 — Lancer les evals (structurellement critique)

Pour chaque test case, spawner **simultanément** deux sub-agents via Task tool :
- `with_skill` : run avec la skill active
- `baseline` : run sans la skill (ou snapshot ancienne version si optimisation)

Résultats dans :
```
<skill>-workspace/iteration-N/eval-<id>/
├── with_skill/outputs/
├── without_skill/outputs/   # ou old_skill/
├── eval_metadata.json
└── timing.json              # total_tokens + duration_ms — capturer dès notification
```

**Générer le eval viewer AVANT de juger soi-même** (`--static` sur Cowork/headless).

---

## Phase 6 — Rédiger les assertions pendant les runs

- Descriptives, vérifiables par script si possible
- Ne pas forcer des assertions sur des outputs subjectifs
- Format `grading.json` : champs exacts `text`, `passed`, `evidence` (le viewer dépend de ces noms)

---

## Phase 7 — Capturer timing

Dès chaque notification de fin de sub-agent → sauvegarder `timing.json` immédiatement.
C'est la seule occasion de capturer `total_tokens` et `duration_ms`.

---

## Phase 8 — Grader, agréger, lancer le viewer

1. Sub-agent grader (lit assertions) → `grading.json`
2. Agréger → `benchmark.json` + `benchmark.md` (pass_rate, time, tokens, mean±stddev, delta)
3. Sub-agent analyste → surface assertions non-discriminantes, evals flaky, tradeoffs
4. **Lancer le eval viewer AVANT de juger** — `--previous-workspace` si itération 2+

---

## Phase 9 — Lire le feedback & améliorer

Depuis `feedback.json` — principes d'amélioration Anthropic :
- **Généraliser** (éviter l'overfitting sur les cas test)
- **Garder lean** (lire les transcripts, pas juste les outputs — supprimer ce qui ne sert pas)
- **Expliquer le pourquoi** (ALL-CAPS MUST = yellow flag → reformuler avec raison)
- **Bundler le travail répété** (si tous les sub-agents ont réécrit le même helper → le mettre dans `scripts/`)

Recommencer depuis Phase 5 jusqu'à convergence.

---

## Phase 10 — Optimisation du déclenchement (description optimization loop)

Générer **~20 trigger queries** :
- 8–10 should-trigger (phrasing varié, cas peu courants)
- 8–10 should-NOT-trigger (near-misses — jamais triviales)

Revue avec l'utilisateur via `assets/eval_review.html`.
Loop : split 60/40 train/held-out, 3 runs par query, max 5 itérations → sélectionner `best_description` sur le score **test** (pas train — évite overfitting).

**Important** : les queries one-step simples ne déclenchent aucune skill (Claude les gère directement) — les queries doivent être substantielles.

---

## Phase 11 — Packaging & distribution

- Packager en `.skill` si distribution souhaitée
- Bundler en plugin pour distribution équipe (manifest `.claude-plugin/plugin.json`)
- Confirmer emplacement par surface :
  - `.claude/skills/` → projet
  - `~/.claude/skills/` → user (enregistrer via UI pour Cowork)
  - plugin-bundled → distribution équipe
- **Cowork** : enregistrer via UI, garder total actif < 30
- Conserver le nom à l'update (jamais `-v2`) ; copier dans temp dir avant d'éditer une skill read-only installée

---

## Checklist avant livraison (OBLIGATOIRE — cocher point par point à voix haute)

- [ ] `description` UNE SEULE LIGNE anglais, ≤ 250 chars pratique — jamais `>-` ni `|`
- [ ] `name` = nom exact du dossier kebab-case
- [ ] Description **directive** : ALWAYS invoke when… / DO NOT … without invoking first
- [ ] Near-miss exclusions incluses dans la description
- [ ] Pas de XML tags dans la description
- [ ] SKILL.md < 500 lignes (sinon `references/`)
- [ ] Pas de `README.md` dans le dossier
- [ ] Section **Gotchas** présente
- [ ] Section **Apprentissage** présente (skills métier)
- [ ] Pas de `$ARGUMENTS` dans des backticks shell
- [ ] Enforcement adapté à l'environnement cible (pas de hooks si Cowork/Portable)
- [ ] Side-effects : `disable-model-invocation: true` + AskUserQuestion gate
- [ ] Si 10+ skills dans le projet : vérifier budget avec `/doctor`
- [ ] Pas de BOM UTF-8 en tête du fichier (PowerShell Out-File → toujours UTF-8 sans BOM)

---

## Mode optimisation / audit (skill existante)

Évaluer chaque point de la checklist 6 dimensions (voir `references/checklist-skill-parfaite.md`).
Scorer violation par violation avec fichier + fix en une ligne. Boucler jusqu'à propre.

Priorités audit rapide :
1. Description passive ou tronquée (> 250 chars pratique) ?
2. SKILL.md > 500 lignes sans `references/` ?
3. Section Gotchas présente ?
4. Section Apprentissage présente (skills métier) ?
5. Near-miss exclusions dans la description ?
6. YAML multi-ligne (`>-` ou `|`) ?
7. ALL-CAPS excessif (> 2-3 = bruit) ?
8. References mortes ou chaînes > 1 niveau de profondeur ?
9. Assertions non-discriminantes dans les evals ?
10. Skill flat-file qui devrait être un dossier (scripts + references) ?

---

## Gotchas

- **BOM UTF-8** (PowerShell `Out-File`/`Set-Content`) → frontmatter YAML cassé silencieusement → skill non chargée ou "plugin validation failed". Toujours UTF-8 sans BOM. Vérifier : 3 premiers octets ≠ `239 187 191`
- **Description > 250 chars** → tronquée par system reminder `/skills` → auto-trigger défaillant même avec YAML valide (73% des skills passives ne se déclenchent jamais)
- **`$ARGUMENTS` dans backticks** → substitution littérale qui casse le quoting (Windows particulièrement)
- **`context: fork` / `agent:`** ignorés si invoqués via le Skill tool → utiliser Task tool explicite dans le body
- **AskUserQuestion** non disponible en sub-agent (issue #18721) → pattern ESCALADE vers session principale
- **Hot reload** : redémarrer la session pour prise en compte d'une nouvelle skill
- **Skills orphelines** dans frontmatter agent sans référence dans le body → jamais activées
- **Plugin force le préfixe** `/<plugin>:<skill>` → pour slash command courte sans préfixe, distribuer comme compétence individuelle (zip SKILL.md à la racine, pas de manifest)
- **Collision de descriptions** entre skills qui se chevauchent → ajouter "Use this for X, NOT for Y"
- **Queries one-step** ne déclenchent aucune skill (Claude les gère directement) → evals trigger = prompts substantiels

---

## Apprentissage

Après chaque création ou optimisation : noter ici les patterns efficaces et gotchas rencontrés.

---

## Références

- `references/checklist-skill-parfaite.md` — checklist 6 dimensions complète
- [[comment-creer-skill]] — doctrine forge canonique
- [[cowork-skills-reliability]] — matrice enforcement CLI/Desktop/Cowork
- [[eval-pattern-anthropic-skill-creator]] — détail infra A/B benchmark
