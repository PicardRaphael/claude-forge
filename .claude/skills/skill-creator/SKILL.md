---
name: skill-creator
description: ALWAYS invoke when user wants to create, edit, audit, optimize, or benchmark a Claude Code skill / SKILL.md, or asks why a skill isn't triggering. Do not hand-write SKILL.md directly — use this skill first.
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, mcp__forge-brain__*
---

# skill-creator

Crée et optimise des skills Claude Code selon la doctrine forge + workflow Anthropic officiel.
Couvre : interview → draft → evals → optimization loop → packaging.

Si besoin du détail complet de la doctrine : `mcp__forge-brain__read_note("comment-creer-skill")`.

## GATE 0 — AUDIT PROFOND OBLIGATOIRE (avant toute action, AUCUNE exception)

**L'audit est TOUJOURS profond. Jamais de raccourci, jamais de mode léger.** Que ce soit une création, une optimisation ou un audit — création triviale incluse — ces 3 étapes sont un PASSAGE OBLIGÉ avant de produire ou modifier quoi que ce soit :

1. **Lire les canoniques vault EN ENTIER** via `mcp__forge-brain__read_note("comment-creer-skill")` — SANS `max_lines`. `search_brain` seul (extraits ~10 lignes) = INSUFFISANT. Bloquant : ne rien rédiger avant.
2. **Passer SYSTÉMATIQUEMENT les 6 dimensions de `references/checklist-skill-parfaite.md`** — toutes, dans l'ordre, rien zappé. Chaque dimension cochée avec evidence (fichier:ligne + écart mesurable). C'est un GATE, pas une option de fin de fichier.
2bis. **VÉRIFIER L'ADÉQUATION DU TYPE DE COMPOSANT (création ET audit — toujours).** Un skill doit-il rester un skill ? Signaler — sans transformer d'office — si le mécanisme ne peut PAS tenir la promesse du composant :
   - Une skill est PROBABILISTE (déclenchement non garanti). Si elle promet un comportement DÉTERMINISTE (« ALWAYS bloquer », « JAMAIS laisser passer », « empêcher »), elle ment sur son mécanisme → candidate HOOK.
   - Si elle décrit surtout du contexte toujours-vrai sans procédure → candidate RULE/CLAUDE.md. Si elle a besoin d'isolation/parallélisme → candidate SUBAGENT.
   Si décalage promesse/mécanisme détecté → le signaler comme observation ARCHITECTURE dans le rapport (« devrait peut-être être un <autre type> parce que <raison> »), distincte des écarts qualité. NE JAMAIS transformer le composant sans validation explicite de Raphaël — c'est une décision d'architecture, pas une correction qualité.

3. **PUIS calibrer l'effort de création/eval à l'enjeu** : profondeur d'audit = toujours 100% ; lourdeur du process de création (evals A/B, optimization loop) = proportionnée (skill réutilisée cross-repo = process complet ; composant trivial = audit complet + création directe). Profondeur ≠ lourdeur mécanique.

Sortie du gate : un rapport d'écarts (CRITIQUE / IMPORTANT / SUGGESTION) présenté AVANT exécution. Pas d'écart mesuré = pas de modification cosmétique inutile.


## Phase 0 — Détecter le point d'entrée

Extraire depuis l'historique AVANT d'interviewer :
- Nom / objectif si mentionné → skip question 1
- Environnement cible si évident → skip question 2
- Mode : création / optimisation / audit / benchmark

Vérifier qu'une skill similaire n'existe pas :

```bash
ls .claude/skills/ ~/.claude/skills/ 2>/dev/null
```

Si similaire → STOP. Expliquer : "La skill [X] couvre déjà ce besoin. Je te recommande de la modifier/optimiser plutôt que d'en créer une nouvelle — ça évite la duplication et le drift. Tu veux qu'on parte sur ça ?"

Si le besoin décrit est en réalité un **subagent** (isolation contexte / parallélisme) ou une **rule** (comportement toujours actif) ou un **hook** (enforcement déterministe) → STOP. Dire pourquoi et proposer le bon composant avant de continuer.

---

## Phase 1 — Interview (OBLIGATOIRE — AskUserQuestion, ≤ 4 questions/round)

Les 3 rounds sont **obligatoires**. Une question peut être skippée uniquement si la réponse est déjà explicite dans l'historique de conversation — jamais supprimée par hypothèse.
Extraire d'abord depuis l'historique, puis combler les trous avec AskUserQuestion.

**Round 1 — Intent**
1. Que doit permettre cette skill ? (texte libre)
2. **Environnement cible ?** → CLI / Desktop / Cowork / Portable ← *branchement critique — détermine l'enforcement strategy*
3. Créer nouvelle ou optimiser/auditer une existante ?

**Round 2 — Déclenchement & frontières**
4. Quand déclencher (phrases exactes utilisateur) ? Quand PAS (near-misses) ?
5. Side-effects ? (deploy/commit/send/delete) → si oui : `disable-model-invocation: true` + slash-only + AskUserQuestion gate

**Round 3 — Forme & outillage**
6. SKILL.md unique ou dossier scripts+references ? (scripts si logique déterministe répétée ; references si doc > 300L)
7. Outils/MCP ? (stdio CLI/Desktop seulement ; remote HTTPS Cowork)
8. Modèle cible ? (Haiku = plus de guidance ; Opus = moins ; Sonnet défaut)
9. Evals ? (OUI obligatoire sauf skill subjective pure)

---

## Phase 2 — Recherche & edge cases

- Probing proactif : edge cases, formats IO, critères de succès, dépendances
- Ne pas écrire les test prompts avant que tout soit clarifié
- Si complexe : recherche via `mcp__forge-brain__search_brain` ou sub-agents en parallèle

---

## Phase 3 — Rédiger SKILL.md

### Frontmatter (règles absolues)

```yaml
---
name: <nom-exact-dossier-kebab-case>
description: <TRIGGER directive 3e personne — UNE SEULE LIGNE, jamais >- ni |>
user-invocable: true
allowed-tools: <liste ou mcp__server__*>
model: sonnet | opus | haiku
effort: high
disable-model-invocation: true   # si side-effects
---
```

**Description = trigger, pas résumé.** Template :
```
ALWAYS invoke when [trigger concret]. <ce que fait la skill>. DO NOT [concurrent] without invoking first.
```

Limites description (mécanisme CC ≥ 2.1.129) :
- ≤ **1024 chars** spec officielle (hard limit) ; description + `when_to_use` ≤ **1536 chars** combiné
- Viser **200-250 chars trigger-dense** : le listing a un budget (`skillListingBudgetFraction`, 1 % du contexte par défaut) — dépassé, CC **droppe des descriptions ENTIÈRES** des skills les moins utilisées (~15-25 skills confortables à 200K). Chaque char superflu augmente le risque de drop pour tout le corpus
- Matching = sémantique LLM pur (pas de keywords ni embeddings) → cross-lingue natif : une description anglaise se déclenche sur des prompts français. 1-2 phrases FR exactes max pour les formules récurrentes ; liste exhaustive entre guillemets = keyword stuffing (note vault e-descriptions-keyword-stuffing)
- Inclure near-miss exclusions ("NOT for X (use Y)")
- Pas de XML tags, pas de YAML multi-ligne (Prettier mangling casse la découverte)

### Corps SKILL.md (< 500 lignes — sinon `references/`)

```markdown
# <Nom skill>
<1-2 phrases — quand utiliser, résultat attendu>

## Étapes
1. <étape concrète>

## Gotchas  ← section la plus importante
- <piège + pourquoi>

## Apprentissage  ← OBLIGATOIRE skills métier
```

Principes :
- Voix impérative ; expliquer le *pourquoi* plutôt que ALL-CAPS MUST
- Réserver ALWAYS/NEVER aux étapes vraiment fragiles/critiques
- Chemins forward-slash uniquement ; scripts/ → préciser EXÉCUTER vs LIRE
- Critique importante : < ligne 25, jamais en bas

### Structure dossier

```
.claude/skills/<nom>/
├── SKILL.md              # < 500 lignes
├── scripts/              # opérations déterministes
└── references/           # doc longue, citée explicitement dans SKILL.md
```

### Enforcement selon environnement cible

| Cible | Ce qui marche | Ce qui NE marche PAS |
|-------|--------------|----------------------|
| **CLI** | Hooks PreToolUse/PostToolUse + description directive + CLAUDE.md routing | — |
| **Desktop** | Description directive + script-output gating + MCP local | Hooks peu fiables |
| **Cowork** | Description directive + script-output gating + remote HTTPS MCP + project Instructions | ZÉRO hooks, pas de stdio MCP, CLAUDE.md non chargé |
| **Portable** | Description directive + script-output gating uniquement | Hooks, MCP stdio |

Ne jamais émettre de hooks dans une skill ciblant Cowork.
Routing : CLAUDE.md/.claude/rules (CLI/Desktop) ou project/folder Instructions (Cowork).

---

## Phase 4 — Test cases (OBLIGATOIRE — 2–3 prompts réalistes)

Montrer à l'utilisateur pour validation → sauvegarder dans `evals/evals.json` avec assertions vides.
Ne pas avancer sans validation des test cases.

---

## Phases 5–9 — Evals A/B, grading, optimization loop (OBLIGATOIRES)

Les evals sont **obligatoires** pour toute skill. Sans mesure, pas de preuve que la skill améliore les résultats.
Voir `references/eval-workflow.md` pour le détail complet des phases 5–9.

Résumé :
- Spawner simultanément `with_skill` + `baseline` via Task tool
- Générer le eval viewer AVANT de juger (`--static` sur Cowork/headless)
- Grader → agréger → analyser → lire `feedback.json` → améliorer → recommencer
- Améliorer : généraliser (éviter overfitting), garder lean, expliquer le pourquoi, bundler le répété
- Seule exception : skill de connaissance pure subjective → éval qualitative uniquement

---

## Phase 10 — Description optimization loop

Générer ~20 trigger queries (8–10 should-fire, 8–10 near-miss should-NOT-fire — substantielles, pas one-step).
Split 60/40 train/held-out, 3 runs/query, max 5 itérations → sélectionner `best_description` sur score test.

---

## Phase 11 — Packaging & distribution

- `.skill` si distribution individuelle ; plugin si distribution équipe
- Emplacement : `.claude/skills/` (projet) / `~/.claude/skills/` (user) / plugin-bundled
- Cowork : enregistrer via UI, garder actif < 30
- Conserver le nom à l'update (jamais `-v2`)

---

## Checklist avant livraison (cocher à voix haute, point par point)

- [ ] **3 rounds d'interview complétés** (ou questions skippées car réponse explicite dans le contexte)
- [ ] **Test cases validés** par l'utilisateur avant les runs
- [ ] `description` UNE SEULE LIGNE anglais — jamais `>-` ni `|`
- [ ] `name` = nom exact du dossier kebab-case
- [ ] Description **directive** : ALWAYS invoke when… / DO NOT … without invoking first
- [ ] Near-miss exclusions dans la description
- [ ] Pas de XML tags dans la description
- [ ] SKILL.md < 500 lignes (sinon `references/`)
- [ ] Pas de `README.md` dans le dossier
- [ ] Section **Gotchas** présente
- [ ] Section **Apprentissage** présente (skills métier)
- [ ] **Zéro méta-commentaire de modification dans le body** : pas de date d'audit, pas de justification de la modif (« cause racine… », « audit du X »), pas de narration — la règle s'écrit nue ; le pourquoi vit dans le CHANGELOG du repo cible ou le vault
- [ ] Pas de `$ARGUMENTS` dans des backticks shell
- [ ] Enforcement adapté à l'environnement (pas de hooks si Cowork/Portable)
- [ ] Side-effects → `disable-model-invocation: true` + AskUserQuestion gate
- [ ] 10+ skills dans le projet → vérifier budget avec `/doctor`
- [ ] Pas de BOM UTF-8 (PowerShell Out-File → toujours UTF-8 sans BOM)
- [ ] **Evals lancés** : test cases validés + runs with_skill/baseline + eval viewer généré
- [ ] **Description optimization loop** : ~20 trigger queries testées, best_description sélectionnée sur score test

---

## Mode optimisation / audit (skill existante)

Voir `references/checklist-skill-parfaite.md` — 6 dimensions complètes.

Priorités audit rapide :
1. Description passive ou > 1024 chars ?
2. SKILL.md > 500 lignes sans `references/` ?
3. Gotchas présente ?
4. Apprentissage présente (skills métier) ?
5. Near-miss exclusions dans la description ?
6. YAML multi-ligne ?
7. ALL-CAPS excessif (> 2-3 = bruit) ?
8. References mortes ou chaînes > 1 niveau ?
9. Assertions non-discriminantes dans les evals ?
10. Skill flat-file qui devrait être un dossier ?

---

## Gotchas

- **BOM UTF-8** (PowerShell `Out-File`/`Set-Content`) → frontmatter YAML cassé silencieusement → skill non chargée ou "plugin validation failed". UTF-8 sans BOM. Vérifier : 3 premiers octets ≠ `239 187 191`
- **`$ARGUMENTS` dans backticks** → substitution littérale casse le quoting (Windows)
- **`context: fork` / `agent:`** ignorés si invoqués via Skill tool → utiliser Task tool explicite
- **AskUserQuestion** non disponible en sub-agent → ESCALADE vers session principale (dispo ici car skill = thread principal)
- **Hot reload** : redémarrer la session pour prise en compte
- **Skills orphelines** dans frontmatter agent sans référence dans le body → jamais activées
- **Plugin force le préfixe** `/<plugin>:<skill>` → pour slash command sans préfixe, distribuer comme compétence individuelle
- **Collision descriptions** → ajouter "Use this for X, NOT for Y"
- **Queries one-step** ne déclenchent aucune skill → evals trigger = prompts substantiels

---

## Apprentissage

Après chaque création ou optimisation : noter ici les patterns efficaces et gotchas rencontrés.

- Batch multi-skills : le delegate-guard accepte une invocation `Skill(skill-creator)` dans la fenêtre du transcript (80 lignes) même quand l'estampille `attributionSkill` reste sur la première skill du tour (empilement CC ≥ 2.1.202). Sur un batch très long, si un Edit est bloqué : ré-invoquer skill-creator. Jamais de contournement par script.
- Raccourcir une description = vérifier les longueurs des drafts par script AVANT d'éditer, préserver 1-2 triggers FR exacts + identifiants de domaine (langue-neutres), et garder les clauses NOT-for qui désambiguïsent les skills voisines.

---

## Références

- `references/checklist-skill-parfaite.md` — checklist 6 dimensions complète
- `references/eval-workflow.md` — phases 5–9 détail complet (evals A/B, grading, optimization)
- `mcp__forge-brain__read_note("comment-creer-skill")` — doctrine forge canonique complète
- `mcp__forge-brain__read_note("cowork-skills-reliability")` — matrice enforcement CLI/Desktop/Cowork
