---
name: subagent-creator
description: ALWAYS invoke when user wants to create, edit, audit, or optimize a Claude Code subagent / agent .md file. Do not hand-write agents/*.md directly — use this skill first.
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, mcp__forge-brain__search_brain, mcp__forge-brain__read_note, mcp__forge-brain__read_note_by_path, mcp__forge-brain__read_section, mcp__forge-brain__list_notes
---

# subagent-creator

Crée et optimise des subagents Claude Code selon la doctrine forge + reference Anthropic officielle.
Couvre : décision créer/PAS → interview → draft → evals → livraison.

Si besoin du détail complet de la doctrine : `mcp__forge-brain__read_note("comment-creer-agent")`.

## GATE 0 — AUDIT PROFOND OBLIGATOIRE (avant toute action, AUCUNE exception)

**L'audit est TOUJOURS profond. Jamais de raccourci, jamais de mode léger.** Que ce soit une création, une optimisation ou un audit — création triviale incluse — ces 3 étapes sont un PASSAGE OBLIGÉ avant de produire ou modifier quoi que ce soit :

1. **Lire les canoniques vault EN ENTIER** via `mcp__forge-brain__read_note("comment-creer-agent")` — SANS `max_lines`. `search_brain` seul (extraits ~10 lignes) = INSUFFISANT. Bloquant : ne rien rédiger avant.
2. **Passer SYSTÉMATIQUEMENT les 5 dimensions de `references/checklist-agent-parfait.md`** — toutes, dans l'ordre, rien zappé. Chaque dimension cochée avec evidence (fichier:ligne + écart mesurable). C'est un GATE, pas une option de fin de fichier.
2bis. **VÉRIFIER L'ADÉQUATION DU TYPE DE COMPOSANT (création ET audit — toujours).** Un subagent doit-il rester un subagent ? Signaler — sans transformer d'office — si le mécanisme ne peut PAS tenir la promesse du composant :
   - Un subagent ne peut PAS poser de questions (AskUserQuestion filtré) ni utiliser le MCP de façon fiable. S'il promet de l'interactif ou un accès vault garanti → mauvais type, candidate SKILL thread principal.
   - S'il doit garantir un comportement déterministe → candidate HOOK. Si c'est une procédure invocable sans isolation → candidate SKILL.
   Si décalage promesse/mécanisme détecté → le signaler comme observation ARCHITECTURE dans le rapport (« devrait peut-être être un <autre type> parce que <raison> »), distincte des écarts qualité. NE JAMAIS transformer le composant sans validation explicite de Raphaël — c'est une décision d'architecture, pas une correction qualité.

3. **PUIS calibrer l'effort de création/eval à l'enjeu** : profondeur d'audit = toujours 100% ; lourdeur du process de création (evals A/B, optimization loop) = proportionnée (skill réutilisée cross-repo = process complet ; composant trivial = audit complet + création directe). Profondeur ≠ lourdeur mécanique.

Sortie du gate : un rapport d'écarts (CRITIQUE / IMPORTANT / SUGGESTION) présenté AVANT exécution. Pas d'écart mesuré = pas de modification cosmétique inutile.


## Phase 0 — Test préliminaire : faut-il vraiment un subagent ?

**Avant tout** — répondre à cette question :

> « Est-ce que cette tâche a besoin d'un contexte frais isolé OU de tourner en parallèle, ET n'a pas besoin de poser des questions ni du contexte de la conversation ? »

- **OUI** → continuer
- **NON** → STOP. Expliquer à l'utilisateur pourquoi un subagent n'est pas le bon outil et proposer l'alternative : "Tu m'as demandé un agent, mais ce que tu décris est [une procédure réutilisable → skill / un comportement toujours actif → rule / un enforcement déterministe → hook]. Je te recommande X parce que Y. Tu veux qu'on parte sur ça plutôt ?"

Un subagent résout exactement deux problèmes : **isolation de contexte** + **parallélisme**. Pas "faire propre", pas "organiser".

**Cas bloquants — NE PAS créer de subagent si :**
- La tâche doit poser des questions → `AskUserQuestion` filtré en subagent (issues #12890 #18721 #20275)
- La tâche a besoin du contexte de conversation → subagent démarre vierge
- La tâche a besoin du MCP vault de façon fiable → MCP non garanti en subagent (`No such tool available`)
- Comportement déterministe obligatoire → hook, pas subagent
- Workers qui communiquent entre eux → Agent Teams, pas subagents

Vérifier qu'un agent similaire n'existe pas :
```bash
ls .claude/agents/ ~/.claude/agents/ 2>/dev/null
```
Si similaire → proposer de modifier/optimiser plutôt que recréer.

---

## Phase 1 — Interview (OBLIGATOIRE — AskUserQuestion, ≤ 4 questions/round)

Les 3 rounds sont **obligatoires**. Skip uniquement si la réponse est explicite dans le contexte.
Extraire d'abord depuis l'historique, puis combler avec AskUserQuestion.

**Round 1 — Intent & décision**
1. Objectif et résultat attendu de l'agent
2. Déclencheur auto (quand CC doit-il le dispatcher ?) + input du prompt d'invocation
3. Confirmation : isolation de contexte OU parallélisme ? (sinon → skill/rule proposée)

**Round 2 — Boundaries & permissions**
4. Accès : lit seulement / écrit / shell / web / MCP ?
5. Side-effects irréversibles ? (commit, deploy, send, delete) → si oui : `permissionMode: plan` obligatoire
6. Agents parallèles ? → `isolation: worktree`

**Round 3 — Modèle & enrichissement**
7. Modèle : dans forge, `opus` (jamais `sonnet`) ; dans un repo projet, sa propre doctrine (ia_back, neo_ia : `sonnet` exécution / `opus` jugement) ; `haiku` pour l'exploration rapide ?
8. Effort : dans forge, `medium` pour l'exécution et le mécanique, `high` pour le jugement ; `low` pour l'inspection triviale ; `xhigh` uniquement si un gain a déjà été mesuré sur ce type de tâche ?
9. Skills à injecter ? (subagents n'héritent PAS des skills du parent — lister explicitement)
10. Mémoire entre sessions → désactivée par défaut. L'activer seulement si un apprentissage durable propre à cet agent est démontré, avec périmètre et méthode de révision. Un relais de pipeline n'est jamais une mémoire persistante.

---

## Phase 2 — Recherche & edge cases

- Vérifier qu'aucun agent existant ne couvre déjà ce besoin
- Identifier les outils minimum nécessaires (moins = mieux → force la délégation)
- Anticiper les raccourcis que l'agent pourrait prendre pour zapper ses skills
- Si besoin : `mcp__forge-brain__search_brain("comment-creer-agent")` pour prior art

---

## Phase 3 — Rédiger le fichier agent

### Frontmatter complet

```yaml
---
name: <nom-exact-fichier-sans-md-kebab-case>
description: <TRIGGER directive 3e personne — UNE SEULE LIGNE anglais, jamais >- ni |>
tools: Read, Grep, Glob, Bash, Skill   # TOUJOURS explicite — inclure Skill si l'agent doit invoquer des skills
disallowedTools: Write, Edit           # pour agents read-only
model: opus | haiku                    # forge : jamais sonnet · repo projet : suivre sa doctrine
effort: medium                         # exécution · high pour le jugement · xhigh seulement si gain mesuré
color: red|orange|yellow|green|blue|purple|cyan|pink
# memory: project                      # OPTIONNEL — besoin durable démontré uniquement
permissionMode: acceptEdits | plan     # OPTIONNEL — explicite si le risque le justifie
skills:
  - subagent-creator                   # contenu complet préchargé au démarrage
isolation: worktree                    # si agents parallèles sur fichiers
maxTurns: 50                           # optionnel
---
```

**Règles absolues frontmatter :**
- `memory` : absent par défaut ; si activé, documenter contenu attendu, scope et révision
- `permissionMode` : optionnel ; préférer `plan` pour un agent read-only ou à side-effects sensibles
- `tools:` TOUJOURS explicite — sans ça, comportement variable (incident git reset mars 2026)
- Inclure `Skill` dans `tools:` si l'agent doit invoquer des skills (sinon impossible mécaniquement)
- `disallowedTools: Write, Edit` sur agents read-only (double protection)
- `disallowedTools: Bash` si l'agent doit déléguer plutôt que faire directement
- `description` UNE SEULE LIGNE en anglais — jamais `>-` ni `|`

**Convention couleurs forge (cross-repo — même rôle = même couleur) :**

| Couleur | Catégorie |
|---------|-----------|
| red | Sécurité / Critique (audits sécu, devil's advocate) |
| orange | Review / Validation (code review, optimisation) |
| yellow | Test / Évaluation / Debug |
| green | Développement (implémentation features) |
| blue | Architecture / Design (architect, API design) |
| purple | Analyse / Stratégie (codebase analyzer, audit projet) |
| cyan | Infra / Maintenance (refactoring, migration) |
| pink | Meta-créateurs forge only |

**Politique modèles :**
- `haiku` : exploration rapide, tâches courtes
- `opus` : tout le reste dans forge — `medium` pour l'implémentation, l'exécution et le mécanique, `high` pour l'orchestration, le jugement et les décisions complexes
- `sonnet` : exclu de forge (vault `raisonnement-2026-09-30-zero-sonnet`) ; reste la norme d'exécution des repos projet qui l'ont validée
- `fable` : step-up seulement, après une mesure qui montre qu'Opus 5.5 plafonne
- Effort : Opus 5.5 démarre à `medium` s'il n'est pas précisé — toujours poser `effort:` explicitement · `xhigh` : step-up réservé à l'agentique long-horizon, et seulement après avoir mesuré un gain matériel · `max` : jamais en frontmatter

### Body (system prompt de l'agent)

Ordre obligatoire :
```markdown
1. Rôle (1 phrase — ce que l'agent fait)
2. Input reçu (ce que la session principale lui passe)
3. Étapes numérotées (workflow impératif)
4. Règles strictes (dont "STOP et escalade si X")
5. Format de sortie (avec exemple exact si pertinent)
```

**Principes body :**
- Si une skill DOIT être invoquée → faire de son invocation l'**ÉTAPE 1 bloquante avec raison** :
  `"ÉTAPE 1 OBLIGATOIRE. Invoque la skill [X] (outil Skill). Raison : sans elle tu produis du format obsolète. Ne génère rien avant."`
- Les 5-6 règles non-négociables vivent **inline dans le body**, pas dans une skill zappable
- Voix impérative ; expliquer le pourquoi plutôt que ALL-CAPS MUST
- Étapes à sortie visible (anti-skip de la validation)
- Corps court : les skills listées dans `skills:` sont injectées EN ENTIER → saturation si long
- Frontmatter fait foi : le body NE DOIT PAS re-commenter ni re-justifier les champs frontmatter

### Pattern ESCALADE (AskUserQuestion indisponible en subagent)

Inclure ce bloc dans TOUT agent qui peut rencontrer une ambiguïté :

```markdown
## Si AMBIGU ou hors-scope — STOP + ESCALADE

Tu ne peux PAS appeler AskUserQuestion (filtré en subagent). Si tu rencontres :
- Specs floues / options multiples valides / contraintes contradictoires
- Tâche hors de ton périmètre

Retourner immédiatement :
```
## AMBIGUÏTÉ DÉTECTÉE — escalade session principale
**Contexte** : <ce que tu as compris>
**Ambiguïté** : <ce qui n'est pas clair>
**Options** : (1) <option + tradeoffs> (2) <option + tradeoffs>
**Recommandation** : <option N + raison courte>
**Question** : <formulation courte à poser via AskUserQuestion>
**État** : <fichiers touchés, branche, dirty/clean>
```
```

---

## Phase 4 — Forcer l'invocation des skills (si applicable)

Si l'agent doit invoquer une skill de façon fiable, choisir le niveau d'enforcement :

| Niveau | Mécanisme | Fiabilité |
|--------|-----------|-----------|
| 1 | Ordre impératif numéroté dans le body | Probabiliste |
| 2 | Critique inliné dans le body (pas dans une skill zappable) | Meilleur côté contenu |
| 3 | Script-output gating (script valide, Claude doit lire/agir sur la sortie) | Déterministe |
| 4 | Hook SubagentStop (parse transcript, exit 0 + JSON decision:block) | Garanti (CLI) |
| 5 | UserPromptSubmit (rappel injecté avant que Claude voie le prompt) | Probabiliste fort |
| 6 | `disallowedTools` (couper les raccourcis directs) | Déterministe |

**Règle d'or** : rules/body/skills = suggestions probabilistes. Seuls hooks (exit 2 / decision:block) + script-output gating = garantis.

**SubagentStop pattern (CLI) :**
```python
data = json.load(sys.stdin)
if data.get("stop_hook_active"): sys.exit(0)  # anti-boucle OBLIGATOIRE
# parser transcript → si skill non invoquée :
print(json.dumps({"decision": "block", "reason": "Invoque la skill X via l'outil Skill puis termine."}))
sys.exit(0)  # exit 0 + JSON (PAS exit 2 — sinon JSON ignoré)
```

---

## Phase 5 — Evals (OBLIGATOIRES)

Les evals sont **obligatoires** pour tout agent créé ou optimisé. Sans mesure → pas de preuve d'amélioration.

- 2–3 test cases validés par l'utilisateur
- Spawner simultanément `with_agent` + `baseline` via Task tool
- Grader outcomes (pas paths) ; eval viewer AVANT jugement
- Seule exception : agent de jugement pur subjectif → éval qualitative uniquement

---

## Checklist avant livraison (OBLIGATOIRE — cocher à voix haute, point par point)

**Process**
- [ ] Test préliminaire passé : isolation contexte OU parallélisme confirmé
- [ ] 3 rounds d'interview complétés (skip = réponse explicite dans contexte uniquement)
- [ ] Aucun agent similaire existant

**Frontmatter**
- [ ] `name` kebab-case = nom exact du fichier sans `.md`
- [ ] `description` UNE SEULE LIGNE anglais — jamais `>-` ni `|`
- [ ] `description` directive : "Use this agent when… Use PROACTIVELY when…"
- [ ] `tools:` TOUJOURS explicite — inclut `Skill` si l'agent doit invoquer des skills
- [ ] Mémoire persistante absente, ou justifiée avec scope et révision
- [ ] `permissionMode` cohérent avec les side-effects quand il est déclaré
- [ ] `color` selon convention forge
- [ ] `disallowedTools: Write, Edit` si read-only
- [ ] `disallowedTools: Bash` si délégation forcée
- [ ] `disallowedTools: Agent` si l'agent doit rester leaf-node — le nesting est depth 3 par défaut (v2.1.219) et `Agent` est hérité si `tools:` est omis

**Body**
- [ ] Ordre : Rôle → Input → Étapes → Règles → Format sortie
- [ ] Skills invoquées = ÉTAPE 1 bloquante avec raison (si applicable)
- [ ] Règles non-négociables inlinées (pas seulement dans une skill zappable)
- [ ] Pattern ESCALADE inclus (AskUserQuestion indisponible)
- [ ] Étapes à sortie visible (anti-skip)
- [ ] Body court (skills injectées EN ENTIER → saturation si long)
- [ ] Frontmatter non re-commenté dans le body

**Evals**
- [ ] Test cases validés par l'utilisateur
- [ ] Runs with_agent + baseline lancés
- [ ] Eval viewer généré AVANT jugement

---

## Mode optimisation / audit (agent existant)

Voir `references/checklist-agent-parfait.md` — 5 dimensions complètes.

Priorités audit rapide :
1. La mémoire persistante est-elle absente ou réellement justifiée ?
2. Les permissions suivent-elles le moindre privilège ?
3. `tools:` explicite ? Inclut `Skill` si skills dans frontmatter ?
4. Description directive (pas passive) ? UNE SEULE LIGNE ?
5. Body court + règles inlinées + pattern ESCALADE ?
6. `Agent` absent de `tools:` (subagents ne peuvent pas spawner) ?
7. Convention couleur respectée ?

---

## Gotchas

- **Mémoire opt-in** — l'absence de persistance évite qu'un ancien biais contamine les runs suivants
- **« mémoire entre agents » ≠ `memory: project`** — `memory: project` = mémoire PERSISTANTE d'UN agent (entre sessions). Des agents qui se PASSENT le travail = RELAIS (la session persiste la sortie de chaque agent dans un fichier-relais ; agents read-only jamais Write). Ne jamais répondre `memory: project` à un besoin de relais. Foyer : [[relais-inter-agents-fiable]] (design + méthode de déploiement)
- **`permissionMode` optionnel** — le déclarer quand il clarifie un profil de risque, pas comme rituel
- **`tools:` toujours explicite** — sans, comportement variable (incident git reset mars 2026)
- **`Skill` doit être dans `tools:`** — sinon le subagent NE PEUT PAS invoquer de skill mécaniquement
- **`skills:` précharge le contenu complet, ne force pas une invocation** — garder la liste minimale
- **Sous-subagents POSSIBLES** — depth 3 par défaut depuis CC v2.1.219 (caps 200 spawns/session, 20 concurrents ; `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1` pour l'ancien comportement) ET `Agent` hérité par défaut si `tools:` omis → pour garder un agent leaf-node : `tools:` explicite sans `Agent`, ou `disallowedTools: Agent`. Escalade vers session principale = défaut recommandé (cf [[anti-reentrance-sub-agents-pattern-escalade]])
- **AskUserQuestion filtré** en subagent (issues #12890 #18721 #20275) → pattern ESCALADE obligatoire
- **MCP non garanti** en subagent (`No such tool available`) → brief inline depuis session principale
- **Subagent auto-commit** malgré instruction → mettre "PAS DE COMMIT" en TOP du prompt en gras
- **`effort: xhigh` posé sans mesure = tokens gaspillés** — l'alias `opus` résout vers Opus 5.5, dont le défaut API est `medium` et pour lequel Anthropic ne donne aucun point de départ (« run an effort sweep ») : un `xhigh` hérité d'un modèle antérieur n'est pas justifié. Omettre `effort:` sur un agent `opus` le fait tourner en `medium`. Le prouver avant de le poser (1 run `high` vs 1 run `xhigh` sur la tâche réelle : un fichier lu en plus qui change la conclusion, pas une réponse plus longue). `medium`/`low` pour le mécanique. Cf [[effort-opus-47-doctrine-anthropic-2026]]
- **`CLAUDE_CODE_FORK_SUBAGENT=1`** (v2.1.117+) — hérite du contexte complet parent, réutilise le cache
- **Self-modification bloquée** — un agent ne peut pas modifier son propre fichier (classifier)
- **BOM UTF-8** sur Windows (PowerShell Out-File) → frontmatter cassé silencieusement

---

## Apprentissage

Après chaque création ou optimisation : noter ici les patterns efficaces et gotchas rencontrés.

---

## Références

- `references/checklist-agent-parfait.md` — 5 dimensions complètes
- `mcp__forge-brain__read_note("comment-creer-agent")` — doctrine forge canonique complète
- `mcp__forge-brain__read_note("cowork-skills-reliability")` — matrice enforcement CLI/Desktop/Cowork
