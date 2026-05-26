---
name: da-blocking-arbitrage
description: "Use when Devil's Advocate verdict BLOCKING >= 1 before shipping. PARTIAL fix != PASS. Explicit user arbitrage mandatory. Stops auto-promotion."
effort: high
---

## Rôle

Appliquer le protocole d'arbitrage obligatoire quand un verdict Devil's Advocate contient au moins un BLOCKING. Empêche le ship/commit/promulgation automatique.

## Étapes

1. **Lire le verdict DA en entier** — pas de troncature. Si tronqué, relancer le DA.

2. **Parser les BLOCKING** — les lister explicitement à l'utilisateur :
   ```
   BLOCKING 1 : [description]
   BLOCKING 2 : [description]
   ```

3. **Pour chaque BLOCKING**, proposer :
   - Option A : fix immédiat dans la session (avec plan concret)
   - Option B : acceptation explicite avec dette documentée (`Knowledge/dettes/<sujet>.md`)

4. **Attendre l'arbitrage utilisateur** — NE PAS ship/commit/promulguer avant décision explicite.

5. **Après fix** — vérifier que le fix couvre 100% du BLOCKING. PARTIAL ≠ PASS.

6. **Si dette acceptée** — créer la note via MCP :
   ```
   mcp__forge-brain__create_note(
     path="Knowledge/dettes/<sujet>.md",
     content="## Dette acceptée\n[Description BLOCKING]\n## Décision\nAcceptée par [user] le [date]\n## Remédiation prévue\n[plan ou N/A]"
   )
   ```

## Scoring 0-100 par issue (filtre faux positifs)

Le verdict global (BLOCKING / PARTIAL / PASS) reste inchangé. Le scoring raffine **quelles issues déclenchent l'arbitrage obligatoire**.

| Score | Signification |
|-------|--------------|
| 0     | Faux positif certain |
| 25    | Peut-être réel |
| 50    | Réel mais mineur |
| 75    | Réel et important |
| 100   | Certain, à corriger |

**Seuil par défaut : 80.** Issues < 80 = warning (logged, pas BLOCKING auto). Issues >= 80 = arbitrage user requis (logique étapes 2-4 ci-dessus).

### Filtres faux positifs (ne pas auto-BLOCK)

- Issues **pré-existantes** dans le code avant la session en cours
- Code "qui ressemble à un bug" mais comportement intentionnel documenté
- **Nitpicks pédantiques** sans impact fonctionnel ou sécu
- Issues **déjà détectées par les linters** (doublon, pas de valeur DA)
- Code avec annotation `lint ignore` / `# noqa` / équivalent explicite

### Application concrète

```
Issue 1 — Score 90 → BLOCKING → arbitrage obligatoire
Issue 2 — Score 75 → warning → logged dans Apprentissage (pas ship-blocking)
Issue 3 — Score 40 → filtré → ignoré
```

Si 0 issue >= 80, même si verdict DA = PARTIAL → pas d'arbitrage bloquant.

*Source : plugin code-review Anthropic, Boris Cherny — veille 26 mai 2026. Voir [[plugins-officiels-veille-2026-05-26]].*

## Gotchas

- **Verdict tronqué = non valide** — relancer DA avant d'agir sur un verdict incomplet.
- **PARTIAL fix ≠ PASS** — si le fix ne couvre pas tout le BLOCKING, c'est encore BLOCKING.
- **Auto-congratulation piège** — "j'ai fixé le principal" n'est pas un pass. Vérifier empiriquement.
- **Acceptation implicite interdite** — "on verra après" ou silence = BLOCKING encore ouvert.
- **BLOCKING 0 = ship libre** — si verdict DA = 0 BLOCKING, pas d'arbitrage requis.

## Apprentissage

Capitaliser dans ce fichier les patterns BLOCKING récurrents :

- Pattern 24-25 mai 2026 : doctrine meta-commentaires promulguée avec BLOCKING "CLAUDE.md viole déjà la règle" → drift garanti. Leçon : self-reference non résolue = dette structurelle, pas cosmétique.
- Chaque BLOCKING ignoré = [[feedback_doctrine_drift_pattern]] qui se reproduit.

Après chaque session avec DA BLOCKING :
```
mcp__forge-brain__append_note(
  file="Knowledge/erreurs/da-blocking-non-arbitre.md",
  content="## [DATE] — [sujet]\nBLOCKING : [desc]\nRésolution : [fix/dette/refus]"
)
```
