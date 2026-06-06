# Checklist skill parfaite — 6 dimensions

Source : research LLM Claude.ai juin 2026 + doctrine forge. Hedges : chiffres Seleznov/SkillsBench = direction solide, non vérifiés primaire.

---

## 1. Discovery / activation

- [ ] Description = identifiant domaine + "ALWAYS invoke when…" + contrainte négative ("Do not X directly")
- [ ] 3e personne ; contient le QUOI et le QUAND ; phrases de trigger concrètes incl. cas où l'utilisateur ne nomme pas la skill
- [ ] `name` kebab-case, ≤ 64 chars, pas "claude"/"anthropic", gérondif préféré
- [ ] ≤ 250 chars pratique (system reminder `/skills` tronque au-delà → auto-trigger défaillant)
- [ ] ≤ 1024 chars spec officielle
- [ ] description + `when_to_use` ≤ 1536 chars combiné dans le listing
- [ ] UNE SEULE LIGNE YAML — jamais `>-` ni `|` (casse la découverte, Prettier mangling)
- [ ] Pas de XML tags
- [ ] Near-miss exclusions incluses ("NOT when X", "Use this for Y not Z")

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

- [ ] Description tronquée / over-budget (> 250 chars pratique, > 1024 spec)
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
