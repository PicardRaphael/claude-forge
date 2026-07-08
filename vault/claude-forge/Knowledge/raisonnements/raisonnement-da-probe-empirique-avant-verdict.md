---
titre: "DA : probe empirique avant verdict — méthode"
resume: "Quand le DA porte sur une idée dont la valeur repose sur une prémisse falsifiable, mesurer AVANT de débattre des garde-fous ; la donnée tranche entre verdict (c) tuer et verdict (b) garde-fous."
aliases:
  - "probe empirique avant verdict DA"
  - "DA mesurer avant débattre"
  - "prémisse falsifiable devil's advocate"
  - "verdict c versus b DA"
  - "data before devil's advocate"
  - "probe avant garde-fous"
type: knowledge
domaine: claude-code
derniere-maj: 2026-07-07
auteur: claude
tags:
  - "#type/raisonnement"
  - "#domaine/claude-code"
  - "#workflow/devils-advocate"
sources:
  - "Session 27 mai 2026 — DA compounding rétroactif A1×A3"
  - "[[critique-2026-05-27-compounding-retroactif]]"
  - "memory/feedback_da_probe_empirique_avant_verdict.md"
---

# DA : probe empirique avant verdict — méthode

Lien : [[critique-2026-05-27-compounding-retroactif]], [[comment-creer-agent]], [[devils-advocate-pipeline]]

## Problème

Un DA sur une idée-produit peut produire un verdict **(b) garde-fous** par défaut, sans jamais vérifier si la prémisse centrale tient. Résultat : du polish sur un puits sec, ou des garde-fous sur une calibration qui n'est pas le vrai problème.

> "Sans le chiffre, ton verdict est de l'opinion." — advisor, session 27 mai 2026

## Critère de déclenchement

Appliquer cette méthode quand le DA porte sur une **idée dont la valeur dépend d'une question mesurable en lecture seule** (ex : "% de transcripts contenant un apprentissage capitalisable et nouveau", "taux de faux positifs d'un filtre", "volume réel d'un gisement supposé").

Si la question n'est pas mesurable → DA standard sans probe préalable.

## Méthode — 3 étapes

### 1. Identifier la question falsifiable

Formuler la prémisse centrale de l'idée en une question binaire :
*"Est-ce que [gisement X] existe réellement en quantité suffisante pour justifier [mécanisme Y] ?"*

### 2. Mesurer sur l'existant (lecture seule)

- Parseur réel ou requête sur données existantes — pas de hand-waving.
- Échantillon classé à la main si nécessaire (n petit mais sur la slice la plus favorable est un signal fort).
- Assumer le caveat de taille et le documenter explicitement.
- Ne jamais biaiser l'échantillon vers le signal défavorable pour "tuer" l'idée — prendre la slice **la plus chargée en signal** pour que le résultat négatif soit robuste.

### 3. Classer (c) vs (b) selon prémisse ou calibration

| Résultat mesure | Diagnostic | Verdict |
|---|---|---|
| Le gisement n'existe pas (ex : 0/12) | Échec de **prémisse** | **(c) Tuer** — les garde-fous seraient du polish sur un puits sec |
| Le gisement existe mais heuristique trop large / fenêtre mal bornée | Échec de **calibration** | **(b) Garde-fous** — ajuster les seuils, borner la fenêtre |

**Règle absolue : ne jamais proposer un "(b) light" pour épargner une idée séduisante quand la donnée dit (c).** C'est le biais que le DA est censé tuer.

## Cas d'application — compounding rétroactif (27 mai 2026)

DA sur l'idée A1×A3 : scanner les transcripts passés à `/done` pour rattraper les apprentissages non capitalisés.

- Question falsifiable : *"Les transcripts contiennent-ils un gisement d'apprentissages capitalisables ET nouveaux ?"*
- Probe : parseur réel `sessions_indexer.parse_transcript` sur 123 transcripts. 12 messages tirés dans la slice la plus chargée en signal (`erreur|decision|pivot`, 120–350 chars).
- Résultat : **0/12 capitalisable ET nouveau** — majority bruit opérationnel ou déjà capitalisé avec citation explicite de la note vault.
- Verdict : **(c) tuer** — prémisse fausse, pas un problème de calibration. Pivot vers `/recall-uncaptured <topic>` on-demand.

Détail complet : [[critique-2026-05-27-compounding-retroactif]].

## Distinction avec autres patterns

- `verify-exhaustive-claims` — grep avant déclaration "tous/zéro/aucun" dans du code/config. Probe empirique DA = mesure de valeur produit, pas d'exhaustivité textuelle.
- [[da-dicte-tests-adverses]] — tests adverses sur du code destructif AVANT push. Probe DA = mesure de prémisse AVANT de rédiger le verdict.
- `brief-premisse-fausse-verifier-avant-executer` — vérifier la prémisse d'un brief avant d'exécuter. Probe DA = vérifier la prémisse d'une idée avant de conclure (b) ou (c).
