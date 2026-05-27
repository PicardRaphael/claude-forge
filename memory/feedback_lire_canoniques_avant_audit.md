---
name: lire-canoniques-vault-en-entier-avant-audit
description: "Ordre correct audit/création — ANALYSER d'abord (faits bruts), LIRE CANONIQUES EN ENTIER ensuite, CROISER → PLAN d'écarts mesurables, exécuter. JAMAIS canoniques avant analyse (biais perception)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: d16cea52-3288-48fe-b266-693dd7948ca2
---

Erreur commise 2026-05-22 lors de l'audit ia_back, double sens :

**Réflexe FAUX 1** (initial) : `mcp__forge-brain__search_brain` sur quelques mots-clés, lire 3-4 extraits, lancer l'audit. Considérer la consultation vault "faite". Conséquence : audit basé mémoire session, pas source de vérité.

**Réflexe FAUX 2** (correction sur-corrective) : lire les canoniques EN ENTIER AVANT l'analyse. Conséquence : biais de perception — on voit ce que les canoniques disent qu'on devrait voir, pas le RÉEL.

**Réflexe CORRECT** : ordre A → B → C → D → E (corrigé par Raphael 2026-05-22) :

## A. ANALYSER LE RÉEL D'ABORD (sans biais)

- Auditer skills/agents/hooks/rules existants (compter, lister, mesurer)
- Scanner le code RÉEL (étape 1 + 5 méthode canonique)
- FAITS bruts uniquement, pas d'interprétation

**Pourquoi en premier** : si tu lis les canoniques avant, tu viens à l'analyse biaisé — tu vois ce que tu t'attends à voir.

## B. LIRE CANONIQUES EN ENTIER (après analyse)

Via `mcp__forge-brain__read_note` SANS `max_lines` ou avec `max_lines: 500+`. JAMAIS `search_brain` seul (extraits ~10 lignes insuffisants).

Notes canoniques à lire en entier selon tâche :

1. [[workflow-claude-code-optimal]] — 7 pratiques (routines / advisor 5× / leaf nodes / multi-clauding / /loop / sonnet-opus / compounding)
2. [[comment-creer-agent]] — frontmatter, 2-agent Justin Young, stat harness > modèle (LangChain 52.8%→66.5%)
3. [[comment-creer-skill]] — 9 catégories Thariq, trigger 3e personne, < 500L, 8 principes
4. [[comment-creer-hook]] — 25+ events, doctrine 22 mai lint/security/scope uniquement
5. [[comment-ecrire-claudemd]] — target 200L, 5 anti-patterns Anthropic, compounding
6. [[methode-analyser-repo]] — grille 6 étapes complète
7. [[raisonnement-22mai-doctrine-vs-enforcement]] — pivot 22 mai, workflow hooks interdits

Puis [[pattern-vault-llm-karpathy]] et [[mcp-vs-skills-doctrine]] selon contexte.

## C. CROISER analyse ⨯ canoniques

Mettre côte-à-côte FAITS observés (A) et RÈGLES canoniques (B). Lister les ÉCARTS mesurables :
- Agent X = Opus mais canonique dit Sonnet → écart sonnet/opus split
- Skill Y = 800L mais canonique dit < 500L → écart taille
- Hook Z = workflow gate mais doctrine 22 mai interdit → écart doctrinal

Pas d'opinion. Que des écarts mesurables.

## D. PLAN basé sur les ÉCARTS

Le plan = liste des écarts à fixer, priorisés. Si pas d'écart sur un point → pas de fix. Pas d'idéologie "appliquer la canonique partout".

## E. EXÉCUTER

**How to apply** :
- TOUTE demande "analyse / audit / crée / propose config" → ordre A → B → C → D → E STRICT
- TOUT agent forge (project-auditor, project-analyzer, skill-creator, agent-creator, hook-creator, claudemd-optimizer) doit avoir cet ordre codifié dans son .md
- `search_brain` OK pour découvrir + naviguer ; `read_note` complet OBLIGATOIRE pour juger
- AVANT tout audit, FAITS d'abord (count agents, count skills, scan code, patterns observés). PUIS canoniques. PUIS écarts.

## Fusionné depuis feedback_checklist_before_modify (2026-05-24)

Le check-before-create canonique = les 5 étapes ci-dessous DOIVENT être faites avant TOUTE modification skill/agent/hook (même "petit ajout"). Observé 2 fois (26 avril + 7 mai 2026) que sauter ces étapes = composants non conformes.

5 étapes obligatoires :
1. Lire feedbacks pertinents dans MEMORY.md (feedback_skill_*, feedback_major_mistakes)
2. Query forge-brain : 04-Techniques/ + Knowledge/erreurs/ + 07-Prompts/
3. Lire references/ du composant cible
4. Charger la skill forge pertinente (cc-skills-ref, cc-agents-ref)
5. PUIS commencer le travail

Pas d'exception "c'est rapide" ou "je connais déjà".

Related : [[feedback_audit_qualite_design_transverse]], [[feedback_analyse_repo_includes_code]], [[feedback_consolidate_searches]], [[feedback_analyse_first_not_questionnaire]].
