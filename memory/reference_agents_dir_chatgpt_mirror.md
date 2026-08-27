---
name: agents-dir-chatgpt-adapters
description: .agents/ et AGENTS.md sont les surfaces Codex versionnées — adapter depuis une doctrine commune, jamais copier librement
trigger: AGENTS.md, .agents, chatgpt, codex, miroir, drift
metadata:
  type: reference
---

`.agents/skills/` et `AGENTS.md` à la racine de claude-forge sont les surfaces
versionnées destinées à ChatGPT/Codex.

**Décision supersédée (27 août 2026) :** la règle du 27 juillet « ne jamais y
toucher » a produit exactement le drift redouté : `cc-news` Codex était restée
au 2 juin, en mojibake, tandis que Claude avançait au 25 juillet. Raphaël a
explicitement autorisé la refonte Claude + Codex et demandé une mise à jour
réelle du vault.

**How to apply :** ne plus maintenir de copie libre. Une procédure partagée vit
dans `docs/second-brain/` ; les fichiers `.claude/skills/` et `.agents/skills/`
sont des adaptateurs minces propres à chaque plateforme. Une demande explicite
qui couvre Codex autorise leur modification. Auditer leur conformité au noyau,
pas leur identité byte-for-byte.
