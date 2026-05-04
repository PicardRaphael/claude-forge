# Bilan comparatif — Acces au vault neoteem-brain via Claude

Auteur : Raphael Picard | Date : 27 avril 2026

Comparaison de toutes les architectures possibles pour donner acces au vault neoteem-brain a tous les collaborateurs Neoteem (devs, support, direction, consultants migration) via Claude et/ou Obsidian.

---

## Contexte

### Ce qui existe aujourd'hui

Le vault **neoteem-brain** (682 notes Obsidian, Bitbucket `neot-v2/neoteem-brain`) est accessible via :
- **3 plugins Claude Code/Desktop** par role : support, dev, dev-ia
- **CLI Obsidian** : moteur de recherche full-text avec ranking, aliases (synonymes), backlinks, tags, proprietes. Integre a Obsidian nativement (Settings > General > CLI > activer).
- **MCP obsidian-brain** : pont entre Claude et la CLI, tourne en local
- **install.bat** : installe tout en 2 min (Obsidian via winget, vault, MCP, config Claude Desktop). 1 seule action manuelle : activer la CLI dans Obsidian.

### Le besoin

Rendre le vault accessible a TOUS les collaborateurs Neoteem :
- **Devs** : deja servis (Claude Code + CLI)
- **Support** : pas de Git, pas forcement Obsidian, doivent pouvoir LIRE et potentiellement ECRIRE
- **Direction** : lecture seule, acces rapide, zero install
- **Consultants migration** : lecture + ecriture dans leur domaine

### Contrainte technique cle

Sur claude.ai et Claude Desktop, le seul moyen d'acceder a des donnees externes est un **serveur MCP**. Une skill seule ne peut pas faire de requete reseau ou SQL. Toute solution "sans install" passe donc obligatoirement par un MCP.

---

## Les 4 architectures possibles

### Option 1 — CLI Obsidian sur chaque poste (actuel)

```
Chaque poste :
  Obsidian (auto-start) → CLI activee → MCP obsidian-brain local
  Claude Code/Desktop → MCP local → CLI → fichiers .md locaux
  Vault : clone Git local, git pull pour les mises a jour
```

### Option 2 — Vault sur partage reseau + Obsidian (sans Git pour les lecteurs)

```
SERVEUR :
  \\SERVEUR\neoteem-brain\  (partage SMB)
  Task Scheduler : git pull origin master toutes les 5 min

CONTRIBUTEURS (devs, 3-5 personnes) :
  Clone Git local → editent → git push → le serveur pull automatiquement

LECTEURS (support, direction) :
  Obsidian ouvert sur \\SERVEUR\neoteem-brain\ (lecture seule)
  MCP obsidian-brain local → CLI → fichiers reseau
  PAS DE GIT sur leur poste
```

### Option 3 — Partage reseau + Obsidian + ecriture support (Obsidian Git plugin)

```
SERVEUR :
  \\SERVEUR\neoteem-brain\  (partage SMB en lecture/ecriture)
  OU : chaque poste a son clone Git local synchronise automatiquement

CONTRIBUTEURS (devs) :
  Git classique (clone local, push/pull)

SUPPORT / CONSULTANTS (ecrivent aussi) :
  Obsidian avec plugin "Obsidian Git" (auto pull/commit/push)
  OU : Obsidian sur partage reseau avec sync bidirectionnelle
  Editent les notes directement dans Obsidian, le plugin gere Git
```

### Option 4 — BDD pgvector + MCP Cloud Run (proposition Benjamin)

```
SERVEUR (Cloud Run) :
  Worker d'ingestion (cron 15 min) : git pull vault → parse → chunk → embed → UPSERT pgvector
  MCP server : expose search/read/expand via API

TOUS les utilisateurs :
  Claude (Desktop, claude.ai, mobile) → MCP Cloud Run → PostgreSQL pgvector
  Rien a installer cote poste (sauf Claude Desktop ou acces claude.ai)
```

---

## Comparatif detaille

### Installation et deploiement

| Critere | Option 1 (CLI locale) | Option 2 (reseau lecture) | Option 3 (reseau R/W) | Option 4 (pgvector) |
|---|---|---|---|---|
| **Setup serveur** | Aucun | 1 partage + 1 cron git pull (1h devops) | 1 partage + config Git (2h devops) | MCP + worker + pgvector (11-17 jours dev) |
| **Install par poste — dev** | `install.bat` (2 min) + activer CLI | `install.bat` (2 min) + activer CLI | Idem | Ajouter URL MCP (30 sec) |
| **Install par poste — support** | `install.bat` (2 min) + activer CLI + **apprendre Git** | `install.bat` (2 min) + activer CLI. **Pas de Git.** | `install.bat` + plugin Obsidian Git. **Pas de Git manuel.** | Ajouter URL MCP (30 sec). **Rien d'autre.** |
| **Install par poste — direction** | Idem support | Idem support | Lecture seule via Obsidian | Ajouter URL MCP (30 sec) |
| **Git requis sur le poste** | Oui (tous) | Contributeurs seulement | Transparent (plugin gere) | Non |
| **Obsidian requis** | Oui (tous) | Oui (tous) | Oui (tous) | Non |
| **Obsidian doit tourner** | Oui | Oui | Oui | Non |
| **Deploiement 20 postes** | GPO + install.bat (~2h devops) | GPO + install.bat + partage (~2h devops) | Idem + config plugin Git (~3h devops) | Push config MCP (~30 min devops) |
| **Automatisation Obsidian** | Auto-start + tray (GPO/Task Scheduler) | Idem | Idem | N/A |
| **Nouveau collaborateur** | install.bat + 1 clic CLI | install.bat + 1 clic CLI | install.bat + 1 clic CLI | URL MCP dans settings |

### Couts

#### Setup initial (one-shot)

Temps estimes avec Claude Code pour le developpement (Option 4).

| Poste | Option 1 | Option 2 | Option 3 | Option 4 |
|---|---|---|---|---|
| Partage reseau | 0 | 1h devops | 2h devops | 0 |
| Cron git pull serveur | 0 | 30 min devops | 30 min devops | 0 |
| GPO / auto-start Obsidian | 1h devops | 1h devops | 1h devops | 0 |
| Schema SQL pgvector | 0 | 0 | 0 | 2h |
| Script ingestion (parse + chunk + embed) | 0 | 0 | 0 | 1-2 jours |
| MCP server Cloud Run (search/read/expand) | 0 | 0 | 0 | 1-2 jours |
| Worker cron Cloud Run | 0 | 0 | 0 | 0.5 jour |
| chunk_relations (extraction wikilinks) | 0 | 0 | 0 | 1 jour |
| Tests + debug chunking | 0 | 0 | 0 | 1-2 jours |
| Deploy Cloud Run | 0 | 0 | 0 | 0.5 jour |
| Re-ranking | 0 | 0 | 0 | 0 (Claude le fait nativement) |
| Agentic retrieval (boucles) | 0 | 0 | 0 | 0 (Claude le fait nativement) |
| **TOTAL** | **~2h devops** | **~3h devops** | **~4h devops** | **~5-8 jours dev** |

Note : le re-ranking et l'agentic retrieval sont gratuits car Claude est l'agent. Quand le MCP retourne des resultats, Claude decide quoi lire en detail — c'est du LLM-based re-ranking natif. Pas besoin de coder un re-ranker ou une boucle agentic.

#### Couts mensuels recurrents

| Poste | Option 1 | Option 2 | Option 3 | Option 4 |
|---|---|---|---|---|
| Serveur fichiers (existant) | 0 | 0 (partage existant) | 0 (partage existant) | 0 |
| Cloud Run — MCP server | 0 | 0 | 0 | ~3 EUR |
| Cloud Run — worker | 0 | 0 | 0 | ~2 EUR |
| Cloud SQL pgvector | 0 | 0 | 0 | ~0-30 EUR* |
| Embeddings API | 0 | 0 | 0 | ~2-5 EUR |
| **TOTAL mensuel** | **0 EUR** | **0 EUR** | **0 EUR** | **~7-40 EUR** |

*Cloud SQL : 0 si instance existante reutilisee, 15-30 EUR si instance dediee.

#### Maintenance humaine mensuelle

| Poste | Option 1 | Option 2 | Option 3 | Option 4 |
|---|---|---|---|---|
| Support utilisateurs ("ca marche pas") | ~2h | ~2h | ~3h | ~1h |
| Maintenance serveur/infra | 0 | ~0.5h | ~0.5h | ~3h |
| Debug qualite recherche/chunking | 0 | 0 | 0 | ~2h |
| **TOTAL** | **~2h** | **~2.5h** | **~3.5h** | **~6h** |

---

### Cout en tokens LLM — argument financier majeur

Les tokens LLM (consommes par Claude pour lire le contexte) representent un cout invisible mais reel. Plus Claude recoit de contexte, plus la requete coute cher en tokens.

#### Par requete

| Etape | Options 1/2/3 (CLI) | Option 4 (pgvector) |
|---|---|---|
| Recherche (search:context / search) | ~200-500 tokens (snippets) | ~200-500 tokens (chunks top-K) |
| Lecture approfondie | read 1-3 notes = ~500-3000 tokens (Claude choisit) | chunks deja injectes, OU read supplementaire ~500-2000 tokens |
| Contexte relationnel | backlinks = ~100-300 tokens | expand() = ~200-500 tokens |
| **Total par requete** | **~700 - 4000 tokens** | **~900 - 3000 tokens** |

Les deux approches sont **comparables en tokens**. L'avantage CLI : Claude ne lit QUE les notes qu'il juge pertinentes (pas de chunks inutiles injectes). L'avantage pgvector : les chunks sont plus petits, donc si la recherche est precise, moins de tokens gaspilles.

#### Sur 100 queries par jour (estimation)

| Metrique | Options 1/2/3 (CLI) | Option 4 (pgvector) |
|---|---|---|
| Tokens LLM consommes | ~70K - 400K | ~90K - 300K |
| Cout embedding externe | 0 EUR | ~0.01-0.05 EUR/jour |
| Cout infra (Cloud Run, Cloud SQL) | 0 EUR | ~0.15-0.30 EUR/jour |
| **Cout total tokens + infra / jour** | **0 EUR** | **~0.20-0.40 EUR/jour** |

Note : le cout des tokens LLM depend du plan Claude (Max, Team, API). Sur claude.ai Max/Team, les tokens sont inclus dans l'abonnement — le volume n'a pas d'impact financier direct. Sur l'API, chaque token est facture. L'ecart de tokens entre les deux options est faible (~20-30%) et depend de la qualite du chunking.

**L'economie de tokens n'est pas l'argument decisif.** Les deux approches consomment un volume comparable. Le vrai avantage de la CLI est la **qualite** du contexte (fichier complet vs chunks), pas le **volume**.

---

### Performance et qualite

#### Impact du reseau sur Obsidian (Options 2/3 vs Option 1)

Obsidian sur un partage reseau SMB (`\\SERVEUR\...`) fonctionne mais avec des differences mesurables :

| Critere | Option 1 (SSD local) | Options 2/3 (reseau SMB) | Impact reel |
|---|---|---|---|
| **Demarrage Obsidian** (indexation vault) | ~3-5 sec (682 notes) | ~10-20 sec (latence SMB par fichier) | Ressenti au 1er lancement, puis cache |
| **Recherche CLI** | ~200ms | ~300-500ms (lecture fichiers via SMB) | Faible — 1 recherche par question |
| **Lecture d'une note** | ~5ms | ~20-50ms | Imperceptible |
| **Ouverture dans Obsidian** | Instantane | ~0.5-1 sec | Leger mais acceptable |
| **Indexation backlinks/tags** | Cache local rapide | Cache local mais index initial lent | 1 seule fois au demarrage |
| **Verrouillage fichier (SMB lock)** | Aucun | Possible si 2 Obsidian ouvrent le meme vault | Option 2 (lecture seule) = aucun risque. Option 3 = rare mais possible. |

**Verdict : le reseau ajoute ~100-300ms par requete et ~15 sec au demarrage. C'est perceptible mais acceptable.** La recherche reste sous la seconde, le demarrage est une fois par jour (auto-start). Ce n'est PAS un bloqueur.

**Mitigation :** Obsidian met en cache l'index localement (dossier `.obsidian/`). Apres le premier demarrage, les recherches suivantes utilisent le cache meme sur reseau. Seule la mise a jour de l'index (quand le cron git pull ajoute/modifie des fichiers) provoque une re-indexation partielle.

#### Qualite de recherche

| Type de requete | Option 1 (CLI locale) | Options 2/3 (CLI reseau) | Option 4 (pgvector) |
|---|---|---|---|
| Terme exact ("f_calc_charges") | Excellent | Excellent (meme CLI) | Excellent |
| Synonyme connu (alias "appel de fonds") | Excellent | Excellent (meme CLI) | Excellent |
| Synonyme inconnu / reformulation | Faible | Faible | **Bon** |
| Faute de frappe | Faible | Faible | **Bon** |
| Requete vague / langage naturel | Moyen | Moyen | **Bon** |
| Filtrage domaine/type/tag | Excellent | Excellent | Excellent |

Les Options 1, 2 et 3 utilisent **la meme CLI Obsidian** donc la meme qualite de recherche. La seule difference est la latence reseau (~100-300ms de plus). pgvector gagne uniquement sur les requetes floues, les reformulations, et les fautes de frappe. A 682 notes avec des aliases bien faits, cet avantage est marginal.

#### Qualite de la reponse de Claude — LE POINT CRITIQUE

| Critere | Options 1/2/3 (CLI) | Option 4 (pgvector) |
|---|---|---|
| Ce que Claude recoit | **Fichier .md entier** | Chunks de ~200 mots |
| Wikilinks visibles | **Oui** — `[[cles-de-repartition]]` | Non — perdus au chunking |
| Navigation entre notes | **Oui** — Claude suit les liens | Non — doit appeler `expand()` |
| Structure du document | **100% preservee** | ~60-70% preservee |
| Aliases dans le frontmatter | **Oui** — visibles | Partiellement (chunk 0) |
| Croiser 2+ notes | **Naturel** — lit les fichiers | Limite aux top-K chunks |
| Contexte pour reponse complete | **Complet** | Fragmente |

**Le paradoxe pgvector : trouve mieux, repond moins bien.** La recherche vectorielle rank mieux, mais Claude recoit des fragments au lieu de documents complets. Les reponses sont plus superficielles.

#### Exemple concret — ce que Claude recoit

**Question utilisateur :** "Comment sont reparties les charges en syndic ?"

**Via CLI (Options 1/2/3) — Claude recoit le fichier entier :**
```markdown
---
titre: "Calcul des charges de copropriete"
aliases: ["calcul charges", "repartition charges", "appel de fonds", "f_calc_charges"]
domaine: syndic
type: regle
---

## Principe
Les charges sont reparties selon les [[cles-de-repartition]]
definies dans le [[reglement-de-copropriete]].
Chaque [[lot]] a des [[tantiemes]] par cle.

## Formule
charge_lot = (montant_total * tantiemes_lot) / total_tantiemes_cle

## Cas particuliers
### Charges ascenseur
Seuls les lots au-dessus du RDC paient.
Voir [[f_calc_charges_ascenseur]] pour l'implementation.

### Charges personnelles
Certaines charges sont affectees directement a un lot.
Ne passent pas par la repartition. Voir [[charges-personnelles]].

## Historique
Refactore en 2024 — voir [[decision-2024-03-refonte-charges]].
```
→ Claude voit TOUT : les 4 aliases, les 7 wikilinks, la structure, l'historique.
→ Il peut suivre `[[cles-de-repartition]]` pour approfondir.
→ Reponse complete et contextualisee.

**Via pgvector (Option 4) — Claude recoit des chunks :**
```
Chunk #4821 (score: 0.87)
Document: "Calcul des charges de copropriete"
Section: "Principe"
---
Les charges sont reparties selon les cles de repartition
definies dans le reglement de copropriete.
Chaque lot a des tantiemes par cle.

Chunk #4823 (score: 0.72)
Document: "Calcul des charges de copropriete"
Section: "Cas particuliers"
---
Charges ascenseur : seuls les lots au-dessus du RDC paient.
Charges personnelles : certaines charges sont affectees
directement a un lot.
```
→ Les wikilinks sont remplaces par du texte brut (plus de navigation).
→ La formule (chunk "Formule") n'est peut-etre pas dans le top-K.
→ L'historique (chunk "Historique") probablement pas retourne.
→ Les aliases ne sont pas visibles.
→ Claude ne peut pas suivre un lien pour approfondir.

**Mitigation pgvector :** apres le `search`, faire un `read()` du document complet pour les top 3-5 resultats. Remonte la qualite a ~85-90% de la CLI. Mais :
- Ca ajoute 3-5 appels MCP supplementaires (search → read x N)
- La latence augmente (~1-2 sec au lieu de ~400ms)
- Claude doit quand meme choisir QUELS documents lire en entier parmi les chunks retournes — s'il choisit mal, l'info est perdue
- Les wikilinks dans le document lu ne pointent vers rien (pas de `read` recursif)

#### Latence detaillee

| Scenario | Option 1 (locale) | Options 2/3 (reseau) | Option 4 (pgvector) | Option 4 + mitigation read |
|---|---|---|---|---|
| Recherche seule | ~200ms | ~300-500ms | ~250ms | ~250ms |
| Lecture 1 resultat | ~5ms | ~20-50ms | ~10ms | ~10ms |
| **Workflow complet (search + lecture top 3)** | **~215ms** | **~400-650ms** | **~280ms** | **~1-2 sec** (search + 3x read) |

Toutes les options restent sous les 2 secondes. La difference est imperceptible dans un chat Claude (le LLM met 3-10 sec a generer sa reponse de toute facon).

#### Fraicheur des donnees

| Evenement | Option 1 | Option 2/3 | Option 4 |
|---|---|---|---|
| Modif visible | Instantane (local) | ~5 min (cron serveur) | ~15 min (worker + embed) |
| Brouillon non pushe | Visible (contributeur local) | Visible (contributeur local) | Invisible |

---

### Accessibilite

| Plateforme | Option 1 | Option 2/3 | Option 4 |
|---|---|---|---|
| Claude Code (terminal) | Oui | Oui | Oui |
| Claude Desktop (poste bureau) | Oui | Oui | Oui |
| claude.ai web | Non | Non | **Oui** |
| claude.ai mobile | Non | Non | **Oui** |
| Obsidian direct (sans Claude) | Oui | Oui | Non |
| Zero install | Non | Non | **Oui** |

**Attention :** les Options 1/2/3 fonctionnent avec Claude Desktop (qui supporte le MCP local). claude.ai web et mobile ne supportent que les MCP heberges (Cloud Run). Si tout le monde est sur Desktop, cette difference disparait.

---

### Ecriture par le support — analyse detaillee

C'est le point cle. Le support (et les consultants migration) doivent-ils pouvoir ajouter/modifier des notes ?

#### Oui, le support doit ecrire

Si le support doit contribuer au vault (FAQ, procedures, problemes connus dans `07-Support/`) :

| Solution | Comment | Complexite | Risque |
|---|---|---|---|
| **Option 3 — Obsidian Git plugin** | Le support edite dans Obsidian. Le plugin auto-commit + auto-push toutes les X minutes. Pas de Git manuel. | Faible | Conflits si 2 personnes editent la meme note. Le plugin gere mal les merges complexes. |
| **Option 3b — Partage reseau R/W** | Le support edite directement sur `\\SERVEUR\neoteem-brain\`. Un cron cote serveur fait `git add -A && git commit && git push`. | Tres faible | Dernier qui save ecrase. Pas de merge. Perte de donnees possible. **DECONSEILLE.** |
| **Option 3c — Branches par role** | Le support edite sur une branche `support`. Un dev review et merge dans `master`. | Moyenne | Necessite un workflow de review. Plus lourd mais plus sur. |
| **Option 4 + formulaire** | Un formulaire web (ou Claude lui-meme) cree un fichier .md et push sur Git via API Bitbucket. | Moyenne | Le support ne touche jamais Obsidian ni Git. Mais faut developper le formulaire. |

**Recommandation pour l'ecriture support :**

**Option 3 — Obsidian Git plugin** avec ces garde-fous :
- Le support ecrit UNIQUEMENT dans `07-Support/` (les autres dossiers sont en lecture)
- Auto-pull toutes les 5 min, auto-commit + push toutes les 10 min
- Template obligatoire (support-faq.md, support-procedure.md)
- Si conflit, le plugin cree un fichier `.conflict` que le dev resout
- Pas besoin d'apprendre Git : le plugin fait tout en arriere-plan

**Configuration Obsidian Git plugin :**
```
Auto pull interval: 5 minutes
Auto push interval: 10 minutes
Auto commit message: "[support] {{hostname}} - {{date}}"
Pull on startup: true
Push on startup: true
```

**Protection des dossiers :** via un hook Git `pre-commit` cote serveur qui refuse les commits du support hors de `07-Support/`.

#### Non, le support lit seulement

Alors **Option 2** suffit. Le support ouvre Obsidian sur le partage reseau, lit les notes, pose des questions a Claude via le MCP local. Zero Git, zero ecriture, zero risque.

---

### Scalabilite

| Volume | Options 1/2/3 (CLI) | Option 4 (pgvector) |
|---|---|---|
| 682 notes (actuel) | Parfait | Overkill |
| 2 000 notes | OK | Confortable |
| 5 000+ notes | CLI ralentit | Confortable |
| 10 000+ notes | Inutilisable | Concu pour |

**Seuil de reevaluation : 2000-3000 notes.** Au rythme actuel (2-5 notes/semaine), ~4-6 ans. Si import massif Confluence ou acceleration des contributeurs, peut arriver en 1 an.

---

### Risques par option

| Risque | Opt 1 | Opt 2 | Opt 3 | Opt 4 |
|---|---|---|---|---|
| Obsidian ferme = plus de recherche | Moyen* | Moyen* | Moyen* | Aucun |
| Reseau down | Aucun (local) | **Bloquant** lecteurs | **Bloquant** lecteurs | Aucun (Cloud) |
| Conflit d'edition | Via Git merge | Aucun (read-only) | Plugin Git gere | N/A |
| Perte de donnees | Git protege | Git protege | Plugin peut rater un push | N/A (read-only) |
| Qualite reponse Claude degradee | Aucun | Aucun | Aucun | **Chunks fragmentes** |
| Cout imprevu | Aucun | Aucun | Aucun | Embeddings + Cloud SQL |
| Maintenance lourde | Faible | Faible | Moyenne | **Elevee** |

*Mitige par auto-start + Task Scheduler : si Obsidian se ferme, il est relance en 5 min.

---

## Tableau de synthese finale

| Critere | Opt 1 (CLI locale) | Opt 2 (reseau R/O) | Opt 3 (reseau R/W) | Opt 4 (pgvector) |
|---|---|---|---|---|
| **Cout setup** | ~2h devops | ~3h devops | ~4h devops | **~5-8 jours dev** |
| **Cout mensuel** | 0 EUR | 0 EUR | 0 EUR | **~5-10 EUR** |
| **Maintenance** | ~2h/mois | ~2.5h/mois | ~3.5h/mois | **~6h/mois** |
| **Git requis (support)** | **Oui** | Non | Non (plugin) | Non |
| **Obsidian requis** | Oui | Oui | Oui | **Non** |
| **Acces claude.ai web/mobile** | Non | Non | Non | **Oui** |
| **Support peut ecrire** | Via Git (dur) | Non | **Oui (plugin)** | Non* |
| **Qualite recherche** | Tres bon | Tres bon | Tres bon | Tres bon + fuzzy |
| **Qualite reponse Claude** | **Excellente** | **Excellente** | **Excellente** | Moyenne |
| **Fraicheur** | Instantanee | ~5 min | ~5-10 min | ~15 min |
| **Scalabilite 5000+** | Faible | Faible | Faible | **Excellente** |
| **Reseau down** | OK (local) | **Bloque** | **Bloque** | OK (Cloud) |
| **Complexite globale** | Faible | Faible | Moyenne | Elevee |

*Option 4 : l'ecriture est possible via formulaire web ou API Bitbucket, mais necessite un dev supplementaire.

---

## Recommandation

### Architecture cible : Option 2 (lecture) ou Option 3 (lecture + ecriture support)

**Pour la majorite des collaborateurs :**

1. **Devs** → Option 1 (CLI locale, deja en place, inchange)
2. **Support/direction** → Option 2 (partage reseau lecture seule) ou Option 3 (Obsidian Git plugin si ecriture necessaire)
3. **Consultants migration** → Option 3 (ecriture dans leur domaine)

**Pourquoi pas pgvector maintenant :**
- ~5-8 jours de dev vs 3-4h devops pour les options reseau
- ~5-10 EUR/mois vs 0 EUR
- ~6h/mois de maintenance vs 2.5-3.5h
- Qualite de reponse inferieure (chunks vs fichiers complets) — mitigeable avec read() mais ajoute de la latence
- Le seul avantage reel (claude.ai web/mobile + recherche floue) ne justifie pas le cout a 682 notes
- Les tokens consommes sont comparables (~20-30% d'ecart, pas un facteur decisif)

**Quand passer a pgvector :**
- Vault atteint 2000+ notes
- OU besoin confirme d'acces claude.ai web/mobile (pas via Desktop)
- OU la recherche floue manque reellement (mesure, pas supposition)

### Plan de deploiement recommande

| Phase | Duree | Action |
|---|---|---|
| 1 | 1h devops | Creer le partage `\\SERVEUR\neoteem-brain\` + cron `git pull` toutes les 5 min |
| 2 | 1h devops | GPO : Obsidian auto-start sur tous les postes + Task Scheduler relance |
| 3 | 30 min/poste | Executer `install.bat` sur les postes support/direction (ou GPO pour deployer) |
| 4 | 15 min | Configurer les postes support : vault = chemin reseau au lieu de clone local |
| 5 (si ecriture) | 1h | Installer + configurer Obsidian Git plugin sur les postes support. Hook pre-commit pour limiter a `07-Support/`. |
| 6 | 30 min | Test : le support pose une question a Claude, verifie la reponse. Si ecriture : cree une note, verifie qu'elle apparait pour les autres. |

**Total : 1 journee devops. Zero dev. Zero cout mensuel.**

### Et le prompt pgvector ?

Le prompt d'embedding (`output/prompt-embedding-neoteem-brain.md`) reste dans le tiroir. Le jour ou le vault atteint 2000+ notes ou qu'un besoin claude.ai web/mobile se confirme, il est pret. Pas besoin de le construire maintenant.

---

## Annexes

### Annexe A : automatisation Obsidian sur les postes

**Auto-start Windows (GPO ou local) :**
```
shell:startup → raccourci Obsidian.exe --minimized
```

**Task Scheduler — relance si ferme (PowerShell) :**
```powershell
if (-not (Get-Process Obsidian -ErrorAction SilentlyContinue)) {
    Start-Process "$env:LOCALAPPDATA\Programs\obsidian\Obsidian.exe" -WindowStyle Minimized
}
```
Configurer : toutes les 5 min, declencheur "A l'ouverture de session" + repetition.

**Obsidian en tray :** comportement par defaut. Cliquer la croix = minimise, pas ferme. Aucune config necessaire.

### Annexe B : configuration Obsidian Git plugin (Option 3)

```json
{
  "autoSaveInterval": 10,
  "autoPullInterval": 5,
  "autoPullOnBoot": true,
  "autoPushAfterCommit": true,
  "commitMessage": "[support] {{hostname}} - {{date}}",
  "pullStrategy": "rebase"
}
```

**Hook pre-commit serveur (limite ecriture support a 07-Support/) :**
```bash
#!/bin/bash
# Verifier que les commits "support" ne touchent que 07-Support/
AUTHOR_PREFIX=$(git log -1 --format=%s HEAD 2>/dev/null | grep -c "^\[support\]")
if [ "$AUTHOR_PREFIX" -gt 0 ]; then
  CHANGED=$(git diff --cached --name-only | grep -v "^07-Support/")
  if [ -n "$CHANGED" ]; then
    echo "ERREUR: Le support ne peut modifier que 07-Support/"
    echo "Fichiers bloques: $CHANGED"
    exit 1
  fi
fi
```

### Annexe C : pourquoi PAS Weaviate / Pinecone / Qdrant ?

pgvector est le bon choix SI vous passez a l'Option 4 :
- **Instance Cloud SQL existante** — pas de service supplementaire
- **682 notes = ~3000-5000 chunks** — pgvector gere des millions
- **Recherche hybride native** — pgvector + tsvector + pg_trgm dans une seule requete
- **Pas de vendor lock-in** — PostgreSQL standard
- **Equipe formee** — Neoteem utilise PostgreSQL partout

### Annexe D : choix du modele d'embedding (si Option 4)

| Modele | Dimensions | Langues | Prix (1M tokens) | Notes |
|---|---|---|---|---|
| `voyage-3` (Voyage AI) | 1024 | Multilingual | ~0.06 USD | **Recommande** — meilleur sur texte technique |
| `text-embedding-3-large` (OpenAI) | 3072 | Multilingual | ~0.13 USD | Bon, dimensions ajustables (MRL) |
| `text-embedding-3-small` (OpenAI) | 1536 | Multilingual | ~0.02 USD | Budget |
| `gemini-embedding-exp` (Google) | 3072 | Multilingual | gratuit (preview) | Experimental |

### Annexe E : ce que le chunking perd et comment compenser (si Option 4)

| Element Obsidian | Perdu au chunking ? | Compensation |
|---|---|---|
| Frontmatter (titre, domaine, type) | Non — table `documents` | Colonnes SQL filtables |
| Aliases | Partiellement | **Chunk 0 metadata** les inclut tous |
| Wikilinks `[[...]]` | Oui dans le texte | Table `links` + `expand()` |
| Backlinks | Oui | Requete inverse sur `links` |
| Structure sections ## | Partiellement | Titre section en metadata du chunk |
| Blocs de code | Non si fences respectees | Regle : jamais couper dans un bloc code |
| Tags | Non — table `documents` | Filtre SQL |
