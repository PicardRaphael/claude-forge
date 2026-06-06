---
name: claudemd-creator
description: ALWAYS invoke when user wants to create, audit, improve, or optimize a CLAUDE.md. Do not hand-write CLAUDE.md directly — use this skill first. Delegate-guard still blocks direct edits.
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, mcp__forge-brain__*
---

# claudemd-creator

Crée et optimise des CLAUDE.md selon la doctrine forge + référence Anthropic officielle.
Couvre : décision → audit → optimisation → création → livraison.

Si besoin du détail complet de la doctrine : `mcp__forge-brain__read_note("comment-ecrire-claudemd")`.

## GATE 0 — AUDIT PROFOND OBLIGATOIRE (avant toute action, AUCUNE exception)

**L'audit est TOUJOURS profond. Jamais de raccourci, jamais de mode léger.** Que ce soit une création, une optimisation ou un audit — création triviale incluse — ces 3 étapes sont un PASSAGE OBLIGÉ avant de produire ou modifier quoi que ce soit :

1. **Lire les canoniques vault EN ENTIER** via `mcp__forge-brain__read_note("comment-ecrire-claudemd")` — SANS `max_lines`. `search_brain` seul (extraits ~10 lignes) = INSUFFISANT. Bloquant : ne rien rédiger avant.
2. **Passer SYSTÉMATIQUEMENT les 4 dimensions de `references/checklist-claudemd-parfait.md`** — toutes, dans l'ordre, rien zappé. Chaque dimension cochée avec evidence (fichier:ligne + écart mesurable). C'est un GATE, pas une option de fin de fichier.
2bis. **VÉRIFIER L'ADÉQUATION DU TYPE DE COMPOSANT (création ET audit — toujours).** Un CLAUDE.md doit-il rester un CLAUDE.md ? Signaler — sans transformer d'office — si le mécanisme ne peut PAS tenir la promesse du composant :
   - Un CLAUDE.md est du contexte PROBABILISTE (~80% compliance). S'il contient un comportement à GARANTIR (« toujours », « jamais ») → candidate HOOK (seul déterministe).
   - S'il contient un workflow multi-étapes réutilisable → candidate SKILL. Si c'est du détail par-sujet → candidate RULE .claude/rules/.
   Si décalage promesse/mécanisme détecté → le signaler comme observation ARCHITECTURE dans le rapport (« devrait peut-être être un <autre type> parce que <raison> »), distincte des écarts qualité. NE JAMAIS transformer le composant sans validation explicite de Raphaël — c'est une décision d'architecture, pas une correction qualité.

3. **PUIS calibrer l'effort de création/eval à l'enjeu** : profondeur d'audit = toujours 100% ; lourdeur du process de création (evals A/B, optimization loop) = proportionnée (skill réutilisée cross-repo = process complet ; composant trivial = audit complet + création directe). Profondeur ≠ lourdeur mécanique.

Sortie du gate : un rapport d'écarts (CRITIQUE / IMPORTANT / SUGGESTION) présenté AVANT exécution. Pas d'écart mesuré = pas de modification cosmétique inutile.


> ⚠️ **`delegate-guard.py` bloque toujours les edits directs de `CLAUDE.md`** — c'est la seule protection qui reste. Cette skill contourne légitimement la protection : invoquée depuis la session principale (thread principal), les edits passent. Ne jamais bypasser le hook autrement.

## Phase 0 — Test préliminaire : est-ce vraiment un CLAUDE.md ?

**Avant tout** — identifier ce qui est vraiment demandé :

- **Contexte/conventions courts et stables, toujours-vrais** → CLAUDE.md ✅ continuer
- **Workflow multi-étapes réutilisable** → STOP. Expliquer : "Ce que tu décris est une **skill** — une procédure invocable à la demande, pas du contexte permanent. Je te recommande `skill-creator` parce que ça sera plus fiable et moins de bruit à chaque session. Tu veux partir sur ça ?"
- **Comportement déterministe à garantir** → STOP. Expliquer : "Ce que tu décris est un **hook** — le seul mécanisme garanti à 100%. Un CLAUDE.md ne force rien, c'est probabiliste. Je te recommande `hook-creator`. Tu veux partir sur ça ?"
- **Contenu folder-specific** → proposer un CLAUDE.md imbriqué ou `@import` plutôt que d'alourdir le racine

Vérifier qu'un CLAUDE.md existe déjà :
```bash
cat CLAUDE.md 2>/dev/null | wc -l
ls .claude/rules/ 2>/dev/null
```
Si existant → proposer **audit + optimisation** plutôt que réécriture complète.

---

## Phase 1 — Interview (OBLIGATOIRE — AskUserQuestion, ≤ 4 questions/round)

Les 2 rounds sont **obligatoires**. Skip uniquement si réponse explicite dans le contexte.

**Round 1 — Contexte & mode**
1. Quel repo / projet ? (stack, langages, frameworks — pour les commandes)
2. Mode : créer un nouveau CLAUDE.md, auditer l'existant, ou optimiser l'existant ?
3. Y a-t-il déjà des `.claude/rules/`, skills, agents, hooks ? (pour le routing et la modularisation)

**Round 2 — Contenu & contraintes**
4. Quelles sont les règles issues d'erreurs réelles du projet ? (le contenu le plus précieux)
5. Y a-t-il des règles « obligatoires » à garantir ? → si oui : rediriger vers hook plutôt que CLAUDE.md
6. Target : < 200 lignes orchestrateur, ou contrainte différente ?

---

## Phase 2 — Découverte du projet (mode création)

```bash
cat package.json 2>/dev/null | head -30
cat pyproject.toml 2>/dev/null | head -30
ls -la .claude/ 2>/dev/null
git log --oneline -5 2>/dev/null
wc -l CLAUDE.md 2>/dev/null
```

Identifier :
- Stack + langages + frameworks (ce que Claude ne déduit pas du code)
- Commandes exactes (dev, test, typecheck, build)
- Skills/agents existants → routing à inclure
- Rules existantes → ne pas dupliquer dans CLAUDE.md

---

## Phase 3 — Mode AUDIT (CLAUDE.md existant)

### Procédure d'audit en 5 étapes

1. `wc -l CLAUDE.md` + lister `.claude/rules/`, `.claude/skills/`, `.claude/agents/`
2. Classer chaque bloc : **garder** / **réécrire-testable** / **déplacer** (rule/skill/hook/import) / **supprimer**
3. Détecter contradictions et doublons (CLAUDE.md ↔ rules ↔ skills)
4. Vérifier le routing : chaque skill/agent important est-il pointé ?
5. Produire rapport priorisé : **CRITIQUE** / **IMPORTANT** / **SUGGESTION** avec correctif par item

### Signaux de maladie à détecter

| Signal | Correctif |
|--------|-----------|
| > 200 lignes | Élaguer agressivement |
| Règles aspirationnelles (« sois cohérent ») | Réécrire en testable + raison |
| Règles sans raison | Ajouter le « parce que » |
| Règles contradictoires | Consolider |
| Contenu que Claude sait déjà | Supprimer |
| Détail folder-specific dans le racine | CLAUDE.md imbriqué ou `@import` |
| Workflows multi-étapes inline | Extraire en skill |
| Comportements « obligatoires » en texte | Migrer vers hook |
| Contenu skill/agent dupliqué | Pointer, pas dupliquer |
| `@import` récursifs | Aplatir à 1 niveau |
| Pas d'owner / cadence | Instaurer revue trimestrielle |

---

## Phase 4 — Mode OPTIMISATION (5 passes successives)

**Passe 1 — Élaguer.** Supprime l'évident, le daté, les doublons. Déplace les 3 sections les plus survolées vers sous-docs ; remplace par 1 ligne + lien.

**Passe 2 — Réécrire en testable.** Chaque règle aspirationnelle → règle spécifique vérifiable + raison. La raison = ce qui permet à Claude de généraliser.

**Passe 3 — Déplacer au bon mécanisme.** Workflows → skills ; comportements obligatoires → hooks ; détail par sujet → `.claude/rules/` ; folder-specific → CLAUDE.md imbriqué.

**Passe 4 — Modulariser.** Monolithe → orchestrateur : maître court + `@import`/rules chargés par pertinence.

**Passe 5 — Cadence.** Owner unique, revue trimestrielle, entrées datées.

---

## Phase 5 — Rédiger le CLAUDE.md

### Squelette orchestrateur type (< 200 lignes)

```markdown
# <Projet> — Contexte Claude Code

**Créé :** YYYY-MM-DD | **Version :** X.Y

## Stack (3-6 lignes)
- Runtime / Language / Framework / Tests / Linter

## Commandes essentielles
- dev : `...`
- test : `...`
- typecheck : `...`

## Conventions critiques (testables + raison)
- <règle> — parce que <raison empirique>

## Anti-patterns
- <ne fais pas X> — <coût observé>

## Routing
- Tâche X → Skill(`nom`)
- Règles détaillées : @.claude/rules/

## Ce qu'il NE faut PAS faire
- Éditer CLAUDE.md directement (hook bloque) → invoquer `claudemd-creator`
```

### Règles de contenu

**Y va ✅**
- Stack et pattern d'archi que Claude ne peut pas déduire du code
- Commandes exactes (copy-paste ready)
- Conventions critiques testables avec raison
- Anti-patterns (« ne fais pas X »)
- Routing vers skills/agents/rules

**N'y va PAS ❌**
- Ce que Claude sait déjà (« écris du code propre »)
- Détail folder-specific → CLAUDE.md imbriqué ou `@import`
- Workflows multi-étapes → skill
- Comportements à garantir → hook
- Contenu d'une skill/agent dupliqué
- Info datée non voulue

### La règle testable (clé de l'adhérence)

| ❌ Aspirationnel (invisible) | ✅ Testable (appliqué) |
|---|---|
| « Sois cohérent » | « Utilise les server components par défaut — 3 crashes runtime en janvier causés par 'use client' mal placé » |
| « Gère bien les types » | « `unknown` pas `any` — parce que les `any` ont causé 2 bugs prod non détectés par TS » |

La **raison** est ce qui permet à Claude de généraliser — sans elle, il ne sait pas quand plier la règle.

---

## Phase 6 — Vérification (test en session fraîche)

Un CLAUDE.md ne se teste PAS comme une skill (pas de cycle A/B lourd — ce serait du sur-process, cf doctrine : modification CLAUDE.md = pas de gate systématique). La vérification se fait en session fraîche.

- Tester en session fraîche : Claude suit-il les règles sans être rappelé ?
- Vérifier `wc -l CLAUDE.md` < 200
- Tester le routing : Claude dispatch-il vers les bonnes skills/agents ?
- Si une règle est ignorée → elle est trop longue, trop vague, ou devrait être un hook

---

## Checklist avant livraison (OBLIGATOIRE — cocher à voix haute)

**Process**
- [ ] Phase 0 passée : c'est bien un CLAUDE.md (pas une skill/hook/rule)
- [ ] 2 rounds d'interview complétés
- [ ] Mode identifié : création / audit / optimisation

**Taille & structure**
- [ ] < 200 lignes, scannable en 90 s
- [ ] Orchestrateur (maître court + imports/rules), pas monolithe
- [ ] `@import` à 1 niveau max
- [ ] Hiérarchie planifiée si monorepo/multi-équipes

**Contenu**
- [ ] Uniquement ce que Claude ne déduit pas du code
- [ ] Commandes présentes et exactes
- [ ] Chaque règle testable + raison
- [ ] Section anti-patterns présente
- [ ] Routing vers skills/agents/rules
- [ ] Zéro contenu que Claude sait déjà
- [ ] Zéro workflow multi-étapes inline (→ skill)
- [ ] Zéro comportement « obligatoire » en texte (→ hook)
- [ ] Zéro duplication de contenu skill/agent

**Cohérence & enforcement**
- [ ] Aucune règle contradictoire
- [ ] Une règle = un seul endroit, au bon mécanisme
- [ ] Le critique-à-garantir est en hook, pas en texte

**Maintenance**
- [ ] Owner désigné
- [ ] Cadence de revue (trimestrielle)

**Evals**
- [ ] Testé en session fraîche : règles suivies ?
- [ ] `wc -l` < 200

---

## Gotchas

- **CLAUDE.md ne force rien** — texte interprété = probabiliste (~80% compliance max). Ce qui doit être garanti → hook
- **> 200 lignes = adhérence silencieuse effondrement** — « la raison n°1 pour laquelle Claude a arrêté de suivre tes règles »
- **Compaction** : sur longue session, le contenu peut être résumé/abandonné → garder court
- **@import circulaire** → boucle ; vérifier l'arbre
- **Règle aspirationnelle = invisible** — sans condition testable et raison, Claude ne sait pas quand l'appliquer
- **delegate-guard.py protège CLAUDE.md** — edit direct bloqué (exit 2) ; seule la skill claudemd-creator (thread principal) passe
- **AGENTS.md** : standard ouvert cross-outils ; beaucoup font un symlink `AGENTS.md` → `CLAUDE.md`
- **`/init`** génère un CLAUDE.md de départ — point de départ à élaguer, pas un livrable final
- **Mise à jour mid-session** : Claude ne recharge pas CLAUDE.md en cours de session → nouvelle session pour prise en compte

---

## Apprentissage

Après chaque création ou optimisation : noter ici les patterns efficaces et gotchas rencontrés.

---

## Références

- `references/checklist-claudemd-parfait.md` — 4 dimensions complètes
- `mcp__forge-brain__read_note("comment-ecrire-claudemd")` — doctrine forge canonique complète
- `mcp__forge-brain__read_note("raisonnement-22mai-doctrine-vs-enforcement")` — pourquoi workflow hors CLAUDE.md
