# Best Practices — Preferences Claude Desktop

Sources : Amanda Askell (Anthropic), Alex Albert (Anthropic), Anthropic docs, power users.

## Principes cles

### 1. TDD pour prompts (Amanda Askell)

Ne pas ecrire les instructions puis les tester. Faire l'inverse :
1. Lister les situations ou Claude repond mal par defaut
2. Ecrire les instructions qui corrigent ces echecs
3. Iterer — Askell envoie "des centaines de prompts en 15 minutes" pour tester

### 2. Briefing jour 1

Penser les preferences comme un briefing pour un nouvel employe brillant mais amnesique. Il n'a aucun contexte sur les normes, styles, ou manieres de travailler. Plus on est precis, mieux c'est.

### 3. BLUF — Bottom Line Up Front

Instruire Claude a donner la reponse directe d'abord, le raisonnement ensuite. Elimine le pattern "laissez-moi reflechir..." qui fait perdre du temps.

### 4. Expert Partner, pas assistant

Cadrer Claude comme un "bras droit" ou "partenaire expert" :
- Doit toujours proposer au moins une alternative non envisagee
- Rendre les risques/limites/compromis explicites
- Finir avec un plan d'action concret

### 5. Anti-slop

Eliminer les patterns IA generiques dans les preferences :
- "Pas de preambules (Bien sur !, Excellente question !)"
- "Pas de disclaimers (en tant qu'IA...)"
- "Pas de recap de la question avant de repondre"

### 6. Explain WHY

Eviter les ALL-CAPS MUST/NEVER/ALWAYS sans explication. Enoncer la regle, puis expliquer pourquoi. Claude generalise mieux aux cas non prevus quand il comprend le pourquoi.

### 7. Negative instructions (high impact)

Dire ce qu'on ne veut PAS est souvent plus efficace que dire ce qu'on veut. Les anti-patterns sont plus faciles a detecter pour Claude que les patterns positifs.

### 8. Timestamp

Ajouter "Derniere mise a jour : [date]" en fin d'instructions. Donne a Claude un contexte temporel.

### 9. Auto Memory

Activer la memoire auto ET le mentionner dans les preferences pour que Claude sache qu'il doit retenir activement les corrections et preferences.

### 10. < 500 mots

Les preferences chargent en tokens a CHAQUE conversation. 500 mots max pour le profil. Utiliser les projets pour le contexte specifique.

## 3 couches (stacking)

| Couche | Portee | Contenu |
|--------|--------|---------|
| Profil | Toutes conversations | Identite, ton, regles universelles |
| Projet | 1 projet specifique | Stack technique, regles domaine |
| Style | Formatage seulement | Ton, longueur, structure |

Plus Cowork (champ separe) pour les sessions Cowork.

Les couches se cumulent : ne jamais dupliquer entre couches.

## Pattern vault-first (Neoteem)

Le pattern force Claude a consulter le vault AVANT de repondre de memoire :

```
Si ma question touche a [domaine] : utiliser la skill [nom-skill] pour 
chercher dans le vault avant de repondre de memoire. Le vault est la 
source de verite. Si le vault ne contient pas l'info, le dire clairement.
```

Pour les non-devs : referencer les SKILLS (pas les outils MCP). Les skills encapsulent la detection CLI/MCP automatiquement.

## Anti-patterns

- Trop long (> 500 mots) — gaspille du contexte
- Trop vague ("sois utile") — pas d'impact
- Contradictoire ("sois bref" + "sois exhaustif") — Claude perd du compute
- Context-dependent en global — instructions trop specifiques pour toutes les conversations
- Duplication entre couches — gaspille des tokens
- Jamais mis a jour — revoir toutes les 4-6 semaines
