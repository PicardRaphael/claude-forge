---
name: secret-management-never-commit-credentials
description: "NE JAMAIS committer credentials (password DB, API keys, tokens) en clair dans .mcp.json ou tout fichier versionné, même si le pattern existe déjà chez d'autres collaborateurs"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8957d13-cb6a-43d0-ae69-71bb7fa375a2
---

NE JAMAIS committer de credentials en clair dans `.mcp.json`, `.env`, configs, ou tout fichier versionné — même si le pattern existe déjà chez d'autres collaborateurs.

> NOTE : ce feedback a été rétroactivement nettoyé le 2026-05-27 lors de l'audit Mémoire Portable. Le secret réel (mot de passe PostgreSQL prod + IP serveur) a été retiré et remplacé par `[REDACTED]`. La leçon ci-dessous reste valide et illustre précisément pourquoi cette règle existe.

**Why:** Session 2026-05-20 — j'allais propager un anti-pattern hérité du setup de Jérôme : password PostgreSQL `[REDACTED]` en clair dans `ia_back/.mcp.json` poussé sur Bitbucket. L'auto-mode classifier Claude a bloqué le push avec un message explicite "credential leakage even if the repo is trusted". Pattern hérité ≠ pattern correct.

**How to apply:**
1. Avant de modifier ou créer un fichier `.mcp.json`, `.env`, `config.json`, `settings.json` ou tout fichier versionné : scanner les valeurs pour détecter mots-clés sensibles (password, secret, token, key, connection-string, api_key)
2. Si trouvé : utiliser variable d'env `${VAR_NAME}` + `.env` gitignored + `.env.example` documenté
3. Si auto-mode classifier bloque un push avec mention "credential" : c'est un signal vrai, ne pas bypasser, présenter à l'utilisateur les options (refactor / push partiel / discussion équipe)
4. Si pattern hérité contient des credentials, le signaler explicitement à l'utilisateur AVANT de le propager — proposer un refactor sécu
5. Référence vault : [[erreur-password-postgres-clair-mcp-json]] et [[mcp-paths-relatifs-portabilite]]

Lien : [[auto-mode-classifier]] — l'outil qui m'a sauvé. Toujours respecter ses blocages credential-related.
