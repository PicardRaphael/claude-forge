# Méta-prompt — Générer la bibliothèque complète de prompts d'analyse réutilisables

> **Version 2 — révisée 25 mai 2026** : intégration apports session MCP forge-brain v1.3 + lecture code RÉEL obligatoire + catégorie 7 Vault/MCP + 5 règles génération critiques ajoutées (10-14) + table navigation enrichie.

> **Quoi** : prompt unique qui, exécuté dans une session Claude Code, lit le vault forge-brain en entier et **génère automatiquement** une bibliothèque de prompts d'analyse réutilisables dans `vault/claude-forge/07-Prompts/analyse/`.
>
> **Pourquoi** : routine higher-order Boris ("I prompt Claude → I create a routine that prompts Claude"). Une fois la bibliothèque générée, Raphael copie-colle un prompt + met le chemin du repo/skill/agent à analyser, et la séquence A→B→C→D→E + doctrine post-23 mai s'applique automatiquement.

---

## ORDRE D'EXÉCUTION (à respecter)

**Ne PAS exécuter ce méta-prompt avant les étapes suivantes** :

1. ✅ **DÉJÀ FAIT** — Audit thématique vault Claude Code 23 mai 2026 (22 corrections, 2 leaders, 1 rule séquence canonique)
2. 🔄 **EN COURS** — Audit Claude-forge dogfooding (`output/audit-vault-thematique/08-claude-forge-dogfooding.md`) — vérifier que forge respecte sa propre doctrine
3. 🆕 **ENSUITE** — Exécuter CE méta-prompt → génère bibliothèque dans `vault/07-Prompts/analyse/`
4. 🆕 **APRÈS** — Lancer les 6 audits thématiques vault (02 à 07) en utilisant la bibliothèque

**Raison de cet ordre** : la bibliothèque est générée À PARTIR du vault. Si forge a du drift, prompts basés sur composants drift. Audit forge d'abord = vault propre = bibliothèque propre.

---

## RECOMMANDATION REVIEW

Ce méta-prompt est rédigé à la fin d'une session longue (audit thématique Claude Code + propagation + capitalisation). **Relire à tête reposée avant exécution** — risque d'erreur de design qui se propagerait dans 15+ prompts générés.

---

## Prompt à coller en session fraîche

```
<role>
Tu es Jarvis dans claude-forge. Ta mission : générer une bibliothèque complète de prompts d'analyse réutilisables dans `vault/claude-forge/07-Prompts/analyse/`, basée sur tout ce que je sais faire selon le vault forge-brain post-audit 23 mai 2026.
</role>

<contexte>
Le vault forge-brain contient la doctrine canonique post-audit 23 mai 2026 + apports session 24-25 mai 2026 :
- Notes canoniques `04-Techniques/claude-code/*` (8 notes 22 mai + leaders Brad-Abrams + Mitchell-Hashimoto)
- Note canonique `04-Techniques/patterns/mcp-vault-llm-design.md` (créée 25 mai : recette MCP vault LLM-optimisé, 9 ops Karpathy + LLM-specific, 7 défenses critiques)
- Rules `.claude/rules/` (sequence-canonique-modification.md = séquence A→B→C→D→E obligatoire)
- Mémoire forge récente : `feedback_da_dicte_tests_adverses` (tests adverses obligatoires sur code rewriting/destructif), `feedback_subagent_audit_category_error` (vérifier source de vérité avant mass-fix), `feedback_5_lignes_karpathy_ouverture` (5 lignes Karpathy verbatim TOP de tout CLAUDE.md forge), `feedback_pas_de_meta_commentaire_doctrine` (zéro meta-commentaire dans composants), `feedback_80_percent_confidence_ship` (80%+ convergence = ship avec tests adverses), `feedback_delegate_guard_env_var_blocked` (matrice classifier par fichier)
- Pattern Karpathy LLM Wiki (3-layers raw/wiki/schema + index.md + log.md + CHANGELOG.md)
- MCP forge-brain v1.3 : 19 outils (8 LLM-optim ajoutés 24-25 mai)

La doctrine validée :
- Séquence A→B→C→D→E pour toute analyse/modification/optimisation
- **Étape 1 enrichie** : pas que metadata — lire 3-5 fichiers code RÉEL par couche + grep patterns récurrents + comprendre frontières (cf [[methode-analyser-repo]] section 1a-1d)
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
- **5 lignes Karpathy obligatoires** au top de tout CLAUDE.md forge (Si ambigu / Diff minimal / done / Vérifie code latest / Code minimum)
- **Tests adverses obligatoires** sur tout code rewriting/destructif (DA pattern, cf 4 silent data loss move_note sauvés 25 mai)
- **Matrice classifier par fichier** : SKILL.md/agents = bypass `CLAUDE_AGENT=X py script.py` marche. CLAUDE.md/settings.json = classifier Anthropic bloque même bypass (édit manuel)
- **MCP vault LLM-optim** : 19 outils (read_section / read_note_resolved / find_by_property / bulk_update_property / move_note / delete_note / lint_vault / usage_stats) vs CLI Obsidian humain
</contexte>

<tache>
Générer une bibliothèque de prompts d'analyse dans `vault/claude-forge/07-Prompts/analyse/`. Chaque prompt = fichier markdown autonome, frontmatter Obsidian conforme, prêt à copier-coller par Raphael avec juste le chemin/nom du composant à analyser.

## Phase 1 — Inventaire (analyser le vault)

1. `mcp__forge-brain__read_note` SANS max_lines sur :
   - 8 notes canoniques claude-code 22 mai
   - `methode-pivoter-doctrine`, `comparaison-skill-anthropic-claude-code-setup`
   - **AJOUTÉ 25 mai** : `mcp-vault-llm-design` (recette MCP vault LLM-optim)
   - **AJOUTÉ 25 mai** : `pattern-vault-llm-karpathy`
2. `mcp__forge-brain__list_notes(folder="04-Techniques/")` + `list_notes(folder="07-Prompts/")` + `list_notes(folder="Knowledge/")`
3. `mcp__forge-brain__read_note("MOC-Claude-Code")` + `read_note("MOC-Techniques")`
4. `Read` les rules `.claude/rules/sequence-canonique-modification.md` + `comportement-proactif.md` + `forge-brain-proactive.md`
5. Lire les feedback mémoire forge cités dans le contexte, en particulier les 6 récents (24-25 mai) :
   - `feedback_da_dicte_tests_adverses`
   - `feedback_subagent_audit_category_error`
   - `feedback_5_lignes_karpathy_ouverture`
   - `feedback_pas_de_meta_commentaire_doctrine`
   - `feedback_80_percent_confidence_ship`
   - `feedback_delegate_guard_env_var_blocked`
6. **AJOUTÉ 25 mai** — `mcp__forge-brain__usage_stats(days=30)` si données disponibles, pour identifier outils MCP réellement utilisés vs morts.

## Phase 2 — Identifier les catégories de prompts à générer

À partir du vault, identifier les **catégories d'analyse** que Jarvis sait faire. Liste de DÉPART (extensible — découvrir d'autres en lisant le vault) :

### Catégorie 1 — Analyse / audit de composants Claude Code
- `analyser-repo-complet` — méthode 6 étapes + propose config CC optimale ([[methode-analyser-repo]])
- `analyser-skill` — optimiser une skill existante ([[comment-creer-skill]] + séquence A→B→C→D→E)
- `analyser-agent` — optimiser un agent existant ([[comment-creer-agent]])
- `analyser-hook` — optimiser un hook existant ([[comment-creer-hook]])
- `analyser-claudemd` — auditer un CLAUDE.md vs doctrine ([[comment-ecrire-claudemd]])
- `analyser-rule` — auditer une rule
- `analyser-mcp-server` — audit un MCP server (cohérence avec [[mcp-vs-skills-doctrine]])
- `analyser-plugin-cowork` — audit un plugin Cowork

### Catégorie 2 — Audit / dogfooding
- `audit-claude-forge-complet` — dogfooding forge (migration depuis `output/audit-vault-thematique/08-...md`)
- `audit-vault-thematique` — méthode A→B→C→D→E pour audit vault par thème (migration depuis `00-TEMPLATE-COMMUN.md`)
- `audit-cross-repos-drift` — comparer doctrine entre ia_back / neo_ia / forge / autres
- `test-comportemental-doctrine` — tester session fraîche que doctrine est chargée (équivalent test 6/6 PASS Claude Code 23 mai)

### Catégorie 3 — Création de composants
- `creer-skill-optimise` — créer une skill respectant 9 catégories Thariq + <250 chars + Gotchas
- `creer-agent-optimise` — créer un agent respectant frontmatter complet + Sonnet/Opus split forge
- `creer-hook-optimise` — créer un hook respectant lint/security/scope only + 29 events + timeouts par type
- `creer-claudemd-optimise` — créer un CLAUDE.md <200L + 5 anti-patterns Anthropic évités
- `creer-rule-optimise` — créer une rule (frontmatter description: obligatoire)

### Catégorie 4 — Prompt engineering / création prompts
- `creer-prompt-optimise` — méta-prompt pour créer un prompt parfait (Claude / Gemini / tout LLM) en utilisant cc-prompt-ref + craft-prompt
- `optimiser-prompt-existant` — auditer un prompt et proposer optims

### Catégorie 5 — Analyses spécialisées (autres domaines IA)
- `analyser-rag-setup` — audit setup RAG (chunking, embeddings, retrieval, reranking, eval, métriques)
- `analyser-chatbot` — audit chatbot (system prompt, tools, mémoire, persona, fallback, sécurité)
- `analyser-finetuning-setup` — audit setup fine-tuning (dataset, méthode LoRA/QLoRA, hyperparams, eval)
- `analyser-agent-ia-multi-framework` — audit pattern agent IA (LangChain / CrewAI / AutoGen / Agent SDK)

### Catégorie 6 — Méta / outils
- `recap-session` — résumer ce qu'on a fait dans une session pour reprise
- `done-session` — capitalisation fin de session (decisions, faits, erreurs)
- `dream-cross-sessions` — équivalent Anthropic Dreaming sur le vault forge

### Catégorie 7 — Vault Karpathy / MCP (AJOUTÉ 25 mai)
- `auditer-vault-karpathy` — audit vault complet (notes + MCP qui le sert + 3-layers + écart vs forge-brain v1.3). Cf [[mcp-vault-llm-design]] et [[pattern-vault-llm-karpathy]].
- `creer-vault-karpathy` — scaffold nouveau vault from scratch (raw/wiki/schema + 4 fichiers obligatoires : SCHEMA.md / index.md / log.md / CHANGELOG.md)
- `creer-mcp-vault-llm-optim` — fork mcp-forge-brain pour nouveau vault. Recette complète : [[mcp-vault-llm-design]]
- `porter-outils-mcp-v13` — port code v1.3 (8 outils LLM-optim) vers un MCP vault existant : read_section, read_note_resolved, find_by_property, bulk_update_property, move_note, delete_note, lint_vault, usage_stats + pagination read_note

**Découvrir d'autres catégories en lisant le vault.** Si tu identifies un pattern d'analyse récurrent dans le vault que je n'ai pas listé → propose-le à Raphael avant de le créer.

## Phase 3 — Génération des prompts

**Mode obligatoire : 1 prompt à la fois.** Présente chaque prompt à Raphael, valide, puis passe au suivant. NE PAS générer 15 fichiers en batch (risque qualité médiocre).

### Structure obligatoire de chaque prompt

Chaque fichier `vault/claude-forge/07-Prompts/analyse/<nom-kebab-case>.md` doit contenir :

```markdown
---
titre: "Prompt — <Nom de l'analyse>"
resume: "<1 phrase spécifique : ce que le prompt fait + quand l'utiliser>"
aliases:
  - "<alias FR principal>"
  - "<alias EN>"
  - "<variante avec mots-clés réels users>"
  - "<abréviation si pertinent>"
  - "<terme technique>"
  (minimum 4-6 aliases)
derniere-maj: 2026-05-XX
type: prompt
domaine: <claude-code | rag | agents-ia | etc.>
sources:
  - "[[methode-analyser-repo]]"
  - "[[sequence-canonique-modification]]"
  - <autres notes canoniques pertinentes>
tags:
  - "#type/prompt"
  - "#sujet/analyse"
  - "#domaine/<domaine>"
---

# Prompt — <Nom de l'analyse>

## Quand l'utiliser
<1-2 phrases sur le cas d'usage>

## Variables à remplir
- `{REPO_PATH}` ou `{SKILL_PATH}` ou autre — chemin/nom du composant à analyser
- `{SCOPE}` — full / léger / spécifique (avec défaut)
- `{EFFORT}` — high / xhigh (défaut high)
- (autres variables si pertinent)

## Prompt à coller (Claude Code session fraîche)

\`\`\`
<role>
[Rôle clair de Claude pour cette analyse]
</role>

<contexte>
[Contexte vault + doctrine canonique à respecter]
</contexte>

<variables>
- {REPO_PATH} = ...
- {SCOPE} = ...
</variables>

<tache>
[Séquence A→B→C→D→E adaptée au scope]
1. ANALYSER LE RÉEL (faits bruts via outils appropriés)
2. LIRE canoniques EN ENTIER via MCP forge-brain
3. CROISER analyse ⨯ canoniques → écarts mesurables
4. PLAN basé sur écarts (Type 1/2/3)
5. EXÉCUTER après validation Raphael
</tache>

<contraintes>
[Doctrine post-23 mai à respecter : pas de paraphrase Anthropic verbatim, hiérarchie sources adaptée, séquence respectée, etc.]
</contraintes>

<format_sortie>
[Format structuré : tableau écarts, plan correction par vague, etc.]
</format_sortie>
\`\`\`

## Output attendu
<Format de la réponse — table PASS/FAIL, plan correction par vague, etc.>

## Variantes
- Mode léger : <quand utiliser version raccourcie>
- Mode expert : <quand utiliser version complète avec DA + outcomes>

## Apprentissages (compounding)
<Section vide initialement, à remplir après chaque utilisation : ce qui a marché, ce qui a échoué, optims observées>

## Wikilinks
- [[methode-analyser-repo]]
- [[sequence-canonique-modification]]
- <autres notes pertinentes>
```

### Règles de génération critiques

1. **XML tags Claude-natifs** dans le bloc prompt (`<role>`, `<contexte>`, `<tache>`, `<contraintes>`, `<format_sortie>`) — Claude les comprend mieux que markdown plat
2. **Variables `{VAR}` explicites** — Raphael remplit, pas devine
3. **Séquence A→B→C→D→E systématique** adaptée au scope (repo entier vs composant existant)
4. **Hiérarchie sources adaptée au domaine** (cf `feedback_anthropic_single_source` scoped + `feedback_regle_scope_pas_universelle`)
5. **Distinguer Type 1/2/3** dans plan correction
6. **Validation par vagues** mentionnée (safe → vérifs → réécriture structurelle)
7. **advisor() AVANT vague 3** ET avant rapport final
8. **Mode obligatoire : présenter UN prompt, valider, suivant**
9. **Table de navigation vault OBLIGATOIRE** dans chaque prompt généré (voir ci-dessous)
10. **AJOUTÉ 25 mai — Lecture code RÉEL obligatoire** : tout prompt d'audit/analyse repo doit imposer (étape 1) la lecture de 3-5 fichiers exemples par couche + grep patterns récurrents. Pas que package.json/README. Référence : [[methode-analyser-repo]] section 1a-1d.
11. **AJOUTÉ 25 mai — Tests adverses obligatoires** : tout prompt qui génère du code rewriting/destructif (move, refactor, mass-fix) doit imposer DA pattern + tests cas adverses (self-link, edge cases, code blocks, case-insensitive). Référence : `feedback_da_dicte_tests_adverses` + `feedback_subagent_audit_category_error`.
12. **AJOUTÉ 25 mai — 5 lignes Karpathy** : tout prompt qui génère/modifie un CLAUDE.md doit imposer les 5 lignes verbatim au top (Si ambigu / Diff minimal / done / Vérifie code latest / Code minimum). Référence : `feedback_5_lignes_karpathy_ouverture`.
13. **AJOUTÉ 25 mai — Matrice classifier par fichier** : tout prompt qui touche fichiers protégés doit mentionner que SKILL.md/agents = bypass `CLAUDE_AGENT=X py script.py` marche, CLAUDE.md/settings.json = édit manuel Raphael. Référence : `feedback_delegate_guard_env_var_blocked`.
14. **AJOUTÉ 25 mai — Outils MCP v1.3 préférés** : tout prompt qui touche vault doit préférer outils v1.3 quand applicable (lint_vault, find_by_property, bulk_update_property, move_note, read_section). Pas update_property×N quand bulk_update_property×1 dispo. Référence : [[mcp-vault-llm-design]].

### Table de navigation vault — OBLIGATOIRE dans chaque prompt généré

Chaque prompt généré DOIT inclure, juste après `<contexte>`, une table de navigation explicite qui dit à Claude **où aller chercher selon le cas d'usage**. Format imposé :

```markdown
## Navigation vault — où lire selon le cas

| Si l'utilisateur demande... | Lire EN ENTIER via `mcp__forge-brain__read_note` SANS max_lines | Pourquoi |
|------------------------------|----------------------------------------------------------------|----------|
| Créer/modifier un agent | `[[comment-creer-agent]]` + `[[workflow-claude-code-optimal]]` | Frontmatter, Sonnet/Opus split, 2-agent Justin Young |
| Créer/modifier une skill | `[[comment-creer-skill]]` + `[[mcp-vs-skills-doctrine]]` | 9 catégories Thariq, 250 chars auto-trigger |
| Créer/modifier un hook | `[[comment-creer-hook]]` + `[[raisonnement-22mai-doctrine-vs-enforcement]]` | 29 events, timeouts par type, lint/security/scope only |
| Optimiser un CLAUDE.md | `[[comment-ecrire-claudemd]]` + `[[pattern-vault-llm-karpathy]]` | <200L, 5 anti-patterns Anthropic |
| Auditer/analyser un repo | TOUTES ci-dessus + `[[methode-analyser-repo]]` | Méthode 6 étapes + pipeline architect→dev→reviewer→test |
| Modifier doctrine forge | `[[methode-pivoter-doctrine]]` + checklist 5 étapes | Éviter régression silencieuse MEMORY/RECAP |
| Comparer avec skill officielle Anthropic | `[[comparaison-skill-anthropic-claude-code-setup]]` | 3 bits utiles repris (commandes bash, tables signal→outil) |
| Vérifier conventions agents (couleurs) | `.claude/rules/agents-color-convention.md` | 8 couleurs cross-repo forge |
| Vérifier scope rule séquence canonique | `.claude/rules/sequence-canonique-modification.md` | A→B→C→D→E obligatoire création/modif/optim |
| Auditer/créer un MCP vault LLM-optim | `[[mcp-vault-llm-design]]` | 9 ops (Karpathy + LLM-specific) + 7 défenses critiques + recette complète v1.3 |
| Auditer/créer un vault Karpathy | `[[pattern-vault-llm-karpathy]]` + `[[mcp-vault-llm-design]]` | 3-layers raw/wiki/schema + 4 fichiers obligatoires |
| Tests adverses sur code rewriting | `feedback_da_dicte_tests_adverses` (mémoire) | Self-link / embeds / case-insensitive / code blocks (4 silent data loss sauvés 25 mai) |
| Pivot doctrinal sans drift | `[[methode-pivoter-doctrine]]` | Checklist 5 étapes anti-régression |

**Adaptation par prompt** : chaque prompt généré customise cette table selon son scope (audit-skill garde les lignes skill+vault doctrine, audit-RAG remplace par les notes RAG du vault, etc.).

**N'oublie pas de regarder** : à la fin de chaque prompt généré, section "Sources vault complémentaires" listant les notes secondaires utiles (`Knowledge/erreurs/*`, `Knowledge/critiques/*`, MOCs, leaders).

**Pattern de référence vault → prompt** : chaque prompt généré = guide de navigation auto-suffisant. Claude qui exécute le prompt n'a pas besoin de chercher quoi lire — c'est dit dans le prompt.

## Phase 4 — Index + propagation

Après génération de TOUS les prompts (validés un par un par Raphael) :

1. Créer `vault/claude-forge/07-Prompts/analyse/index.md` content-oriented (pattern Karpathy) :
   ```markdown
   # Index — Prompts d'analyse réutilisables

   ## Analyse / audit composants Claude Code
   - [[analyser-repo-complet]] — méthode 6 étapes
   - [[analyser-skill]] — optimiser skill existante
   - ...

   ## Audit / dogfooding
   - [[audit-claude-forge-complet]]
   - ...

   ## Création
   - [[creer-skill-optimise]]
   - ...
   ```

2. Mettre à jour `vault/claude-forge/00-Hub/MOC-Claude-Code.md` avec lien vers `07-Prompts/analyse/`

3. Append `vault/claude-forge/log.md` : `## [YYYY-MM-DD] biblioteque-prompts-generee | analyse - N prompts`

4. Mettre à jour `CHANGELOG.md` vault

5. Mémoire forge : ajouter `feedback_bibliotheque_prompts_analyse` qui pointe vers le dossier

6. Commit + push une fois bibliothèque complète

</tache>

<contraintes>
- AUCUNE génération avant inventaire phase 1 complet
- UN PROMPT À LA FOIS, validation Raphael entre chaque
- Chaque prompt respecte la structure obligatoire (XML tags + variables + séquence A→B→C→D→E + sections)
- AUCUNE invention de claim doctrinale — toujours citer notes canoniques vault verbatim ([[note]])
- Hiérarchie sources adaptée au domaine de l'analyse (pas "Anthropic single source" universel)
- advisor() AVANT de finaliser le dernier prompt (relecture cohérence bibliothèque entière)
- Test session fraîche après génération : prendre 1 prompt généré, l'utiliser sur un cas réel, vérifier qu'il fonctionne
</contraintes>

<format_sortie>
Pour chaque prompt généré :
- Présenter le fichier complet en bloc markdown
- Attendre validation Raphael
- Si validation → écrire via `Write` dans `vault/claude-forge/07-Prompts/analyse/<nom>.md`
- Si reformulation → itérer

À la fin :
- Récap : N prompts générés par catégorie
- Liste des fichiers créés
- Index.md créé
- Commit message proposé
</format_sortie>
```

---

## Notes pour Raphael — review demain

### Points à vérifier dans le méta-prompt

1. **Liste des catégories** (6 catégories, ~25 prompts envisagés) — exhaustive ? Manque-t-il une catégorie majeure de ce que je sais faire ?
2. **Mode "un prompt à la fois"** — préférable à du batch ? Si batch acceptable, supprimer cette contrainte (gain de temps × 25)
3. **Variables `{VAR}`** — format OK ou tu préfères `[VAR]` ou `<VAR>` ?
4. **Localisation** — `vault/claude-forge/07-Prompts/analyse/` validée ?
5. **Apprentissages compounding** — section "Apprentissages" en fin de chaque prompt pour itération à l'usage = OK ou trop ?

### Optionnel — élargir scope

Si tu veux que la bibliothèque couvre vraiment **tout ce que je sais faire** :
- Catégorie 7 — **Capitalisation** : prompts pour `/done`, `/recap`, `/dream`, `/reasoning-cache`
- Catégorie 8 — **Recherche / cc-news** : prompts pour fetch tendances IA, capitaliser dans vault
- Catégorie 9 — **Spec / planification** : prompts /spec, /expand, planification feature
- Catégorie 10 — **Tests** : prompts pour outcomes-test, behavioral tests, regression checks

Si tu en veux d'autres → ajoute-les avant exécution.

---

## Quand exécuter ce méta-prompt

**Pas avant que ces étapes soient faites** :

| Étape | Statut | Bloque méta-prompt ? |
|-------|--------|---------------------|
| Audit Claude Code 23 mai | ✅ DONE | Non |
| Audit Claude-forge dogfooding (08) | 🔄 EN COURS | **OUI — attendre fin** |
| Review ce méta-prompt à tête reposée | 🆕 À FAIRE | OUI |
| Validation localisation `vault/07-Prompts/analyse/` | 🆕 À FAIRE | OUI |

Une fois ces 4 conditions OK → coller le prompt dans une session fraîche et laisser la routine higher-order générer la bibliothèque.

---

## Pourquoi ce méta-prompt vaut le coup

- **1 routine vs 25 prompts manuels** : tu écris 1 méta-prompt, il génère 25 prompts. Compounding ×25.
- **Bibliothèque maintenue** : chaque prompt référence les notes canoniques vault — si tu mets à jour `methode-analyser-repo`, les prompts pointent vers la version à jour automatiquement
- **Reuse à vie** : chaque nouveau projet (repo / skill / chatbot / RAG / fine-tuning) = tu copies-colles le prompt avec le bon chemin, et la méthode 23 mai s'applique
- **Effet Boris "compute allocator"** : 99% des tokens vont dans la planification (ces prompts), pas dans la production code session par session

ROI massif sur 6-12 mois.
