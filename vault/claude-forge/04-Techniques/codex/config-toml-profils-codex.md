---
titre: "config.toml et profils Codex — réglages machine, couches, requirements.toml"
resume: "Note canonique forge — config.toml de Codex : emplacements (user/projet/système), champs clés (sandbox_mode, model, effort, approval, MCP, hooks), RUPTURE profils 0.134.0 (un fichier par profil, legacy = crash boot), précédence des couches, requirements.toml admin non-overridable. Vérifié doc officielle au 15 juil. 2026, modèle par défaut réactualisé le 5 sept. 2026."
aliases:
  - "config.toml codex"
  - "profils codex"
  - "codex profile fichier"
  - "requirements.toml codex"
  - "sandbox_mode approval_policy"
  - "precedence config codex"
  - "managed config codex"
derniere-maj: 2026-09-05
auteur: claude
type: technique
sources:
  - "https://learn.chatgpt.com/docs/config-file/config-basic · /config-advanced · /config-reference"
  - "https://learn.chatgpt.com/docs/enterprise/managed-configuration"
  - "https://learn.chatgpt.com/docs/changelog (modèle par défaut, vérifié 5 sept. 2026)"
  - "https://github.com/openai/codex/issues/24858 (crash profils legacy 0.134.0)"
tags:
  - "#type/technique"
  - "#domaine/codex"
  - "#doctrine/2026"
---
# config.toml et profils Codex

> Note canonique forge — `config.toml` porte les **réglages machine/projet** de Codex (modèle, sandbox, approbation, MCP, hooks). Distinct de [[agents-md-codex]] (conventions repo) et de [[comment-creer-skill-codex]] (how-to). Vérifié au **15 juil. 2026** ; le modèle par défaut a été réactualisé au **5 sept. 2026**.

---

## COMMENT — Emplacements et couches

Trois emplacements + une couche managée :

| Fichier | Portée | Note |
|---------|--------|------|
| `~/.codex/config.toml` | user (global) | base |
| `.codex/config.toml` | projet (racine repo) | chargé **seulement si projet « trusted »** |
| `/etc/codex/config.toml` | système (Unix) | *probable* (une source) |
| `requirements.toml` / managed | admin | **écrase tout, même les CLI flags** |

Projet non-trusted → Codex « skips project-scoped `.codex/` layers, including project-local config, hooks, and rules ». Depuis la CLI **0.150.0 (26 août 2026)**, cela s'étend explicitement aux instructions : *« Untrusted projects no longer supply project-level `AGENTS.md` instructions »* — cf [[agents-md-codex]]. `CODEX_HOME` déplace `~/.codex/` (*à vérifier* — évoqué, pas défini verbatim). Redémarrer Codex après édition de `~/.codex/config.toml`.

### Précédence (du plus fort au plus faible)

```
requirements.toml / MDM / managed_config.toml   (managé, gagne toujours)
  > CLI flags / --config key=value
  > projet .codex/config.toml (dossier le plus proche)
  > fichiers profil (~/.codex/<profil>.config.toml)
  > user ~/.codex/config.toml
  > système /etc/codex/config.toml
  > défauts intégrés
```

*Nuance majeure* : les couches managées surchargent **même les `--config`**. Verbatim : « CLI `--config key=value` overrides apply to the base, but managed layers override them. »

---

## COMMENT — Champs clés (CERTAIN)

```toml
model = "gpt-6-astra"                   # défaut de bundle depuis la CLI 0.153.4 (4 sept. 2026)
model_reasoning_effort = "high"         # minimal|low|medium|high|xhigh (Responses API only, xhigh model-dependent)
approval_policy = "on-request"          # untrusted|on-request|never
sandbox_mode = "workspace-write"        # read-only|workspace-write|danger-full-access
```

- **`model`** : sans configuration explicite, Codex applique son **défaut de bundle**, qui est `gpt-6-astra` depuis la **0.153.4 (4 sept. 2026)** — verbatim : *« made it the bundled default when no model is explicitly configured »*. Le défaut précédent, du 9 juil. au 3 sept., était `gpt-5.6-sol`. Renseigner ce champ transforme le défaut subi en choix délibéré : c'est le réflexe recommandé sur un CLI qui a changé de modèle par défaut deux fois en deux mois. ⚠️ L'accès à Astra dépend du déploiement et de la méthode de connexion — sur un compte non éligible, le modèle réellement servi peut différer.
- **`model_reasoning_effort`** : cinq valeurs, `minimal | low | medium | high | xhigh`. `ultra`, `max` et `none` **ne sont pas valides** (cf [[subagents-cloud-codex]] § Effort). Aucun défaut n'est déclaré dans la référence.
- **`approval_policy`** : `untrusted | on-request | never`. **`on-failure` est DÉPRÉCIÉ** (n'utiliser que `on-request` interactif / `never` non-interactif). Forme granulaire :
```toml
approval_policy = { granular = { sandbox_approval = true, rules = true, mcp_elicitations = true, request_permissions = false, skill_approval = false } }
```
- **`sandbox_mode`** : réseau coupé par défaut (`network_access = false`), racines writables via `[sandbox_workspace_write]`. Détail sandbox : voir [[subagents-cloud-codex]] et la doctrine sécu ci-dessous.
- **MCP** : `[mcp_servers.<id>]` avec `command`/`args`/`env` (stdio) ou `url`/`bearer_token_env_var` (Streamable HTTP).
- **Hooks** : `[[hooks.<Event>]]` — cf [[comment-creer-hook-codex]].
- **Outil de planning** : `tools.update_plan.enabled = true` — **désactivé par défaut** depuis la 0.152.0 (1er sept. 2026). À activer explicitement pour les tâches longues.

---

## COMMENT — Profils : RUPTURE en 0.134.0 (CERTAIN, triple source)

> ⚠️ **Depuis Codex 0.134.0 (26 mai 2026), le mécanisme de profils a changé.** Les blocs `[profiles.<nom>]` dans `config.toml` et le sélecteur top-level `profile = "<nom>"` **ne sont plus supportés**. Un `config.toml` legacy avec `profile = "..."` **empêche Codex de démarrer** (crash au boot, pas un warning — issue GitHub #24858).

**Nouveau modèle** : un profil = **un fichier dédié** `~/.codex/<nom>.config.toml`, à clés top-level (overlay des valeurs qui diffèrent de la base), activé par `--profile`.

```toml
# ~/.codex/deep-review.config.toml
model = "gpt-6-astra"
model_reasoning_effort = "xhigh"
approval_policy = "on-request"
```
```bash
codex --profile deep-review
codex exec --profile deep-review "review this change"
```

- Noms de profil : lettres/chiffres/tirets/underscores.
- `profile`/`profiles` sont dans la liste des clés **ignorées en config projet** → la sélection de profil est **user-level uniquement**.

---

## COMMENT — requirements.toml (admin/enterprise, CERTAIN)

`requirements.toml` = config **admin-enforced non-overridable** par l'utilisateur. Contraint les réglages sensibles : approval policy, reviewer, auto-review, sandbox mode, permission profiles, web search mode, **managed hooks**, quels MCP servers l'user peut activer.

- Conflit config user vs requirement → « local client falls back to a compatible value and notifies the user ».
- Emplacements (précédence croissante) : `/etc/codex/requirements.toml` (ou `%ProgramData%\OpenAI\Codex\` Windows) → cloud bundle → legacy `managed_config.toml` → macOS MDM.
- Exemple :
```toml
allowed_approval_policies = ["untrusted", "on-request"]
allowed_sandbox_modes = ["read-only", "workspace-write"]
```
- **Frontière prouvée** : `allow_managed_hooks_only = true` n'est supporté **que** dans `requirements.toml` (ignoré s'il est mis dans `config.toml`). Depuis 0.138.0, préférer `allowed_permission_profiles`.

---

## Doctrine sandboxing (OpenAI)

Sandboxing OS-natif (*probable* — DeepWiki repo + investigations Willison, pas doc primaire OpenAI) : macOS Seatbelt (`sandbox-exec -p`), Linux Landlock + seccomp (`codex-linux-sandbox` binaire séparé), Windows tokens/ACLs restreints. Réseau off par défaut (`CODEX_SANDBOX_NETWORK_DISABLED`). Debug : `codex debug seatbelt` / `codex debug landlock`. La doctrine « sandboxing agressif assumé » attribuée à Fouad Matin / Sottiaux dans les fiches leaders **n'a pas été confirmée verbatim en source primaire** — traiter comme angle éditorial, pas citation.

---

## ANTI-PATTERNS

- ❌ **`[profiles.NAME]` dans config.toml** — périmé depuis 0.134.0, empêche le démarrage (crash boot).
- ❌ **`profile = "..."` top-level** — même crash. Migrer vers `~/.codex/<nom>.config.toml` + `--profile`.
- ❌ **`on-failure`** en approval_policy — déprécié.
- ❌ **Laisser `model` non renseigné en croyant connaître le défaut** — il a changé deux fois en deux mois. L'écrire explicitement coûte une ligne.
- ❌ **Mettre `allow_managed_hooks_only` dans config.toml** — sans effet, requirements.toml only.
- ❌ **Attendre qu'un profil projet fonctionne** — `profile`/`profiles` ignorés en config projet (user-level only).
- ❌ **Credentials en clair dans config.toml versionné** — utiliser `env_vars` / `bearer_token_env_var`.

---

## SOURCES

- `learn.chatgpt.com/docs/config-file/{config-basic,config-advanced,config-reference}` (15/07/2026, valeurs d'effort recroisées le 05/09/2026).
- `learn.chatgpt.com/docs/changelog` — modèle par défaut, outil de planning, projets non-trusted (05/09/2026).
- `learn.chatgpt.com/docs/enterprise/managed-configuration`.
- `github.com/openai/codex/issues/24858` — issue officielle : crash profils legacy post-0.134.0.
- Sandboxing OS-natif : DeepWiki `openai/codex` + `simonwillison.net/2025/Nov/9/codex-sandbox-investigation/` (*secondaire*).

---

## WIKILINKS

- [[workflow-codex-optimal]] — note maître
- [[agents-md-codex]] — conventions repo (frère)
- [[comment-creer-hook-codex]] — hooks configurés dans config.toml
- [[subagents-cloud-codex]] — sandbox par agent, MCP par agent
- [[GPT-6 Astra]] — défaut de bundle depuis la 0.153.4
- [[mcp-vs-skills-doctrine]] — doctrine MCP commune
