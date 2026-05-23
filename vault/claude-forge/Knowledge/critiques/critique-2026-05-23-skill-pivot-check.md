---
titre: "Critique — skill /pivot-check (audit post-pivot doctrinal)"
type: knowledge
domaine: claude-code
derniere-maj: 2026-05-23
auteur: claude
aliases:
  - "critique pivot-check"
  - "DA pivot-check 23 mai"
  - "critique skill pivot-check"
  - "verdict pivot-check"
tags:
  - "#type/critique"
  - "#domaine/claude-code"
  - "#sujet/skill"
sources:
  - "[[methode-pivoter-doctrine]]"
  - "[[feedback_doctrine_drift_pattern]]"
  - ".claude/skills/pivot-check/SKILL.md"
---

# DA — Critique skill /pivot-check (23 mai 2026)

## Verdict global

**PARTIAL — GO-WITH-FIXES**

La skill est légitime au regard de la doctrine 22 mai (advisory tool, pas hook workflow, scope grep/lint OK). Elle ne duplique pas la canonique vault — elle la **complète** en outillant l'étape 4 (purge MEMORY/RECAP) qui est précisément celle qui a sauté 2× en 2 jours. Mais 3 problèmes opérationnels la rendent fragile en production.

## Objections BLOQUANTES

**B1 — Couverture incomplète de la PURGE (étape 4 canonique)**

La canonique `methode-pivoter-doctrine` étape 4 mentionne explicitement 3 cibles à purger : `MEMORY.md`, `.claude/RECAP.md`, **`.claude/agent-memory/*/MEMORY.md`**. Le tableau de la skill (étape 2 — périmètre) **omet** :
- `.claude/RECAP.md` (cité absent du tableau)
- `.claude/agent-memory/*/MEMORY.md` (cité absent du tableau)

Or c'est précisément cette dernière cible (agent-memory) qui a annulé silencieusement le pivot 22 mai sur neo_ia. Une skill censée détecter le drift Type 1 qui rate la principale source du drift = anti-objectif. **À FIXER avant livraison**.

## Objections FORTES

**F1 — Étape 2 (interactive) incompatible avec auto-trigger**

Description directive `"ALWAYS invoke after correcting a canonical note..."` → l'agent est censé l'auto-trigger. Mais étape 1 demande à l'utilisateur les termes obsolètes en mode interactif. En auto-trigger, l'utilisateur n'est pas là — la skill va soit s'arrêter, soit inventer des termes. **Soit déduire** les termes par diff git de la note canonique modifiée (recommandé), **soit retirer** le "ALWAYS" de la description.

**F2 — Risque doctrinal : "workflow déguisé" — limite acceptable mais risquée**

Doctrine 22 mai : "hooks = lint/security/scope, JAMAIS workflow". Une **skill** advisory pour vérifier conformité doctrinale est légitime (≠ hook bloquant). MAIS l'étape 6 (capitalisation vault automatique) + délégation étape 5 → la skill commence à ressembler à un pipeline workflow. Garder la skill **advisory pure** : rapport + suggestions, **pas d'action automatique**. La capitalisation vault doit rester à la discrétion de la session principale.

**F3 — Scope cross-repo absent**

Question #5 du brief : drifts cross-repo capturés ? Réponse de la skill : non. Le tableau scope `vault/claude-forge/` et `.claude/` du repo courant uniquement. Or `feedback_doctrine_drift_pattern` cite explicitement ia_back et neo_ia comme victimes. Si forge corrige une canonique mais qu'ia_back garde `pipeline-enforcement` dans son MEMORY.md, la skill ne détecte rien. **Ajouter** : si terme obsolète détecté, recommander relancer `/pivot-check` sur les autres repos (Documents/neot-v2/, Documents/neofront/).

## Objections N1-N5

**N1 — Description 269 chars** (sweet spot Anthropic 250). Trim recommandé : retirer "or when the user types /pivot-check" (redondant avec `user-invokable: true`). Cible 220-240.

**N2 — Numérotation divergente** : canonique vault = 5 étapes, skill = 6 étapes (la 6 étant capitalisation). Risque de confusion sur "checklist 5 étapes" vs "skill 6 étapes". Soit aligner (fusionner étapes 5+6), soit clarifier que l'étape 6 est skill-specific.

**N3 — Gotcha manquant** : Grep natif CC sur `vault/claude-forge/` viole la rule "MCP forge-brain UNIQUEMENT pour accès vault" (CLAUDE.md ligne 11). Justification présente (gotcha #4) mais formulation faible — ajouter explicitement que c'est une **dérogation documentée** (et non un oubli) pour cette skill spécifique.

**N4 — Apprentissage vide** : section présente avec hooks à compléter mais zéro exemple. Conforme au pattern forge mais on perd l'opportunité de pré-remplir avec le cas neo_ia 22 mai (qui est précisément la source d'inspiration).

**N5 — `Bash` dans `allowed-tools`** alors que la méthode décrit Grep uniquement. Soit retirer Bash (principle of least privilege), soit documenter pourquoi (probablement `git diff` pour déduire termes obsolètes — voir F1).

## Confirmations (ce qui marche)

- **Légitimité doctrinale** : skill ≠ hook. Pas de blocage workflow. Conforme pivot 22 mai.
- **Non-redondance** : la canonique vault est la **méthode** (humaine, 5 étapes). La skill est l'**outil** (grep cross-files). Complémentaires, pas dupliquées.
- **Délégation aux spécialistes** (étape 5) respecte `delegate-to-specialists.md` + `delegate-guard.py`.
- **Exclusions structurelles** (CHANGELOG, archives, 05-Leaders) bien pensées — anti-pattern faux-positifs documenté + évité.
- **Lien vers `methode-pivoter-doctrine`** explicite — single source of truth respectée.

## Recommandation

**GO-WITH-FIXES** — applicable après B1 + F1 + F2.

Priorité de fix :
1. **B1 (bloquant)** : ajouter `RECAP.md` + `agent-memory/*/MEMORY.md` au scope étape 2
2. **F1** : décider auto-trigger (déduction via git diff) OU interactif (retirer ALWAYS) — pas les deux
3. **F2** : étape 6 capitalisation = recommandation, pas exécution
4. **F3** : ajouter recommandation cross-repo
5. N1-N5 : nice-to-have

Une fois B1+F1+F2 traités, la skill est solide et résout effectivement le pattern `feedback_doctrine_drift_pattern`. La transformer en hook PreCommit serait **anti-pattern doctrinal** (refusé 22 mai pour `doctrine-drift-guard.py`) — la skill advisory reste le bon outil.

## Wikilinks

- [[methode-pivoter-doctrine]] — canonique inspirante
- [[critique-2026-05-22-doctrine-drift-guard]] — DA qui a refusé l'approche hook (précédent direct)
- [[raisonnement-22mai-doctrine-vs-enforcement]] — doctrine source
- [[feedback_doctrine_drift_pattern]] — pattern reproduit 2× en 2 jours

