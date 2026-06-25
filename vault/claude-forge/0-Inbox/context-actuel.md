---
titre: Context Actuel
resume: Working memory dynamique -- mis a jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, memoire de travail, etat actuel]
type: context
status: active
derniere-maj: 2026-06-25
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---

## Phase actuelle
Audit + durcissement config Claude Code des repos d'équipe (migration_script terminé).

## Dernière session (2026-06-25)
### Décisions prises
- **migration_script `.claude/` = CONFORME** (audit profond 31 objets, 4 grilles dont portabilité dominante). Repo assaini depuis l'incident du 24 juin : zéro wikilink vault, zéro MCP forge-brain, zéro chemin machine, zéro `exit 2`.
- **Fix É1 appliqué + poussé** (commit `50b88378`, branche `raphael_claude_setup`, PR Bitbucket #1514) : table de routage dédupliquée → CLAUDE.md = source unique (lu en premier par un dev), `dispatch-skills.md` réduit à un stub pointeur, README:62 ajusté. Sens de fix inversé par le DA (découvrabilité humaine > réflexe forge « rule = canonique »).
- **É2 (descriptions > 250 chars) laissé tel quel** : gain tokens marginal, risque auto-activation.
- **Isolation stricte forge ↔ migration_script** : aucune liaison, intervention uniquement sur demande explicite de Raphael.

### En cours
Rien — chantier migration_script clos.

### Prochaines étapes
- Si Raphael ouvre la PR #1514 → merge vers Master (décision humaine, repo d'équipe).
- Appliquer la même grille d'audit repo-d'équipe aux autres repos partagés si demandé.

## Fils ouverts
- **Récidive Edit direct CLAUDE.md** (2/3 vers seuil [[feedback-reviole-3x-regle-insuffisante]]) : à la 3e occurrence, envisager un réflexe pré-Edit structurel plutôt qu'une note. Enrichi dans `memory/feedback_ecrire_partout_invoquer_skill_creatrice.md`.
- `vera/gen_tags_patch.py:193` : chemin machine en dur (`C:/Data/ctrl/controls.sql`) — dans le CODE de migration_script, hors scope `.claude/`. Signalé, non traité.

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
