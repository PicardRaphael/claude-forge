---
titre: "Changelog vault forge-brain"
resume: "Historique des ajouts et modifications du vault forge-brain"
aliases:
  - changelog vault
  - historique vault
type: index
derniere-maj: 2026-05-08
auteur: claude
tags:
  - "#type/index"
---

## 2026-05-09 — MCP forge-brain + /watch + Context Note + devil's advocate

- **Ajoutées** :
  - `mcp-forge-brain/` — MCP server self-contained (SQLite FTS5, port 8091), copie autonome de mcp-obsidian-brain
  - `.mcp.json` — config MCP projet pour forge-brain
  - `0-Inbox/context-actuel.md` — Working memory dynamique (/done écrit, /recap lit)
  - Skill `/watch` — transcription YouTube via yt-dlp
- **Modifiées** :
  - Skill `/done` : fix cross-projet, routing 1-Projets/2-Casquettes, frontmatter nettoyé, garde anti-hallucination, Context Note en étape 6
  - Skills `forge-brain`, `recap` : structure vault + scan 1-Projets/2-Casquettes
  - Skill `vault-audit` + `audit.py` : nouveaux dossiers dans FOLDER_TO_MOC + TEMPLATE_SECTIONS
  - Rule `memory-discipline.md` : frontière memory↔vault canonique
  - CLAUDE.md : 2 lignes vault structure + standard qualité
  - Notes vault enrichies : ia_back, neo_ia, bdd, neoteem-brain (détails composants Claude Code)
  - Memory project_*.md : 4 fichiers slimmés (pointeurs vers vault 1-Projets/)
- **Devil's advocate** : critique `/done` sauvée dans `Knowledge/critiques/`, 3 bloquants corrigés
- **Source** : Analyse Eliott Meunier + recherche MCP servers + advisor

## 2026-05-09 — Structure holistique vault + skill /done + standard qualité

- **Ajoutées** :
  - `0-Inbox/` — dossier capture rapide
  - `1-Projets/Claude-Forge/Claude-Forge.md` — contexte projet forge
  - `1-Projets/Neoteem/Neoteem.md` — contexte projet Neoteem
  - `1-Projets/Neoteem/ia_back/ia_back.md` — contexte repo ia_back
  - `1-Projets/Neoteem/neo_ia/neo_ia.md` — contexte repo neo_ia
  - `1-Projets/Neoteem/neoteem-brain/neoteem-brain.md` — contexte repo neoteem-brain
  - `1-Projets/Neoteem/bdd/bdd.md` — contexte repo bdd
  - `1-Projets/Expertise-IA/Expertise-IA.md` — projet vision expert IA
  - `2-Casquettes/Raphael-Picard.md` — profil holistique complet
  - `2-Casquettes/Famille.md` — casquette famille
  - `2-Casquettes/Gaming.md` — casquette gaming
  - `Templates/context-projet.md` — template note de contexte projet
  - `Templates/context-casquette.md` — template note de contexte casquette
- **Modifiées** : Rule `forge-brain-proactive.md` — standard qualité (4-6 aliases, résumé, wikilinks) + routage dossiers 0/1/2
- **Skills** : `/done` créée — métacognition fin de session (extraction décisions/faits/préférences)
- **Source** : Analyse vidéo Eliott Meunier "Son système IA remplace une équipe entière" — ontologie par utilité, contexte holistique, /done auto-update

## 2026-05-08 — Erreur paths hardcodés multi-poste

- **Ajoutées** : `Knowledge/erreurs/erreur-settings-paths-hardcodes-multi-poste.md` — bug paths absolus user-spécifiques dans settings.json + hooks Python + marker files, cassent quand on pull sur un autre poste
- **Source** : premier usage de claude-forge sur poste perso (rapha) après pull depuis poste pro (raphael.picard_neote) — flot d'erreurs `Python was not found` + guard vault-query bloqué en permanence

## 2026-05-08 — Skill reasoning-cache + template raisonnement

- **Ajoutees** : `Templates/raisonnement.md` — template pour noter les chaines de raisonnement validees
- **Modifiees** : `00-Hub/MOC-Techniques.md` — section "Raisonnements caches" ajoutee avec lien vers Knowledge/raisonnements/
- **Source** : creation skill reasoning-cache (chain-of-thought caching au niveau tooling)

## 2026-05-08 — Base de connaissances Agents IA complète

- **Ajoutées** : `04-Techniques/agents/` — 6 notes (Agents IA MOC, frameworks, architecture, automation, évaluation, sécurité)
- **Leaders** : 6 fiches agents dans `05-Leaders/` (Shunyu Yao, Andrew Ng, Lilian Weng, Jim Fan, Simon Willison, Ethan Mollick)
- **Synthèse** : `techniques-inedites.md` — 8 combinaisons innovantes RAG × Agents jamais faites
- **cc-news** : section Agents IA & Automation leaders ajoutée (12 sources)
- **CLAUDE.md** : v1.9, mindset Jarvis/Innovateur ajouté
- **Source** : recherche via 5 agents parallèles (frameworks, architecture, leaders, automation, évaluation)

## 2026-05-08 — Base de connaissances RAG complète

- **Ajoutées** : `04-Techniques/rag/` — 7 notes (RAG MOC, chunking, embeddings, architecture, metadata, reranking, vector-databases)
- **Leaders** : 10 fiches RAG dans `05-Leaders/` (Jonas Roman, Omar Khattab, Douwe Kiela, Jerry Liu, Harrison Chase, Han Xiao, Chip Huyen, Greg Kamradt, Nils Reimers, James Briggs)
- **Synthèses** : `rag-obsidian-claude-video-analyse.md` (analyse critique vidéo YouTube), `outils-portabilite-forge.md` (defuddle, yt-dlp)
- **cc-news** : section RAG & Embeddings leaders ajoutée (9 sources)
- **Source** : recherche approfondie via 5 agents parallèles (chunking, embeddings, architecture, experts, metadata) + analyse vidéo YouTube RAG+Obsidian+Claude
