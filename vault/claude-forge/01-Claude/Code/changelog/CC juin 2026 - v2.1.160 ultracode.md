---
titre: "CC juin 2026 — v2.1.155→2.1.160 (workflow→ultracode)"
resume: "Drop CC post-Opus 4.8 : le mot-déclencheur des Dynamic Workflows passe de 'workflow' à 'ultracode' (2.1.160), Claude in Chrome via /chrome (2.1.157), Auto Mode Bedrock/Vertex/Foundry (2.1.158), durcissements sécu écriture fichiers shell/git config"
aliases:
  - "CC v2.1.160"
  - "ultracode workflow keyword"
  - "Claude in Chrome /chrome"
  - "CC changelog juin 2026"
  - "workflow trigger renamed ultracode"
type: changelog
domaine: claude-code
derniere-maj: 2026-06-02
auteur: claude
sources:
  - "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md"
  - "https://www.anthropic.com/news"
tags:
  - "#type/changelog"
  - "#domaine/claude-code"
  - "#domaine/anthropic"
---

## Contexte

Drop CC postérieur au changelog vault du 28 mai (v2.1.154 Opus 4.8 + Dynamic Workflows). Versions 2.1.155 → 2.1.160. **Source primaire vérifiée** (raw GitHub CHANGELOG + anthropic.com/news) — les claims d'aggregateurs non confirmés (crédits programmatiques 15 juin, /powerup, PermissionDenied hook) sont écartés (cf [[erreur-4-fabrications-vault-prompt-engineering-2026-05-23]] pattern hallucination chiffrée aggregateurs).

## v2.1.160 — le changement qui impacte forge

- **`workflow` → `ultracode`** : le mot-déclencheur des Dynamic Workflows est renommé. Dire « workflow » dans un prompt ne déclenche plus un dynamic workflow ; c'est désormais `ultracode`. ⚠️ Impacte tout setup forge qui s'appuyait sur le mot « workflow » comme déclencheur.
- Prompt de confirmation **avant écriture** dans les fichiers de démarrage shell et `~/.config/git/` (durcissement sécu).
- Mode `acceptEdits` demande confirmation avant d'écrire un fichier de config de build exécutable.
- Fix copier-sélection sur **WSL/Windows** (PowerShell interop au lieu d'OSC 52) — pertinent machine forge.
- Corrections : sessions background, `agents list`, Windows, IME, voice mode.

## v2.1.158 — Auto Mode cloud providers

- **Auto Mode sur Bedrock, Vertex et Foundry** pour Opus 4.7 et 4.8. Opt-in via `CLAUDE_CODE_ENABLE_AUTO_MODE=1`.

## v2.1.157 — Plugins + Chrome

- Plugins dans `.claude/skills` **chargés automatiquement**.
- `claude plugin init <name>` pour scaffolder un plugin.
- **Claude in Chrome** : sélection du navigateur connecté via `/chrome` → « Select browser… ».
- `EnterWorktree` peut basculer entre worktrees en cours de session.

## v2.1.156

- Correction des erreurs API liées aux blocs thinking sur Opus 4.8.

## Confirmé source primaire anthropic.com/news (industrie)

- **1er juin 2026** : Anthropic dépose confidentiellement son S-1 auprès de la SEC (process IPO).
- **28 mai 2026** : Series H 65 Md$ à 965 Md$ post-money (déjà tracé) + Opus 4.8.

## Écarté (non confirmé en source primaire)

- ❌ Système de crédits programmatiques 15 juin (20$/100$/200$ par tier) — absent du changelog ET de anthropic.com/news. Claim aggregateur (blog.mean.ceo, InfoWorld) non vérifiable. À surveiller, pas à capitaliser.
- ❌ `/powerup`, hook `PermissionDenied`, `CLAUDE_CODE_NO_FLICKER` dans cette plage — absents du changelog réel 2.1.154→160.

## Liens

- [[CC 28 mai 2026 - Opus 4.8 + Dynamic Workflows]] — drop précédent
- [[Code with Claude 2026]] — keynote, higher order prompts
- [[MOC-Claude-Code]]
