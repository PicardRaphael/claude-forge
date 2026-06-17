# Handoff — construire 4 skills RAG/outils-IA + enrichir responsable-ia

> Prompt à coller dans une **session Claude Code fraîche** (repo `claude-forge`, après `/clear`).
> Rédigé le 2026-06-17. Architecture validée par Raphael en session précédente.
> Corpus vault source = déjà rédigé (notes RAG + 4 notes-paysage build-vs-buy + MOC parent).

---

Tu es dans le repo `claude-forge`. Objectif : créer **4 nouvelles skills** et **enrichir 1 skill existante**, à partir d'un corpus vault déjà rédigé. L'architecture a été validée par Raphael — TON job est la CONSTRUCTION, pas la re-conception. MAIS commence par une phase d'investigation (phase 0 ci-dessous) pour confirmer qu'il ne manque rien.

## ⚠️ Règles non négociables (doctrine forge)

1. **NE JAMAIS écrire un SKILL.md à la main.** Le hook `delegate-guard` bloque l'édition directe. Tu DOIS passer par la skill `skill-creator` (y compris pour enrichir `responsable-ia`).
2. **Séquence canonique A→B→C→D→E** (`.claude/rules/sequence-canonique-modification.md`) :
   - A. Lire le RÉEL : les SKILL.md existants cités + les notes vault sources EN ENTIER.
   - B. Lire les canoniques EN ENTIER via MCP : `mcp__forge-brain__read_note(file="comment-creer-skill")` SANS max_lines + `read_note(file="mcp-vs-skills-doctrine")`.
   - C. Croiser → écarts. D. Plan présenté à Raphael. E. Construire via skill-creator.
3. **Frontières anti-doublon** (vérifiées) : `responsable-ia` couvre le cadrage stratégique Lead IA (CODIR, RICE, build-vs-buy AU NIVEAU DÉCISION, archi RAG au cadrage). `spec` = idée→tickets. `cc-advisor` = besoin flou→composant. `outcomes-test` = éval vs rubrique. `cc-news` = veille Claude Code. Les nouvelles skills sont plus profondes/opérationnelles — elles ne doublent pas. Chevauchement réel détecté → STOP, signale.
4. **Piège `\|` en cellule de tableau** : dans le markdown VERS le vault, `[[note\|alias]]` dans une cellule casse l'index SQLite. Utiliser `[[note]]` nu en cellule. (Ne concerne pas les SKILL.md.)
5. **Budget tokens** : 84+ skills = ~6.8k tokens au démarrage. Description ≤ 250-300 chars, UNE ligne, jamais `>-` ni `|`. Skills de référence = préchargement LÉGER (pointeurs `references/`, pas les notes en full).
6. **DA conditionnel** : skills réutilisées → agent `devils-advocate` sur chaque SKILL.md avant de déclarer terminé.
7. **Git** : `git status` + `git diff` à la fin. NE PAS commit/push sans demander.

## Phase 0 — investigation des trous (AVANT de construire)

Raphael a explicitement demandé : « il manque pas une skill ou quoi ? vois s'il y en a d'autres ». Donc :

1. Lire `MOC-paysage-outils-ia-marche-2026` + `RAG` (index) + lister `.claude/skills/` + lire `responsable-ia/SKILL.md`.
2. Dresser le **parcours projet IA** (idée → cadrage → choix outil → conception → spec → tickets → build → éval → veille) et mapper chaque étape à une skill existante ou manquante.
3. Pour CHAQUE trou détecté, rendre un verdict avec preuve : **`créer` / `enrichir l'existant` / `déjà couvert`**. Lister explicitement ce que tu écartes et pourquoi (barème : 1 skill = 1 responsabilité ; tokens précieux ; enrich-before-create).

**Reads de la session précédente (à confirmer, pas à re-litiger) :**
- **Éval RAG** → probablement **déjà couvert** (note `rag-evaluation` + skill `outcomes-test`). Vérifier les deux AVANT de proposer un `rag-eval` autonome. C'est l'étape 6 de `rag-design` + pointeur, pas une skill neuve.
- **Archi agent non-RAG** → tranché **non** 2× (responsable-ia couvre le cadrage). Reconfirm-only, basse priorité.
- **Workflow FRIA/conformité IA déclenchable** → **seul candidat neuf plausible**, mais dans l'orbite de `responsable-ia` (qui a déjà `ai-act-eu-cheatsheet` + `rgpd-ia-cnil-article-22`). Verdict à rendre : enrichissement de `responsable-ia` vs skill workflow distincte ?

→ **Une seule porte d'approbation** : phase 0 + les 4 skills validées = présentées ensemble à Raphael dans le plan (étape D). Il tranche. PAS de build pendant la phase 0.

## Les 4 skills validées + 1 enrichissement

### 1. `cc-rag-ref` — référence RAG active (`user-invocable: false`)
Rôle : rendre le corpus RAG actif en contexte (comme `python-ref`/`cc-features-ref`). Chargée quand le sujet RAG arrive.
Lire AVANT (EN ENTIER) : `RAG`, `rag-data-audit-discovery`, `rag-data-models-par-cas-usage`, `rag-metadata`, `rag-architecture`, `rag-embeddings`, `rag-reranking`, `rag-vector-databases`, `rag-chunking`, `rag-evaluation`, `rag-production`.
Contenu : sommaire dense + pointeurs `references/` ; NE PAS recopier les notes (elles vivent dans le vault, pointer via MCP). Décider explicitement préchargé vs lazy. Modèle : `cc-features-ref/SKILL.md`.

### 2. `rag-design` — workflow conception RAG (`user-invocable: true`)
Rôle : dialogue guidé déroulant **audit data → data model → ingestion → récupération → UX**, qui remplit un template livrable au fil de l'eau (dialogue + template combinés).
Lire AVANT : `rag-data-audit-discovery` (6 étapes), `rag-data-models-par-cas-usage` (8 schémas), `rag-architecture`. Consomme `cc-rag-ref`. Étape 6 = éval via `outcomes-test` + `rag-evaluation`.
Frontière : ≠ `spec` (vient APRÈS, design→tickets) ; ≠ `responsable-ia` (cadrage, pas conception technique).

### 3. `choix-outils-ia` — choix build-vs-buy de TOUT outil IA (`user-invocable: true`)
Rôle : sur un besoin en langage naturel (« je veux de la voix / OCR / un context engine / mettre l'IA en prod »), DIALOGUE avec Raphael (questions de cadrage) → consulte le vault AVANT de proposer → verdict **build-vs-buy + outil(s) reco** + pricing + pièges de licence. Raphael : « échange avec moi, look le vault avant ».
Lire AVANT : `MOC-paysage-outils-ia-marche-2026` + les 4 notes-paysage (`outils-voix-ia-build-vs-buy`, `briques-produit-ia-build-vs-buy`, `intelligence-de-code-build-vs-buy`, `outils-memoire-rag-gouvernance-juin-2026`) + `economie-agentique-pricing-2026`.
Couvre TOUT : voix, briques produit, productivité, infra/LLMOps, plateformes, intelligence de code.
Frontière : `responsable-ia` = build-vs-buy au niveau DÉCISION stratégique ; `choix-outils-ia` = acte OPÉRATIONNEL outillé.

### 4. `veille-outils-ia` — refresh des notes-paysage (`user-invocable: true`)
Rôle (≠ `cc-news` qui surveille Claude Code) : veille CIBLÉE sur les outils IA marché. Re-vérifie les **faits volatils** (pricing, ⭐ GitHub, valorisations, M&A, outils MORTS type PlayHT/Humanloop) via web search/fetch source primaire, détecte les écarts vs vault, **met à jour les notes** (MCP `update_note`/`insert_section`) + CHANGELOG (rule `changelog-vault.md`).
Lire AVANT : les 4 notes-paysage + `cc-news/SKILL.md` (frontière) + `changelog-vault.md`.
Garde-fou : vérifié-source-primaire vs rapporté ; re-vérifier les pricing à la source AVANT de patcher (les agents hallucinent les chiffres précis — cf `feedback_llm_deep_research_version_numbers`).

### 5. ENRICHIR `responsable-ia`
Ajouter au catalogue 2 lignes de routage : « concevoir un RAG / NeoDocs » → `rag-design` ; « choisir un outil IA (voix/OCR/context engine/LLMOps) » → `choix-outils-ia`. Diff minimal, ne pas réécrire le reste. (+ si phase 0 conclut « FRIA = enrichissement » : l'ajouter ici aussi.)

## Ordre de construction
1. `cc-rag-ref` → 2. `rag-design` → 3. `choix-outils-ia` → 4. `veille-outils-ia` → 5. enrichir `responsable-ia` → 6. `devils-advocate` sur les 4 SKILL.md → présenter à Raphael.

## Vérification finale (empirique)
`git status` + `git diff`. Chaque skill : description ≤ 300 chars UNE ligne, `user-invocable` correct, pas de BOM, section Apprentissage. NE PAS commit/push sans demander.

**Commence par la phase 0 + la séquence canonique (lire les 2 notes-creer-skill EN ENTIER), puis présente ton plan A→B→C→D AVANT de construire.**
