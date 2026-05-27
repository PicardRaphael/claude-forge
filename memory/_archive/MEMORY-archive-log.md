# MEMORY — Journal d'archivage (append-only)

Journal **append-only** des feedbacks/références retirés de `memory/MEMORY.md` et déplacés vers `memory/_archive/YYYY-MM/`. Ne JAMAIS modifier une entrée après écriture — uniquement ajouter en bas.

Chaque entrée trace : quand, quoi, pourquoi, où (chemin archive), comment rollback.

## Format

```
## [YYYY-MM-DD] <action> — <résumé court>
- **Fichiers** : <slug-original> → memory/_archive/YYYY-MM/<slug>.md
- **Raison** : <pourquoi archivé : obsolète doctrine X / fusionné dans <méta-feedback> / désindexé>
- **Méta-feedback** (si fusion) : <slug du feedback consolidé qui remplace>
- **Index MEMORY.md** : entrée(s) retirée(s) / ajoutée(s)
- **Rollback** : copier memory/_archive/YYYY-MM/<slug>.md → memory/<slug>.md + ré-ajouter l'entrée index
```

## Rollback — procédure générale

1. Localiser l'entrée dans ce journal (recherche par slug ou date).
2. Copier le(s) fichier(s) depuis `memory/_archive/YYYY-MM/` vers `memory/`.
3. Restaurer l'entrée index dans `memory/MEMORY.md` (section Feedback/Reference/Project).
4. Si une fusion avait créé un méta-feedback : décider s'il reste (couvre d'autres cas) ou s'il est retiré.
5. NE PAS supprimer l'entrée de ce journal — ajouter une nouvelle entrée `[date] rollback — <slug>` à la place.

---

## Entrées

## [2026-05-27] archivage — 2 feedbacks auto-déclarés obsolètes (doctrine pivot 22 mai)
- **Fichiers** :
  - `feedback_hooks_enforcement_pattern` → memory/_archive/2026-05/feedback_hooks_enforcement_pattern.md
  - `feedback_markers_pipeline_complete` → memory/_archive/2026-05/feedback_markers_pipeline_complete.md
- **Raison** : les deux fichiers se déclarent eux-mêmes "OBSOLÈTE depuis 22 mai 2026 — Conservé en archive" dans leur propre description. Le pattern marker+guard pour forcer un workflow agentique (architect → dev → reviewer) est un anti-pattern selon la doctrine pivot 22 mai ([[raisonnement-22mai-doctrine-vs-enforcement]]). Étaient restés dans `memory/` (non indexés) faute de vrai dossier `_archive/` jusqu'à aujourd'hui.
- **Méta-feedback** : néant (archivage sec, pas fusion). Doctrine vivante = [[feedback_enforce_not_advise]] (hooks = lint/sécu/scope).
- **Index MEMORY.md** : aucune entrée à retirer (étaient déjà orphelins, jamais indexés).
- **Rollback** : copier les 2 fichiers depuis _archive/2026-05/ vers memory/ — mais déconseillé (doctrine révoquée).

## [2026-05-27] archivage — marker-ttl-antipattern (orphelin, doctrine pivot 22 mai)
- **Fichiers** : `feedback_marker_ttl_pattern` → memory/_archive/2026-05/feedback_marker_ttl_pattern.md
- **Raison** : cœur du feedback = TTL sur markers architect/commit-guard, dispositif de workflow enforcement déclaré anti-pattern par la doctrine pivot 22 mai ([[raisonnement-22mai-doctrine-vs-enforcement]]). Frères déjà archivés (hooks_enforcement_pattern, markers_pipeline_complete). Les 2 résidus valides hors-workflow (async:true sur PostToolUse quality, éviter hooks user-level globaux) sont déjà couverts par la note canonique vault [[comment-creer-hook]] — pas de perte nette.
- **Méta-feedback** : néant. Doctrine vivante = [[feedback_enforce_not_advise]].
- **Index MEMORY.md** : aucune entrée à retirer (orphelin, jamais indexé).
- **Rollback** : copier depuis _archive/2026-05/ vers memory/ — déconseillé (cœur obsolète).

## [2026-05-27] archivage — neoteem-brain-vault-pipeline (pollution cross-repo)
- **Fichiers** : `feedback_neoteem_brain_pipeline` → memory/_archive/2026-05/feedback_neoteem_brain_pipeline.md
- **Raison** : feedback décrivant un pipeline d'agents propre au repo **neoteem-brain** (repo-analyzer → vault-linker → sync-checker), n'a rien à faire dans la mémoire de claude-forge = pollution conceptuelle cross-repo. claude-forge ne capitalise QUE ce qui concerne claude-forge. Un éventuel système de pipeline neoteem-brain doit vivre dans le repo neoteem-brain, pas via un feedback forge. Pas d'obsolescence doctrinale — mauvais repo.
- **Méta-feedback** : néant.
- **Index MEMORY.md** : aucune entrée à retirer (orphelin, jamais indexé).
- **Rollback** : si besoin, recréer le feedback DANS le repo neoteem-brain (pas ici).

## [2026-05-27] archivage — vault-query-before-create (orphelin, hook supprimé + doctrine 22 mai)
- **Fichiers** : `feedback_vault_query_before_create` → memory/_archive/2026-05/feedback_vault_query_before_create.md
- **Raison** : double motif vérifié empiriquement. (1) Factuel : le hook `vault-query-guard.py` qu'il documente est ABSENT de `.claude/hooks/` (vérif `ls` directe) et de `settings.json` — déjà retiré. (2) Doctrinal : un hook qui bloque Write tant que le vault n'a pas été consulté = workflow enforcement, contredit le pivot 22 mai et la rule actuelle `vault-consultation-protocol.md` (« Pas d'enforcement par hook »). Doctrine vivante = consultation vault advisory.
- **Méta-feedback** : néant. Doctrine vivante = `.claude/rules/vault-consultation-protocol.md` + [[feedback_enforce_not_advise]].
- **Index MEMORY.md** : aucune entrée à retirer (orphelin, jamais indexé).
- **Rollback** : déconseillé (hook supprimé ET doctrine révoquée).

## [2026-05-27] fusion A1 — vérifier les claims empiriquement
- **Fichiers** : feedback_audit_claims_after_brief → memory/_archive/2026-05/feedback_audit_claims_after_brief.md, feedback_sub_agent_claim_sans_empirie → memory/_archive/2026-05/feedback_sub_agent_claim_sans_empirie.md
- **Raison** : doublon conceptuel — `sub_agent_claim_sans_empirie` se déclarait lui-même « extension exacte de audit_claims_after_brief sur les sub-agents éditeurs ». Même réflexe (vérifier un claim avant de le relayer), 2 portées (brief général + sub-agent éditeur) consolidées.
- **Méta-feedback** : feedback_verifier_claims_empiriquement.md (aliases `audit-claims-after-brief`, `audit-claims-after-brief-or-subagent`, `sub-agent-claim-sans-empirie` pour préserver les 8+2 backlinks entrants).
- **Index MEMORY.md** : entrées `audit-claims-after-brief` et `sub-agent-claim-sans-empirie-verifier-post-dispatch` retirées / entrée `verifier-claims-empiriquement` ajoutée.
- **Rollback** : git mv les 2 fichiers depuis _archive/2026-05/ vers memory/, supprimer le méta-feedback, restaurer les 2 lignes index.

## [2026-05-27] fusion A2 — tests adverses hooks sécu
- **Fichiers** : feedback_tests_adverses_obligatoires → memory/_archive/2026-05/feedback_tests_adverses_obligatoires.md, feedback_tests_adverses_ratio_3_1 → memory/_archive/2026-05/feedback_tests_adverses_ratio_3_1.md
- **Raison** : doublon conceptuel — `tests_adverses_ratio_3_1` se déclarait « règle enfant » de `tests_adverses_obligatoires`. Parent (tester bypass + DA avant push + false-positives) + précision quantitative (ratio ≥3:1, caractériser bugs) sur le même sujet exact (tests adverses hooks sécu) consolidés.
- **Méta-feedback** : feedback_tests_adverses_hooks_secu.md (aliases `tests-adverses-obligatoires`, `tests-adverses-ratio-3-1-hooks-secu` pour préserver les 3 backlinks entrants).
- **Index MEMORY.md** : entrées `tests-adverses-obligatoires` et `tests-adverses-ratio-3-1-hooks-secu` retirées / entrée `tests-adverses-hooks-secu` ajoutée.
- **Rollback** : git mv les 2 fichiers depuis _archive/2026-05/ vers memory/, supprimer le méta-feedback, restaurer les 2 lignes index.

## [2026-05-27] fusion A3 — bras-droit absorbé dans jarvis-innovator
- **Fichiers** : feedback_bras_droit → memory/_archive/2026-05/feedback_bras_droit.md
- **Raison** : `bras_droit` = version antérieure et plus pauvre du Contrat Jarvis (proactif, propose, MAJ mémoire, pose questions). Même message, absorbé dans `jarvis_innovator` (contrat complet). Distinct : seul `bras_droit` archivé ; `jarvis_innovator` édité en place (fichier conservé) pour préserver son backlink + son rôle de Contrat. `never-pure-executor` et `autonomy-rule` NON fusionnés (angles distincts confirmés par arbitrage).
- **Méta-feedback** : feedback_jarvis_innovator.md (édité en place, alias `bras-droit-proactif` ajouté).
- **Index MEMORY.md** : entrée `bras-droit-proactif` retirée / entrée `jarvis-innovator-mindset` mise à jour (mention bras droit).
- **Rollback** : git mv feedback_bras_droit.md depuis _archive/2026-05/ vers memory/, retirer la mention bras-droit du jarvis-innovator, restaurer la ligne index `bras-droit-proactif`.
