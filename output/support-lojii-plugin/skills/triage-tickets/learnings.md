# Learnings — Corrections de classification

Ce fichier est mis à jour automatiquement pendant les sessions `/analyse` quand une classification est corrigée.

**Lire ce fichier avant toute classification** pour éviter de répéter les mêmes erreurs.
Appliquer les patterns listés ici en priorité sur les définitions générales du SKILL.md.

## Format des entrées

`[YYYY-MM-DD] | [Ticket] | [Classe Claude] → [Classe correcte] | [Pattern à retenir]`

---

## Apprentissages

[2026-04-27] | (cas remonté par équipe) | Bug → Support | Message d'erreur "ce numéro de facture existe déjà" = garde métier, pas bug. La facture existait réellement en base. RÈGLE : quand le message d'erreur est descriptif (existe déjà, doublon, format invalide, champ obligatoire), TOUJOURS vérifier dans LOJII si le message dit vrai AVANT de classifier. Si vrai → Support (le client tente une action invalide), pas Bug.

[2026-04-27] | (règle globale) | Toutes classifications | RÈGLE : chaque note interne DOIT contenir une section '📋 Étapes de vérification / actions dans LOJII' avec des étapes concrètes, numérotées, spécifiques au ticket. Bug = étapes reproduction. Support = vérifications config/état. SR = étapes intervention. Jamais vide. Toujours chemin menu LOJII + actions précises.
