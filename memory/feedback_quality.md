---
name: deep-analysis-no-shortcuts
description: Toujours lire les fichiers en entier (Read complet, pas head/limit), analyser chaque section sans rush
type: feedback
---

Jamais de raccourcis sur l'analyse de fichiers massifs. Paginer en morceaux (~500 lignes) mais TOUT couvrir jusqu'a la derniere ligne.

**Why:** Sur neoteem-brain, un agent a lu seulement les 80 premieres lignes de fonctions SQL de 1822 lignes avec `head 80`, ratant les sections lots, compta, historique, locataires, factures, contrats, membres CS. Le fichier genere etait incomplet.

**How to apply:**
- Paginer avec `Read` (`offset`/`limit`) ou `head`/`tail` — en morceaux de ~500 lignes max pour gerer le contexte
- MAIS toujours continuer jusqu'a la derniere ligne — ne jamais s'arreter au milieu
- Si un dossier contient plusieurs fichiers, les lire UN PAR UN completement
- Documenter chaque section trouvee (UUID, calculs, erreurs) au fur et a mesure
- Prendre son temps : 5 passes completes > 1 passe incomplete
- Ne JAMAIS dire "c'est massif, je ne peux pas tout lire" — paginer et couvrir
