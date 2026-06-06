---
titre: "Cowork — Pourquoi les skills ne suivent pas les instructions"
resume: "Diagnostic complet quand une skill Cowork ne suit pas les instructions — 2 problemes distincts, checklist debugging 9 etapes, bugs connus et pattern Skill Activation Hook"
aliases:
  - "cowork skills reliability"
  - "skills ne suivent pas instructions"
  - "skill activation failure"
  - "skill drift"
  - "debugging skills cowork"
  - "pourquoi skill marche pas"
domaine: claude-code
type: technique
derniere-maj: 2026-06-06
auteur: claude
sources:
  - "https://dev.to/thestack_ai/i-audited-214-claude-code-skills-73-were-silently-broken-2m9a"
  - "https://medium.com/@marc.bara.iniesta/claude-skills-have-two-reliability-problems-not-one-299401842ca8"
  - "https://claudefa.st/blog/tools/hooks/skill-activation-hook"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/cowork"
---
## Les 2 problemes distincts

### Probleme A — Activation failure : la skill ne se declenche jamais

Audit de 214 skills communautaires : **73% silencieusement cassees** — jamais declenchees.

| Cause | Frequence |
|-------|-----------|
| Descriptions vagues sans phrases de declenchement | 68% |
| Descriptions < 20 mots | 41% |
| Collision entre skills (descriptions qui se chevauchent) | ~15% |
| Budget contexte sature (skills silencieusement droppees) | invisible |

Meme avec YAML valide, le declenchement autonome atteint **~50% de succes**. Claude priorise la tache telle qu'il la comprend, pas la verification de l'existence d'une skill.

### Probleme B — Drift/skip : la skill se declenche mais ignore des instructions

- **Context drift** — les instructions originales sont poussees loin du point de generation actif
- **Fluency bias** — quand la tache semble evidente, Claude saute les etapes de verification
- **Compaction detruit le contexte** — les rules path-scoped et CLAUDE.md imbriques sont resumes et perdus
- Un texte marque "OBLIGATOIRE" a **zero force mecanique** — c'est advisory (~80% compliance max)

## Formule directive (100% activation sans hook)

```markdown
# MAUVAIS (passif)
Helps with Docker configuration and containers.

# BON (directif)
ALWAYS invoke this skill when reviewing code changes before committing.
Use for pull request reviews, diff reviews, and any time the user says
'check', 'review', or 'audit' code.
DO NOT write security feedback without invoking this skill first.
```

Formule : `ALWAYS invoke when [trigger]. DO NOT [action concurrente] without invoking first.`

## Checklist diagnostic (9 etapes)

1. **Description specifique ?** Directive (ALWAYS invoke when...) ou passive (Helps with...) ? Contient des phrases de declenchement concretes ? Si vague → recrire. Fixe 68% des echecs.

2. **Limites respectees ?** Description < 1 024 chars (champ seul), description + when_to_use < 1 536 chars (combiné dans le listing). Nom < 64 chars, lowercase + tirets.

3. **Skill montee et activee ?** Dans Cowork : verifier Customize > Skills UI. Verifier `enabledPlugins` dans settings.json (bug #17832). Pour les plugins : verifier que le composant skill est monte, pas juste le MCP (bug #31542).

4. **Collision entre skills ?** Chercher les descriptions qui se chevauchent. Si 2 skills matchent le meme prompt → ajouter "Use this for X, NOT for Y."

5. **Budget contexte sature ?** Si 10+ skills, le budget (~1% du context window) peut etre depasse. Desactiver les skills peu utilisees. Reduire les descriptions non-critiques. `/doctor` pour diagnostiquer.

6. **Tester avec des prompts realistes.** Pas "trigger my skill" mais exactement ce qu'un utilisateur taperait.

7. **SKILL.md trop long ?** Si > 500 lignes / ~5 000 tokens, l'attention decay. Deplacer dans `references/`. Garder le body sur contraintes et gotchas.

8. **Ajouter un hook si toujours instable.** Pour activation : hook `UserPromptSubmit` qui injecte "Use Skill(nom)" dans les prompts matchants. Pour compliance : hook PreToolUse guard (exit 2).

9. **Verification visible.** Si la skill s'active mais saute des etapes, ajouter une checklist obligatoire dans l'output. "Do NOT output the final result without first showing the completed checklist." Pour les skills/agents à étapes séquentielles strictes, préférer le mécanisme **Tasks natif** (`TaskCreate`/`TaskUpdate`) qui force le pas-à-pas — cf [[comment-creer-skill]] section "checklist Tasks natif (anti-oubli)".

## Cas empirique — régression intermittente du Problème B (PO Neoteem, 6 juin 2026)

Skill `spec` PO : règles présentes dans le SKILL.md mais appliquées **par intermittence** — émojis de section qui sautent, puces rendues en `*` markdown au lieu d'ADF, encadré maquette présent 1 ticket sur 2. Symptôme typique du **fluency bias** : à chaque génération le modèle « réinterprète » et lâche une contrainte différente. Triptyque de fix qui a tenu :

1. **Consigne FERME, pas descriptive** : une liste de questions « à poser » devient « RÈGLE FERME : poser TOUTES les questions via AskUserQuestion AVANT de rédiger, ne rien supposer ». Une question d'interview non posée (« y a-t-il une maquette ? ») se propage en section manquante (encadré maquette oublié) — la régression vient souvent d'une **étape d'entrée sautée**, pas de la règle de sortie.
2. **Checklist de vérification AVANT l'action critique** (cf étape 9) : bloc « VÉRIFICATION AVANT CRÉATION JIRA » coché point par point (ADF/émojis/titres colorés/template/sections vides/anti-invention/encadré) juste avant l'appel `createJiraIssue`. C'est le « give Claude a way to verify » de Boris.
3. **Remonter en `rule` chargée en permanence > `reference` chargé à la demande** : une contrainte non négociable enfouie dans un `references/*.md` (chargé seulement quand le modèle décide de le lire) dérive ; la même contrainte dans une `rule` du `.claude` (chargée à chaque session) tient bien mieux. En Claude Code (≠ Cowork qui n'a pas de hooks), doubler d'un guard si critique ([[erreur-advisory-rules-insuffisantes]]).

Leçon : pour une contrainte de rendu/format **répétée à chaque exécution**, ne pas se reposer sur le SKILL.md seul → consigne TOUJOURS/JAMAIS + checklist pré-action + rule permanente.
### Renforcement (même session) — gate dur + frontière de responsabilité skill

4. **Checklist passive → GATE impératif « à voix haute ».** La checklist de l'étape 9 tient mieux formulée en STOP : « avant CHAQUE création, vérifie point par point EN CITANT le passage du livrable qui satisfait chaque point ; tu ne passes pas à l'appel tant que tout n'est pas validé dans ta réponse ». Placer **le point qui régresse le plus en DERNIER, traité explicitement** (« ce ticket a-t-il une maquette PO ? si oui l'encadré DOIT être là, sinon je le dis »). Cocher sans citer la preuve = cochage de complaisance.

5. **Frontière de responsabilité : la garde anti-oubli va dans le skill PROPRIÉTAIRE de l'artefact, pas « partout ».** Erreur commise puis corrigée par Raphael : rappel « encadré maquette PO » ajouté à tort dans le skill `maquette`. Or `maquette` ne crée PAS de ticket (HTML/Figma uniquement) — l'encadré est une obligation de **ticket**, donc du seul skill `spec`. Mettre le rappel « partout pour être sûr » viole « 1 skill = 1 responsabilité ». Une obligation se place dans le skill qui possède l'artefact, pas dans tous ceux qui le frôlent.

6. **Garde générique transverse (Claude Code) : « relire le SKILL.md invoqué et cocher ses obligations avant toute validation/création ».** Plutôt que dupliquer une checklist par skill, une `rule` permanente impose, avant l'action critique de N'IMPORTE quel skill, de relire le SKILL.md en cours et de cocher point par point ses sections OBLIGATOIRE/GATE/Comportement attendu. Couvre spec, maquette, review-*, et tout skill futur sans modification. Cf rule PO `verification-skill-avant-validation.md`.

## Matrice enforcement par environnement (CLI / Desktop / Cowork)

> Source : recherche LLM (Claude.ai juin 2026) + vault empirique forge. Numéros d'issues = non vérifiés primaire, indicatifs.

| Mécanisme | Claude Code CLI | Code Desktop | Cowork |
|---|---|---|---|
| **PreToolUse / PostToolUse hooks** | ✅ Fiable | ⚠️ Partiel (certains paths contournés) | ❌ Silent no-op — user hooks exclus par `--setting-sources user` |
| **SessionStart / Stop hooks** | ✅ Fiable | ⚠️ Peu fiable | ❌ SessionStart ne fire pas ; Stop hooks aléatoires |
| **Skills auto-activation (description directive)** | ✅ | ✅ | ✅ (sujet aux bugs scanning ci-dessous) |
| **Slash-command / invocation explicite** | ✅ | ✅ | ✅ (`/` liste les skills) |
| **CLAUDE.md / .claude/rules** | ✅ Chargé | ✅ Chargé | ❌ Non chargé en sandbox → utiliser **project/folder Instructions** à la place |
| **MCP local (stdio)** | ✅ | ✅ (proxié Desktop) | ❌ Non accessible — **remote HTTPS MCP uniquement** |
| **MCP remote HTTPS** | ✅ | ✅ | ✅ (seul type supporté) |
| **Skills depuis `.claude/skills/`** | ✅ | ✅ | ⚠️ Bugs mounting sur certains setups |
| **Skills depuis `~/.claude/skills/`** | ✅ | ✅ | ❌ Non scanné — enregistrer via UI obligatoire |
| **Plugin skills** | ✅ | ✅ | ⚠️ Composant skill parfois non monté même si plugin installé (#31542) |
| **Limite ~30 skills affichées** | ⚠️ Tronque | ⚠️ Tronque | ⚠️ Tronque + "Showing 30 of N" |
| **`context: fork` / `agent:`** | ⚠️ Ignoré si invoqué via Skill tool | ⚠️ Idem | ⚠️ Idem |

### Stratégie d'enforcement recommandée par cible

**CLI — enforcement fort possible**
- Hooks PreToolUse/PostToolUse = couche déterministe (exit 2)
- Description directive + script-output gating + CLAUDE.md/.claude/rules pour routing
- MCP local (stdio) et remote tous deux disponibles
- Seul environnement où l'enforcement est garanti

**Desktop — enforcement best-effort**
- Ne PAS compter sur les hooks pour la sécurité
- Description directive + slash-command entry (`disable-model-invocation: true`) pour side-effects
- Script-output gating : le script imprime le verdict, Claude doit agir dessus
- MCP local fonctionne (proxié), MCP-side validation viable

**Cowork — enforcement par discipline, pas par construction**
- Hooks absents → **zéro enforcement déterministe natif**
- Remplacer CLAUDE.md par **project/folder Instructions** (Cowork sandbox)
- Enforcement = (1) description directive, (2) script-output gating, (3) remote HTTPS MCP validation, (4) AskUserQuestion gate pour side-effects, (5) checklist "à voix haute" obligatoire dans l'output
- Skills : installer via UI, garder total actif < 30, enregistrer `~/.claude/skills/` via manifest
- Pour générer une skill ciblant Cowork : **refuser d'émettre des hooks** dans la skill générée, émettre script-output gating + slash entry à la place

## Bugs connus Cowork

| Bug | Description |
|-----|-------------|
| **#50669** | Cowork ne charge que 3/27 skills personnelles. Ne scanne PAS `~/.claude/skills/` au demarrage — les skills doivent etre explicitement enregistrees via UI ou manifest |
| **#31542** | Le composant skill d'un plugin installe peut ne pas etre monte dans le container VM Cowork, meme si le plugin apparait comme installe. Le MCP du meme plugin fonctionne |
| **#17832** | Race condition : plugins ajoutes a `installed_plugins.json` mais PAS a `enabledPlugins` dans settings.json. Edit manuel necessaire |

### Budget contexte Cowork

Plus serre que CC pur. Plugins et MCP tools en competition pour le contexte. Si Claude agit comme s'il oublie une skill → saturation de budget, pas un bug du modele.

## IMPORTANT : Cowork n'a PAS de hooks

Contrairement a Claude Code, **Cowork ne supporte pas les hooks** (PreToolUse, PostToolUse, etc.). Les patterns d'enforcement deterministe (exit 2, marker+guard) ne fonctionnent PAS dans Cowork.

Consequence : pour fiabiliser une skill Cowork, on ne peut compter que sur :
- La qualite du SKILL.md (description directive, gotchas, contraintes explicites)
- Les instructions globales Cowork (identity + rules dans les settings Claude Desktop)
- Le pattern socratique ("Avant de commencer, quelles questions tu as ?")
- Le scope des skills : `~/.claude/skills/` ou plugin (PAS `.claude/skills/`)

Le Skill Activation Hook (ci-dessous) fonctionne dans Claude Code mais PAS dans Cowork.

## Pattern Skill Activation Hook (Claude Code uniquement)

Un hook `UserPromptSubmit` qui intercepte les prompts et ajoute des recommandations de skills avant que Claude ne les voie. Claude ne peut pas oublier car il n'a jamais eu a se souvenir.

Le hook track ce qu'il a deja recommande et ne repete pas. Complement aux guard hooks (qui gerent la compliance, pas l'activation).

## Liens

- [[comment-creer-skill]] — Format et best practices
- [[comment-creer-hook]] — Patterns d'enforcement
- [[harness-engineering]] — 65% des echecs = harness, pas modele
- [[erreur-advisory-rules-insuffisantes]] — Preuve empirique que l'advisory ne suffit pas
- [[prompting-chat-cowork-code]] — Differences de prompting par plateforme
