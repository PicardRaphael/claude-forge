---
name: feedback-triage
description: Analyze pending user feedbacks from the Neoteem database, investigate Langfuse traces and sessions, classify ticket type ([IA] Bug / [IA] Feature / [IA] A CLASSER), and create Jira tickets in project N2 linked to parent N2-109957. Use when asked to triage feedbacks, analyze pending feedbacks, or on a daily schedule.
allowed-tools: Bash
model: sonnet
effort: high
---

# Feedback Triage — Analyse et creation de tickets Jira

Cette skill orchestre le triage automatique des feedbacks utilisateurs NeoChat/NeoDoc/NeoMail.

## Services utilises

| Service | Type | URL / Acces |
|---------|------|-------------|
| **MCP feedback-neoteem** | MCP HTTP cloud | `https://mcp-feedback-dev-20945515568.europe-west1.run.app/mcp` |
| **Langfuse CLI** | npx en sandbox | `npx langfuse-cli api ...` |
| **neoteem-brain-dev + dev-ia** | Plugins Cowork installes | Skills `/neo-brain`, `/neo-brain-dev-ia` |
| **Jira N2** | Connecteur Cowork | Connecteur natif — projet N2, parent N2-109957 |
| **Code repos** | Dossiers montes Cowork | `ia_back/`, `neo_ia/`, `bdd/` |

## Flux complet

```
1. Recuperer les feedbacks pending          (MCP feedback-neoteem)
2. Pour chaque feedback :
   a. Analyser la trace Langfuse            (langfuse CLI)
   b. Si besoin, remonter la session        (langfuse CLI)
   c. Consulter le brain contexte metier    (skill /neo-brain si besoin)
   d. VERIFIER L'EXISTANT                   (skill /neo-brain-dev-ia — OBLIGATOIRE)
   e. Classifier : [IA] Bug / [IA] Feature / [IA] A CLASSER
   f. Analyse technique profonde            (selon la classification)
   g. VERIFIER LES DOUBLONS                 (Jira search avant creation)
   h. Creer ticket Jira OU commenter        doublon existant
   i. Marquer le feedback traite            (MCP feedback-neoteem)
```

## Etape 1 — Recuperer les feedbacks pending

Utiliser le MCP `feedback-neoteem` (deploye sur Cloud Run) :

```
Tool: get_pending_feedbacks
Args: { "type": "negative", "limit": 20 }
```

Chaque feedback contient :
- `feedback_id` — identifiant unique
- `feedback_messages` — contexte riche (question user, reponse agent, nom agent, score)
- `feedback_commentaire` — commentaire libre de l'utilisateur (peut etre null)
- `feedback_trace_id` — ID de la trace Langfuse (l'echange precis note)
- `feedback_threadid` — ID de la session Langfuse (toute la conversation)
- `feedback_exchange` — paire question/reponse epuree
- `feedback_acteurid` — qui a donne le feedback
- `feedback_clientid` — quel client

Si aucun feedback pending, terminer avec un message "Aucun feedback a traiter".

## Etape 2a — Analyser la trace Langfuse

Les credentials Langfuse (`LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST`) sont configurees dans les variables d'environnement du projet. Pas besoin de les charger manuellement.

Pour chaque feedback avec un `feedback_trace_id`, recuperer la trace :

```bash
npx langfuse-cli api traces get <feedback_trace_id> --json
```

**ATTENTION TOKENS** : une trace complete peut faire 30 000+ tokens. Ne PAS lire le JSON entier. Extraire uniquement les champs utiles :

```bash
# Recuperer seulement input, output, metadata et tags
# IMPORTANT : la reponse langfuse-cli wrappe tout dans "body"
npx langfuse-cli api traces get <feedback_trace_id> --json | python3 -c "
import sys,json
r=json.load(sys.stdin)
t=r.get('body', r)
print(json.dumps({
  'name': t.get('name'),
  'input': t.get('input'),
  'output': t.get('output'),
  'metadata': t.get('metadata'),
  'tags': t.get('tags'),
  'latency': t.get('latency'),
  'sessionId': t.get('sessionId')
}, indent=2, ensure_ascii=False))
"
```

Examiner :
- **input/output** : la question user et la reponse finale
- **statusMessage** : erreur eventuelle
- **metadata** : agent name, model

Pour les **observations** (detail des tool calls et LLM calls), ne les lister que si le diagnostic l'exige :

```bash
npx langfuse-cli api observations-v2s list --traceId <id> --json --limit 10
```

Si la trace seule ne suffit pas (ex: l'erreur vient d'un message precedent), passer a l'etape 2b.

Reference detaillee : [references/langfuse-cli.md](references/langfuse-cli.md)

## Etape 2b — Remonter la session complete

Utiliser le `feedback_threadid` pour voir toute la conversation :

```bash
npx langfuse-cli api sessions get <feedback_threadid> --json
npx langfuse-cli api traces list --sessionId <feedback_threadid> --json
```

Examiner les traces precedentes pour trouver si le probleme a commence plus tot dans la conversation.

## Etape 2c — Consulter neoteem-brain (si besoin)

Deux skills disponibles selon le besoin :

### `/neo-brain-dev-ia` — pour le technique (RECOMMANDE pour le triage)

Retourne un etat structure de ce qui existe dans les repos dev :
- Fonctions PG dans **bdd**
- Endpoints dans **ia_back**
- Tools/agents dans **neo_ia**
- Pages dans **lojii-front**

**Invocation :**
```
/neo-brain-dev-ia est-ce qu'un endpoint pour les charges de copropriete existe deja ?
```

La skill repond avec un verdict structure : ce qui existe, ce qui manque, ou creer.

### `/neo-brain` — pour le pur contexte metier

Si tu as juste besoin de comprendre un concept metier (regles syndic, comptabilite, etc.), utiliser `/neo-brain`.

**Invocation :**
```
/neo-brain explique la difference entre charges copropriete et charges locatives
```

### Quand utiliser quoi

| Besoin | Skill |
|--------|-------|
| Verifier si un endpoint/tool/fonction existe | `/neo-brain-dev-ia` |
| Comprendre une regle metier pure | `/neo-brain` |
| Analyser une evolution (existant vs a creer) | `/neo-brain-dev-ia` |
| Valider si le comportement de l'agent est correct | Les deux (metier + technique) |

## Etape 2d — OBLIGATOIRE : Verifier l'existant via /neo-brain-dev-ia AVANT de classifier

**AVANT de classifier le type de ticket, tu DOIS invoquer `/neo-brain-dev-ia`** pour verifier si les fonctionnalites mentionnees existent. Ne JAMAIS classifier sans cette verification.

### Priorite des sources : brain D'ABORD, repos EN COMPLEMENT

**REGLE ABSOLUE : ne JAMAIS chercher dans les repos (Grep, Read) avant d'avoir interroge `/neo-brain-dev-ia`.**

Le vault neoteem-brain documente les tools, agents, endpoints, fonctions PG et le contexte metier. Une recherche brain coute 5-10x moins de tokens que grep dans du code brut.

```
CORRECT :
  1. /neo-brain-dev-ia "existe-t-il un tool pour les debiteurs ?"
  2. Reponse suffisante → classifier. STOP.
  3. Reponse insuffisante → completer avec Grep/Read dans les repos.

INTERDIT :
  1. Grep dans neo_ia/ et ia_back/ en parallele  ← gaspillage de tokens
  2. /neo-brain-dev-ia en meme temps que Grep     ← pareil
```

Ne PAS lancer brain et code en parallele. Brain d'abord, code ensuite si besoin.

### Etape 1 — Analyser le probleme dans neo_ia D'ABORD

Commencer TOUJOURS par neo_ia. Beaucoup de problemes se resolvent uniquement dans neo_ia :

```
1. Le tool existe dans neo_ia ?
   → OUI mais mal utilise → [IA] Bug. STOP.
   → NON → passer a 2.

2. Le probleme peut-il etre resolu UNIQUEMENT dans neo_ia ?
   Exemples de solutions purement neo_ia :
   - Ajouter une source dans le whitelist d'un agent (ex: ajouter INSEE)
   - Modifier le prompt de l'agent
   - Modifier la classification/routing de l'agent
   - Ajouter un mot-cle dans le classify.py
   - Connecter un tool existant a un agent qui ne l'a pas
   → OUI → [IA] Feature (ou Bug). Decrire la modification neo_ia. STOP.
   → NON (besoin de nouvelles donnees pas accessibles dans neo_ia) → passer a 3.
```

### Etape 2 — Chercher dans ia_back SEULEMENT si neo_ia ne suffit pas

Ne descendre dans ia_back QUE si la solution necessite des donnees ou un endpoint qui n'existe pas :

```
3. L'endpoint existe dans ia_back ?
   → OUI → creer le tool neo_ia qui l'appelle. STOP.
   → NON → passer a 4.
```

### Etape 3 — Chercher dans bdd SEULEMENT si ia_back n'a pas l'endpoint

```
4. Des fonctions PG existent dans bdd pour ce besoin ?
   → OUI → proposer de creer l'endpoint ia_back (refacto en TS) puis le tool neo_ia.
           Lister les fonctions bdd comme reference.
   → NON → tout est a creer from scratch.
```

Rappel : ia_back refactore la logique des fonctions PG en TypeScript (archi hexagonale). Les fonctions bdd servent de **reference**, pas d'appel direct.

### Exemples concrets

**Exemple 1 — Solution uniquement neo_ia :**
- Feedback : "quelle est l'evolution de l'indice ILC" → agent web repond "aucun resultat"
- Analyse : l'agent web n'a pas INSEE dans ses sources. L'ILC est publie par INSEE.
- Solution : ajouter `insee.fr` dans `WebSourceType` de l'agent web. **Pas besoin d'ia_back.**
- Classification : [IA] Feature (simple, neo_ia seulement)

**Exemple 2 — Besoin d'ia_back :**
- Feedback : "liste des personnes qui me doivent de l'argent"
- Analyse : aucun tool dans neo_ia. Endpoint `GET /api/v1/locataires-en-retard` EXISTE dans ia_back.
- Solution : creer un tool qui appelle l'endpoint. **Pas besoin de bdd.**
- Classification : [IA] Feature (creer tool neo_ia)

**Exemple 3 — Besoin de bdd :**
- Feedback : "montre-moi le detail des charges de copropriete"
- Analyse : aucun tool dans neo_ia. Aucun endpoint dans ia_back. Mais `f_donne_detail_charges_copro` existe dans bdd.
- Solution : creer endpoint ia_back (inspire de la fonction PG) puis tool neo_ia.
- Classification : [IA] Feature (complet)

## Etape 2e — Classifier le type de ticket

C'est le champ **Type** du ticket Jira. Trois types possibles dans le projet N2 :

| Type Jira | Criteres |
|-----------|----------|
| **[IA] Bug** | Un tool existant dans neo_ia donne un mauvais resultat, un endpoint existant dans ia_back retourne une erreur, un retrieval ramene le mauvais contenu |
| **[IA] Feature** | La fonctionnalite n'existe pas dans le code (ni tool dans neo_ia, ni endpoint dans ia_back). Inclut les cas ou le bot promet une capacite non implementee |
| **[IA] A CLASSER** | Apres verification dans le code, impossible de determiner si Bug ou Feature (feedback ambigu, manque d'info) |

### Comment distinguer Bug de Feature

| Situation | Classification |
|-----------|----------------|
| Tool existe et fonctionne mal | **[IA] Bug** |
| Config agent a corriger (source, prompt, routing) | **[IA] Bug** ou **[IA] Feature** selon le cas |
| Solution possible uniquement dans neo_ia (ajout source, modif config) | **[IA] Feature** (neo_ia seul) |
| Tool a creer, endpoint ia_back existe | **[IA] Feature** (creer tool) |
| Tool + endpoint a creer, fonctions bdd existent | **[IA] Feature** (ia_back + neo_ia) |
| Tout a creer from scratch | **[IA] Feature** (complet) |
| Impossible de trancher apres analyse | **[IA] A CLASSER** |

## Etape 2f — Analyse technique profonde

### Si BUG — Localiser la source

1. Dans la **trace Langfuse**, identifier l'observation qui a echoue ou donne le mauvais resultat
2. Dans **neo_ia** (`neo_ia/packages/<app>/`), identifier :
   - Le tool qui a ete appele
   - Le prompt de l'agent
   - La config du retrieval (NeoDoc) ou du graph (NeoChat)
3. Si le bug vient d'un endpoint, remonter dans **ia_back** (`ia_back/src/`)
4. Si le bug vient de la donnee, remonter dans **bdd** (fonctions PG)

Lister precisement les fichiers impliques dans le commentaire Jira.

### Si [IA] FEATURE — Proposer la solution au bon niveau

La verification a deja ete faite a l'etape 2d. Selon le niveau ou on s'est arrete, proposer :

**Niveau 0 — Solution purement neo_ia (pas besoin d'ia_back)**
Exemples : ajouter une source web, modifier le prompt, changer le routing, connecter un tool existant.
→ Lister les fichiers neo_ia a modifier (config agent, classify.py, state.py, prompts)
→ Ne PAS chercher dans ia_back ni bdd

**Niveau 1 — Creer tool neo_ia, endpoint ia_back EXISTE**
→ Proposer quel tool creer, dans quel package, connecte a quel agent
→ Ne PAS chercher dans bdd

**Niveau 2 — Creer endpoint ia_back + tool neo_ia, fonctions bdd EXISTENT**
→ Lister les fonctions bdd comme **reference** (logique metier a refactorer en TS)
→ Proposer quel endpoint creer dans ia_back, puis quel tool dans neo_ia

**Niveau 3 — Tout creer from scratch**
→ Proposer la logique metier a implementer dans ia_back, quel endpoint, quel tool

Dans le commentaire Jira, ecrire precisement a quel niveau on est et ce qu'il faut creer.

## Etape 2g — VERIFIER LES DOUBLONS (OBLIGATOIRE)

**Avant de creer un ticket**, chercher dans Jira **projet N2** (sous le parent N2-109957) si un ticket similaire existe deja — **sur TOUS les etats** (A specifier, En cours, Resolu, Ferme, etc.). Un ticket deja ferme peut indiquer une regression ou un feedback recurrent.

```
Rechercher dans le projet N2 sous le parent N2-109957 avec :
- Meme type de ticket ([IA] Bug, [IA] Feature, [IA] A CLASSER)
- Meme agent concerne (ex: support, neodoc)
- Meme domaine metier ou meme probleme technique
- TOUS les etats confondus
```

**Regles de deduplication :**

| Situation | Action |
|-----------|--------|
| Ticket existe avec meme trace_id deja reference | Pas de doublon — feedback deja analyse, juste marquer traite |
| Ticket ouvert avec meme probleme | **Ajouter un commentaire** au ticket existant, NE PAS creer |
| Ticket deja ferme/resolu avec meme probleme | **Ajouter un commentaire** signalant une potentielle regression ou un feedback recurrent, NE PAS creer |
| Aucun ticket similaire | **Creer un nouveau ticket** |

**Commentaire a ajouter sur un ticket existant** (cas doublon) :

```
## Feedback similaire recu

**Date:** <feedback_date_creation>
**Feedback:** "<commentaire utilisateur>"
**Agent:** <nom_agent> | **Client:** <client_id>
**Trace:** <trace_id> | **Session:** <thread_id>

Ce feedback confirme le probleme deja identifie dans ce ticket.
Nombre de feedbacks similaires sur ce ticket : <compter les precedents commentaires>
```

## Etape 2h — Creer le ticket Jira (ou commenter le doublon)

### Si nouveau ticket

Creer dans le projet **N2** (Neoteem) via le connecteur Jira :

- **Parent** : `N2-109957` ([IA] Parent) — OBLIGATOIRE sur tous les tickets
- **Type** : `[IA] Bug`, `[IA] Feature`, ou `[IA] A CLASSER`
- **Etat initial** : `A specifier`
- **Titre** : resume court du probleme (max 80 chars)
- **Description** : utiliser le template adapte (voir [references/jira-comment-templates.md](references/jira-comment-templates.md))

Le commentaire Jira est le **livrable principal**. Il doit etre :
1. **Comprehensible par l'equipe** — pour qu'ils puissent valider ou rejeter
2. **Exploitable par Claude Code** — pour qu'il puisse developper ensuite (chemins fichiers precis, fonctions a creer)

### Si doublon

Ajouter le commentaire "Feedback similaire recu" sur le ticket existant, sans creer de nouveau ticket.

## Etape 2i — Marquer le feedback comme traite

```
Tool: mark_feedback_processed
Args: { "feedback_ids": ["<feedback_id>"] }
```

A faire dans tous les cas : nouveau ticket, commentaire sur doublon, ou feedback ignore.

## Gotchas

- **Feedbacks positifs** : par defaut on ne traite que les negatifs. Si un positif a une suggestion interessante, le signaler sans creer de ticket.
- **Trace ID null** : analyser uniquement via `feedback_messages` et `feedback_exchange`. Mentionner dans le ticket que la trace n'est pas disponible.
- **Session longue** : si > 20 traces, se concentrer sur les 3-5 autour du feedback.
- **Ne pas traiter les feedbacks sans substance** : si `feedback_commentaire` est null ET `feedback_messages` ne montre pas de probleme evident, classifier en `[IA] A CLASSER`.
- **[IA] Feature avec endpoint existant** : si l'endpoint existe dans ia_back mais n'est pas utilise par neo_ia, c'est un `[IA] Bug` (tool manquant ou mal configure), pas une Feature.
- **Parent obligatoire** : TOUS les tickets doivent avoir `N2-109957` ([IA] Parent) comme parent. Aucune exception.

## Apprentissage

Apres chaque session de triage, noter ici les patterns recurrents :
- Types de bugs frequents (ex: mauvais retrieval, hallucination sur tel domaine)
- Agents les plus concernes
- Clients avec le plus de feedbacks
- Evolutions recurrentes (demandes qui reviennent souvent)
