# Session capture — contrat Raphaël

Ce pipeline est distinct de la veille. Il transforme seulement les informations
de la conversation courante en mémoire relationnelle utile.

## Classification

| Classe | Destination | Politique |
|---|---|---|
| `EXPLICIT_FACT` | `memory/user_raphael_profile.md` | mise à jour si durable et non sensible |
| `EXPLICIT_PREFERENCE` | profil, section « Comment travailler » | mise à jour si elle change la collaboration |
| `HYPOTHESIS` | batch « À confirmer » | jamais écrite comme vérité |
| `VOLATILE_CONTEXT` | `memory/project_*.md` ou context note | TTL court, pas le profil |
| `SENSITIVE` | aucune par défaut | demande explicite « mémorise ceci » requise |
| `NOOP` | aucune | déjà couvert, banal ou sans valeur future |

Sont sensibles par défaut : santé, finances, secrets, identifiants, localisation
précise et nouvelles données familiales. Une donnée déjà présente n'autorise pas
l'accumulation automatique d'autres données de même nature.

## Preuve et idempotence

Chaque delta accepté porte une provenance courte : date de session, `explicit`
ou `confirmed`, et prédicat concerné. L'identifiant logique est
`schema_version + session_date + event_id + predicate + normalized_object`.

- Enrichir ou corriger une puce existante ; ne pas créer un second profil.
- Une préférence plus récente explicitement contradictoire remplace l'état actif.
- Garder seulement la provenance nécessaire, pas des extraits intimes du chat.
- Permettre la révocation : « oublie X » retire X du profil versionné et de son index.

## Autorisation

L'invocation explicite de `/done` autorise `profile-apply` pour les faits et
préférences explicites, durables et non sensibles. Les hypothèses, nouvelles
données sensibles et nouveaux fichiers restent proposés en un batch.

En dehors de `/done`, une session peut préparer des candidats, mais ne doit pas
interrompre la conversation ni utiliser un hook agentique pour décider quoi
mémoriser. La règle `memory-discipline.md` porte le routage ; le hook éventuel
reste un signal déterministe non bloquant.

## Vérification

1. Relire le profil et la mémoire existante avant mutation.
2. Vérifier doublon, contradiction, sensibilité et durabilité.
3. Appliquer un delta minimal au bon foyer.
4. Relire le profil et confirmer que l'ancienne préférence contradictoire n'est
   plus active.
5. Rapporter : appliqué, proposé, ignoré, révoqué.
