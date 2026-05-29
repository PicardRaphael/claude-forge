---
name: spec-must-stop-at-specs-no-dev
description: "/spec doit STOP après génération des fichiers TODO/feature-X/ — jamais développer, jamais appeler /go, jamais toucher au code applicatif ni à d'autres repos"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8957d13-cb6a-43d0-ae69-71bb7fa375a2
---

La skill `/spec` doit s'arrêter ABSOLUMENT à la génération des fichiers de spec dans `TODO/feature-<nom>/`. JAMAIS de :
- Développement de code applicatif
- Appel automatique à `/go`
- Modification de fichiers hors `TODO/`
- Modification d'un autre repo (cross-repo INTERDIT en write)

**Why:** Session 2026-05-20 incident chez Jérôme : `/spec` ia_back a directement commencé à développer du code au lieu de générer les SPECs, et en plus a touché neo_ia depuis ia_back (cross-repo non autorisé). Cause racine identifiée : instruction "ne touche pas au code" était dans les gotchas en fin de fichier (ligne 179), sous-pondérée par l'agent vs le `/spec` neo_ia qui a la même consigne en gras ligne 18 juste après le titre — d'où marche sur neo_ia mais pas ia_back.

**How to apply:**
- Toute skill de type `/spec` doit avoir l'instruction STOP en gras dans les 20 premières lignes
- Pipeline obligatoire : Phase 1-4 → AskUserQuestion bloquant "STOP / Ajuster / OK pour /go" → fin de skill
- JAMAIS de transition automatique de `/spec` vers implémentation, même si user dit "vas-y" — toujours valider via AskUserQuestion explicite
- Cross-repo : seulement Read/Glob/Grep autorisés sur autres repos, JAMAIS Write/Edit. Le BRIEF généré doit être copié manuellement par l'user dans le repo cible.
- Si Claude est tenté d'enchainer /spec → /go → dev-agent en autonome : STOP, c'est un anti-pattern documenté
- Voir [[critique-session-2026-05-20-running-notes-decompose-xread-mcp]] et la skill `/spec` neo_ia comme référence du bon pattern
