---
type: reference
domaine: claude-code
sujet: claude-md
mis_a_jour: 2026-06-06
tags: [claude-code, claude-md, rules, skills, agents, hooks, audit, optimisation, contexte]
---

# Référence — Analyser / Créer / Optimiser un CLAUDE.md parfait

> Méthode générique applicable à n'importe quel repo contenant agents + skills + hooks + rules. Pour le CLI. Orienté fiabilité et économie de contexte. À utiliser par Jarvis pour auditer et améliorer les CLAUDE.md des autres repos.

## TL;DR

- **Le CLAUDE.md n'est PAS une doc, c'est un budget de contexte.** Il est lu EN ENTIER au début de chaque session, avant que Claude écrive une ligne. Chaque ligne inutile dilue les instructions qui comptent. Cible : **< 200 lignes, scannable en 90 secondes.**
- **Le CLAUDE.md est un ORCHESTRATEUR, pas un entrepôt.** Il contient les essentiels toujours-vrais + des pointeurs (`@import` / renvois vers `.claude/rules/`, skills, agents). Un CLAUDE.md « orchestrateur » bat un monolithe **à nombre de lignes égal** — le modèle gère mieux un petit contexte lié que de gros blocs inline.
- **Une règle vit à UN seul endroit, au bon mécanisme.** Style/conventions → CLAUDE.md ou rules. Workflow réutilisable → skill. Comportement obligatoire déterministe → hook. Routing → CLAUDE.md/rules (pointeur). Dupliquer = diluer + diverger.
- **Le CLAUDE.md ne FORCE rien.** C'est du texte interprété (probabiliste). Pour garantir → hook. « Une règle aspirationnelle est invisible ; une règle testable est appliquée. »

---

## PARTIE 1 — Ce qu'est vraiment un CLAUDE.md (le modèle mental)

Au démarrage, Claude Code remonte l'arbre des répertoires depuis le cwd vers la racine et **concatène** tous les CLAUDE.md rencontrés (pas de fusion avec règles de priorité, pas de filtrage). Tout fichier découvert contribue au jeu d'instructions actif.

Trois conséquences directes :

1. **Coût permanent.** Tout est chargé à chaque session. Un CLAUDE.md de 400 lignes = des tokens consommés et du bruit qui dilue avant même la première action.
2. **Probabiliste.** C'est un message d'instructions, pas une config imposée. Claude juge la pertinence et peut sauter. Pour bloquer une action quoi qu'il arrive → hook PreToolUse, jamais une ligne de CLAUDE.md.
3. **Effet de position douce.** En cas de conflit, le fichier le plus spécifique / lu en dernier (le plus proche du cwd) pèse davantage — mais c'est un poids mou, pas un override strict. D'où : **des règles claires et non-contradictoires comptent plus que de compter sur l'ordre de chargement.**

> Le signe d'un CLAUDE.md malade : « un fichier mémoire qui a cessé d'être lu. Le modèle est le seul à le savoir. »

---

## PARTIE 2 — La hiérarchie (où vivent les CLAUDE.md)

| Niveau | Emplacement | Portée |
|---|---|---|
| Global / user | `~/.claude/CLAUDE.md` | Tous les projets de la machine |
| Projet | `<repo>/CLAUDE.md` | Le repo (committable) |
| Sous-dossier | `<repo>/sous/dossier/CLAUDE.md` | Les fichiers de ce dossier |
| Local (gitignored) | `CLAUDE.local.md` | **Déprécié** → utiliser `@import` |

**Précédence (poids douce)** : le plus spécifique l'emporte. Sous-dossier > projet > global, pour ce qui touche au contexte courant. Principe de spécificité : l'instruction la plus proche du contexte de travail pèse le plus.

**Règle d'architecture** : dans un monorepo / multi-équipe, planifie la hiérarchie explicitement (sections folder-specific dans des CLAUDE.md imbriqués) plutôt que laisser les conflits apparaître par accident.

---

## PARTIE 3 — Le modèle ORCHESTRATEUR (la structure cible)

Le CLAUDE.md racine doit être **scannable en 90 secondes**. Tout ce qui est détaillé ou folder-specific descend d'un cran.

### Les trois leviers de modularisation

1. **`@import`** — `@path/to/file.md` tire le contenu quand pertinent. Garde le fichier maître léger. Récursif (à utiliser avec parcimonie — pas de labyrinthe de renvois). Exemples : `See @docs/api-patterns.md for API conventions`, `See @package.json for npm scripts`.
2. **`.claude/rules/*.md`** — instructions modulaires auto-chargées chaque session, même priorité que CLAUDE.md. Pour décomposer un gros CLAUDE.md par sujet. `paths:` (quoté) pour scoper par type de fichier.
3. **Skills / agents** — le CLAUDE.md ne décrit pas leur contenu, il pointe juste le routing (« pour X, utilise le skill Y »).

### Squelette type d'un CLAUDE.md orchestrateur

```markdown
# <Projet> — Contexte Claude Code

## Stack & architecture (3-6 lignes max)
<langages, frameworks, pattern d'archi — ce que Claude ne peut PAS déduire du code>

## Commandes
- dev : `...`
- test : `...`   (préférer les tests ciblés, pas toute la suite)
- typecheck : `...`

## Conventions critiques (avec raison)
- <règle testable> — parce que <raison>
- ...

## Ce qu'il NE faut PAS faire
- <anti-pattern> — <coût>

## Routing (quel mécanisme quand)
- Tâche <X> → skill `<nom>`
- Sous-tâche lourde isolée → agent `<nom>`
- Règles détaillées : voir @.claude/rules/

## Détails déportés
- API : @docs/api-patterns.md
- Tests : @docs/testing.md
```

> Un orchestrateur (maître + sous-fichiers chargés par pertinence) bat le monolithe **même à nombre total de lignes identique**, et reste bien plus facile à maintenir à jour sur un trimestre.

---

## PARTIE 4 — Ce qui va dans le CLAUDE.md (et ce qui n'y va PAS)

### Y va ✅
- La stack et le pattern d'architecture que Claude ne peut pas déduire du code
- Les commandes (dev, test, typecheck, build)
- Les conventions critiques **testables et avec raison**
- Les anti-patterns (« ne fais pas X »)
- Le routing vers skills/agents/rules
- Les décisions d'archi importantes (ou pointeur vers les ADR)

### N'y va PAS ❌
- **Ce que Claude sait déjà** (« écris du code propre », « gère les erreurs ») — énoncer l'évident dilue.
- **Le détail folder-specific** → CLAUDE.md imbriqué ou `@import`.
- **Les workflows multi-étapes réutilisables** → skill.
- **Les comportements à garantir** → hook (le CLAUDE.md ne force rien).
- **Le contenu d'une skill/agent** → ça vit dans la skill/agent, pas dupliqué ici.
- **L'info datée** (« migré vers tRPC le 20/01 ») — sauf une courte section « Recent changes » datée si tu y tiens.

### La règle testable (clé de l'adhérence)
| ❌ Aspirationnel (invisible) | ✅ Testable (appliqué) |
|---|---|
| « Sois cohérent » | « Utilise les server components par défaut ; n'ajoute 'use client' que pour les forms/UI interactive » |
| « Gère bien les types » | « Utilise `unknown` pas `any` — parce qu'on a eu 3 crashes runtime d'API typées `any` le trimestre dernier » |

La **raison** est ce qui permet à Claude de généraliser : sans elle, il ne sait pas quand plier la règle.

---

## PARTIE 5 — CLAUDE.md vs rules vs skills vs agents vs hooks

Le cadre de décision complet (le CLAUDE.md est le chef d'orchestre, pas l'exécutant) :

| Tu veux… | Mécanisme | Garantie |
|---|---|---|
| Contexte/conventions toujours vrais, courts, stables | **CLAUDE.md** | Probabiliste |
| Instructions modulaires par sujet/chemin | **`.claude/rules/`** | Probabiliste |
| Workflow réutilisable invocable à la demande | **Skill** | Probabiliste (activation) |
| Sous-tâche lourde isolée / parallèle | **Agent** | — |
| Comportement OBLIGATOIRE déterministe | **Hook (exit 2)** | **Garanti** |
| Routing (quel skill/agent quand) | **CLAUDE.md / rules** (pointeur) | Probabiliste → doubler d'un hook si critique |

**Doctrine officielle** : « CLAUDE.md pour le style, hooks pour les règles dures, skills pour les jobs multi-étapes répétés. »

Note : `commands/` est fusionné dans `skills/`. Si un skill et une commande partagent un nom, le **skill** gagne. Repo neuf → que des skills.

---

## PARTIE 6 — Les budgets et les pièges de contexte

- **Limite pratique : ~200 lignes.** Au-delà, l'adhérence s'effondre silencieusement (« la raison n°1 pour laquelle Claude a 'arrêté de suivre' tes règles, c'est que le fichier a grossi »). `wc -l CLAUDE.md` > 200 → élaguer.
- **Compaction** : sur une longue session, le contenu du CLAUDE.md peut être résumé/abandonné. Garde-le court pour qu'il survive.
- **AGENTS.md** : standard ouvert cross-outils ; beaucoup font un symlink `AGENTS.md` → `CLAUDE.md`.
- **`/init`** : génère un CLAUDE.md de départ depuis l'analyse du repo (build, tests, patterns). Point de départ, à élaguer ensuite.

---

## PARTIE 7 — MODE AUDIT (analyser un CLAUDE.md existant)

Ce que Jarvis doit détecter en auditant un repo. Chaque point = un signal + un correctif.

### Signaux de maladie
- [ ] **> 200 lignes** (`wc -l`) → bloat, élaguer agressivement
- [ ] **Lecture > 90 s** → trop long
- [ ] **Règles aspirationnelles** (« sois cohérent ») → réécrire en testable
- [ ] **Règles sans raison** → ajouter le « parce que »
- [ ] **Règles contradictoires** (accumulées par couches) → consolider
- [ ] **Contenu que Claude sait déjà** → supprimer
- [ ] **Détail folder-specific dans le racine** → descendre en CLAUDE.md imbriqué / `@import`
- [ ] **Workflows multi-étapes inline** → extraire en skill
- [ ] **Comportements « obligatoires » en texte** → migrer vers hook
- [ ] **Contenu de skill/agent dupliqué** → pointer, pas dupliquer
- [ ] **Info datée / obsolète** → supprimer (sauf section datée volontaire)
- [ ] **Monolithe** alors qu'un orchestrateur serait mieux → modulariser
- [ ] **Labyrinthe de `@import` récursifs** → aplatir à 1 niveau
- [ ] **Pas d'owner / pas de cadence de revue** → instaurer revue trimestrielle

### Procédure d'audit (Jarvis)
1. `wc -l CLAUDE.md` + lister `.claude/rules/`, `.claude/skills/`, `.claude/agents/`, hooks.
2. Classer chaque bloc du CLAUDE.md : garder / réécrire-testable / déplacer (rule/skill/hook/import) / supprimer.
3. Détecter les contradictions et les doublons (CLAUDE.md ↔ rules ↔ skills).
4. Vérifier le routing : chaque skill/agent important est-il pointé ?
5. Produire un rapport priorisé : CRITIQUE / IMPORTANT / SUGGESTION, avec le correctif par item.

---

## PARTIE 8 — MODE OPTIMISATION (la passe de compression)

Méthode en passes successives (inspirée des audits terrain 2026) :

**Passe 1 — Élaguer.** Supprime l'évident, le daté, les doublons. Déplace les 3 sections les plus « survolées » vers des sous-docs liés ; remplace par une ligne de résumé + le lien.

**Passe 2 — Réécrire en testable.** Chaque règle aspirationnelle → règle spécifique vérifiable, avec sa raison.

**Passe 3 — Déplacer au bon mécanisme.** Workflows → skills ; comportements obligatoires → hooks ; détail par sujet → `.claude/rules/` ; folder-specific → CLAUDE.md imbriqué.

**Passe 4 — Modulariser.** Passe du monolithe à l'orchestrateur : maître court + `@import`/rules chargés par pertinence.

**Passe 5 — Cadence.** Owner unique, revue trimestrielle, entrées datées. Sans cadence, l'élagage est défait en deux sprints.

> Objectif final : root file scannable en 90 s, < 200 lignes, zéro contradiction, chaque règle testable avec raison, tout le reste déporté.

---

## PARTIE 9 — Checklist d'un CLAUDE.md parfait

**Taille & structure**
- [ ] < 200 lignes, scannable en 90 s
- [ ] Orchestrateur (maître court + imports/rules), pas monolithe
- [ ] `@import` à 1 niveau, pas de labyrinthe
- [ ] Hiérarchie planifiée (racine vs sous-dossiers)

**Contenu**
- [ ] Uniquement ce que Claude ne déduit pas du code
- [ ] Commandes présentes (dev/test/typecheck)
- [ ] Chaque règle est testable + a une raison
- [ ] Section anti-patterns (« ne fais pas »)
- [ ] Routing vers skills/agents/rules
- [ ] Zéro contenu que Claude sait déjà
- [ ] Zéro workflow multi-étapes inline (→ skill)
- [ ] Zéro comportement « obligatoire » qui devrait être un hook
- [ ] Zéro info datée non voulue
- [ ] Zéro duplication de contenu skill/agent

**Cohérence & enforcement**
- [ ] Aucune règle contradictoire
- [ ] Une règle = un seul endroit, au bon mécanisme
- [ ] Le critique-à-garantir est en hook, pas en texte
- [ ] Routing critique doublé d'un hook si nécessaire

**Maintenance**
- [ ] Owner unique désigné
- [ ] Cadence de revue (trimestrielle)
- [ ] Versionné, relu en PR, re-testé en session fraîche

---

## La vérité dure

1. **Le CLAUDE.md est un budget, pas une doc.** Chaque ligne inutile coûte des tokens à chaque session et dilue ce qui compte. Court > exhaustif.
2. **Il ne force rien.** Texte interprété = probabiliste. Ce qui doit être garanti va dans un hook.
3. **Orchestrateur > monolithe**, même à lignes égales. Le modèle gère mieux du petit contexte lié.
4. **Une règle vit à un seul endroit, au bon mécanisme.** Dupliquer entre CLAUDE.md / rules / skill = diluer et diverger.
5. **Sans owner ni cadence, tout CLAUDE.md pourrit** : il gonfle, se contredit, et cesse d'être suivi sans que personne ne le voie.
