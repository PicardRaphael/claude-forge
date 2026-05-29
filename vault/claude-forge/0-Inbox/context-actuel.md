---
titre: Context Actuel
resume: Working memory dynamique -- mis a jour par /done, lu par /recap
aliases: ["context actuel", "contexte courant", "working memory", "memoire de travail", "etat actuel"]
type: context
status: active
derniere-maj: 2026-05-29
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---

## Phase actuelle
Production d'une **trilogie de documents stratégiques IA pour le CODIR Neoteem** (Raphaël, casquette Responsable IA). Documents prêts, à faire valider par Jérôme puis présenter au CODIR.

## Dernière session (2026-05-29)
### Décisions prises
- **3 documents distincts** dans `output/neoteem/` : Stratégique (le *pourquoi*, 24p), Roadmap IA (le *quoi/quand*, 21p), Modèle économique (le *combien*, 9p). Rôles séparés, références croisées, pas de répétition inutile.
- **Charte graphique Neoteem** figée : `output/neoteem/_charte/neoteem-charte.css` + `CHARTE.md`. Identité réelle (logo.webp couleur, bleu #0a3a5c, teal #00a78e, dégradé teal→corail→magenta).
- **Génération PDF** : Chrome headless `--no-pdf-header-footer` + Poppler pour vérif visuelle. Recette + gotchas → `reference_pdf_chrome_headless_charte.md`.
- **NeoMail = « à cadrer totalement »** (besoin/fonctionnalités/forme : add-on Gmail/panneau Loji/extension/MCP). Le back existant = prototype, pas un acquis (construit sans cadrage) → estimations intègrent le re-travail.
- **Moat = base de données Loji** (pas l'IA, qui est une commodité). Message central des 3 docs.

### En cours
- Rien en cours d'écriture. Les 3 PDF sont à jour et cohérents (relus mot à mot ; incohérences corrigées : Office 365→agent mail, double thead, NeoMail back, timeline, MCP Gemini grand public = NON self-service).

### Prochaines étapes
- Raphaël envoie les 3 docs à **Jérôme** (co-validation réalisme technique, déjà mentionnée dans la roadmap) → puis CODIR.
- **1re action post-validation** : cadrage NeoMail via le **Club Utilisateurs Neoteem** (canal pour la donnée client réelle, comble le seul trou : zéro donnée client validée à ce jour).
- Volet **tarifs / packs** : dans le doc Modèle économique (fourchettes à valider marché, pas figées).

## Fils ouverts
- **Idées d'agents** sauvegardées dans le vault ([[idees-agents-ia-issues-tickets-support]]) : auto-diagnostic support, pré-vol comptable, préparation révision loyers, qualification/triage ticket, agent sinistre. Toutes fondées sur 250 tickets réels. Ajoutées au catalogue roadmap (badge Claude).
- **Chatbot B2B2C** : sujet porté par la direction, à mettre en avant ; audit à lancer tôt.
- **Maintenance forge** (hors Neoteem) : `memory/` à 277 fichiers vs 100 cible → `/clean-memory` en session dédiée un jour.

## Notes vault Neoteem créées cette session
- [[comprendre-neoteem-vue-responsable-ia]] — architecture, domaines, moat
- [[veille-concurrents-ia-syndic]] — concurrents + verdict MCP Gemini grand public
- [[idees-agents-ia-issues-tickets-support]] — idées agents issues des 250 tickets

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
