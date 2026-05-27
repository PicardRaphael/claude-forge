---
titre: Context Actuel
resume: Working memory dynamique — mis à jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, memoire de travail, etat actuel]
type: context
status: active
derniere-maj: 2026-05-27
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---

## Phase actuelle
**Chantier A — pont veille→doctrine : Paquet 1 LIVRÉ.** Le pont pull-based est opérationnel : un finding majeur de cc-news → étape 8 invoque `doctrine-impact-check` → croisement avec les canoniques → verdict (INFO / DOCTRINE_PIVOT_CANDIDATE / DOCTRINE_REINFORCE) → gate humaine `[v]/[m]/[i]`. Dirigé, jamais aveugle. Suivant immédiat = **étape 2b — fix structurel du bug MCP décoratif sub-agent** (chantier-bug né en cours de route, dette tracée ci-dessous).

## Dernière session (2026-05-27) — Chantier A
### Décisions prises
- **Cadrage 2 paquets** (advisor + arbitrage Raphael) : Core = C1+C2+C3 (livré). C4-C7 = différés, à évaluer après usage réel (éviter le format-zombie / piège du scan A1×A3 tué).
- **C1** [[doctrine-vivante]] : note canonique posant le moteur EXTERNE d'évolution doctrinale (extension de « CLAUDE.md DOIT évoluer », du local interne au global externe). Gate humaine non négociable, scan aveugle interdit (lien 0/12).
- **C2** skill `doctrine-impact-check` (156L, opus, description 225 chars) : brouillon argumenté + gate `[v]/[m]/[i]`, n'appelle JAMAIS methode-pivoter-doctrine directement (décision Raphael : gate humaine maximale). 3 TODO différés capitalisés dans le body (C5 fraîcheur triggered-by-event, C6 ligne méta-doctrine, C7 arbitrage conflits).
- **C3** `cc-news` étape 8 : doctrine-impact-check sur findings MAJEURS uniquement (anti-cascade).
- **Bug MCP décoratif sub-agent** découvert et confirmé empiriquement (verdict, pas inférence) → fix structurel reporté en session dédiée (anti-fragmentation).

### En cours
Rien en suspens sur le Paquet 1. 4 commits poussés sur main (C1 note, C2 skill, C3 cc-news, doc vault). Working tree à vérifier propre après push.

### Prochaines étapes
1. **/done + /clear**, puis **étape 2b — fix structurel MCP décoratif** (session continue ou dédiée).
2. Évaluer Paquet 2 (C4-C7) après 2-3 semaines d'usage réel du pont.

## DETTE TRACÉE — étape 2b : fix MCP décoratif sub-agent (À TRAITER, NE PAS SUPPRIMER)

### Cause racine (fait empirique confirmé)
Le frontmatter `tools: ... mcp__forge-brain__*` d'un sub-agent est **décoratif** : le serveur MCP n'est PAS connecté dans le contexte d'exécution du sub-agent. Preuve : 2 agents testés (skill-creator observé cat le vault ; hook-creator → `No such tool available: mcp__forge-brain__read_note`). Conséquence : un sub-agent à qui on ordonne « lis les canoniques via MCP » mais sans MCP réel fallback sur `cat`/`find` du vault (viole la doctrine MCP-only). **Règle architecturale : la session principale est le seul contexte avec MCP effectif. Tout brief sub-agent impliquant le vault contient les extraits inline, jamais « lis via MCP ».**

### Périmètre (audit transverse des 11 agents fait)
- **6 bugs latents francs** (MCP frontmatter + ordre systématique de lecture vault) : `skill-creator` (confirmé), `agent-creator`, `hook-creator` (confirmé), `claudemd-optimizer`, `repo-inspector` (le plus exposé, 2 blocs lecture), `responsable-ia`.
- **2 cas spéciaux ISOLÉS** (pattern brief-inline ne s'applique pas — leur métier EST d'écrire dans le vault) : `vault-maintainer`, `devils-advocate` (create_note dur). Traiter en note de dette dédiée avec déclencheur « rencontrer un cas où l'un doit être délégué en sub-agent et écrire dans le vault ».
- **2 risques faibles** : `self-updater` (consigne vault sans MCP dans tools), `python-dev` (conditionnel).
- **1 sain** : `outcomes-grader`.

### Composants à créer/modifier en 2b
1. ~~Note canonique `subagent-mcp-non-herite`~~ → FAIT autrement : cause-racine capitalisée en **amendement de [[pattern-mcp-brief-then-direct]]** (section AJOUT 27 mai) + feedback mémoire `subagent-mcp-non-connecte-brief-inline`. Pas de nouvelle note (évite doublon).
2. Amender briefs des 6 creators : remplacer « lire EN ENTIER via MCP » par « contenu canonique fourni dans le brief ; si manque, ESCALADE ; JAMAIS cat/find/grep/Read sur le vault ».
3. Hook `vault-cat-guard` (proposition Jarvis validée) — PreToolUse Bash, bloque cat/find/grep sur `vault/` (enforcement structurel, défense en profondeur ; doctrine hooks 22 mai = scope/sécurité OK).
4. Amender canoniques creator ([[comment-creer-skill]], [[comment-creer-agent]], [[comment-creer-hook]]) avec la règle.
5. MAJ CLAUDE.md éventuelle si jugé assez structurant.

### Note d'attention — hook mcp-alias (4e re-violation aujourd'hui)
Le pattern `mcp-alias-ambigu-chemin-exact` re-violé 4× le 27 mai (dont ce /done : `append_note(file="log vault")` malgré la RÈGLE FERME interdisant tout alias sur stem multi-dossier). Seuil garde-fou hook atteint (cf [[feedback_feedback_reviole_3x_regle_insuffisante]]). À considérer en 2b / session future : hook PreToolUse sur `mcp__forge-brain__append_note` vérifiant l'unicité du stem dans le vault avant écriture (erreur si log/index/CHANGELOG multi-dossiers). Distinct de vault-cat-guard. Pas maintenant (anti-fragmentation), tracé.

### Dépendance circulaire à résoudre
Pour modifier `agent-creator` on cross-dispatch via `skill-creator` (pattern self_modification_agent_cross_dispatch) — mais `skill-creator` est l'agent buggé. Résolution : **fixer skill-creator EN PREMIER** via le pattern brief-inline (ou édition directe par la session principale en exception assumée, car on fixe skill-creator lui-même). Puis skill-creator durci fixe les autres.

### Méta — alignement doctrine-vivante
La doctrine forge a évolué par **signal externe natif** (MCP CC déconnecté en sub-agent) le jour même de la création de [[doctrine-vivante]] : illustration vivante du principe (la doctrine challengée par le monde, pas seulement par l'erreur interne).

## Fils ouverts
- **Double-source mémoire transitoire** : auto-memory native encore injectée en parallèle de l'@import. Dette tracée. Cf [[import-ajoute-pas-remplace-automemory]].
- **A1×A3 tué** : ne pas réouvrir le scan rétroactif systématique sans nouvelle donnée infirmant le 0/12. Cf [[idee-compounding-retroactif]] (TUÉE).
- **Paquet 2 Chantier A (C4-C7)** : différés, à évaluer après usage réel du Paquet 1. Reformulations capitalisées dans les TODO de `doctrine-impact-check`.
- **TODO P0** : rotation password PostgreSQL prod (secret redacté mais pas tourné). Cf [[todo-rotation-password-postgres-prod]].
- **README périmé** (21 outils / 412 notes) — session dédiée.

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
[[doctrine-vivante]]
[[critique-2026-05-27-compounding-retroactif]]
[[methode-pivoter-doctrine]]
[[resolution-path-3-contextes]]
