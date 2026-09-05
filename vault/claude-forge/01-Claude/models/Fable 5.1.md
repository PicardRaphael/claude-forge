---
titre: "Claude Fable 5.1 — modèle Fable par défaut depuis le 1er septembre 2026"
resume: "Sorti le 1er sept. 2026 : claude-fable-5-1, 1M contexte / 128K output, $10/$50 par MTok, cache read $0,25/MTok (un quart du tarif Fable 5), thinking adaptatif toujours actif, effort défaut high, cutoff juin 2026. Trois breaking changes vs Fable 5 : forced tool use interdit, thinking blocks liés au modèle, historique append-only. Anthropic recommande de démarrer sur Opus 5 et de réserver Fable 5.1 au raisonnement exigeant et à l'agentique longue durée. Mythos 5.1 = même modèle, safeguards renforcés."
aliases:
  - "Claude Fable 5.1"
  - "Fable 5.1"
  - "claude-fable-5-1"
  - "fable-5-1"
  - "Mythos 5.1"
  - "claude-mythos-5-1"
derniere-maj: 2026-09-05
auteur: claude
type: modele
sources:
  - "https://platform.claude.com/docs/en/models/fable-5-1/overview"
  - "https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1"
  - "https://www.anthropic.com/claude-fable-and-mythos-5-1"
  - "https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1"
  - "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md"
tags:
  - "#type/modele"
  - "#domaine/anthropic"
  - "#domaine/claude"
---

# Claude Fable 5.1

> Publié le **1er septembre 2026**, en même temps que Mythos 5.1. Devient **le modèle Fable par défaut**, y compris dans Claude Code (v2.1.257, verbatim : *« Added Claude Fable 5.1 (`claude-fable-5-1`), now the default Fable model — 1M context, $10/$50 per Mtok with $0.25/Mtok cache reads »*).

## Specs

| Item | Valeur |
|------|--------|
| ID modèle | `claude-fable-5-1` |
| Date | 1er septembre 2026 |
| Prix | **$10 / M input · $50 / M output** — identiques à Fable 5 |
| Cache writes | $12,50 / MTok (5 min) · $20 / MTok (1 h) — inchangés |
| Cache read | **$0,25 / MTok** = 0,025 × input, contre 0,1 × input sur les autres modèles Claude — *« pay a quarter of the Claude Fable 5 rate »* |
| Contexte | **1M tokens** (défaut ET maximum) / 128K output |
| Thinking | **Adaptatif, toujours actif** (non désactivable) |
| Effort | défaut **`high`** ; `low` · `medium` · `xhigh` · `max` disponibles |
| Batch | $5 / M input · $25 / M output |
| Knowledge cutoff | juin 2026 |
| Rétention | 30 jours, pas de zero-data-retention sans autorisation expresse |

## Positionnement officiel

Verbatim, doc plateforme : *« For most workloads, start with Claude Opus 5… Use Claude Fable 5.1 for demanding reasoning and long-horizon agentic work, or when your evals on Claude Opus 5 at higher effort still fall short. »*

Autrement dit : [[Opus 5]] reste le point de départ par défaut, Fable 5.1 est le **step-up mesuré** quand Opus 5 à effort élevé ne suffit plus. Ce n'est pas « le meilleur modèle, donc le modèle à prendre ».

## Mythos 5.1 — même modèle, autres safeguards

Verbatim annonce : *« Claude Fable 5.1 and Claude Mythos 5.1 are the same model, but with different levels of safeguards. Fable 5.1 is generally available, while Mythos 5.1 is available only through trusted access programs; its safeguards are specifically designed to support work in cybersecurity and the life sciences. »*

Mythos 5.1 n'est donc **pas un modèle distinct** : c'est Fable 5.1 avec un profil de garde-fous différent, réservé aux organisations vetted via **Project Glasswing**. Aucune fiche séparée n'est justifiée.

## Trois breaking changes vs [[Fable 5]]

Une intégration qui appelait déjà Fable 5 casse sur ces trois points :

1. **Forced tool use interdit.** `tool_choice: {"type": "any"}` et `{"type": "tool", "name": "…"}` renvoient un **400** (`tool_choice: type "tool" and "any" are not supported for this model`). Motif : le thinking étant toujours actif, un appel forcé le court-circuiterait et le modèle écrirait son raisonnement dans les arguments de l'outil, dégradant leur qualité. Remède : garder `{"type": "auto"}` et passer par **strict tool use** (`strict: true`) ou les **structured outputs** ; pour forcer l'usage, le dire en clair dans le prompt (« Use the `get_weather` tool to answer »).
2. **Les thinking blocks sont liés au modèle qui les a produits.** La préservation est unidirectionnelle : 5.1 lit les blocs des modèles antérieurs, aucun modèle antérieur ne lit ceux de 5.1. Une conversation qui *monte* vers 5.1 garde son raisonnement ; une conversation qui en *redescend* le perd. Les blocs illisibles sont retirés avant le modèle, ne comptent pas dans `input_tokens` et ne sont pas facturés — mais le retrait est **silencieux** sans le beta header `thinking-binding-controls-2026-08-01`. À surveiller sur tout routeur ou fallback qui change de modèle en cours de conversation.
3. **Modifier un tour antérieur invalide les thinking blocks.** Voir le gotcha append-only ci-dessous.

## Nouveautés exploitables

- **Effort modifiable en cours de conversation** (beta `mid-conversation-output-config-2026-07-01`) : monter l'effort pour une étape dure, le redescendre ensuite, **sans invalider le prompt cache**. Se pose via un message `role: "system"` portant `output_config: {"effort": …}`, actif au tour utilisateur suivant. Supporté par Fable 5.1, Mythos 5.1 et Opus 5.
- **Messages système à portée d'un tour** (beta `mid-conversation-system-clear-at-2026-08-21`) : `clear_at: "next_user_message"` donne l'autorité d'un system prompt pour le tour courant, puis cesse de rendre. Le message reste dans `messages` et se renvoie verbatim — le cache continue de matcher et les blocs suivants restent valides. C'est la manière propre de faire un rappel par tour dans une boucle d'outils, à la place d'un texte injecté puis supprimé.
- **Progress updates lisibles** (beta `thinking-display-updates-2026-08-18`) : `thinking.display: "updates"` renvoie en texte les mises à jour inter-outils tout en gardant le raisonnement caché.
- **Provenance du contenu** : watermark statistique sur tout texte produit, Content Credentials C2PA signés sur les fichiers image/vidéo/audio récupérés via la Files API. Aucun token ajouté, aucune information sur l'utilisateur.

## Ce qui change vs [[Fable 5]] (sans changement de code)

| | Fable 5 | Fable 5.1 |
|---|---|---|
| Statut | génération précédente | **défaut Fable** |
| Cache read | $1 / MTok (0,1 × input) | **$0,25 / MTok** (0,025 × input) |
| Safeguards | classifier renforcé post-redéploiement, faux positifs fréquents en coding/debugging | **moins de faux positifs** ; *« finding vulnerabilities in source code is permitted »* |
| Appels d'outils parallèles | groupait plusieurs appels | **plus variable** — parfois un seul appel par tour, ce qui coûte des tours sans dégrader la réponse |
| Narration | plus bavard entre les tool calls | **moins d'updates**, surtout à effort élevé — nécessite `thinking.display: "updates"` |
| Formatage | — | **moins** de gras, de titres et de listes |
| Écriture | — | prose **plus dense** |
| Citations | — | reproduit plus souvent des passages sans les marquer comme citations |
| Édition de fichiers | — | réécrit plus volontiers un fichier entier au lieu d'une édition ciblée |

Anthropic garantit la compatibilité des prompts : *« Your existing Claude Fable 5 prompts should perform well on Claude Fable 5.1 without changes, but a handful of behavioral differences are worth knowing about. »*

## ⚠️ Gotchas

- **Historique append-only obligatoire.** Pour les comptes créés depuis le **31 août 2026**, modifier quoi que ce soit avant un thinking block (system prompt, tableau `tools`, message antérieur) fait échouer la requête suivante avec un 400 *« The block is bound to a different conversation »*. Cassent l'historique : éditer/réordonner/supprimer un tour antérieur, injecter puis retirer un texte par requête, reconstruire `system` ou `tools` entre deux requêtes, servir des octets différents derrière une même URL d'image. Ne cassent rien : retirer une série de blocs **en partant du plus ancien**, laisser la compaction ou le context editing côté serveur tronquer, déplacer les marqueurs `cache_control`, changer l'effort. Remèdes : messages système en cours de conversation plutôt qu'édition du prompt, et le header `thinking-binding-controls-2026-08-01` avec `prefix_mismatch_behavior: "drop_block"` pour continuer malgré le décalage (le retrait est alors reporté dans `input_transformations`). Claude Code, claude.ai et l'Agent SDK gèrent déjà ce préfixe. Mythos 5.1 ne fait pas ce contrôle.
- **Le sweep d'effort n'est pas transférable** : *« effort level names don't correspond to the same amount of thinking across models »*. À `medium`, 5.1 égale Fable 5 pour moins cher ; à `low`, il est *« often competitive with Claude Opus and Claude Sonnet models on cost per task while scoring higher »*.
- **Alias gateway** : derrière un Claude apps gateway, `fable` et `best` **continuent de résoudre vers Fable 5** tant que le gateway n'est pas configuré pour 5.1 — sélectionner Fable 5.1 explicitement dans `/model`.
- **Tag `[1m]`** : un agent `model: fable` pouvait tourner silencieusement en **200K** au lieu de 1M si le tag était ignoré sur un pin `ANTHROPIC_DEFAULT_FABLE_MODEL` (corrigé CC v2.1.260).
- **Recherche à effort `low`** : 5.1 déclenche moins les outils de recherche et répond de mémoire — Anthropic cite nommément *« a fast-moving area like AI models and developer tools »*. Ne jamais faire tourner une veille à `low`.
- **Refus** : `stop_reason: "refusal"` reste possible, en HTTP 200 avec un objet `stop_details` nommant la politique déclenchée. Un refus arrivant avant toute sortie n'est pas facturé, et le *fallback credit* rembourse le coût de cache du changement de modèle. Cibles de fallback autorisées : **Opus 4.8 et Opus 5**. Trois déclencheurs de faux positifs : phrasé « est-ce que ça compile sans erreur » (préférer « y a-t-il des bugs »), langages peu connus, **base64 en sortie d'outil**.
- **Inchangé depuis Fable 5** : prefill de la réponse assistant → 400 ; `temperature`/`top_p`/`top_k` non défaut → 400 ; longueur minimale cacheable de 512 tokens ; thinking interleaved automatique sans header.

## Pertinence forge

- L'alias `fable` de Claude Code résout désormais vers Fable 5.1 — aucun composant forge n'épingle `claude-fable-5`, donc pas de migration à faire.
- Vérifié le 5 sept. 2026 : **aucun composant forge ne porte de règle anti-formatage sur les réponses, d'instruction « montre ton raisonnement », ni de suppression de narration**. Rien à corriger côté prompts.
- Le point `low`/`medium` renforce l'anti-biais de Raphaël sur l'effort : Anthropic désigne lui-même les efforts bas comme compétitifs, ce que forge n'exploite quasiment pas.
- L'effort modifiable en cours de conversation est la brique qui manquait au step-up mesuré : au lieu de choisir un niveau pour toute une session, on peut monter sur l'étape de jugement et redescendre sur la mécanique — sans perdre le cache.

## Liens

- [[Fable 5]] — génération précédente, cycle suspension/redéploiement
- [[Opus 5]] — point de départ recommandé par Anthropic
- [[prompting-fable5-cheatsheet]] — patterns de prompting + différences 5.1 par symptôme
- [[doctrine-par-modele-opus5-fable5]] — quel modèle pour quel agent
- [[MOC-Modeles]]
