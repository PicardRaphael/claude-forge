---
titre: "[architecture-decision] — écriture fichier byte-for-byte : splice vs re-dump, et pourquoi le test live est non négociable"
resume: "Chaîne décisionnelle réutilisable pour toute exigence byte-for-byte sur écriture fichier : disqualifier a priori toute ré-sérialisation globale (re-dump), et ne jamais conclure 'validé' sans test live byte-exact — un diff mémoire peut mentir sur le comportement disque."
aliases:
  - "byte-for-byte écriture fichier"
  - "splice vs re-dump frontmatter"
  - "test live byte-exact obligatoire"
  - "byte-exact write decision"
  - "zero-diff file edit reasoning"
  - "EOL translation write_text gotcha"
  - "splice chirurgical frontmatter"
  - "gate-zero-diff-test-live-byte-exact"
type: raisonnement
domaine: general
derniere-maj: 2026-06-07
auteur: claude
tags:
  - "#type/raisonnement"
  - "#domaine/claude-code"
---

## Problème

Modifier UNE propriété d'un fichier (ici frontmatter YAML) sous une exigence stricte : **zéro diff collatéral, byte-for-byte** — seul le champ ciblé change, tout le reste du fichier reste identique octet par octet. Sur un corpus réel hétérogène (encodages mêlés).

## Contexte

Fix d'un outil MCP qui écrit sur disque (chantier 5 forge). Détails du bug et du code : [[erreur-mcp-yaml-dump-corruption]] section RÉSOLU 2026-06-07. Cette note ne garde que le **chemin de décision**, pas le récit.

## Chaîne de raisonnement

1. **Deux voies pour « modifier 1 champ sans toucher le reste »** : (a) `yaml.safe_load` + re-dump du frontmatter entier ; (b) splice chirurgical du seul span de la propriété (édition ciblée du texte).
2. **Re-dump disqualifié AVANT d'écrire une ligne**, pas après échec : une ré-sérialisation globale (PyYAML) réordonne les clés, re-quote les dates, échappe l'unicode, change l'indentation. Elle viole le byte-for-byte **par construction**. `ruamel.yaml` (round-trip préservant) écarté aussi : dépendance externe + toujours pas garanti byte-perfect.
3. **Splice retenu** : remplacer uniquement le span de la propriété (ligne-clé + continuations), rendu calibré sur le style réel observé. Le reste du fichier n'est jamais re-sérialisé → byte-for-byte tenable.
4. **12 tests verts en mémoire + diff "chirurgical" → verdict provisoire "validé".** C'est ici que le piège se referme.
5. **Le gate live a renversé le verdict.** Test sur fichier disque réel (LF forcé) : un 2e bug invisible apparaît — la couche IO (`read_text`/`write_text`, mode texte Windows) **traduit les fins de ligne** (`\n`↔`\r\n`). Un fichier LF entier ressortait en CRLF = diff full-file. Mesure : une large part du corpus était LF → bug **actif**, pas latent.
6. **Fix par construction** : `newline=""` en lecture ET écriture → le code devient seule autorité EOL (LF reste LF, CRLF reste CRLF, BOM préservé). Verrouillé par des tests de régression **live** permanents (pas string).

## Insight clé

**Un diff en mémoire « chirurgical » peut MENTIR sur le comportement disque, et un harnais de diff `splitlines()`+`difflib` est aveugle PAR CONSTRUCTION aux conversions de fins de ligne** — il efface les EOL avant de comparer le contenu, donc une conversion LF→CRLF massive s'affiche « propre ». Les tests sur string pure ne traversent jamais la couche IO où vit la traduction d'encodage/EOL. Conséquence opérationnelle : pour tout code qui écrit sur disque sous une exigence byte-for-byte, **le test live byte-exact (`read_bytes`/`write_bytes`, comparer les octets, sur LF ET CRLF) n'est pas optionnel** — le test mémoire ne prouve que la *logique*, jamais l'*IO*. C'est l'advisor + l'exigence d'un test discriminant (fichier LF) qui ont forcé la découverte ; sans eux, le bug partait en prod.

## Résultat

Splice + `newline=""` → byte-for-byte prouvé sur disque (LF et CRLF), reparse propre, autres champs intacts. Tests de régression live permanents verrouillent les deux encodages. Suite complète verte. Fix commité.

## Réutilisation

Déclencher ce raisonnement quand :
- une tâche exige « modifier sans toucher le reste / byte-for-byte / zéro diff collatéral » sur un fichier → **disqualifier d'emblée toute ré-sérialisation globale**, viser une édition ciblée du span.
- on s'apprête à conclure « validé » sur une écriture fichier à partir d'un **diff mémoire ou d'un diff qui normalise les lignes** → **ne pas conclure** : exiger un test live byte-exact octets, couvrant LF et CRLF (et BOM si le corpus en a).
- dev d'un outil/MCP qui lit-transforme-écrit un fichier sur Windows → se méfier de la traduction EOL par défaut de `read_text`/`write_text`/`open(...,"a")` ; `newline=""` rend le code seule autorité.

## Symétrique — read/compare-path (audit de divergence)

Même racine EOL Windows, autre moment : lors d'un **audit de synchro cross-repo**, `md5sum` et `diff` bruts crient **DIFFÉRENT** alors que le contenu est identique — seul l'encodage des fins de ligne diffère (`core.autocrlf` ou outil d'écriture).

**Vécu 26 juin 2026 (audit skill /spec ×3 repos) :** MD5 « DIFFERENT » sur 13/14 références → diagnostic « les références divergent → cause du bug ». Re-diff `--strip-trailing-cr` : **0 ligne de diff réel** sur 12/13. Faux diagnostic complet.

**Réflexe avant tout verdict de divergence/synchro :**
1. `file <a> <b>` → repère « with CRLF line terminators » d'un côté seulement.
2. Re-comparer en neutralisant les EOL : `diff --strip-trailing-cr a b` (ou `git diff --ignore-cr-at-eol`, ou normaliser avant `md5sum`).
3. Le verdict « identique / divergent » se prononce sur le diff EOL-neutre, jamais sur le MD5/diff brut.

Write-path : la couche IO Python traduit `\n`→`\r\n` à l'écriture (ce raisonnement, fix `newline=""`). Compare-path : `md5sum`/`diff` bruts mentent à la *lecture/comparaison*. Même faille, deux contextes.
## Liens

- [[erreur-mcp-yaml-dump-corruption]] — le bug et le code (détails)
- [[erreur-tests-heureux-vs-adverses]] — des tests verts ne prouvent pas ce qu'on croit ; l'advisor/DA dicte le test discriminant qu'on n'aurait pas écrit (cf feedback mémoire `da-dicte-tests-adverses-pas-moi`)
