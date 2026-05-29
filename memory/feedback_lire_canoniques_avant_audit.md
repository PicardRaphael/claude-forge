---
name: lire-canoniques-vault-en-entier-avant-audit
description: "Ordre correct audit/création — ANALYSER d'abord (faits bruts), LIRE CANONIQUES EN ENTIER ensuite, CROISER → PLAN d'écarts mesurables, exécuter. JAMAIS canoniques avant analyse (biais perception)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: d16cea52-3288-48fe-b266-693dd7948ca2
---

Cf [[methode-analyser-repo]] (doctrine : ordre canonique A→B→C→D→E — analyser le réel d'abord, lire canoniques EN ENTIER via `read_note` sans `max_lines`, croiser → écarts mesurables, plan, exécuter ; `search_brain` seul = extraits ~10 lignes insuffisants pour juger ; table des notes canoniques à lire par type de tâche).

**Cas empirique(s) :**

- **Audit ia_back 2026-05-22 — double erreur corrigée par Raphael** : Réflexe FAUX 1 (initial) = `search_brain` sur quelques mots-clés, lire 3-4 extraits, lancer l'audit en considérant la consultation vault "faite" → audit basé mémoire session, pas source de vérité. Réflexe FAUX 2 (sur-correction) = lire les canoniques EN ENTIER AVANT l'analyse → biais de perception, on voit ce que les canoniques disent qu'on devrait voir, pas le RÉEL. Correction Raphael : ordre A (analyser le réel sans biais) → B (canoniques en entier après) → C (croiser) → D (plan) → E (exécuter).

- **Fusionné depuis feedback_checklist_before_modify (2026-05-24) — composants non conformes, observé 2 fois (26 avril + 7 mai 2026)** : sauter les 5 étapes pré-modification (même pour un "petit ajout") = composants non conformes. 5 étapes obligatoires avant TOUTE modification skill/agent/hook : (1) lire feedbacks pertinents dans MEMORY.md (feedback_skill_*, feedback_major_mistakes) ; (2) query forge-brain 04-Techniques/ + Knowledge/erreurs/ + 07-Prompts/ ; (3) lire references/ du composant cible ; (4) charger la skill forge pertinente (cc-skills-ref, cc-agents-ref) ; (5) PUIS commencer le travail. Pas d'exception "c'est rapide" ou "je connais déjà".

Related : [[feedback_audit_qualite_design_transverse]], [[feedback_analyse_repo_includes_code]], [[feedback_consolidate_searches]], [[feedback_analyse_first_not_questionnaire]].
