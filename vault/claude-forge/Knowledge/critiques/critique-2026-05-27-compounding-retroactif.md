---
titre: "Critique DA — Compounding rétroactif (A1×A3)"
resume: "Devils-advocate sur l'idée de scanner les transcripts passés à /done pour rattraper les apprentissages non capitalisés. Verdict (c) tué : probe empirique 0/12 capitalisable-ET-nouveau + circularité C5 by-design. Pivot retenu : /recall-uncaptured on-demand."
aliases:
  - "critique compounding retroactif"
  - "DA compounding retroactif"
  - "critique A1xA3"
  - "devils advocate compounding retroactif"
  - "verdict compounding retroactif"
  - "puits sec transcripts"
type: knowledge
derniere-maj: 2026-05-27
auteur: claude
tags:
  - "#type/critique"
  - "#projet/claude-forge"
  - "#workflow/devils-advocate"
sources:
  - "[[idee-compounding-retroactif]]"
  - "[[phase-4-comparaison-hermes-roadmap]]"
  - "[[ajouter-source-donnees-mcp-forge-brain]]"
---

# Critique DA — Compounding rétroactif (A1×A3)

Lien : [[idee-compounding-retroactif]], [[phase-4-comparaison-hermes-roadmap]], [[ajouter-source-donnees-mcp-forge-brain]]

## Idée auditée

À `/done`, croiser **A1** (recherche FTS5 des transcripts passés `~/.claude/projects/*.jsonl`) et **A3** (capitalisation proposée à validation `[v]/[m]/[i]`) : scanner l'historique brut pour les apprentissages **jamais capitalisés** et les proposer. Présenté en Phase 4 comme le différenciateur Jarvis unique (ni Hermes ni forge ne le font).

## Verdict : **(c) Tuer l'idée telle que formulée — pivoter vers un design on-demand**

La prémisse de l'idée est empiriquement fausse : *« les transcripts contiennent un gisement d'apprentissages capitalisables non capitalisés »*. La mesure dit l'inverse. Ce n'est pas un problème de calibration d'heuristique (qui justifierait des garde-fous = verdict b), c'est un échec de prémisse structurelle.

## Probe empirique (la donnée qui tranche)

Mesures réelles sur les 123 transcripts de claude-forge (parseur réel `sessions_indexer.parse_transcript`) :

- **9631 messages indexables** (7913 assistant / 1718 user), len médiane 195 chars.
- Fréquence des termes "riches" : `erreur` 8,1%, `feedback` 9,1%, `decision` 5,7%, `doctrine` 5,6%, `capitalis` 6,5%, `pivot` 2,5%, `ne plus refaire/jamais` 0,6%.

**Échantillon qualitatif décisif** : 12 messages tirés au hasard (seed fixé) parmi les 154 candidats filtrés sur `erreur|decision|pivot` en 120-350 chars — soit la **slice la plus chargée en signal** qu'on puisse sélectionner.

Classement manuel : **0/12 capitalisable ET nouveau.**
- ~8/12 = bruit opérationnel ou méta (chat sur un draft, "rien à sauvegarder", question utilisateur, annonce de méthode). Items [2][3] sont littéralement des `/done` ayant conclu vide.
- ~4/12 = déjà capitalisé — et dans plusieurs cas l'assistant **cite explicitement** la note vault / le feedback existant ([1] cite 3 notes, [7] cite le feedback delegate-guard, [11] est l'assistant en train de capitaliser).

Caveat assumé : n=12, sélection biaisée **vers** le signal. Un échantillon non filtré sur les 9631 messages serait pire, pas meilleur. La taille est petite mais le résultat (0 hit) sur la slice la plus favorable est un signal fort, pas marginal.

## Lecture des 5 risques (asymétrique — pas de symétrie artificielle)

### C5 — Circularité (RISQUE STRUCTUREL N°1, promu depuis "additionnel")

`sessions_indexer` garde les messages `user` ET `assistant` en texte plein (`_extract_text`, seuls tool_use/thinking sont droppés). Donc :
- Les blocs que `/done` **propose** (format `name:/description:/How to apply:`) sont indexés.
- Les validations de Raphael (`[v]/[m]/[i]`) sont indexées.
- Les `/done` qui concluent "rien à sauvegarder" sont indexés.

Mesure : 9 messages contiennent déjà un bloc `/done` proposé ; **135 messages (1,4%) citent un `feedback_*.md`** ; 189 (2,0%) citent un wikilink `[[X]]`. Au prochain scan rétroactif, ces messages remontent comme "apprentissages potentiels non capitalisés" alors que ce sont des artefacts de la capitalisation elle-même. **La circularité est by-design**, pas un edge case. La dedup devient le composant load-bearing — et elle doit matcher du texte transcript contre des fichiers `memory/` + wikilinks vault, ce que C4 montre techniquement flou.

### C4 — Heuristique de pertinence (problème dur, pas calibrable)

L'heuristique proposée dans la note ("segment transcript sans backlink vault ni entrée mémoire sur le même sujet") est techniquement floue : matcher un segment de conversation libre contre l'ensemble des wikilinks vault + feedbacks demande soit un embedding semantic match, soit un FTS5 cross-table (vault ⨯ transcripts) sur tokens partagés — non trivial, faux positifs/négatifs garantis. Le 1,4% de C5 montre que même un matcher parfait sur `feedback_*.md` ne couvrirait pas les reformulations. Ce n'est pas un seuil à monter, c'est un problème ML.

### C1 — Bruit : confirmé par la donnée (0/12), mais c'est un symptôme de C5+prémisse, pas la cause

Le bruit n'est pas "à filtrer" — le puits est sec. Resserrer l'heuristique ne ramène pas du contenu qui n'existe pas.

### C2 — Coût LLM : trivial à mesurer, NON rédhibitoire (mais hors sujet vu le verdict)

L'indexation FTS5 est **eager au boot** du serveur MCP (scan 2,68s mesuré, hors `/done`). Un scan rétroactif à `/done` = quelques requêtes FTS5 (millisecondes) + un appel LLM pour classer les hits. Coût acceptable en soi. Mais classer 0 signal utile = coût non nul pour valeur nulle.

### C6 — Obsolescence temporelle (identifié en plus)

Un apprentissage du 1er avril peut être contredit par un pivot doctrinal du 27 mai (cf [[methode-pivoter-doctrine]]). Une proposition rétroactive aveugle ressusciterait de la doctrine périmée. Aggrave C5.

### C7 — Gate humaine illusoire (identifié en plus)

En fin de session fatiguée (cf [[feedback_session_fatigue_decision]]), Raphael valide par lassitude. Si `/done` propose 10 blocs rétroactifs dont 0 pertinent, la gate `[v]/[m]/[i]` devient un tampon. Le contrôle humain — pilier du positionnement forge vs Hermes — est érodé par le volume.

## Matrice risques

| Risque | Sévérité | Probabilité | Mitigable ? | Coût mitigation |
|--------|----------|-------------|-------------|-----------------|
| C5 circularité | **Critique** | Certaine (by-design) | Partiellement (dedup robuste) | Élevé — composant load-bearing |
| Prémisse fausse (0/12) | **Rédhibitoire** | Mesurée | Non | — (puits sec) |
| C4 heuristique pertinence | Critique | Élevée | Non (problème ML) | Très élevé |
| C7 gate illusoire | Moyen | Élevée si volume | Oui (on-demand) | Faible si pivot |
| C6 obsolescence | Moyen | Moyenne | Oui (borne `since`) | Faible |
| C1 bruit | Élevé | Mesurée (0/12) | Non (symptôme) | — |
| C2 coût LLM | Faible | Certaine | Oui (borne) | Faible |

## Pivot retenu — `/recall-uncaptured <topic>` on-demand

Pas un garde-fou de (b) : un **design différent**. Raphael invoque la commande quand il a une intuition ("on avait parlé de X il y a 2 semaines"), au lieu d'un scan systématique à chaque `/done`.

Sidestep des risques :
- **Pas de bruit aveugle** : Raphael fournit le topic → scope étroit.
- **Pas de coût récurrent** : invoqué à la demande, pas à chaque `/done`.
- **Dedup tractable** : un seul topic, pas tout l'historique.
- **Pas de circularité systémique** : le topic exclut naturellement les méta-`/done`.
- **Heuristique triviale** : "tout ce qui matche le topic et n'est pas déjà dans le vault" — pas de détection ML du "capitalisable".

Faisabilité : ~30 min sur l'existant. `search_sessions(topic, since=...)` (déjà livré en A1) → résumé LLM des hits → gate `[v]/[m]/[i]` réutilisée d'A3. Validation empirique simple : si après ~5 invocations réelles il y a 0 capitalisation utile → tuer. Si ≥1 → garder.

## Ce qui est tué et ce qui survit

- **Tué** : A1×A3 systématique à `/done` (scan rétroactif aveugle). Prémisse fausse (0/12) + circularité by-design (C5). Ne pas réouvrir sans nouvelle donnée infirmant le 0/12.
- **Survit** : l'intention "rattraper le passé" via `/recall-uncaptured <topic>` on-demand, à valider empiriquement avant tout investissement.

## Angle mort assumé

Ce que je ne peux pas évaluer sans test en conditions réelles : la valeur subjective pour Raphael d'un `/recall-uncaptured` ciblé sur un topic qu'il a en tête. Le 0/12 mesure le scan **aveugle**, pas le rappel **dirigé**. C'est précisément pourquoi le pivot est proposé à validation empirique (5 invocations) et non buildé en dur.
