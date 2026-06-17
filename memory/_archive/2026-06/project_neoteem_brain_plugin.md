---
name: neoteem-brain-plugin
description: Plugins Neoteem CC. SOURCE DE VÉRITÉ = 2 marketplaces Bitbucket (4 juin 2026) — neoteem-plugin-claude (support+brain, large) et neoteem-plugin-claude-admin (po+brain-admin, restreint). Doctrines brain admin-first / Jira acli-ou-MCP / N2 format PO / MCP non bundlé.
type: project
originSessionId: d55234b8-f33e-4de6-acb1-6bda9799e651
---
## Plugins neoteem-brain v2.0.0

Split du plugin monolithique en 3 plugins standalone le 2026-04-21. Marketplace locale pointant vers `neoteem-brain/plugin/`.

**Structure :**
```
plugin/
├── .claude-plugin/marketplace.json (3 plugins)
├── neoteem-brain-support/ (equipe support — CLI + MCP adaptive)
├── neoteem-brain-dev/ (devs — CLI direct, vault complet)
└── neoteem-brain-dev-ia/ (devs IA — CLI + cross-ref 4 repos)
```

**Install equipe :** `mcp-obsidian-brain\install.bat` — 3 profils (support/dev/dev-ia).
- Support : installe MCP + configure `claude_desktop_config.json` (lance auto par Cowork)
- Dev : installe Obsidian + repos Bitbucket + plugin dev
- Dev IA : idem + plugin dev-ia

**Scope :** user (global machine)
**Repos connectes :** neo_ia (dev + dev-ia), ia_back (dev + dev-ia), neoteem-brain (dev local)

**Why:** Le plugin monolithique forcait a installer 3 skills quand on en voulait 1. Novices ne savaient pas quoi utiliser. Le split par role + install.bat guide permet un onboarding autonome.

**How to apply:**
- Modifier le plugin → bumper version dans plugin.json correspondant
- Bug cache connu : toujours bumper version pour forcer refresh
- Support = MCP tools (lecture seule) + CLI si dispo. Devs = CLI direct
- Ancien plugin `neoteem-brain@neoteem` desinstalle, cache purge

## Marketplaces Bitbucket Neoteem (4 juin 2026) — SOURCE DE VÉRITÉ

**2 marketplaces Bitbucket = la source unique** (décision Raphael 4 juin, remplace output/lojii qui devient jetable) :

| Repo Bitbucket | marketplace `name` | Accès | Plugins |
|---|---|---|---|
| `neot-v2/neoteem-plugin-claude` | `neoteem` | large (droits repo) | `neoteem-support`, `neoteem-brain` (lecture seule) |
| `neot-v2/neoteem-plugin-claude-admin` | `neoteem-admin` | restreint PO/admin (droits repo) | `neoteem-po`, `neoteem-brain-admin` (écriture) |

Chemins locaux : `C:\Users\...\Documents\neot-v2\neoteem-plugin-claude(-admin)`. **C'est ICI qu'on travaille désormais** (plus dans output/lojii). Install à la carte CLI : `/plugin marketplace add <url bitbucket>` puis `/plugin install <x>@neoteem|neoteem-admin`. Desktop = upload `.zip` du contenu d'un dossier plugin.

**Structure réelle des dossiers (4 juin 2026, commits 3c2eb1b + 70fdb45) — plugins thématiques 2 skills, PAS mini-plugins :** dossiers courts dans chaque repo, noms de plugins INCHANGÉS (invocation `/neoteem-support:triage-tickets` etc.). Équipe : `support/` (plugin `neoteem-support` = triage-tickets + analyse-qualification-tickets) + `neo-brain/` (plugin `neoteem-brain` = neo-brain + neo-brain-support). Admin : `po/` (plugin `neoteem-po` = spec + review-ticket) + `neo-brain/` (plugin `neoteem-brain-admin` = neo-brain-dev-admin + neo-brain-support-admin) + `neo-brain-dev-ia/` (plugin `neoteem-brain-dev-ia` **SOLO**, 1 skill, sélectionnable seul — réservé aux 2 devs stack IA Raph+Jeje, doctrine MCP-only appliquée). 2 skills d'un container = obligatoires ensemble (décision Raphael : on n'éclate PAS en mini-plugins). `build-skills-zip.ps1` génère `dist/chat/<skill>.zip` (compétences Desktop) + `dist/plugin/<dossier>.zip` (plugins entiers), nommés d'après les dossiers (`support.zip`, `po.zip`, `neo-brain.zip`, `neo-brain-dev-ia.zip`).

**Contrôle d'accès admin** : pas de mot de passe par plugin (n'existe pas dans CC — feature request #9756 fermée sans solution). Le « mot de passe » = les droits git sur le repo restreint. Orga Cowork (préférences Required/Default/Available/Not available + groupes) serait le vrai contrôle mais exige github.com privé → bloqué chez Neoteem (cf [[org-blocks-github]]) → on reste Bitbucket + 2 repos.

**MCP obsidian-brain NON bundlé** (décision 4 juin) : pas de `.mcp.json` dans les plugins. Le MCP se branche au niveau environnement (Connector Desktop/orga `https://mcp-brain.neoteem.fr/mcp`, ou `claude mcp add` global CLI). Fallback CLI Obsidian **supprimé** des skills (tout le monde a le MCP).

**⚠️ Gotcha collision nom serveur MCP (4 juin)** : les 5 skills brain ont `allowed-tools: mcp__obsidian-brain__*` — **figé sur le nom `obsidian-brain`**. Or le même vault (`mcp-brain.neoteem.fr/mcp`) peut être branché sous 2 noms différents : (a) CLI `claude mcp add obsidian-brain ...` → serveur `obsidian-brain`, (b) Connector orga claude.ai → serveur `NeoBrain` (ou autre nom). Quand les deux pointent la même URL, CC en **masque un** (`/mcp` affiche `◯ hidden — same URL as your server 'obsidian-brain'`) — anti-doublon, pas un bug. **Conséquence distribution** : si un collègue branche le vault sous un nom ≠ `obsidian-brain`, les `allowed-tools` des skills ne préapprouvent pas ses tools (ils restent appelables mais avec prompt de permission — `allowed-tools` = préapprobation, pas restriction, cf [[feedback_allowed_tools_pas_allowlist]]). **Convention à imposer en INSTALL : brancher le MCP vault sous le nom `obsidian-brain`** (CLI ou connector renommé) pour que le matching fonctionne. Garder `obsidian-brain` actif, ne pas le `claude mcp remove` au profit du connector orga.

**Vérif fraîcheur zip avant distribution** : valider le CONTENU des zip, pas leur nom. Version embarquée via Python (`zipfile` lit les chemins backslash Windows que `unzip -p` rate sur glob `*/...`), SKILL.md à la racine des compétences (`SKILL.md` sans backslash), grep des résidus doctrine dans les `.md` zippés. Les 9 compétences + 5 plugins vérifiés en 1.0.1 propres (4 juin).

**Ménage fait (4 juin)** : `output/lojii/` supprimé (migré dans les 2 repos). `neot-v2/neoteem-brain/plugin/` supprimé du repo neoteem-brain via `git rm -r` + commit (PAS encore pushé — repo vault+MCP, push à valider par Raphael). Les 5 anciens plugins (support/support-admin/dev/dev-admin/**dev-ia**) sauvegardés dans `claude-forge/output/neoteem-brain-plugin-ancien/` (« pour Jeje et Raph », dev-ia notamment sans équivalent dans les marketplaces). Restent à trier dans `output/` : `po-lojii`, `support-lojii-plugin`, `support-lojii-plugin-v3`, `po`, `neoteem` (anciennes sources, suppression item par item à valider).

**plugin.json displayName+description seuls visibles UI ; README non affiché ; CLAUDE.md de plugin ignoré ; cache CLI interdit les `../` (aucun cross-plugin).**

## Audit qualité des 9 skills + bump 1.0.1 (4 juin 2026)

Audit complet 1-par-1 des 9 SKILL.md croisé avec canoniques forge ([[comment-creer-skill]] + [[mcp-vs-skills-doctrine]]). **Verdict : skills solides et conformes** (doctrine Karpathy, anti-invention, format N2=PO, dual-engine, admin-first, Gotchas riches). Aucun P0. Écarts corrigés :
- **Résidus doctrine CLI Obsidian** (P1, 4 occurrences) : `triage-tickets` "Fonctionne en CLI et MCP", + réf morte "et les equivalents CLI" dans `neo-brain`/`neo-brain-dev-admin`/`neo-brain-support-admin` (les `vault-access.md` étaient déjà nettoyés → SKILL.md mentait). Nettoyés.
- **Port local obsolète** (P2, 3 occurrences) : "port 8090 en local" → MCP distant `https://mcp-brain.neoteem.fr/mcp` branché environnement, dans `neo-brain`/`neo-brain-support`/`neo-brain-dev-ia`.
- **Descriptions** : ajout formule directive `DO NOT ... without invoking first` sur `analyse-qualification-tickets` (226 ch) + `triage-tickets` (218 ch), ≤250.

Frontmatter homogène : tous `effort: high` + `memory: project` + `user-invocable: true`. **Model** : `spec`/`review-ticket`/`analyse-qualification-tickets`/`triage-tickets` = **opus** (jugement) ; les 5 skills brain = **sonnet** (accès vault = exécution). Toutes < 500L (`neo-brain-support-admin` 493L = limite, non déportée car skill brain dupliquée). **Duplication assumée** : ~150L doctrine Karpathy/pagination répétées entre les 5 skills brain (cross-plugin interdit par cache CLI → répétition obligée, pas un défaut).

**Versions = 1.0.1** (bump 4 juin, commits `05fa09f` équipe + `5a5a498` admin). Bumper la version est le SEUL déclencheur de refresh : ceux déjà branchés (ex. Jérôme) reçoivent la maj via `/plugin marketplace update <name>`. **Règle : tout changement de contenu d'un plugin → bumper sa `version` dans plugin.json, sinon les utilisateurs branchés gardent l'ancienne (bug cache CLI connu).**

**Doctrine brain « admin d'abord, read-only en repli » (universelle PO ET support, 4 juin) :** chaque skill métier invoque `neo-brain-*-admin` ; si la variante admin absente de la session, bascule sur la read-only équivalente (`neo-brain` / `neo-brain-support`). PO a toujours admin (capitalise). Support : brain read-only suffit, admin seulement pour capitaliser en /analyse. ⚠️ N'ouvre PAS l'écriture batch/Phase C de triage (contrainte run planifié, indépendante). Skill ne peut pas introspecter l'installé → instruction textuelle résolue au runtime, jamais un mécanisme de détection inventé.

**Doctrine Jira PO « acli OU MCP » (dual-engine, 4 juin) :** spec/review-ticket détectent acli (`acli --version`) ; si absent → MCP de plein droit (`mcp__claude_ai_Atlassian_2__createJiraIssue/editJiraIssue` CRUD + MCP Jira Neoteem pour PJ/notes internes). PAS « moteur + fallback dégradé ». Support = MCP-only (zéro acli, vérifié). MCP Atlassian ne fait pas d'upload PJ natif → copy_attachments.

**N2 support = format PO (4 juin) :** la description d'un N2 créé par le support (analyse-qualification-tickets §8.2) suit le squelette des vrais N2 PO (`references/template-n2.md` : Problématique → Description → Comportement attendu/observé* → Règles de gestion → Écrans impactés → Étapes repro* → Points d'attention tests* → Impact ; *=BUG/BLOQUANT only, pas Intervention BDD). Plus de « copie intégrale » brute. Cf [[feedback_plugin_admin_absorbe_readonly]], [[feedback_askuserquestion_arbitrage_destructif]].
