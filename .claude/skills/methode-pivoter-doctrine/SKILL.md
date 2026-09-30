---
name: methode-pivoter-doctrine
description: ALWAYS invoke when a forge canonical doctrine is invalidated by new evidence (Anthropic update, empirical measurement, audit verdict). Executes 5-step checklist to pivot without residual drift. DO NOT pivot doctrine without invoking first.
user-invocable: true
allowed-tools: Read, Grep, Glob, Write, Edit, Bash, mcp__forge-brain__read_note, mcp__forge-brain__update_note, mcp__forge-brain__create_note
model: opus
effort: medium
---

# Méthode pivot doctrinal — sans régression silencieuse

Chaque pivot doctrinal majeur DOIT traverser les 5 étapes ci-dessous. Sans l'étape 4 (purge MEMORY/RECAP), le pivot est **invisiblement annulé** à chaque nouvelle session.

**Incident origine** : pivot 22 mai 2026 neo_ia — rules mises à jour, MEMORY/RECAP non purgés → ancienne doctrine réactivée 10 jours sans détection.

---

## Critère d'application

### Pivot MAJEUR — checklist complète (5 étapes)
- Suppression/ajout de hooks workflow
- Changement structurel du pipeline (TDD strict → conditionnel)
- Suppression/ajout d'agent critique
- Changement de modèle/effort par défaut
- Renaming de patterns structurants

### Évolution MINEURE — checklist légère (étapes 2-3-5)
- Modification d'une seule rule
- Ajout d'un nouveau skill
- Renaming non doctrinal

---

## Checklist 5 étapes

### Étape 1 — Note canonique vault
Créer ou mettre à jour `raisonnement-<date>-<sujet>.md` dans `Knowledge/raisonnements/` via `mcp__forge-brain__create_note`. Cette note est la source de vérité (motivation, décisions, hooks supprimés, rules modifiées).

### Étape 2 — Rules du repo
Pour chaque repo concerné :
- Mettre à jour `.claude/rules/` (quality-gates, when-to-architect, orchestrator-mindset)
- Supprimer les rules devenues obsolètes
- Vérifier `description:` frontmatter présent (sinon rule MORTE silencieusement)

### Étape 3 — CLAUDE.md (racine + secondaires)
- Mettre à jour CLAUDE.md racine
- Mettre à jour CLAUDE.md secondaires (`apps/*/CLAUDE.md`, `packages/*/CLAUDE.md`)
- Ajouter bloc STOP avant ligne 25 si pivot critique

### Étape 4 — PURGE MEMORY / RECAP / agent-memory ⚠️ CRITIQUE
**L'étape la plus oubliée.** C'est elle qui crée la régression silencieuse.

- `MEMORY.md` racine : supprimer ou réécrire les entrées contradictoires
- `.claude/RECAP.md` : refonte complète si pipeline a pivoté
- `.claude/agent-memory/*/MEMORY.md` : vérifier chaque dossier agent
- **Préférer marquer plutôt que supprimer** : préfixer `[OBSOLÈTE <date>]` ou pointer vers la note canonique du pivot

### Étape 4bis — GATE `pivot-check` (validateur PASS/FAIL avant le test) ⚠️
Avant de passer en session fraîche, verrouiller la purge avec un gate statique :
- Invoquer la skill `pivot-check` (détection statique du drift Type 1 : claims obsolètes survivants dans rules / CLAUDE.md / MEMORY / RECAP).
- **PASS** = zéro drift Type 1 → passer à l'étape 5.
- **FAIL** = au moins un claim obsolète survit → **retour étape 4** (purge incomplète), puis re-gate.

Complémentarité (les deux sont nécessaires) : `pivot-check` = vérif **statique** (le drift résiduel est-il purgé du texte ?) ; étape 5 = vérif **comportementale** (la session re-propose-t-elle l'ancienne doctrine ?). Ce gate est **skill-invoqué** (logique interne à cette skill), jamais un hook — cohérent avec le gotcha « pas de hook substring-matching sur MEMORY/RECAP » ci-dessous (`pivot-check` juge, un hook matcherait à l'aveugle).

### Étape 5 — Test session fraîche
- Lancer une nouvelle session Claude Code dans le repo
- Demander une tâche typique (feature, bug fix)
- Vérifier que la session NE PROPOSE PAS la doctrine pré-pivot
- Si l'ancienne doctrine ressurface → retour étape 4, audit plus profond

---

## Gotchas

- **Ne PAS créer un hook substring-matching** sur MEMORY/RECAP : signal-to-noise = 0 par construction (la doc correcte du pivot mentionne toujours l'ancienne doctrine pour la déclarer obsolète → 26/26 faux positifs sur neo_ia post-purge). Hook workflow = anti-pattern doctrine 22 mai.
- **Ne PAS modifier uniquement les rules** sans étape 4 : le pivot reste actif en rules mais MEMORY/RECAP réactivent l'ancienne doctrine à chaque session.
- **Ne PAS supprimer brutalement** les entrées contradictoires : préfixer `[OBSOLÈTE]` + pointer vers note canonique pour garder la traçabilité.
- **Ne PAS sauter l'étape 5** : sans test session fraîche, la régression reste latente plusieurs sessions.
- Les CLAUDE.md secondaires (`apps/*/`, `packages/*/`) sont souvent oubliés — les auditer explicitement.

---

## Anti-patterns observés

- ❌ Pivot par rules seule → régression silencieuse MEMORY/RECAP
- ❌ Hook palliatif doctrine-drift-guard → auto-réfutant par construction
- ❌ Suppression brutale → perd traçabilité historique
- ❌ Pas de test session fraîche → régression latente non détectée

---

## Référence

Source canonique vault : `[[methode-pivoter-doctrine]]` (`04-Techniques/claude-code/`)
Pivot exemple : `[[raisonnement-22mai-doctrine-vs-enforcement]]`
DA critique du hook palliatif : `[[critique-2026-05-22-doctrine-drift-guard]]`

---

## Apprentissage

Après chaque pivot doctrinal appliqué avec cette méthode, sauvegarder en mémoire projet :
- Le repo concerné
- Les étapes ayant requis le plus de travail
- Tout résidu trouvé à l'étape 4 non attendu (type de fichier oublié)

Mettre à jour `vault/Knowledge/raisonnements/<nom-pivot>.md` avec le bilan de conformité par étape.
