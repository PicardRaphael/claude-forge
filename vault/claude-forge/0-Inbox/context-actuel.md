---
titre: Context Actuel
resume: Working memory dynamique -- mis a jour par /done, lu par /recap. Session 2026-05-23 : audit thematique vault Claude Code (22 corrections) + audit forge dogfooding (11 drifts) + meta-prompt bibliotheque + 6 prompts thematiques enrichis navigation.
aliases:
  - "context actuel"
  - "contexte courant"
  - "working memory"
  - "memoire de travail"
  - "etat actuel"
type: context
status: active
derniere-maj: 2026-05-23
auteur: claude
tags:
  - "#type/context"
  - "#meta/working-memory"
---

## Phase actuelle

Audit complet vault forge-brain en cours — 1/8 thèmes terminé (Claude Code), audit forge dogfooding terminé. Préparation infrastructure pour les 6 audits thématiques restants.

## Derniere session (2026-05-23)

### Décisions prises

1. **Méthode audit thématique validée** : sub-agents par CLUSTER (pas par note) + checkpoint write A avant B + self-verify FAUX fort impact avant D + distinguer Type 1/2/3 erreurs
2. **Hiérarchie sources scopée** : "Provider/auteur officiel sur SON produit/recherche = single source" — PAS "Anthropic universal"
3. **Ordre exécution audits** : forge dogfooding ✅ → méta-prompt bibliothèque → 6 thématiques (02-07)
4. **Rule transverse créée** : `.claude/rules/sequence-canonique-modification.md` pour propagation séquence A→B→C→D→E sur tous composants créateurs/modificateurs/analyseurs
5. **Architecture prompts auto-suffisants** : chaque prompt = table "Navigation vault — où lire selon le cas" obligatoire

### En cours

- Skill `/pivot-check` v1 draftée dans `Knowledge/drafts/pivot-check-skill/` — 4 fixes DA pending avant activation (cf `PIVOT-CHECK-FIXES-PENDING.md`)
- Méta-prompt bibliothèque prompts d'analyse écrit dans `output/meta-prompt-generer-bibliotheque-analyse.md` — **à relire à tête reposée avant exécution**
- 6 prompts thématiques (02-07) enrichis avec navigation vault explicite — prêts pour exécution séquentielle

### Prochaines etapes

1. **Demain à tête reposée** : relire le méta-prompt + valider catégories (~25 prompts visés)
2. **Exécuter méta-prompt en session fraîche** → génère bibliothèque dans `vault/claude-forge/07-Prompts/analyse/`
3. **Lancer les 6 audits thématiques** (02-07) en utilisant la bibliothèque générée
4. **Pending workstream séparé** : appliquer les 4 fixes DA sur skill `/pivot-check`, puis activer
5. **Test comportemental** post-bibliothèque : prendre 1 prompt généré, l'utiliser sur cas réel, vérifier qu'il fonctionne

## Fils ouverts

- **Karpathy enrichment canoniques vault** : décision = SKIP (advisor verdict, scope creep). Si plus tard un prompt généré échoue par manque navigation dans une note canonique, fixer cette note précise.
- **6 audits thématiques** : prompts prêts mais pas encore lancés (~3-4h chacun en session fraîche dédiée)
- **Propagation cross-repo audit forge** : ia_back partiellement corrigé (1 fix), neo_ia et autres repos à auditer ultérieurement

## Apprentissages clés session

- **3e incident drift doctrinal en 3 jours** (22 mai pivot neo_ia + 23 mai matin MOCs + 23 mai aprem forge dogfooding) → pattern récurrent, justifie automation `/pivot-check`
- **Fatigue session signal** : >15 échanges = arrêter options A/B/C, décider directement quand Raphael délègue
- **22 erreurs propagées dans vault Claude Code** : Justin Young split = extrapolation forge, Brad Abrams (pas Angela Jiang) = créateur Advisor Strategy, lethal trifecta = Willison, etc.

## Liens

- [[Raphael-Picard]]
- [[Claude-Forge]]
- [[methode-pivoter-doctrine]]
- [[methode-analyser-repo]]
- [[Knowledge/erreurs/erreur-22-claims-fausses-vault-claude-code-2026-05-23]]
- [[feedback_doctrine_drift_pattern]]
- [[feedback_audit_thematique_methode]]
- [[feedback_anthropic_single_source]]
- [[feedback_regle_scope_pas_universelle]]
- [[feedback_session_fatigue_decision]]
