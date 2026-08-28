---
titre: "DA blocking — résolutions et arbitrages"
resume: "Journal des verdicts Devil's Advocate bloquants rencontrés sur forge, de leur arbitrage explicite et de la preuve de résolution."
aliases:
  - "da blocking non arbitre"
  - "journal da blocking"
  - "arbitrages devil advocate"
  - "résolutions bloquants da"
type: erreur
derniere-maj: 2026-08-28
auteur: codex
tags:
  - "#type/erreur"
  - "#domaine/qualite"
  - "#doctrine/2026"
---

# DA blocking — résolutions et arbitrages

## 2026-08-28 — faux portage learning-reminder sur Stop Codex

**BLOCKING (score 100)** : le prototype Codex retournait `additionalContext` sur `Stop`, champ non supporté ; son test vérifiait seulement une fonction locale, pas le protocole runtime. Un portage via `decision:"block"` aurait forcé une continuation.

**Arbitrage** : option A, fix immédiat. Raphaël avait donné carte blanche puis demandé « reprend » après l'annonce explicite du retrait du faux hook.

**Résolution vérifiée à 100 %** :

- copie `.codex/hooks/learning-reminder.py` supprimée ;
- aucun enregistrement Stop Codex ;
- validateur anti-régression sur l'absence du fichier et de son câblage ;
- 281 tests hooks Codex passent ;
- doctrine vault corrigée : détecteur Claude uniquement, recall/règles/skills côté Codex.

Aucune dette acceptée.
