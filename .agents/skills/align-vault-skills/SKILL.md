---
name: align-vault-skills
description: ALWAYS invoke when checking doctrine alignment between the forge-brain vault and the cc-*-ref skills + agents. Scans both ways, reports NEW gaps only. Use for the weekly /loop alignment watch.
argument-hint: "[optionnel : composant ou thème à cibler]"
allowed-tools: Read, Glob, Grep, Bash, mcp__forge-brain__search_brain, mcp__forge-brain__read_note, mcp__forge-brain__read_note_by_path, mcp__forge-brain__read_section, mcp__forge-brain__list_notes
user-invocable: true
model: opus
effort: high
---

# align-vault-skills — Veille d'alignement vault ↔ composants

Compare la doctrine du vault forge-brain avec les skills de référence (`cc-*-ref`) et les agents `.claude/agents/`, **dans les deux sens**, et produit un rapport des **NOUVEAUX** écarts uniquement (idempotent). Conçue pour tourner en `/loop` hebdo sur la machine locale.

Un écart silencieux = un composant qui enseigne une doctrine périmée ou incomplète. Cas déclencheur historique : `/goal` + Agent View documentés au vault mais absents de `cc-features-ref` (trouvé à la main le 5 juin 2026).

## Ce que cette skill n'est PAS

- **PAS `/skill-evolve`** — skill-evolve améliore l'efficacité d'UNE skill (patterns d'exécution, cross-pollination). Ici on vérifie la **cohérence doctrinale** vault↔composant, pas la qualité interne.
- **PAS `/forge-review`** — forge-review est un challenge stratégique mensuel (KILL/EVOLVE/KEEP/MISSING) du setup. Ici, scan **bidirectionnel automatisé, idempotent, factuel** : « telle doctrine vault est-elle reflétée tel composant, oui/non ». Pas de jugement stratégique.
- **PAS un correcteur** — produit un rapport + commandes de dispatch suggérées. JAMAIS de modif de composant (delegate-guard l'impose).

## Étapes

### 1. Kill-switch + état (Python, EN TÊTE — obligatoire)

```bash
python3 .claude/skills/align-vault-skills/scripts/alignment_state.py check
```

Le JSON retourné porte `stop`, `date`, `state_path`, `resolved`, `ignored`.

- Si `stop: true` (fichier `.claude/.alignment-loop.stop` présent) → **STOP IMMÉDIAT**. Ne rien scanner, ne rien écrire. Afficher « kill-switch actif, arrêt » et terminer.
- Sinon, retenir `date` (jamais recalculée côté skill) et l'état (clés déjà traitées/ignorées).
- Le 1er run matérialise `_alignment-state.json` vide `{"resolved":[],"ignored":[]}`.

### 2. Lister les composants à scanner (couverture)

- 6 skills-ref : `.claude/skills/cc-*-ref/SKILL.md` (`Glob`).
- Agents : `.claude/agents/*.md` (`Glob`).
- Si `$ARGUMENTS` cible un composant/thème précis, restreindre à celui-ci (sinon scan complet).

Compter le nombre attendu (`expected`). C'est le dénominateur de la couverture.

### 3. Scanner chaque composant dans les 2 sens

Pour chaque composant : lire son body via `Read`/`Grep` (extraire les affirmations doctrinales + wikilinks cités). Puis comparer au vault via MCP forge-brain, **borné à N=3-4 notes** par sujet (SEARCH → SELECT → READ) :

```
mcp__forge-brain__search_brain(query="<doctrine du composant>", limit=4)
→ sélectionner les 3-4 notes les plus pertinentes
→ mcp__forge-brain__read_note(file="<note>") sur celles qui tranchent
```

Détecter dans les **deux sens** :
- **Descendant** (vault → composant) : une doctrine/feature canonique du vault est absente d'un composant qui devrait la refléter. → action « ajouter X ».
- **Montant** (composant → vault) : une affirmation du composant est absente ou contredite par le vault. → marquer **« à arbitrer »** : peut être légitime (composant plus récent que le vault), pas forcément à corriger.

Chaque écart candidat = `{component, direction (descendant|montant), note, action}`.

### 4. Filtrer les écarts déjà connus (idempotence — en raisonnement, pas de fichier)

L'étape 1 (`check`) a déjà renvoyé les tableaux `resolved` et `ignored`. Pour chaque écart candidat, construire sa clé composite `component::note::direction` (exactement le format de `make_key`) et **écarter en raisonnement** ceux dont la clé est dans `resolved` ou `ignored`. Aucun fichier temporaire : la clé est une simple concaténation lisible que le LLM produit de façon déterministe à partir des 3 champs déjà en main.

Ne restent que les **nouveaux** écarts → eux seuls vont au rapport. Pas de re-signalement, pas de fatigue de lecture.

> Le script expose un sous-commande `filter --gaps <json>` équivalente, mais elle exige de matérialiser un JSON candidat — inutile ici (pas de tool Write, et un heredoc Windows avec du JSON généré par le LLM casse silencieusement). Le filtrage en raisonnement est volontaire et suffisant : il ne touche aucun fichier.

### 5. Vérification PASS/FAIL (composite)

- **Couverture** : `scanned == expected` ET `expected > 0` (mécanique, via le count étape 2).
- **Reproductibilité** : la comparaison sémantique est un jugement LLM instable. Garde principale = 2 passes doivent concorder sur le même set d'écarts. **Pas un double-scan complet obligatoire chaque cycle** (coût) — c'est une méthode de spot-check : re-scanner un échantillon de composants et confirmer le même verdict. Documenter dans le verdict.
- **Échantillon (0 faux positif)** : relire 3-5 écarts signalés, confirmer qu'ils sont réels (note vault citée existe, affirmation composant exacte).

`pass: true` seulement si les 3 tiennent. Afficher le verdict.

### 6. Écrire le livrable (Python)

Composer le payload JSON `{date, coverage, verdict, new_gaps}` (cf `references/livrable-format.md`) dans un fichier temporaire, puis :

```bash
python3 .claude/skills/align-vault-skills/scripts/alignment_state.py write-report --payload <payload.json>
```

Le script écrit `TODO/alignment-report-<date>.md` (date résolue côté Python à l'étape 1, jamais en JS/skill) et renvoie son chemin.

### 7. Restituer

Afficher : chemin du rapport + verdict de vérification + nombre de nouveaux écarts. **Ne pas déclencher les dispatches** — Raphaël relit et tranche. Les clés ne passent en `resolved`/`ignored` que sur action humaine en session interactive (`resolve`/`ignore` du script), pas par le loop.

## Idempotence & état

Détail complet : `references/state-schema.md`. En bref : clé composite lisible `component::note::direction` (PAS un hash — un LLM ne produit pas de hash stable, ça casserait la reproductibilité). L'état n'est mis à jour qu'en fin de cycle après écriture du livrable ; un scan interrompu se relance de zéro (lecture seule, aucun effet de bord).

## Gotchas

**Kill-switch EN TÊTE, avant tout scan.** L'étape 1 (`check`) est la première chose exécutée. Si `.claude/.alignment-loop.stop` existe, on s'arrête sans rien lire ni écrire. Tester le flag plus tard = avoir déjà consommé des tokens MCP pour rien.

**Date via Bash, JAMAIS `Date.now` ni date en dur.** Le nom du livrable `alignment-report-<date>.md` vient de `resolve_date()` (commande OS `date`). Une date hallucinée par le LLM corromprait l'horodatage des runs et la rétention 30 j.

**JAMAIS modifier un skill/agent directement.** Cette skill produit un rapport + des commandes de dispatch suggérées. La correction passe par `skill-creator`/`subagent-creator` après validation Raphaël. `delegate-guard` bloque de toute façon l'édit direct d'un SKILL.md / agent.

**Écart montant = « à arbitrer », pas « à corriger ».** Un composant peut être plus récent que le vault (skill mise à jour avant capitalisation). Ne jamais formuler d'office « corriger le composant » pour un écart montant — proposer l'arbitrage (mettre à jour le vault OU corriger le composant).

**La comparaison sémantique est un jugement LLM → reproductibilité = garde.** « Cette note vault ≈ cette section skill ? » est flou et instable. Le critère de reproductibilité (2 passes concordantes) est la défense principale contre les hallucinations. Si deux passes divergent beaucoup → le verdict est FAIL, affiner le critère avant de fiabiliser.

**Borner le scan à N=3-4 notes vault par sujet.** Ne pas explorer le vault en grand (coût + bruit). SEARCH/SELECT/READ : les snippets `search_brain` identifient les candidates, on ne `read_note` que celles qui tranchent. Scan borné aux composants listés, pas d'exploration ouverte (SPEC §7 cap coût).

**Tout I/O fichier passe par le script Python.** `allowed-tools` n'inclut pas Write/Edit volontairement (spec) : le helper `alignment_state.py` écrit le livrable `.md` ET l'état `.json` via Python, donc Bash ne fait jamais que `python3 scripts/...` et `date`. Cela contourne aussi la casse heredoc Windows (contenu LLM dans un heredoc casse silencieusement). Le nom de la skill contient « vault » mais `vault-cat-guard` ne se déclenche pas : il faut une commande de lecture (cat/grep/...) co-occurrente avec le chemin `vault/claude-forge`, ce qui n'arrive jamais ici.

**En `/loop` non supervisé : scan seul, jamais resolve/ignore automatique.** Le loop LIT l'état et écrit le rapport. Marquer un écart `resolved`/`ignored` est une action humaine (sinon un écart réel disparaît sans correction). Le loop ne ferme jamais une boucle tout seul.

## Exemples

```
# Scan complet (tous composants), en interactif
/align-vault-skills

# Cibler un composant
/align-vault-skills cc-features-ref

# Loop hebdomadaire
/loop 7d /align-vault-skills

# Stopper le loop : créer le flag
#   .claude/.alignment-loop.stop
```

## Apprentissage

Après un cycle significatif, capitaliser :
- **Faux positif récurrent** sur un type de comparaison → affiner le critère de jugement (étape 3) et le documenter ici. Si ça persiste → V2 = 2e agent validateur (SPEC §5).
- **Pattern d'écart récurrent** (ex : cc-news capitalise au vault mais oublie systématiquement de propager à cc-features-ref) → le signaler dans `Knowledge/erreurs/` du vault et envisager un garde-fou en amont.
- **Divergence entre 2 passes** sur les mêmes composants → noter quels sujets sont instables (jugement LLM fragile) pour calibrer la reproductibilité.
- Sauvegarder en mémoire projet le nombre d'écarts résolus/ignorés cumulés pour suivre le drift dans le temps.

```
# Format mémoire projet
project_alignment_loop.md :
  - Date dernier run : YYYY-MM-DD
  - Composants scannés : N
  - Nouveaux écarts : N (descendants / montants)
  - Résolus cumulés : N | Ignorés cumulés : N
  - Verdict : PASS/FAIL
```

## Références

- `references/livrable-format.md` — payload JSON + structure du rapport + sens descendant/montant.
- `references/state-schema.md` — schéma `_alignment-state.json` + clé d'idempotence.
- SPEC source : `TODO/SPEC-loop-alignement-vault-skills.md`.
