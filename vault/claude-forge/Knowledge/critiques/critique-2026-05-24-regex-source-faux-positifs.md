---
titre: "Critique - Regex Source: faux positifs propagation meta-commentary-detector"
type: knowledge
domaine: claude-code
derniere-maj: 2026-05-24
auteur: claude
aliases:
  - "critique-regex-source-faux-positifs"
  - "fp-source-label-2026-05-24"
  - "meta-commentary Source FP"
  - "patch lookahead source-label"
tags:
  - "#type/critique"
  - "#domaine/claude-code"
sources:
  - "[[erreur-meta-commentaires-composants]]"
  - "[[feedback_workaround_sediment]]"
---

# Critique - Regex Source: faux positifs (propagation ia_back + neo_ia)

## Verdict

Bloquants : 1 | Avertissements : 3 | Decision : LIVRER AVEC CORRECTIONS - Option E (5eme option proposee par DA).

## Contexte

Audit pre-propagation meta-commentary-detector.py sur ia_back + neo_ia : 2 faux positifs sur 9 patterns, tous deux sur source-label. Cas :
- ia_back/.claude/agents/schema-mapper.md:86 - directive de format (l'agent doit indiquer la source de ses donnees)
- neo_ia/.claude/skills/neochat-agents/SKILL.md:289 - reference vers fichier code

CLAUDE.md = 0 infraction. Composants = 0 autre infraction.

## Pourquoi les options A/B/C/D echouent

| Option | Failure mode |
|---|---|
| A (capitalisation) | Brittle. Heuristique nom propre = drift sur N futurs leaders |
| B (whitelist par repo) | Workaround noqa-style. Bypass par flemme. Anti-pattern feedback_workaround_sediment |
| C (rename Source -> Provenance) | Cout pedagogique. Source = mot francais standard |
| D (laisser passer 2 FP) | Premier "OK plus tard" = signal hook negociable = effondrement valeur |

## Option E retenue - Lookahead syntaxique

Frontiere "autorite doctrinale vs reference technique" est codable par SYNTAXE MARKDOWN, pas par lexique de noms.

Patch regex source-label final (apres bug fix advisor):

```python
("source-label", re.compile(
    r"(?m)^[ \t]*Source\s*:[ \t]+(?![`<{]|\[(?!\[))",
    re.IGNORECASE
)),
```

Autorise (lookahead negatif) : backtick (code), chevron (placeholder), accolade (variable), bracket simple (enum/format).
Bloque : texte libre (attribution auteur), double-bracket [[wikilink]] (attribution wikilink), URL.

## Bug initial du regex DA

Premier regex propose par DA utilisait `\s*` avant le lookahead. Probleme : `\s*` greedy + backtrack laissait le moteur matcher 0 espace, lookahead voyait alors l'espace lui-meme (pas dans la blacklist) => faux positif.

Fix advisor : remplacer par `[ \t]+` (au moins 1 espace, restreint aux espaces/tabs). Force position juste apres l'espace, lookahead voit le premier caractere non-blanc reel.

## Tests de regression ajoutes (6 cas)

- expect_pass : Source : code en backticks
- expect_pass : Source : enum entre brackets
- expect_pass : Source : placeholder entre chevrons
- expect_block : Source : double-bracket attribution wikilink
- expect_block : Source : URL HTTPS
- expect_block : Source : nom propre libre

21/21 tests passent au total.

## Bug structurel cross-repo decouvert

Le hook claude-forge scannait TOUS les fichiers matchant SCOPED_PATTERNS, peu importe le repo. Resultat : tentative de Write dans neot-v2/ia_back/ a ete bloquee par le hook claude-forge.

Fix : ajout d'une fonction is_inside_forge(path) comme dans delegate-guard.py. Hook fail-open immediatement si le path n'est pas dans claude-forge.

Lecon : tout hook avec scope par pattern de chemin doit AUSSI verifier le scope par repo via is_inside_<project_dir>. Sinon pollution cross-repo garantie.

## Avant propagation ia_back + neo_ia

1. Patch lookahead applique
2. Self-test 21/21 vert
3. is_inside_forge guard ajoute (anti-pollution cross-repo)
4. Scanner ia_back + neo_ia avec hook patche : 0 violation
5. neo_ia : adapte commande uv run python dans settings.json
6. ia_back : port TS complet (stack bun, 14/14 self-tests)

## Apprentissage

- Pattern meta : avant whitelist ou abandon, regarder si la frontiere est codable SYNTAXIQUEMENT plutot que SEMANTIQUEMENT. Syntaxe markdown = set ferme stable.
- Anti-pattern recurrent : regex large `^\s*X\s*:` sans contrainte sur ce qui suit = source garantie de faux positifs sur domaines ou le mot X est ambigu.
- Bug greedy `\s*` + lookahead : toujours forcer la position avec `[ \t]+` quand un lookahead suit, sinon backtrack laisse passer.
- Tout hook avec scope par chemin DOIT verifier scope par repo (is_inside_project) - sinon pollution cross-repo.

[[erreur-meta-commentaires-composants]] | [[feedback_workaround_sediment]] | [[feedback_recurring_meta_anti_pattern]]
