---
name: verify-exhaustive-claims
description: Toujours valider les déclarations exhaustives (zéro, tous, aucun) par grep/search avant de les affirmer
type: feedback
originSessionId: d059faa4-9130-4f07-a9d6-4f39f900e355
---
Ne JAMAIS déclarer "zéro référence à X" ou "migration complète" sans grep de validation.

**Why:** Session 2026-05-09 — la migration CLI→MCP a été déclarée "zéro ref CLI" dans la context note et le commit message, mais 3 fichiers contenaient encore des références obsidian-cli (delegate-guard.py, recap/SKILL.md, skill-evolve cross-pollination). La QA a trouvé ce que l'auteur a raté.

**How to apply:** Avant tout commit/note affirmant une exhaustivité (zéro, tous, aucun, complet), exécuter un grep de validation. Si le grep trouve des résultats → corriger avant d'affirmer. Pattern : `grep -rEl "<terme>" <scope> --include="*.md" --include="*.py"`.

**Validation empirique 2026-05-27 (Mémoire Portable) :** j'allais déclarer le baseline "143 tests verts" après avoir lancé une seule suite. Raphael a forcé la vérification — les tests hooks (`.claude/hooks/tests/`, 101 tests) n'avaient pas été lancés. Total réel = **244** (143 MCP + 101 hooks). Sans la vérif, toute régression hooks aurait été invisible. La règle marche : un chiffre de baseline est une déclaration exhaustive, donc à vérifier en lançant TOUTES les suites, pas une. Corollaire : `cd` dans un sous-dossier (ex: `mcp-forge-brain/`) peut fausser les chemins relatifs des commandes suivantes — toujours repartir du `git rev-parse --show-toplevel`.

**Validation empirique 2026-06-16 (alignement chemin cross-repo) — le SCOPE du grep est aussi une déclaration exhaustive :** pour un renommage de chemin (`docs/implementation-notes/` → `.tmpclaude/feature-notes/`), j'avais inventorié les pointeurs dans `.claude/` seul (9 fichiers) et j'allais déclarer « 0 résiduel ». L'advisor a forcé un grep **repo-wide** : 3 pointeurs-relais survivaient HORS `.claude/` — `CLAUDE.md`, `doc/cahier-des-charges.md`, `memory/reference_*` — exactement le drift que `zero-dette` veut tuer. Leçon : grepper le dossier ÉVIDENT ne prouve pas l'exhaustivité ; un renommage/déprication se cherche **à la racine du repo**, puis on trie chaque hit avec jugement (pointeur à corriger vs livrable durable légitime qui cite un fichier réel). Ne jamais revendiquer « 0 résiduel repo-wide » après un grep scopé à un sous-dossier. Cf rule `cross-repo-propagation` (grep le terme modifié sur chaque repo après propagation).
