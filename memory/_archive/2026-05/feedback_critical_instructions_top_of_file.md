---
name: critical-instructions-top-of-file-not-gotchas
description: "Toute instruction critique (STOP, interdit, contrat sécurité) DOIT être placée en haut de fichier (ligne <25, en gras/callout), JAMAIS en gotcha de fin de fichier"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8957d13-cb6a-43d0-ae69-71bb7fa375a2
---

Pour les SKILL.md, AGENTS.md, CLAUDE.md : toute instruction critique (STOP CRITIQUE, interdits explicites, contrat sécurité) DOIT être placée dans les 25 premières lignes du body, idéalement en blockquote/gras juste après le titre. JAMAIS en gotcha de fin de fichier.

**Why:** Session 2026-05-20 — bug observé chez Jérôme : `/spec` ia_back développait directement du code et touchait neo_ia depuis ia_back. Root cause = instruction "Ne lance pas /go, ne touche pas au code" placée en gotcha ligne 179 (fin de fichier). Comparaison empirique : `/spec` neo_ia avec la même consigne en gras ligne 18 (juste après titre) → marchait pour Raphael. Différence de position = différence de comportement modèle. Confirmé par `forge-prompt-machine` vault (primacy/recency effect : Claude donne plus de poids aux instructions au début et à la fin du prompt).

Fix appliqué : nouvelle skill `/spec` unifiée déployée avec STOP CRITIQUE en blockquote ligne 18 + gate AskUserQuestion bloquant fin Phase 4. Pattern à généraliser sur toutes futures skills.

**How to apply:**
- Création skill/agent : checklist obligatoire "Instruction critique présente lignes 1-25 ? En gras ou callout blockquote ?"
- Review skill existante : grep "STOP\|JAMAIS\|interdit" et vérifier position. Si en gotcha → remonter en tête de body
- Audit DA : check structurel "Position des règles critiques dans le top 20% du fichier"
- Ne pas confondre "Gotchas" (rappels secondaires) avec "STOP CRITIQUE" (règles non-négociables) — pas la même catégorie
- Pour `/spec`, `/decompose-ticket`, `/go`, `/notes` et toute skill qui modifie/génère des fichiers : règle absolue
- Lien vault : [[critique-fusion-spec-decompose-ticket-en-cours]] (si créée par DA) et [[forge-prompt-machine]]
