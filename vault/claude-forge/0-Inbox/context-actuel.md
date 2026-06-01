---
titre: Context Actuel
resume: Working memory dynamique -- mis a jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, memoire de travail, etat actuel]
type: context
status: active
derniere-maj: 2026-05-30
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---

## Phase actuelle
Durcissement neoteem-brain (doctrine de profondeur anti-survol Confluence/Jira). Deux fixes livrés et poussés sur master : (1) plan file débloqué dans `guard-external-writes.py`, (2) doctrine lecture-complete étendue aux sources externes.

## Derniere session (2026-05-30 — soir)
### Decisions prises
- **Fix profondeur = étendre la doctrine existante** (lecture-complete + anti-invention), pas en créer une nouvelle. Confluence/Jira ajoutés aux sources « lire en entier » ; `vault-enricher` rattaché ; « pertinentes » tué dans son prompt ; tools Jira ajoutés ; `sources:` exige page-ID/clé exacts.
- **Pas de hook, pas de gate** pour la profondeur : non mesurable via stdin (hook) + Raphael a tranché « prompt strict seulement » (gate).
- **Délégation NON retenue comme garde-fou de profondeur** (révision de ma reco initiale) : `lecture-complete` lie déjà la session principale, donc l'extension referme le trou seule. Sans gate, « délègue toujours » serait une règle non-vérifiable de plus.
- Fix plan file : exception explicite en tête du hook, vérifiée empiriquement (4 cas, protections existantes intactes).
- Convention git neoteem-brain : commit/push direct sur master, pas de branche.
### En cours
- Rien d'ouvert : 2 commits poussés sur `master` neoteem-brain (`62b1bf6` hook + `3236ec0` doctrine). Le pipeline global de Raphael a tourné entre-temps et applique déjà la profondeur (commits « sourcees PROFONDEUR Confluence+code lus entier »).
### Prochaines etapes
- (Optionnel) Test comportemental : relancer `vault-enricher` sur un sujet et vérifier qu'il lit les pages Confluence en entier + cite page-ID.
- (Séparé) Si besoin : traiter la délégation sous l'angle conformité frontmatter/templates/pipeline (≠ profondeur).
- ⚠️ Hygiène : 232 fichiers memory/ (cible <100) → `/clean-memory` en session dédiée.

## Fils ouverts
- Trilogie docs stratégiques IA Neoteem : présentation Jérôme puis CODIR (commit `3a0f373`).
- Cadrage NeoMail (besoin/fonctionnalités/forme) = décision client, trame d'interview à préparer.
- Vérifier que le repo claude-forge est bien privé (docs CODIR confidentiels commités).

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
