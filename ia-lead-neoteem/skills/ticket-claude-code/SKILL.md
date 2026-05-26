---
name: ticket-claude-code
description: Aide Raphael a rediger des tickets Jira nets et clairs, exploitables soit par un developpeur humain, soit directement par Claude Code en autonomie. A declencher des qu'il mentionne "ticket Jira", "user story", "specs dev", "ticket pour Claude Code", "rediger un ticket", "epic IA", "spec technique", "ecrire un ticket", "convertir cette demande en ticket", "structurer une demande dev", "decoupage en sous-taches", "ticket pour mon equipe", ou demande de formaliser une demande metier en ticket exploitable. Produit Epics, User Stories, Tasks au format Jira (markdown / ADF) avec criteres d'acceptation testables, contraintes techniques, et prompts Claude Code pretes a l'emploi.
---

# Redaction tickets Jira pour Claude Code

Tu aides Raphael a rediger des tickets Jira exploitables. **Double cible** : un developpeur humain doit pouvoir bosser dessus, ET Claude Code doit pouvoir l'executer en autonomie si choisi. Cela impose une rigueur particuliere.

## Principe directeur

Un bon ticket pour Claude Code = un bon ticket pour un humain, en mieux. Tout ce qui rend un ticket exploitable par Claude (contexte explicite, criteres testables, contraintes nommees, fichiers cites) le rend aussi plus rapide a executer par un humain.

## Avant de rediger - questions a Raphael

1. **Quel est le besoin exprime** ? (verbatim metier / direction / client si possible)
2. **Niveau de granularite** : Epic, Story, Task, Sub-task ?
3. **Cible execution** : developpeur humain seul, humain + Claude Code, Claude Code en autonomie ?
4. **Projet Jira** : back2.0, Loji, Neo* (NeoChat / NeoDocs), autre ?
5. **Dependances connues** : autres tickets, services, decisions en attente ?
6. **Estimation deja faite** ou je propose ?

Si le besoin est tres flou, propose plusieurs decoupages possibles avant d'ecrire.

## Templates par type de ticket

### EPIC - vision feature complete

```markdown
# [EPIC] <Nom de la feature>

## Objectif
<En 2-3 lignes, le pourquoi business / utilisateur>

## Utilisateur cible
- Persona : <gestionnaire syndic / comptable / locataire / interne ...>
- Contexte d'usage : <quand et ou il declenche>

## Hypothese de valeur
- Si on livre cette feature, alors <metric mesurable> ameliorera de <ordre de grandeur>
- Indicateur de succes : <KPI quantifie>

## Perimetre IN
- <Chose 1 que la feature DOIT faire>
- <Chose 2>
- <Chose 3>

## Perimetre OUT (explicite)
- <Chose qu'on ne fait PAS dans cette epic>
- <Chose qu'on reportera>

## Decoupage propose en stories
- [ ] <STORY-1> : <titre court>
- [ ] <STORY-2> : <titre court>
- [ ] <STORY-3> : <titre court>

## Architecture cible (haut niveau)
- Briques touchees : <back2.0 / Loji front / NeoChat / NeoDocs ...>
- Nouveaux composants : <liste>
- Dependances externes : <Anthropic API / GEMINI / autres>

## Risques identifies
- Techniques : <ex : latence acceptable ?>
- RGPD : <ex : DPIA requise ?>
- Adoption : <ex : changement processus utilisateur>

## Definition of Done (Epic)
- [ ] Toutes les stories livrees et acceptees
- [ ] Doc Confluence a jour
- [ ] Telemetrie en place
- [ ] Communication faite (interne / client)
```

### STORY - unite de livraison

```markdown
# [STORY] <Titre clair, action utilisateur ou systeme>

## Contexte
<3-5 lignes : pourquoi cette story, ou elle s'inscrit dans l'epic>

## Lien Epic
<KEY-XXX>

## User story (si applicable)
En tant que <persona>, je veux <action>, afin de <benefice>.

## Criteres d'acceptation (testables, format Gherkin recommande)

### Scenario 1 : <nom du cas nominal>
- Etant donne que <pre-condition>
- Quand <action>
- Alors <resultat attendu>
- Et <verification additionnelle>

### Scenario 2 : <cas limite>
- ...

### Scenario 3 : <cas d'erreur>
- ...

## Specs techniques

### Fichiers concernes (paths absolus si possible)
- `src/...` <description>
- `apps/...` <description>

### Contrats / API
<Schema OpenAPI extrait, types TypeScript, ou description claire>

### Architecture hexagonale (si back2.0)
- Port : <interface a respecter / a creer>
- Adapter : <implementation concrete>
- Use case : <orchestration>

### Donnees touchees
- Tables Drizzle : <liste>
- Migrations : <oui / non, et numero attendu>

## Contraintes
- Performance : <ex : reponse <500ms p95>
- Securite : <ex : auth requise, role X>
- RGPD : <ex : pas de donnees identifiantes en log>
- Compatibilite : <ex : retro-compat API publique>

## Tests attendus
- [ ] Tests unitaires sur <module>
- [ ] Test integration sur le port
- [ ] Test e2e si UI

## Documentation a mettre a jour
- [ ] OpenAPI / Swagger
- [ ] neoteem-brain note (si decision technique notable)
- [ ] Doc utilisateur si feature visible

## Definition of Done
- [ ] Code reviewe et merge
- [ ] Tests verts
- [ ] Doc a jour
- [ ] Deployement staging ok
- [ ] Validation PO / Raphael

## Estimation
<3 / 5 / 8 / 13>

## Notes pour Claude Code (si execution Claude)
- Lire d'abord : <fichiers de contexte>
- Respecter : <conventions specifiques au projet>
- Ne PAS toucher : <fichiers / modules a eviter>
- Verifier en fin de tache : `bun test`, `bun lint`, et <commande projet specifique>
```

### TASK - tache technique sans valeur utilisateur directe

```markdown
# [TASK] <Action technique precise>

## Objectif
<Pourquoi cette tache existe (dette, refacto, upgrade, outillage)>

## Contexte
<2-3 lignes>

## Travail a faire
1. <Etape 1>
2. <Etape 2>
3. <Etape 3>

## Criteres de fin
- [ ] <Condition 1>
- [ ] <Condition 2>

## Notes pour Claude Code
- Lire : <fichiers>
- Ne pas casser : <comportements existants>
- Commandes de verification : <list>
```

### SUB-TASK - decoupage operationnel

```markdown
# [SUB-TASK] <Action atomique>

## Parent
<STORY-KEY-XXX>

## A faire
<En 1 phrase>

## Verification
<En 1 phrase>
```

## Prompts Claude Code prets a coller

Apres avoir redige le ticket, propose **toujours** un prompt Claude Code pret a l'emploi si execution Claude envisagee :

```
J'ai un ticket Jira <KEY-XXX> a executer. Avant de coder :

1. Lire le ticket Jira <KEY-XXX> via MCP Atlassian
2. Explorer le code existant dans <chemins>
3. Me confirmer ta comprehension du besoin et ton plan d'attaque
4. Attendre mon GO avant de modifier des fichiers

Contraintes :
- Architecture hexagonale obligatoire
- Pas de modification hors perimetre du ticket
- Tests obligatoires pour tout nouveau code
- Commit atomiques avec messages conventional commits

Quand le code est ecrit :
- Lancer `bun test` et `bun lint`
- Si erreurs, corriger avant de me revenir
- Me presenter le diff avant commit
```

## Pieges a eviter

- **Verbe flou** : "ameliorer", "optimiser", "rendre plus performant" -> exiger une metrique
- **Pas de criteres d'acceptation** : le dev (ou Claude) interpretera, et tu seras decu
- **Trop gros ticket** : si > 1 semaine de dev, decouper en stories
- **Pas de definition of done** : la story trainera en review
- **Pas de cas d'erreur** : Claude Code et un dev humain feront tous les deux du code sans gestion d'erreur
- **Confusion EPIC / STORY** : l'epic ne se code pas, la story oui
- **Ticket pour Claude Code mais sans fichiers cites** : Claude va chercher seul, peut diverger
- **Ticket pour humain mais avec prompt Claude Code dedans** : confusion, separer en encarts

## Bonus - hierarchie typique d'un projet IA Loji

```
EPIC : "Assistant juridique pour gestionnaire syndic" (3-6 mois)
  STORY : "Recherche augmentee dans la base d'AG" (2-3 sprints)
    SUB-TASK : Indexation des PV d'AG
    SUB-TASK : Endpoint /search avec RAG
    SUB-TASK : UI front widget recherche
  STORY : "Generation de reponse type avec citations" (2 sprints)
    SUB-TASK : Service generation avec Claude
    SUB-TASK : Logique citation des sources
    SUB-TASK : UI affichage des sources
  STORY : "Feedback utilisateur pouce + / -" (1 sprint)
    SUB-TASK : Schema BDD feedback
    SUB-TASK : Endpoint POST /feedback
    SUB-TASK : UI thumbs
TASK : "Mise en place telemetrie LangSmith sur tous les appels LLM"
TASK : "Documentation neoteem-brain : architecture RAG Loji"
```

## Rappel RGPD / risques (court systematique)

Quand le ticket concerne une feature IA touchant des donnees client :
- Mentionner explicitement les donnees manipulees dans la section "Contraintes" -> "RGPD"
- Exiger logs sans donnees identifiantes
- Demander base legale et localisation traitement dans la story (pas en oubliant la phrase)
- Pour Claude Code : preciser "ne pas inclure de donnees client dans les exemples / fixtures, utiliser des donnees fictives"
