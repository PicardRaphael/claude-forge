---
name: doublons-vault-marquer-canonique-pas-supprimer
description: "Doublons de fiches vault leaders cross-dossiers : marquer 'canonique = X / doublon de Y' plutôt que supprimer. Préserve les backlinks Obsidian [[Name]] et permet à Raphael de décider plus tard."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c6c61616-50af-4cd8-8b0b-68932b824064
---

Quand un audit vault détecte une fiche doublonnée dans 2+ dossiers (ex: Harrison Chase dans `05-Leaders/agents/` ET `05-Leaders/rag/`) :

**Action correcte** :
1. Identifier le dossier du **scope primaire** du leader (Harrison Chase = LangChain/LangGraph → agents/)
2. Marquer la fiche canonique avec un encart en haut : `## ⚠️ FICHE DOUBLON — voir canonique [[Name]] (dossier/)`
3. Garder le contenu spécifique au scope secondaire (RAG pour Chase)
4. NE PAS supprimer la fiche doublon

**Why** : Les wikilinks Obsidian `[[Harrison Chase]]` résolvent vers la première fiche trouvée. Si on supprime la fiche secondaire, les backlinks `[[05-Leaders/rag/Harrison Chase]]` (chemin explicite) cassent. Les backlinks `[[Harrison Chase]]` (alias) continuent à fonctionner via aliases, mais la perte de contenu domaine-spécifique appauvrit le vault.

**How to apply** : Sur tout audit vault qui détecte des doublons leaders. Décidé audit thème 07 (23 mai 2026) sur 4 cas : Harrison Chase, Jerry Liu, Ethan Mollick, Hashimoto. Confirmé par advisor() : "fusion vers dossier primaire" en marquage canonique vs doublon = la bonne approche, pas suppression.

Lié : [[feedback_single_source_truth_vault_canonique]] — règles universelles vivent dans canonique. Adaptation ici : fiches doublons restent mais pointent explicitement vers canonique.
