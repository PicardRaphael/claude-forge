---
name: capitalisation-proposee-pas-auto
description: "Une skill peut PROPOSER du contenu de capitalisation pret-a-ecrire (diff visible), mais JAMAIS ecrire sans validation humaine explicite par item. Couverture Hermes + controle forge."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 492c167d-73c8-42da-8e57-f7b41a17bfa8
---

Quand une skill capitalise des apprentissages (mémoire, vault, ADR), elle doit GÉNÉRER des blocs concrets prêts-à-écrire et les présenter en diff visible, puis attendre une validation explicite item par item (`[v]alider / [m]odifier / [i]gnorer`) avant toute écriture. La proposition réduit l'effort cognitif ("ce qui est proposé est-il juste ?" au lieu de "quoi capitaliser ?") sans retirer le contrôle à l'humain.

**Why:** Croisement Jarvis identifié Phase 4 (comparaison Hermes Agent). Hermes a un background review qui écrit en mémoire SANS validation (notif après coup) — forte couverture, zéro contrôle. claude-forge avait l'inverse : `/done` rappelait quoi capitaliser mais Raphael devait tout rédiger. Le bon point d'équilibre = importer la COUVERTURE de Hermes (proposer auto) en gardant le CONTRÔLE forge (humain valide avant écriture). Une écriture auto silencieuse viole le principe "Raphael tranche" et est incompatible avec le use case synchrone de forge. La différence clé vs Hermes : un diff que Raphael relit, jamais un overwrite silencieux.

**How to apply:** Toute skill/composant qui capitalise (`done`, futurs équivalents) → (1) détecter les items capitalisables après filtre, (2) vérifier les doublons (search_brain) avant de proposer — si doublon, proposer un AMENDEMENT pas une création, (3) générer le bloc prêt-à-écrire au format cible (feedback MEMORY.md / note vault Obsidian / ADR), (4) présenter type + chemin + contenu, (5) écrire SEULEMENT après validation explicite. Anti sur-généralisation : 1 occurrence = feedback ponctuel, jamais une "règle". "Rien à proposer" est une réponse honnête valide. Cf [[done]] (skill), roadmap Phase 4 A3.
