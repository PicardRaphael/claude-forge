# Grille de maturite — skill-evolve

Scores 1-5 pour evaluer une SKILL.md.

Le score est une synthese des 4 axes. Ne pas faire une moyenne mathematique — un score 1 sur Efficacite suffit a tirer le score global vers le bas.

---

## Score 1 — Needs rework

**Label :** Needs rework

**Caracteristiques :**
- Description vague ou absente (pas de triggers)
- Pas de section Gotchas
- Workflow incomplet ou absent
- SKILL.md > 500 lignes sans references/
- Modele/effort obsoletes ou incorrects

**Action :** Recrire avec skill-creator. Pas de patch incremental — repartir du template.

**Exemple typique :** Une skill creee "vite fait" sans checklist, description en une phrase generique, aucune mention des cas d'erreur.

---

## Score 2 — Functional but weak

**Label :** Functional but weak

**Caracteristiques :**
- Description presente mais sans triggers naturels
- Section Gotchas presente mais superficielle (enonce l'evident)
- Workflow fonctionnel mais incomplet (pas de validation inputs, pas de format output)
- SKILL.md entre 400-500 lignes, bientot a deporter

**Action :** Ameliorations ciblees. 2-3 propositions impact eleve suffisent.

**Exemple typique :** Skill qui marche quand on la demande directement, mais qui ne se declenche pas automatiquement et echoue sur les edge cases.

---

## Score 3 — Solid

**Label :** Solid

**Caracteristiques :**
- Description avec triggers, en anglais, une ligne
- Section Gotchas avec vrais Gotchas specifiques
- Workflow complet avec validation inputs et format output
- SKILL.md < 400 lignes (ou > 400 avec references/ bien organisees)
- Modele/effort corrects

**Action :** Ameliorations mineures. Cross-pollination peut apporter de la valeur. Evolution technique si le vault a de nouveaux patterns.

**Exemple typique :** Skill qui fonctionne bien, couvre les cas normaux, mais n'exploite pas encore les derniers patterns forge.

---

## Score 4 — Mature

**Label :** Mature

**Caracteristiques :**
- Tous les criteres Score 3 +
- Triggers negatifs presents pour disambiguation
- Fallbacks documentes (ex: vault indisponible, outil absent)
- Section Apprentissage non vide (apprentissages reels documentes)
- References/ bien structurees si SKILL.md > 200 lignes
- Cross-pollination deja appliquee (patterns des meilleures skills integres)

**Action :** Micro-ameliorations uniquement. Surveiller le vault pour nouvelles techniques.

**Exemple typique :** Skill stable avec historique git > 5 commits, utilisee regulierement, qui evolue avec les besoins.

---

## Score 5 — Optimal

**Label :** Optimal

**Caracteristiques :**
- Tous les criteres Score 4 +
- Scripts deterministes pour les validations critiques (pas de langage naturel)
- Progressive disclosure appliquee (SKILL.md court, details dans references/)
- Pas d'instructions enoncant l'evident
- Apprentissages regulierement capitalises
- Teste sur haiku ET sonnet (marche sur les deux)

**Action :** Maintenance uniquement. Verifier une fois par mois si de nouvelles techniques vault s'appliquent.

**Exemple typique :** vault-audit avec ses scripts Python, forge-brain avec son wrapper CLI et ses fallbacks documentes.

---

## Table de decision rapide

| Critere | Score max si absent |
|---------|-------------------|
| Description avec triggers | 2 |
| Section Gotchas | 2 |
| Workflow complet | 3 |
| SKILL.md < 500L | 3 |
| Fallbacks documentes | 4 |
| Section Apprentissage non vide | 4 |
| Scripts deterministes pour validations | 5 |
| Progressive disclosure | 5 |
