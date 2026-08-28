# Session capture — contrat Raphaël

Ce pipeline transforme les informations explicites de la conversation courante
en deltas contrôlés. Le vault est la source canonique ; la mémoire locale sert
uniquement d'adaptateur, d'incident empirique ou de contexte temporaire.

## Classification

| Classe | Destination | Politique |
|---|---|---|
| `EXPLICIT_FACT` | `Raphael-Picard` ou casquette adaptée | appliquer si durable et non sensible |
| `EXPLICIT_PREFERENCE` | profil, casquette ou projet selon portée | remplacer l'état actif si nécessaire |
| `HYPOTHESIS` | batch « À confirmer » | ne jamais écrire comme vérité |
| `PROJECT_DECISION` | foyer projet ou décision reliée | appliquer si le choix est explicitement acté |
| `VOLATILE_CONTEXT` | `memory/project_*.md` | TTL court, jamais le profil |
| `SENSITIVE` | aucune par défaut | « mémorise ceci » explicite requis |
| `NOOP` | aucune | banal, déjà couvert ou sans valeur future |

Sont sensibles par défaut : santé, finances, secrets, identifiants, localisation
précise et nouvelles données familiales. Une donnée déjà présente n'autorise pas
l'accumulation automatique d'autres données de même nature.

## Choisir le foyer personnel

1. Lire `Raphael-Picard` entièrement.
2. Si l'information concerne une casquette durable existante, lire aussi cette
   note et y placer le détail ; garder seulement le résumé utile dans le profil.
3. Créer une nouvelle casquette uniquement lorsqu'un domaine durable autonome
   émerge. Ne jamais créer une note pour une préférence isolée.
4. Le fichier `memory/user_raphael_profile.md` reste un pointeur mince.

## Preuve et idempotence

Chaque delta accepté porte une provenance concise : date, `explicit` ou
`confirmed`, et prédicat. Enrichir/corriger la bonne section, sans journaliser la
conversation. Une préférence contradictoire plus récente remplace l'ancienne.

« Oublie X » révoque X dans chaque foyer actif concerné. Une suppression de note
entière reste destructive et demande une autorisation séparée.

## Autorisation

L'invocation de `/done`, « retiens/mémorise ceci » ou une demande explicite de
création de projet autorise les deltas non sensibles nécessaires dans les foyers
existants et la création du foyer clairement demandé. Les hypothèses et données
sensibles restent soumises à validation.

En dehors de ces signaux, préparer des candidats sans interrompre la conversation
et sans écrire silencieusement depuis un hook.

## Vérification

1. Lire chaque cible entière avant mutation.
2. Vérifier doublon, contradiction, portée, sensibilité et durabilité.
3. Appliquer le delta minimal via MCP pour le vault ou par patch versionné pour
   la mémoire repo temporaire.
4. Relire chaque cible et vérifier l'absence de l'ancien état contradictoire.
5. Rapporter : appliqué, proposé, ignoré et révoqué.
