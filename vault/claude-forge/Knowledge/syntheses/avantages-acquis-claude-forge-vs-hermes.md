---
titre: "Avantages acquis claude-forge vs Hermes — selling points"
resume: "Avantages prouvés de claude-forge sur les axes prioritaires mémoire/apprentissage/compounding face à Hermes Agent (169k stars). Matière pour comm externe LinkedIn et Anthropic Partner Network."
aliases:
  - "avantages claude-forge hermes"
  - "selling points forge"
  - "forge vs hermes avantages"
  - "claude-forge superiority memory"
  - "comm externe forge"
derniere-maj: 2026-05-27
tags:
  - "#type/synthese"
  - "#projet/claude-forge"
  - "#concurrent/hermes"
---

# Avantages acquis claude-forge vs Hermes — selling points

Lien : [[phase-4-comparaison-hermes-roadmap]], [[adr-gaps-hermes-declines-phase-4]]

Comparaison sur code source réel (Phase 4, 2026-05-27). Hermes Agent = 169 296 stars, agent autonome. claude-forge = studio mémoire/apprentissage synchrone, 1 auteur.

## Thèse

Sur la **mémoire structurée, la conformité par construction et la traçabilité de l'apprentissage**, claude-forge est strictement supérieur à Hermes — parce qu'il optimise le contrôle et la structure, là où Hermes optimise l'automatisation autonome.

## Selling points forts (vérifiés code)

### 1. Mémoire cross-projet structurée (vs MEMORY.md plat)

- claude-forge : vault 417 notes, 2717 wikilinks, 2462 aliases, 3 layers (raw/wiki/SCHEMA), MCP forge-brain FTS5 BM25 (file_stem:10 / aliases:8 / content:1), ontologie 07 dossiers, navigation active.
- Hermes : `MEMORY.md` + `USER.md` plats, limités à 2200 / 1375 caractères, scope global par profil, pas d'ID, pas de hiérarchie. Holographic SQLite optionnel mais SNR dégrade au-delà de ~256 faits/catégorie sans purge auto.
- Argument : une mémoire de connaissance EST un graphe navigable, pas un fichier texte de 2 Ko.

### 2. Conformité par construction — delegate-guard bloquant

- claude-forge : `delegate-guard.py` BLOQUE (exit 2) l'édition directe des composants qui doivent passer par un créateur dédié. 207 tests verts, ratio adverse ≥3:1 sur les hooks sécu.
- Hermes : AUCUN équivalent. `skills_guard` ne couvre que l'install externe. `file_safety` est explicitement "NOT a security boundary" (le terminal contourne tout).
- Argument : "conformité par construction" est prouvable par le code, pas par discipline.

### 3. Doctrine versionnée + anti-drift

- claude-forge : CLAUDE.md v3.3 datée, [[methode-pivoter-doctrine]] (checklist 5 étapes), skill pivot-check (détection drift résiduel), CHANGELOG vault narratif.
- Hermes : AGENTS.md avec politiques datées narratives ("Rule, Teknium, May 2026") mais pas de version structurée, pas de changelog de doctrine, pas d'outil anti-drift.

### 4. Capitalisation décisionnelle tracée (règle + pourquoi + déclencheur)

- claude-forge : feedback files + Knowledge/raisonnements/ + reasoning-cache capturent la règle ("quand faire X"), le POURQUOI, et le déclencheur de réactivation. Versionné git.
- Hermes : le background review cible "When X do Y rules" mais en langue naturelle libre dans SKILL.md, sans le pourquoi, avec risque de sur-généralisation. Overwrite atomique sans historique git.

### 5. Humain dans la boucle by design

- claude-forge : Raphael valide avant écriture (learning-reminder advisory + capitalisation manuelle réfléchie). Cohérent use case synchrone.
- Hermes : background review écrit automatiquement sans validation, notification après coup, pas de diff. Cohérent use case autonome mais incorrectible en amont.
- Argument : pour un studio personnel synchrone, le contrôle et la correctibilité battent la couverture automatique.

### 6. Honnêteté méthodologique prouvée

- claude-forge : 2 bugs caractérisés ET fixés (Phase 2), dette tracée avec déclencheurs, ratio tests adverses ≥3:1, 207 tests verts, 0 régression sur 3 phases (+130%).
- Hermes : 14 224 issues ouvertes, pas de trace publique de bugs caractérisés.

## Où Hermes gagne (honnêteté)

- Recherche dans les transcripts de sessions passées (`session_search`) — gap réel pertinent, à combler (plan A1).
- Lifecycle/usage tracking des skills (curator) — gap réel, P2.
- Vitesse de capitalisation (background review automatique) — couverture supérieure, à importer sans l'autonomie (plan A3).
- Ambition self-improvement (GEPA) — mais POC hors runtime, décliné.

## Usage comm externe

Sélection pour LinkedIn / Anthropic Partner Network : points 1, 2, 4 (mémoire graphe, delegate-guard bloquant, capitalisation tracée). Ce sont les différenciateurs vérifiables et compréhensibles par un public technique, face à un concurrent à 169k stars.
