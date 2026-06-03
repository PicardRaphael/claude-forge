---
name: spec
description: Use when user describes a need, pastes a Jira ticket, or asks for spec before implementing. Transforms ticket/idea/bug into TODO/feature-X/ folder with SPEC.md, BRIEFs, parallel waves. STOPS at file generation — never develops code.
argument-hint: "[ticket text, paste it, or describe in natural language]"
allowed-tools: Read, Write, Glob, Grep, Bash, Task, AskUserQuestion
user-invocable: true
model: opus
effort: high
memory: project
skills:
  - neo-brain-dev-ia
---

# /spec — Ticket/Idée → TODO/ structuré

Transforme un ticket, une idée floue ou un bug en dossier `TODO/feature-<nom>/` ou `TODO/fix-<nom>/`.

> **STOP CRITIQUE — règles non-négociables :**
> - Ne commit pas. Ne lance pas `/go`. Ne touche pas au code applicatif.
> - Ne modifie aucun fichier hors de `TODO/feature-<nom>/` ou `TODO/fix-<nom>/`.
> - Ne modifie JAMAIS un autre repo (ex: neo_ia depuis ia_back). Génère le BRIEF dans `TODO/` du repo courant. L'utilisateur copie manuellement.
> - La skill s'arrête au gate de validation Phase 4. Tout dev est HORS scope.

Taille par défaut : **M**. Re-calibration obligatoire après Phase 2. Pas de taille S.

---

## Phase 1 — Interview (max 8-10 questions)

Lire `$ARGUMENTS`. Si format Jira structuré détecté (`### Détail métier`, `### Règles de gestion RG-X`, `### Contexte technique`) : raccourcir l'interview aux points non couverts.

AskUserQuestion — max 4 questions par appel, 2 appels max :
- Batch 1 (universel) : type / repos touchés / critères de succès / contraintes
- Batch 2 (spécifique au type) : voir `references/interview-bank.md`

---

## Phase 2 — Exploration (ne jamais skipper)

Lancer en parallèle selon contexte :
- **Agent `codebase-analyst`** sur le repo courant (code existant, patterns similaires)
- **Agent `db-inspector`** si tables BDD impliquées
- **MCP `postgres`** (`mcp__postgres__query`) pour vérifications précises de colonnes/types/FK — disponible dans ia_back et neo_ia
- **Skill `neo-brain-dev-ia`** (MCP `neoteem-brain-dev-ia`) pour contexte cross-repo BDD/ia_back/neo_ia — disponible dans ia_back et neo_ia
- **Glob/Read READ-ONLY** sur autres repos si multi-repo (jamais Write hors `TODO/`)

Re-calibration taille après exploration :

| Taille | Critères |
|--------|---------|
| M | 1 repo, < 5 fichiers à toucher |
| L | 2+ repos OU < 15 fichiers |
| XL | 2+ repos, 15+ fichiers, multi-sprint |

---

## Phase 3 — Architecture

- **Agent `architect`** avec outputs Phase 2 en contexte
- **Agent `api-designer`** si endpoints à créer
- XL : 2-3 approches (minimal / clean / pragmatic) avec tradeoffs
- M / L : approche pragmatique par défaut, alternatives notées sans bloquer
- PAS d'AskUserQuestion bloquant en Phase 3 (sauf override utilisateur)

---

## Phase 4 — Génération

Créer `TODO/feature-<nom>/` ou `TODO/fix-<nom>/` à la racine du repo courant.

| Taille | Structure |
|--------|-----------|
| M | SPEC.md + BRIEF.md |
| L | SPEC.md + BRIEF-IA-BACK.md + BRIEF-NEOIA.md + BRIEF-FRONT.md (si besoin) |
| XL | 00-vision + 01-architecture + 02-endpoints + 03-tools + 04-priorites + BRIEFs |

Templates complets dans `references/output-templates.md`.

Tout BRIEF doit inclure : Contexte (Phase 2) · À faire (QUOI) · Fichiers · Critères de done · Référence BDD · Implementation Notes · Acceptance Tests.

Implementation Notes : chaque BRIEF mentionne de maintenir `docs/implementation-notes/<feature>.md` pendant l'implémentation (pattern running-notes).

Si multi-BRIEF : exécuter le contradiction check (`references/contradiction-prompt.md`).

### Gate de validation OBLIGATOIRE — fin Phase 4

Après écriture de tous les fichiers :

1. Afficher la liste des fichiers générés + chemin `TODO/`
2. **AskUserQuestion bloquant** :
   - Option A : "STOP — j'inspecte les specs avant de décider" ← **recommandé, par défaut**
   - Option B : "Ajuster un point avant validation"
   - Option C : "OK pour /go — implémenter maintenant"
3. Si A ou B → skill se termine immédiatement. Zéro action supplémentaire.
4. Si C → afficher uniquement : *"Lance `/go` toi-même pour démarrer l'implémentation."* La skill NE lance JAMAIS `/go`.

---

## Phase 5 — Vagues parallèles

**CONDITIONNEL — lancer UNIQUEMENT si taille XL OU si utilisateur a demandé explicitement.**
Si taille M ou L et pas de demande explicite : SKIP Phase 5, terminer après gate Phase 4.

Étapes (voir `references/decompose-waves.md` pour format complet) :
1. Vérifier l'existant via `neo-brain-dev-ia` par CU (OBLIGATOIRE — non sautée)
2. Cartographier les couches (bdd lecture seule / backend / LLM)
3. Organiser en vagues (règle d'or : pas de collision de fichiers, pas de dépendances implicites)
4. Résoudre les POs activement (chercher dans vault + repos avant d'exposer)
5. Validation croisée 3 checks (voir `references/cross-validation.md`) — preuve citée obligatoire
6. Écrire `EXECUTION-PLAN.md` dans `TODO/feature-<nom>/`

Inclure TDD pipeline (architect → test-writer red → dev → refactor → code-reviewer) dans chaque tâche de vague.

---

## Gotchas

- **JAMAIS développer dans /spec** — génère SPEC/BRIEF et STOP. Appel à `/go`, dev-agent ou modification de code hors `TODO/` = violation.
- **JAMAIS écrire dans un autre repo** — ne pas créer/modifier de fichiers hors du repo courant. L'utilisateur copie manuellement.
- **Gate AskUserQuestion obligatoire** — pas de transition automatique vers l'implémentation.
- **Re-calibration après Phase 2, pas avant** — l'exploration change souvent la taille estimée.
- **Pas de contenu spéculatif** — tout vient de Phase 1 ou Phase 2. Si info manque : "à confirmer".
- **Skip Phase 2 = JAMAIS** — même feature "simple", l'exploration révèle code réutilisable ou conflits.
- **Phase 5 conditionnel** — M/L sans demande explicite : NE PAS lancer la Phase 5.
- **Paths via `${NEOT_V2_ROOT}`** — jamais de paths utilisateur hardcodés.
- **Format Jira autodétecté** — si argument contient `### Détail métier` → raccourcir l'interview, mais Phase 2 reste OBLIGATOIRE.
- **Stack-agnostic** — ce SKILL.md master se déploie sur ia_back et neo_ia. Conventions spécifiques par stack dans `references/stack-conventions.md`.
- **QUOI, pas COMMENT** — les BRIEFs ne prescrivent pas de patterns ou d'architecture. Les rules du repo cible s'en chargent.

---

## Format HTML alternatif (Thariq Shihipar — Anthropic mai 2026)

Pour features L/XL avec besoin de visuel (mockups, diagrammes, comparaisons), proposer en **bonus** un fichier `plan.html` interactif en plus du `SPEC.md` Markdown.

**Quand proposer HTML** :
- Feature L/XL multi-repo (taille déterminée Phase 1)
- Spec destinée à review humaine collaborative (Raphael + équipe)
- Besoin de mockups UI / diagrammes architecture / comparaison d'approches side-by-side
- Document persistant qui sera relu plusieurs fois

**Quand garder Markdown seul** :
- Feature M mono-repo (default)
- Spec consommée par un autre LLM sans humain dans la boucle
- Document court (< 50 lignes)
- Diff git fortement nécessaire (HTML diff = bruit)

**Si Phase 1 détermine taille L/XL** → en Phase 4 (génération) : produire `SPEC.md` **ET** `plan.html` (single file, CSS inline, sections scrollables, mockups CSS si UI touchée).

**Template HTML minimal** :

```html
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Plan — feature-<slug></title>
<style>
  body { font-family: system-ui; max-width: 1100px; margin: 2rem auto; padding: 0 1.5rem; line-height: 1.6; }
  section { border-left: 3px solid #4f46e5; padding: 0.5rem 1rem; margin: 1.5rem 0; background: #f9fafb; }
  .risk-low { background: #d1fae5; padding: 2px 8px; border-radius: 4px; font-size: 0.85em; }
  .risk-med { background: #fef3c7; padding: 2px 8px; border-radius: 4px; font-size: 0.85em; }
  .risk-high { background: #fee2e2; padding: 2px 8px; border-radius: 4px; font-size: 0.85em; }
  .mockup { border: 2px dashed #cbd5e1; padding: 1rem; border-radius: 8px; margin: 1rem 0; }
  pre { background: #1e293b; color: #f1f5f9; padding: 1rem; border-radius: 6px; overflow-x: auto; }
  nav { position: sticky; top: 0; background: white; padding: 1rem; border-bottom: 1px solid #e5e7eb; }
</style>
</head>
<body>
<nav>
  <a href="#vision">Vision</a> · <a href="#archi">Architecture</a> · <a href="#tasks">Tâches</a> · <a href="#risks">Risques</a>
</nav>
<h1>Feature — <slug></h1>
<section id="vision"><h2>Vision</h2><!-- ... --></section>
<section id="archi"><h2>Architecture</h2><!-- mockup/diagramme --></section>
<section id="tasks"><h2>Tâches par vague</h2><!-- ... --></section>
<section id="risks"><h2>Risques</h2><!-- <span class="risk-high">HIGH</span> ... --></section>
</body>
</html>
```

Référence canonique : [[html-vs-markdown-thariq]]

---

## Apprentissage

- 2026-05-20 : fusion `/spec` + `/decompose-ticket` en skill unifiée. Cause : duplication cross-repo générait drift, instruction STOP noyée en gotcha causait bug Jérôme (dev direct sans SPEC, touche neo_ia depuis ia_back). Fix : STOP CRITIQUE en gras ligne 1, gate AskUserQuestion obligatoire, Phase 5 conditionnel XL.
- 2026-05-20 : master stack-agnostic créé — conventions Bun/postgres.js/Drizzle/Hono (ia_back) et Python/FastAPI (neo_ia) déportées dans `references/stack-conventions.md`.
- Pattern Thariq running-implementation-notes intégré : chaque BRIEF mentionne `docs/implementation-notes/<feature>.md`.

---

## Références

- `references/interview-bank.md` — banque de questions par type
- `references/output-templates.md` — templates SPEC/BRIEF M/L/XL stack-agnostic
- `references/contradiction-prompt.md` — check contradictions multi-BRIEFs
- `references/decompose-waves.md` — format vagues parallèles (Phase 5 XL)
- `references/cross-validation.md` — 3 checks pré-génération vagues
- `references/stack-conventions.md` — conventions spécifiques ia_back (TS/Bun) et neo_ia (Python)
