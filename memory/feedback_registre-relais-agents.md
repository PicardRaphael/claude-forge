---
name: registre-relais-agents
description: HYPOTHÈSE (non validée) — pour une tâche multi-agent, tenir un registre léger « recherche/lecture X faite → artefact Y », 1 ligne par opération coûteuse, consulté AVANT toute op coûteuse pour éviter de la refaire. Pointeur jamais contenu. À valider sur 2-3 cas avant promotion vault.
metadata:
  type: feedback
---

**Statut : hypothèse à valider sur 2-3 cas réels** (workflow de promotion : 1 incident isolé ≠ canonique ; cf [[memory-discipline]]).

**L'idée :** quand N agents travaillent une même tâche, la session principale tient un registre minimal de ce qui a déjà été fait — une ligne par opération **coûteuse** (recherche vault/web, lecture de gros fichier, audit, requête DB) : `op + cible → artefact où est le résultat`. Tout agent consulte ce registre **avant** de lancer une op coûteuse ; s'il y est déjà, il lit l'artefact au lieu de refaire. Jamais le contenu, seulement le pointeur (discipline tokens).

**Why :** matérialise les fuites #2/#3 de la note-hub [[relais-inter-agents-fiable]]. Le « niveau expert » de [[pattern-mcp-brief-then-direct]] l'évoque (« kit contexte réutilisable ») mais 0 cas éprouvé dans forge → hypothèse, pas doctrine.

**How to apply :** registre tenu à la main par la session principale (dans son fil ou le dossier `TODO/feature-X/`). *Comment* le construire — pointeur manuel vs fichier `registre.md` formaté — se tranche au **premier usage réel**, pas d'avance (ne pas formaliser un artefact avant d'en avoir prouvé le gain).

**Distinct de** [[idee-compounding-retroactif]] : celui-ci cherche dans les *transcripts passés* (session_search, mémoire cross-session) ; le registre est le scratchpad *de la tâche en cours*, vivant le temps de la tâche puis jeté.
