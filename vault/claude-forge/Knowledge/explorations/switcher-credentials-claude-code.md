---
titre: "Switcher de credentials Claude Code — mécanisme qui dure, et pourquoi NeoBoard a cassé"
resume: "Un switcher de comptes Claude Code doit COPIER le credential et laisser Claude Code rafraîchir lui-même (re-capture du token frais à chaque switch) — jamais tenter un refresh OAuth maison, qui dépend d'un client_id réservé au CLI et qu'Anthropic a invalidé en février 2026."
aliases:
  - "switcher credential claude code"
  - "claude switcher neoboard"
  - "switch compte claude code sans login"
  - "credential json claude refresh token"
  - "pourquoi claude code demande login switcher"
  - "client_id oauth claude code"
domaine: "04-Techniques/claude-code"
derniere-maj: 2026-06-22
tags:
  - claude-code
  - oauth
  - outillage
  - neoteem
---

# Switcher de credentials Claude Code — mécanisme qui dure, et pourquoi NeoBoard a cassé

## Le besoin

Basculer entre plusieurs comptes/licences Claude Code (team) sans refaire `/login` à chaque fois,
en copiant le bon `credentials.json` à la place de l'actif. NeoBoard faisait ça et un credential
durait 3-4 mois. Puis ça a cassé (juin 2026) : `/login` demandé / `401 Invalid authentication credentials`.

## Anatomie d'un credential Claude Code

`~/.claude/.credentials.json` — clés racine : `claudeAiOauth` (le compte) + `mcpOAuth` (connexions MCP perso).
`claudeAiOauth` contient : `accessToken` (`sk-ant-oat01-…`, ~1 jour), `refreshToken` (`sk-ant-ort01-…`, longue durée),
`expiresAt` (ms epoch, = expiration de l'**accessToken**, PAS du refreshToken), `scopes`, `subscriptionType`, `rateLimitTier`.

## Le mécanisme qui DURE (NeoBoard 30 mars 2026, commit f4912f7)

Le switch d'origine était une **simple copie** (`writeCredentials`), zéro refresh, zéro client_id :

1. **Switch = COPIE** du credential choisi dans `~/.claude/` (en préservant `mcpOAuth` perso).
2. **Claude Code rafraîchit le token LUI-MÊME** au fil de l'usage — c'est SON client_id officiel
   (`9d1c250a-e61b-44d9-88ed-5944d1962f5e`), le seul qu'Anthropic accepte.
3. **Re-capture** : avant chaque switch, resauvegarder le credential actif (que CC vient de rafraîchir)
   dans le dossier du compte → il reste perpétuellement frais.

Tant qu'un compte est utilisé régulièrement, il ne meurt jamais. D'où les 3-4 mois.

## Pourquoi NeoBoard a cassé (commit af22c3c, 3 avril 2026)

Ajout de `switchAccountWithRefresh` : quand le token est expiré, NeoBoard tente un **refresh OAuth maison**
avec SON client_id codé en dur `22422756-60c9-4084-8eb7-27705fd5cf9a`. Deux coups fatals en juin 2026 :

- **Durcissement OAuth Anthropic (février 2026)** : l'auth OAuth est réservée à Claude Code/claude.ai.
  Le client_id de NeoBoard renvoie désormais `Client with id … not found`.
- **Auto-update de Claude Code** (2.1.183→2.1.185 le 21 juin) qui a fini d'aligner le comportement.

Résultat : le refresh maison échoue ET, sur certains chemins, **vide le refreshToken** du compte dans la base.
Tant que l'accessToken n'était pas expiré au moment du switch, le bug restait invisible (pure copie) —
d'où « ça marchait hier ». Dès qu'un token expire, le refresh casse.

## Vérités contre-intuitives (vérifiées empiriquement, juin 2026)

- **`expiresAt` = accessToken, pas refreshToken.** Un fichier « expiré en avril » peut avoir un refreshToken
  encore vivant. La date seule ne dit RIEN sur la récupérabilité.
- **refreshToken présent ≠ vivant.** Anthropic peut l'avoir révoqué côté serveur. Le seul test fiable :
  switcher dessus + lancer Claude Code. S'il démarre → vivant ; `/login` / 401 → révoqué (fichier frais requis).
- **Refresh OAuth manuel (curl) depuis la machine = rate-limité en permanence**, même avec le bon client_id
  et les headers CC (`anthropic-version`, `anthropic-beta: oauth-2025-04-20`). N'essaie pas de rafraîchir à la main :
  c'est le job de Claude Code. (Le rate-limit a tenu >16h sur ~10 essais.)
- **Un fichier « frais » d'un collègue = `expiresAt` dans le FUTUR.** Piège vécu : un collègue renvoie un ancien
  fichier (expiré) en croyant avoir fait `/login` → inutilisable. Toujours vérifier la date avant de switcher.

## Pièges d'implémentation d'un switcher maison

- **Re-capture destructrice** : si on resauvegarde le credential actif sans garde, un token vidé par un 401
  (CC l'efface avant de demander /login) écrase la bonne sauvegarde. **Garde obligatoire : ne re-capturer
  QUE si `refreshToken` non vide.**
- **Identité de l'actif par fichier `.active`, jamais par token** : le token tourne quand CC le rafraîchit,
  donc le matcher par accessToken rate l'actif → re-capture no-op. Persister le nom du compte actif.
- **Préserver `mcpOAuth`** : remplacer uniquement `claudeAiOauth` dans la cible, sinon on perd les connexions MCP.

## Implémentation forge (Neoteem)

`Documents/credential-claude/` — comptes en `<nom>/credentials.json`, actif dans `.active`.
- `switch.mjs` (+ `Switch Credential.bat`) : menu terminal.
- `switch-web.mjs` (+ `Switch Web.bat`) : front web local (port 3849), UI dark, quotas 5h/7j
  (lecture headers `unified-5h-utilization`/`unified-7d-utilization` via petit appel API, caché 45s), clic = switch.

Les deux : copie + re-capture gardée, zéro refresh maison. Front inspiré de l'ancien
`claude-forge/output/claude-switcher/` (lui-même extrait de NeoBoard `electron/services/accounts.js`).

## Sources

NeoBoard `electron/services/accounts.js` (commits f4912f7 / af22c3c), doc Anthropic
[Authentication - Claude Code](https://code.claude.com/docs/en/authentication), politique OAuth février 2026.
