# RAG classique vs neoteem-brain

Document de reference interne Neoteem — Avril 2026 (version corrigee)

## En une phrase

Le RAG injecte des morceaux de texte dans le prompt de l'IA. neoteem-brain donne a Claude des outils pour naviguer la connaissance lui-meme.

---

## Comment Claude recoit le contexte

C'est LA difference fondamentale. Les deux approches donnent du contexte a Claude, mais pas de la meme maniere.

### Avec RAG : contexte passif (on lui donne des morceaux)

```
Utilisateur pose une question a Claude
  |
Le systeme RAG cherche dans la vector DB
  |
5 chunks de ~200-500 tokens sont recuperes automatiquement
  |
Ces chunks sont INJECTES dans le prompt de Claude
(il ne choisit pas lesquels, il les recoit passivement)
  |
Claude lit les chunks et essaie de repondre
```

Claude ne controle rien. Il recoit des morceaux de texte decoupes et doit se debrouiller avec. S'il lui manque du contexte, il ne peut pas aller le chercher. S'il recoit un chunk inutile, il a quand meme consomme les tokens.

C'est comme donner a quelqu'un 5 pages arrachees d'un livre et lui demander de repondre a une question.

### Avec neoteem-brain : contexte actif (il va chercher lui-meme)

```
Utilisateur pose une question a Claude
  |
Claude DECIDE de chercher dans le vault
  |
search:context query="..." --> snippets cibles (~200-500 tokens)
Claude LIT les snippets et CHOISIT quelles notes lire
  |
read file="..." --> seulement les 1-3 notes pertinentes
  |
Claude VOIT les [[wikilinks]] dans la note
Il DECIDE de suivre un lien ou non selon le besoin
  |
backlinks file="..." --> il decouvre les notes liees
  |
Claude construit sa comprehension pas a pas
comme un humain qui navigue dans une documentation
```

Claude est un agent actif. Il cherche, il lit, il navigue, il decide quand il en a assez. S'il lui manque du contexte, il suit un wikilink. S'il a assez d'info, il s'arrete. Il ne consomme que les tokens necessaires.

C'est comme donner a quelqu'un l'acces a une bibliotheque bien rangee avec un index et le laisser trouver ce dont il a besoin.

### Impact concret sur la qualite des reponses

| Situation | RAG (contexte passif) | neoteem-brain (contexte actif) |
|---|---|---|
| Question simple ("c'est quoi un ADF ?") | Recoit 5 chunks dont certains hors sujet. Repond avec du bruit. ~1500-2500 tokens | search:context trouve la bonne note en 1 appel. Read cible. ~500-1200 tokens |
| Question complexe ("comment fonctionne la compensation syndic-gerance ?") | Recoit des chunks partiels de notes differentes. Ne peut pas reconstituer la chaine sans appels supplementaires. | Suit les wikilinks : regle metier → fonction PG → table → ecran Lojii. Chaine complete. |
| Question cross-domaine ("impact d'une resiliation de bail sur la compta") | Les chunks viennent probablement d'un seul domaine. L'autre domaine est absent du top-K. | backlinks file="bail" → trouve les notes compta liees. Traverse les domaines. |
| Info obsolete ("la table t_xyz...") | Le chunk obsolete remonte. Pas de signal que c'est perime. | La note a un callout [!warning] Obsolete + lien vers le remplacement. |
| Suivi de conversation ("et cote frontend ?") | Nouveau retrieval, re-embedding, re-injection de chunks. | Claude a deja lu la note. Il suit le wikilink vers la note frontend. Pas de nouveau search. |

---

## Architecture comparee

### RAG classique

```
Documents bruts (PDF, pages web, code, Confluence...)
  |
Chunking (decoupage en morceaux de ~200-500 tokens)
  |
Embedding API (OpenAI, Voyage, Gemini...) --> vecteurs numeriques
  |
Vector DB (pgvector, Pinecone, Weaviate, ChromaDB...)
  |
Query --> embedding --> recherche cosine --> top-K chunks
  |
Chunks injectes dans le prompt LLM --> reponse
```

### neoteem-brain

```
Notes Obsidian curatees (682 fichiers structures)
  |
Index natif Obsidian (full-text + aliases comme synonymes)
  |
CLI search:context --> snippets cibles (~200-500 tokens)
  |
Read cible sur 1-3 notes pertinentes seulement
  |
Wikilinks --> navigation vers les notes liees si besoin
  |
Reponse avec contexte complet (chaine front --> API --> PG)
```

---

## Cout en tokens par requete

| Etape | RAG classique | neoteem-brain |
|---|---|---|
| Recherche | Embedding de la query (~50 tokens) + appel API embedding payant | search:context via CLI = outil local, resultats ~200-500 tokens |
| Resultats injectes | 5 chunks x ~300 tokens = ~1500 tokens dans le prompt | Snippets cibles = ~200-500 tokens |
| Lecture approfondie | Pas possible, on n'a que les chunks (sauf mitigation read) | read sur 1-3 notes = ~500-3000 tokens (si necessaire) |
| Contexte relationnel | Aucun, les chunks sont isoles (sauf table de liens) | backlinks + wikilinks = relations dans le texte |
| **Total par requete** | **~1500 - 5000 tokens + cout embedding** | **~700 - 4000 tokens, 0 cout externe** |

Note : les deux approches ont des fourchettes larges. Une question simple consomme le bas de la fourchette, une question complexe avec navigation le haut. L'avantage de neoteem-brain est que Claude ne lit que ce dont il a besoin — le RAG injecte toujours le meme volume de chunks, qu'ils soient utiles ou non.

### Sur 100 queries par jour

| Metrique | RAG classique | neoteem-brain |
|---|---|---|
| Tokens LLM | ~150K - 500K | ~70K - 400K |
| Cout embedding externe | ~$0.01-0.05/jour | $0 |
| Cout vector DB (pgvector sur instance existante) | ~$0-5/mois | $0 |
| Cout vector DB (Pinecone/Weaviate heberge) | ~$20-100/mois | $0 |
| Economie tokens | baseline | ~30-50% de reduction |

Note : l'economie de tokens depend fortement de la qualite du chunking RAG. Un RAG bien implemente avec des chunks semantiques et un re-ranking reduit l'ecart. L'avantage principal de neoteem-brain n'est pas le volume de tokens mais leur **pertinence** — Claude choisit ce qu'il lit.

---

## Qualite des reponses

### Contexte

**RAG** : Chunks de ~300 tokens decoupes par section. Si la reponse chevauche 2 chunks non adjacents dans le top-K, le contexte est incomplet. Un RAG bien configure avec chunking semantique (par section ##) mitigue ce probleme.

**neoteem-brain** : Notes completes et structurees. Frontmatter avec metadonnees. Wikilinks vers les notes liees. Claude recoit toujours le document complet avec sa structure.

### Relations entre concepts

**RAG** : Les chunks sont isoles par defaut. Une table `chunk_relations` peut reconstituer les liens, mais c'est une reconstruction manuelle de ce qu'Obsidian fait nativement. Claude doit faire des appels supplementaires (`expand()`) pour naviguer.

**neoteem-brain** : Wikilinks bidirectionnels. La commande `backlinks file="t-bail"` trouve toutes les regles metier, fonctions PG et FAQ qui parlent de cette table. Les relations sont explicites, dans le texte, et navigables par Claude.

### Chaine complete front-to-back

**RAG** : Difficile. Le RAG retourne les chunks les plus proches vectoriellement, pas la chaine d'appels. Il faudrait que tous les maillons de la chaine soient dans le top-K, ce qui est peu probable.

**neoteem-brain** : La chaine complete est documentee et liee. On peut suivre : bouton Lojii → route Vue.js → endpoint Go → fonction PG. Chaque maillon est une note avec des wikilinks vers les maillons adjacents.

### Fraicheur de l'information

**RAG** : Necessite un re-embedding a chaque modification de document (worker toutes les 15 min dans notre scenario). Si le worker tombe, le RAG retourne des reponses obsoletes silencieusement.

**neoteem-brain** : Notes mises a jour directement. Le champ `derniere-maj` dans le frontmatter trace la derniere modification. Un callout `[!warning] Obsolete` est ajoute si un concept est supprime, avec un lien vers le remplacement. Modifications visibles instantanement (local) ou en ~5 min (partage reseau).

### Contradictions

**RAG** : Peut retourner 2 chunks contradictoires. Claude est capable de detecter les contradictions dans son contexte, mais sans les wikilinks il ne peut pas remonter a la source pour trancher.

**neoteem-brain** : L'agent sync-checker audite les contradictions. Les wikilinks permettent de croiser les sources et identifier les incoherences. Claude peut suivre les liens pour verifier.

### Hallucinations

**RAG** : Le LLM peut "completer" un chunk partiel avec des informations inventees, surtout si le chunk est tronque au milieu d'une explication.

**neoteem-brain** : Les notes sont curatees et verifiees par les equipes. Chaque note a un champ `sources` dans le frontmatter qui trace l'origine (Confluence, code, Jira). Le risque d'hallucination existe toujours mais le contexte complet le reduit.

---

## Exemple concret

**Question** : "C'est quoi le calcul des charges en copropriete ?"

### Avec RAG (scenario realiste, chunking par section ##)

1. Embedding de la question → vecteur
2. Recherche cosine dans ~3000-5000 chunks → top 5 resultats :
   - Chunk : section "Principe" de la note charges → pertinent, contient la regle
   - Chunk : section "Formule" de la note charges → pertinent, contient la formule
   - Chunk : section de la note "appel-de-fonds" → contexte partiel
   - Chunk : section de la note "f_calc_charges" → technique, pas demande
   - Chunk : section d'une note sur les budgets → tangentiellement lie
3. Claude recoit ces 5 chunks sans wikilinks, sans frontmatter, sans structure hierarchique
4. Il ne peut pas suivre un lien vers les cles de repartition ou l'historique

Resultat : reponse correcte sur le principe et la formule, mais sans la chaine complete ni le contexte historique. ~2500 tokens consommes.

### Avec neoteem-brain

1. `search:context query="calcul charges copropriete" limit=5` → 3 notes pertinentes identifiees, ~300 tokens
2. `read file="calcul-charges"` → note metier structuree complete : principe, formule, cas particuliers, historique. ~800 tokens
3. Wikilinks dans la note : `[[cles-de-repartition]]`, `[[f-calc-charges]]`, `[[decision-2024-03-refonte-charges]]` → Claude sait que ces notes existent. Pour une question metier, pas besoin de tout lire.
4. Si besoin d'approfondir : `read file="cles-de-repartition"` → ~400 tokens supplementaires

Resultat : reponse complete avec la chaine metier, les cas particuliers, et le contexte historique. ~1100-1500 tokens consommes.

---

## Infrastructure

| Element | RAG classique (pgvector) | neoteem-brain |
|---|---|---|
| Base de donnees | PostgreSQL + pgvector (schema dedie, index HNSW) | Aucune. Fichiers markdown + git |
| Pipeline d'embedding | Script d'ingestion + chunking + embedding + upsert. Worker cron toutes les 15 min. | Aucun. Les notes sont ecrites directement dans le vault |
| API externe | Embedding API (Voyage, OpenAI) — payant, dependance cloud | Aucune. Tout est local |
| Maintenance | Worker a surveiller, re-embedding si modele change, monitoring qualite chunks | git pull + Obsidian ouvert |
| Debugging | Inspecter les chunks retournes, les scores cosine, le prompt assemble. Moins intuitif. | Transparent. Ouvrir Obsidian, lire la note, voir les wikilinks. |
| Backup | Git (source) + dump SQL (index). L'index est reconstructible. | git push (deja fait, versionne) |
| Cout mensuel (pgvector sur instance existante) | ~5-10 EUR (embeddings + Cloud Run) | 0 EUR |
| Cout mensuel (vector DB heberge type Pinecone) | ~25-120 EUR | 0 EUR |
| Securite | Donnees envoyees a une API externe pour l'embedding. Les embeddings eux-memes ne sont pas reversibles, mais le contenu brut transite. | 100% local, chiffrable, aucune donnee externalisee |

---

## Couverture semantique : aliases vs embeddings

Le principal avantage du RAG : la recherche semantique. Si quelqu'un cherche "impayes" mais que la note s'appelle "relances-locataires", les embeddings trouvent le lien semantique automatiquement.

Notre solution : les aliases dans le frontmatter de chaque note.

```yaml
# relances-locataires.md
aliases:
  - "impayes"
  - "loyers impayes"
  - "recouvrement locataire"
  - "RAL"
  - "relance impaye"
  - "locataire qui paye pas"
```

L'index Obsidian cherche dans les aliases. Le resultat est deterministe (100% fiable) contre les embeddings qui sont probabilistes (le score cosine peut varier, surtout en francais ou les modeles d'embedding sont historiquement moins performants qu'en anglais — meme si les modeles recents comme voyage-3 ont fortement reduit cet ecart).

**Limites des aliases :**
- Les aliases doivent etre ecrits manuellement. Si un synonyme n'est pas prevu, la recherche echoue silencieusement.
- A grande echelle (5000+ notes), maintenir les aliases devient couteux.
- Les reformulations inattendues ("le truc pour faire payer les locataires") ne sont pas couvertes.

**Limites des embeddings :**
- Resultats probabilistes — un score cosine de 0.85 ne garantit pas la pertinence.
- Les termes techniques tres specifiques (noms de fonctions PG, noms de tables) sont mal captures par les embeddings.
- Le francais technique specialise (jargon syndic/gerance) peut etre mal represente dans les modeles d'embedding generiques.

Sources de vocabulaire :
- `glossaire.md` : 70+ termes metier officiels Neoteem
- `glossaire-support.md` : reformulations simples pour les equipes support
- Chaque note a au minimum 3 aliases, sans maximum, couvrant : synonyme metier, abreviation, vocabulaire support, terme technique

---

## Quand le RAG serait meilleur

| Situation | Pourquoi RAG gagnerait | Notre cas ? |
|---|---|---|
| 10 000+ documents | L'index keyword ne suffit plus, les aliases deviennent ingerables a maintenir | Non aujourd'hui. 682 notes, seuil estime a 2000-3000. Mais possible dans 2-4 ans si l'adoption accelere. |
| Documents non structures (PDF bruts, emails, logs) | Le chunking est le seul moyen de les rendre cherchables par une IA | Non. Notes curatees en markdown structure. |
| Recherche multi-langue | Les embeddings multilingues trouvent cross-langue | Non. Tout est en francais avec quelques termes techniques anglais. |
| Utilisateurs sans vocabulaire metier | Impossible de deviner tous les aliases necessaires pour des reformulations inattendues | Partiellement. Le support utilise parfois des formulations imprevues. Les glossaires couvrent la majorite mais pas 100%. |
| Cross-referencing vault + code source | Chercher dans les notes ET dans le code en une seule requete vectorielle | Partiellement. neo-brain-dev-ia fait le cross-ref mais en 2-3 appels sequentiels, pas en 1 requete. |

---

## Les 4 agents du vault

Le vault est maintenu par 4 agents specialises :

| Agent | Role | Quand |
|---|---|---|
| repo-analyzer | Lit les repos de code (Go, TS, Vue, Python, PG), cree des notes techniques dans le vault | Quand un nouveau repo ou module doit etre documente |
| vault-enricher | Lit Confluence (espaces NeoIA et DTI), cree des notes dans le vault | Quand de la documentation Confluence doit etre importee |
| vault-linker | Ajoute les wikilinks bidirectionnels, met a jour les MOCs (Maps of Content) | Automatiquement apres chaque creation de notes |
| sync-checker | Audite l'integrite : frontmatter complet, liens valides, pas d'orphelins | Automatiquement apres les batch de creation |

Un pipeline conditionnel orchestre ces agents : les gros batch declenchent tous les agents, les petites modifications ne declenchent que le minimum necessaire.

---

## Optimisations token-smart (avril 2026)

| Optimisation | Economie estimee | Description |
|---|---|---|
| search:context d'abord | ~30-50% sur les queries | Retourne des snippets, pas le fichier entier. Lecture complete seulement si necessaire |
| Pipeline conditionnel | ~30-40% sur les ecritures | Un append ne declenche plus tous les agents. Seuls les batch declenchent le pipeline complet |
| Check avant auto-creation | Reduction des doublons | Verifie si une FAQ existe avant d'en creer une nouvelle |
| Correction sur place | Prevention | Info obsolete = mise a jour de la note existante + propagation aux backlinks. Pas de nouvelle note |
| Aliases obligatoires | Prevention | Au minimum 3 aliases par note couvrant synonymes, abreviations, vocabulaire support et technique |

---

## Faiblesses de neoteem-brain (honnetete intellectuelle)

| Faiblesse | Impact | Mitigation |
|---|---|---|
| Obsidian doit tourner sur le poste | Si ferme, plus de recherche | Auto-start + Task Scheduler relance toutes les 5 min |
| Recherche floue / reformulations limitee | Le support qui tape "le truc pour les charges" ne trouve rien | Aliases + glossaires. Couvre ~90% mais pas 100% |
| Aliases maintenus manuellement | Cout humain, risque d'oubli | Rule aliases-obligatoires.md + sync-checker verifie |
| Pas d'acces claude.ai web/mobile natif | Limite l'accessibilite | Partage reseau + MCP local. Ou pgvector si besoin web/mobile. |
| CLI ne scale pas au-dela de 2000-3000 notes | Degradation performance a terme | Seuil de reevaluation defini. Migration pgvector possible. |
| Necessite Obsidian + Git (ou partage reseau) | Installation sur chaque poste | install.bat automatise, GPO pour le deploiement |

---

## Resume

| Dimension | RAG classique (pgvector) | neoteem-brain |
|---|---|---|
| Comment l'IA recoit le contexte | Passif : chunks injectes dans le prompt | Actif : l'IA cherche, lit, navigue elle-meme |
| Tokens par query | ~1500 - 5000 | ~700 - 4000 |
| Infrastructure | PostgreSQL pgvector + embedding API + worker | Git + Obsidian |
| Cout mensuel (pgvector existant) | ~5-10 EUR | 0 EUR |
| Cout mensuel (vector DB heberge) | ~25-120 EUR | 0 EUR |
| Qualite contexte | Chunks isoles (mitigation possible via read) | Notes liees par wikilinks |
| Debugging | Moins intuitif (inspecter chunks + scores) | Transparent (ouvrir Obsidian) |
| Fraicheur | ~15 min (worker cron) | Instantanee (local) ou ~5 min (reseau) |
| Securite | Donnees transitent vers API embedding | 100% local |
| Recherche semantique | Native (embeddings) — gere les reformulations inattendues | Aliases deterministes — fiables mais manuels |
| Scalabilite | Illimitee | Bonne jusqu'a ~2000-3000 notes |

### En conclusion

neoteem-brain est **la meilleure solution pour notre cas d'usage actuel** (682 notes, equipe interne, vocabulaire metier maitrise). L'approche "contexte actif" produit des reponses plus completes et plus fiables que le RAG classique, a un cout inferieur.

Le RAG deviendra pertinent si le vault depasse 2000-3000 notes, si des utilisateurs externes sans vocabulaire metier doivent y acceder, ou si un acces claude.ai web/mobile sans Obsidian devient necessaire. A ce moment-la, les deux approches pourront coexister : CLI pour les devs, pgvector pour les autres.
