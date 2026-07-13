---
name: dont-prefill-files
description: Ne pas pré-créer des fichiers que les agents doivent générer au fil du travail.
type: feedback
---

Ne jamais pré-remplir ou scaffolder des fichiers que les agents vont créer naturellement pendant le workflow.

**Why:** L'utilisateur a refusé la création de `doc/migration-tracker.md` pré-rempli — c'est aux agents (via la skill `migration-status`) de le créer quand une migration est effectivement complétée.

**How to apply:** Ne créer que les fichiers de configuration (.claude/, settings.json, hooks). Les fichiers de contenu (doc/, src/) sont créés par les agents au moment où ils en ont besoin. Un fichier vide ou placeholder n'a pas de valeur.
