# Bank de questions — Blocs 3-4-5 (branche CODE)

Questions à poser en 1-2 appels `AskUserQuestion` (batches de 4 max).

---

## Bloc 3 — Inputs / Outputs

Questions à sélectionner selon le contexte :

- **Input** : quelles sont les données d'entrée de chaque itération ? (fichier, ligne BDD, résultat API, variable d'env, stdout d'un outil)
- **Source** : d'où viennent ces données ? (dossier à surveiller, table SQL, queue/topic, webhook, argument CLI)
- **Output** : que produit chaque itération ? (fichier transformé, ligne insérée en BDD, message envoyé, log enrichi)
- **Destination** : où vont ces outputs ? (dossier de sortie, table SQL, topic, API distante, slack/discord)
- **Format** : quel format ? (JSON, CSV, Markdown, binaire, texte brut)
- **Volume** : ordre de grandeur des données ? (N fichiers/jour, N lignes/batch, N appels API/heure)
- **Idempotence** : si le loop tourne deux fois sur le même input, est-ce sûr ? Que se passe-t-il ?

---

## Bloc 4 — Stack et outils

Questions à sélectionner selon le contexte :

- **Langage / runtime** : Python, Bun/Node, Bash, autre ?
- **Outils CLI** : quels outils doivent être disponibles ? (`git`, `jq`, `curl`, `psql`, `ffmpeg`, etc.)
- **APIs / services** : quels services externes sont appelés ? (OpenAI, Anthropic, S3, Postgres, Redis, etc.)
- **Auth** : comment les credentials sont-ils gérés ? (env vars, secrets manager, fichier `.env`)
- **Repo cible** : dans quel repo le code du loop vivra-t-il ?
- **Dossier cible** : où dans le repo ? (`scripts/`, `cron/`, `workers/`, `jobs/`, autre)
- **Dépendances** : y a-t-il des dépendances npm/pip à ajouter ?
- **Tests** : faut-il un test unitaire / un dry-run mode ?
- **Scheduler existant** : y a-t-il déjà un scheduler (cron system, Task Scheduler Windows, GitHub Actions, Celery, etc.) à utiliser ?

---

## Bloc 5 — Gestion d'erreur et résilience

Questions à sélectionner selon le contexte :

- **Retry** : en cas d'erreur transitoire, faut-il réessayer ? Combien de fois ? Avec quel délai ? (exponentiel, fixe)
- **Erreur fatale vs non-fatale** : quelles erreurs arrêtent le loop ? Lesquelles sont ignorées/loggées et le loop continue ?
- **État persistant** : faut-il mémoriser la progression entre deux runs ? (fichier d'état, table SQL, redis)
- **Partial failure** : si le loop tourne sur 100 items et échoue au 37e, que faire ? (reprendre au 38e, tout recommencer, rapport partiel)
- **Dead letter** : où vont les items qui ont échoué ? (dossier `_failed/`, table SQL, alerte manuelle)
- **Timeout** : y a-t-il un timeout par itération ? Global ?
- **Concurrence** : le loop peut-il tourner en plusieurs instances simultanées ? Faut-il un verrou ?
- **Alerting** : qui est notifié et comment si le loop crash ? (email, Slack, Discord webhook, PagerDuty)

---

## Notes pour la spec

Dans la SPEC-loop générée, la section "Stack / Implémentation" doit inclure :
- Le langage + outils principaux
- Le mode de déclenchement (cron expression si planifié)
- La gestion d'erreur choisie (retry policy, dead letter)
- Le path exact dans le repo
- L'idempotence : OUI / NON / PARTIELLE (avec explication)
