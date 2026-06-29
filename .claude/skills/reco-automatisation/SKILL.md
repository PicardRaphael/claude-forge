---
name: reco-automatisation
description: ALWAYS invoke when the user has process sheets (from audit-departement or pasted) and wants recommendations on what to automate with AI and at what level. Triggers "fais-moi les recos d'automatisation", "qu'est-ce qu'on automatise pour le service X", "analyse cette fiche process", "/reco-automatisation". Applies the quality-equation + bottleneck + chatbot/workflow/agent grading. NOT for running the interview (audit-departement), NOT for picking which Claude Code brick to build (methode-monter-systeme-workflow).
user-invocable: true
allowed-tools: Read, mcp__forge-brain__*
model: opus
effort: high
argument-hint: "[chemin ou colle la/les fiche(s) process]"
---

# reco-automatisation — de la fiche process à la reco priorisée

Prend une ou plusieurs **fiches process** (produites par `audit-departement` ou collées) et en tire des **recommandations d'automatisation priorisées** : pour chaque process, le bon niveau de solution (chatbot assisté / workflow contextualisé / agent autonome), un Opportunity Solution Tree de synthèse, et les quick wins (impact × effort).

C'est la PHASE 2 (analyse). La PHASE 1 (interview) est la skill `audit-departement`. Cette skill JUGE, elle n'interviewe pas.

Méthode canonique (le socle — à NE PAS recopier ici) : `mcp__forge-brain__read_note(file="auditer-departements-pour-automatisation")`, section « Phase 2 ». La lire si un point est incertain.

## Entrée

- Soit un chemin de fichier (Read), soit une/des fiche(s) collée(s) directement, soit des notes brutes sur les process d'un département.
- Si l'entrée est trop maigre pour juger (pas de fréquence, pas d'indice règles vs jugement, pas de douleur claire) : le dire et lister précisément ce qui manque — renvoyer vers `audit-departement` pour compléter plutôt que d'inventer.

## Étapes

### 1. Lire la méthode + l'entrée

- Lire la note canonique (section Phase 2) si la méthode n'est pas déjà fraîche en contexte.
- Charger la/les fiche(s) process.

### 2. Reframe par l'équation de qualité

Pour chaque process, rappeler que **Qualité output = Puissance modèle × Outils connectés × Contexte**. Le levier n'est pas le modèle (tous puissants) mais le **contexte** : le process a-t-il une méthode documentée, des données accessibles, un format de livrable clair ? Un process sans contexte explicitable n'est pas automatisable tel quel — le signaler.

### 3. Diagnostic du goulot d'étranglement

Situer chaque process dans : **Acquisition / Production-Delivery / Rétention**. Identifier celui qui bloque le plus le département aujourd'hui. C'est le candidat prioritaire (croisé avec l'adhésion de l'équipe si l'info est dans la fiche).

### 4. Qualifier le niveau de solution (la gradation)

Pour chaque process candidat, trancher le niveau avec les signaux de la fiche :

| Niveau | Quand le recommander |
|---|---|
| **1 — Chatbot assisté** | L'humain peut faire la plomberie ; gain = assistance ponctuelle. Cas d'entrée simple. |
| **2 — Workflow contextualisé** | Données accessibles + méthode explicitable + livrable standardisé ; l'IA va chercher, produit, l'humain déclenche et relit. **Le sweet spot par défaut.** |
| **3 — Agent autonome** | Seulement si le niveau 2 est déjà prouvé ET qu'un trigger événementiel clair existe. Jamais en premier. |

Règle de tranche : **règles explicites + précision 99 % requise → automatisation déterministe** ; **ambiguïté / langage / jugement, 85-95 % suffit → IA**. Savoir tacite fort → pas automatisable tel quel (documenter d'abord). Process instable → stabiliser avant d'automatiser.

### 5. Synthèse Opportunity Solution Tree

Agréger toutes les fiches sous un Outcome unique (ex : « réduire le temps de traitement d'un dossier de X % ») :
```
Outcome
├── Opportunité 1 (douleur racontée)
│   ├── Solution candidate 1.1 (niveau chatbot/workflow/agent) → test
│   └── Solution candidate 1.2
├── Opportunité 2
```
Sizing : compter combien de fiches mentionnent la même douleur = priorité par fréquence.

### 6. Priorisation impact × effort

- Placer chaque solution candidate sur une matrice **impact × effort**.
- Recommander de commencer par le quadrant **fort impact / faible effort** (quick wins).
- Rappeler la séquence 3-layers : ne pas livrer un agent (layer 3) avant d'avoir le contexte (layer 1) et le mapping (layer 2) — sinon ça casse en quelques semaines.

### 7. Livrable de sortie (markdown)

```markdown
## Recommandations d'automatisation — [département]

### Synthèse
- Goulot principal : [zone + process]
- Outcome visé : [...]

### Par process (priorisé)
1. **[process]** — niveau **[chatbot/workflow/agent]**
   - Pourquoi ce niveau : [règles vs jugement, données, savoir]
   - Brique à construire (→ methode-monter-systeme-workflow) : [skill / workflow / agent]
   - Impact × effort : [quadrant]
   - Prérequis (contexte/données manquants) : [...]

### Opportunity Solution Tree
[arbre]

### Quick wins (à démarrer)
- [...]
```

## Gotchas

- **Cette skill juge, elle n'interviewe pas.** Si l'entrée manque d'info, renvoyer vers `audit-departement` — ne pas combler les trous par hypothèse, ça produirait une reco inventée.
- **Niveau 2 (workflow) est le défaut, pas niveau 3 (agent).** « Ce qui est vendu comme agent IA est en réalité plus un workflow » : recommander l'autonomie seulement après preuve de valeur sur les niveaux inférieurs.
- **Ne pas inverser les 3 layers.** Proposer un agent sans le contexte (world model) ni le mapping des process en amont = la reco qui « casse en 2-6 semaines ». Toujours flaguer les prérequis de contexte/données.
- **Savoir tacite ≠ automatisable tout de suite** : si la fiche dit « ça dépend de l'expérience », la reco est « documenter la méthode d'abord », pas « mettre un agent ».
- **Stabiliser avant d'automatiser** : un process bancal automatisé crée de la dette. Le signaler si la fiche révèle un process instable.
- **Ne pas citer comme canon** : « McKinsey 70-80 % » (attribution fausse), seuils « 2 FTE » / délais « 6-8/12-16 semaines » (directionnels). Seule grille adossée à une source primaire = UiPath Automation Hub. Cf mises en garde de la note canonique.

## Apprentissage

Après une reco réelle, noter ici :
- Un schéma de qualification récurrent par département (ex : la plupart des process Migration tombent en niveau 2) → enrichir.
- Un cas où la gradation chatbot/workflow/agent a mal collé à la réalité → ajuster les critères de tranche.
- Si un type de process revient sur plusieurs départements → capitaliser dans `[[auditer-departements-pour-automatisation]]`.
