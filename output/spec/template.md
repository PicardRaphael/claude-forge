# Template Spécification User Story

```markdown
### Résumé
[1-2 phrases : le problème à résoudre et la solution proposée.]

### Contexte
[Contexte métier issu de neo-brain-support. Pourquoi c'est important. 2-4 phrases.]

### Critères d'acceptation

1. **[Fonctionnalité / Point 1]**
   - Critère vérifiable
   - Critère vérifiable

2. **[Fonctionnalité / Point 2]**
   - Critère vérifiable
   - Critère vérifiable

### Règles de gestion

- **RG-1** — [Règle claire, une phrase — issue de neo-brain-support]
- **RG-2** — [Règle claire, une phrase]

### Détail métier
[Ce que neo-brain-support a renvoyé : règles business, cas particuliers, vocabulaire domaine, contexte historique.
Cette section peut être plus longue si le domaine l'exige. Ne pas la brider.]

### Hors périmètre
- [Ce qui N'EST PAS inclus dans cette US]

### Maquettes
[Lien Figma ou "À définir"]
```

---

## Principes de rédaction — ticket principal

- **QUOI et POURQUOI uniquement** : jamais le COMMENT. Les détails d'implémentation vont dans les sous-tâches.
- **Zéro jargon technique** : pas de noms de tables, fonctions PG, composants Vue. Si neo-brain-dev en remonte, les déplacer dans les sous-tâches.
- **Scannable** : chaque section lisible en 10 secondes. Un bullet = une idée, pas un paragraphe.
- **Bullets simples** : pas de checkboxes `- [ ]`, pas de préfixes `**CA-1.1**`. Juste des tirets avec des phrases courtes.
- **CA groupés par fonctionnalité** : si l'US couvre plusieurs points, numéroter et grouper les CA. Plus facile à tester pour la QA.
- **Règles séparées des CA** : CA = ce qu'on vérifie (testable). RG = comment ça fonctionne (détail). Ne pas mélanger.
- **Détail métier** : ne pas brider. Si le domaine est complexe, laisser neo-brain-support s'exprimer ici.
- **Headers `###`** : partout, jamais `#` ni `##` — meilleur rendu dans Jira.
- **Pas de tables complexes** : préférer les listes. Tables OK pour 2-3 colonnes simples (ex : matrice avant/après).

---

## Template sous-tâche technique ([BACK] / [FULL])

```markdown
### Contexte
[Ce que cette sous-tâche doit faire, en une phrase.]

### Travail à réaliser
- [Action concrète 1]
- [Action concrète 2]

### Contexte technique (neo-brain-dev)
- Endpoint existant : [URL et méthode si applicable]
- Fonction PG : [nom si applicable]
- Outils neo_ia : [agent ou tool si applicable]
- Contraintes : [schéma DB, règles de validation, etc.]

### Critères de complétion
- [Ce qui doit être livré / testé]
```

---

## Template sous-tâche UX

```markdown
### Contexte
[Ce que cette sous-tâche doit produire.]

### Périmètre UX
- [Écran / composant concerné]
- [Interactions à concevoir]

### Contraintes
- [Guideline, accessibilité, responsive, etc.]

### Livrable attendu
- [Maquette Figma, prototype, spécifications visuelles]
```
