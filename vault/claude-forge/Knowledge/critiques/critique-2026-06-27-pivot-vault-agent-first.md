---
titre: "Critique — Plan pivot vault agent-first (Karpathy échafaudage dépassé)"
type: knowledge
domaine: claude-code
derniere-maj: 2026-06-27
auteur: claude
tags:
  - "#type/critique"
  - "#domaine/claude-code"
  - "#domaine/vault"
sources:
  - "[[decision-vault-agent-first]]"
  - "[[pattern-vault-llm-karpathy]]"
  - "[[methode-pivoter-doctrine]]"
aliases:
  - "critique pivot vault agent-first"
  - "DA pivot agent-first 27 juin"
  - "critique 2026-06-27 vault agent-first"
  - "verdict devils-advocate pivot vault"
  - "critique suppression raw layer"
---

## Devils Advocate — Plan pivot vault agent-first

**Intention déclarée :** purger le drift résiduel de la décision agent-first (raw/ supprimé, MOCs non auto-maintenus, 3-layers caducs) sur 6 foyers / 13 chirurgies sans effacer la trace historique.

### Verdict

**Bloquants : 1 | Avertissements : 4 | Nitpicks : 1**
**Décision : LIVRER AVEC CORRECTIONS.** Le plan échoue sa propre barre "zéro drift résiduel" — l'énumération des foyers est incomplète. C'est exactement le failure mode que methode-pivoter-doctrine existe pour attraper. Fix peu coûteux (ajouter foyers), donc pas BLOQUER, mais ne pas shipper le plan à 6 foyers tel quel.

### BLOQUANT (score 90) — Énumération de foyers incomplète

Au moins **5 foyers manqués**, prouvés empiriquement (search_brain large + grep `.claude/` + lint_vault) :

1. **`04-Techniques/patterns/LLM Wiki.md`** (note séparée, derniere-maj 2026-05-23) — "Ce vault implémente le pattern Karpathy : 3 layers (raw/wiki/schema)" = FAUX désormais. Aussi "3 layers : raw/ (sources immuables)..." dans Specs verbatim. NON couvert.
2. **`index.md` (racine)** — DEUX claims présent-actuel : nav par dossier "raw/ — sources immuables (Karpathy layer 1) : ... (8)" + métadonnées "Pattern : Karpathy LLM Wiki (3-layers raw/wiki/schema)". C'est de l'ORIENTATION courante, pas de la trace → MUST correct. NON couvert.
3. **`00-Hub/Home.md`** — resume "340+ notes pattern Karpathy 3-layers" + "[[pattern-vault-llm-karpathy]] — 3-layers + index.md + log.md". NON couvert.
4. **`.claude/rules/forge-brain-proactive.md:58`** — "SCHEMA.md (13 dossiers wiki + Knowledge/ + raw/)". Le plan foyer 5 ne mentionne QUE cette même ligne... mais c'est dans un AUTRE fichier que celui listé. À vérifier : le plan vise-t-il bien forge-brain-proactive ou un autre ? Doublon de ligne identique à traiter.
5. **`.claude/skills/forge-brain/SKILL.md`** — body décrit "Pattern Karpathy opérationnel" + anti-patterns Karpathy + "Layer Karpathy strict". NON couvert. (Édition via skill-creator car delegate-guard.)

**Sous-insuffisance — `mcp-vault-llm-design` (foyer 4, plan = 1 chirurgie)** : raw/ apparaît ≥2× (mention inline "raw/ — sources externes immuables" ET bloc "Layer Karpathy strict : raw/ — sources externes immuables, LLM ne touche pas"). 1 chirurgie insuffisante. Note aussi un wikilink mort `[[old]]` préexistant (hors scope).

### AVERTISSEMENT (score 70) — Wikilink mort raw/ confirmé (Q4)

`lint_vault` confirme : `[[pattern-vault-llm-karpathy]] -> [[recherche-karpathy-vault-canonique]]` pointe vers un fichier raw/ `git rm`. Le plan ne prévoit AUCUN nettoyage de lien raw/ mort. La note pattern elle-même cite ce lien dans sa section DRIFT. Recommandation : texte nu (pas crochets) pour ce nom mort, conformément au gotcha lint documenté dans mcp-vault-llm-design (noms morts en `[[]]` = re-injectés comme cassés à chaque scan).

### AVERTISSEMENT (score 75) — Palimpseste pattern-vault-llm-karpathy (Q3)

Après 2.1-2.4, la note empile 3 états temporels CONTRADICTOIRES sur raw/ : DRIFT "ABANDONNÉ" → REQUALIFICATION "écart assumé, NON supprimé, rouvrir si incident" → pivot "SUPPRIMÉ, délibéré". Les 4 caveats inline dispersés aggravent. Recommandation : UN bandeau autoritaire en tête `## STATUT 2026-06-27 — agent-first (supersede les analyses drift/requalification ci-dessous)` qui cadre les sections anciennes comme trace dépassée, plutôt que 4 caveats qui se contredisent. Note : le trigger de réouverture REQUALIFICATION ("1er incident hallucination source non archivée") devient sans objet une fois raw/ supprimé — le plan 2.4 le conserve comme "condition de falsification" mais une condition de réouverture d'un dossier fermé par suppression n'a plus de sens identique : à reformuler en "si besoin fiabilité émerge, re-créer raw/", pas "rouvrir l'arbitrage".

### AVERTISSEMENT (score 80) — Ordre A-puis-B : drift doctrine↔réel frais (Q5)

A-avant-B (doctrine avant retrait code FOLDER_TO_MOC) défendable SI les notes réécrites formulent en termes d'INTENTION ("MOCs ne doivent plus être auto-maintenus, retrait code = ÉTAPE B tracée"). MAIS `FOLDER_TO_MOC` tourne encore dans `vault-audit/scripts/audit.py:62` ET `fix.py:35`. Si une note réécrite affirme au présent factuel "les MOCs ne sont PAS auto-maintenus" pendant que le code les auto-maintient → c'est précisément le drift doctrine↔réel que le vault documente en boucle (cf doctrine-drift-silent-regression). Discriminateur bloquant : aucune note ne doit énoncer comme fait présent ce que le code contredit. Phraser au futur/intention + tracker ÉTAPE B avec déclencheur.

### Q2 — Sur-correction : caveat OK, NE PAS scinder

L'approche caveat "forge-brain exception" est CORRECTE. Le pattern Karpathy générique reste valide pour neo_ia/neoteem-brain (autres vaults). Ne PAS éviscérer la note pattern ni la scinder. Seul `LLM Wiki.md` a UNE phrase forge-spécifique fausse à corriger — le reste de cette note est générique et juste. L'orchestrateur ne doit PAS sur-lire cette critique comme "abandonner le pattern".

### NITPICK — CHANGELOG + Home.derniere-maj

Vérifier que le plan inclut une entrée CHANGELOG.md datée 2026-06-27 (rule changelog-vault obligatoire). Home.md derniere-maj figé 2026-05-24.

### Si je devais le faire marcher

1. Étendre à **11 foyers** : ajouter LLM Wiki.md, index.md racine, Home.md, SKILL.md forge-brain ; corriger mcp-vault-llm-design en ≥2 chirurgies ; vérifier la ligne forge-brain-proactive.
2. Bandeau STATUT unique en tête de pattern-vault-llm-karpathy au lieu de 4 caveats.
3. Nettoyer le wikilink mort `recherche-karpathy-vault-canonique` (texte nu).
4. Phraser les claims MOC au futur/intention tant que FOLDER_TO_MOC tourne ; tracker ÉTAPE B.
5. Entrée CHANGELOG datée.
6. Re-grep `.claude/` après corrections pour prouver zéro survivance "raw immuable / 3-layers actuel".
