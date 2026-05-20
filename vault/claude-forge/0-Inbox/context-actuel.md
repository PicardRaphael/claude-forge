---
titre: Context Actuel
resume: Working memory dynamique — mis à jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, mémoire de travail, état actuel]
type: context
status: active
derniere-maj: 2026-05-18
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---

## Phase actuelle
Capitalisation du guide officiel Anthropic Opus 4.7 + fiabilisation des skills cross-repo (neo_ia, ia_back).

## Dernière session (2026-05-18)

### Décisions prises
- Capitalisation guide officiel Anthropic "Prompting best practices" (~900 lignes) en 5 notes vault
- Création du cheat sheet `prompting-opus47-cheatsheet` — 20 prompts officiels copier-coller
- Création de `opus-47-design-defaults` — style persistant cream/Georgia + 2 contre-mesures
- 20 skills passées `user-invokable: true` sur neo_ia (13) et ia_back (7) — toutes les skills référence/conventions
- Nouvelle note feature vault : `auto-mode-classifier` (système Anthropic non documenté ailleurs)

### En cours
- Rien en cours — session clôturée.

### Prochaines étapes
1. Vérifier que /goal et autres workflows neo_ia utilisent bien les skills maintenant accessibles
2. Étendre `config-guardian` pour détecter les skills référence marquées `false` (pattern récurrent)
3. Fusionner `claudemd-maintenance.md` dans `claudemd-guide.md` (DA bloquant)
4. Tests architecture multi-agents : `0-Inbox/tests-architecture-repos.md`
5. cc-news post-Google I/O (19-20 mai) — Gemini Omni attendu

## Fils ouverts
- Le guide "31 pages" Anthropic = la page docs officielle (pas un PDF) — sources à jour dans notes Opus 4.7
- Classifier auto-mode bloque les git cross-repo sans permission explicite — note feature créée
- Skills `user-invokable: false` = invisibles à Claude sauf référencées par autre skill → règle systémique
- Forge = PRIVÉ, jamais d'open-source (feedback explicite Raphael)
- Deprecation Sonnet 4 / Opus 4 le 15 juin — vérifier aucun code ne référence les anciens IDs
- Cowork n'a PAS de hooks — checklist harness engineering uniquement

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[Claude-Forge|Claude-Forge]]
[[prompting-opus47-cheatsheet]]
[[auto-mode-classifier]]
