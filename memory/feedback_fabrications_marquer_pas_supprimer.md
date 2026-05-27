---
name: fabrications-vault-marquer-pas-supprimer-aveuglement
description: "Quand un audit détecte des claims 'fabriqués' (0 source externe accessible), marquer ⚠️ 'à confirmer livestream/source primaire' plutôt que supprimer. La source peut exister hors WebFetch (livestream non transcrit, doc interne)."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c6c61616-50af-4cd8-8b0b-68932b824064
---

Quand un sub-agent audit détecte un claim "fabriqué" (verbatim que aucune source externe accessible ne mentionne), 2 cas possibles :

**Cas A — vraie fabrication** : claim inventé par session précédente, aucun support réel.
**Cas B — source primaire inaccessible** : livestream YouTube non transcrit, doc interne, podcast paywall, slide deck non public.

Distinction impossible à faire en audit. Donc :

**Action correcte** :
1. NE PAS supprimer aveuglément
2. Marquer le claim avec ⚠️ + note explicite : *"À confirmer livestream/source X — non trouvé dans sources externes accessibles (audit YYYY-MM-DD)"*
3. Documenter dans note erreur la liste des sources externes vérifiées (Every podcast, MIT Tech Review, Fortune, etc.)
4. Laisser à Raphael / future session le soin de confirmer ou supprimer

**Why** : Sur audit 07 (23 mai 2026), 3 fabrications détectées (Mercado Libre 23K/500K/9K, Oscar Mowen, Dreaming specs `dreaming-2026-04-21`). Toutes possibles si vues dans livestream YouTube CwC London (transcription post-event non publiée au 23 mai). Supprimer aveuglément = perdre une info potentiellement valable. WebFetch ne couvre pas tout l'internet.

**How to apply** : Pour tout claim "0 source externe" lors d'un audit. Adapter formulation : *"⚠️ Non vérifiable via [sources externes vérifiées], à confirmer [source primaire candidate]"*.

**Anti-pattern** : "❌ FAUX, supprimer" sans avoir vérifié toutes les sources primaires possibles (livestream, transcript, slide deck).

Lié : [[feedback_audit_thematique_methode]] — méthode sub-agents clusters. Cette règle = nuance sur la phase D (corrections).
