---
titre: "Raisonnement 30 sept. 2026 — plus de Sonnet dans forge : Opus medium pour l'exécution, Opus high pour le jugement"
resume: "Pivot validé par Raphaël le 30 sept. 2026 : aucun composant forge ne tourne plus sur Sonnet ni sur Haiku, ni en effort low. Exécution et mécanique passent en opus + effort medium, le jugement reste opus + high, Fable 5.1 reste un step-up mesuré. Périmètre forge seul ; ia_back et neo_ia gardent leur partage Sonnet/Opus."
aliases:
  - "zero sonnet forge"
  - "pivot zero sonnet septembre 2026"
  - "plus de sonnet"
  - "opus medium execution"
  - "allocation modele 30 septembre 2026"
  - "plancher opus medium"
type: raisonnement
derniere-maj: 2026-09-30
auteur: claude
sources:
  - "https://code.claude.com/docs/en/model-config"
  - "https://platform.claude.com/docs/en/models/sonnet-5-5/whats-new-sonnet-5-5"
  - "https://platform.claude.com/docs/en/about-claude/pricing"
tags:
  - "#type/raisonnement"
  - "#domaine/claude-code"
  - "#statut/canonique"
---

# Plus de Sonnet dans forge (30 sept. 2026)

## Décision

Arbitrage de Raphaël, 30 sept. 2026 : *« plus de sonnet, minimum opus medium ou opus high ou fable »*, précisé en deux choix :

| Type de composant | Avant | Après |
|---|---|---|
| Exécution et mécanique (dev, maintenance, scan, recap) | `sonnet` + `high` (ou `medium` pour le mécanique) | **`opus` + `medium`** |
| Jugement (reviewers, analystes, critique) | `opus` + `high` | inchangé |
| Step-up | Fable 5.1 mesuré | inchangé : Fable seulement après une mesure qui montre qu'Opus 5.5 plafonne |

Le plancher `opus` + `medium` vaut pour tout composant forge : ni `haiku` (autrefois « exploration rapide »), ni effort `low` (autrefois « inspection triviale »). Raphaël l'a confirmé le même jour, en réponse à la question sur ces deux résidus. Aucun composant n'utilisait l'un ou l'autre ; seules la doctrine écrite et les gabarits les proposaient encore.

Périmètre : **forge uniquement**. Les repos projet (ia_back, neo_ia) gardent leurs agents dev `sonnet, high` jusqu'à une décision séparée.

## Pourquoi

- Depuis Claude Code 2.1.284 (28 sept.), l'alias `sonnet` résout vers **Sonnet 5.5** sur l'API Anthropic, dont les niveaux d'effort sont recalibrés (*« Re-run your effort sweep rather than carrying a setting over »*) et dont l'effort par défaut dans Claude Code est `medium`. Le `sonnet, high` de forge était donc un réglage hérité de Sonnet 5, jamais mesuré sur le nouveau modèle.
- Doc Claude Code (`code.claude.com/docs/en/model-config`, 30 sept.) : *« In Anthropic's testing, Opus 5.5 at `medium` matches or exceeds Opus 5 at `high` on coding and knowledge-work evaluations. »* Opus 5.5 à `medium` donne un plafond de capacité supérieur à Sonnet pour un effort modéré.
- Critère Lydia Hallie (« did it not try hard enough, or did it not know enough? ») : passer d'un petit modèle à effort élevé vers un gros modèle à effort modéré achète du *savoir*, pas seulement du travail par tour.

## Coût accepté

Opus 5.5 coûte le double de Sonnet 5.5 au token ($4/$20 contre $2/$10 par MTok). L'effort `medium` en compense une partie. Raphaël a tranché en connaissance de cause.

## Précédent

Forge a déjà appliqué une politique « zéro Sonnet » le **5 mai 2026**, remplacée le **21 mai** par le partage Sonnet exécution / Opus jugement (argument EVE Legal CwC : *« frontier quality at 5x lower cost »*). Ce qui diffère le 30 sept. : Sonnet 5.5 casse la calibration existante, Opus 5.5 est moins cher qu'Opus 5 ($4/$20 contre $5/$25) et Anthropic documente Opus 5.5 `medium` au niveau d'Opus 5 `high`. Un retour au partage devrait s'appuyer sur une mesure, pas sur le prix seul.

## Application (checklist methode-pivoter-doctrine)

- **Composants** : agents `code-dev`, `self-updater` ; skills `audit-departement`, `agentshield-like-scanner`, `config-guardian`, `configure-claude-desktop`, `evolve`, `methode-pivoter-doctrine`, `python-ref`, `recap`, `skill-evolve`, `vault-health` → `opus` + `medium`, jumeaux `.agents/skills/` compris.
- **Doctrine** : `CLAUDE.md`, gabarits et checklists `subagent-creator` / `skill-creator`, `cc-features-ref`, critères « split » et « downgrade Haiku » de `repo-inspector`, rule `sequence-canonique-modification`, grilles `skill-evolve` / `outcomes-test`.
- **Mémoire** : `feedback_allocation_modele_effort`, `feedback_preference_modele_opus`, index `MEMORY.md`.
- **Vault** : [[effort-opus-47-doctrine-anthropic-2026]], [[doctrine-par-modele-opus5-fable5]], [[comment-creer-agent]], [[workflow-claude-code-optimal]].

## Ce qui reste ouvert

- Le `high` des composants de jugement sur Opus 5.5 reste un choix délibéré non mesuré (pivot du 25 sept., [[raisonnement-2026-09-25-effort-opus-5-5]]).
- Aucune mesure n'établit encore qu'`opus, medium` bat `sonnet, high` sur les tâches d'exécution de forge : c'est une décision de préférence adossée à la doc Anthropic, à confirmer par un run comparatif si le coût devient un sujet.

## Liens

- [[raisonnement-2026-09-25-effort-opus-5-5]] — pivot effort Opus 5.5
- [[Opus 5.5]] · [[Sonnet 5]] · [[Fable 5.1]]
- [[methode-pivoter-doctrine]]

## Bilan d'application (30 sept. 2026)

| Étape methode-pivoter-doctrine | État |
|---|---|
| 1. Note canonique | cette note |
| 2. Rules | `sequence-canonique-modification` alignée |
| 3. CLAUDE.md | ligne « Modèles » réécrite (v5.1), puis plancher `opus` + `medium` explicité (ni `haiku` ni `low`) |
| 4. Mémoire | `feedback_allocation_modele_effort` (ancien partage marqué obsolète pour forge), `feedback_preference_modele_opus`, index `MEMORY.md` |
| 4bis. `pivot-check` | PASS (commit `e187fa0`) — résidus trouvés et corrigés : [[methode-analyser-repo]], [[Home]], [[MOC-Modeles]], [[Opus 5]], [[Sonnet 5]] ; second passage pour `haiku` / `low` après la précision de Raphaël |
| 5. Session fraîche | à faire par Raphaël |
