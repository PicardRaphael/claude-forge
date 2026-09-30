---
name: skill-evolve
description: ALWAYS invoke when user says 'evolve skill', 'améliore la skill' or 'sweep skills'. Scores skill maturity, surfaces cross-pollination, delegates deep fixes to skill-creator. NOT for project architecture (evolve) or config audit (repo-inspector).
argument-hint: "[skill-name | all | friction [jours]]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, mcp__forge-brain__search_brain, mcp__forge-brain__read_note, mcp__forge-brain__read_note_by_path, mcp__forge-brain__read_section, mcp__forge-brain__list_notes
model: opus
effort: medium
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
Usage : /skill-evolve <skill-name>     → repérage + cross-pollination d'une skill
        /skill-evolve all              → sweep de toutes les skills
        /skill-evolve friction [jours] → skills qui frottent en usage réel (cross-session, défaut 14j)
```
Ne pas deviner une skill par défaut. `friction` accepte un entier optionnel = fenêtre en jours.

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

## Mode 3 — Friction (analyse cross-session)

Objectif : repérer les skills qui **frottent en usage réel de façon RÉPÉTÉE** (sur plusieurs sessions), et proposer un rapport d'amendements à valider. Comme les autres modes : **PROPOSE et DÉLÈGUE, n'applique jamais**.

**Frontière avec `/done`** : `/done` capture les erreurs d'UNE session à chaud (mono-session). Ce mode ne remonte QUE ce qui se **répète sur ≥2-3 sessions** — le pattern cross-session que `/done` ne peut pas voir. Ne pas re-surfacer ce que `/done` a déjà capté en mono-session.

### Étape 1 — Lire la source de friction (MCP)
Requêter `mcp__forge-brain__search_tool_events` (source `tool_events` : les `tool_use`/`tool_result` indexés). Ne PAS parser les `.jsonl` à la main.
- Erreurs récentes : `search_tool_events(is_error=true, since="<fenêtre>")` → regrouper par signature d'erreur (normaliser chiffres/paths) pour trouver les récurrences.
- Collisions : examiner les `tool_use` d'invocation de skills concurrentes sur des tours proches.

Si l'outil `search_tool_events` est absent → **signaler** que le MCP doit être rechargé avec `tool_events.enabled: true` (voir Gotchas). Ne pas fallback sur un parse brut.

### Étape 2 — Classer par signal + confiance
| Signal | Confiance | Détection |
|--------|-----------|-----------|
| 3 — erreur récurrente (≥2-3 sessions, même signature) | **[FIABLE]** | `is_error=true` groupé par signature |
| 4 — collision de déclenchement | **[FIABLE]** | `tool_use` de skills concurrentes |
| 2 — résultat corrigé par l'utilisateur | **[CANDIDAT — à vérifier]** | miner haute-précision, corrections nettes uniquement |
| 1 — skill manquée (dispo + non appelée + invoquée à la main ensuite) | **[CANDIDAT — à vérifier]** | proxy comportemental, jamais affirmé comme fait |

Les signaux 1 & 2 sont structurellement fragiles (pas de vérité-terrain fiable — cf `Knowledge/dettes/dette-detection-signaux-friction-skills`). Les surfacer comme **candidats à valider**, jamais comme certitudes.

### Étape 3 — Rapport (chaque item cite sa preuve)
```
# Friction skills — fenêtre <N> jours
| Skill | Signal | Confiance | Preuve | Amendement proposé |
|-------|--------|-----------|--------|--------------------|
| skill-X | 3 erreur récurrente | [FIABLE] | "<signature>" ×N sessions | ajouter gotcha … |
```
**Item sans preuve citée = rejeté** (pas de proposition à l'intuition). Preuve = signature d'erreur + nb de sessions, ou extrait daté.

### Étape 4 — Validation + délégation
- Raphael valide item par item. Seuls les amendements validés partent vers `skill-creator` (écriture en **append incrémental**, jamais réécriture complète d'une skill).
- **Idempotence** : ne pas re-lister comme neuf un amendement déjà proposé lors d'un run précédent — signaler « déjà proposé » (état léger si disponible).

---

## Gotchas

- **Mode friction — MCP rechargé requis** : `search_tool_events` exige `tool_events.enabled: true` dans `mcp-forge-brain/config.yaml` + kill port 8091 + nouvelle session (le handshake MCP est figé au SessionStart). Outil absent → le signaler, jamais parser les `.jsonl` à la main.
- **Mode friction ≠ `/done`** : `/done` = mono-session à chaud ; friction = récurrence cross-session. Ne pas re-surfacer les erreurs déjà capturées par `/done`.
- **Signaux friction 1 & 2 fragiles** : skill manquée + résultat corrigé = candidats à valider, jamais des certitudes (pas de vérité-terrain dans les transcripts).
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

Après chaque usage : skills repérées + scores, patterns de cross-pollination identifiés et transférés, skills déléguées à skill-creator. Pour le mode friction : signatures d'erreur récurrentes utiles + faux positifs des signaux candidats (1 & 2) à affiner.

- Sweep orienté descriptions (50 skills) : un seul script py (longueur / one-line / Gotchas / externe) couvre tout le corpus en 1 Bash call — jamais 50 lectures. 21 internes > 250 chars raccourcies via skill-creator en batch ; les externes (obsidian-*, json-canvas, defuddle) qui dépassent se SIGNALENT sans jamais être touchées.
- Le vrai risque des descriptions longues (CC ≥ 2.1.129) n'est plus la troncature à 250 mais le drop ENTIER des descriptions des skills les moins utilisées quand le listing dépasse son budget (1 % du contexte) — raccourcir tout le corpus réduit le risque pour chaque skill.
- Mode friction (RUN de vérif 15 juil.) — `search_tool_events(is_error=true)` remonte bien les vraies frictions récurrentes cross-session (schémas MCP read_section/update_property/insert_section, delegate-guard, pre-write-guards, mcp-alias-guard). MAIS l'heuristique is_error a des FAUX POSITIFS — AskUserQuestion, certains Read/search_brain sont marqués [ERROR] car le mot « error » figure dans leur contenu. Au regroupement par signature, filtrer sur le champ is_error natif quand présent + écarter les outils non-faillibles (AskUserQuestion) et les patterns « error » cosmétiques. Le signal utile (vraies erreurs récurrentes) reste dominant, mais le bruit doit être filtré avant de proposer un amendement.
