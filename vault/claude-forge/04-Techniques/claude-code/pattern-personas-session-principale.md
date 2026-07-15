---
titre: "Pattern personas chargées en session principale (@rôle) — vs subagents vs Agent Teams"
resume: "Pattern communautaire validé : des rôles/personas en fichiers .md chargés dans la conversation PRINCIPALE (convention @dev/@docu portée par CLAUDE.md), à distinguer des subagents (isolés, non-interactifs — AskUserQuestion officiellement indisponible) et des Agent Teams (teammates interactifs, expérimental 2026). Grille de décision, piège namespace .claude/agents/, cas réel repo bdd."
aliases:
  - "personas session principale"
  - "pattern roles claude code"
  - "roles @dev @docu"
  - "persona vs subagent"
  - "roles session vs agents"
  - "quand creer un subagent"
type: technique
derniere-maj: 2026-07-15
auteur: claude
sources:
  - "https://code.claude.com/docs/en/sub-agents (officiel — liste des outils indisponibles en subagent, champs frontmatter, vérifié 15 juil. 2026)"
  - "https://claude.com/blog/subagents-in-claude-code (doctrine officielle : quand rester en session principale)"
  - "https://code.claude.com/docs/en/agent-teams (officiel — teammates)"
  - "https://github.com/jasonhanna/claude-personas"
  - "https://github.com/tommcfarlin/claude-code-persona-generator"
  - "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/roles/ai-roles.md"
  - "https://dev.to/lazydev_oh/same-claude-different-roles-my-5-agent-dev-team-3jlc"
  - "Cas réel : repo bdd Neoteem, chantier 13-15 juil. 2026 (branche us/RPI/PP-N2-111820-claude-skills, commit fa59af0)"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#doctrine/2026"
---
# Pattern personas chargées en session principale (@rôle)

## QUOI — Définition

Une **persona de session principale** est un fichier markdown d'instructions (méthode de travail, ton, expertise, format de sortie) chargé **dans la conversation principale** quand l'utilisateur tape `@<nom>` — pas un subagent. Le mécanisme n'est PAS natif : c'est une **convention portée par le CLAUDE.md** du repo (« quand une requête commence par `@dev`, lire `roles/dev.md` et appliquer strictement la méthode »), avec en option un **rôle par défaut** activé à chaque session.

## Les 3 étages du paysage 2026 — ne pas les confondre

| | Persona session principale | Subagent | Agent Teams (teammates) |
|---|---|---|---|
| Nature | Convention CLAUDE.md (fichier lu comme texte) | Feature native `.claude/agents/` | Feature native expérimentale (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`) |
| Contexte | **Partagé** avec la conversation | **Isolé** (retour = résumé) | Isolé mais **sessions communicantes** |
| Interaction utilisateur | ✅ totale (checkpoints, questions) | ❌ **`AskUserQuestion` officiellement indisponible** (verbatim doc : « depend on the main conversation's UI… aren't available to subagents, even when listed in the tools field » — idem `EnterPlanMode`, `ScheduleWakeup`) | ✅ partielle : l'utilisateur peut messager un teammate directement ; plan approval lead↔teammate |
| Frontmatter `model:`/`tools:` | ❌ ignoré | ✅ appliqué (name, description, tools, disallowedTools, model, permissionMode, skills, memory, effort, color) | ✅ (hérite du lead) |
| Cas d'usage | Posture de DIALOGUE : méthode avec allers-retours, validation humaine, ton persistant | Travail « noisy, bounded, easy to summarize » (verbatim officiel) : exploration, review, parallélisme | Coordination multi-couches où les workers doivent se parler (front+back+tests) |
| Exemples | bdd `@dev`/`@docu`/`@brainstorm`, claude-personas, « 5-Agent Dev Team » | forge repo-inspector/devils-advocate, neo_ia (12 agents), Explore/Plan natifs | reviews croisées, chantiers parallèles |

**Réponse à la question fréquente « mon repo X a des agents, mon repo Y n'en a pas — lequel est faux ? » : aucun.** Les agents de X sont des *workers d'isolation* (le bon usage subagent) ; les « rôles » de Y sont des *postures de dialogue* (le bon usage persona). Le seul FAUX état : des personas rangées dans `.claude/agents/` (voir piège n°1).

## QUAND — Grille de décision

- **Persona session principale** : le rôle pilote le DIALOGUE — checkpoints de validation humaine, questions à l'utilisateur, ton/méthode persistants sur la session. Verbatim doctrine officielle : rester en principal quand le travail est « small, tightly coupled, or depends on a shared mental model ».
- **Skill** : savoir/procédure réutilisable activable à la demande. Une persona qui n'a pas besoin de « rester active toute la session » est souvent mieux en skill user-invocable.
- **Subagent** : exploration massive, review indépendante, parallélisme — JAMAIS pour un rôle qui doit poser des questions (indisponibilité outillée, pas juste doctrinale).
- **Agent Teams** : quand les workers doivent se coordonner entre eux (expérimental ; depuis le 15 juin 2026, équipe implicite — teammates spawnés par le paramètre `name` de l'outil Agent, `TeamCreate` supprimé).

## Best practices (sources croisées + cas réel)

1. **JAMAIS ranger les personas dans `.claude/agents/`** — piège n°1 : tout `.md` de ce dossier est AUSSI enregistré comme subagent natif → la typeahead `@` peut spawner un subagent isolé (l'inverse du but) et l'interactivité y casse. Dossier inerte dédié : `.claude/roles/` ou `personas/`.
2. **Le routage vit dans CLAUDE.md** (3-5 lignes) : `@<nom>` → lire `roles/<nom>.md`, rôle par défaut éventuel, persistance (« reste actif toute la session, `@autre` remplace, `/clear` réinitialise sur le défaut »).
3. **Un rôle = un fichier**, structure type Role / Expertise / Critères / Voix (pattern persona-generator). Garder court — le contenu reste chargé toute la session.
4. **Rôle par défaut** = LE différenciateur vs skills : imposer la méthode maison à chaque session (ex. `@dev` auto-actif).
5. **Sortir de `agents/` fait perdre le frontmatter** (`model:`, `tools:` ne sont lus que pour les subagents) — noter avant migration si un rôle comptait sur `model: opus` implicite.
6. **Évolution naturelle** : persona interactive → reste rôle ; persona de pur savoir → skill ; la phase d'exploration d'un rôle → déléguée à un vrai subagent DEPUIS la session (l'architecte explore via Explore, le checkpoint de validation reste en principal).

## Cas réel — repo bdd Neoteem (13-15 juil. 2026)

`@dev` (méthode dev SQL, défaut de session) / `@docu` / `@brainstorm` vivaient dans `.claude/agents/` → bug de collision namespace (faux subagents, `AskUserQuestion` de docu cassé en spawn isolé). Fix : `git mv` vers `.claude/roles/` + section « Rôles de session » dans le CLAUDE.md orchestrateur (commit `fa59af0`). Les checkpoints humains de `/ticket` reposent sur ces rôles en session principale — la conversion en subagents les aurait cassés. Les VRAIS subagents du repo (architecte-sql read-only, verificateur/optimiseur parallèles) sont planifiés séparément (§9, après validation du /ticket converti).

## Gotchas

- Le pattern est **une convention, pas une feature** : sans la section de routage dans CLAUDE.md, les fichiers `roles/` sont morts. Compliance probabiliste (~80 %) comme tout CLAUDE.md.
- Ne pas dupliquer le contenu d'un rôle dans une skill « jumelle » — un besoin = un mécanisme (cf [[mcp-vs-skills-doctrine]]).
- La typeahead `@nom` native n'existe que pour les subagents — après migration vers `roles/`, `@dev` reste une convention textuelle interprétée (suffisant, mais l'autocomplétion disparaît).
- Vérifié 15 juil. 2026 sur la doc officielle ; l'indisponibilité d'`AskUserQuestion` en subagent est structurelle (UI de la session principale), peu susceptible de changer — mais Agent Teams comble progressivement ce trou par un autre chemin (teammates messagés directement).

## Wikilinks

- [[comment-creer-agent]] — quand c'est un vrai subagent qu'il faut
- [[comment-creer-skill]] — quand c'est du savoir réutilisable
- [[architecture-claude-folder]] — anatomie du dossier .claude/ et règles de chargement
- [[comment-ecrire-claudemd]] — le CLAUDE.md orchestrateur qui porte le routage
- [[methode-monter-systeme-workflow]] — grille besoin → brique
- [[anti-reentrance-sub-agents-pattern-escalade]] — escalade quand un subagent a besoin de l'utilisateur
