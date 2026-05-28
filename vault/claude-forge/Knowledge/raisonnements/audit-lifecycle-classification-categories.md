---
titre: "Audit lifecycle — classifier par catégorie avant verdict, jamais à l'œil"
resume: "Raisonnement validé 28 mai 2026 — audit composants forge à l'œil sans canoniques vault → recadrage utilisateur → lecture canoniques EN ENTIER → classification 4 catégories (référence/outil-pur/exécution/audit-jugement) → mass-AMEND évité, AMEND ciblés 2/49 légitimes"
aliases:
  - "audit lifecycle 4 categories"
  - "classification composants vault requis"
  - "grille audit reproductible forge"
  - "lifecycle audit classification"
  - "vault invocation audit pattern"
  - "audit-with-canonicals reasoning"
type: raisonnement
domaine: claude-code
derniere-maj: 2026-05-28
auteur: claude
tags:
  - "#type/raisonnement"
  - "#domaine/claude-code"
  - "#sujet/audit"
  - "#sujet/doctrine"
---
## Probleme

Comment auditer le lifecycle complet d'un repo `.claude/` (49 skills + 13 agents + 10 rules + hooks) sans dériver vers (a) mass-AMEND aveugle ni (b) audit à l'œil sans consulter les canoniques vault.

## Contexte

Audit forge 28 mai 2026. Mission : KEEP/AMEND/KILL/MERGE par composant + cohérence cross-composants. État repo : SAIN avec dette légère soupçonnée. Outil disponible : MCP forge-brain (5 canoniques pertinentes + grille audits passés). Pression : `NE LANCE PAS LES COMMITS` (STOP humain avant destructif) + auto-mode (continuer sans question si raisonnable).

## Chaine de raisonnement

1. **Démarrage à l'œil** — cartographie empirique (grep références skills, frontmatter agents, hooks fs↔settings). Plan D présenté avec 3 KILL proposés. Aucune canonique vault lue via `read_note`. Anti-pattern violé : `feedback_lire_canoniques_avant_audit` (tier-1 MEMORY).

2. **Recadrage utilisateur** — "ton rapport ne montre PAS empiriquement quelles canoniques vault tu as consultées pour FONDER tes critères". Demande explicite d'audit de cohérence rétroactive sur les 3 KILL : quelle canonique supporte chacun ? Si rien → REQUEUE comme dette, pas KILL.

3. **Aveu honnête** — réponse "0 read_note doctrinale ce tour-ci". Audit conduit sur CLAUDE.md + MEMORY.md + savoir interne. Validation rétroactive : KILL1 (vault-maintainer) supporté par `pattern-mcp-brief-then-direct` AJOUT 27 mai ; KILL2 (rule color) supportable si matrice 8 couleurs présente dans `comment-creer-agent` (non lu) ; KILL3 (forge-status) sans canonique probable.

4. **Pivot complet** — lecture EN ENTIER (sans `max_lines`) des 5 canoniques : `comment-creer-agent`, `comment-creer-skill`, `pattern-mcp-brief-then-direct`, `3-axes-strategiques-forge`, `doctrine-vivante`. Plus 2 `search_brain` pour vérifier existence `comment-creer-hook` (présente) et `comment-creer-rule` (absente = trou doctrinal).

5. **Découverte** — le pattern "workflow vault invocation" (Règles 1/2/3 exprimées par utilisateur) **est déjà canonisé** dans `pattern-mcp-brief-then-direct`. Pas un trou doctrinal. Ce qui manque : la grille d'audit empirique applicable.

6. **Premier instinct — mass-AMEND** — 22 skills à `read_note=0 search=0 wikilinks=0`. Tentation : tagger AMEND partout pour les forcer à consulter le vault.

7. **Recadrage advisor** — "0/0/0 n'est pas une violation par défaut. Classifier par catégorie avant de juger. Mass-AMEND sur refs/tools = overreach". Liste des skills légitimement 0/0/0 fournie.

8. **Construction grille 4 catégories** — (1) Skills référence (cc-*-ref, python-ref) : elles SONT la doctrine → vault non requis ; (2) Skills outil pur (json-canvas, defuddle, watch, etc.) : pas de doctrine → vault non requis ; (3) Agents exécution pure (python-dev, self-updater, outcomes-grader) : reçoivent contexte structuré → vault non requis ; (4) Audit/jugement : vault REQUIS.

9. **Critères audit empirique** — pour catégorie 4, checker ≥1 marqueur : `read_note` body, `search_brain` body, ≥2 wikilinks `[[note]]`, section "Étape 0 canoniques", brief inline marker pour sub-agents.

10. **Validation résultat** — sur 49 skills : 22 catégories 1-3 (légitimement 0/0/0), 25 catégorie 4 dont **23 conformes** + 2 AMEND ciblés (cc-advisor, evolve). Sur 13 agents : 10 conformes + 3 exécution pure légitime. Mass-AMEND évité — seulement 2 actions au lieu de 22.

11. **Capitalisation** — AJOUT 28 mai à `pattern-mcp-brief-then-direct` (grille 4 catégories + critères audit reproductibles). Pas de nouvelle note (anti-doublon). Feedback `kill-pragmatique-vide-doctrinal` créé pour KILL3 (forge-status) sans support canonique → tracé honnêtement.

## Insight cle

**La grille de classification 4 catégories rend l'audit empirique reproductible ET défendable**. Sans elle :
- Soit on audit à l'œil (anti-pattern recadré par utilisateur)
- Soit on mass-AMEND aveuglément (anti-pattern recadré par advisor)

La grille filtre 22 faux positifs (skills légitimement sans vault) et révèle 2 vrais AMEND. Le ratio 2/49 (4%) est cohérent avec l'état SAIN du repo — un mass-AMEND aurait simulé un audit "rigoureux" alors qu'il aurait été du bruit.

**Le pattern méta** : avant d'auditer N composants contre une règle, classifier par catégorie de composant pour identifier où la règle s'applique vraiment. Sans classification, la règle universalisée produit overreach.

## Resultat

- 3 KILL (1 P0 + 2 P1) + 2 AMEND ciblés + 1 AJOUT canonique vault + 1 feedback memory + dette `comment-creer-rule` tracée
- Tests baseline 181 maintenus
- Grille 4 catégories appended à `pattern-mcp-brief-then-direct` (canonique vivante, pas doublon)
- 2/49 skills AMEND (4%) au lieu de 22/49 (45%) — mass-AMEND évité
- Validation post-hoc : 2/3 KILL supportés doctrinalement, 1/3 pragmatique assumé (forge-status)

## Reutilisation

Utiliser ce raisonnement quand :
- **Tâche** : audit lifecycle / refonte massive / verdict KEEP-AMEND-KILL-MERGE sur N composants `.claude/`
- **Signal** : tentation de mass-AMEND sur tous les composants à 0/0/0 OU audit "à l'œil" sans lire canoniques vault
- **Application** : (1) lire canoniques EN ENTIER AVANT verdict, (2) classifier les N composants par catégorie (référence / outil pur / exécution / audit-jugement), (3) appliquer la règle SEULEMENT sur catégorie pertinente, (4) si KILL sans support canonique → tracer "pragmatique non-doctrinal", pas inventer

Anti-pattern à éviter : "tout composant doit X" sans classifier d'abord. C'est universaliser une règle qui ne s'applique qu'à une sous-catégorie.

## Liens

- [[pattern-mcp-brief-then-direct]] — canonique du pattern, contient maintenant la grille 4 catégories (AJOUT 28 mai)
- [[methode-analyser-repo]] — séquence A→B→C→D→E (étape B = lire canoniques EN ENTIER)
- [[doctrine-vivante]] — canonique 3 verdicts (INFO/PIVOT/REINFORCE)
- [[feedback_lire_canoniques_avant_audit]] — feedback tier-1 violé puis recadré
- [[feedback_kill_pragmatique_vide_doctrinal]] — feedback créé pour KILL3 forge-status
