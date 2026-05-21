---
titre: Architect neo_ia fouille le repo bdd sans autorisation
aliases:
  - architect neo_ia bdd
  - architect cross-repo bdd
  - erreur scope architect neo_ia
  - architect sortie scope repo
  - repo-scope-guard origine
  - bdd interdit neo_ia
resume: L'architect agent de neo_ia est allé fouiller dans le repo bdd voisin alors que sa source de vérité externe doit être ia_back uniquement, le contexte BDD passant par le MCP neo-brain-dev-ia
derniere-maj: 2026-05-21
tags:
  - "#type/erreur"
  - "#erreur/agent"
  - "#erreur/scope"
  - "#domaine/claude-code"
  - "#projet/neo_ia"
---

# Architect neo_ia fouille le repo bdd sans autorisation

## Ce qui s'est passé

Pendant une session sur neo_ia, l'architect agent a commencé à explorer le repo `bdd/` voisin (PostgreSQL/PL-pgSQL) pour collecter du contexte sur des fonctions PG. Raphael a remarqué : neo_ia ne doit JAMAIS aller dans bdd directement, sa source de vérité métier passe par le MCP `neo-brain-dev-ia` (read-only sur le vault neoteem-brain).

## Pourquoi c'était une erreur

1. **Mauvaise source de vérité** : pour le contexte BDD/métier, le canal canonique = vault neoteem-brain (documenté, à jour, structuré). Aller dans `bdd/` brut = code SQL/PL-pgSQL difficile à interpréter sans contexte métier.
2. **Pas de garde-fou** : architect avait `Read, Glob, Grep, Bash` sans aucune contrainte de scope dans son frontmatter ni dans CLAUDE.md. Rien ne lui disait "tu restes dans neo_ia / ia_back".
3. **Pattern récurrent potentiel** : les autres agents (dev-lead, code-reviewer, etc.) ont le même profil → même risque.

## La solution déployée (2026-05-21)

Triple couverture (pattern [[enforce-not-advise]]) :

### 1. Rule `repo-scope.md`
`neo_ia/.claude/rules/repo-scope.md` — frontière déclarée. neo_ia + ia_back = libres ; tous les autres repos voisins = bloqués par défaut. Autorisation par phrase naturelle dans le prompt ("autorisé bdd", "regarde bdd", "check bdd", "accès bdd").

### 2. Patch top-of-file de `architect.md`
Section `## ⛔ SCOPE REPO — RÈGLE ABSOLUE` insérée ligne 22 (avant ligne 25, voir [[critical-instructions-top-of-file]]) — rappel explicite que bdd est interdit, contexte BDD = MCP neo-brain-dev-ia.

### 3. Trois hooks Python
- `auth-detector.py` (UserPromptSubmit) — regex sur le prompt, pose marker `.claude/.repo-auth-<repo>` (whitelist dynamique = dossiers réels de neot-v2/)
- `repo-scope-guard.py` (PreToolUse sur Read|Grep|Glob|Bash|Write|Edit|MultiEdit) — résout path absolu via `pathlib.Path.resolve()`, bloque exit 2 si repo hors scope ET marker absent
- `auth-cleanup.py` (SessionStart) — supprime tous les markers au démarrage (PAS de TTL, [[marker-ttl-antipattern]])

## Pattern réutilisable

Cette solution est composée à partir de trois patterns vault existants :
- [[delegate-guard-pattern]] — PreToolUse exit 2 + marker (déployé 3× dans forge avant)
- [[prompt-rewriter-pattern]] — UserPromptSubmit qui détecte un signal dans le prompt
- [[pattern-architect-first-pipeline]] — marker sans TTL, reset SessionStart

**Combinaison inédite** : path-based scope enforcement avec auth par phrase naturelle. À répliquer si un autre repo a besoin du même cloisonnement (typiquement quand un repo en agente plusieurs voisins).

## Tests empiriques (validation)

8/8 PASS testés en conditions réelles le 2026-05-21 :
- Read bdd → exit 2 ✅
- Read ia_back → exit 0 ✅
- Read neo_ia → exit 0 ✅
- Bash `cat ../bdd/foo.sql` → exit 2 (path résolu via token containing `/`) ✅
- "autorise bdd" dans prompt → marker posé, additionalContext injecté ✅
- Read bdd après auth → exit 0 ✅
- auth-cleanup → markers supprimés ✅
- Read bdd après cleanup → exit 2 (retour à l'état bloqué) ✅

## Liens

- [[delegate-guard-pattern]]
- [[prompt-rewriter-pattern]]
- [[pattern-architect-first-pipeline]]
- [[marker-ttl-antipattern]]
- [[critical-instructions-top-of-file]]
- [[enforce-not-advise]]
- [[erreur-advisory-rules-insuffisantes]]
- [[neo_ia]]

## Méta — leçon Jarvis

L'erreur n'était pas dans l'architect (il a fait son job, il a cherché du contexte). L'erreur était dans la **config de l'agent** : on lui a donné Read+Grep+Bash sans définir où il a le droit de regarder. Quand un agent fait quelque chose qu'on ne veut pas, le bon réflexe = chercher quel garde-fou manque, pas blâmer l'agent.

Devil's advocate a aussi soulevé pendant cette même session que le hook `vault-before-specialist.py` de claude-forge a un TTL 60min qui viole [[marker-ttl-antipattern]] — dette notée pour session dédiée.
