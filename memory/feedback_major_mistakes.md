---
name: major-mistakes-to-never-repeat
description: Erreurs majeures faites sur le projet back-refacto. Ne JAMAIS refaire.
type: feedback
originSessionId: a0d051cb-3e6f-429d-9908-b2cfe3295ea9
---
## Erreurs commises et corrections

### 1. Créé un agent CTO orchestrateur
- **Erreur :** Créé un agent CTO qui devait déléguer aux autres agents
- **Pourquoi c'est cassé :** Un subagent ne peut PAS spawner de sub-agents (GitHub #19077, by design). Avec des outils → fait le travail lui-même. Sans outils → ne fonctionne pas.
- **Correction :** La session principale est l'orchestrateur. Rules pour le routing.
- **Leçon :** TOUJOURS vérifier les limitations techniques AVANT de concevoir.

### 2. Mis le routing dans CLAUDE.md
- **Erreur :** Le workflow agents, les tableaux de triage, les compétences CTO étaient dans CLAUDE.md
- **Pourquoi c'est mal :** CLAUDE.md = contexte projet (config, standards, conventions). Le routing et les comportements obligatoires vont dans `.claude/rules/`
- **Correction :** `rules/agent-delegation.md`, `rules/cto-mindset.md`, `rules/skill-navigator.md`, `rules/database-rules.md`
- **Leçon :** Regarder les projets existants de l'utilisateur AVANT de proposer une architecture.

### 3. Pas regardé le projet neo_ia existant
- **Erreur :** J'ai inventé une architecture sans regarder les patterns déjà en place
- **Correction :** neo_ia avait déjà la bonne structure (rules/, agents/, skills/, commands/, hooks/, scripts/)
- **Leçon :** TOUJOURS demander "tu as un projet existant que je peux regarder ?" en début de session.

### 4. Testé 5 fois le CTO au lieu de chercher la vraie solution
- **Erreur :** Retiré Bash → Grep → Read → Glob un par un au lieu de comprendre le problème fondamental
- **Correction :** Rechercher AVANT d'itérer. La doc disait clairement que les subagents ne peuvent pas spawner.
- **Leçon :** Quand un fix ne marche pas, RECHERCHER la cause racine au lieu de bricoler.

**Why:** L'utilisateur a perdu du temps à cause de ces erreurs en cascade. Un expert devrait valider l'architecture avant de construire.

### 5. Utilisé plugin externe au lieu de ses propres skills forge
- **Erreur :** Invoqué `plugin-dev:plugin-structure` qui mentionnait `commands/` (déprécié) au lieu de consulter memoire + `cc-cowork-ref`
- **Correction :** Toujours : memoire → skills forge → plugins externes (en dernier recours)
- **Leçon :** Les skills forge sont la source canonique. Les plugins externes peuvent avoir des infos obsolètes.

**Why:** L'utilisateur a perdu du temps à cause de ces erreurs en cascade. Un expert devrait valider l'architecture avant de construire.

### 6. Propagé le mauvais format de permissions Bash partout
- **Erreur :** Utilisé `Bash(git commit:*)` avec `:` au lieu de `Bash(git commit *)` avec espace dans TOUS les settings.json (9 fichiers sur 6 projets)
- **Pourquoi c'est grave :** Aucune permission Bash ne marchait silencieusement. Claude demandait la permission a chaque commande. Propagé sur claude-forge, ia_back, neo_ia, neoteem-brain, bdd, neopsql, neoauth.
- **Correction :** Format correct = `Bash(command_prefix *)` avec ESPACE, jamais `:`
- **Leçon :** Vérifier la doc/le web AVANT de copier un format dans plusieurs fichiers. Une erreur de syntaxe propagée = dette x nombre de fichiers.

### 7. Créé 4 skills sans consulter forge-brain ni cc-skills-ref
- **Erreur :** Créé backlog-triage, strategic-advisor, prompt-boost, daily-pilot sans lire le vault (best practices, erreurs passées) ni charger cc-skills-ref (format descriptions, structure)
- **Pourquoi c'est grave :** Descriptions YAML bourrées de triggers FR entre guillemets ("Use when the user says X, Y, Z"). Violation des règles que je connais (descriptions sémantiques, anglais, concises). L'utilisateur a dû me corriger.
- **Correction :** Descriptions réécrites en triggers sémantiques anglais. Erreur documentée dans vault Knowledge/erreurs/.
- **Leçon :** Les règles forge-brain-proactive et read-references-first existent pour ça. Les LIRE ne suffit pas, il faut les APPLIQUER à chaque création.

### 8. Ignoré TOUTES les rules lors d'une analyse complète (ia_back, 2026-04-26)
- **Erreur :** Lors d'une analyse complète de ia_back, ignoré 4 rules (check-before-create, delegate-to-specialists, forge-brain-proactive, memory-discipline). 6 skills modifiées + 14 agents modifiés à la main sans aucun agent spécialisé. Zéro consultation du vault ou de la mémoire.
- **Pourquoi c'est grave :** Les rules advisory ne sont pas respectées sous pression. Tout le travail doit être refait.
- **Correction :** Hook déterministe `delegate-guard.py` ajouté. Bloque Edit/Write sur SKILL.md, agents/*.md, CLAUDE.md. Les rules seules ne suffisent pas.
- **Leçon :** Chaque rule critique doit être doublée d'un hook déterministe. "OBLIGATOIRE" dans une rule = juste un mot si rien ne l'enforce.

**How to apply:** 
1. Avant toute architecture multi-agents → vérifier les limitations de Claude Code (subagents, tools)
2. Avant de proposer où mettre quoi → regarder les projets existants de l'utilisateur
3. Si un fix ne marche pas une fois → rechercher, pas bricoler
4. Toujours consulter memoire + skills forge AVANT les plugins externes
5. Avant de propager un pattern dans plusieurs fichiers → vérifier le format exact dans la doc officielle
6. AVANT de créer TOUTE skill/agent/hook → consulter forge-brain (best practices + erreurs) + charger la skill ref correspondante (cc-skills-ref, cc-agents-ref, cc-hooks-ref)
7. TOUJOURS utiliser les agents spécialisés (skill-creator, agent-creator, hook-creator) au lieu d'éditer directement les fichiers
8. Les rules advisory ne suffisent JAMAIS seules — doubler chaque règle critique d'un hook déterministe
9. Le scope des hooks doit couvrir TOUS les chemins proteges — delegate-guard ne couvrait que skills/agents, pas vault/output. Fix : vault-query-guard.py bloque Write sur vault/output/skills/agents tant que le vault n'a pas ete consulte (marqueur session < 60 min)

### 9. Créé 3 notes vault sans consulter le vault (2026-05-06)
- **Erreur :** Créé agentic-engineering-karpathy, neoteem-mapping, pattern-agentic dans vault/ sans lire Knowledge/erreurs/ ni 04-Techniques/ ni feedbacks mémoire. Même pattern que #7 et #8 mais sur notes vault au lieu de skills.
- **Pourquoi c'est grave :** L'erreur #8 disait explicitement de doubler les rules de hooks. Le hook delegate-guard ne couvrait pas Write sur vault/ — scope trop étroit.
- **Correction :** Deux hooks couplés vault-query-tracker.py (PostToolUse, écrit marqueur) + vault-query-guard.py (PreToolUse, bloque Write si marqueur absent). Pattern tracker/guard réutilisable.
- **Leçon :** Le fluency bias ("je sais quoi faire") est le pire ennemi des rules advisory. Plus la conversation coule, plus on skip les vérifications. Seul un hook déterministe résiste.
