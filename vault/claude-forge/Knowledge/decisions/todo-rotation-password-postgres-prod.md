---
titre: "TODO P0 — Rotation du mot de passe PostgreSQL prod Neoteem"
resume: "Le mot de passe PostgreSQL prod + IP serveur GCP ont été committés en clair dans 3 notes vault claude-forge (poussées sur GitHub origin) ET dans l'historique git ia_back (Bitbucket). Redacté de HEAD le 2026-05-27, mais présent dans l'historique git des deux repos. Le seul fix réel = rotation du mot de passe côté serveur."
aliases:
  - "rotation password postgres"
  - "rotation mdp prod neoteem"
  - "secret postgres compromis"
  - "todo rotation secret"
  - "fix secret postgres prod"
  - "password leak postgres rotation"
type: decision
statut: a-faire
priorite: P0
derniere-maj: 2026-05-27
auteur: claude
tags:
  - "#type/todo"
  - "#domaine/securite"
  - "#projet/neoteem"
  - "#priorite/P0"
---

# TODO P0 — Rotation du mot de passe PostgreSQL prod

> Statut : À FAIRE — P0. Découvert pendant l'audit confidentialité de la session Mémoire Portable (2026-05-27).

## Le problème

Le mot de passe PostgreSQL de production Neoteem (utilisateur `postgres`, superuser) et l'IP publique du serveur GCP ont été committés **en clair** :

- **Repo claude-forge** (remote GitHub `github.com:PicardRaphael/claude-forge.git`) — dans 3 notes vault :
  - `Knowledge/critiques/critique-2026-05-22-audit-neo_ia.md`
  - `Knowledge/critiques/critique-session-2026-05-20-running-notes-decompose-xread-mcp.md`
  - `Knowledge/erreurs/erreur-password-postgres-clair-mcp-json.md`
- **Repo ia_back** (Bitbucket) — `.mcp.json` dans l'historique git (chez Jérôme + clones équipe).

Redacté de **HEAD** le 2026-05-27 (`[REDACTED]`), mais le secret reste **dans l'historique git des deux repos**.

## Pourquoi le redact ne suffit pas

`[REDACTED]` sur HEAD évite la propagation future, mais quiconque a accès à l'historique git (GitHub, Bitbucket, clones existants) peut récupérer le secret. La purge d'historique (`git filter-repo`/BFG) :
- Ne ferme pas la fuite Bitbucket ia_back (clones équipe déjà faits).
- Requiert un force-push coordonné, casse les clones existants, hors scope.

**Le seul fix réel = rotation du mot de passe côté serveur PostgreSQL.** Tant que le mot de passe n'est pas changé, le secret reste valide quel que soit le nettoyage git.

## Actions

1. **Rotation du mot de passe** de l'utilisateur `postgres` sur l'instance PostgreSQL prod (IP redactée des notes, conservée hors vault).
2. Mettre à jour les connection strings consommatrices (`.mcp.json` ia_back/neo_ia via `${VAR_ENV}` + `.env` gitignored — déjà la doctrine, cf [[erreur-password-postgres-clair-mcp-json]]).
3. (Optionnel, post-rotation) Restreindre l'accès réseau de l'IP publique (firewall GCP / Cloud SQL authorized networks).
4. Vérifier que `NODE_TLS_REJECT_UNAUTHORIZED=0` n'est plus utilisé (TLS off observé dans le `.mcp.json` original).

## Appels

- [[erreur-password-postgres-clair-mcp-json]] — l'erreur d'origine
- [[decision-memoire-dans-le-repo]] — la session qui a re-découvert le secret en HEAD
- [[secret-management-never-commit-credentials]] — feedback mémoire (la règle violée)
