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
