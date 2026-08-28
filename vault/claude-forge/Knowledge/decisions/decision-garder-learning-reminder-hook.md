---
titre: "Décision — learning-reminder : détecteur advisory Claude uniquement (V3, 28 août 2026)"
resume: "Le Stop hook learning-reminder reste un détecteur déterministe non bloquant côté Claude seulement. Il émet un systemMessage si un signal n'a pas de preuve de capitalisation correspondante. Aucun portage Stop Codex : protocole incompatible et risque de continuation forcée."
aliases:
  - "decision learning-reminder"
  - "learning-reminder detecteur"
  - "learning-reminder V3"
  - "garder learning-reminder"
  - "exception doctrine learning-reminder"
  - "Stop hook learning-reminder décision"
  - "proactivity-reminder supprimé"
domaine: claude-code
type: decision
derniere-maj: 2026-08-28
auteur: codex
tags:
  - "#type/decision"
  - "#domaine/claude-code"
  - "#sujet/hooks"
  - "#doctrine/2026"
---

# Décision — learning-reminder : détecteur advisory Claude uniquement

## Décision active (28 août 2026)

`learning-reminder` reste un **capteur déterministe, non bloquant et sans écriture**, déployé sur le Stop Claude Code uniquement.

| Propriété | Contrat |
|---|---|
| Détection | liste fermée : correction explicite, nouvelle norme, claim périmé, gotcha/bug et préférence personnelle explicite |
| Preuve de traitement | par catégorie ; une lecture ne compte jamais comme écriture |
| Sortie | `systemMessage` seulement si un signal reste non capitalisé |
| Effet | aucune mutation, aucune décision sémantique, aucune continuation forcée |
| Anti-boucle | `stop_hook_active` + marqueur par `session_id` |
| Robustesse | fail-open sur transcript absent, JSON invalide ou erreur |
| Writer | session principale uniquement, selon `docs/second-brain/session-capture.md` |

La preuve de profil est stricte : seuls un mutateur MCP ciblant exactement [[Raphael-Picard]] ou une écriture legacy explicite de l'adaptateur local comptent. `read_note("Raphael-Picard")`, une simple mention textuelle ou une mutation d'une autre note ne masquent pas le signal.

## Pourquoi Claude uniquement

Ne pas simuler la parité avec Codex :

- `additionalContext` n'est pas supporté sur l'événement Stop Codex ;
- `decision:"block"` signifie « continuer le tour » côté Codex ;
- un hook Codex nouveau ou modifié est skippé jusqu'à validation de son hash.

Codex utilise donc les règles, les skills `done` / `project-memory` et `memory-recall` en pré-action. Aucun Stop hook `learning-reminder` n'est enregistré sous `.codex/`.

## Pourquoi garder le capteur

Le rappel systématique historique avait un payoff nul : huit réponses « rien à sauvegarder » et aucune capture attribuable. Le détecteur conditionnel reste acceptable car :

- silence sur une session banale ou déjà capitalisée ;
- coût borné par lecture de queue de transcript et regex locales ;
- aucun jugement ni écriture cachée ;
- filet mesurable pour les signaux explicitement formulés.

## Clause de sortie

Supprimer ou repenser le détecteur si l'une de ces conditions est mesurée :

- au moins deux faux positifs où une preuve correspondante existait ;
- un faux négatif sur un signal de la liste fermée ;
- un coût ou bruit supérieur à son apport ;
- un mécanisme pré-action couvre empiriquement le cas sans perte.

Mesurer les alertes émises contre les captures réelles ; ne pas conclure depuis une impression.

## Historique conservé

### V2 — 29 juillet 2026

Le rappel systématique `decision:block` est devenu détecteur conditionnel après mesure du payoff nul. La version forge a aussi reçu `stop_hook_active` et un marqueur par session. La V2 gardait toutefois le blocage conditionnel et décrivait des preuves trop larges.

### V1 — 29 mai 2026

`proactivity-reminder` a été supprimé ; `learning-reminder` a été gardé comme exception au motif que `/done` n'était pas exécuté de façon fiable. Les piliers techniques de cette décision ont ensuite été invalidés : `additionalContext` Claude est devenu disponible et `once:true` s'est révélé ignoré dans `settings.json`.

## Liens

- [[da-blocking-non-arbitre]] — journal de la résolution du faux portage Codex

- [[comment-creer-hook]]
- [[comment-creer-hook-codex]]
- [[loop-apprentissage-codex]]
- [[raisonnement-2026-08-28-profil-projets-vault-canoniques]]
- [[feedback_recurring_meta_anti_pattern]]
