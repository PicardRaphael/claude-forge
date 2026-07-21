---
titre: "Dreaming — Self-Learning Agents via Review de Sessions"
resume: "Process scheduled qui review les sessions passées des managed agents, extrait patterns/erreurs récurrentes, déduplique, vérifie et enrichit la mémoire. Research preview mai 2026. Inspiré du sommeil humain — consolidation mémoire entre sessions"
aliases:
  - "dreaming"
  - "dreaming agents"
  - "dreaming managed agents"
  - "self-learning agents"
  - "agent dreaming"
  - "dream process"
  - "rêve agents"
type: feature
derniere-maj: 2026-07-21
auteur: claude
sources:
  - "https://www.youtube.com/watch?v=RtywqDFBYnQ"
  - "https://claude.com/code-with-claude/session/sf-memory-and-dreaming-for-self-learning-agents"
tags:
  - "#type/feature"
  - "#domaine/claude-code"
  - "#domaine/agents"
---

## Contexte

Lancé en **research preview** dans le Managed Agents API, 6 mai 2026 (Code with Claude SF). Présenté par Mahesh Murag. Complète [[Memory Managed Agents]] avec un process de review automatique.

## Comment ça marche

Dreaming = process schedulé qui :
1. **Review** les transcripts des sessions récentes (configuré : ex. 7 derniers jours)
2. **Identifie** les patterns, erreurs récurrentes, workflows convergents, préférences partagées
3. **Déduplique** les entrées redondantes (5 entrées identiques → 1)
4. **Vérifie** que les mémoires existantes sont encore valides (ajoute des "verification notes")
5. **Enrichit/backfill** avec les patterns cross-sessions qu'un seul agent ne peut pas voir
6. **Supprime** les entrées stales/obsolètes
7. Produit un **diff** appliqué à la memory store

### Analogie humaine
"Quand on dort, le cerveau review les souvenirs et renforce ceux qui valent la peine d'être gardés." Dreaming fait pareil pour les agents.

## Contrôle développeur

- **Auto** : dreaming met à jour la mémoire automatiquement
- **Review** : les changements sont proposés comme diff, le développeur approuve avant application
- Visible dans le Claude Console : sessions d'entrée, sub-agents de review, diff de sortie

## Ce que Dreaming voit qu'un agent seul ne voit pas

> "It surfaces patterns that a single agent can't see on its own: recurring mistakes, workflows that agents converge on, and preferences shared across a team."

Exemple SRE démontré :
- Plusieurs agents SRE déclenchés à exactement 60s après un spike CPU
- Aucun agent individuel ne remarque le pattern
- Dreaming identifie : "retry logic inefficace déclenche des alertes cascade avec délai fixe de 60s"
- Note ajoutée → les futurs agents bénéficient de cette découverte

## Amortissement du coût

> "Creating this index up front and curating it so that all downstream agents can use it effectively lets us amortize this effort across all of those agents."

Le coût du dreaming est payé une fois, réparti sur tous les agents qui lisent la mémoire.

## Pertinence pour forge

| Dreaming feature | Équivalent forge actuel | Gap |
|---|---|---|
| Review sessions passées | `/done` (1 session) | Pas de cross-session |
| Déduplication | `vault-audit` (score) | Pas de dedup contenu |
| Vérification mémoire | Aucun | Notes > 30j jamais revérifiées |
| Enrichissement cross-session | Aucun | Le compounding qu'on construit manuellement |
| Pattern detection | Aucun | Pas d'automatisme |

**Implémentation possible** : skill `/dream` comme `/schedule` hebdo qui review git log + vault + mémoire, déduplique, vérifie, enrichit. Pas une feature native Claude Code — à construire comme routine.

## Liens

- [[Memory Managed Agents]] — Primitive memory (storage + structure)
- [[Managed Agents]] — Feature Managed Agents
- [[MOC-Claude-Code]]


## Limites techniques (mai 2026)

| Paramètre | Valeur |
|-----------|--------|
| Sessions par dream | Max 100 |
| Input store | Jamais modifié (review-before-attach) |
| Modèles supportés | Opus 4.7, Sonnet 4.6 uniquement |
| Header API | `dreaming-2026-04-21` |
| Billing | Standard API rates |

## Démo live keynote SF (6 mai)

Startup fictive "Lumara" — landing drones sur la Lune :
- Simulation initiale : 4/6 sites réussis (Site 3 crash à 398 m/s, Site 4 en descente à 20.8 m/s)
- Dreaming lancé overnight via bouton "Dream" dans Developer Console
- Agent produit un "descent-playbook.md" avec heuristiques des missions précédentes
- Simulation post-dreaming : **6/6 sites réussis**, pas de régression

Le hill-climbing s'est fait sans intervention humaine — juste un clic sur "Dream".


---

## AJOUT 21 juillet 2026 — Intérieur d'un dreaming pass (talk AI DevCon by Tessl, Lamis, Applied AI)

> Source : même talk que [[Memory Managed Agents]] § AJOUT 21 juillet 2026 (vidéo native X transcrite + slides). Détaille l'ARCHITECTURE interne d'un pass, au-delà de la doc publique.

### Architecture d'un dreaming pass (slide « Inside a dreaming pass »)

```
Input memory store ($MEM) ──① clone──▶ Output memory store ($MEM_OUT)
        │
        ▼
  Orchestrateur ──② one per session──▶ Subagent × N
        ▲                                   │
  Session transcripts (1..N)                └──③ read/write to reorganise ──▶ $MEM_OUT
```

- **① Clone** : l'input store n'est JAMAIS modifié (confirme le review-before-attach documenté).
- **② Un subagent PAR transcript de session** — l'orchestrateur déploie une flotte, chaque subagent analyse un transcript. Les transcripts incluent les passes agent↔user **ET les métadonnées : tool calls, skills utilisées** — « we're really scrutinizing those tool calls », central pour détecter les misconfigurations.
- **③ L'orchestrateur review les retours des subagents** et ne propose un changement que si le pattern est **assez prévalent** (« where there are prevalent enough patterns that it thinks this warrants a change »).
- **Output livré avec preuves** : chaque changement proposé est accompagné de **transcripts d'exemple** où le pattern apparaît + **stats de prévalence** → l'humain accepte/rejette changement par changement.

### Steering — curation configurable

On peut dire aux agents memory ET dreaming « ce qui est important / pas important » pour SON organisation → le processus de curation est orientable par domaine, pas générique.

### Analogie école (pédagogie du talk)

Élèves (agents) + professeurs + **proviseur qui review toutes les copies** (dreaming) :
- Tous les élèves de géo ratent la même question → le sujet **manque au curriculum** (= trou dans le memory store, backfill).
- Tous les élèves de maths répondent en **radians au lieu de degrés** → consigne « configurez vos calculatrices » (= tool misconfiguration détectée dans les tool calls des transcripts).
- « Tout le monde abuse des em-dashes » → changement de contexte **org-wide** (= préférence de flotte).

### Économie du pass

Objection « c'est cher de dédier des tokens à ça » → contre-argument : les memory stores efficaces font baisser les coûts downstream (**one-shotting** plus fréquent, moins de tokens par tâche) ; le dreaming a « its own allocated resources » précisément pour supprimer le **split focus** de la mémoire in-band (l'agent de tâche n'a plus à arbitrer tâche vs curation). Rejoint l'amortissement documenté (coût payé une fois, réparti sur tous les agents lecteurs).

### Slide « How dreaming works » (vue d'ensemble)

Transcripts des sessions quotidiennes → **Dreaming (periodic batch process)** → updated memory state (« new insights » + « organized structure ») → « **next day's agent sessions are automatically more intelligent** ». Le système unifié = Memory (real-time, pendant que les agents bossent) + Dreaming (batch périodique, entre les sessions) — les deux écrivent le même store versionné.
