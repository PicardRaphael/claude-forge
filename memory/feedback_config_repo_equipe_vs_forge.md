---
name: config-repo-equipe-vs-forge
description: Configurer un repo d'ÉQUIPE PARTAGÉ depuis forge ≠ transplanter la machinerie forge. Skills auto-portantes + hooks non-bloquants.
metadata:
  type: feedback
---

Quand Raphael demande « configure / propose la config CC » sur un repo **partagé par une équipe** (signaux : nombreuses PRs, Bitbucket/remote, refs d'autres devs type `david-beaufour`, CI), la doctrine forge ne se copie PAS telle quelle — pas par dogme, par mécanique : les hooks et fichiers `.claude/` versionnés s'exécutent chez CHAQUE dev qui ouvre Claude Code sur le repo.

**Pièges concrets identifiés (migration_script, 24 juin 2026) :**
- **Wikilinks `[[vault]]` dans les skills** → pointent vers le vault forge-brain LOCAL de Raphael. Chez un autre dev ou en CI : ne résolvent rien → contenu mort, skill cassée. Idem MCP `forge-brain` (branché que chez Raphael).
- **`delegate-guard`** → bloque l'édition de tout `.md`/`SKILL.md`/`CLAUDE.md` en pointant vers les skills créatrices forge (`skill-creator`...) que les autres devs N'ONT PAS → ils sont coincés sans porte de sortie.
- **Chemins machine** hardcodés dans les sources legacy (`C:/tmp/`, `C:/Data/`, `~/.bashrc`, `~/.claude/projects/C--Users-<autre-dev>/`) → à purger lors de la conversion.

**Why :** un hook versionné = contrat imposé à toute l'équipe ; une skill avec dépendance forge = livrable cassé pour qui n'a pas forge. « Le truc parfait » sur un repo d'équipe = bien dimensionné + portable, pas un max de machinerie forge.

**How to apply :**
1. Skills **auto-portantes** : référencer les docs DU REPO en chemins relatifs Markdown (`CONVENTIONS_NOMMAGE.md`, `vera/VERA.md`...), JAMAIS de wikilink vault ni d'appel MCP forge-brain.
2. Hooks = uniquement ceux **utiles à toute l'équipe** (lint/encoding/sécu), **non-bloquants** (warning/fail-open, jamais `exit 2` qui coince un dev). Pas de delegate-guard. Raphael a explicitement redemandé « pas trop bloquant » (24 juin).
3. Structure forge (memory/, rules, agents avec couleur/effort/permissionMode, CLAUDE.md enrichi) OK — c'est le CONTENU qui doit être portable, pas la forme.
4. Convertir la valeur des slash commands legacy en skills AVANT de supprimer le dossier `commands/` (« commands c'est nul » = le format, pas le contenu = doctrine métier précieuse).

Distinct de [[plugin-vs-skill-anatomie]] (distribuer un setup = plugin) : ici c'est la PORTABILITÉ du contenu généré, pas le packaging. Si ce pattern récidive (2-3 repos équipe), promouvoir en note canonique vault et enrichir [[methode-analyser-repo]] avec une branche « repo équipe vs repo perso/forge ».
