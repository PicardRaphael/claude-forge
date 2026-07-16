---
name: vault-health
description: ALWAYS invoke when the user types /vault-health or asks for the weekly vault health check — lint + closed-list fixes, usage trend, cross-repo adoption, inbox, dated report. NOT for deep note fixes (vault-audit) or strategic review (forge-review).
user-invocable: true
allowed-tools: mcp__forge-brain__*, Bash, Write
model: sonnet
effort: medium
---

# vault-health — check santé hebdo du cerveau forge-brain

Routine hebdo légère (cron lundi 09h00 ou invocation manuelle) : mesure la santé du vault, applique UNIQUEMENT les micro-fixes de la liste fermée, écrit un rapport daté dans `Knowledge/reviews/`. Spec d'origine : `TODO/SPEC-loop-vault-health.md`.

## Garde-fous critiques

- **Écritures vault autorisées = liste FERMÉE de l'étape 1 + le rapport de l'étape 5. Rien d'autre.**
- **JAMAIS `delete_note` ni `move_note`** dans cette routine — tout ce qui dépasse la liste fermée se SIGNALE dans le rapport, ne se répare pas.
- Maximum **5 notes modifiées par run** (rapport non compris). Au-delà : signaler.
- Toute erreur MCP à mi-parcours → terminer en FAIL (étape 5), ne jamais boucler ni réessayer plus d'une fois.
- Budget : run court (~10-15 min), session unique, aucun dispatch d'agent.

## Étape 0 — Pré-check MCP

1. Appeler `mcp__forge-brain__vault_stats` comme ping.
2. Si erreur : `REPO=$(git rev-parse --show-toplevel)` puis `py "$REPO/.claude/hooks/mcp-autostart.py"`, attendre ~10 s, retenter UNE fois.
3. Toujours en échec → sauter à l'étape 5 en FAIL (cause = MCP injoignable).

## Étape 1 — Lint + micro-fixes (liste fermée)

1. `lint_vault()` → noter les comptes PRÉ-fixes par catégorie.
2. Fixes autorisés, et eux seuls :
   - **(a) Wikilink brisé vers une NON-note** (skill, rule, fichier, exemple de code) → réécrire en texte nu/backticks via `update_note`. Conditions cumulatives : la cible n'est manifestement pas une note à créer (un wikilink vers une future note est LÉGITIME, cf SCHEMA §3 — dans le doute, signaler au lieu de fixer) ET la note à réécrire fait < 150 lignes (`update_note` remplace tout le contenu — au-delà, le risque de corruption dépasse le gain : signaler).
   - **(b) Aliases < 4** → compléter via `update_property(file, "aliases", [liste])` — maximum 2 notes par run, jamais sur des notes miroirs de sources externes.
3. Re-lancer `lint_vault()` → comptes POST-fixes. La comparaison alimente le triple check (b).

## Étape 2 — Tendance consultation (7 jours)

1. `usage_stats(days=7)`.
2. Chercher le rapport précédent : `list_notes("Knowledge/reviews", limit=20)` → dernier `vault-health-*`. S'il existe, `read_note` et comparer `search_brain` / `read_note` / `create_note` (calls). Sinon noter « première mesure ».
3. Signal d'alerte à reporter : consultation en baisse ≥ 40 % vs rapport précédent, ou create_note > 3× search_brain (vault write-only = début de stagnation — c'est le failure mode documenté dans [[pattern-vault-llm-karpathy]]).

## Étape 3 — Adoption cross-repo

1. `search_tool_events(tool_name="mcp__forge-brain__search_brain", since=<date du rapport précédent, sinon J-7>, limit=50)` puis idem avec `tool_name="mcp__forge-brain__read_note"`.
2. Compter les événements `tool_use` dont le projet ≠ `claude-forge` (le chemin de session dans chaque résultat donne le projet).
3. **Verdict J+14 (à rendre au premier run ≥ 2026-08-03, puis à chaque run)** : ≥ 10 consultations hors forge sur 14 jours = extension vivante. En dessous : RECOMMANDER dans le rapport le retrait de `~/.claude/CLAUDE.md` + note de dette — ne jamais appliquer ce retrait soi-même, c'est un arbitrage Raphael (critère de falsification du DA, cf [[decision-vault-agent-first]] § Validation externe).

## Étape 4 — Inbox

`list_notes("0-Inbox")` → si > 3 notes, les lister dans le rapport comme « à trier ».

## Étape 5 — Rapport + triple check

1. Date du jour : `date +%F` en Bash.
2. `create_note("Knowledge/reviews/vault-health-<YYYY-MM-DD>.md", ...)` avec frontmatter complet (titre, resume spécifique avec les chiffres du run, ≥ 4 aliases, `type: synthese`, `derniere-maj`, tags `#type/synthese` + `#domaine/vault`, wikilinks vers [[pattern-vault-llm-karpathy]] et [[decision-vault-agent-first]]) et QUATRE sections obligatoires :
   - `## Lint` — comptes pré/post, fixes appliqués (liste exacte), signalements
   - `## Consultation (7 j)` — chiffres + tendance + alerte éventuelle
   - `## Adoption cross-repo` — comptage hors forge + verdict (dont J+14)
   - `## Inbox` — état
   Le verdict global **PASS/FAIL** s'écrit en première ligne du corps.
3. **Triple check** (le run se note lui-même) :
   - (a) relire le rapport créé (`read_note`) → les 4 headers présents ;
   - (b) lint POST ≤ lint PRÉ sur chaque catégorie touchée ;
   - (c) zéro erreur MCP pendant le run.
4. Un seul check en échec → FAIL : écrire `$(git rev-parse --show-toplevel)/output/vault-health-FAIL-<date>.md` (tool Write, hors vault) avec la cause et l'état atteint. Si le rapport vault a pu être créé, y noter aussi FAIL en première ligne.

## Gotchas

- La session cron doit tourner avec le repo claude-forge en cwd — le MCP projet, les hooks et `git rev-parse` en dépendent. La convention single-writer autorise `update_note`/`update_property` ici PARCE QUE c'est une session forge.
- Les rapports ont un stem daté unique (`vault-health-YYYY-MM-DD`) → pas d'ambiguïté d'alias ; un second run le même jour écrase le rapport du jour via `create_note` (comportement accepté).
- `search_tool_events` sans filtre `project` renvoie tous les projets — filtrer côté lecture, il n'y a pas de paramètre d'exclusion.
- Ne pas confondre avec `vault-audit` (fixes qualité profonds, à la demande) ni `forge-review` (revue stratégique mensuelle) : vault-health observe et micro-répare, il ne restructure jamais.
- Machine éteinte à l'heure du cron → run manqué, non critique. Le comportement de rattrapage du cron est à observer au premier lundi (noter le constat en Apprentissage).

## Apprentissage

Après chaque run notable : noter ici les patterns observés (rattrapage cron, faux positifs lint, seuils à recalibrer).

- 2026-07-16 (premier run, PASS) : le run ne committe pas (arbitrage « note vault seule ») → il laisse 3+ fichiers vault modifiés dans le working tree. Le commit ultérieur qui les embarque doit ajouter l'entrée `CHANGELOG.md` du vault (rule changelog-vault) — le CHANGELOG n'est PAS dans la liste fermée d'écritures du run, il se traite au moment du commit, hors run. Zéro faux positif lint ; seuls des low_aliases en reliquat (résorption 2/semaine).
