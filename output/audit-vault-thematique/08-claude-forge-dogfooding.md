# Audit claude-forge — dogfooding doctrine vault + pattern Karpathy

> **Audit transverse complet** du repo claude-forge : tous les composants `.claude/` + `CLAUDE.md` + vault doivent respecter la doctrine canonique vault post-23 mai 2026 + le pattern Karpathy LLM Wiki que forge prône lui-même.

> **Lire d'abord** : `output/audit-vault-thematique/00-TEMPLATE-COMMUN.md` (méthode A→B→C→D→E + règles absolues) + `feedback_audit_thematique_methode.md` (méthode validée audit 23 mai : sub-agents par CLUSTER, checkpoint write A avant B, self-verify FAUX fort impact avant D, distinguer Type 1/2/3 erreurs).

## OBJECTIF

Audit dogfooding : forge prône une doctrine canonique (notes vault 04-Techniques/claude-code/* post-23 mai) + un pattern d'organisation vault (Karpathy LLM Wiki Gist). **Forge respecte-t-il sa propre doctrine sur lui-même ?**

Cible : **100% des composants forge alignés avec doctrine canonique vault**. Détecter chaque drift, chaque oubli post-audit 23 mai, chaque entorse au pattern Karpathy.

## Périmètre

### Composants `.claude/` à auditer (forge perso)
- `.claude/agents/*.md` (11 agents : agent-creator, skill-creator, hook-creator, claudemd-optimizer, project-analyzer, project-auditor, devils-advocate, outcomes-grader, python-dev, self-updater, vault-maintainer)
- `.claude/skills/*/SKILL.md` (30+ skills : cc-*, analyze-project, evolve, skill-evolve, spec, done, recap, forge-review, vault-audit, watch, etc.)
- `.claude/hooks/*.py` + références dans `.claude/settings.json`
- `.claude/rules/*.md` (~10 rules)
- `.claude/settings.json` + `.claude/settings.local.json`
- `CLAUDE.md` racine

### Vault à auditer pour pattern Karpathy
- `vault/claude-forge/index.md` — content-oriented (pas sommaire) ?
- `vault/claude-forge/log.md` — append-only format `## [YYYY-MM-DD] action | titre` ?
- `vault/claude-forge/SCHEMA.md` — conventions documentées ?
- `vault/claude-forge/raw/` — sources immuables, jamais modifiées par LLM ?
- `vault/claude-forge/CHANGELOG.md` — prosaique, à jour ?
- 3 layers stricts respectés (raw / wiki / schema) ?

## Doctrine de référence (sources de vérité)

### Vault canoniques post-23 mai 2026
1. `comment-creer-agent` — frontmatter complet, Sonnet/Opus split forge, convention 8 couleurs, 2-agent Justin Young SANS split modèles, Advisor Strategy Brad Abrams
2. `comment-creer-skill` — 9 catégories Thariq (post Anthropic mars 2026), < 500L body, description ~250 chars auto-trigger
3. `comment-creer-hook` — 29 events officiels, timeouts 600/30/60 par type, exit codes, `once: true` skill frontmatter only, doctrine lint/security/scope only (PAS workflow)
4. `comment-ecrire-claudemd` — target 200L, test "Would removing this cause mistakes?", 5 anti-patterns Anthropic
5. `workflow-claude-code-optimal` — Routines Boris, Advisor Strategy Brad Abrams, Sonnet/Opus split, multi-clauding 5 terminal + 5-10 browser
6. `methode-analyser-repo` — séquence A→B→C→D→E, pipeline architect→dev→reviewer→test conditionnel
7. `mcp-vs-skills-doctrine` — MCP data / Skills how-to / Bash exploration, lethal trifecta Willison
8. `pattern-vault-llm-karpathy` — 3-layers raw/wiki/schema, index.md content-oriented, log.md append-only, qmd Tobi Lütke

### Rules transverses
- `.claude/rules/sequence-canonique-modification.md` — séquence A→B→C→D→E obligatoire pour création/modification/optimisation
- `.claude/rules/comportement-proactif.md` — dispatch + brief minimum sub-agents
- `.claude/rules/check-before-create.md` — ordre canonique avant création
- `.claude/rules/forge-brain-proactive.md` — MCP forge-brain obligatoire, standards qualité notes
- `.claude/rules/vault-consultation-protocol.md` — protocole consultation vault
- `.claude/rules/delegate-to-specialists.md` — délégation obligatoire aux agents-créateurs (delegate-guard.py)
- `.claude/rules/agents-color-convention.md` — 8 couleurs cross-repo
- `.claude/rules/devils-advocate-pipeline.md` — DA conditionnel (pas systématique)
- `.claude/rules/memory-discipline.md` — frontière mémoire/vault
- `.claude/rules/changelog-vault.md` — CHANGELOG après modifs vault

### Mémoire forge (à croiser, pas à corriger)
- `feedback_anthropic_single_source` — Anthropic = single source suffit
- `feedback_audit_thematique_methode` — méthode sub-agents clusters
- `feedback_single_source_truth_vault_canonique` — règles vivent dans canonique vault UNIQUEMENT
- `feedback_doctrine_drift_pattern` — pivot doctrinal SANS purge MEMORY/RECAP = régression silencieuse

## MÉTHODE — A → B → C → D → E (adaptée audit transverse)

### ÉTAPE A — INVENTAIRE empirique de l'existant

**Pas de prescription à ce stade.** Faits bruts uniquement.

#### A.1 — Composants `.claude/`

Pour chaque catégorie, produire un inventaire structuré :

```bash
# Agents
ls .claude/agents/ | wc -l
for f in .claude/agents/*.md; do
  echo "=== $f ==="
  head -20 "$f" | grep -E "^(name|model|effort|color|memory|permissionMode|disallowedTools|skills):"
done

# Skills
ls .claude/skills/ | wc -l
for f in .claude/skills/*/SKILL.md; do
  basename "$(dirname $f)"
  wc -l "$f"
  head -10 "$f" | grep -E "^(name|description):"
done

# Hooks
cat .claude/settings.json | python -c "import sys,json; data=json.load(sys.stdin); print(json.dumps(data.get('hooks',{}), indent=2))"
ls .claude/hooks/ 2>/dev/null

# Rules
ls .claude/rules/ | wc -l
for f in .claude/rules/*.md; do
  echo "=== $f ==="
  head -3 "$f"  # frontmatter description
done

# CLAUDE.md
wc -l CLAUDE.md
```

**Sortie A.1** : `output/audit-vault-thematique/08-claude-forge/A-inventaire-composants.md`
- Tableau agents : name / model / effort / color / memory / permissionMode / disallowedTools / skills présent ?
- Tableau skills : name / description chars / body LOC / scripts/ / references/ présent ?
- Tableau hooks : event / matcher / type / commande / timeout (default 600/30/60 selon type)
- Tableau rules : nom / frontmatter description ? / référencée depuis CLAUDE.md ou rules autres ?
- CLAUDE.md : nombre lignes / sections / critiques < ligne 25 / sources canoniques référencées ?

#### A.2 — Vault forge-brain

```bash
ls vault/claude-forge/
# raw/ wiki/ index.md log.md SCHEMA.md CHANGELOG.md présents ?

wc -l vault/claude-forge/index.md
wc -l vault/claude-forge/log.md
wc -l vault/claude-forge/SCHEMA.md
wc -l vault/claude-forge/CHANGELOG.md

# log.md : format append-only ## [YYYY-MM-DD] action | titre ?
grep -c "^## \[" vault/claude-forge/log.md

# Stats vault via MCP
mcp__forge-brain__vault_stats()
```

**Sortie A.2** : `output/audit-vault-thematique/08-claude-forge/A-inventaire-vault.md`
- 3 layers présents (raw/wiki/schema) ?
- 2 fichiers obligatoires Karpathy (index.md content-oriented + log.md append-only) conformes ?
- CHANGELOG.md à jour avec dernier audit ?
- Stats vault : nombre notes, aliases moy/note, wikilinks moy/note

### ÉTAPE B — LIRE canoniques EN ENTIER + croiser composants

Lire via MCP forge-brain SANS max_lines les 8 notes canoniques + rules forge. Puis pour chaque composant, lister les **claims doctrinales** qu'il doit respecter.

**Outils** :
- `mcp__forge-brain__read_note(file="comment-creer-agent")` SANS max_lines
- `mcp__forge-brain__read_note(file="comment-creer-skill")` idem
- `mcp__forge-brain__read_note(file="comment-creer-hook")` idem
- `mcp__forge-brain__read_note(file="comment-ecrire-claudemd")` idem
- `mcp__forge-brain__read_note(file="methode-analyser-repo")` idem
- `mcp__forge-brain__read_note(file="workflow-claude-code-optimal")` idem
- `mcp__forge-brain__read_note(file="mcp-vs-skills-doctrine")` idem
- `mcp__forge-brain__read_note(file="pattern-vault-llm-karpathy")` idem

### ÉTAPE C — CROISER inventaire ⨯ canoniques → écarts mesurables

**Sub-agents parallèles par CLUSTER** (méthode validée audit 23 mai — cf `feedback_audit_thematique_methode`) :

#### Cluster 1 — Agents forge vs `comment-creer-agent`
Pour chaque agent `.claude/agents/*.md`, vérifier :
- ✅ `memory: project` présent ?
- ✅ `permissionMode` présent (acceptEdits/auto/plan/dontAsk/bypassPermissions/default) ?
- ✅ `model` valide (sonnet/opus/haiku) ?
- ✅ `effort` valide (low/medium/high/xhigh/max) ? `xhigh` réservé architect/dev-lead/refactor-pg ?
- ✅ `color` parmi les 8 conventions forge (red/orange/yellow/green/blue/purple/cyan/pink) ?
- ✅ `description` 3e personne directive, max ~500 chars ?
- ✅ Skills déclarées dans `skills:` frontmatter sont-elles référencées dans le body ?
- ✅ Sonnet/Opus split appliqué (exécution=Sonnet, jugement=Opus) ?
- ✅ Pas d'agent CTO orchestrateur ? Pas d'agent doc dédié ?
- ✅ `disallowedTools: Write, Edit` sur agents read-only (project-auditor, devils-advocate, outcomes-grader) ?
- ❌ Référence vers "Angela Jiang 5×" ou "Init=Opus Coding=Sonnet" Justin Young (drift doctrinal) ?

#### Cluster 2 — Skills forge vs `comment-creer-skill`
Pour chaque skill `.claude/skills/*/SKILL.md`, vérifier :
- ✅ `name` = nom exact dossier kebab-case ?
- ✅ `description` 3e personne directive ?
- ✅ `description` < 250 chars (limite pratique auto-trigger system reminder) ?
- ✅ `description` < 1024 chars (spec) ?
- ✅ Body < 500 lignes ?
- ✅ Si > 500L → `references/` présent et référencé dans body ?
- ✅ Section Gotchas présente (mesurablement améliore accuracy selon Thariq) ?
- ✅ Section Apprentissage pour skills métier ?
- ✅ Pas de README.md dans dossier skill ?
- ✅ Skills user-invokable:false orphelines = référencées depuis skills: frontmatter d'agent ET dans body ?
- ✅ Rentre dans 1 des 9 catégories Thariq ? Sinon justifié comme "cas particulier forge" ?

#### Cluster 3 — Hooks forge vs `comment-creer-hook`
Pour chaque hook dans `.claude/settings.json` + `.claude/hooks/*.py`, vérifier :
- ✅ Event utilisé fait partie des 29 officiels ?
- ✅ Matcher triplet `Write|Edit|MultiEdit` pour interception writes ?
- ✅ Pas de hook workflow agentique (architect-guard, commit-guard, dispatch-guard, marker-protect, TTL markers — anti-pattern doctrine 22 mai) ?
- ✅ Hooks lint/security/scope only ?
- ✅ Chemins absolus (cross-machine via `py` launcher Windows) ?
- ✅ Exit codes corrects (exit 2 pour bloquer) ?
- ✅ `once: true` UNIQUEMENT dans skill frontmatter, jamais settings.json ni agent ?
- ✅ Timeout < default par type (600s command/http/mcp_tool, 30s prompt, 60s agent) ?
- ✅ Pas de bash heredoc Windows (boucle quoting) ?
- ✅ Stack identique au projet (Python pour forge) ?

#### Cluster 4 — CLAUDE.md forge vs `comment-ecrire-claudemd`
Vérifier CLAUDE.md racine :
- ✅ < 200 lignes (target Anthropic) ?
- ✅ Critiques < ligne 25 (pattern critical-instructions-top-of-file) ?
- ✅ Test "Would removing this cause mistakes?" applicable à chaque ligne ?
- ✅ 5 anti-patterns Anthropic évités (kitchen sink, correcting over and over, over-specified, trust-then-verify gap, infinite exploration) ?
- ✅ Pas de routing (appartient à `.claude/rules/`) ?
- ✅ Pas de description du code ?
- ✅ Pas de TODO list ?
- ✅ Pas de référence à "max déprécié v2.1.91" (corrigé audit 23 mai) ?
- ✅ Section Notes canoniques chantier référence les 8+1 notes post-23 mai (avec [[methode-pivoter-doctrine]] + [[comparaison-skill-anthropic-claude-code-setup]]) ?
- ✅ Encoding UTF-8 sans BOM ?

#### Cluster 5 — Rules forge vs `methode-analyser-repo` + Karpathy + check-before-create
Pour chaque `.claude/rules/*.md`, vérifier :
- ✅ Frontmatter `description:` présent (sinon rule MORTE silencieusement — cf `feedback_rules_frontmatter_mandatory`) ?
- ✅ Référence séquence A→B→C→D→E si applicable (créateur/modificateur/analyste) ?
- ✅ Pas de doublon avec autre rule (single source of truth `feedback_single_source_truth_vault_canonique`) ?
- ✅ Référencée depuis CLAUDE.md ou autre rule (pas orpheline) ?
- ✅ Anti-pattern hook workflow respecté ?
- ✅ Doctrine 22 mai (pas de gate systématique, DA conditionnel) ?

#### Cluster 6 — Vault forge-brain vs `pattern-vault-llm-karpathy`
Vérifier structure vault :
- ✅ 3 layers stricts : `raw/` immuable + `wiki/` LLM-owned + `SCHEMA.md` ?
- ✅ `index.md` **content-oriented** (concepts clés + domaines + erreurs documentées) — PAS sommaire généré ?
- ✅ `log.md` **append-only** format strict `## [YYYY-MM-DD] action | titre` ?
- ✅ `log.md` jamais modifié rétroactivement (vérifier git log -- log.md) ?
- ✅ `CHANGELOG.md` prosaique à jour avec audit 23 mai ?
- ✅ `raw/` jamais modifié par LLM (vérifier git log) ?
- ✅ Stats qualité notes (via vault_stats) : aliases moy ≥ 5 ? Wikilinks moy ≥ 2 ?
- ✅ Frontmatter strict respecté (titre, resume, aliases ≥ 4, derniere-maj, tags ≥ 2) ?

### ÉTAPE D — PLAN correction par CLUSTER (priorisé)

Distinguer **3 types d'erreur** (cf `feedback_audit_thematique_methode`) :

#### Type 1 — Drift doctrinal (RÉÉCRITURE)
Composant fait référence à doctrine pré-audit 23 mai :
- Agent qui cite "Angela Jiang advisor 5×" → corriger Brad Abrams
- Skill qui cite "25+ events" → corriger 29 events
- CLAUDE.md qui dit "max déprécié v2.1.91" → corriger "toujours disponible mai 2026"
- Rule qui cite "Init=Opus Coding=Sonnet Justin Young" → corriger 2-agent sans split

#### Type 2 — Drift technique (CHIRURGIE)
- Frontmatter manquant (`memory:`, `permissionMode:`)
- Description > 250 chars
- Couleur agent non conforme conventions 8
- Hook timeout incorrect par type
- Skill body > 500L sans references/

#### Type 3 — Drift structurel (REFONTE)
- Hook workflow agentique encore présent → supprimer
- Agent CTO orchestrateur → kill
- Agent doc dédié → kill
- Rule sans `description:` frontmatter → ajouter
- `log.md` non append-only → restaurer historique
- `index.md` sommaire au lieu de content-oriented → réécrire

**Plan par vagues** (cf advisor 23 mai) :
1. **Vague 1** — Type 2 safe (chirurgies frontmatter, chiffres, descriptions) : autonomes, peu de risque
2. **Vague 2** — Type 1 drift doctrinal : nécessite vérification croisée mais mécanique
3. **Vague 3** — Type 3 structurel : nécessite advisor + DA avant exécution

### ÉTAPE E — EXÉCUTION via agents-créateurs

⚠️ **Hook `delegate-guard.py` bloque l'édit direct des composants forge**. Toute modification doit passer par :
- `agent-creator` pour agents
- `skill-creator` pour skills
- `hook-creator` pour hooks
- `claudemd-optimizer` pour CLAUDE.md
- Édit direct OK pour rules (pas de delegate-guard)

**Validation Raphael par vague** (pas en batch). Commit par cluster.

**CHANGELOG.md vault** + log.md mis à jour à chaque vague.

**Test session fraîche après vague 3** (cf `methode-pivoter-doctrine` étape 5).

## ÉTAPE F — Propagation cross-repo (BONUS)

Forge corrigé → vérifier dans **ia_back** et **neo_ia** que les composants équivalents reflètent la même doctrine. Identifier les drifts cross-repo (cf `feedback_propagate_decisions_cross_repo`).

**Outils** :
```bash
grep -r "Angela Jiang\|25+ events\|max déprécié\|Init.*Opus.*Coding.*Sonnet" \
  ../neot-v2/ia_back/.claude/ \
  ../neot-v2/neo_ia/.claude/ \
  2>/dev/null
```

## OUTPUT attendu

`output/audit-vault-thematique/08-claude-forge/`
- `A-inventaire-composants.md` — tableaux exhaustifs agents/skills/hooks/rules/CLAUDE.md
- `A-inventaire-vault.md` — état Karpathy pattern
- `B-canoniques-lues.md` — récap claims doctrinales par cluster
- `C-croisement.md` — écarts mesurables par cluster (6 sub-agents parallèles)
- `D-plan-correction.md` — Type 1/2/3, priorisé par vague
- `E-modifications.md` — après validation Raphael, journal des modifs par cluster
- `F-propagation-cross-repo.md` — bonus ia_back/neo_ia
- `rapport-final.md` — synthèse + verdict global PASS/FAIL

## RÈGLES ABSOLUES

- ❌ AUCUNE modif composant avant validation Raphael (commit par vague)
- ❌ AUCUNE invention de claim doctrinale (toujours citer notes vault verbatim)
- ❌ PAS DE COMMIT avant Raphael OK explicite
- ❌ Hook `delegate-guard.py` respecté → passer par agents-créateurs
- ✅ Sub-agents par cluster en parallèle (méthode validée audit 23 mai)
- ✅ Checkpoint write A-inventaire AVANT lancer C (cluster vérifs)
- ✅ Self-verify FAUX fort impact AVANT phase D (cf `feedback_audit_thematique_methode`)
- ✅ advisor() AVANT vague 3 (Type 3 structurel) ET avant propagation F

## FORMAT RAPPORT FINAL

```markdown
# Audit claude-forge dogfooding — <date>

## Verdict global
PASS / PARTIAL / FAIL — sur le ratio composants alignés doctrine canonique

## Bilan inventaire
- Agents: N audités / X alignés / Y drift doctrinal / Z drift technique
- Skills: N / X / Y / Z
- Hooks: N / X / Y / Z
- Rules: N / X / Y / Z
- CLAUDE.md: PASS/FAIL avec liste corrections
- Vault Karpathy: PASS/FAIL avec liste corrections

## Top 10 drifts détectés
[liste priorisée par impact]

## Plan corrections (3 vagues)
[Type 1 / Type 2 / Type 3, par cluster]

## Étape F — Propagation cross-repo
[N drifts détectés dans ia_back, X dans neo_ia]

## Verdict advisor()
[résumé verbatim]

## Recommandation finale
[go/no-go par vague, attente Raphael]
```

---

**Méthode A→B→C→D→E + sub-agents clusters + checkpoint write + self-verify + distinguer Type 1/2/3 = méthode validée audit 23 mai.** advisor() avant vague 3 ET avant propagation F. Honnêteté intellectuelle absolue. Forge respecte sa propre doctrine ou la corrige.
