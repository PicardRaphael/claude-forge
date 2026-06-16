---
name: ccnews-structure-vault-provider-drift
description: La skill cc-news encode l'ancienne ontologie vault (02-Concurrents/ + 03-Modeles/) ; le SCHEMA a basculé en dossiers provider le 14 juin. Vérifier le SCHEMA réel AVANT de capitaliser, pas se fier au routage de la skill.
metadata:
  type: feedback
---

Run cc-news du 16 juin 2026 : Raphael a prévenu « la structure du vault a été mise à jour ». Vérifié via `vault_stats` + `SCHEMA` : réorg du **14 juin** — un dossier par acteur IA premier niveau (`01-Claude`, `02-OpenAI`, `03-Google`, `08-xAI`, `09-Anysphere`, `10-Microsoft`…) contenant `models/` + `products/`, créés à la demande. **Dissolution de `02-Concurrents/` et `03-Modeles/`** ; pas de dossier « Concurrents » (les fournisseurs sont des acteurs suivis). Comparatifs cross-fournisseurs → thématique (`04-Techniques/` ou MOC `00-Hub/`).

**Le drift** : la skill `cc-news` (SKILL.md section « Capitalisation vault » + routage) pointe encore vers `02-Concurrents/<produit>/` et `03-Modeles/<provider>/<nom>.md`. Un run qui suit la skill aveuglément écrira au mauvais endroit.

**Why** : la skill est une référence figée ; le vault évolue (SCHEMA `derniere-maj` fait foi). Drift skill↔vault = capitalisation mal classée, future dette de rangement.

**How to apply** :
1. Au moment de capitaliser (étape 8 cc-news), lire `SCHEMA` via MCP forge-brain et suivre sa table d'ontologie, PAS la section capitalisation de la skill si elle diverge.
2. Modèle fondation → `<NN>-<Provider>/models/` · produit/CLI/IDE → `<NN>-<Provider>/products/` · comparatif → `04-Techniques/` ou MOC.
3. **Corriger la skill cc-news** (via `skill-creator`) quand validé par Raphael : aligner routage + section capitalisation sur la réorg provider. Tant que non fait, ce feedback est le garde-fou.

Cf [[methode-analyser-repo]] (vérifier le RÉEL avant de prescrire) + `.claude/rules/sequence-canonique-modification.md` (A. analyser le réel). Vault SCHEMA section « Convention fournisseur (14 juin 2026) ».
