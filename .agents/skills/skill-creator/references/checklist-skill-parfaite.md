# Checklist skill parfaite — 6 dimensions

Source : research LLM Claude.ai juin 2026 + doctrine forge. Hedges : chiffres Seleznov/SkillsBench = direction solide, non vérifiés primaire.

---

## 0. Process — Interview & evals (OBLIGATOIRES)

- [ ] **3 rounds d'interview complétés** via AskUserQuestion (skip question seulement si réponse explicite dans le contexte — jamais par hypothèse)
  - Round 1 : intent + environnement cible + mode (create/optimize/audit)
  - Round 2 : déclenchement + near-misses + side-effects
  - Round 3 : forme (SKILL.md unique / dossier) + outils/MCP + modèle + evals
- [ ] **Test cases validés** par l'utilisateur avant les runs (2–3 prompts réalistes, `evals/evals.json`)
- [ ] **Evals A/B lancés** : with_skill + baseline simultanés, eval viewer généré AVANT jugement
- [ ] **Description optimization loop** : ~20 trigger queries, best_description sélectionnée sur score test (60/40 split, 3 runs/query, max 5 itérations)
- [ ] Seule exception evals : skill de connaissance pure subjective → éval qualitative uniquement

## 1. Discovery / activation

- [ ] Description = identifiant domaine + "ALWAYS invoke when…" + contrainte négative ("Do not X directly")
- [ ] 3e personne ; contient le QUOI et le QUAND ; phrases de trigger concrètes incl. cas où l'utilisateur ne nomme pas la skill
- [ ] `name` kebab-case, ≤ 64 chars, pas "claude"/"anthropic", gérondif préféré
- [ ] ≤ 1024 chars spec officielle (hard limit)
- [ ] description + `when_to_use` ≤ 1536 chars combiné dans le skill listing
- [ ] Viser court et dense — triggers concrets en premier, contexte ensuite
- [ ] UNE SEULE LIGNE YAML — jamais `>-` ni `|` (casse la découverte, Prettier mangling)
- [ ] Pas de XML tags
- [ ] Near-miss exclusions incluses ("NOT when X", "Use this for Y not Z")

## Champs frontmatter VALIDES (liste FERMÉE — ne jamais en inventer)

Seuls ces champs existent dans le frontmatter d'une skill Claude Code. **Tout autre champ = ERREUR à signaler, JAMAIS à ajouter.**

| Champ | Obligatoire ? | Valeurs |
|-------|---------------|---------|
| `name` | OUI | kebab-case = nom du dossier |
| `description` | OUI | une ligne directive, ≤ 1024 chars |
| `user-invocable` | recommandé | `true` / `false` |
| `allowed-tools` | si write/MCP | liste outils ou `mcp__server__*` |
| `model` | optionnel | `opus` / `haiku` (forge) · `sonnet` accepté dans un repo projet qui l'a validé |
| `effort` | optionnel | `low` / `medium` (exécution) / `high` (jugement) / `xhigh` |
| `disable-model-invocation` | si side-effects | `true` |
| `argument-hint` | optionnel (slash) | indice d'argument, ex `"[prompt]"` — OFFICIEL |

**Champs INTERDITS (n'existent PAS pour une skill, ne jamais les proposer/ajouter)** : `version`, `author`, `date`, `created`, `tags`, `color` (color = agents uniquement), `tools` (skill = `allowed-tools`, pas `tools`), `memory`, `permissionMode` (ces 2 = agents uniquement).

Si un audit signale l'absence d'un champ interdit comme un écart → c'est l'audit qui se trompe, pas la skill. Vérifier contre cette liste fermée AVANT de classer un champ « manquant ».

**Si un champ inconnu de cette liste apparaît dans une skill réelle : NE PAS conclure « inventé » d'emblée.** Claude Code évolue ; des champs officiels peuvent manquer ici (ex : `argument-hint` pour les slash commands). Signaler comme « à vérifier », demander confirmation, JAMAIS supprimer un champ sans certitude qu'il est non-officiel.

## 2. Body / exécution

- [ ] SKILL.md body < 500 lignes ; `references/` une seule profondeur ; ToC si > 100 lignes
- [ ] Voix impérative ; expliquer le *pourquoi* plutôt que ALL-CAPS MUST
- [ ] Réserver ALWAYS/NEVER aux étapes vraiment fragiles/critiques uniquement
- [ ] Scripts : préciser EXÉCUTER vs LIRE ; pas de constantes magiques ; packages listés
- [ ] Gestion d'erreur explicite ; chemins forward-slash uniquement
- [ ] Boucles de validation pour opérations quality-critical
- [ ] Checklist copiable pour workflows multi-étapes

## 3. Structure / enforcement (par environnement cible)

- [ ] **CLI** → hooks PreToolUse/PostToolUse ok + description directive
- [ ] **Desktop** → hooks best-effort ; script-output gating préféré
- [ ] **Cowork** → ZÉRO hooks ; script-output gating + slash entry + remote HTTPS MCP + AskUserQuestion gate session principale + project/folder Instructions (≠ CLAUDE.md)
- [ ] **Portable** → description directive + script-output gating uniquement
- [ ] Side-effecting : `disable-model-invocation: true` + `allowed-tools` whitelist + AskUserQuestion gate
- [ ] MCP type adapté à la surface (stdio CLI/Desktop ; remote HTTPS Cowork)
- [ ] Scripts enforceables uniquement via leur OUTPUT — Claude doit lire/agir sur la sortie
- [ ] Routing dans CLAUDE.md/.claude/rules (CLI/Desktop) ou project Instructions (Cowork) — jamais dupliquer le contenu dans CLAUDE.md

## 4. Évaluation

- [ ] ≥ 3 task evals substantielles (pas one-step)
- [ ] ~20 trigger queries : 8–10 should-fire (phrasing varié) + 8–10 near-miss should-NOT-fire
- [ ] Baseline-without-skill vs with-skill ; 3–5 trials par case ; runs isolés
- [ ] Grader outcomes (pas paths) ; assertions descriptives et vérifiables
- [ ] Eval viewer généré AVANT de juger soi-même (`--static` Cowork/headless)
- [ ] `timing.json` capturé dès la notification de fin (seule occasion)
- [ ] Testé sur Haiku/Sonnet/Opus effectivement utilisés

## 5. Optimisation / audit (skill existante)

Détecter et corriger chaque item — scorer avec fichier + fix en une ligne, boucler jusqu'à propre :

- [ ] Description tronquée / over-budget (> 1024 chars spec, ou description + when_to_use > 1536 listing)
- [ ] Description passive (non-directive)
- [ ] Chaînes de references > 1 niveau de profondeur
- [ ] References mortes ou cassées
- [ ] "Why" manquant (ALL-CAPS sans explication = yellow flag)
- [ ] ALL-CAPS excessif (> 2-3 occurrences = bruit)
- [ ] Near-miss exclusions manquantes
- [ ] SKILL.md > 500 lignes
- [ ] Skill flat-file qui devrait être un dossier (scripts + references)
- [ ] Doctrine dupliquée/divergente entre skills
- [ ] Assertions non-discriminantes dans les evals
- [ ] YAML multi-ligne (Prettier mangling)

## 6. Packaging / distribution

- [ ] Packager en `.skill` si distribution souhaitée
- [ ] Bundler en plugin pour distribution équipe (manifest `.claude-plugin/plugin.json`)
- [ ] Emplacement par surface : `.claude/skills/` (projet) / `~/.claude/skills/` (user) / plugin-bundled
- [ ] **Cowork** : enregistrer via UI, garder total actif < 30
- [ ] Conserver le nom à l'update (jamais `-v2`)
- [ ] Copier dans temp dir avant d'éditer une skill read-only installée
