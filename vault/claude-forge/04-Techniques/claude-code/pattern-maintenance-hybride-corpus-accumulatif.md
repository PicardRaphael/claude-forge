---
titre: "Maintenance hybride d'un corpus accumulatif — déterministe + LLM + gate humaine"
resume: "Pattern canonique pour empêcher un corpus accumulatif (index mémoire, doctrine, FAQ, changelog) de se diluer : 3 couches déterministe (détection mécanique cheap) / LLM (clustering sémantique) / humain (gate [v]/[m]/[i] typée par section). Canonique vivante modifiable + archive append-only sacré. Anti enforcement-théâtre : pas de couche déterministe lourde sur corpus court/homogène."
aliases: ["maintenance hybride corpus", "pattern compaction mémoire", "déterministe llm gate humaine", "archive append-only canonique vivante", "clean-memory pattern", "maintenance données accumulatives", "architecture cognitive memory vault", "feedback ou note vault"]
type: technique
derniere-maj: 2026-06-07
auteur: claude
tags: ["#type/technique", "#domaine/claude-code", "#sujet/maintenance", "#doctrine/2026"]
---
# Maintenance hybride d'un corpus accumulatif

Tout corpus qui s'accumule par ajout (index mémoire `MEMORY.md`, notes de doctrine, FAQ, changelog, base de feedbacks) se dilue avec le temps : doublons conceptuels, amendements successifs non consolidés, items dormants. Sans maintenance, le signal se noie dans le volume et le coût de lecture croît. Ce pattern structure la maintenance sans automatisme aveugle.

## Principe — trois couches

| Couche | Rôle | Quand |
|--------|------|-------|
| **Déterministe** (script, grep) | Détection mécanique *cheap* : orphelins (fichier sans entrée index), citations entrantes, liens morts | Métriques objectives uniquement |
| **LLM** | Clustering **sémantique** : doublons conceptuels, amendements, ambigus à NE PAS fusionner, dormants | Le jugement, pas la mécanique |
| **Humain** | Gate `[v]/[m]/[i]` typée par section, `[m]` anti tout-ou-rien | Toute opération destructive |

Le LLM lit le corpus entier et regroupe mieux que toute heuristique lexicale sur corpus court/homogène — la couche déterministe se limite aux métriques objectives. Construire une couche déterministe lourde (Jaccard, ML) par-dessus une lecture LLM possible = **enforcement-théâtre** (cf [[llm-lit-court-homogene-pas-couche-deterministe]]). Mesurer que le LLM rate AVANT de construire l'aide.

## Architecture cognitive — trois acteurs

Le pattern de maintenance ci-dessus s'applique à un système à trois acteurs qu'il faut distinguer nettement avant tout choix d'écriture.

| Acteur | Rôle | Cible empirique |
|--------|------|-----------------|
| **`MEMORY.md`** (auto-chargé via `@import`) | Table des matières + déclencheurs critiques visibles à chaque session | ≤ 50 entrées tier-1 |
| **Vault canoniques** (`vault/claude-forge/`) | Source de vérité complète — wikilinks, MOC, recherche sémantique MCP, 438+ notes | Pas de plafond (corpus de connaissance) |
| **`memory/*.md`** (fichiers physiques) | Exceptions empiriques uniquement (cas précis non couvert vault) | ≤ 100 fichiers |

Le vault porte la **doctrine** (règle énoncée, réutilisable). `memory/*.md` porte les **cas empiriques précis** que la doctrine vault ne pourrait pas absorber sans dilution (ex : « brief annonçait baseline 319, mesuré 176, écart 143 »). `MEMORY.md` ne porte que les **déclencheurs** (1 ligne pointeur).

### Workflow décision — créer un nouveau feedback

Quatre étapes obligatoires AVANT toute création de fichier dans `memory/` :

1. **`search_brain`** sur le sujet dans le vault.
2. **Canonique vault existe ?** → pointeur 1 ligne dans `MEMORY.md`, pas de nouveau fichier `memory/`.
3. **Cas empirique précis non couvert vault ?** → feedback `memory/*.md` ciblé, tier-1 ou tier-2 selon impact.
4. **Sujet majeur sans canonique ET pattern récurrent (2-3 incidents observés) ?** → promouvoir vault d'abord (créer la note canonique), PUIS pointeur `MEMORY.md` vers elle. Si 1 seul incident isolé : garder en feedback `memory/*.md` jusqu'à récurrence.

### Template pointeur 1 ligne

```
- [slug-pointeur](pointer.md) — Cf [[note-vault-canonique]] (cas empirique : <une ligne si applicable>)
```

Le fichier pointeur est minimal : frontmatter + 2-3 lignes renvoyant à la canonique vault. Pas de duplication doctrinale.

### Exemples PASS / FAIL

- ✅ **PASS** — `feedback_claim_security_must_be_provable` pointeur 1 ligne vers [[hooks-conformite-audit-passif-continu]] (doctrine "by construction vs by discipline" est dans la note vault, le feedback ne garde que l'incident x-read 2026-05-20).
- ❌ **FAIL** — feedback verbeux qui réécrit la doctrine vault sans cas empirique unique = doublon (à fusionner / réduire à un pointeur).
- ✅ **PASS** — `feedback_verifier_claims_empiriquement` (cas empirique « sub-agent annonce 296L, fichier réel 211L ») : aucun équivalent vault, KEEP en feedback spécifique.
- ❌ **FAIL** — créer une note vault canonique sur la base d'**un seul** incident sans pattern récurrent prouvé = promotion prématurée. Garder en feedback `memory/*.md` jusqu'à 2-3 récurrences.

### Cibles empiriques mesurées (pilote 28 mai 2026)

Cartographie sur 274 fichiers `memory/*.md` et pilote 29 fichiers (clusters verify-empirique + advisor-da + audit-methode) :

- **38 %** de fichiers du pilote = doublon vault complet ou partiel (candidats PURGE/POINTEUR).
- **62 %** = cas empirique précis sans canonique vault équivalente (KEEP).
- Projection corpus complet : cible `memory/*.md` ≤ 100 fichiers, `MEMORY.md` ≤ 50 entrées tier-1 atteignable via amend chirurgical séquentiel (pas refonte massive).

Le hook `memory-saturation-watcher.py` (SessionStart, advisory) signale WARNING ≥ 80 fichiers, CRITICAL ≥ 100. Pas de blocage, advisory pure cohérent doctrine 22 mai (hooks lint/sécu, jamais workflow).

### Tension cible vs mesure (constat 2026-06-07)

Après tri du critère « cité ≥1 OU stratégique » sur les 38 entrées tier-1 **non citées** de la section Feedback (`MEMORY.md`) : **137 tier-1 retenus** (section Feedback 97 → 80, total MEMORY 154 → 137). L'écart avec la cible ≤ 50 suggère soit une cible trop optimiste, soit que les 59 entrées « citées ≥1 » — gardées en KEEP **automatique, jamais examinées** — méritent un second tri (cité ≠ stratégique).

Ni 50 ni 137 ne sont prouvés comme la bonne cible : le tri n'a porté que sur les non-cités. Le vrai chiffre juste est peut-être < 137 si on auditait aussi les 59 cités. **À trancher lors d'une passe dédiée** appliquant le critère stratégique aux 59 cités, pas seulement la présence d'une citation entrante. La cible ≤ 50 reste inchangée tant que cette mesure complète n'a pas été faite.

### Anti-patterns spécifiques

- **Création feedback sans `search_brain` vault préalable** → produit doublon mécaniquement.
- **Feedback memory qui réécrit la canonique vault** → la doctrine appartient au vault, le feedback ne porte que l'incident empirique.
- **Promotion vault prématurée** (1 incident → note canonique) → attendre 2-3 récurrences. La note canonique doit énoncer un pattern, pas raconter une histoire.
- **Accumulation sans curation** → tous les 1-2 mois, `/clean-memory` ou audit ciblé déclenché par hook CRITICAL.

## Architecture stockage

- **Canonique vivante** (`MEMORY.md`, note doctrine) : modifiable.
- **Archive append-only sacré** (`_archive/YYYY-MM/`) : jamais modifiée après écriture. Réversibilité totale.
- **Journal** (`MEMORY-archive-log.md`) : append-only, trace par opération (fichiers, raison, méta-feedback, rollback).

## Gate typée par section (critères LLM)

- **A — doublons conceptuels** → fusion (méta consolidé + archive originaux + aliases pour préserver backlinks)
- **B — amendements successifs** → fusion (le récent absorbe l'ancien)
- **C — ambigus** → **rejeter la fusion par défaut**, présenter la distinction, arbitrage. Fusionner deux concepts distincts pour gagner des lignes efface une nuance utile.
- **D — dormants** → archive solo ; non-cité = nécessaire mais NON suffisant, critère décisif = obsolescence/absorption prouvée.

## Méta-principe partagé avec doctrine-vivante

Même ADN que [[doctrine-vivante]] : **gate humaine non négociable + anti-scan-aveugle**. Différence de cible : doctrine-vivante fait évoluer *la doctrine* sur signal externe ; ce pattern empêche *un corpus accumulatif* de se diluer. Deux applications d'un même principe (l'humain tranche, le mécanisme propose).

## Cas empirique — clean-memory (27 mai 2026)

`MEMORY.md` 196 feedbacks. Couche déterministe a révélé 10 orphelins + 57% sans citation entrante (→ citation = mauvais critère d'archivage seul). LLM a proposé 3 fusions (claims, tests-adverses, jarvis) + 2 ambigus correctement rejetés. Gate humaine : 3 fusions validées, A4 ignoré (parent/spécialisation), C1/C2 séparés. Couche Python Jaccard initialement prévue puis **coupée** (enforcement-théâtre). Skill : `/clean-memory`.

## Wikilinks

- [[llm-lit-court-homogene-pas-couche-deterministe]] — anti enforcement-théâtre (fondement de la limite déterministe)
- [[doctrine-vivante]] — méta-principe partagé (gate humaine + anti-scan-aveugle)
- [[methode-pivoter-doctrine]] — autre application de gate humaine sur changement structurant
- [[pattern-mcp-brief-then-direct]] — skill = écritures MCP denses en session principale
- [[comment-creer-skill]] — skill de jugement LLM = validation par exécution, pas test unitaire
- [[memory-discipline]] — rule forge appliquant ce pattern sur `memory/*.md` (workflow décision)
- [[decision-memoire-dans-le-repo]] — ADR memory dans repo (architecture physique `<repo>/memory/`)

## Mesure corpus complet — clean-memory 2026-05-29

Première application du pattern au corpus **complet** (216 feedbacks, vs pilote 29 du 28 mai). Méthode : 3 Dynamic Workflows croisés (235 agents) — WF1 clustering doublons/dormants + verify, WF2 classification KEEP/POINTEUR/PURGE sur les 216, WF3 slim des POINTEUR verbeux + verify.

- **Répartition mesurée** : 94 KEEP (44%) / 73 POINTEUR (34%) / 49 PURGE (23%). Le pilote 29 projetait 62/28/10% — le corpus complet est nettement plus dilué (PURGE 23% vs 10%) : les feedbacks anciens accumulent plus de doublons-vault que l'échantillon récent du pilote.
- **Couche déterministe inopérante** : 0 orphelin, 0 lien mort, index parfaitement synchro (216 fichiers ↔ 215 entrées, écart = 1 faux positif de casse). Confirme [[llm-lit-court-homogene-pas-couche-deterministe]] : sur ce corpus, seule la classification LLM bouge l'aiguille, pas le grep mécanique.
- **Exécution option (b)** : 50 PURGE archivés (216→166 feedbacks) + 22 POINTEUR verbeux (>25L) slimmés en pointeurs enrichis (−502 lignes, −52%, zéro incident perdu, verify 22/22). Total racine 282→232.
- **Plancher structurel** : <100 fichiers hors d'atteinte par dedup feedbacks seul (94 KEEP + 44 reference + 18 project ≈ 158). Atteindre la cible exigerait de trier reference/project ou d'archiver les POINTEUR gardés — décision utilisateur, passe séparée.
- **Garde-fous validés** : tie-break sur divergence WF1/WF2 = bucket le moins destructif ; backlinks vault vérifiés cross-namespace (notation `[[>>> x <<<]]` = déjà danglant, archiver ne casse rien) ; commit phase PURGE avant slim in-place (restore point) ; gotcha workflow `args` array → [[workflow-args-array-gotcha]].
