# Langfuse CLI — Reference pour le triage

## Commandes essentielles

```bash
# Recuperer une trace specifique
npx langfuse-cli api traces get <id> --json

# Lister les traces d'une session
npx langfuse-cli api traces list --sessionId <id> --json
# Note : list utilise des flags (--sessionId), get utilise un argument positionnel

# Recuperer une session
npx langfuse-cli api sessions get <id> --json

# Lister les observations (LLM calls, tool calls) d'une trace
npx langfuse-cli api observations-v2s list --traceId <id> --json

# Lister les scores d'une trace
npx langfuse-cli api score-v2s list --traceId <id> --json
```

## Credentials — OBLIGATOIRE avant tout appel

Les credentials Langfuse sont configurees dans les variables d'environnement du projet (`settings.local.json`). Elles sont chargees automatiquement au demarrage de la session. Pas besoin d'export manuel.

Variables utilisees par la CLI :
- `LANGFUSE_PUBLIC_KEY` (pk-lf-...)
- `LANGFUSE_SECRET_KEY` (sk-lf-...)
- `LANGFUSE_HOST` (https://cloud.langfuse.com)

## Analyse d'une trace — Quoi regarder

1. **Input/Output de la trace** : la question user et la reponse finale
2. **Observations enfants** :
   - `GENERATION` = appel LLM (verifier le prompt, la reponse, les tokens)
   - `SPAN` = etape logique (retrieval, tool call, routing)
   - Chercher les observations avec `statusMessage` non vide (erreurs)
3. **Scores** : thumbs, rating, commentaires deja attaches
4. **Metadata** : agent name, model, latency

## Analyse d'une session — Quand remonter

Remonter la session si :
- La trace isolee ne montre pas de probleme evident
- Le feedback dit "depuis le debut ca marche pas"
- L'erreur semble liee a un message precedent (mauvais contexte accumule)

Strategie : lister les traces de la session, lire les 3-5 autour du feedback (par date).

## Tips

- Toujours utiliser `--json` pour un parsing propre
- Preferer `observations-v2s` a `observations` (plus riche)
- Preferer `score-v2s` a `scores` (v1 ne supporte que create/delete)
- `--limit` et `--page` pour la pagination
- `--curl` pour previsualiser la requete HTTP sans l'executer
