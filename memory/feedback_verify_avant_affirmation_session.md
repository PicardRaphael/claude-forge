---
name: verify-empirique-avant-affirmation-session
description: "Avant d'affirmer \"X parce que Y\" sur changement filesystem/repo, vérifier empiriquement (git log/blame/diff). User questionne souvent \"pourquoi ?\" → ne pas inventer la raison"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e91e446c-e32c-4517-ab41-e1e4c5555314
---

# Vérifier empiriquement AVANT d'affirmer la raison d'un changement

## La règle

Quand on présente un changement filesystem/repo (delete file, rename, fusion agents) et qu'on affirme une raison ("audit X mai", "fusion intentionnelle", "déprécié"), **vérifier empiriquement AVANT** :

- `git log --diff-filter=D -- <file>` pour les deletes
- `git log --follow` pour les renames
- `git blame` pour les modifs
- `ls -la` pour dates filesystem si pas commité

Sinon = paraphrase non-vérifiée (anti-pattern documenté [[feedback_tweet_hype_paraphrase_pattern]]).

## Why

Validé 26 mai 2026 session forge commits multi-repos :
- J'ai affirmé "audit 25 mai forge a supprimé code-reviewer + security-reviewer pour fusion en reviewer.md"
- User a questionné : "pourquoi suppression code reviewer ? security reviewer rexplique"
- Vérification empirique : git log montrait seulement commit jan 2026 (création), pas de commit suppression
- Réalité : delete dans working tree NON commité, créé par moi-même ou autre session récente
- Bonne réflexe user de demander avant commit → évité de propager fausse justification dans commit message

## How to apply

Avant d'affirmer "ce changement vient de [raison]" :

1. Si commité : `git log --diff-filter=D --summary -- <path>` ou `git show <sha>`
2. Si working tree : `git status` + `ls -la` pour date filesystem
3. Si pattern fusion : grep le nouveau fichier pour voir s'il contient bien les responsabilités des supprimés
4. Si user demande "pourquoi ?" : **ne pas inventer**, dire "je vérifie empiriquement"
5. Reformuler avec verbe d'évidence : "déduction empirique du diff/contenu", pas "audit X mai a décidé"

## Anti-patterns à éviter

- ❌ Affirmer "audit forge 25 mai a fusionné X" sans avoir le commit en main
- ❌ Inventer justification cohérente pour combler ignorance
- ❌ Reprendre une affirmation passée sans re-vérifier (mémoire session ≠ source de vérité)
- ❌ Mettre la justification inventée dans le commit message → propagation erreur

## Pattern positif à reconnaître

Quand user dit "pourquoi ?" ou "rexplique" :
- = Signal qu'il sent une affirmation faible
- = Bon réflexe défense contre paraphrase non-vérifiée
- Toujours répondre par **vérification empirique + correction si différence**, pas par re-affirmation

## Wikilinks

- [[feedback_tweet_hype_paraphrase_pattern]] — paraphrase non-vérifiée
- [[feedback_gotchas_line_numbers_verifies]] — line numbers verifies grep
- [[feedback_audit_claims_after_brief]] — claims sub-agent verifies
- [[feedback_verify_exhaustive_claims]] — grep avant claim exhaustive
