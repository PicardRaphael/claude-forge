---
titre: "architecture-decision — Niveaux 1/2/3 pour décider d'un refactor d'agents (capacité vs usage)"
resume: "Avant tout refactor mass d'agents/skills/hooks basé sur métriques frontmatter, exiger Niveau 2 transcripts JSONL minimum. Niveau 1 statique = carte. Niveau 2 transcripts = verdict échantillon. Niveau 3 hook PostSubagentStop CSV = verdict statistique. Sans niveaux croisés, refactor sur Niveau 1 seul reproduit le pattern F1/F2 (claims non vérifiés) à grande échelle."
aliases:
  - "niveaux mesure agents"
  - "capacité vs usage agents"
  - "audit agents 3 niveaux"
  - "agent measurement levels"
  - "capacity vs usage decision"
  - "transcripts JSONL agent audit"
  - "PostSubagentStop instrumentation"
  - "Cat Wu 6-8 ops verdict"
type: raisonnement
domaine: claude-code
derniere-maj: 2026-05-23
auteur: claude
tags:
  - "#type/raisonnement"
  - "#domaine/claude-code"
  - "#domaine/agents"
  - "#meta"
---

## Problème

Comment décider si un agent Claude Code mérite d'être refactoré (split, élagage tools, réduction sections) sur base de mesures objectives, sans tomber dans le refactor à l'aveugle quand les seuils statiques sont dépassés ?

## Contexte

Session 3 déploiement neo_ia (22-23 mai 2026). Mandat Raphael : "rends-toi parfait par rapport au canonique forge". Un agent collaborateur partage une méthodologie 3 niveaux (Niveau 1 mesure statique frontmatter, Niveau 2 transcripts JSONL, Niveau 3 hook PostSubagentStop CSV).

État initial neo_ia :
- 14 agents, 26 skills, 8 hooks, 19 rules
- Doctrine 22 mai : "lint/security/scope only, pas de workflow hooks"
- Canonique [[comment-creer-agent]] : "max 6-8 ops/agent" (Cat Wu)

Tentation initiale : appliquer Niveau 1 sur les 14 agents → 4 agents flaggés (architect-deep 5/5 seuils, dev-neochat/neodoc/neomail 3 seuils chacun) → refactor mass.

## Chaîne de raisonnement

1. **Hypothèse initiale** : "Niveau 1 statique me donne un verdict — architect-deep 211L, 1518 mots, 10 tools, 8 skills, 11 sections H2 = candidat split urgent. Trois dev-app à 11 tools partagés = duplication, à élaguer."

2. **Étape A→B→C→D→E déclarée** : audit ABCDE conclut "0 écart structurel" sur le contenu technique session 3. Conformité Sonnet/Opus split, xhigh whitelist, hooks workflow absents, etc.

3. **Contradiction interne détectée par advisor** : "Tu te contredis. Étape C disait '0 écart structurel'. Soit ce verdict était faux, soit Bloc B (refactor 7 agents) est over-claim." → Le sentiment d'incomplétude post-ABCDE m'a poussé à inventer du travail.

4. **Insight advisor pivot** : "Niveau 1 = indication, pas verdict. Cat Wu '6-8 ops/agent' = ops dans TRANSCRIPT RÉEL, PAS tools listés dans frontmatter. Tu conflates capacité (ce que l'agent PEUT faire) avec usage (ce qu'il FAIT). Sans Niveau 2, refactor mass = casser des choses qui marchent. F1/F2 à grande échelle." → Direction inversée : pas refactor, instrumenter.

5. **Validation Niveau 2 empirique** sur 35 invocations transcripts JSONL (`~/.claude/projects/<repo>/<session>/subagents/agent-*.jsonl`) :
   - **architect-deep** (n=1) : 6 ops typique → **SOUS le seuil** Cat Wu. Niveau 1 → faux positif total.
   - **dev-neochat** (n=31) : mean=42.8 mais p50=27, p75=52, p90=116, max=198. Distribution outlier — pas surcharge steady state, invocations parfois mal scopées.
   - **dev-neodoc** (n=2), **dev-neomail** (n=1) : données pauvres, verdict reporté.

6. **Réconciliation Niveau 1 / Niveau 2** : agent avec 5/5 seuils Niveau 1 dépassés peut avoir 6 ops typique (sous seuil) → Niveau 1 mesure CAPACITÉ (potentiel), Niveau 2 mesure USAGE (réel). Les deux ne sont PAS corrélés mécaniquement.

7. **Décision finale non-évidente** : pas de refactor split (option a). Deux solutions plus cheap :
   - **(b) Rule scope invocations** : 1 ligne dans `agent-delegation.md` "invocations dev-* doivent être scopées ~30 LOC". Coût = 0 risque structurel. Si (b) suffit, (a) jamais nécessaire.
   - **Niveau 3 instrumentation** : hook `PostSubagentStop` → `.claude/agent-metrics.csv` (append-only). Laisser tourner 1-2 semaines avec n>>30 invocations distribuées avant réanalyse statistique. Pattern Boris/Anthropic interne pour "+200% PRs Cat Wu measure".

8. **Validation a posteriori** : commits 96142b0 (corrections F1+F2) + 70a841c (Niveau 3 hook + rule scope). 11 commits ahead origin/develop, working tree clean, doctrine respectée.

## Insight clé

**Capacité (frontmatter) ≠ Usage (transcript). Niveau de mesure ≠ Niveau de verdict.**

Trois découvertes liées impossibles à reconstruire sans cette trace :

(1) Un agent peut dépasser 5/5 seuils Niveau 1 et être parfaitement calibré en usage (architect-deep). Refactor sur Niveau 1 seul = casser un agent qui marche.

(2) Une moyenne (mean=42.8 ops) peut masquer un pattern outlier (p50=27, p90=116). Il faut p50/p75/p90, pas la moyenne, pour décider. n=31 reste insuffisant pour verdict statistique : pattern "soit petite tâche soit grosse refonte" ≠ pattern "surcharge steady state".

(3) Quand Niveau 2 montre un pattern outlier, la solution canonique n'est PAS de splitter l'agent (option a coûteuse) mais d'inviter les callers à scoper leurs invocations (option b 1-ligne). On corrige le **callsite**, pas le **callee**.

(4) Sans Niveau 3 instrumentation continue (hook PostSubagentStop → CSV), aucun verdict statistique sur les agents. C'est ce que Boris/Anthropic font en interne pour leurs métriques "+200% PRs Cat Wu". Pattern reproductible cross-repos.

## Résultat

- Commit 70a841c neo_ia develop : rule scope + hook agent-metrics-logger.py + .gitignore CSV
- Note exploration vault forge `[[niveau-1-static-mesure-agents-neo-ia-2026-05-22]]` UPDATE 2026-05-23 avec Niveau 2 findings
- 2 nouveaux feedback mémoire projet forge : `feedback_methode_abcde_carte_pas_verdict.md` + `feedback_gotchas_line_numbers_verifies.md`
- 1 note erreur vault `Knowledge/erreurs/erreur-gotchas-line-numbers-non-verifies-claudemd.md`
- 0 agent refactoré à l'aveugle. Risque évité de casser architect-deep.

## Réutilisation

Utiliser ce raisonnement quand :
- On envisage un **refactor mass** d'agents/skills/hooks basé sur métriques statiques (lines, tools, sections, mots)
- On observe un **écart entre verdict ABCDE et tentation post-hoc** (sentiment d'incomplétude qui pousse à inventer du travail)
- On lit un agent flaggé sur un seuil canonique et on veut savoir s'il faut vraiment le toucher
- On audite un repo qui n'a pas d'instrumentation Niveau 3 et on doit décider entre "agir vite mais aveugle" et "instrumenter d'abord, agir après"

**Signal de déclenchement** : tout prompt utilisateur du type "rends-toi parfait par rapport au canonique" ou "corrige toutes les dettes structurelles". Risque que le perfectionnisme produise du refactor non justifié.

**Anti-pattern à éviter** : transformer un seuil canonique en verdict mécanique sans empirie. "X > seuil → refactor" sans Niveau 2 = reproduction F1/F2 à grande échelle.

## Liens

- [[niveau-1-static-mesure-agents-neo-ia-2026-05-22]]
- [[comment-creer-agent]]
- [[feedback_audit_claims_after_brief]]
- [[critique-2026-05-22-doctrine-drift-guard]]
- [[workflow-claude-code-optimal]]
- [[methode-analyser-repo]]
- [[erreur-gotchas-line-numbers-non-verifies-claudemd]]
