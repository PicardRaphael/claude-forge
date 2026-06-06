# Checklist CLAUDE.md parfait — 4 dimensions

Source : reference-claude-md.md (research LLM juin 2026) + doctrine forge.

---

## 0. Décision — Est-ce vraiment un CLAUDE.md ? (OBLIGATOIRE)

- [ ] C'est du contexte/convention court et stable, toujours-vrai ? → CLAUDE.md OK
- [ ] Ce n'est PAS un workflow multi-étapes réutilisable ? (→ skill à la place)
- [ ] Ce n'est PAS un comportement à garantir déterministement ? (→ hook à la place)
- [ ] Ce n'est PAS du détail folder-specific ? (→ CLAUDE.md imbriqué / `@import`)
- [ ] Mode identifié : création / audit / optimisation ?

## 1. Taille & structure

- [ ] < 200 lignes (`wc -l CLAUDE.md`)
- [ ] Scannable en 90 secondes
- [ ] Orchestrateur (maître court + imports/rules), pas monolithe
- [ ] `@import` à 1 niveau max — pas de labyrinthe récursif
- [ ] Hiérarchie planifiée si monorepo / multi-équipes (racine vs sous-dossiers)

## 2. Contenu

- [ ] Uniquement ce que Claude ne peut pas déduire du code
- [ ] Stack + langages + frameworks présents (3-6 lignes)
- [ ] Commandes exactes et copy-paste ready (dev/test/typecheck/build)
- [ ] Chaque règle **testable** (condition vérifiable) + **raison** (le « parce que »)
- [ ] Section anti-patterns (« ne fais pas X — coût »)
- [ ] Routing vers skills/agents/rules
- [ ] Zéro contenu que Claude sait déjà (« écris du code propre »)
- [ ] Zéro workflow multi-étapes inline (→ skill)
- [ ] Zéro comportement « obligatoire » en texte (→ hook)
- [ ] Zéro info datée non voulue / obsolète
- [ ] Zéro duplication de contenu skill/agent

## 3. Cohérence & enforcement

- [ ] Aucune règle contradictoire (accumulées par couches)
- [ ] Une règle = un seul endroit, au bon mécanisme
- [ ] Le critique-à-garantir est en hook, pas en texte dans CLAUDE.md
- [ ] Routing critique doublé d'un hook si nécessaire

## 4. Maintenance & evals

- [ ] Owner unique désigné
- [ ] Cadence de revue (trimestrielle)
- [ ] Versionné, relu en PR
- [ ] Testé en session fraîche : Claude suit-il les règles sans rappel ?
- [ ] Routing testé : dispatch vers bonnes skills/agents ?
- [ ] Si règle ignorée → la convertir en hook ou la supprimer

---

## Signaux de maladie (audit rapide)

| Signal | Correctif |
|--------|-----------|
| > 200 lignes | Élaguer — passe 1 (supprimer évident/daté/doublons) |
| Règles aspirationnelles | Réécrire en testable + raison |
| Règles sans raison | Ajouter le « parce que » |
| Règles contradictoires | Consolider |
| Contenu Claude sait déjà | Supprimer |
| Détail folder-specific | CLAUDE.md imbriqué / `@import` |
| Workflows inline | Extraire en skill |
| Comportements obligatoires | Migrer vers hook |
| Contenu skill/agent dupliqué | Pointer, pas dupliquer |
| @import récursifs | Aplatir à 1 niveau |
| Pas d'owner/cadence | Instaurer revue trimestrielle |
