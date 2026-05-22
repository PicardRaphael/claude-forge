---
titre: "Audit cleanup Knowledge/ — chantier 22 mai"
resume: "Audit READ-ONLY des 39 notes Knowledge/ post-doctrine 22 mai — verdict GARDER/REFONDRE/SUPPRIMER par note, comptage final et plan d'action"
derniere-maj: 2026-05-22
auteur: claude
type: audit
tags:
  - "#type/audit"
  - "#chantier/22mai2026"
  - "#sujet/vault"
---

# Audit cleanup Knowledge/ — chantier 22 mai 2026

Audit READ-ONLY post-doctrine 22 mai (hooks lint/security/scope, JAMAIS workflow ; pipeline markers SUPPRIMÉ ; TDD strict hooks SUPPRIMÉ).

Référentiel : 8 canoniques dans `04-Techniques/claude-code/` (workflow-claude-code-optimal, mcp-vs-skills-doctrine, pattern-vault-llm-karpathy, trail-of-bits-config, methode-analyser-repo, comment-creer-{agent,hook,skill}, comment-ecrire-claudemd).

---

## 1. `Knowledge/erreurs/` — 20 notes

| Note | Verdict | Raison |
|------|---------|--------|
| `e-descriptions-keyword-stuffing` | GARDER | Erreur prompt-engineering unique, frontmatter OK, encore valide |
| `erreur-advisory-rules-insuffisantes` | GARDER | Pattern fondateur "hooks > rules", toujours actuel, frontmatter OK |
| `erreur-architect-neo_ia-fouille-bdd` | GARDER | Incident scope unique → origine repo-scope-guard, doctrine scope (hooks OK) |
| `erreur-auto-mode-classifier-self-modification` | GARDER | Limitation infra Anthropic unique, factuel et durable |
| `erreur-claude-agent-env-var-dead-code` | GARDER | Dead code factuel, leçon réutilisable detection sub-agent |
| `erreur-da-heredoc-bash-silencieux` | GARDER | Incident technique unique (Bash write déguisé), fix MCP create_note encore valide |
| `erreur-deploy-sans-advisor-da-cwc2026` | GARDER | Erreur process Jarvis, contrat advisor+DA toujours actif |
| `erreur-devils-advocate-tronqué` | GARDER | Incident structural agent + violation contrat Jarvis, frontmatter OK |
| `erreur-edit-direct-skills` | GARDER | Origine delegate-guard, doctrine "skill-creator obligatoire" encore valide |
| `erreur-hooks-bash-quoting-windows` | GARDER | Bug portabilité Windows factuel, frontmatter OK |
| `erreur-hooks-workflow-enforcement` | GARDER | Note PIVOT 22 mai — référence canonique doctrine actuelle, lien `[[raisonnement-22mai-doctrine-vs-enforcement]]` |
| `erreur-mcp-stopwords-semantiques` | GARDER | Bug infra MCP forge-brain unique et corrigé |
| `erreur-mcp-yaml-dump-corruption` | GARDER | Bug infra MCP unique et corrigé, anti-pattern yaml.dump réutilisable |
| `erreur-password-postgres-clair-mcp-json` | GARDER | Erreur sécu critique, leçon "JAMAIS de credentials versionnés" toujours active |
| `erreur-pipeline-trop-long-frustration` | GARDER | Symptôme déclencheur refonte 22 mai, signal Lead IA, encore pertinent |
| `erreur-settings-paths-hardcodes-multi-poste` | GARDER | Bug portabilité multi-poste factuel, leçon path-agnostic encore active |
| `erreur-skill-monolithique-sans-references` | GARDER | Anti-pattern skill > 500L, encore appliqué (cf comment-creer-skill canonique) |
| `erreur-stop-critique-position-gotcha-fin` | GARDER | Bug primacy/recency factuel, leçon "instructions critiques en haut" encore valide |
| `erreur-tests-heureux-vs-adverses` | GARDER | Erreur process tests adverses, leçon DA AVANT push encore active |
| `erreur-vault-before-specialist-ttl-scope` | GARDER | Marker TTL anti-pattern, suppression confirmée post-doctrine, frontmatter OK |

**Sous-total erreurs : 20 GARDER / 0 REFONDRE / 0 SUPPRIMER**

Note : aucune erreur n'est devenue obsolète après le pivot 22 mai. `erreur-hooks-workflow-enforcement` et `erreur-vault-before-specialist-ttl-scope` documentent justement l'origine de la doctrine actuelle — à GARDER explicitement.

---

## 2. `Knowledge/critiques/` — 15 notes

| Note | Verdict | Raison |
|------|---------|--------|
| `critique-2026-05-09-skill-done` | GARDER | Critique livrable unique daté, frontmatter OK |
| `critique-2026-05-13-setup-lojii` | GARDER | DA setup lojii avec 4 bloquants, contenu factuel daté |
| `critique-2026-05-21-brief-distant-template-spec` | GARDER | DA refonte BRIEF cross-repo, fix appliqué et toujours actif |
| `critique-2026-05-21-outcomes-test-deploy` | GARDER | DA outcomes daté avec bloquants concrets, frontmatter OK |
| `critique-2026-05-21-refonte-hooks-16-vers-6` | GARDER | Trace DA refonte hooks → directement à l'origine de la doctrine 22 mai, lien canonique |
| `critique-2026-05-21-refonte-pipeline-boris-pattern` | GARDER | DA pivot pipeline Boris, source documentaire raisonnement-revirement |
| `critique-2026-05-21-repartition-opus-sonnet` | GARDER | DA model split daté, leçons toujours actives (feedback_all_opus en mémoire) |
| `critique-2026-05-22-8-canoniques-chantier` | GARDER (PROTÉGÉ) | NE PAS TOUCHER — critique des canoniques produites 22 mai |
| `critique-2026-05-22-audit-neo_ia` | GARDER | DA audit consolidé avec bloquant sécu confirmé (password Postgres), critique 22 mai |
| `critique-2026-05-22-vault-doctrine-renversement` | GARDER | DA bloque renversement vault — décision active doctrine 22 mai |
| `critique-capitalisation-blog-large-codebases-tweet-thariq` | GARDER | DA capitalisation 5 livrables vault, vérifications factuelles |
| `critique-notes-neochat-architecture` | GARDER | DA archi NeoChat avec 3 erreurs factuelles corrigées, trace utile |
| `critique-notes-neodoc-architecture` | GARDER | DA archi NeoDoc validé contre code source, trace utile |
| `critique-notes-neomail-architecture` | GARDER | DA archi NeoMail validé contre code source, trace utile |
| `critique-session-2026-05-20-running-notes-decompose-xread-mcp` | GARDER | DA multi-livrables avec bloquant sécu (rotation password), trace utile |

**Sous-total critiques : 15 GARDER / 0 REFONDRE / 0 SUPPRIMER**

Note : les critiques sont des **artefacts historiques** par nature — elles datent du moment de la critique. Même si la doctrine évolue, la critique reste la trace de la décision et ne doit pas être supprimée. Le rôle d'une critique est de documenter la chaîne décisionnelle, pas de refléter l'état courant.

---

## 3. `Knowledge/raisonnements/` — 4 notes

| Note | Verdict | Raison |
|------|---------|--------|
| `architecture-decision-hook-maison-vs-plugin-tiers` | GARDER | Décision archi datée (hook maison vs tdd-guard) — MÊME si TDD strict est mort, la grille "déterminisme vs LLM dans guard" reste réutilisable pour TOUT futur hook |
| `raisonnement-22mai-doctrine-vs-enforcement` | GARDER (PROTÉGÉ) | NOTE CANONIQUE doctrine 22 mai — interdiction de suppression |
| `raisonnement-kill-tdd-strict-hooks-mai-2026` | GARDER | Raisonnement décisionnel pivot 21 mai, source citée par doctrine 22 mai, frontmatter OK |
| `raisonnement-revirement-pipeline-mai-2026` | GARDER | Trace multi-étapes du pivot pipeline, précieux pour comprendre POURQUOI, lien canoniques |

**Sous-total raisonnements : 4 GARDER / 0 REFONDRE / 0 SUPPRIMER**

---

## 4. Autres sous-dossiers — état général

| Dossier | Notes (hors _index) | État | Action |
|---------|---------------------|------|--------|
| `syntheses/` | 6 notes | 3 à jour 22 mai (analyse-plugin-claude-code-setup, neoteem-agentic-engineering-mapping, synthese-audit-coherence-neo-ia-ia-back), 3 plus anciennes (outils-portabilite-forge 9 mai, rag-obsidian-claude 8 mai, techniques-inedites 8 mai) | Audit ultérieur — pas critique post-22 mai. Les 3 anciennes méritent un check obsolescence en lot séparé |
| `questions/` | 1 note (question-idor-coproprietes 21 mai) | Récente, métier | Pas d'action |
| `reviews/` | 0 notes (_index seul) | Vide | Pas d'action |
| `evolutions/` | 0 notes (_index seul) | Vide | Pas d'action |
| `explorations/` | 1 note (neo-ia-tests-lenteur-diagnostic 21 mai) | Récente, exploration tests | Pas d'action |

**Recommandation** : auditer `syntheses/` (notamment les 3 d'avant le pivot mai) dans un chantier séparé. Les autres sous-dossiers sont vides ou récents.

---

## 5. Indexes `_index.md`

Chaque sous-dossier a un `_index.md` (8 au total). Ils décrivent le rôle du dossier sans lister les notes. **Pas de mise à jour requise** après cet audit puisque tout est GARDÉ — la sémantique des dossiers est inchangée.

Si dans un chantier suivant des notes sont effectivement supprimées/refondues, alors mettre à jour les `_index.md` concernés.

---

## 6. Verdict global

### Comptage final

| Catégorie | GARDER | REFONDRE | SUPPRIMER | Total |
|-----------|--------|----------|-----------|-------|
| erreurs/ | 20 | 0 | 0 | 20 |
| critiques/ | 15 | 0 | 0 | 15 |
| raisonnements/ | 4 | 0 | 0 | 4 |
| **TOTAL audité** | **39** | **0** | **0** | **39** |

### Top 5 notes à supprimer en priorité

**Aucune.** Cet audit ne recommande aucune suppression dans les 39 notes auditées.

### Pourquoi rien à supprimer

1. **Nature des sous-dossiers** : `erreurs/`, `critiques/`, `raisonnements/` sont des **archives historiques** par construction. Chaque note documente un incident, une critique ou une décision *datés*. Une doctrine qui évolue ne rend pas l'incident faux — elle rend la leçon plus précieuse (trace du POURQUOI).
2. **Pivot 22 mai bien capturé** : les notes-clés du pivot (`erreur-hooks-workflow-enforcement`, `erreur-vault-before-specialist-ttl-scope`, `raisonnement-22mai-doctrine-vs-enforcement`, `raisonnement-kill-tdd-strict-hooks-mai-2026`, `raisonnement-revirement-pipeline-mai-2026`, `critique-2026-05-21-refonte-hooks-16-vers-6`) sont précisément la mémoire institutionnelle de la doctrine actuelle. Elles seraient destructrices à supprimer.
3. **Frontmatter conforme partout** : aliases 4-6, resume spécifique, derniere-maj présent, tags structurés. Aucune note REFONDRE détectée.
4. **Pas de doublon avec les 8 canoniques** : les canoniques sont des *techniques* (how-to réutilisables) ; les Knowledge sont des *traces* (incident → leçon). Pas de chevauchement de fait.

### Plan d'action recommandé

1. **Cette session** : aucune action destructive. Le Knowledge/ est cohérent post-doctrine 22 mai.
2. **Chantier séparé (priorité basse)** : audit de `Knowledge/syntheses/` (3 notes pré-pivot, 8-9 mai) pour vérifier obsolescence et éventuel rafraîchissement.
3. **Compounding futur** : continuer à écrire dans `Knowledge/erreurs/` et `Knowledge/critiques/` après chaque incident/livrable majeur. Ces dossiers sont la mémoire qui rend les canoniques crédibles.
4. **Audit léger trimestriel** : revisiter ce verdict si la doctrine pivote à nouveau. Le critère "encore valide après pivot ?" est le bon discriminant pour SUPPRIMER une trace (pas avant).

### Liens

- [[raisonnement-22mai-doctrine-vs-enforcement]] — doctrine de référence
- [[critique-2026-05-22-8-canoniques-chantier]] — DA des canoniques produites
- [[workflow-claude-code-optimal]] — canonique workflow
