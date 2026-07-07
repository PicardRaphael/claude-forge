---
titre: "Worktrees & sessions parallèles — setup validé"
resume: "Pattern complet pour paralléliser des US avec `claude -w` natif + skill pipeline branche-aware : 4 briques, garde hook path-based, limites."
aliases:
  - worktrees sessions parallèles
  - claude -w natif
  - sessions parallèles US
  - worktree pipeline feature
  - worktreeinclude
  - sessions parallèles claude code
derniere-maj: 2026-07-07
tags:
  - claude-code
  - worktrees
  - sessions-parallèles
  - git
type: technique
---

## Principe

`claude -w` natif suffit pour des sessions parallèles par US **DÈS QUE** la skill pipeline crée elle-même la branche. Pas besoin de worktree manuel. Peu importe que le worktree démarre sur `origin/HEAD` (=master) avec une branche `worktree-<nom>` hors convention — `/feature` fait `git fetch` + switch `us/N2-XXXX` depuis `origin/develop` et tout est d'équerre.

> Validé et déployé 11 juin 2026 : neoteem-back-ts (a415bfe) + neo_ia (0e0a696).

`worktree.baseRef` est limité à `fresh|head` — jamais un ref arbitraire (vérifié doc officielle code.claude.com/docs/en/worktrees).

## Les 4 briques (à committer une fois par repo)

| Brique | Contenu | Rôle |
|--------|---------|------|
| `.worktreeinclude` (racine) | `.env`, `certs/`, `.claude/settings.local.json` | Sans le dernier, `permissions.allow` re-promptent. Mécanisme natif : s'applique à `-w`/subagents/desktop — **JAMAIS** aux worktrees manuels. |
| `.claude/worktrees/` dans `.gitignore` | Entrée gitignore | Évite de committer les worktrees |
| Skill pipeline worktree-aware | `pnpm install` si `node_modules` absent + branche depuis `origin/develop` après fetch + mort du worktree en fin de pipeline | Le cerveau du système |
| Section README | Instructions humaines | Onboarding équipe |

## 5e brique critique — hooks path-based

Tout hook qui matche `.claude/` sur le chemin **absolu** (config-guard, delegate-guard…) **bloque toutes les écritures sub-agent dans un worktree** — le chemin contient `.claude/worktrees/<slug>/`.

**Fix obligatoire** : strip du préfixe worktree avant match :
```python
# Pattern regex à appliquer dans chaque hook path-based
import re
path = re.sub(r'^(.*/)?\.claude/worktrees/[^/]+/', '', path)
# La protection du .claude/ du worktree survit au strip
```

Vécu : back-ts (premier `/feature` en worktree US4) + porté neo_ia. **À vérifier dans tout repo recevant le système** (ia_back : non porté au 11 juin 2026).

## Garde gratuite & limites

**Garde gratuite** : git interdit de checkout une branche déjà checkoutée ailleurs → checkout principal sur `develop` = develop physiquement inaccessible aux sessions worktree.

**Limites** :
- Worktrees isolent les **fichiers**, jamais la BDD partagée ni les ports
- Ne paralléliser que des US déclarées parallélisables (packages/tables disjoints)

**Cleanup** : prompt natif à la sortie de session. Rattrapage : `git worktree list` + `git worktree remove`.

## Source canonique

Doc officielle : code.claude.com/docs/en/worktrees — **jamais** howborisusesclaudecode.com (compilation tweets non officielle).

## Liens

- [[workflow-claude-code-optimal]]
- [[comment-creer-hook]]
- [[comment-creer-skill]]
- [[anti-reentrance-sub-agents-pattern-escalade]]
