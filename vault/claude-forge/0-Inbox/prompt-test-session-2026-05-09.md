---
titre: Prompt de test session 2026-05-09
resume: Prompt de validation forge v2 — XML, CoT, critères déterministes, validé devil's advocate
aliases:
  - prompt test
  - test session
  - validation session
  - prompt validation forge
type: context
status: active
derniere-maj: 2026-05-09
auteur: claude
tags:
  - "#type/context"
  - "#meta/test"
---

## Comment utiliser

Ouvre une nouvelle session Claude Code dans `claude-forge`. Copie le contenu du bloc ``` ci-dessous. Colle dans le prompt initial.

Techniques appliquées : Role prompting, XML tags, Chain-of-Thought (`<thinking>`), Format Control déterministe, Context Explanation, critères OK/FAIL sans ambiguïté.

Validé par devil's advocate (3 bloquants corrigés : reset markers déterministe, regex grep large, validation /done sémantique).

## Prompt à copier

```
<role>
Tu es un agent QA pour claude-forge. Tu exécutes des tests de validation et rapportes les résultats SANS indulgence. Un test partiel = FAIL avec détail. Tu copies-colles les erreurs exactes (jamais de paraphrase). Tu n'inventes pas de résultats.
</role>

<context>
claude-forge a subi une refonte le 2026-05-09 :
- MCP forge-brain (11 outils, port 8091, auto-start SessionStart) remplace toute la CLI Obsidian
- Vault holistique : 0-Inbox/ + 1-Projets/ + 2-Casquettes/ + technique existant
- Skills /done (métacognition) et /watch (transcription YouTube)
- Devil's advocate : Stop hook + guard intelligent (déclenche uniquement sur créations/architecture, PAS sur fixes/migrations)
- Migration CLI→MCP totale (10 agents, 6 skills, 2 rules, 3 references)
- Règle d'autonomie : advisor + devil's advocate valident → agir sans demander
- Standard qualité notes : 4-6 aliases, résumé spécifique, 2+ wikilinks

Ton job : prouver que TOUT fonctionne réellement. Pas une croyance, des preuves.
</context>

<setup>
1. `bash netstat -an | grep 8091` (sur Windows : `netstat -an | findstr 8091`)
2. Si port absent : `python mcp-forge-brain/start.py &` puis attendre 3s
3. Confirmer port LISTENING avant de continuer
4. Reset propre : `rm -f .claude/.devil-advocate-needed .claude/.devil-advocate-done`
</setup>

<methodology>
Avant chaque verdict, écris ton raisonnement dans <thinking> tags.
Compare le résultat OBSERVÉ aux critères OK SANS interprétation.
Si ambigu → FAIL.
</methodology>

<tests>

<test id="1.1" bloc="MCP">
<objectif>vault_stats fonctionne</objectif>
<action>Appeler mcp__forge-brain__vault_stats()</action>
<critere_ok>Réponse contient les 4 nombres : notes, tags, wikilinks, aliases ET un tableau par dossier avec au moins 5 lignes</critere_ok>
</test>

<test id="1.2" bloc="MCP">
<objectif>search_brain trouve une note précise</objectif>
<action>mcp__forge-brain__search_brain(query="Raphael Picard", limit=3)</action>
<critere_ok>Au moins 1 résultat dont le path est exactement `2-Casquettes/Raphael-Picard.md`</critere_ok>
</test>

<test id="1.3" bloc="MCP">
<objectif>Résolution par alias</objectif>
<action>mcp__forge-brain__read_note(file="forge")</action>
<critere_ok>Le contenu retourné contient la ligne `titre: Claude-Forge` dans le frontmatter</critere_ok>
</test>

<test id="1.4" bloc="MCP">
<objectif>list_notes par dossier</objectif>
<action>mcp__forge-brain__list_notes(folder="1-Projets", limit=20)</action>
<critere_ok>Le résultat contient EXACTEMENT ces 7 paths : Claude-Forge.md, Neoteem.md, ia_back.md, neo_ia.md, neoteem-brain.md, bdd.md, Expertise-IA.md</critere_ok>
</test>

<test id="2.1" bloc="Vault">
<objectif>Profil Raphael complet et conforme</objectif>
<action>mcp__forge-brain__read_note(file="Raphael-Picard")</action>
<critere_ok>Le contenu contient TOUTES ces strings exactes : `23 janvier 1990`, `Jennifer`, `Rose`, `Louis`, `Diablo 4`, `Path of Exile 2`, `expert IA reconnu`, `moniteur d'équitation`</critere_ok>
</test>

<test id="2.2" bloc="Vault">
<objectif>Context Note structurée</objectif>
<action>Read vault/claude-forge/0-Inbox/context-actuel.md</action>
<critere_ok>Contient les 4 headers : `## Phase actuelle`, `## Dernière session`, `## Prochaines étapes`, `## Fils ouverts`</critere_ok>
</test>

<test id="3.1" bloc="Skills">
<objectif>/watch transcrit une vidéo réelle</objectif>
<action>Lance `/watch https://www.youtube.com/watch?v=AJpK3YTTKZ4` (Anthropic "Introducing Claude Code", 3min)</action>
<critere_ok>Retourne au moins 500 caractères de transcription (texte réel, pas une erreur). Vérifier la longueur.</critere_ok>
</test>

<test id="4.1" bloc="DevilsAdvocate">
<objectif>État initial propre</objectif>
<action>Bash : `rm -f .claude/.devil-advocate-needed .claude/.devil-advocate-done && ls .claude/.devil-advocate-* 2>&1`</action>
<critere_ok>stdout contient `No such file or directory` (ou équivalent shell)</critere_ok>
</test>

<test id="4.2" bloc="DevilsAdvocate">
<objectif>Guard NE déclenche PAS sur "fix"</objectif>
<action>Bash reset : `rm -f .claude/.devil-advocate-needed`. Puis lance Agent(description="Fix something minor", subagent_type="general-purpose", prompt="dis bonjour"). Puis Bash : `ls .claude/.devil-advocate-needed 2>&1`</action>
<critere_ok>Le ls retourne `No such file or directory` (le mot "fix" est dans NON_DELIVERABLE_KEYWORDS)</critere_ok>
</test>

<test id="4.3" bloc="DevilsAdvocate">
<objectif>Guard DÉCLENCHE sur "create"</objectif>
<action>Bash reset : `rm -f .claude/.devil-advocate-needed`. Puis lance Agent(description="Create a test something", subagent_type="skill-creator", prompt="liste juste les fichiers de .claude/skills/ sans rien créer"). Puis Bash : `ls .claude/.devil-advocate-needed 2>&1`</action>
<critere_ok>Le ls retourne `.claude/.devil-advocate-needed` (le fichier existe)</critere_ok>
</test>

<test id="4.4" bloc="DevilsAdvocate">
<objectif>Stop hook bloque correctement</objectif>
<action>Avec marker needed présent, marker done absent : Bash `rm -f .claude/.devil-advocate-done && touch .claude/.devil-advocate-needed && echo '{}' | python .claude/hooks/devil-advocate-stop.py`</action>
<critere_ok>Stdout contient EXACTEMENT la string `"decision": "block"` ET `"reason"`</critere_ok>
</test>

<test id="4.5" bloc="DevilsAdvocate">
<objectif>Stop hook laisse passer après devil's advocate</objectif>
<action>Bash : `touch .claude/.devil-advocate-done && echo '{}' | python .claude/hooks/devil-advocate-stop.py; echo "---END---"`</action>
<critere_ok>Stdout vide entre la commande et `---END---` (aucun JSON block produit)</critere_ok>
</test>

<test id="5.1" bloc="Migration">
<objectif>Zéro référence CLI Obsidian dans .claude/</objectif>
<action>Bash : `grep -rEl "obsidian[-_]cli" .claude/ --include="*.md" --include="*.py" 2>/dev/null`</action>
<critere_ok>stdout VIDE (aucun fichier listé). Si des fichiers apparaissent, FAIL avec la liste exacte.</critere_ok>
</test>

<test id="6.1" bloc="Done">
<objectif>/done réécrit la Context Note avec contenu sémantique</objectif>
<action>
1. Bash : `cat vault/claude-forge/0-Inbox/context-actuel.md > /tmp/before-done.md`
2. Lance `/done`
3. Bash : `diff /tmp/before-done.md vault/claude-forge/0-Inbox/context-actuel.md`
</action>
<critere_ok>Le diff montre des changements (pas vide) ET le nouveau fichier contient encore les 4 headers (Phase actuelle, Dernière session, Prochaines étapes, Fils ouverts) ET la `derniere-maj` est mise à jour à la date du jour</critere_ok>
</test>

<test id="7.1" bloc="E2E">
<objectif>Workflow end-to-end : créer note → vérifier wikilinks</objectif>
<action>
1. mcp__forge-brain__create_note(path="0-Inbox/test-e2e-VALIDATION.md", content="---\ntitre: Test E2E\nresume: Test bout en bout\naliases: [test e2e, e2e]\ntype: context\nderniere-maj: 2026-05-09\ntags:\n  - '#meta/test'\n---\n\n# Test E2E\n\nLien : [[Raphael-Picard]]\n")
2. mcp__forge-brain__get_backlinks(file="Raphael-Picard")
3. Cleanup : `rm vault/claude-forge/0-Inbox/test-e2e-VALIDATION.md`
</action>
<critere_ok>Étape 1 retourne "Note creee". Étape 2 retourne une liste qui contient `test-e2e-VALIDATION` (le wikilink est indexé en moins de 30s par le watcher MCP). Étape 3 supprime sans erreur.</critere_ok>
</test>

</tests>

<output_format>
Livre ce format EXACT à la fin :

## Rapport de validation forge v2 — 2026-05-09

### Résultats

| Test | Bloc | Statut | Détail |
|------|------|--------|--------|
| 1.1 | MCP | OK / FAIL | (résumé 1 ligne, ou erreur exacte si FAIL) |
| 1.2 | MCP | OK / FAIL | ... |
| 1.3 | MCP | OK / FAIL | ... |
| 1.4 | MCP | OK / FAIL | ... |
| 2.1 | Vault | OK / FAIL | ... |
| 2.2 | Vault | OK / FAIL | ... |
| 3.1 | Skills | OK / FAIL | ... |
| 4.1 | DevilsAdvocate | OK / FAIL | ... |
| 4.2 | DevilsAdvocate | OK / FAIL | ... |
| 4.3 | DevilsAdvocate | OK / FAIL | ... |
| 4.4 | DevilsAdvocate | OK / FAIL | ... |
| 4.5 | DevilsAdvocate | OK / FAIL | ... |
| 5.1 | Migration | OK / FAIL | ... |
| 6.1 | Done | OK / FAIL | ... |
| 7.1 | E2E | OK / FAIL | ... |

### Score
**X/15 tests passés**

### FAILs détaillés
Pour chaque FAIL, donner :
- Test ID
- Action exécutée
- Résultat observé (copier-coller la sortie)
- Hypothèse de cause

### Verdict
- 15/15 → SHIP IT
- 13-14/15 → SHIP avec correctifs mineurs
- < 13/15 → BLOCK

### Recommandations Jarvis
1-3 propositions d'amélioration concrètes basées sur les observations.
</output_format>

<constraints>
- Critères OK/FAIL DÉTERMINISTES — ne jamais marquer OK sur "presque"
- Erreurs : copier-coller stderr exact, jamais paraphraser
- Tests indépendants — un FAIL n'arrête pas la suite
- MCP down → BLOCKED sur 1.1-1.4, 2.1, 7.1, continuer les autres
- Reset déterministe des markers AVANT chaque test 4.x avec `rm -f`
- Le test 4.5 : si stderr non vide ou stdout non vide → FAIL avec la sortie exacte
- Cleanup obligatoire après test 7.1
- Ne PAS modifier de fichier hors des cleanups documentés
</constraints>
```
