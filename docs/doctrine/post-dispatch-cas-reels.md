# Vérifier un CONSTAT d'audit — cas réels et raisonnement long

Référence historique de la règle de vérification post-dispatch, désormais condensée dans `AGENTS.md` et la skill `auditor-empirical-verify`. **Non chargée en contexte** : lue seulement pour comprendre les cas réels.

## Pourquoi c'est non négociable sur un audit de repo

Un audit produit 20 à 50 findings d'un coup, et son autorité apparente est haute : rapport structuré, `file:line`, ton assuré. Relayer sans mesurer, c'est propager des faux **à l'échelle** — et si l'audit débouche sur un plan de nettoyage, chaque faux devient une suppression.

La mécanique de l'erreur : un agent d'audit rapporte ce qu'il a **déduit** de ce qu'il a lu. Entre le fichier et le verdict il y a une inférence, et c'est l'inférence qui casse — pas la lecture. D'où la parade : reproduire soi-même la mesure la plus courte qui tranche le verdict.

## Trois cas réels — session du 29 juillet 2026

Mêmes agents, **aucun fichier écrit**, trois faits faux. Aucun des trois n'aurait été attrapé par la checklist « fichiers » : aucun fichier n'était en jeu.

**1. « Chemin mort `Documents/ia_back` »** → le chemin existe, **sur l'autre PC de Raphael**. Le fait mesuré (« absent ici ») était juste ; l'interprétation (« chemin erroné, à corriger ») était fausse. Leçon : un `ls` négatif signifie « absent sur cette machine », pas « chemin faux ».

**2. « Repo fantôme `lojii/neofront` »** → le dossier existe bel et bien. `ls -d neofront/.git` a tranché : ce n'est pas un repo, c'est un **conteneur d'une dizaine de repos indépendants**. Deux erreurs opposées (« n'existe pas » / « est un repo ») corrigées par une seule mesure.

**3. « `git merge *` est en deny global intentionnel »** — écrit dans un feedback depuis mai, rechargé à chaque session. Parse de `settings.json` : **zéro entrée deny**. Une intention rassurante avait été fabriquée pour une garde que personne n'avait jamais lue. Cf `feedback_diagnostic_empirique_avant_affirmer_garde`.

## Le cas du frontmatter « vide »

Audit neo_ia, 27 juillet : deux findings CRITIQUES sur des `tools:` prétendument vides. En réalité une liste YAML multi-lignes (`tools:` suivi de `- Read`) — l'agent l'avait lue comme un champ vide. Contre-vérifier chaque finding bloquant par un `Read` direct avant de le relayer ou d'agir.

Symétriquement, un frontmatter *présent* peut être **cassé** : le motif deux-points-espace dans un scalaire non quoté (`Modes: mode=audit`) lève une `ScannerError` et rend le composant **invisible silencieusement**. 9 composants étaient dans cet état le 29 juillet, dont 7 antérieurs à la session. D'où `check-frontmatter.py` : parser le YAML plutôt que le regarder.

## Ce qui ne se re-vérifie pas

Une opinion de conception (« cette skill gagnerait à être découpée »), une recommandation, un jugement de priorité. Il n'y a pas de fait à mesurer — c'est un avis, à discuter, pas à confirmer. Re-vérifier un avis coûte sans rien trancher.

## Ce qui est mécanisable, et ce qui ne l'est pas

Trois scripts couvrent les findings qui ne demandent aucune interprétation (`check-frontmatter.py`, `check-refs.py`, `check-portability.py`) — détail et chaînage dans la rule.

⚠️ **Portée de `check-refs.py`** : il ne regarde que les citations en **contexte de routage** (« agent `x` », « invoquer `y` », `Skill(z)`). Son silence prouve qu'aucun routage ne pointe vers le vide, pas qu'il n'existe aucune référence morte ailleurs. Un filtre plus large avait produit 108 faux positifs — un outil qui crie 108 fois est ignoré au premier usage.

Le reste n'est pas mécanisable : un script peut vérifier qu'une colonne « Mesure » existe, jamais que la mesure a réellement été faite.
