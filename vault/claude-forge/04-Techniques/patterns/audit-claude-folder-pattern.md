---
titre: "Pattern audit complet .claude/ d'un repo — 4 auditeurs parallèles + vérif empirique"
type: technique
domaine: claude-code
derniere-maj: 2026-07-15
auteur: claude
aliases:
  - audit claude folder pattern
  - audit .claude/ méthode
  - 4 project-auditor parallèles
  - audit repo claude-code complet
  - pattern audit conformité .claude/
resume: "Méthode validée pour auditer le .claude/ d'un repo : 4 project-auditor en parallèle (agents/skills/hooks/rules+CLAUDE.md), checklist explicite par auditeur, vérification empirique des claims douteux, consolidation + DA, application des fix par vagues via agents spécialisés. Testé sur neo_ia (72 composants, 26 fix) et ia_back (74 composants, 30+ fix) le 22 mai 2026."
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#pattern/audit"
sources:
  - "[[Boris Cherny]]"
  - "[[workflow-claude-code-optimal]]"
  - "[[feedback_audit_repo_method]]"
---

# Pattern Audit Complet .claude/

## Quand utiliser
## Variante — audit COUCHE 2 quand un plan de modernisation existe déjà (15 juil. 2026)

Avant de lancer un audit à froid, **chercher un plan d'audit/modernisation récent en cours** dans le repo (`.claude/todo/`, `docs/`, un `*.md` daté listant des `[x]`/`[ ]`). S'il existe et est largement exécuté (cas bdd : plan du 13 juil., ~80 % coché), NE PAS refaire l'audit — ce serait redondant et risquerait de contredire un travail validé (et négocié avec l'équipe). Basculer en **audit couche 2** :

1. **Vérifier empiriquement les `[x]` « FAIT »** — un claim de complétion non tenu (commit absent, réf morte laissée) = finding majeur. Barre : lire le fichier réel, confirmer le commit (`git log -- <path>`).
2. **Traquer le drift plan↔réel dans LES DEUX SENS** — pas seulement les `[ ]` non faits. Le décalage inverse existe et est fréquent : un `[ ]` en réalité FAIT (le réel a dépassé le plan sans re-cocher). Cas bdd : `settings.json` activé alors que le todo le disait « en attente d'activation humaine ». Un plan périmé fait auditer une fausse réalité au prochain relecteur.
3. **Chercher les angles morts que le plan n'a pas couverts** — mesure jamais faite (`/doctor` budget listing), écart d'inventaire non réconcilié (cible 22 skills vs 33 réelles), pas d'étape « cleanup des artefacts transitoires » (`.proposed`, `last_index.txt` stale qui traînent une fois leur rôle fini).

Effet de bord fréquent d'un `git mv agents/ → roles/` (ou tout déplacement de composant) : **propagation incomplète** — une skill continue de dispatcher `Task(subagent_type=dev)` alors que `dev` n'est plus un agent enregistré (réf morte fonctionnelle silencieuse). Grep exhaustif de l'ancien nom dans tout `.claude/` après tout déplacement. Cohérent avec le gotcha « refonte interne casse l'index de recâblage » plus bas — auditer les **arêtes**, pas que les feuilles.

Piège de brief (session principale) : un check « zéro chemin machine hardcodé » qui ne grep QUE le nom du dev courant (`raphael.picard`) manque les chemins d'un AUTRE dev (`bastien.stagnoli_neo` dans un `paths.json` tracké malgré `.gitignore` — le gitignore n'a aucun effet sur un fichier déjà tracké). Grep le pattern générique `C:\\` / `/Users/`, jamais un nom précis. Un sous-agent bien briefé rattrape ce blind spot — le laisser le faire (registre des op coûteuses : la session injecte le contexte, l'agent vérifie).

- Le user demande "audite mon repo" / "vérifie .claude/" / "le PARFAIT"
- Repo avec 50+ composants `.claude/` (agents + skills + hooks + rules)
- Suspicion de drift après migration stack/refonte majeure
- Maintenance trimestrielle

## Volumétrie typique

| Repo | Agents | Skills | Hooks | Rules | CLAUDE.md | Total |
|------|--------|--------|-------|-------|-----------|-------|
| neo_ia | 12 | 25 | 14 | 17 | 4 | 72 |
| ia_back | 16 | 27 | 14 | 16 | 1 | 74 |
| forge | 11 | 34 | ~20 | ~25 | 1 | 91 |

## Méthode

### Phase 0 — Orientation (5 min)

```bash
ls .claude/agents/*.md | wc -l
ls -d .claude/skills/*/ | wc -l
ls .claude/hooks/ | wc -l
ls .claude/rules/ | wc -l
find . -name CLAUDE.md -not -path "*/node_modules/*"
```

Identifier signaux pré-audit :
- Compteurs CLAUDE.md vs filesystem
- Fichiers suspects (`.test.md` dans hooks/, paths Windows mal échappés)
- Sédiments (`.architect-marker`, `.tdd-bypass`)
- Stack du repo (TS/Python/Go)

### Phase 1 — 4 auditeurs en parallèle

**JAMAIS Explore** (read-only mais pas conçu pour conformité). **JAMAIS general-purpose** (dilue). **JAMAIS 1 seul** (tronque).

Lancer 4 `project-auditor` avec `run_in_background: true` :

1. **Agents** — Frontmatter (permissionMode, memory, effort, color) + body + cross-check code
2. **Skills** — Frontmatter + body + structure references/ + doublons
3. **Hooks + settings.json** — Stack same-stack, pipeline markers complet, matcher MultiEdit, orphelins
4. **Rules + CLAUDE.md** — Frontmatter description obligatoire, compteurs cohérents, sweet spot <150L

Checklist par auditeur : voir [[workflow-claude-code-optimal]] pour les standards.

### Phase 2 — Vérification empirique des claims (CRITIQUE)

Les project-auditor produisent des **faux positifs récurrents** :

| Claim auditeur | Vérif | Source |
|----------------|-------|--------|
| Skill "inexistante" | `grep <skill> ~/.claude/plugins/installed_plugins.json` | Plugin scope user actif partout |
| "`allowed-tools` obligatoire" | docs Anthropic | FAUX — optionnel |
| "`skills:` invalide SKILL.md" | docs Anthropic | Subagent-only mais ignoré silencieusement |
| "Agent X inexistant" | Vérifier scope repo (ia_back vs neo_ia) | Spec-specific |

Si doute → WebSearch `code.claude.com/docs/skills`.

### Phase 3 — Consolidation rapport

Format markdown structuré :
```
# AUDIT <repo> — Rapport consolidé
## 🔴 BLOQUANTS (corrections obligatoires)
## 🟠 DÉRIVES (à corriger)
## 🟡 OPTIMISATIONS
## ✅ CONFORME (à garder)
## SCORE GLOBAL : X/Y PARFAITS
```

Sauvegarder dans `claude-forge/output/audit-<repo>-YYYY-MM-DD.md`.

### Phase 4 — Devil's Advocate (optionnel mais recommandé)

Lancer `devils-advocate` sur le rapport. ATTENTION : DA peut planter sur PowerShell heredoc (bug récurrent Windows). Si DA planté, vérifier manuellement les angles morts.

**Manques fréquents auditeurs** (à challenger manuellement) :
- Fichiers racine repo (`.mcp.json*`, `conftest.py`, `coverage_final.json`)
- Worktrees + agent-memory
- Plugins scope project vs user

### Phase 5 — Application des fix par vagues

**3 vagues recommandées :**

- **Vague 1 — Bloquants doctrine** (rapide, zéro risque) : compteurs CLAUDE.md, description test-writer alignée, effort xhigh→high, matcher MultiEdit ajouté
- **Vague 2 — Bloquants structurels** : renaming rules, fix skills bloquantes, nettoyage sédiments
- **Vague 3 — Dérives + optimisations** : renaming naming anti-patterns, dédup, CLAUDE.md <120L, gotchas vides

Lancer en parallèle dans chaque vague (agents indépendants). Utiliser les agents spécialisés :
- `claudemd-optimizer` pour CLAUDE.md + rules
- `agent-creator` pour agents/*.md
- `skill-creator` pour skills/*/SKILL.md
- `hook-creator` pour hooks/* + settings.json

### Phase 6 — Vérification empirique post-fix

**TOUJOURS** vérifier ce que les sub-agents ont **vraiment** fait (feedback `audit-claims-after-brief`) :

```bash
grep -n "18 rules" CLAUDE.md  # compteur
ls .claude/rules/ | wc -l     # vs filesystem
grep "MultiEdit" .claude/settings.json | wc -l  # tous les guards
grep -rl "Drizzle" .claude/  # zéro si purge faite
```

### Phase 7 — Commit isolé

⚠️ **IMPORTANT** : Stage UNIQUEMENT les fichiers de l'audit. Ne pas mixer avec chantiers en cours (ex code applicatif).

```bash
git add CLAUDE.md .claude/agents/* .claude/skills/*/SKILL.md \
        .claude/hooks/* .claude/rules/* .claude/settings.json
git commit -m "chore(claude): audit complet .claude/ + N fix en 3 vagues..."
git push
```

## Gotchas (highest-signal)

- **Repo à plugins distribués — auditer le `.claude/` SOURCE, pas les bundles** : sur un repo qui publie des plugins, les plugins distribués sont la partie émergée. La maintenance réelle (scripts `scripts/`, agents `vault-linker`/`vault-validator`, rules, pipeline) vit dans le `.claude/` complet du repo source. Auditer uniquement les bundles produit des faux positifs garantis (ex. neoteem-brain : "lint manquant / 3 agents redondants" — TOUS faux). Avant tout verdict "X manque / Y est redondant" sur un tel repo → cartographier `.claude/agents`, `.claude/skills`, `scripts/`, `.claude/rules` du repo source, puis croiser avant de conclure.

- **Matcher `Write|Edit` sans MultiEdit** = trou architectural (cf feedback `multiedit-matcher-blind-spot-hooks`)
- **Stack drift** : code migré ≠ prompts migrés. Grep stack OLD vs NEW (Drizzle→postgres.js sur ia_back : 17 fichiers contaminés découverts)
- **Decisions cross-repo** : pas de propagation automatique. Renaming neo_ia 22 mai (cto-mindset, outcomes-after-architect) à refaire sur ia_back
- **`allowed-tools: Agent` dans skill** = INVALIDE. Utiliser `Task` pour invoquer subagent
- **Plugin scope user** (ex `neoteem-brain-dev-ia@neoteem`) actif partout — pas un faux phantôme
- **Sédiments .tdd-bypass / .architect-marker** à la racine repo = `pipeline-reset` pas tourné
- **DA bug Windows PowerShell heredoc** : si DA planté, sa critique vault peut être tronquée (que le frontmatter). Le titre du frontmatter contient parfois le verdict utile
- **Description = routing CC** : si elle ment, dispatch cassé même si le body est correct (cas test-writer phase=refactor)

## Gotcha — refonte interne d'une feature casse l'index de recâblage (24 juin 2026)

Variante sœur du « stack drift » (code migré ≠ prompts migrés) : une **refonte INTERNE à un repo** qui ajoute/renomme/supprime des fichiers de `references/` (ou des hooks) laisse muets les **index qui recâblent ces fichiers**. Le fichier-feuille est juste, mais ce qui pointe vers lui ment. Audit `ia-workbench` post-refonte `/spec` (modèle epics-jira → Module) : 4 casses, toutes en amont des fichiers refondus, aucune dans les fichiers refondus eux-mêmes.

Checklist post-refonte (à passer EN PLUS de l'audit de chaque fichier) :
- **Table de routage du SKILL.md** : `ls references/ | wc -l` vs nb de lignes de la table « quand lire ». Un fichier ajouté mais non recâblé = invisible à l'exécution (3 templates ux/devops/qa ajoutés, table à 10 lignes).
- **Préfixe MCP mort dans `allowed-tools`** : si une déclaration `.mcp.json` a été supprimée/renommée, son préfixe `mcp__<ancien>__*` survit en frontmatter. Croiser `allowed-tools` ⨯ `claude mcp list` (préfixe = NOM du serveur, cf [[reference_mcp_tool_prefix_nom_serveur]]).
- **`.mcp.json` résiduel** : un brain/serveur copié d'un autre repo (forge-brain localhost vs connector claude.ai NeoTeem) reste « Pending approval » et n'est référencé nulle part. Croiser `.mcp.json` ⨯ préfixes réellement cités dans `.claude/`.
- **Hook tracker/marker jamais reset** : un fichier d'état (`.skill-recommendations-session`) écrit par un hook mais nettoyé par un autre hook **qui n'existe pas** (cité dans une docstring) → le tracker fige (`["spec"]`) et la feature ne se re-déclenche plus. Vérifier que CHAQUE writer de marker a un cleaner réel au SessionStart.
- **Doc feature (`doc/features/<nom>.md`)** : décrit souvent encore l'ancien modèle. Grep le vocabulaire de l'ancien design (`epic`, `epics-jira`), pas seulement les noms de fichiers.

Réflexe : après une refonte, l'audit ne suffit pas fichier-par-fichier — auditer les **arêtes** (qui pointe vers quoi). Un `git rm` d'une reference exige un grep de TOUS ses référents (table de routage, body SKILL, doc, CLAUDE.md).

## Apprentissage (méta sur le pattern lui-même)

- **Règle** : Toujours présenter le rapport AVANT d'appliquer les fix (feedback `present-before-build`)
  - **Why** : Raphael tranche les zones grises (agents à créer ou retirer, plugins à installer)
  - **How to apply** : Phase 4 → AskUserQuestion avec options claires, ensuite Phase 5

- **Règle** : Test comportemental PASS/FAIL en session fraîche après audit massif (feedback `behavioral-test-after-setup`)
  - **Why** : Audit statique = 95% confiance, comportemental = 100%
  - **How to apply** : Après commit, générer un prompt qui teste 3-5 patterns critiques (dispatch test-writer, hook MultiEdit, etc.)

## Liens

- [[workflow-claude-code-optimal]] — Standards Anthropic
- [[feedback_audit_repo_method]] — Mémoire forge méthode
- [[feedback_auditor_false_positives]] — Vérif empirique claims
- [[feedback_multiedit_matcher_blind_spot]] — Gotcha matcher
- [[feedback_drizzle_postgresjs_drift]] — Pattern stack drift
- [[feedback_propagate_decisions_cross_repo]] — Propagation cross-repo
- [[pattern-vault-query-guard]] — Hook deterministe pattern (variante enforcement)
