---
name: gate-zero-diff-test-live-byte-exact
description: Gate "zéro diff collatéral" sur une écriture fichier = exige un test LIVE byte-exact ; les tests sur string pure + diff splitlines() sont aveugles à la couche IO (write_text traduit \n→\r\n sur Windows)
metadata:
  type: feedback
---

Quand un livrable promet « **zéro diff collatéral** » sur une écriture de fichier (modifier 1 champ sans toucher le reste byte-for-byte), valider sur **string pure** ne suffit PAS. La couche IO traduit silencieusement les fins de ligne.

**Le piège concret (chantier 5, fix `update_property` MCP, 7 juin 2026)** : un helper de splice testé sur 12 strings LF passait parfaitement. Mais `read_text()` (mode texte) aplatit `\r\n`→`\n` à la lecture, et `write_text()` reconvertit `\n`→`\r\n` à l'écriture sur Windows. Conséquence : un fichier **LF** était intégralement réécrit en **CRLF** = diff full-file. Mesure réelle : 166 des 469 notes du vault étaient LF → bug **actif**, pas latent. Fix : `read_text/write_text(..., newline="")` pour que le code soit seule autorité EOL.

**Pourquoi mes vérifs initiales étaient aveugles** :
- Tests unitaires : appelaient le helper avec des strings LF → ne traversaient jamais la traduction read_text/write_text.
- Harnais de diff : `splitlines()` + `difflib` comparent le *contenu* en supprimant les fins de ligne → une conversion LF→CRLF massive s'affiche « chirurgicale ».
- Le seul test live initial utilisait un fichier CRLF — la seule combinaison où le round-trip ressort propre par coïncidence.

**Why** : un gate de non-régression doit exercer le **chemin de production réel** (disque → lecture → transformation → écriture → relecture des octets), pas une approximation en mémoire. La traduction d'encodage/EOL vit dans la couche IO, invisible aux tests qui court-circuitent cette couche. C'est l'advisor qui a forcé le test discriminant (fichier LF sur Windows, comparaison **octets bruts**).

**How to apply** :
1. Gate « zéro diff / byte-for-byte » sur écriture fichier → **toujours** un test live byte-exact : écrire un fichier réel (`write_bytes`), passer par la vraie chaîne, relire avec `read_bytes()`, comparer les **octets**.
2. Couvrir les variantes d'encodage du corpus réel : LF **et** CRLF (et BOM si présent). Mesurer la répartition réelle (scan octets, comme le scan BOM) pour savoir si un bug est actif ou latent.
3. Ne jamais conclure « chirurgical » depuis un diff `splitlines()`/`difflib` — il efface les fins de ligne. Pour prouver le byte-for-byte : comparer les octets, ou `git diff --unified=0` sur le fichier réel.
4. Réflexe Python Windows : `read_text`/`write_text` traduisent les EOL par défaut (`newline=None`). Pour une écriture byte-exacte, `newline=""`. Même piège sur `open(..., "a")` (append).

Connexe : [[behavioral-test-after-setup]] (tester le comportement réel après modif), [[verify-exhaustive-claims]] (prouver avant d'affirmer), [[da-dicte-tests-adverses-pas-moi]] (l'advisor/DA dicte les tests que je n'aurais pas écrits). Détail technique du fix : vault [[erreur-mcp-yaml-dump-corruption]] section RÉSOLU 2026-06-07.
