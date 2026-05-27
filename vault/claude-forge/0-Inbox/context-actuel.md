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
**Chantier C — sync leaders vault↔cc-news : MOITIÉ VISIBILITÉ LIVRÉE, MOITIÉ CHASSE TRACÉE (2026-05-27).** Script `sync-leaders.py` créé : régénère le bloc « Leaders canonisés » des 6 `domain-*.md` depuis `list_notes(05-Leaders/<dom>)` entre marqueurs SYNC (idempotent, round-trip vérifié, lecture vault en `open()` direct = équivalent hook). 6 domain-*.md migrés (table → marqueurs + section « Watchlist signaux non canonisés » pour les cibles chassées sans fiche). SKILL.md cc-news documenté (163→179L). Note canonique [[pattern-vault-source-unique-sync-mecanique]] créée. **Vault = source unique des NOMS de leaders (résolu).** **Dette : les QUERIES cc-news ne sont PAS régénérées** — ~50 leaders synced sans query qui les vise (listés par le report `[!]` du script), à compléter à froid ; + normalisation `handle_x` des 80 fiches (mode dégradé). Le diagnostic a invalidé la prémisse « runtime fetch » (le vault donne des noms, pas des queries). À commiter.

---

### Chantier A étapes 2b + 3 + cas spéciaux — LIVRÉES (2026-05-27, antérieur)
**Chantier A étapes 2b + 3 + cas spéciaux — LIVRÉES (2026-05-27).** 2b = fix structurel MCP décoratif sub-agent (2 hooks de garde `vault-cat-guard`/`mcp-alias-guard`, 6 creators durcis, canoniques amendées). Étape 3 = durcissement hooks suite à usage réel. **Cas spéciaux `vault-maintainer` + `devils-advocate` = FAIT** : dette structurelle MCP décoratif sub-agent entièrement résolue. `vault-maintainer` KILLÉ (doublon de la skill `/vault-audit` qui tourne en session principale avec MCP effectif ; trigger proactif porté dans `/vault-audit` ; exemption hook `vault-cat-guard` retirée). `devils-advocate` GARDÉ + brief clarifié (cause structurelle MCP décoratif explicitée ; mode dégradé texte confirmé — 23/24 critiques persistées empiriquement). Pattern méta capitalisé dans [[pattern-mcp-brief-then-direct]] (KILL > faire marcher quand doublon ; agents = écritures rares, skills = écritures MCP denses). Tests hooks 176 verts (180→176 = suppression mécanisme exemption). À commiter (7 commits groupés par concern).

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

## ÉTAPE 2b — RÉSOLUE (2026-05-27)

**Livré** : 2 hooks de garde (`vault-cat-guard.py` matcher Bash|Read|PowerShell ; `mcp-alias-guard.py` matcher append_note) + 6 creators durcis (agent-creator en premier par bypass `.new`+`mv`, puis cascade via agent-creator) + 3 canoniques amendées (comment-creer-skill/agent/hook) + note `hook-intercepte-mcp-et-read-tools` + section bypass dans comment-creer-agent. Tests 170 verts (101 baseline + 46 vault-cat-guard + 23 mcp-alias-guard).

**Décisions empiriques de la session** :
- PreToolUse intercepte les tools MCP, Read ET PowerShell (3 probes confirmés). Capitalisé : [[hook-intercepte-mcp-et-read-tools]].
- vault-cat-guard : Bash/PowerShell dumps bloqués 2 contextes ; Read bloqué sub-agent uniquement (main session Read le vault légitimement pour préparer un Edit) ; vault-maintainer exempt.
- mcp-alias-guard : append_note uniquement (4 violations toutes sur append_note, pas d'extension spéculative).

**DETTE RÉSIDUELLE (déclencheurs de réactivation)** :
- ~~**Cas spéciaux `vault-maintainer` + `devils-advocate`**~~ → RÉSOLU (27 mai, session dédiée). `vault-maintainer` KILLÉ (doublon `/vault-audit`, métier MCP-write impossible en sub-agent) ; `devils-advocate` gardé + brief clarifié (mode dégradé texte, métier = analyse + 0-1 write). Pattern méta : agents = écritures rares, skills = écritures MCP denses → [[pattern-mcp-brief-then-direct]].
- ~~Trou PowerShell vault-cat-guard~~ → FERMÉ cette session (matcher Bash|Read|PowerShell, vérifié empiriquement : Get-Content vault bloqué).
- ~~Audit transverse « trou PowerShell » sur hooks PreToolUse Bash-only~~ → FAIT (étape 3, 27 mai). Cartographie : `security-guard.py` était le seul `Bash`-only vulnérable (les 5 patterns git contournables via tool PowerShell) → matcher passé à `Bash|PowerShell`. `vault-cat-guard` déjà fermé (2b). `delegate-guard`/`meta-commentary-detector` = matchers Edit|Write|MultiEdit, hors sujet. `mcp-alias-guard` = MCP.
- **GAP résiduel sécu — cmdlets PowerShell-natifs destructeurs** (tracé séparément, distinct de l'angle mort matcher) : `security-guard.py` ne couvre que la syntaxe POSIX/git. `Remove-Item -Recurse -Force`, `Stop-Process`, `Clear-Content` ne sont PAS détectés (leur équivalent Bash `rm -rf` relatif ne l'est pas non plus → gap pré-existant de scope). Déclencheur : session sécu dédiée OU incident. ~30 min : ajouter patterns cmdlets PS + équivalents Bash manquants.
- **Skill `/probe-tool`** (proposition Jarvis — verdict : TRACER, ne PAS builder maintenant). Opérationnaliserait le pattern probe utilisé 2× le 27 mai (stub log stdin → settings.local matcher → déclencher → lire log → nettoyer). Refusée maintenant : 2 probes en 14 sessions ≈ 2-3×/an → risque skill-zombie ; cohérence avec le kill de C4 (« signal d'usage requis ») ; pattern déjà capitalisé en prose dans [[hook-intercepte-mcp-et-read-tools]]. Déclencheurs de réactivation : (a) 3 probes en 1 mois, OU (b) 3+ nouveaux MCP servers métier sur peu de temps, OU (c) évolution majeure CC changeant les formats stdin/events → re-vérif systématique.

---

### Archive — Cause racine (fait empirique confirmé)
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

### Note d'attention — hook mcp-alias → RÉSOLU 2b (mcp-alias-guard.py créé)
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
- **Chantier C — chasse opérationnelle** : ~50 leaders synced dans les domain-*.md mais sans query qui les vise (report `[!]` de `py scripts/sync-leaders.py`). À compléter à froid dans les blocs `## Queries à exécuter`. Distinct de la normalisation `handle_x` (80 fiches). La visibilité (liste synced) est faite ; la chasse ne l'est pas. Cf [[pattern-vault-source-unique-sync-mecanique]].
- **README périmé** (21 outils / 412 notes) — session dédiée.

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
[[doctrine-vivante]]
[[critique-2026-05-27-compounding-retroactif]]
[[methode-pivoter-doctrine]]
[[resolution-path-3-contextes]]
