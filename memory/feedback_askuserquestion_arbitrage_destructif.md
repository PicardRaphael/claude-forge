---
name: askuserquestion-arbitrage-destructif
description: "Actions destructives (>3 plugins desinstall, refonte rules, scope changes) = AskUserQuestion structure par item, jamais en bloc"
metadata:
  type: feedback
---

Pour toute serie d'actions destructives (desinstallation plugins, suppression skills/agents, scope changes settings.json, refonte structures), presenter chaque decision via AskUserQuestion structure avec 2-4 options par question, plutot qu'un bloc unique "tu valides ?". L'arbitrage par item permet a Raphael de corriger les recommandations par defaut sur la base d'info contextuelle non visible (usage Cowork remote, role admin/read-only, scope cross-repo).

**Why** : 28 mai 2026 Step 6 audit plugins — 4 AskUserQuestion successives ont produit 3 corrections importantes sur les recommandations initiales (feedback-triage = Cowork only, obsidian = scope forge+neoteem-brain, dev-ia = admin a lui seul). Chaque correction modifie une action destructive. En "valide tout" en bloc, ces corrections auraient ete perdues. Lien doctrine : [[comment-creer-skill]] (skill propose, humain valide par item).

**How to apply** : seuil = >3 actions destructives independantes. Questions multi-options (pas binaires) + label "(Recommande)" sur la 1ere option. Toujours offrir "Statu quo" et "Plus radical" pour cadrer le spectre. Si user repond "[v]alide tout en bloc", l'accepter (preference contextuelle).
