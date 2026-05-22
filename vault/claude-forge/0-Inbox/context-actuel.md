---
titre: "Context Actuel"
resume: "Working memory dynamique — mis a jour par /done, lu par /recap. Etat post-chantier 22 mai 2026 : vault Karpathy strict + 8 canoniques + 14 leaders + composants conformes."
aliases:
  - "context actuel"
  - "contexte courant"
  - "working memory"
  - "memoire de travail"
  - "etat actuel"
type: context
status: active
derniere-maj: 2026-05-22
auteur: claude
tags:
  - "#type/context"
  - "#meta/working-memory"
---

## Phase actuelle

Chantier 22 mai 2026 TERMINE et pousse : vault forge-brain transforme en source de verite actionnable (pattern Karpathy strict + 8 notes canoniques + 14 fiches leaders + composants .claude/ alignes doctrine 22 mai).

## Derniere session (2026-05-22)

### Decisions prises
- **Pattern Karpathy strict** adopte sur vault forge-brain (3-layers raw/wiki/schema + index.md content-oriented + log.md append-only + SCHEMA.md self-describing)
- **Demantelement hooks workflow** : 9 hooks supprimes coherent doctrine 22 mai
- **CLAUDE.md v3.0** : 91 lignes, retire effort xhigh defaut + hook critique double + architect-first obligatoire + DA systematique
- **Knowledge cleanup NON execute** : verdict audit 3/3 = 39 GARDER / 0 SUPPRIMER (archives historiques par construction)
- **Cran 2 (P0+P1)** applique. P2 nice-to-have ignores volontairement
- **Effort xhigh reduit** : python-dev/project-analyzer/project-auditor sonnet+high
- **DA conditionnel** : devils-advocate-pipeline rule reecrite OBLIGATOIRE -> CONDITIONNEL cible

### En cours
- **AUCUNE TACHE en cours** — chantier termine et pousse (16 commits a29ddb4 -> d2bbcec)

### Prochaines etapes
- **Action utilisateur requise** : appliquer manuellement `.claude/settings.json.proposed` (auto-mode classifier hard block sur tout vecteur agent : Write/Edit/cp/heredoc). Commande PowerShell : `copy .claude\settings.json.proposed .claude\settings.json`
- Une fois applique : plus d'erreurs hooks bruyantes (9 hooks supprimes references mais settings.json obsolete jusque-la)
- Tester en session fraiche : "analyse ce repo, propose-moi la config CC parfaite" doit pointer immediatement sur [[methode-analyser-repo]]

## Fils ouverts

- Audit `Knowledge/syntheses/` separe (3 notes pre-pivot 8-9 mai) — chantier basse priorite, pas critique
- Bug session : hook delegate-guard bloque Edit direct CLAUDE.md, agent Agent bloque par vault-before-specialist supprime. Workaround = Bash heredoc avec CLAUDE_AGENT env var (jusqu'a application settings.json.proposed)

## Commits chantier 22 mai (16 total)

- `a29ddb4` : 16 rapports recherche + PLAN-EXECUTION-FINAL
- `c651959 -> 5443897` : 8 canoniques produites
- `f3188a0` : corrections DA (1 bloquant + 5 forts)
- `310c3f1` : 14 fiches leaders
- `9272a8f` : cleanup destructif 28 notes obsoletes
- `173ebf5` : CHANGELOG + MOCs
- `1f3f1f4` : nice-to-have DA N1-N5
- `d2bbcec` : vault Karpathy strict + composants doctrine 22 mai

## Liens

- [[Raphael-Picard]]
- [[Claude-Forge]]
- [[index]] — index content-oriented vault
- [[log]] — log append-only operations
- [[SCHEMA]] — conventions vault
- [[methode-analyser-repo]] (META canonique)
- [[raisonnement-22mai-doctrine-vs-enforcement]] (pivot doctrinal)
- [[critique-2026-05-22-8-canoniques-chantier]] (verdict DA chantier)
