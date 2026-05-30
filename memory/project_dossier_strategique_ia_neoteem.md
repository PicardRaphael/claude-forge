---
name: dossier-strategique-ia-neoteem
description: Trilogie docs IA Neoteem (Stratégique + Roadmap + Modèle éco) pour CODIR, charte graphique réutilisable, à finaliser
metadata:
  type: project
---

Raphael (Lead/Responsable IA Neoteem, débutant dans le rôle, assumé devant la direction) prépare une **trilogie de documents IA** pour la direction, dans `output/neoteem/` (= espace Neoteem dédié) :

1. **Neoteem_Dossier_Strategique_IA_v2.pdf** — le *pourquoi* (diagnostic, benchmark concurrents, options A/B + séquence « B finance A », équipe Raphael+Jérôme valorisée SANS chiffrage salarial).
2. **Neoteem_Roadmap_IA_v2.pdf** — le *quoi/quand* (catalogue idées Équipe+Claude, roadmap réalisable 2 colonnes « à 2 » / « renforcé », coût caché, roadmap vivante). NeoChat parqué. **Ne PAS y mettre de contenu mettant Raphael personnellement en avant** (consigne 29 mai).
3. **Neoteem_Modele_Economique_IA.pdf** — le *combien* (4 modèles : usage/forfait/crédits/inclus, fourchettes à valider, revenus clients only).

**Charte graphique** : `output/neoteem/_charte/neoteem-charte.css` + `CHARTE.md`. Identité réelle (logo.webp) : bleu #0a3a5c, teal #00a78e, dégradé teal→corail→magenta. PDF via Chrome headless `--headless=new --no-pdf-header-footer --print-to-pdf` (PAS `--print-to-pdf-no-header`, ignoré sur Chrome 148). Poppler installé (scoop) pour vérifier le rendu : `pdftoppm -png`. **Gotcha pages blanches résolu** : footers/headers retirés du flux (causaient pages orphelines) ; tables sans `break-inside:avoid` (se coupent entre lignes, thead répété) ; seul h1 garde `break-after:avoid`.

**Avis franc donné (29 mai)** — 5 trous niveau « grand Responsable IA » : (1) aucun chiffre de valeur CLIENT réel ; (2) zéro gouvernance données/RGPD ; (3) vélocité concurrence non datée ; (4) pas de KPI succès+condition pivot ; (5) le « moat » murmuré au lieu d'être le cœur du pitch.

**MOAT — formulation validée par Raphael (29 mai), distinction clé** : le vrai moat = **la BASE DE DONNÉES Loji** (données réelles clients : immeubles, lots, copropriétaires, OS/interventions, comptes, baux, impayés, SEPA). Les **682 notes métier = accélérateur INTERNE** (n'va pas aux clients, aide à construire), PAS le moat. Argument CODIR le plus fort : « L'IA est une commodité — Bellman/Genius/Gemini ont le même Claude/GPT. Ce qui ne se copie pas = la base de données Loji. L'IA sans données = générique. » Confirmé marché (Coprolab : connexion couche IA = critère survie 2026).

**En cours d'ajout (29 mai)** : sections KPI succès + IA responsable/données + moat. Chiffres sourcés web (syndic pro 15-25€/lot/mois, 180-300€/lot/an, IdF +30-50% ; Genius n'affiche pas ses prix ; insight Coprolab : « connexion à une couche d'automatisation IA = critère de survie 2026 » → valide le moat). Crédit à donner : l'agent Support fait DÉJÀ du VERBATIM anti-hallucination + LLM-as-Judge (approche eval existante).

**Tranché (30 mai) — choix stratégique BINAIRE A ou B** : le « B finance A » est MORT (démonté par Raphael : risque de cannibalisation, les clients ont déjà ChatGPT/MCP moins cher). Le dossier pose désormais un **choix net A ou B** (verdict §16, lean B recommandé honnêtement), avec 3 dangers écrits noir sur blanc : (1) clients ont ChatGPT → un agent pas meilleur nous décrédibilise → QUE de l'IA branchée Loji ; (2) MCP ouvert tue les produits ; (3) retard concurrentiel. **Mon avis de fond franc** est dans le mot de la fin (encadré « sans filtre ») : le vrai facteur décisif n'est ni A ni B = la **vitesse de décision + le changement d'organisation**. Roadmap recadrée « = scénario A ; l'interne vaut A ou B ». Commit `3a0f373`. Cf [[feedback_avis_franc_ecrit_dans_livrable]].

**À FAIRE plus tard (reporté par Raphael)** : trame d'interview client (5-6 questions à 2-3 syndics) pour obtenir la vraie donnée de valeur — phase 2, comble le trou n°1.

Vault neoteem-brain (MCP obsidian-brain) = mine d'infos métier : OS mobilité (interventions/fournisseurs/relances), SEPA/appels de fonds (pain.001/008), régularisation charges, baux/GLI, module G-Suite Lojii, 682 notes support/FAQ/problèmes connus. Utiliser à fond pour ancrer les propositions. Cf [[chiffre-baseline-brief-verifier-empiriquement]] + [[llm-deep-research-version-numbers-hallucinated]].
