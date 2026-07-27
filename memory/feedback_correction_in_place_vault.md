---
name: correction-in-place-vault
description: Corriger une claim périmée dans une note vault = réécrire le CORPS en place, jamais bannière AMENDE + texte périmé conservé + addendum en fin de note
metadata:
  type: feedback
---

Consigne Raphael (27 juillet 2026, sweep anti-drift) : « je veux que tu modifies directement les notes dedans, pas que tu fasses un document mis à jour, parce que sinon tu vas mal les lire ».

**Why :** le pattern bannière-AMENDE-en-tête + texte périmé conservé + AJOUT correctif en fin de note laisse la claim fausse dans le corps. Un agent qui lit la note (ou une section via read_section) peut consommer la claim périmée avant d'atteindre la correction — le correctif en couches produit des lectures fausses.

**How to apply :**
- Claim périmée dans une canonique → **réécrire la phrase/section en place** (update_note MCP avec contenu complet corrigé). La traçabilité du « pourquoi » vit dans le CHANGELOG vault + Knowledge/critiques, pas dans le corps de la note.
- Les sections AJOUT datées restent OK pour du contenu **additif** (fait nouveau daté qui ne contredit rien au-dessus) — jamais pour corriger une claim existante.
- Les archives (Knowledge/erreurs|critiques|tests, CHANGELOG, log, notes changelog datées) restent append-only : l'historique ne se réécrit pas.
- Attention update_note = remplacement TOTAL : toujours avoir lu la note EN ENTIER avant, jamais de reconstruction depuis une lecture partielle (risque de perte silencieuse).

Cf [[feedback_zero_dette_technique]] (nettoyage complet immédiat) — même esprit appliqué au vault.
