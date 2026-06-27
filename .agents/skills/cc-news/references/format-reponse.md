# Format de réponse — cc-news

Template de sortie pour les scans cc-news. Omettre les sections sans nouvelles.

```markdown
## [Date] — Mise à jour cc-news

### Officiel (changelog)
- [version] : [features]

### Équipe Claude Code
- **[leader]** : [tips/annonces]
- _(répéter pour chaque membre ayant posté quelque chose de notable)_

### Dépréciations
- [feature] → [remplacement]

### Prompt Engineering & Techniques
- **Nouvelles techniques** : [techniques genuinely new]
- **Techniques dépréciées** : [techniques now counterproductive on frontier models]
- **Papers académiques** : [notable papers]
- **[leader prompt engineering]** : [insights]

### Concurrents — Modèles
- **[provider]** : [nouveau modèle, capacités, pricing, API changes]
- _(répéter pour chaque provider avec news)_

### Concurrents — Produits Coding
- **[produit]** : [features, changelog]
- **Patterns à adopter** : [ce que les concurrents font bien qu'on devrait intégrer]

### Leaders & Visionnaires
- **[leader]** : [insights, annonces]

### RAG & Embeddings
- **[leader/outil]** : [updates, nouvelles techniques]
- **Nouveaux benchmarks** : [MTEB, etc.]

### Agents IA & Automation
- **[leader/framework]** : [updates, patterns]

### Fine-tuning, Local AI & Quantization
- **[leader/outil]** : [updates, benchmarks]
- **Nouveaux modèles open-source** : [modèles notables]

Sources : [URLs consultées]
```

## Règles de remplissage

1. **Indiquer la date de la recherche** en en-tête
2. **Distinguer** "officiel" vs "équipe" vs "industrie" vs "communauté"
3. **Si rien de nouveau dans une section** → omettre cette section entièrement
4. **Si rien de nouveau du tout** → dire que le studio est à jour depuis la date de référence
5. **Pour les concurrents** : distinguer modèle vs produit. Un nouveau GPT-X → section "Modèles". Une feature Codex CLI → section "Produits Coding"
6. **Capitalisation** : mentionner à la fin les notes vault créées/mises à jour

## Structure capitalisation (résumé)

Après chaque scan, noter en fin de réponse :
```
### Vault mis à jour
- Créé : [chemin note] — [sujet]
- Mis à jour : [chemin note] — [changement]
- MOCs mis à jour : [MOC concerné]
```
