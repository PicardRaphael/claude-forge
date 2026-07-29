---
name: localiser-repos-avant-workflow-multi-repo
description: Avant audit/workflow multi-repo, vérifier que les repos cibles existent SUR la machine courante — la doctrine les suppose présents, ce n'est pas garanti
trigger: multi-repo, fan-out, audit, tous les repos
metadata:
  type: feedback
---

Avant de lancer un audit ou un workflow fan-out multi-repo (forge + ia_back + neo_ia + …), **localiser empiriquement chaque repo cible sur la machine courante** (`ls */.claude` ou demander le chemin) AVANT de scoper/lancer. Ne pas supposer qu'ils sont sous `Documents/` ni qu'ils sont clonés ici.

**Why:** 29 mai 2026, scope d'un audit Dynamic Workflows sur les 3 repos IA : ia_back et neo_ia introuvables sous `Documents/`. Cause réelle confirmée par Raphael : ils sont sous `Documents\neot-v2\` (`neot-v2\neo_ia`, `neot-v2\ia_back`), pas à la racine. La doctrine forge liste ces repos comme acquis (cf [[decision-memoire-dans-le-repo]]) mais leur emplacement réel n'était documenté nulle part. Lancer un workflow (centaines d'agents, grosse conso) sur des chemins inexistants = gaspillage pur. Instance multi-repo de [[feedback_brief_premisse_fausse_verifier_avant_executer]].

**How to apply:** Étape 0 de tout dispatch multi-repo : `ls */.claude` sous chaque racine candidate OU demander les chemins exacts à Raphael. Si un repo manque → STOP + remonter (options : chemin, piloter sur le repo dispo d'abord, substituer). Ne jamais improviser un audit sur un chemin non vérifié. Cf aussi [[feedback_git_C_pas_cd]] (multi-repo).
