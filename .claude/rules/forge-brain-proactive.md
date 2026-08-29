---
description: Query forge-brain vault proactively — at session start, before creating components, after learning, and after mistakes
globs: "*"
---

# Forge Brain — Requêtage proactif

Le vault forge-brain = mémoire infinie. L'interroger est un RÉFLEXE.

## COMMENT — MCP forge-brain UNIQUEMENT

Accès vault EXCLUSIVEMENT via MCP `forge-brain` (auto-start SessionStart, port 8091). JAMAIS Grep/Read/Glob brut, JAMAIS CLI Obsidian.

**22 outils disponibles** — matrice de décision complète : skill `forge-brain` + [[mcp-vault-llm-design]].

Outils les plus utilisés :
- `search_brain` — FTS5 BM25 (file_stem:10 / aliases:8 / content:1)
- `read_note` (lit ENTIÈRE par défaut), `read_section` (1 section)
- `create_note`, `append_note`, `update_property`, `bulk_update_property`
- `move_note`, `delete_note` (atomiques + wikilinks auto)

Si le MCP est indisponible, ne jamais lire ni modifier le vault par le filesystem. Continuer sans contexte vault quand c'est sûr, sinon signaler le blocage.

## QUAND interroger

| Situation | Action |
|---|---|
| **Début de session** | Notes récentes pertinentes |
| **Avant CRÉER skill/agent/hook/rule/CLAUDE.md** | Best practices + `Knowledge/erreurs/` |
| **Avant répondre technique** | Vérifier vault + `derniere-maj` (> 7j = compléter web) |
| **Analyse repo/projet** | Notes concurrents + patterns existants |
| **Après cc-news ou recherche web** | Capitaliser en notes atomiques + MAJ MOCs |
| **Après erreur significative** | Note `Knowledge/erreurs/` |
| **Avant d'affirmer « pas de note / rien dans le vault sur X »** | `search_brain` OBLIGATOIRE (+ `list_notes` du dossier attendu) — jamais de mémoire. « Fausse absence » = failure mode n°1 des vaults LLM (consensus juil. 2026, cf [[pattern-vault-llm-karpathy]]) |
| **Après réponse substantielle composée depuis vault + web** | **Refiler** le fait distillé : enrichir le foyer existant (`insert_section`/`append_note`), note neuve seulement si aucun foyer (cf `.claude/rules/memory-discipline.md`). Boucle Query→refile = ce qui fait composer le vault (« file back », gist Karpathy) — boucle mesurée morte le 16 juil. 2026 (Knowledge/questions : 2 notes), à tenir vivante |

## read_section vs read_note (absorbe l'ex-rule read-section-preference)

- Question PRÉCISE + section identifiable depuis `search_brain` → `read_section` (économe).
- Scope LARGE, première lecture d'une note, ou doute sur la pertinence d'une section seule → `read_note` ENTIÈRE (mieux vaut redondance qu'info manquante).
- Après un `read_section` insuffisant → escalader à `read_note`. Refuser la lecture entière par dogme tokens quand le besoin est large = info manquante garantie.
- ❌ `read_note` systématique sur grosse note (CHANGELOG, log) quand 1 section suffit · ❌ `read_section` sans connaître la structure de la note.

## Protocole par type d'agent (absorbe l'ex-rule vault-consultation-protocol)

Vault check = advisory (doctrine 22 mai : pas de hook d'enforcement). Si le prompt d'invocation contient déjà les infos vault, l'étape est satisfaite. Écriture de notes → skill `obsidian-markdown` pour la syntaxe.

| Type d'agent | Vault |
|---|---|
| Créateurs (skill/agent/hook/claudemd) | Systématique au démarrage |
| Analyseurs (repo-inspector tous modes) | Systématique — référentiel pour juger |
| Exécutants (code-dev, self-updater) | Si sujet nouveau ou doute sur prior art |
| devils-advocate | Conditionnel ciblé, max 2 requêtes |

Référence dans un agent (2 lignes, pas de copier-coller) : « Vault check : consulter le vault selon `.claude/rules/forge-brain-proactive.md` (advisory). »
Anti-patterns : scanner le vault par réflexe sans besoin · skipper le vault sur un créateur « parce que simple » · Bash heredoc pour écrire des notes (boucle quoting Windows) · répondre « aucune note là-dessus » sans `search_brain` préalable (fausse absence).

## OÙ écrire — Ontologie vault

Source canonique : `vault/claude-forge/SCHEMA.md` (dossiers wiki + Knowledge/ — `raw/` supprimé au pivot agent-first 2026-06-27). Voir aussi [[decision-vault-agent-first]].

## Standard qualité notes

Source canonique : [[architecture-cerveau-obsidian-mcp]] section "Standard qualité" + skill `obsidian-markdown` pour syntaxe.

Minimums : 4-6 aliases · resume 1 phrase spécifique · derniere-maj ISO · 2+ tags · 2+ wikilinks.

## Cycle d'apprentissage vault

Le vault = système nerveux forge. Les agents lisent selon leur besoin ; la session principale reste l'unique writer sémantique.

| Agent/Skill | Lit | Écrit |
|---|---|---|
| `devils-advocate` | `Knowledge/erreurs|critiques/` | propose un delta à la session principale |
| `reasoning-cache` | `Knowledge/raisonnements/` | `Knowledge/raisonnements/` |
| `skill-evolve` | Skills + `Knowledge/evolutions/` + mémoire | `Knowledge/evolutions/` |
| `forge-review` | CLAUDE.md + rules + skills + agents | `Knowledge/reviews/` |

## Vault path

`vault/claude-forge/`
