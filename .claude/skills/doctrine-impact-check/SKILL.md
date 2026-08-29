---
name: doctrine-impact-check
description: ALWAYS invoke when a finding (leader URL, cc-news, or empirical measure) must be confronted with forge doctrine. Crosses it against canonical notes and emits one verdict — INFO, DOCTRINE_PIVOT_CANDIDATE, or DOCTRINE_REINFORCE.
allowed-tools: Read, mcp__forge-brain__search_brain, mcp__forge-brain__read_note, mcp__forge-brain__read_note_by_path, mcp__forge-brain__read_section, mcp__forge-brain__list_notes
user-invocable: true
model: opus
---

# doctrine-impact-check

Cross a directed finding against forge canonical doctrine notes and emit a single verdict with a human gate.

## QUOI / QUAND — Entrée dirigée obligatoire

**Entrée** : un finding précis fourni en `$ARGUMENTS` ou dans le message.

Formes valides :
- URL d'un article/post d'un leader reconnu (`05-Leaders/`) avec résumé de la conclusion
- Conclusion d'un run `cc-news` ("Anthropic vient de publier...")
- Mesure empirique forge ("j'ai testé effort: high sur haiku, résultat...")
- Résumé de tweet avec lien source

**Si aucun finding fourni** : demander lequel. Ne PAS scanner le vault "au cas où". Le scan aveugle produit 0 pivot utile (probe historique : 0/12).

## Méthode — 3 étapes

### Étape 1 — Identifier le finding et évaluer son crédit

Extraire du finding :
- La **claim précise** (formulation courte, ce qui est affirmé)
- La **source** : auteur, date, URL
- Le **niveau de crédit** :

| Source | Crédit |
|--------|--------|
| Anthropic officiel (platform.claude.com, docs.anthropic.com, blog officiel) | MAX — source de référence sur Claude/CC |
| Leader reconnu dans `05-Leaders/` du vault, sur son domaine d'expertise | ÉLEVÉ |
| Mesure empirique forge (observé dans cette session ou session citée avec données) | DÉCISIF si reproductible |
| Article tiers, tweet paraphrasant sans lien primaire | INSUFFISANT — traiter INFO au mieux |

Si crédit INSUFFISANT → verdict INFO immédiat sans croiser les canoniques.

### Étape 2 — Croiser avec les notes canoniques de doctrine

Périmètre : dossier vault `04-Techniques/claude-code/`.

Séquence MCP :
1. `search_brain(query="<mots-clés du finding>", limit=5)` — identifier la ou les notes canoniques concernées
2. `read_note(file="<note canonique>")` — lire EN ENTIER la note pertinente (sans max_lines)

Notes canoniques cibles les plus fréquemment impactées :
- `doctrine-vivante` — règles actives et leur statut
- `comment-creer-skill`, `comment-creer-agent`, `comment-creer-hook`, `comment-ecrire-claudemd`
- `workflow-claude-code-optimal`, `mcp-vs-skills-doctrine`
- `methode-pivoter-doctrine`, `methode-analyser-repo`
- `raisonnement-22mai-doctrine-vs-enforcement`
- `effort-opus-47-doctrine-anthropic-2026`

**Test de contradiction** : le finding affirme-t-il X quand la doctrine prescrit ¬X sur un cas mesurable ?

- Oui, sur un point précis → **DOCTRINE_PIVOT_CANDIDATE**
- Non, confirme la doctrine → **DOCTRINE_REINFORCE**
- Pas d'intersection doctrine → **INFO**

### Étape 3 — Émettre le verdict et activer la gate

Présenter selon le format de verdict ci-dessous, puis attendre `[v] / [m] / [i]`.

---

## Les 3 verdicts

### INFO

Le finding apporte un fait nouveau sans intersection avec une doctrine canonique.

```
Verdict : INFO
Finding : [claim courte]
Source : [URL/auteur] — Crédit : [niveau]
Recommandation : capitaliser comme note de fait dans vault/06-Industrie/ ou 04-Techniques/ selon le sujet.
Aucun pivot doctrinal.
```

### DOCTRINE_PIVOT_CANDIDATE

Le finding contredit une doctrine canonique sur un point précis et mesurable.

Présenter le brouillon ci-dessous, puis la gate :

```
Verdict : DOCTRINE_PIVOT_CANDIDATE

## Brouillon de pivot doctrinal — À VALIDER

**Doctrine actuelle** : [note canonique — chemin exact + passage cité VERBATIM, jamais résumé]
**Source externe** : [URL/source + crédit + date]
**Contradiction observée** : [ce que le finding affirme qui contredit la doctrine]
**Position proposée** : [nouvelle doctrine suggérée — précise, pas générique]
**Notes canoniques impactées** : [liste des notes à modifier si pivot validé]

[v]alider → lancer methode-pivoter-doctrine sur cette base
[m]odifier → ajuster le brouillon
[i]gnorer → ne rien faire (finding noté INFO au mieux)
```

- `[v]` → la session principale lancera ensuite `/methode-pivoter-doctrine` avec ce brouillon comme input
- `[m]` → attendre la version ajustée, re-présenter, puis `[v]` ou `[i]`
- `[i]` → aucune écriture

### DOCTRINE_REINFORCE

Le finding confirme une doctrine canonique existante.

```
Verdict : DOCTRINE_REINFORCE
Finding : [claim courte]
Source : [URL/auteur — Crédit : niveau]
Doctrine confirmée : [note canonique + passage confirmé]
Proposition : tracer "challengée + confirmée le {date} par {source}" sur [note canonique].

[v]alider → écrire la trace sur la note canonique via append_note
[m]odifier → ajuster le libellé de la trace
[i]ignorer → ne rien écrire
```

---

## Gotchas

- **Jamais scanner le vault sans finding dirigé** — si l'utilisateur dit "vérifie si quelque chose dans le vault est impacté", demander d'abord quel finding déclenche la vérification.
- **Crédit insuffisant = INFO direct** — ne pas construire un brouillon de pivot sur un tweet sans source primaire. Le crédit insuffisant n'invalide pas l'info, il empêche le pivot.
- **Un finding = un verdict** — ne pas produire DOCTRINE_PIVOT_CANDIDATE + INFO en même temps. Trancher.
- **Ne jamais appeler methode-pivoter-doctrine directement** — `[v]` sur DOCTRINE_PIVOT_CANDIDATE signale à la session principale de le faire ; cette skill ne l'invoque pas.
- **Gate obligatoire** — rien n'est écrit (ni trace REINFORCE, ni brouillon enregistré) avant que l'utilisateur tape `[v]`. Présenter d'abord, écrire ensuite.
- **read_note sans max_lines** — lire la note canonique EN ENTIER pour ne pas rater une nuance qui invaliderait la contradiction supposée.
- **Pas de contradiction sur un résumé** — une doctrine paraphrasée fabrique des contradictions qui n'existent pas dans le corps. Citer la ligne verbatim de la canonique ET la phrase verbatim de la source, lue dans sa section (un texte à l'intérieur d'un bloc d'exemple n'est pas une assertion de l'auteur). Vérifier aussi le périmètre de la source : une consigne cadrée pour un modèle donné ne vaut pas pour un autre. Si les deux citations ne peuvent pas être produites → verdict **INFO**, jamais PIVOT.

---

## Apprentissage

Après chaque verdict DOCTRINE_PIVOT_CANDIDATE validé :
- Mémoriser le pattern de finding déclencheur (quel type de source, quel domaine) dans `memory/project_*.md` si c'est une tendance récurrente.
- Si la même note canonique est impactée 3 fois en pivot, proposer une révision structurelle de cette note.

---

## TODO — extensions différées

Ces extensions ne sont PAS implémentées. À activer quand les conditions ci-dessous sont réunies.

**C5 (fraîcheur)** : ajouter une propriété frontmatter `derniere-challenge: YYYY-MM-DD` sur la note canonique concernée, mise à jour TRIGGERED-BY-EVENT uniquement (quand cette skill produit un PIVOT validé ou un REINFORCE) — JAMAIS en bulk init (sinon "lying data"). À activer quand l'usage réel le justifie.

**C6 (méta-doctrine)** : ajouter UNE ligne dans la checklist de `methode-pivoter-doctrine` ("noter la limite de l'ancienne doctrine + la source externe déclencheuse dans le raisonnement"). PAS de nouveau dossier. À faire après 2-3 pivots réels observés.

**C7 (arbitrage conflits experts)** : créer une skill `doctrine-arbitrate-conflict` au PREMIER conflit empirique réel entre deux leaders reconnus sur un même point doctrinal. Defer jusqu'à occurrence.
