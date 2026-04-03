# Patterns des skills officielles Anthropic

Source : github.com/anthropics/skills (17 skills)

## Structure type d'une skill Anthropic

Chaque skill officielle a :
- `SKILL.md` — instructions courtes et ciblées
- `references/` — guides détaillés, patterns, exemples
- `scripts/` — code Python/Bash pour les validations et transformations
- `assets/` — templates, fonts, thèmes

## Exemples de structure

### pdf/ (traitement PDF)
```
pdf/
├── SKILL.md          ← instructions : quand utiliser pypdf vs pdfplumber vs reportlab
├── REFERENCE.md      ← guide détaillé des outils CLI et Python
└── FORMS.md          ← guide formulaires PDF
```

### skill-creator/ (création de skills)
```
skill-creator/
├── SKILL.md          ← guide interactif de création
├── scripts/
│   ├── generate_review.py  ← génère UI de review dans le navigateur
│   └── run_loop.py         ← boucle d'optimisation des descriptions (train/test)
```

### mcp-builder/ (création MCP)
```
mcp-builder/
├── SKILL.md          ← 4 phases : Research → Implement → Review → Eval
```

### docx/ (documents Word)
```
docx/
├── SKILL.md
├── scripts/
│   ├── create_docx.js      ← création via docx-js
│   ├── edit_docx.py         ← édition via unpack XML
│   └── validate_docx.py     ← validation
├── references/
│   └── style-guide.md
```

## Patterns récurrents

### 1. Scripts de validation (le plus important)
Chaque skill qui produit un output a un script de validation :
- `validate.py` qui vérifie la qualité du résultat
- Déterministe — pas de "vérification par instructions"
- Exécuté automatiquement après génération

### 2. Subagent pour fresh-eyes review
La skill `doc-coauthoring` et `pptx` lancent un subagent avec ZÉRO contexte préalable pour reviewer le résultat. Un lecteur frais détecte les problèmes que l'auteur ne voit pas.

### 3. Boucle d'optimisation (skill-creator)
```python
# run_loop.py — optimise la description d'une skill
# 1. Génère des cas de test (positifs + négatifs)
# 2. Split train/test
# 3. Teste la skill sur les cas train
# 4. Ajuste la description
# 5. Teste sur les cas test
# 6. Répète jusqu'à 5 itérations
```

### 4. Progressive disclosure systématique
SKILL.md ne contient que les instructions essentielles. Tout le reste dans :
- `references/` pour la doc de fond
- `scripts/` pour le code exécutable
- `assets/` pour les templates

### 5. Negative triggers dans la description
```yaml
description: "...Do NOT use for simple data exploration (use data-viz skill instead)."
```

## Leçons pour claude-forge

1. **Ajouter des scripts de validation** aux skills qui produisent des outputs
2. **Subagent fresh-eyes** pour reviewer les résultats importants
3. **Boucle d'optimisation** pour les descriptions — tester sur des cas positifs ET négatifs
4. **Max 5000 mots** dans SKILL.md — tout le reste en references/
5. **Negative triggers** quand une skill risque de trigger trop large
