---
titre: "Méthode pour pivoter une doctrine sans régression silencieuse"
resume: "Checklist 5 étapes obligatoires lors d'un pivot doctrinal majeur (ex: 22 mai 2026 doctrine vs enforcement). Sans elle : MEMORY/RECAP non purgés annulent invisiblement le pivot à chaque session. Ne pas remplacer par un hook (anti-pattern documenté)."
aliases:
  - "methode pivoter doctrine"
  - "checklist pivot doctrinal"
  - "comment changer doctrine"
  - "purge MEMORY RECAP apres pivot"
  - "regression silencieuse doctrine"
  - "doctrine drift one-shot fix"
derniere-maj: 2026-05-23
auteur: claude
type: technique
sources:
  - "Bug session 2026-05-22 neo_ia — MEMORY/RECAP non purgés annulaient doctrine 22 mai"
  - "DA critique-2026-05-22-doctrine-drift-guard — verdict BLOQUER hook palliatif"
  - "[[raisonnement-22mai-doctrine-vs-enforcement]]"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#sujet/methode"
  - "#meta"
---
# Méthode pour pivoter une doctrine sans régression silencieuse

> **Note méta canonique forge** — quand la doctrine d'un repo pivote (changement de pipeline, ajout/suppression de hooks, changement workflow), cette checklist S'APPLIQUE obligatoirement.

---

## QUOI — Définition

**Checklist 5 étapes** pour effectuer un pivot doctrinal sans laisser de résidus textuels qui réactivent l'ancienne doctrine à chaque session future.

---

## POURQUOI — Le bug évité

### Incident origine (session 2026-05-22 neo_ia)

Le pivot 22 mai ("doctrine vs enforcement", suppression de 7 hooks workflow) avait été appliqué dans les rules (`when-to-architect.md`, `quality-gates.md`, `orchestrator-mindset.md`). MAIS :

- `MEMORY.md` racine contenait toujours `pipeline-enforcement` ("TOUJOURS architect → dev → test → reviewer → commit") et `no-direct-coding` ("Session principale = CTO, ne code JAMAIS directement. Hooks architect-guard et commit-guard bloquent.")
- `.claude/RECAP.md` décrivait le pipeline pré-pivot avec phase REFACTOR explicite

**Résultat** : à chaque démarrage de session, l'utilisateur rechargeait l'ancienne doctrine. Le travail doctrinal du 22 mai était **invisiblement annulé**.

Découvert seulement par l'audit profond 10-agents du 22 mai (audit workflow E2E spécifiquement).

### Pourquoi PAS un hook palliatif

Tentation : créer un hook SessionStart `doctrine-drift-guard.py` qui scanne MEMORY/RECAP et alerte sur phrases-signal. **REFUSÉ** par DA (cf [[critique-2026-05-22-doctrine-drift-guard]]) :

1. **Signal-to-noise = 0 par construction** : la doc correcte du pivot mentionne TOUJOURS l'ancienne doctrine pour la déclarer obsolète → le hook punit la documentation correcte. Test empirique : 26/26 faux positifs sur neo_ia post-purge.
2. **Mauvaise forme** : pivot doctrinal = événement one-shot (~1×/trimestre). Hook permanent au SessionStart = mauvais outil.
3. **Self-violation doctrine 22 mai** : "hooks = lint/security/scope, JAMAIS workflow". Mécaniser conformité doctrinale = workflow hook abstrait. Isomorphe à `architect-guard` (supprimé 22 mai).

**Pattern à mémoriser** : avant d'écrire un hook substring/regex, grep les patterns sur les fichiers cibles. Si le grep matche la doc canonique de ce que le hook protège, le hook est mal conçu.

---

## COMMENT — Checklist 5 étapes (one-shot, manuelle)

### Étape 1 — Note canonique vault à jour

Créer ou mettre à jour la note `raisonnement-<date>-<sujet>.md` dans `Knowledge/raisonnements/` du vault forge-brain. Cette note est la **source de vérité** du pivot (motivation, décisions, hooks supprimés, rules modifiées).

### Étape 2 — Rules du repo

Pour chaque repo concerné par le pivot :
- Mettre à jour les rules `.claude/rules/` (quality-gates, when-to-architect, orchestrator-mindset, agent-delegation, etc.)
- Supprimer les rules devenues obsolètes
- Vérifier `description:` frontmatter présent partout (sinon rule MORTE silencieusement)

### Étape 3 — CLAUDE.md du repo (racine + secondaires)

- Mettre à jour le CLAUDE.md racine
- Mettre à jour les CLAUDE.md secondaires (`apps/*/CLAUDE.md`, `packages/*/CLAUDE.md`)
- Ajouter STOP bloc <ligne 25 si pivot critique (pattern `critical-instructions-top-of-file`)

### Étape 4 — PURGE MEMORY / RECAP / agent-memory ⚠️ CRITIQUE

**Étape la plus oubliée.** C'est CELLE qui crée la régression silencieuse si manquée.

- `MEMORY.md` racine : supprimer ou réécrire les entrées contradictoires
- `.claude/RECAP.md` : refonte complète si pipeline a pivoté
- `.claude/agent-memory/*/MEMORY.md` : chaque dossier agent — vérifier les entrées et purger
- **Marquer historique au lieu de supprimer si l'info reste utile** : préfixer `[OBSOLÈTE <date>]` ou créer entrée explicative qui CITE l'ancienne doctrine pour la déclarer obsolète

### Étape 5 — Test session fraîche

- Lancer une nouvelle session Claude Code dans le repo
- Demander une tâche typique (feature M, bug fix)
- **Vérifier** que la session NE PROPOSE PAS la doctrine pré-pivot
- **Vérifier** que la session applique la nouvelle doctrine sans friction

Si la session pré-propose l'ancienne doctrine → retour étape 4, audit plus profond des fichiers texte.

---

## QUAND — Critère d'application

### Pivot doctrinal MAJEUR (checklist complète obligatoire)

- Suppression/ajout de hooks workflow
- Changement structurel du pipeline (TDD strict → conditionnel, etc.)
- Suppression/ajout d'agent critique
- Changement de modèle/effort par défaut sur agents
- Renaming de patterns (architect → architect-quick + architect-deep)

### Évolution mineure (checklist légère — étapes 2-3-5)

- Modification d'une seule rule
- Ajout d'un nouveau skill
- Renaming non doctrinal

---

## ANTI-PATTERNS

### ❌ Hook substring-matching sur MEMORY/RECAP

Voir [[critique-2026-05-22-doctrine-drift-guard]]. Trois bloquants conceptuels indépendants. Ne pas refaire cette erreur.

### ❌ Pivot par modification des rules seule

Sans étape 4 (purge MEMORY/RECAP), le pivot est invisiblement annulé.

### ❌ Suppression brutale des entrées MEMORY contradictoires sans note explicative

Préférer : remplacer par une entrée qui POINTE vers la note canonique du pivot (`[[raisonnement-<date>-<sujet>]]`). Garde la traçabilité historique.

### ❌ Pas de test session fraîche

Sans étape 5, on ne sait pas si le pivot a vraiment pris. La régression peut rester latente plusieurs sessions avant d'être détectée.

---

## EXEMPLE CONCRET — Pivot 22 mai 2026 neo_ia

| Étape | Status | Détail |
|-------|--------|--------|
| 1. Note canonique vault | ✅ | `[[raisonnement-22mai-doctrine-vs-enforcement]]` créée |
| 2. Rules repo | ✅ | when-to-architect.md créé, quality-gates.md réécrit, orchestrator-mindset.md mis à jour |
| 3. CLAUDE.md repo | ✅ | racine mis à jour. Secondaires non auditeés (faille découverte 22 mai) |
| 4. PURGE MEMORY/RECAP | ❌ → ✅ session 2026-05-22 | MEMORY.md L4-5 + RECAP.md L12-21 contenaient doctrine pré-pivot. Découvert par audit 10-agents. Purgé en session. |
| 5. Test session fraîche | ⏳ post-session 2 | À faire après déploiement complet |

**Délai régression non détectée** : ~10 jours (22 mai pivot initial → 22 mai 2026 audit profond)

---

## WIKILINKS

- [[raisonnement-22mai-doctrine-vs-enforcement]] — exemple concret de pivot doctrinal
- [[critique-2026-05-22-doctrine-drift-guard]] — DA qui a refusé l'approche hook palliatif
- [[methode-analyser-repo]] — méta-méthode (analyse repo) — étape 1 devrait inclure scan MEMORY/RECAP
- [[workflow-claude-code-optimal]] — workflow général
- [[comment-creer-hook]] — critères pour décider hook vs rule (ce hook palliatif NE PASSAIT PAS les critères)
- [[feedback_recurring_meta_anti_pattern]] — anti-pattern Jarvis (1 incident → refonte structurelle)

---

**Fin note canonique `methode-pivoter-doctrine.md`** — 9/8 chantier 22 mai 2026 (BONUS post-pivot).

---

## CORRECTION POST-AUDIT 23 MAI 2026 — citation pivot reformulée

### C5.7 — "Claude decides when to parallelize" (formule paraphrasée)

**Avant** : citation du pivot 22 mai présentée comme verbatim Anthropic Agent SDK :
> "Claude decides when to parallelize — you're defining the capability, not the scheduling."

**Vérification directe docs Anthropic 23 mai 2026** : cette formule exacte n'apparaît pas dans Agent SDK overview. Les verbatims réels sont :

- [code.claude.com/docs/en/agent-sdk/overview](https://code.claude.com/docs/en/agent-sdk/overview) : *"Claude decides when to call a tool based on the user's request"*
- Docs Skills : *"Skills are model-invoked: Claude autonomously chooses when to use them based on context"*
- *"Claude autonomously invokes when relevant"*

### Le pivot 22 mai reste 100% valide

Le **principe** "Claude decides when to invoke (sub-agents, tools, skills)" est canonique Anthropic, attesté par 3+ phrases verbatim. La **formule exacte** "Claude decides when to parallelize — you're defining the capability, not the scheduling" était une **paraphrase pédagogique** (probablement inférée du concept Agent SDK).

**Sources solides du pivot 22 mai** (à utiliser à la place) :
- Boris Cherny "thinnest wrapper" (Latent Space, Pragmatic Engineer)
- Boris "All the secret sauce — it's all in the model" (Latent Space verbatim)
- Anthropic docs hooks recommandés pour lint/security
- Anthropic Agent SDK : "Claude decides when to call a tool", "Claude autonomously invokes"

### Anti-pattern à mémoriser

**Présenter une paraphrase comme verbatim Anthropic** = même pattern d'erreur que :
- C5.6 Justin Young split modèles (inféré, pas verbatim)
- C8.1 "Agent = Model + Harness" attribué à Fowler (en fait Hashimoto popularise)
- C3.3 Angela Jiang advisor 5× (en fait Brad Abrams, pas de chiffre)

**Méthode anti-régression** : avant de citer verbatim Anthropic, **fetch directement la page docs**. Sub-agents peuvent se tromper.

---

Source audit : `output/audit-vault-thematique/01-claude-code/C-croisement-revise.md`
