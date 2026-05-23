# Template commun — Audit thématique vault forge

> **Ce template est intégré dans chaque prompt thématique (01 à 07).** Lire ici les règles partagées.

## OBJECTIF

Pour le thème ciblé, **valider à 2000%** chaque note vault :
- Aucune claim sans **minimum 4 sources convergentes** (sites + vidéos + papers + tweets + LinkedIn + slides)
- Hiérarchie experts respectée (Anthropic team > tous pour Claude Code, autres hiérarchies adaptées par thème)
- Propagation : après nettoyage notes, vérifier skills/agents/hooks/CLAUDE.md qui les utilisent

## RÈGLES ABSOLUES (toutes thématiques)

### Règle 1 — Minimum 4 sources convergentes par claim
- 4 sources INDÉPENDANTES (auteurs différents, canaux différents, dates différentes)
- < 4 → marquer `⚠️ Single source` ou `❌ Mythe`
- Pas d'invention. Pas de "probablement". Pas de paraphrase présentée comme verbatim.

### Règle 2 — Hiérarchie de priorité (adaptée par thème)
Voir chaque prompt thématique pour la hiérarchie spécifique. Pattern général :
1. **Source officielle du provider/framework** (Anthropic, OpenAI, Google, LangChain, etc.)
2. **Team verbatim** sur talk public, podcast, post
3. **Experts reconnus du domaine** (validés étape 0)
4. **Papers académiques** (arXiv, conférences)
5. **Articles tiers convergents**

### Règle 3 — Sources exhaustives à fouiller

**Web** :
- WebSearch 3-5 requêtes variées par claim
- WebFetch sources candidates
- Defuddle pour extraction markdown propre
- Archive.org si URL morte

**Vidéos** :
- Skill `watch` pour YouTube transcripts (talks, podcasts, conférences)
- yt-dlp si watch insuffisant
- Whisper local si pas de transcript auto

**Papers** :
- arXiv search
- pypdf / pdfplumber pour parser PDFs
- pytesseract pour OCR images dans PDFs (slides scannées)

**GitHub** :
- `gh api repos/...` pour fouiller configs/READMEs/releases
- Commits + issues + discussions

**Social** :
- X.com / Twitter (threads experts)
- LinkedIn posts
- Bluesky / Mastodon si actif

**Scripts Python custom (AUTORISÉ et ENCOURAGÉ)** :
Si tu dois traiter > 20 sources, créer ton propre script Python dans `output/scripts-verif-canoniques/`. Exemples : scraper docs récursif, extracteur transcripts batch, parser PDFs en lot. Ne pas hésiter à écrire 200-500 lignes de scraper si ça permet de vérifier 50 claims d'un coup.

### Règle 4 — Citation verbatim obligatoire
Chaque source = citation verbatim + URL exacte (timestamp si vidéo). Stocker dans `output/audit-vault-thematique/<theme>/sources-collected.md`.

### Règle 5 — Honnêteté intellectuelle absolue
- "single source" → garder avec disclaimer `⚠️ Single source — [auteur], [date], [URL]`
- "mythe / extrapolation" → `❌ NON CANONIQUE — pas de source identifiable, extrapolation forge`
- "convergence partielle (2-3)" → `⚠️ Convergence partielle (N sources)`

Pas d'invention. Si pas sûr, dis-le.

## MÉTHODE A → B → C → D → E (récursive sur le vault)

### ÉTAPE 0 — VALIDER LISTE D'EXPERTS RECONNUS

Avant l'audit, valider la **liste des experts** dont on accepte les sources pour ce thème.

**Action** :
1. Lire la liste actuelle (fournie dans le prompt thématique)
2. WebSearch pour :
   - Manque-t-on des experts (vérifier sur Twitter, LinkedIn, conferences, awards récents) ?
   - Notre liste est-elle dépassée (certains ont perdu en crédibilité) ?
   - Biais géographique (que des US/anglophones) ?
3. Sortir liste finale : **chaque expert validé par 3+ mentions par autres experts ou contributions officielles vérifiées**

C'est cette liste qui sert ensuite à valider les claims.

### A. EXTRAIRE toutes les claims des notes du thème

Pour CHAQUE note du thème :
1. `mcp__forge-brain__read_note(file="<nom>")` SANS `max_lines`
2. Lister chaque claim numérique, verbatim, ou règle forte :
   - Chiffres (seuils, métriques, stats)
   - Verbatim (citations attribuées)
   - Règles fortes (recommandations canoniques)
   - Stats benchmark
   - Convergences citées

Sortir : `output/audit-vault-thematique/<theme>/A-inventaire-claims.md`

### B. VÉRIFIER chaque claim (4+ sources, sauf Anthropic = single source)

> **Méthode validée audit Claude Code 23 mai 2026** — cf mémoire forge `feedback_audit_thematique_methode`. Méthode obligatoire pour tous les thèmes restants (02 à 07 + 08 dogfooding).

#### B.1 — Checkpoint write OBLIGATOIRE avant lancer B

**Sauvegarder `A-inventaire-claims.md` AVANT lancer les sub-agents phase B.** Si la session crashe pendant les sub-agents (5-10 min chacun), tu repars de l'inventaire. Si tu sautes ce checkpoint et perds la session, tout est à refaire.

#### B.2 — Lecture parallèle SANS sub-agents pour phase A

Read_note des N notes en parallèle depuis session principale = 1 message. **Pas de sub-agents par note pour la lecture** — sinon 10 formats différents et claims dupliquées (un même claim apparaît dans plusieurs notes, tu vérifies N fois).

#### B.3 — Sub-agents par CLUSTER thématique (PAS par note)

Découper les claims en **5-7 clusters thématiques** (verbatim Anthropic team / chiffres benchmarks / repos GitHub publics / verbatim externes reconnus / etc.). Lancer **1 sub-agent par cluster en parallèle**, avec brief structuré :

```
1. CLAIM verbatim (texte exact à vérifier)
2. URLs candidates pré-identifiées (issues de phase 0 + recherche initiale)
3. Format de sortie IMPOSÉ (statut + sources + verbatim cités + URLs)
```

Sans (2)+(3) tu reçois N rapports incohérents qu'il faudra reformater.

#### B.4 — Hiérarchie de validation (adaptée par thème)

**Principe général** : auteur/provider officiel sur SON propre produit ou SA propre recherche = single source acceptable. Hors de son scope = règle 4+ sources.

| Source | Suffit pour ✅ CANONIQUE |
|--------|--------------------------|
| **Provider/auteur officiel sur SON produit ou SA recherche** | **Single source suffit** |
| Exemples : Anthropic sur Claude, OpenAI sur GPT, Karpathy sur ses propres patterns, Dettmers sur QLoRA, Reimers sur Sentence-BERT, Willison sur lethal trifecta | |
| **Papers académiques peer-reviewed** (arXiv conférences ACL/EMNLP/NeurIPS/ICML) | Single source suffit |
| **Docs officielles** d'un framework (LangChain, CrewAI, LangGraph, Unsloth, etc.) sur LEUR produit | Single source suffit |
| **LinkedIn/X officiel d'un leader** sur son propre rôle/affiliation | Single source suffit |
| **Externes/tiers** parlant d'un sujet hors de leur scope | **4+ sources convergentes obligatoire** |
| Couverture presse tech reconnue (Fortune, MIT Tech Review, TechCrunch) | 2+ sources convergentes |
| Articles tiers / blogs / Medium / DEV community | 4+ sources convergentes |

**⚠️ Piège à éviter** : ne pas faire de "Anthropic single source" une règle absolue cross-thèmes. Anthropic n'est canonique que pour Claude/Anthropic. Pour le prompt engineering général, RAG, fine-tuning, etc. — les meilleurs du domaine (qui ne sont pas chez Anthropic) sont les sources primaires.

**Chaque prompt thématique (02 à 07)** liste explicitement ses sources primaires par domaine.

#### B.5 — Verdict par claim

```
✅ CANONIQUE — verbatim attesté source primaire (Anthropic ou ≥ 4 externes)
⚠️ PARTIEL — 2-3 sources convergentes externes
⚠️ SINGLE SOURCE — 1 source externe (citer + disclaimer)
❌ NON CANONIQUE — 0 source ou paraphrase présentée comme verbatim
```

#### B.6 — Méthode anti-régression : `WebFetch` direct avant relayer

Tout verbatim Anthropic présumé doit être **fetch directement** sur docs.claude.com / code.claude.com / anthropic.com avant relayage. Pattern d'erreur récurrent : paraphrase pédagogique présentée comme citation (cf erreur "Claude decides when to parallelize" audit 23 mai).

Sortir : `output/audit-vault-thematique/<theme>/B-verifications.md` (1 fichier par cluster recommandé : `B-verif-cluster1-anthropic.md`, etc.)

### C. CROISER claims vs vérifications

Tableau par note vault :
```
| Note | Claim | Statut | Sources convergentes | Citations verbatim |
```

Sortir : `output/audit-vault-thematique/<theme>/C-croisement.md`

### C-bis. SELF-VERIFY les FAUX à fort impact AVANT phase D

> **Étape critique validée audit 23 mai** — les sub-agents se trompent (cf mémoire `feedback_auditor_false_positives`).

Pour chaque claim marquée ❌ NON CANONIQUE ou correction structurelle proposée par sub-agent dont l'impact est élevé (fondation doctrinale, attribution majeure, chiffre cité dans plusieurs notes) :

1. **Refetch directement** la source primaire via WebFetch (docs Anthropic, blog officiel, gist auteur)
2. **Vérifier verbatim** ce que dit réellement le passage cité
3. **Distinguer** :
   - Sub-agent confirmé FAUX → Type 3 réécriture
   - Sub-agent partiellement faux (principe juste, source mal citée) → Type 1 correction source
   - Sub-agent faux (concept était canonique, formule paraphrasée) → Type 1 reformulation

Si tu ne self-verifies pas, tu réécris des fondations correctes sur la foi de sub-agents qui ont parsé trop vite. Coût : 30-45 min de WebFetch en parallèle.

### D. PLAN correction par note — distinguer 3 types d'erreur

**Distinguer 3 types** (méthode validée audit 23 mai) :

| Type | Nature | Action |
|------|--------|--------|
| **Type 1** | Citation/date/attribution fausse, **principe juste** | Corriger source, garder concept |
| **Type 2** | Chiffre inventé / mesure non sourcée | Remplacer par qualitatif ou retirer |
| **Type 3** | Doctrine fausse au fond | Réécrire section |

Pour chaque note vault, actions priorisées :
- **Garder telle quelle** : claims ✅ canoniques
- **Type 1** : `⚠️ Single source — [source]` ou correction source précise
- **Type 2** : retirer chiffre ou remplacer par qualitatif
- **Type 3** : réécrire complètement la section (`update_note` MCP)
- **Marquer mythe** : `❌ NON CANONIQUE — extrapolation` si principe non sourcé
- **Supprimer** : si claim fausse contredite par source canonique

**Plan par vagues** (cf advisor 23 mai) :
1. **Vague 1** — Type 2 safe (chirurgies chiffres/sources faciles) : autonomes, peu de risque
2. **Vague 2** — Type 1 drift attribution : nécessite vérif croisée mais mécanique
3. **Vague 3** — Type 3 structurel : nécessite advisor() + DA AVANT exécution

Sortir : `output/audit-vault-thematique/<theme>/D-plan-correction.md`

### E. EXÉCUTER après advisor()

**STOP** avant la moindre modification vault.

1. `advisor()` avec tout le contexte (A + B + C + D)
2. Présenter à Raphael rapport global :
   - N claims auditées
   - X validées, Y partielles, Z mythes
   - Liste détaillée des modifs par note
3. **Raphael valide commit par commit** (note par note)
4. Appliquer via `mcp__forge-brain__update_note` ou `insert_section`
5. Commit final vault

## ÉTAPE F — PROPAGATION (NOUVELLE, OBLIGATOIRE)

**Après chaque note vault corrigée**, vérifier les composants qui s'en servent et les mettre à jour si nécessaire.

### Actions étape F

1. **Identifier les utilisateurs de la note** :
   ```
   grep -r "<nom-note-corrigée>" forge/.claude/ neot-v2/*/. claude/ output/
   ```
   Lister tous les fichiers qui citent la note (skills, agents, hooks, rules, CLAUDE.md, autres notes vault).

2. **Pour chaque utilisateur trouvé** :
   - Vérifier s'il référence des claims `❌ NON CANONIQUE` ou `⚠️ Single source`
   - Si oui → mettre à jour le composant (ajouter disclaimer ou retirer la mention)

3. **Backlinks vault** :
   ```
   mcp__forge-brain__get_backlinks(file="<nom-note-corrigée>")
   ```
   Vérifier autres notes vault qui pointent vers cette note. Mettre à jour si nécessaire.

4. **Test comportemental** (si modifs significatives) :
   - Générer un prompt PASS/FAIL en session fraîche
   - Vérifier que les composants modifiés routent correctement avec les nouvelles règles

5. **Présenter rapport propagation** à Raphael :
   - N composants identifiés comme utilisateurs
   - X mis à jour
   - Y intacts (pas d'impact)
   - Test comportemental PASS/FAIL

### Pourquoi étape F

Sans propagation : on corrige une note vault, mais les skills/agents/hooks qui citent ses claims périmées **continuent à diffuser le mythe**. Le vault devient incohérent.

Single source of truth = note vault canonique + composants qui pointent vers elle (pas duplication).

## RÈGLES ABSOLUES POUR LE RUN

- ❌ AUCUNE modif vault avant validation Raphael note par note
- ❌ AUCUNE invention de citation ou source
- ❌ AUCUNE paraphrase présentée comme verbatim Anthropic (pattern d'erreur récurrent — toujours WebFetch direct avant)
- ❌ AUCUN chiffre inventé (toujours mesurer empiriquement : `gh api`, WebFetch, grep)
- ❌ PAS DE COMMIT avant Raphael OK explicite
- ✅ Lectures, recherches web, skill watch, MCP read_note — autorisés
- ✅ Scripts Python custom pour automation batch — encouragés
- ✅ Sub-agents parallèles **par CLUSTER thématique** (pas par note)
- ✅ Checkpoint write A-inventaire AVANT lancer phase B
- ✅ Self-verify FAUX fort impact AVANT phase D
- ✅ advisor() AVANT vague 3 (Type 3 réécriture) ET AVANT rapport final ET AVANT propagation étape F
- ✅ **Provider/auteur officiel sur SON produit ou SA recherche = single source suffit** (Anthropic sur Claude, Karpathy sur ses patterns, Dettmers sur QLoRA, etc.)
- ✅ Externes sur un sujet hors de leur scope = 4+ sources convergentes
- ✅ Adapter la hiérarchie au thème — chaque prompt 02 à 07 liste ses sources primaires par domaine
- ✅ Posture Jarvis : remettre en cause TOUT y compris ce qui vient d'être écrit si incohérence détectée

## CHECKLIST PRE-EXÉCUTION (à valider AVANT lancer l'audit)

Avant de lancer un audit thématique, vérifier :

- [ ] Lu `feedback_audit_thematique_methode` (méthode sub-agents clusters validée)
- [ ] Lu `feedback_anthropic_single_source` (directive hiérarchie sources)
- [ ] Lu `Knowledge/erreurs/erreur-22-claims-fausses-vault-claude-code-2026-05-23` (patterns d'erreurs détectés audit Claude Code)
- [ ] Lu prompt thématique cible (02 à 08)
- [ ] MCP forge-brain actif (`/mcp` doit lister forge-brain auto-start)
- [ ] Dossier `output/audit-vault-thematique/<theme>/` créé
- [ ] advisor() AVANT lancer phase B substantielle

## FORMAT RAPPORT FINAL

```markdown
# Audit thème <X> — vault forge — <date>

## Résumé
- N notes auditées
- M claims totales
- Répartition : X canoniques / Y partielles / Z single / W mythes

## Détail par note
[table par note avec claims + statut + sources + citations]

## Plan corrections vault
[diff proposé par note]

## Étape F — Propagation
- N composants utilisateurs identifiés
- X composants à mettre à jour
- Test comportemental : PASS/FAIL

## Verdict advisor()
[résumé verbatim]

## Recommandation finale
[go/no-go par note, attente Raphael]
```

---

**Méthode A→B→C→D→E + propagation F obligatoires. advisor() avant toute modif vault. Minimum 4 sources convergentes. Anthropic/officiel > tous en cas de désaccord (hiérarchie par thème). Honnêteté intellectuelle absolue.**
