---
name: doctrine-impact-check
description: 'ALWAYS invoke when a finding (leader URL, cc-news, or empirical measure) must be confronted with forge doctrine. Crosses it against canonical notes and emits one verdict: INFO, DOCTRINE_PIVOT_CANDIDATE, or DOCTRINE_REINFORCE.'
allowed-tools: Read, mcp__forge-brain__*
user-invocable: true
model: opus
---

# doctrine-impact-check

Cross a directed finding against forge canonical doctrine notes and emit a single verdict with a human gate.

## QUOI / QUAND â€” EntrÃ©e dirigÃ©e obligatoire

**EntrÃ©e** : un finding prÃ©cis fourni en `$ARGUMENTS` ou dans le message.

Formes valides :
- URL d'un article/post d'un leader reconnu (`05-Leaders/`) avec rÃ©sumÃ© de la conclusion
- Conclusion d'un run `cc-news` ("Anthropic vient de publier...")
- Mesure empirique forge ("j'ai testÃ© effort: high sur haiku, rÃ©sultat...")
- RÃ©sumÃ© de tweet avec lien source

**Si aucun finding fourni** : demander lequel. Ne PAS scanner le vault "au cas oÃ¹". Le scan aveugle produit 0 pivot utile (probe historique : 0/12).

## MÃ©thode â€” 3 Ã©tapes

### Ã‰tape 1 â€” Identifier le finding et Ã©valuer son crÃ©dit

Extraire du finding :
- La **claim prÃ©cise** (formulation courte, ce qui est affirmÃ©)
- La **source** : auteur, date, URL
- Le **niveau de crÃ©dit** :

| Source | CrÃ©dit |
|--------|--------|
| Anthropic officiel (platform.claude.com, docs.anthropic.com, blog officiel) | MAX â€” source de rÃ©fÃ©rence sur Claude/CC |
| Leader reconnu dans `05-Leaders/` du vault, sur son domaine d'expertise | Ã‰LEVÃ‰ |
| Mesure empirique forge (observÃ© dans cette session ou session citÃ©e avec donnÃ©es) | DÃ‰CISIF si reproductible |
| Article tiers, tweet paraphrasant sans lien primaire | INSUFFISANT â€” traiter INFO au mieux |

Si crÃ©dit INSUFFISANT â†’ verdict INFO immÃ©diat sans croiser les canoniques.

### Ã‰tape 2 â€” Croiser avec les notes canoniques de doctrine

PÃ©rimÃ¨tre : dossier vault `04-Techniques/claude-code/`.

SÃ©quence MCP :
1. `search_brain(query="<mots-clÃ©s du finding>", limit=5)` â€” identifier la ou les notes canoniques concernÃ©es
2. `read_note(file="<note canonique>")` â€” lire EN ENTIER la note pertinente (sans max_lines)

Notes canoniques cibles les plus frÃ©quemment impactÃ©es :
- `doctrine-vivante` â€” rÃ¨gles actives et leur statut
- `comment-creer-skill`, `comment-creer-agent`, `comment-creer-hook`, `comment-ecrire-claudemd`
- `workflow-claude-code-optimal`, `mcp-vs-skills-doctrine`
- `methode-pivoter-doctrine`, `methode-analyser-repo`
- `raisonnement-22mai-doctrine-vs-enforcement`
- `effort-opus-47-doctrine-anthropic-2026`

**Test de contradiction** : le finding affirme-t-il X quand la doctrine prescrit Â¬X sur un cas mesurable ?

- Oui, sur un point prÃ©cis â†’ **DOCTRINE_PIVOT_CANDIDATE**
- Non, confirme la doctrine â†’ **DOCTRINE_REINFORCE**
- Pas d'intersection doctrine â†’ **INFO**

### Ã‰tape 3 â€” Ã‰mettre le verdict et activer la gate

PrÃ©senter selon le format de verdict ci-dessous, puis attendre `[v] / [m] / [i]`.

---

## Les 3 verdicts

### INFO

Le finding apporte un fait nouveau sans intersection avec une doctrine canonique.

```
Verdict : INFO
Finding : [claim courte]
Source : [URL/auteur] â€” CrÃ©dit : [niveau]
Recommandation : capitaliser comme note de fait dans vault/06-Industrie/ ou 04-Techniques/ selon le sujet.
Aucun pivot doctrinal.
```

### DOCTRINE_PIVOT_CANDIDATE

Le finding contredit une doctrine canonique sur un point prÃ©cis et mesurable.

PrÃ©senter le brouillon ci-dessous, puis la gate :

```
Verdict : DOCTRINE_PIVOT_CANDIDATE

## Brouillon de pivot doctrinal â€” Ã€ VALIDER

**Doctrine actuelle** : [note canonique + position actuelle citÃ©e verbatim ou rÃ©sumÃ©e fidÃ¨lement]
**Source externe** : [URL/source + crÃ©dit + date]
**Contradiction observÃ©e** : [ce que le finding affirme qui contredit la doctrine]
**Position proposÃ©e** : [nouvelle doctrine suggÃ©rÃ©e â€” prÃ©cise, pas gÃ©nÃ©rique]
**Notes canoniques impactÃ©es** : [liste des notes Ã  modifier si pivot validÃ©]

[v]alider â†’ lancer methode-pivoter-doctrine sur cette base
[m]odifier â†’ ajuster le brouillon
[i]gnorer â†’ ne rien faire (finding notÃ© INFO au mieux)
```

- `[v]` â†’ la session principale lancera ensuite `/methode-pivoter-doctrine` avec ce brouillon comme input
- `[m]` â†’ attendre la version ajustÃ©e, re-prÃ©senter, puis `[v]` ou `[i]`
- `[i]` â†’ aucune Ã©criture

### DOCTRINE_REINFORCE

Le finding confirme une doctrine canonique existante.

```
Verdict : DOCTRINE_REINFORCE
Finding : [claim courte]
Source : [URL/auteur â€” CrÃ©dit : niveau]
Doctrine confirmÃ©e : [note canonique + passage confirmÃ©]
Proposition : tracer "challengÃ©e + confirmÃ©e le {date} par {source}" sur [note canonique].

[v]alider â†’ Ã©crire la trace sur la note canonique via append_note
[m]odifier â†’ ajuster le libellÃ© de la trace
[i]ignorer â†’ ne rien Ã©crire
```

---

## Gotchas

- **Jamais scanner le vault sans finding dirigÃ©** â€” si l'utilisateur dit "vÃ©rifie si quelque chose dans le vault est impactÃ©", demander d'abord quel finding dÃ©clenche la vÃ©rification.
- **CrÃ©dit insuffisant = INFO direct** â€” ne pas construire un brouillon de pivot sur un tweet sans source primaire. Le crÃ©dit insuffisant n'invalide pas l'info, il empÃªche le pivot.
- **Un finding = un verdict** â€” ne pas produire DOCTRINE_PIVOT_CANDIDATE + INFO en mÃªme temps. Trancher.
- **Ne jamais appeler methode-pivoter-doctrine directement** â€” `[v]` sur DOCTRINE_PIVOT_CANDIDATE signale Ã  la session principale de le faire ; cette skill ne l'invoque pas.
- **Gate obligatoire** â€” rien n'est Ã©crit (ni trace REINFORCE, ni brouillon enregistrÃ©) avant que l'utilisateur tape `[v]`. PrÃ©senter d'abord, Ã©crire ensuite.
- **read_note sans max_lines** â€” lire la note canonique EN ENTIER pour ne pas rater une nuance qui invaliderait la contradiction supposÃ©e.

---

## Apprentissage

AprÃ¨s chaque verdict DOCTRINE_PIVOT_CANDIDATE validÃ© :
- MÃ©moriser le pattern de finding dÃ©clencheur (quel type de source, quel domaine) dans `memory/project_*.md` si c'est une tendance rÃ©currente.
- Si la mÃªme note canonique est impactÃ©e 3 fois en pivot, proposer une rÃ©vision structurelle de cette note.

---

## TODO â€” extensions diffÃ©rÃ©es

Ces extensions ne sont PAS implÃ©mentÃ©es. Ã€ activer quand les conditions ci-dessous sont rÃ©unies.

**C5 (fraÃ®cheur)** : ajouter une propriÃ©tÃ© frontmatter `derniere-challenge: YYYY-MM-DD` sur la note canonique concernÃ©e, mise Ã  jour TRIGGERED-BY-EVENT uniquement (quand cette skill produit un PIVOT validÃ© ou un REINFORCE) â€” JAMAIS en bulk init (sinon "lying data"). Ã€ activer quand l'usage rÃ©el le justifie.

**C6 (mÃ©ta-doctrine)** : ajouter UNE ligne dans la checklist de `methode-pivoter-doctrine` ("noter la limite de l'ancienne doctrine + la source externe dÃ©clencheuse dans le raisonnement"). PAS de nouveau dossier. Ã€ faire aprÃ¨s 2-3 pivots rÃ©els observÃ©s.

**C7 (arbitrage conflits experts)** : crÃ©er une skill `doctrine-arbitrate-conflict` au PREMIER conflit empirique rÃ©el entre deux leaders reconnus sur un mÃªme point doctrinal. Defer jusqu'Ã  occurrence.
