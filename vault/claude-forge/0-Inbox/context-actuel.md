---
titre: Context Actuel
resume: Working memory dynamique -- mis a jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, memoire de travail, etat actuel]
type: context
status: active
derniere-maj: 2026-06-01
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---

## Phase actuelle
Renforcement du réflexe de consultation vault sur claude-forge + bascule workflow git en full-main. Deux livrables poussés sur `main`.

## Derniere session (2026-06-01)
### Decisions prises
- **Réflexe vault = Option C appliquée** : `skill-activation.py` re-fire le rappel `forge-brain` **par SUJET** (skill/agent/hook/claudemd/general) au lieu de once-per-session global. Cas skill→agent dans une même session = 2 rappels (canoniques vault différentes), anti-spam même sujet préservé. Rétro-compatible avec les 23 entrées legacy. Advisory (exit 0, conforme doctrine 22 mai non-workflow-hook).
- **`.skill-triggers.json`** : entrée `forge-brain` en `triggers_by_subject`, sujet `general` couvre les mots d'intention (propose/audit/analyse profonde/ton avis/recommande/optimise/pourquoi). Exclut fix/corrige/salut/merci.
- **FULL MAIN par défaut** (CLAUDE.md v3.5) : commit/push direct sur `main`, plus jamais la question branche/main. Branche uniquement sur demande explicite. Capitalisé `feedback_commit_full_main_defaut`.
- **Tripartite hors-scope** : trou de routing « analyse profonde » → boris/ecc/will-auditor laissé documenté non-appliqué (Raphael a redscopé « juste pour le mcp »). Advisor disait non, DA disait trigger-rappel léger. Option prête-à-coller dans la note d'erreur.
### En cours
- Rien d'ouvert. 4 commits poussés sur `main` : `4744b56` (hook réflexe vault), `45903c7` (CLAUDE.md v3.5 full main), `5edbcad` (cleanup output/ + metrics). Working tree propre.
### Prochaines etapes
- (Optionnel) Observer si le rappel vault est suivi en pratique. S'il est ignoré malgré le rappel → signal qu'il faut un cran plus fort (mais commencer par le moins intrusif, doctrine 22 mai).
- (Réactivation) Si une demande d'audit à fond repart en mono-agent et frustre → coller le trigger-rappel tripartite documenté.
- ⚠️ Hygiène : 232 fichiers memory/ (cible <100) → `/clean-memory` en session dédiée.

## Fils ouverts
- Audit skills en cours (l'agent qui avait déclenché cette session) — non repris ici, c'était le contexte déclencheur pas le travail.
- Trilogie docs stratégiques IA Neoteem : présentation Jérôme puis CODIR (commit `3a0f373`).
- Cadrage NeoMail (besoin/fonctionnalités/forme) = décision client, trame d'interview à préparer.
- Vérifier que le repo claude-forge est bien privé (docs CODIR confidentiels commités).

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
