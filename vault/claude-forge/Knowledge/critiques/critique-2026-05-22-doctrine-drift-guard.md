---
titre: "Critique — doctrine-drift-guard.py (hook SessionStart forge)"
type: knowledge
domaine: claude-code
derniere-maj: 2026-05-22
auteur: claude
aliases:
  - "critique doctrine-drift-guard"
  - "da hook drift doctrine 22 mai"
  - "verdict bloquer doctrine drift sensor"
  - "critique substring matching memory recap"
  - "DA hook regression silencieuse doctrine"
sources:
  - "Session 2026-05-22 forge — proposition Jarvis post-audit neo_ia"
  - "Test empirique : 26/26 faux positifs sur neo_ia post-purge MEMORY/RECAP"
  - "[[raisonnement-22mai-doctrine-vs-enforcement]]"
  - "[[comment-creer-hook]]"
  - "[[critique-2026-05-21-refonte-hooks-16-vers-6]]"
tags:
  - "#type/critique"
  - "#domaine/claude-code"
  - "#technique/hooks"
  - "#doctrine/2026"
resume: "DA sur doctrine-drift-guard.py — 26/26 faux positifs sur neo_ia post-purge. Verdict BLOQUER : signal-to-noise nul par construction, self-violation doctrine 22 mai, mauvaise forme (sensor permanent pour pivot one-shot). Alternative = méthode canonique de pivot doctrinal."
---

# DA — doctrine-drift-guard.py (hook SessionStart forge)

## Intention déclarée

Hook SessionStart forge qui scanne `MEMORY.md`, `.claude/RECAP.md`, `CLAUDE.md`, `.claude/agent-memory/*/MEMORY.md` et signale via `additionalContext` les phrases verbatim contredisant la doctrine 22 mai 2026, pour empêcher la régression silencieuse au prochain pivot.

## Verdict

**BLOQUANTS : 3 | AVERTISSEMENTS : 2 | NITPICKS : 1**

**Décision : BLOQUER — supprimer hook + bloc settings.json.**

Trois bloquants **indépendants** se cumulent. Aucun n'est réparable par tweak des `DRIFT_SIGNALS`. Le design est défaillant à la racine.

## Test empirique préalable

Sur neo_ia **post-purge MEMORY/RECAP session 1** :
- MEMORY.md L7 : 3 signals (architect-guard, commit-guard, dispatch-guard) → c'est `feedback_doctrine_22mai.md` créé en session 1 qui CITE ces hooks pour expliquer leur suppression. **Faux positif.**
- RECAP.md L12 + L21 + 9 autres : 11 signals → section "STOP — Doctrine 22 mai" qui liste les hooks supprimés pour les documenter. **Faux positifs.**
- CLAUDE.md L24, L98 : 12 signals → section Critiques mentionne "Workflow hooks supprimés 22 mai 2026". **Faux positifs.**

**Total : 26 alertes, 100% faux positifs**, alors que MEMORY/RECAP ont été correctement purgés.

## Bloquant 1 — Signal-to-noise = 0 par construction

Substring matching case-insensitive ne distingue PAS :
- **Prescription** ("TOUJOURS architect" → vrai positif)
- **Mention historique** ("Le hook architect-guard a été supprimé" → faux positif)
- **Négation** ("Ne PAS faire X" → devrait être OK)

Défaut **conceptuel**, pas défaut de patterns. Aucune liste de regex polish n'amène ce hook au-dessus de ~50% de précision : **la documentation correcte d'un pivot mentionne TOUJOURS l'ancienne doctrine pour la déclarer obsolète. Le hook punit la documentation correcte.**

Le steady state du hook EST le bruit. La seule fenêtre où il dirait vrai = entre le moment du pivot et la rédaction de la note canonique qui le documente. Dès que la note canonique existe (ce qui DOIT arriver), elle déclenche le hook éternellement. **Sensor anti-corrélé avec sa propre raison d'être.**

## Bloquant 2 — Mauvaise forme pour le problème

Le bug est un **événement one-shot** (un pivot doctrinal arrive ~1×/trimestre). Un SessionStart hook qui tourne à *chaque* démarrage de session est la mauvaise forme pour un événement ponctuel.

Alternative : checklist process exécutée une seule fois au moment du pivot.

## Bloquant 3 — Self-violation doctrine 22 mai

Doctrine canonique ([[raisonnement-22mai-doctrine-vs-enforcement]] + [[comment-creer-hook]]) :
> "Hooks = lint / security / scope UNIQUEMENT. **JAMAIS workflow agentique.**"

Ce hook :
- N'est PAS du **lint** (pas d'AST, pas de validation syntaxique)
- N'est PAS de la **sécurité** (pas de credential, pas de secret, pas de scope filesystem)
- N'est PAS du **scope** (pas de boundary cross-repo)
- EST un **workflow hook sur la méta-doctrine** — il mécanise la conformité doctrinale d'un texte d'opinion (MEMORY/RECAP)

C'est exactement le pattern que la doctrine 22 mai a tué en supprimant `architect-guard`. On transpose le même anti-pattern un niveau au-dessus. **Même classe d'erreur, abstraction supérieure.**

Référence vault : [[critique-2026-05-21-refonte-hooks-16-vers-6]] — pattern identique ("raisonner par sensors permanents au lieu de par friction/valeur réelle").

## Avertissements

### Détection `repo_root` par cwd

`find_repo_root()` remonte 6 niveaux en cherchant `.claude/`. Sur poste avec repos imbriqués (`neot-v2/neoteem-brain` dans `neot-v2/`), le repo root remonté peut être surprenant.

### `DRIFT_SIGNALS` hardcodé en Python

Une approche déclarative (YAML) atténuerait mais NE résoudrait PAS le problème — la critique conceptuelle (signal-to-noise, self-violation, mauvaise forme) reste. **Ne pas chercher à sauver ce hook par du polish.**

## Nitpick

Deux patterns redondants pour "Aucune commande a/à taper" (accent et sans accent). Workaround pour un problème qui ne devrait pas exister si on traite le problème à la racine.

## Alternative correcte

**Ne pas faire marcher ce hook. Le remplacer par une étape de process.**

Le bug réel session 22 mai = **j'ai oublié de purger MEMORY/RECAP au moment du pivot doctrinal**. C'est un défaut de *méthode*, pas un défaut d'*enforcement*.

Solution : créer note canonique `[[methode-pivoter-doctrine]]` avec checklist 5 étapes :
1. Note canonique vault à jour
2. Rules du repo
3. CLAUDE.md du repo (racine + secondaires)
4. **PURGE MEMORY / RECAP / agent-memory** ⚠️ étape la plus oubliée
5. Test session fraîche

Optionnel : script one-shot manuel `tools/doctrine-pivot-checklist.py` invoqué une seule fois au moment du pivot (PAS un hook permanent).

## Pattern à mémoriser

**Avant d'écrire un hook substring/regex** : grep les patterns sur les fichiers cibles AVANT de coder le hook. Si le grep produit des matches dans la documentation canonique de ce que le hook protège, le hook est mal conçu — sa raison d'être documentée déclenche sa propre alarme. Symétrique de [[feedback_da_failure_options]] mais en amont : tester adversement le hook avant écriture, pas seulement après.

## Actions appliquées (session 2026-05-22)

- ✅ Hook supprimé : `C:/Users/raphael.picard_neote/Documents/claude-forge/.claude/hooks/doctrine-drift-guard.py`
- ✅ Bloc activation retiré : `C:/Users/raphael.picard_neote/Documents/claude-forge/.claude/settings.json` (SessionStart)
- ✅ Note canonique créée : [[methode-pivoter-doctrine]] (vrai fix au bon endroit)
- ✅ Feedback mémoire forge mis à jour pour pointer vers méthode au lieu de hook

## Wikilinks

- [[methode-pivoter-doctrine]] — la VRAIE solution
- [[raisonnement-22mai-doctrine-vs-enforcement]] — doctrine violée par le hook
- [[comment-creer-hook]] — critères que le hook NE PASSAIT PAS
- [[critique-2026-05-21-refonte-hooks-16-vers-6]] — pattern d'erreur identique transposé
- [[feedback_recurring_meta_anti_pattern]] — anti-pattern Jarvis caractérisé

---

**Fin critique DA** — verdict BLOQUER appliqué session 2026-05-22.
