---
titre: "Erreur — pattern de capitalisation ex post sur sessions 23-24 mai"
resume: "Audit doctrinal des sessions 23-24 mai (55 commits) a révélé que feedbacks, hooks et canoniques sont régulièrement créés APRÈS découverte du manquement dans la même session, jamais relus AVANT l'action. Note factuelle non prescriptive."
aliases:
  - "capitalisation ex post 23-24 mai"
  - "audit doctrine session 23-24 mai"
  - "feedback created after action pattern"
  - "shipping before DA pattern"
derniere-maj: 2026-05-24
auteur: claude
type: erreur
domaine: claude-code
tags:
  - "#type/erreur"
  - "#domaine/claude-code"
  - "#projet/claude-forge"
  - "#audit/doctrine"
---

# Erreur — pattern de capitalisation ex post sur sessions 23-24 mai

## Contexte

Audit doctrinal en session fraîche du 24 mai 2026, sur les commits forge des sessions 23 mai (25 commits, 07:45→15:34) et 24 mai (30 commits, 07:13→10:52). Total 55 commits.

Application du prompt `self-audit-doctrine-session` (7 checks). Résultat : **0 PASS / 4 FAIL / 3 PARTIAL** sur 7 checks applicables.

## Pattern dominant observé

Les apprentissages d'une session sont capitalisés EX POST (feedback créé, hook ajouté, canonique enrichie) APRÈS découverte du manquement dans cette même session, jamais relus AVANT l'action.

## Evidence empirique

**Commits 24 mai démontrent le pattern en chaîne** :

- `7614f51` — hook meta-commentary-detector + auto-injection canonique `read_note` dans 6 agents. Commit message verbatim : *"Résout finding audit '0 agent ne fait read_note dans son body'"* — la session corrige le manquement qu'elle vient de constater.
- `b586bc4` — `methode-analyser-repo` étape 1 enrichie "lecture code RÉEL obligatoire" — correction suite à relance Raphael que l'étape A était sous-spécifiée pendant les audits 23 mai.
- `d07f8fa` — regex `Source:` refinée 30 min après ship du hook 7614f51 (faux positifs détectés en prod sur ia_back/neo_ia). Tests adverses insuffisants au premier round.
- `5f0efca` — critique-2026-05-24-meta-commentaires arrive 20 min APRÈS commit doctrine `74916cd` (08:17 → 08:37). DA post-ship.
- Feedbacks mémoire créés le 24 mai (`innovations_24mai_doctrine`, `pas_de_meta_commentaire_doctrine`, `5_lignes_karpathy_ouverture`) — tous datés du jour même de l'action qu'ils encadrent.

**MCP forge-brain v1.3** (`3001182` + `37821e5`) — 4 nouveaux outils destructifs (delete_note, move_note, bulk_update_property, lint_vault). Aucun fichier `critique-MCP-v1.3` dans `Knowledge/critiques/` malgré mention "DA verdict GO-WITH-FIXES applique" en commit message.

**Refonte vault** (`0a3d857`, 21 deletions) shipped sans critique DA dédiée.

**Canonique nouvelle** `mcp-vault-llm-design.md` (`5f0efca`) shipped sans critique DA dédiée.

## Validation à 3 voix

Audit + DA + advisor consultés en session 24 mai sur la proposition de capitaliser via un nouveau feedback `feedback_capitalisation_ex_post_pattern`. **Verdict convergent : rejet**.

**Arguments du rejet** :
1. MEMORY.md saturé (25.2KB > 24.4KB limite, troncature active dans la session même).
2. Hook `vault-query-guard.py` référencé dans 4 docs mais absent du disque — résidu doctrinal type 1 du chantier 22 mai (drift documenté par `methode-pivoter-doctrine`). La vraie cause racine était structurelle, pas comportementale.
3. Redondance directe avec `feedback_lire_canoniques_avant_audit` + `feedback_check_before_modify_mandatory` + rule `sequence-canonique-modification.md`. Si 3 sources textuelles sont ignorées, la 4ème le sera aussi.
4. Audit lui-même biaisé : 0 PASS / 4 FAIL / 3 PARTIAL = par construction négatif (checks dérivés des manquements connus, comme `lint_vault` qui trouve toujours des problèmes).

## Le vrai anti-pattern (plus étroit)

Pas "créer un feedback en fin de session" (apprentissage normal). Mais **prétendre avoir suivi ABCDE alors que B (lire canoniques) a été sauté**. La capitalisation post-découverte est saine ; la déclaration de conformité à une séquence non suivie est l'anti-pattern.

## Pas de prescription

Cette note est **factuelle, non prescriptive**. Aucun nouveau feedback créé. Capitalisation traçable sans amputer l'historique ni ajouter de rite à un système déjà saturé.

## Actions correctives prises en session 24 mai

1. Patch `delegate-guard.py` (cause racine d'un autre bug observé pendant l'audit) — voir [[erreur-delegate-guard-env-var-vs-stdin]].
2. Purge des références au hook `vault-query-guard` fantôme dans `.claude/rules/vault-consultation-protocol.md`, `.claude/skills/forge-review/references/baseline.md`, `.claude/agent-memory/hook-creator/hook_vault_query_pair.md` (deprecated banner).
3. Consolidation MEMORY.md : fusion `feedback_checklist_before_modify` dans `feedback_lire_canoniques_avant_audit`.
4. Fix tools MCP frontmatter sur 8 agents + 6 skills forge (chantier en cours).

## Wikilinks

- [[self-audit-doctrine-session]]
- [[methode-pivoter-doctrine]]
- [[methode-analyser-repo]]
- [[erreur-delegate-guard-env-var-vs-stdin]]
- [[raisonnement-22mai-doctrine-vs-enforcement]]
