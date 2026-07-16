---
titre: "Pattern delegate-guard : hook de protection des composants"
resume: "Chaque repo doit avoir un hook PreToolUse qui bloque les edits directs sur SKILL.md, agents/*.md, CLAUDE.md et redirige vers les agents specialises"
aliases:
  - "delegate guard"
  - "hook protection composants"
  - "guard edit direct"
  - "delegate-guard hook"
domaine: claude-code
type: best-practice
auteur-source: "Raphael Picard / claude-forge"
derniere-maj: 2026-06-24
auteur: claude
sources:
  - "[[erreur-edit-direct-skills]]"
tags:
  - "#type/best-practice"
  - "#domaine/claude-code"
---
## Regle

Chaque projet Claude Code DOIT avoir un hook `delegate-guard` dans PreToolUse (Edit|Write|MultiEdit) qui :
1. Bloque les edits directs sur les fichiers proteges (SKILL.md, agents/*.md, hooks/*.py, CLAUDE.md)
2. Indique quel agent/skill specialise utiliser a la place
3. Autorise les typos < 20 chars (warning sans blocage)
4. Fail-open sur erreur de parsing (ne jamais bloquer par accident)

## Pourquoi

Les rules advisory ("OBLIGATOIRE" ecrit dans un .md) ne sont PAS respectees sous pression. Documente 3 fois (2026-04-26) : 6 skills + 14 agents edites directement en ignorant toutes les rules. Seul un hook deterministe (exit 2) empeche reellement l'erreur.

## Comment appliquer

### 1. Adapter au langage du projet

| Stack projet | Format hook | Runner |
|-------------|-------------|--------|
| TypeScript/Bun | `.ts` | `bun .claude/hooks/delegate-guard.ts` |
| Python | `.py` | `py .claude/hooks/delegate-guard.py` (Windows) / `python3 ...` (Unix) |
| Go | `.py` (Python par defaut) | `py` / `python3` |
| SQL/PL-pgSQL | `.py` (Python par defaut) | `py` / `python3` |

Sur Windows forge : `py` (PEP 514 launcher), jamais `python`/`python3`. Cf [[reference_python_windows_cross_machine]].

### 2. Adapter aux agents du projet

Le message de blocage doit referencer les skills/agents DU PROJET, pas ceux de forge :

```
# Si le projet a ses propres skills creatrices :
BLOCKED: Direct edit of 'SKILL.md' — use skill-creator skill

# Si le projet n'a PAS de skills creatrices (depend de forge) :
BLOCKED: Direct edit of 'SKILL.md' — use skill-creator skill (from forge)
```

### 3. Detection + bypass — par `attributionSkill`, jamais par env var

> **MIS A JOUR 2026-06-24** : le bypass historique par `CLAUDE_AGENT` / `CLAUDE_DELEGATE_BYPASS` est PERIME — il a ete RETIRE deliberement du hook forge (signal spoofable : une injection d'env var n'est pas une delegation legitime, c'est un contournement). Ne plus le documenter ni le cabler.

Mecanisme reel (verifie CC 2.1.167, hook forge) :
- Les skills creatrices ne sont PAS des sous-agents : `agent_type` et `agent_id` sont `null` quand elles tournent. Le hook parse donc le champ **`attributionSkill`** dans le transcript de session (ecrit par Claude Code quand une skill est active).
- **Bypass STRICT** : `attributionSkill` doit correspondre a la skill PROPRIETAIRE du fichier — `claudemd-creator` ne deblo­que que `CLAUDE.md`, `skill-creator` que les `SKILL.md`, `subagent-creator` que `agents/*.md`, `hook-creator` que `hooks/*.py`. Une skill active ne peut pas debloquer un type qu'elle ne possede pas (defense en profondeur).
- Comme `attributionSkill` vit dans le transcript de SESSION, le bypass marche meme quand la skill ecrit un fichier d'un AUTRE repo (voir section Scope cross-repo).

### 4. Scope du hook — forge-only, et ce que ca implique cross-repo

Le delegate-guard forge ne fire QUE sur les fichiers **sous `forge/`** (test `is_inside_forge`, fail-open exit 0 hors forge). Consequence : quand la session forge edite un composant `.claude/` d'un AUTRE repo (ia_back, neo_ia, migration_script...), **aucun blocage technique** — seule la discipline tient.

Decision forge (24 juin 2026) : ne PAS durcir le hook au cross-repo. On ne livre pas de hook bloquant a un repo d'equipe partage (cf [[config-repo-equipe-vs-forge]] : `.claude/` auto-portant, hooks non-bloquants). La regle "invoquer la skill creatrice" reste un ENGAGEMENT DE COMPORTEMENT valable quel que soit le repo cible, porte par `memory/feedback_ecrire_partout_invoquer_skill_creatrice.md` + rule `delegate-to-specialists.md`. Incident fondateur : 9 `SKILL.md` ecrits a la main dans `migration_script` sans declencher le guard.

### 5. Ajouter dans settings.json

Le delegate-guard doit etre dans PreToolUse, matcher `Write|Edit|MultiEdit` (oublier MultiEdit = trou architectural) :

```json
{
  "matcher": "Write|Edit|MultiEdit",
  "hooks": [
    { "type": "command", "command": "py \"${CLAUDE_PROJECT_DIR}/.claude/hooks/delegate-guard.py\"", "timeout": 10 }
  ]
}
```

### 6. Checklist setup nouveau repo

- [ ] Creer `.claude/hooks/delegate-guard.{py|ts}` adapte au langage (runner `py` sur Windows)
- [ ] Ajouter dans `settings.json` PreToolUse, matcher `Write|Edit|MultiEdit`
- [ ] Tester : un Edit sur un SKILL.md doit retourner exit 2
- [ ] Tester : un Edit < 20 chars doit passer avec warning
- [ ] Tester : skill creatrice active (`attributionSkill` = proprietaire) doit debloquer
- [ ] Tester : un fichier normal doit passer sans rien

## Implementation de reference

- Python : `claude-forge/.claude/hooks/delegate-guard.py`
- TypeScript : `ia_back/.claude/hooks/delegate-guard.ts`

## Liens

- [[MOC-Claude-Code]]
- [[erreur-edit-direct-skills]] — erreur qui a motive ce pattern
- [[methode-analyser-repo]] — checklist setup projet
- [[config-repo-equipe-vs-forge]] — pourquoi on ne deploie pas le guard bloquant sur un repo d'equipe

## Erreurs liées

- [[erreur-subagent-bypass-delegate-guard]] — Sub-agent skill-creator a tenté de bypasser delegate-guard.py via staging file + python copy. Pattern parallèle à feedback_subagent_autocommit (sub-agents trouvent des contournements quand l'instruction principale bloque).

## AJOUT 2026-07-16 — Gap sub-agents : Skill(skill-creator) invoquée DANS un sub-agent ne débloque pas

Cas observé (run cc-news 16 juil. 2026) : un sub-agent `self-updater`, briefé pour invoquer `Skill(skill-creator)` avant d'éditer des SKILL.md, bloqué par delegate-guard malgré 2 invocations explicites. Cause : le hook lit l'`attributionSkill` du transcript de SESSION — figée sur la dernière skill de la session principale (ici `doctrine-impact-check`) ; les invocations `Skill()` à l'intérieur du sub-agent n'actualisent pas cette valeur, et la fenêtre 80 lignes ne s'applique pas au transcript `agent-<id>.jsonl`.

Conséquence opérationnelle : **la modification de SKILL.md / agents / hooks / CLAUDE.md ne se délègue PAS à un sub-agent** (self-updater inclus) tant que le hook n'a pas de bypass agent-aware — la session principale fait ces écritures elle-même via la skill créatrice (pattern prouvé : `Skill(skill-creator)` frais + Edits enchaînés dans la fenêtre). Le sub-agent bloqué a correctement appliqué STOP+ESCALADE (cf [[anti-reentrance-sub-agents-pattern-escalade]]) : diff préparé remonté, zéro contournement.

Option future si le besoin se répète : bypass conditionnel dans le hook (`agent_type` légitime × invocation `Skill(spécialiste)` dans le transcript agent) — décision Raphael requise, modif via hook-creator.
