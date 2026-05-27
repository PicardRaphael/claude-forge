---
name: diagnostic-empirique-avant-affirmer-une-garde
description: Avant d'ÉCRIRE dans un fichier doctrinal (CLAUDE.md, note canonique, settings, hook) qu'une garde technique existe (deny/hook/permission/bloqué), la vérifier matériellement (parse JSON settings, grep hooks, ls). JAMAIS inférer une garde depuis un comportement observé. Citer la preuve dans le commit/body, sinon ne pas écrire l'affirmation.
metadata:
  type: feedback
---

Avant d'écrire « X est en deny / protégé / bloqué par hook / en permission » dans n'importe quel artefact doctrinal (CLAUDE.md, notes canoniques vault, settings, hooks, ADR), EXÉCUTER la vérification matérielle ET citer la preuve. Ne JAMAIS inférer l'existence d'une garde technique à partir d'un comportement observé.

**Why:** 27 mai 2026 — écrit dans CLAUDE.md « `git merge *` est en deny global (`~/.claude/settings.json`), by design » à partir du seul symptôme observé « l'agent travaille sur une branche par défaut ». Diagnostic empirique ultérieur (parse JSON sur 4 couches settings + grep hooks) : **aucun deny merge nulle part**, aucun hook bloquant. Les 12 entrées deny globales sont toutes des commandes destructives OS (`rm -rf`, `format`, `mkfs`...), zéro git. Le « branch first » est un mécanisme NATIF du harness Claude Code (system prompt), pas une permission. Doctrine fausse documentée ~6h avant détection. Cause racine : inférer une cause technique depuis un comportement sans matérialiser la preuve.

**How to apply:** avant d'écrire une affirmation de garde dans un fichier doctrinal :
- Parse settings : `py -c "import json,os; print(json.load(open(os.path.expanduser('~/.claude/settings.json')))['permissions']['deny'])"` (+ settings.local.json global + repo `.claude/settings.json` + `.claude/settings.local.json` = 4 couches)
- Grep hooks : `grep -i "<pattern>" .claude/hooks/`
- Citer la preuve dans le commit message OU le body de la note. **Si pas de preuve = ne pas écrire l'affirmation.**

Distinct de [[verify-empirique-avant-affirmation-session]] (vérifier une affirmation factuelle EN COURS de session, ex « pourquoi X a changé ») : ici l'angle est l'**écriture durable d'une garde dans un artefact doctrinal** — l'erreur survit à la session et se propage (CLAUDE.md lu chaque session). Lié à [[verify-exhaustive-claims]] (grep avant « tous/aucun/zéro ») et au piège méta : une affirmation de garde fausse peut traverser agent + humain + advisor sans que personne ne demande la preuve.
