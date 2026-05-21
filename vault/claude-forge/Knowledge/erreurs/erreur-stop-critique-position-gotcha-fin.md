---
titre: "STOP CRITIQUE en gotcha fin de fichier ignoré par le modèle"
resume: "Skill /spec ia_back développait directement le code au lieu de générer SPECs car instruction STOP en gotcha ligne 179 (fin de fichier), sous-pondérée vs version neo_ia avec STOP en gras ligne 18 (haut de fichier)"
aliases:
  - "erreur STOP gotcha fin"
  - "erreur instruction critique position"
  - "primacy recency skills"
  - "STOP CRITIQUE position"
  - "instruction sous-ponderee fin fichier"
gravite: haute
domaine: claude-code
type: erreur
derniere-maj: 2026-05-21
auteur: claude
tags:
  - "#type/erreur"
  - "#domaine/claude-code"
  - "#erreur/skill"
  - "#domaine/prompt-engineering"
sources:
  - "Session 2026-05-20 — bug observé chez Jérôme sur /spec ia_back"
  - "[[forge-prompt-machine]] — primacy/recency effect"
---

## Ce qui s'est passé

Session 2026-05-20 chez Jérôme : `/spec` ia_back lancé avec un ticket Jira. La skill aurait dû :
1. Générer SPEC.md + BRIEFs dans `TODO/feature-X/`
2. STOP — attendre validation user
3. Lancer `/go` seulement après validation

À la place, la skill a **directement développé** du code (pas de dossier TODO créé) et **tenté de toucher neo_ia depuis ia_back** (cross-repo non autorisé). Jérôme a dû interrompre via `/btw` pour éviter perte de travail.

## Cause racine

Diagnostic comparatif `/spec` ia_back vs `/spec` neo_ia (qui marchait pour Raphael) :

| Repo | Position instruction STOP | Comportement modèle |
|------|---------------------------|---------------------|
| neo_ia (marche) | **Ligne 18, en gras, juste après titre** | Suit la consigne, génère SPECs et STOP |
| ia_back (bug) | **Ligne 179, en gotcha fin de fichier** | Ignore la consigne, développe directement |

**Texte identique. Position différente. Comportement opposé.**

Confirmation théorique : note vault `forge-prompt-machine` documente le **primacy/recency effect** — Claude donne plus de poids aux instructions au début et à la fin du prompt. Une instruction en gotcha noyée au milieu/fin d'une longue liste de gotchas se retrouve dans la "vallée d'attention" du modèle.

## Fix appliqué

Nouvelle skill `/spec` unifiée (fusion `/spec` + `/decompose-ticket`) avec :

1. **STOP CRITIQUE en blockquote ligne 18** (en gras, immédiatement après le titre)
2. **Gate AskUserQuestion bloquant** en fin de Phase 4 (3 options A/B/C, décision tree explicite)
3. **Phase 5 (vagues parallèles) CONDITIONNEL** XL uniquement (pas auto-lancement)
4. Source unique dans `claude-forge/.claude/skills/spec/`, déployée vers ia_back + neo_ia

Commits : `e8ef466` (forge), `2d0d094` (ia_back), `e690461` (neo_ia).

## Apprentissage

**Pattern à appliquer sur toutes les skills futures :**

- Instructions critiques (STOP, interdit, contrat sécurité) → top 20% du fichier OBLIGATOIRE
- En gras/callout blockquote, pas en bullet point noyé
- Section "Gotchas" = rappels secondaires uniquement, jamais l'unique placement d'une règle critique
- Audit existant : tout skill avec une section Gotchas DOIT être audité — toute règle critique en Gotchas doit être remontée en tête de body

## Anti-pattern documenté

Erreur typique de rédacteur (humain ou IA) : "Je mets cette règle dans Gotchas pour ne pas alourdir le début". Faux raisonnement — une règle critique JUSTIFIE d'alourdir le début. Si elle n'est pas critique, elle n'a rien à faire en Gotchas non plus.

## Liens

- [[forge-prompt-machine]] — Primacy/recency effect documenté
- [[Thariq Shihipar]] — Section Gotchas = "contenu le plus important" (mais pas exclusif des règles critiques)
- [[critique-session-2026-05-20-running-notes-decompose-xread-mcp]] — DA matin avait identifié le pattern claim-vs-code pour x-read, même famille
- [[pattern-spec-driven-development]] — Pattern foundational mis à jour avec ce learning
- [[feedback_critical_instructions_top_of_file]] (mémoire) — Règle généralisée
