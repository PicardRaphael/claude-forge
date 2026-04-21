# Pourquoi connecter GitHub a Claude — Avantages pour les plugins

**Date : 10 avril 2026 | Contexte : distribution des plugins neoteem-brain**

## Situation actuelle

L'orga Team "Claude IA" bloque l'acces GitHub. Les plugins (skills IA pour Claude Code et Cowork) doivent etre distribues manuellement : copie de dossiers, ZIP, ou configuration forcee par l'admin.

## Ce que GitHub debloque

### Pour les developpeurs (Claude Code)

| Sans GitHub | Avec GitHub |
|-------------|-------------|
| Copier le dossier plugin dans chaque repo | 1 ligne dans `settings.json`, propagee via `git pull` |
| Aucun controle de version des plugins | Git tags = versioning. On sait qui a quelle version |
| Bug corrige = recopier partout a la main | Merge PR = mise a jour auto en 30 min pour toute l'equipe |
| Pas de catalogue de plugins | Marketplace privee Neoteem : les devs voient les plugins disponibles et installent en 1 clic |
| `/schedule` (taches planifiees cloud) desactive | Taches planifiees fonctionnelles (sync brain quotidien, audit hebdo, etc.) |
| Pas de review sur les changements de plugins | PRs + reviews = audit trail complet |

### Pour les utilisateurs Cowork (support, metier, non-technique)

| Sans GitHub | Avec GitHub |
|-------------|-------------|
| L'admin doit installer manuellement le plugin sur chaque poste ou via managed-settings | Le plugin se synchronise automatiquement depuis le repo |
| Nouvelle version = re-upload ZIP dans Cowork | Merge sur GitHub = resync auto, zero intervention utilisateur |
| Chaque utilisateur peut avoir une version differente | Tout le monde a la meme version, toujours a jour |
| Pas de catalogue self-service dans Cowork | Marketplace interne : l'utilisateur choisit ses plugins dans un catalogue |
| Aucun moyen de proposer de nouveaux plugins sans intervention admin | Ajouter un plugin au repo = visible pour tous automatiquement |

### Pour l'admin / le management

| Aspect | Benefice |
|--------|----------|
| **Controle centralise** | Un seul repo `neoteem/plugins` — l'admin decide ce qui est auto-install, self-service ou cache |
| **Audit trail** | Historique Git complet : qui a change quoi, quand, pourquoi |
| **Securite** | Review obligatoire avant publication (branch protection) |
| **Scalabilite** | Aujourd'hui 1 plugin (2 skills), demain 10+ — meme workflow |
| **Zero maintenance** | Pas de ZIP a redistribuer, pas de managed-settings a mettre a jour manuellement |

## 3 modes de distribution par plugin

Avec GitHub + marketplace, l'admin choisit pour chaque plugin :

| Mode | Comportement | Exemple |
|------|-------------|---------|
| **Auto-install** | Installe automatiquement pour tous | `neoteem-brain` (tout le monde en a besoin) |
| **Self-service** | Visible dans le catalogue, chacun choisit | Plugins optionnels ou specifiques a un role |
| **Hidden** | Invisible, reserve a certains | Plugins experimentaux ou en cours de dev |

## Ce qui fonctionne pour Claude Code ET Cowork

Les plugins sont **cross-compatibles** : meme format, meme structure. Un plugin publie via GitHub est utilisable :
- Dans **Claude Code** (terminal, IDE) par les developpeurs
- Dans **Claude Cowork** (desktop) par le support, les chefs de projet, le metier
- Sans aucune adaptation — c'est le meme fichier

## Actions requises

### Prerequis : compte GitHub pour l'organisation

Si l'organisation n'a pas encore de compte GitHub :

1. **Creer une organisation GitHub** sur github.com (gratuit pour les repos publics, GitHub Team pour les repos prives)
2. **Creer un repo prive** `neoteem/plugins` (ou equivalent) pour heberger les plugins internes
3. **Inviter les membres** de l'equipe dans l'organisation GitHub

> Note : Neoteem utilise Bitbucket pour le code source. GitHub n'est necessaire QUE pour la distribution des plugins Claude. Les deux coexistent sans conflit — aucun code metier ne migre vers GitHub.

### Connecter Claude a GitHub

Une fois l'organisation GitHub en place :

1. **Installer l'app Claude GitHub** sur l'organisation (Settings > Applications > Claude)
2. **Autoriser l'acces** au repo plugins uniquement (pas besoin de donner acces aux repos de code)

### Estimation de l'effort

| Etape | Temps estime | Qui |
|-------|-------------|-----|
| Creer l'orga GitHub + repo plugins | 15 min | Admin |
| Installer l'app Claude GitHub | 5 min | Admin |
| Publier le premier plugin | 30 min | Dev (Raphael) |
| **Total** | **~50 min, une seule fois** | |

### Points importants

- Pas de migration de donnees ni de code
- Aucun impact sur Bitbucket ni sur les repos existants
- GitHub n'est utilise QUE pour les plugins Claude, pas pour le code source
- Reversible a tout moment
- Acces restreint au seul repo plugins (principe du moindre privilege)

## Risques de ne pas le faire

1. **Divergence de versions** — chaque poste a potentiellement une version differente des plugins
2. **Temps perdu** — distribution manuelle a chaque mise a jour, multiplied par le nombre de postes
3. **Pas de scalabilite** — acceptable pour 1 plugin, ingerablea 5+
4. **Pas de taches planifiees** — les automatisations cloud (`/schedule`) restent desactivees
5. **Friction adoption** — les utilisateurs Cowork n'ont pas de catalogue self-service, ca freine l'adoption des outils IA internes
