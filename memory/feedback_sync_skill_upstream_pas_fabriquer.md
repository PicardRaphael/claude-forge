---
name: sync-skill-upstream-pas-fabriquer
description: "Asset manquant (references/) dans une skill installée depuis un marketplace = WebFetch/sync verbatim depuis upstream, JAMAIS fabriquer du contenu local."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f598fcbc-1e1f-4161-bd42-75eddf13fbdf
---

Quand une skill installée depuis un marketplace (ex: kepano/obsidian-skills) référence un asset (`references/EXAMPLES.md`) absent de notre copie, l'asset a été perdu lors de la copie/installation — il existe upstream.

**Why:** Fabriquer le contenu localement crée un fork silencieux : si upstream publie le sien plus tard, conflit ; si on a inventé du contenu pour combler un dangling ref, on le maintient à vie. Le 27 mai, j'allais fabriquer EXAMPLES.md pour json-canvas — l'advisor a stoppé. Vérification : l'upstream `kepano/obsidian-skills` AVAIT bien `skills/json-canvas/references/EXAMPLES.md` (6476 octets). Récupéré verbatim.

**How to apply:** Asset manquant dans skill marketplace → (1) vérifier l'arbre upstream via `api.github.com/repos/<owner>/<repo>/git/trees/main?recursive=1`, (2) si l'asset existe upstream → télécharger verbatim (`Invoke-WebRequest` raw.githubusercontent, vérifier bytes serveur == bytes fichier), (3) si dangling chez eux aussi → retirer la référence locale, pas fabriquer. Diff minimal > authoring. Note : WebFetch paraphrase (petit modèle) — pour du verbatim, utiliser Invoke-WebRequest/curl. Cf [[obsidian-skills-sacred]].
