---
titre: "Méta-prompt — Générateur de bibliothèque de prompts d'analyse"
resume: "Méta-prompt routine higher-order Boris qui génère ~40 prompts d'analyse réutilisables dans 07-Prompts/analyse/ via lecture vault forge-brain post-audit 23 mai 2026"
aliases:
  - "meta-prompt-bibliotheque"
  - "generateur-prompts-analyse"
  - "routine-higher-order-prompts"
  - "biblioteque-prompts-jarvis"
  - "meta-generator-analyse"
  - "prompts-library-generator"
derniere-maj: 2026-05-23
type: meta-prompt
domaine: claude-code
statut: draft-en-attente-execution
sources:
  - "[[methode-analyser-repo]]"
  - "[[sequence-canonique-modification]]"
  - "[[methode-pivoter-doctrine]]"
  - "[[comparaison-skill-anthropic-claude-code-setup]]"
  - "[[pattern-vault-llm-karpathy]]"
tags:
  - "#type/meta-prompt"
  - "#sujet/routine-higher-order"
  - "#domaine/claude-code"
  - "#statut/draft"
---

# Méta-prompt — Générateur de bibliothèque de prompts d'analyse

> **Routine higher-order Boris** : prompt unique qui, exécuté en session fraîche, lit le vault forge-brain en entier et génère automatiquement ~40 prompts d'analyse réutilisables dans `vault/claude-forge/07-Prompts/analyse/`.

## Décisions validées (Raphael — 2026-05-23)

| Décision | Valeur |
|----------|--------|
| **Mode génération** | Full batch + review groupée |
| **Localisation** | `vault/claude-forge/07-Prompts/analyse/` (cette note y vit déjà) |
| **Scope** | 10 catégories (~40 prompts) |
| **Persistance méta-prompt** | Cette note `_META-GENERATOR.md` |

## Ordre d'exécution (BLOQUE l'exécution tant que pas vert)

| Étape | Statut |
|-------|--------|
| 1. Audit Claude Code 23 mai | ✅ DONE |
| 2. Audit Claude-forge dogfooding (08) | 🔄 EN COURS |
| 3. Review ce méta-prompt à tête reposée | 🆕 À FAIRE |
| 4. Validation localisation | ✅ DONE (cette note) |

**Tant que 2 et 3 pas verts → ne PAS exécuter.**

## Pourquoi ce méta-prompt

- **1 routine vs 40 prompts manuels** — compounding ×40
- **Bibliothèque maintenue** — prompts pointent vers notes canoniques vault, mise à jour auto
- **Reuse à vie** — chaque nouveau projet = copier-coller + chemin
- **Boris "compute allocator"** — 99% tokens dans planification, pas production session par session

## Les 10 catégories à générer

### Cat 1 — Analyse/audit composants Claude Code (~8 prompts)
- `analyser-repo-complet` — méthode 6 étapes [[methode-analyser-repo]]
- `analyser-skill` — optimiser skill existante
- `analyser-agent` — optimiser agent existant
- `analyser-hook` — optimiser hook existant
- `analyser-claudemd` — auditer CLAUDE.md
- `analyser-rule` — auditer rule
- `analyser-mcp-server` — audit MCP server
- `analyser-plugin-cowork` — audit plugin Cowork

### Cat 2 — Audit/dogfooding (~4 prompts)
- `audit-claude-forge-complet` — dogfooding forge
- `audit-vault-thematique` — méthode A→B→C→D→E par thème
- `audit-cross-repos-drift` — comparer doctrine ia_back / neo_ia / forge
- `test-comportemental-doctrine` — session fraîche valide doctrine chargée

### Cat 3 — Création composants (~5 prompts)
- `creer-skill-optimise`
- `creer-agent-optimise`
- `creer-hook-optimise`
- `creer-claudemd-optimise`
- `creer-rule-optimise`

### Cat 4 — Prompt engineering (~2 prompts)
- `creer-prompt-optimise` — méta pour créer prompt parfait
- `optimiser-prompt-existant`

### Cat 5 — Analyses spécialisées IA (~4 prompts)
- `analyser-rag-setup`
- `analyser-chatbot`
- `analyser-finetuning-setup`
- `analyser-agent-ia-multi-framework`

### Cat 6 — Méta/outils (~3 prompts)
- `recap-session`
- `done-session`
- `dream-cross-sessions`

### Cat 7 — Capitalisation (~3 prompts) — AJOUT scope 10
- `done-session-detaille`
- `reasoning-cache-multi-etapes`
- `forge-review-strategique`

### Cat 8 — Recherche/cc-news (~3 prompts) — AJOUT scope 10
- `veille-tendances-ia`
- `capitaliser-recherche-web`
- `cc-news-fetch-personalise`

### Cat 9 — Spec/planification (~4 prompts) — AJOUT scope 10
- `spec-ticket-vers-structure`
- `expand-prompt-flou`
- `planification-feature-multi-app`
- `brainstorming-architecture`

### Cat 10 — Tests (~4 prompts) — AJOUT scope 10
- `outcomes-test-rubric`
- `test-comportemental-systematique`
- `regression-checks-cross-session`
- `devils-advocate-livrable-majeur`

**Total estimé : ~40 prompts.** Découvrir d'autres en lisant le vault → proposer à Raphael avant création.

## Structure obligatoire de chaque prompt généré

Voir section "Règles de génération critiques" du prompt ci-dessous.

---

## Prompt à coller en session fraîche (DEMAIN après audit dogfooding terminé)

```
<role>
Tu es Jarvis dans claude-forge. Ta mission : générer une bibliothèque complète de ~40 prompts d'analyse réutilisables dans `vault/claude-forge/07-Prompts/analyse/`, basée sur le vault forge-brain post-audit 23 mai 2026. Mode : full batch + review groupée. Scope : 10 catégories.
</role>

<contexte>
Le vault forge-brain contient la doctrine canonique post-audit 23 mai 2026 :
- Notes canoniques `04-Techniques/claude-code/*` (8 notes + leaders Brad-Abrams + Mitchell-Hashimoto)
- Rules `.claude/rules/` (sequence-canonique-modification.md = séquence A→B→C→D→E obligatoire)
- Mémoire forge `feedback_audit_thematique_methode` + `feedback_anthropic_single_source` (scoped) + `feedback_regle_scope_pas_universelle`
- Pattern Karpathy LLM Wiki (3-layers / index.md / log.md / append-only)

La doctrine validée :
- Séquence A→B→C→D→E pour toute analyse/modification/optimisation
- Sub-agents par CLUSTER (pas par note)
- Checkpoint write A-inventaire AVANT phase B
- Self-verify FAUX fort impact AVANT phase D
- Distinguer Type 1 (citation/source fausse) / Type 2 (chiffre inventé) / Type 3 (doctrine fausse au fond)
- Hiérarchie sources adaptée par domaine (provider/auteur officiel sur SON produit = single source ; externes hors scope = 4+ sources)
- Hooks lint/security/scope only (pas workflow)
- 2-agent Justin Young SANS split modèles
- Advisor Strategy Brad Abrams (pas Angela Jiang)
- 9 catégories Thariq (post Anthropic mars 2026)
- Pipeline architect→dev→reviewer→test conditionnel
- description SKILL.md ~250 chars auto-trigger

Lire `_META-GENERATOR.md` (cette note) pour la liste des 10 catégories et ~40 prompts à générer.
</contexte>

<tache>

## Phase 1 — Inventaire (analyser le vault)

1. `mcp__forge-brain__read_note` SANS max_lines sur les 8 notes canoniques claude-code + `methode-pivoter-doctrine` + `comparaison-skill-anthropic-claude-code-setup`
2. `mcp__forge-brain__list_notes(folder="04-Techniques/")` + `list_notes(folder="07-Prompts/")` + `list_notes(folder="Knowledge/")`
3. `mcp__forge-brain__read_note("MOC-Claude-Code")` + `read_note("MOC-Techniques")`
4. `Read` les rules `.claude/rules/sequence-canonique-modification.md` + `comportement-proactif.md`
5. Lire `_META-GENERATOR.md` pour la liste des 10 catégories
6. Lire les feedback mémoire forge cités dans le contexte

## Phase 2 — Génération full batch

Générer les ~40 prompts en batch (mode validé). Présenter le récap à Raphael à la fin pour review groupée.

### Structure obligatoire de chaque prompt

Chaque fichier `vault/claude-forge/07-Prompts/analyse/<nom-kebab-case>.md` doit contenir :

\`\`\`markdown
---
titre: "Prompt — <Nom de l'analyse>"
resume: "<1 phrase spécifique>"
aliases:
  - "<4-6 aliases min>"
derniere-maj: 2026-05-XX
type: prompt
domaine: <claude-code | rag | agents-ia | etc.>
sources:
  - "[[methode-analyser-repo]]"
  - "[[sequence-canonique-modification]]"
tags:
  - "#type/prompt"
  - "#sujet/analyse"
  - "#domaine/<domaine>"
---

# Prompt — <Nom de l'analyse>

## Quand l'utiliser
<1-2 phrases>

## Navigation vault — où lire selon le cas

| Si l'utilisateur demande... | Lire EN ENTIER via `mcp__forge-brain__read_note` SANS max_lines | Pourquoi |
|------------------------------|----------------------------------------------------------------|----------|
| <cas 1> | `[[note-canonique]]` | <raison> |
| ... | ... | ... |

(Customiser cette table selon le scope du prompt)

## Variables à remplir
- `{REPO_PATH}` / `{SKILL_PATH}` / autre
- `{SCOPE}` — full / léger / spécifique
- `{EFFORT}` — high / xhigh

## Prompt à coller (Claude Code session fraîche)

\\\`\\\`\\\`
<role>...</role>
<contexte>...</contexte>
<variables>...</variables>
<tache>
1. ANALYSER LE RÉEL
2. LIRE canoniques EN ENTIER via MCP forge-brain
3. CROISER analyse ⨯ canoniques → écarts mesurables
4. PLAN basé sur écarts (Type 1/2/3)
5. EXÉCUTER après validation Raphael
</tache>
<contraintes>...</contraintes>
<format_sortie>...</format_sortie>
\\\`\\\`\\\`

## Output attendu
<format réponse>

## Variantes
- Mode léger / Mode expert

## Apprentissages (compounding)
<vide initialement>

## Sources vault complémentaires
- `Knowledge/erreurs/*`, MOCs, leaders pertinents

## Wikilinks
- [[methode-analyser-repo]]
- [[sequence-canonique-modification]]
\`\`\`

### Règles de génération critiques

1. **XML tags Claude-natifs** dans le bloc prompt (`<role>`, `<contexte>`, `<tache>`, `<contraintes>`, `<format_sortie>`)
2. **Variables `{VAR}` explicites**
3. **Séquence A→B→C→D→E systématique** adaptée au scope
4. **Hiérarchie sources adaptée au domaine** (cf feedback_regle_scope_pas_universelle)
5. **Distinguer Type 1/2/3** dans plan correction
6. **Validation par vagues** mentionnée
7. **advisor() AVANT vague 3** ET avant rapport final
8. **Table de navigation vault OBLIGATOIRE** dans chaque prompt généré
9. **Mode FULL BATCH** — générer les 40 prompts, présenter récap final à Raphael

## Phase 3 — Index + propagation

1. Créer `vault/claude-forge/07-Prompts/analyse/index.md` content-oriented (pattern Karpathy)
2. Mettre à jour `vault/claude-forge/00-Hub/MOC-Claude-Code.md` avec lien vers `07-Prompts/analyse/`
3. Append `vault/claude-forge/log.md` : `## [2026-05-XX] biblioteque-prompts-generee | analyse - 40 prompts`
4. Mettre à jour `CHANGELOG.md` vault
5. Mémoire forge : ajouter `feedback_bibliotheque_prompts_analyse` pointant vers le dossier
6. Commit + push une fois bibliothèque complète

</tache>

<contraintes>
- AUCUNE génération avant inventaire phase 1 complet
- FULL BATCH mode validé (différent du méta-prompt original "un par un")
- Chaque prompt respecte la structure obligatoire (XML tags + variables + séquence A→B→C→D→E + table navigation + sections)
- AUCUNE invention de claim doctrinale — toujours citer notes canoniques vault verbatim ([[note]])
- Hiérarchie sources adaptée au domaine (pas "Anthropic single source" universel)
- advisor() AVANT le batch final pour relecture cohérence bibliothèque entière
- Test session fraîche après génération : prendre 1 prompt généré, l'utiliser sur cas réel, vérifier fonctionnement
- Si tu identifies un pattern d'analyse récurrent dans le vault non listé dans les 10 catégories → propose à Raphael avant création
</contraintes>

<format_sortie>
Phase 1 : récap inventaire vault (notes lues, MOCs scannés, rules lues)
Phase 2 : génération full batch des ~40 prompts → écriture via `Write` dans `vault/claude-forge/07-Prompts/analyse/<nom>.md`
Phase 3 : récap final
- N prompts générés par catégorie (table)
- Liste des fichiers créés
- Index.md créé + MOC mis à jour
- log.md + CHANGELOG.md mis à jour
- Mémoire forge mise à jour
- Commit message proposé
- 1 test session fraîche sur 1 prompt généré (validation empirique)
</format_sortie>
```

---

## Notes pour Raphael — review à tête reposée

### Points à vérifier avant exécution

1. **Liste des 10 catégories / 40 prompts** — exhaustive ? Manque un pattern d'analyse que tu sais que je fais ?
2. **Variables `{VAR}` format** — OK ou tu préfères `[VAR]` ou `<VAR>` ?
3. **Apprentissages compounding** — section en fin de chaque prompt OK ?
4. **Mode full batch** — vraiment OK pour 40 prompts d'un coup, ou tu préfères batch par catégorie (6 vagues) finalement ?

### Risque résiduel

Méta-prompt rédigé fin de session longue. Risque d'erreur de design qui se propagerait dans 40 prompts. **Review à tête reposée demain matin OBLIGATOIRE** avant exécution.

## Wikilinks

- [[methode-analyser-repo]]
- [[sequence-canonique-modification]]
- [[methode-pivoter-doctrine]]
- [[comparaison-skill-anthropic-claude-code-setup]]
- [[pattern-vault-llm-karpathy]]
- [[workflow-claude-code-optimal]]
