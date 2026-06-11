---
name: worktree-natif-vs-convention-develop
description: claude -w natif marche AVEC un flow develop-based SI la skill de pipeline gère la branche (fetch + switch us/ticket depuis origin/develop) — le worktree démarre sur origin/HEAD (=master) avec branche worktree-<nom>, peu importe. .worktreeinclude pour .env/certs/settings.local.json.
metadata:
  type: reference
---

**Setup validé et déployé (11 juin 2026, neoteem-back-ts commit a415bfe)** : sessions parallèles par US = `claude -w` natif + `/feature <ticket>` dans chaque terminal. RÉVISION de ma 1re conclusion (« worktree manuel requis ») : le natif suffit DÈS QUE la skill de pipeline crée elle-même la branche — peu importe que le worktree démarre sur `origin/HEAD` (=master) avec une branche `worktree-<nom>` hors convention, `/feature` fait `git fetch` + switch `us/N2-XXXX` depuis `origin/develop` et tout est d'équerre. `worktree.baseRef` reste limité à `fresh|head` (jamais un ref arbitraire — vérifié doc officielle).

**Les 4 briques à committer une fois par repo** : `.worktreeinclude` racine (`.env`, `certs/`, `.claude/settings.local.json` — sans le dernier les permissions.allow re-promptent ; mécanisme natif, s'applique à `-w`/subagents/desktop, JAMAIS aux worktrees manuels) · `.claude/worktrees/` dans `.gitignore` · skill pipeline worktree-aware (pnpm install si `node_modules` absent + branche depuis `origin/develop` après fetch + mort du worktree en fin de pipeline) · section README pour les humains.

**Garde gratuite** : git interdit de checkout une branche déjà checkout ailleurs → checkout principal sur `develop` = develop physiquement inaccessible aux sessions worktree. **Limites** : worktrees isolent les FICHIERS, jamais la BDD partagée ni les ports — ne paralléliser que des US déclarées parallélisables (packages/tables disjoints). **Cleanup** : prompt natif à la sortie de session ; rattrapage `git worktree list` + `git worktree remove`.

**Source canonique** : doc officielle code.claude.com/docs/en/worktrees (fetchée 11 juin) — jamais howborisusesclaudecode.com (compilation de tweets non officielle, rappel Raphael). Cf [[feedback_git_C_pas_cd]].
