# Proposition : Connecter GitHub a l'organisation Claude IA

**Date :** 9 avril 2026
**Auteur :** Raphael Picard
**Pour :** Direction + DevOps Neoteem

---

## Resume executif

Notre abonnement Claude Team inclut **Claude Cowork** (automatisation pour les equipes non-techniques) et **Claude Code** (pour les developpeurs). Pour exploiter pleinement ces outils, nous avons besoin de connecter un compte GitHub a notre organisation Claude.

**Action requise :** L'administrateur de l'organisation "Claude IA" doit connecter GitHub dans les parametres. C'est une operation de 5 minutes, une seule fois.

**Impact :** Mise a jour automatique des outils IA pour toute l'equipe, sans intervention manuelle.

---

## Pourquoi pas Bitbucket ?

Bitbucket est notre outil principal pour le code et il le restera. Mais pour les **plugins Claude**, Bitbucket a des limitations techniques qu'on ne peut pas contourner :

| Fonctionnalite | GitHub | Bitbucket |
|---------------|--------|-----------|
| Auto-sync marketplace Cowork (30 min) | Oui | Non — Anthropic ne supporte que GitHub |
| Plugin auto-install pour les non-devs | Oui | Non — upload ZIP manuel a chaque MAJ |
| Triggers cloud (/schedule) | Oui | Non — pas supporte par l'API Anthropic |
| `settings.json` git URL | Oui | Oui — mais MAJ au `git pull` seulement |

**La raison technique :** Anthropic a un partenariat avec Microsoft/GitHub (annonce "Copilot Cowork" mars 2026). Le marketplace Cowork utilise l'API GitHub (webhooks, GitHub App) pour detecter les changements et resynchroniser automatiquement. Cette integration n'existe pas pour Bitbucket, GitLab ou d'autres providers.

**Concretement :** si on reste 100% Bitbucket pour les plugins :
- L'admin doit **re-uploader le ZIP manuellement** a chaque mise a jour
- Les non-devs (support) ne recoivent **jamais** les MAJ automatiquement
- Les triggers cloud sont **impossibles**
- On perd **l'interet principal** de Cowork pour une equipe

**Ce qu'on propose :** utiliser GitHub **uniquement pour les plugins Claude** (2-3 repos). Le code reste sur Bitbucket (128 repos). C'est une coexistence, pas une migration.

---

## Pourquoi GitHub ?

### Aujourd'hui (sans GitHub)

| Probleme | Impact |
|----------|--------|
| Les plugins/skills doivent etre installes manuellement sur chaque poste | Temps perdu, versions differentes |
| Pas de mise a jour automatique | Les correctifs ne sont pas deployes |
| Impossible d'utiliser les triggers cloud (automatisation planifiee) | Pas d'agents autonomes |
| Les developpeurs ne peuvent pas partager leurs outils via la marketplace interne | Fragmentation |

### Demain (avec GitHub connecte)

| Avantage | Detail |
|----------|--------|
| **Auto-update plugins** | Un push sur GitHub → tout le monde recoit la mise a jour en 30 minutes |
| **Marketplace interne** | Nos propres plugins (support, dev, analyse) distribues a toute l'equipe |
| **Triggers cloud** | Agents autonomes qui tournent sur les serveurs Anthropic (pas besoin que la machine soit allumee) |
| **Zero intervention utilisateur** | Les non-techniques recoivent tout automatiquement |

---

## Cas d'usage concrets

### 1. Equipe Support — Automatisation tickets

**Objectif :** Les supports utilisent Claude Cowork pour trier, analyser et repondre aux tickets.

**Ce que ca donne :**
- Un support recoit un ticket → ouvre Claude Cowork → Claude cherche dans la base de connaissances partagee → propose une reponse
- Si le support corrige la reponse → Claude apprend pour la prochaine fois
- Les skills de triage et reponse sont partagees et mises a jour automatiquement

**Besoin GitHub :** Le plugin "Support Neoteem" est sur GitHub, l'admin le connecte au marketplace Cowork en mode auto-install. Quand on ameliore le plugin, tout le monde recoit la mise a jour sans rien faire.

### 2. Equipe Dev — Outils partages

**Objectif :** Les developpeurs ont des agents et skills Claude Code partages (architecture, tests, review, migration).

**Ce que ca donne :**
- Un dev ouvre Claude Code → les agents (architect, dev, test-writer, code-reviewer) sont deja configures
- Les skills de reference (conventions API, patterns SQL, regles metier) sont partagees
- Quand on corrige un agent ou ajoute un skill → tout le monde recoit la mise a jour

**Besoin GitHub :** Le plugin "Neoteem Dev Tools" est sur GitHub, reference dans les `settings.json` des repos Bitbucket. Les devs recoivent les updates au `git pull`.

### 3. Agents autonomes planifies

**Objectif :** Des agents qui tournent automatiquement sans intervention humaine.

**Exemples :**
- Lundi-vendredi 8h : sync de la base de connaissances (deja en place en local)
- Tous les 2 jours : verification des nouveautes Claude Code
- Chaque semaine : audit de qualite des repos

**Besoin GitHub :** Les triggers cloud necessitent un repo GitHub pour cloner/modifier/push.

---

## Ce que ca ne change PAS

- **Bitbucket reste notre source principale** pour le code (repos neot-v2, neofront)
- **Aucune migration de code** — GitHub est utilise uniquement pour les plugins/outils Claude
- **Aucun cout supplementaire** — GitHub gratuit pour les repos publics, et les repos prives sont gratuits pour les petites equipes
- **Aucun risque securite** — GitHub est utilise par 100M+ de developpeurs, et Anthropic est un partenaire officiel de Microsoft/GitHub

---

## Action requise

### Pour l'administrateur (5 minutes, une seule fois)

1. Se connecter a **https://claude.ai** avec le compte admin
2. Aller dans **Settings** → **Organization** → **Integrations**
3. Cliquer **Connect GitHub**
4. Autoriser l'acces (uniquement aux repos necessaires)

### Pour les DevOps (1 heure, une seule fois)

1. Creer un repo GitHub prive `neoteem/claude-plugins` (ou public si on prefere)
2. Y mettre les plugins (skills, agents, configurations)
3. Configurer le GitHub sync dans le marketplace Cowork

### Pour les utilisateurs (rien a faire)

Les plugins arrivent automatiquement. Aucune action requise.

---

## Comparaison des couts

| Solution | Cout mensuel | Maintenance |
|----------|-------------|-------------|
| **Sans GitHub** (actuel) | 0 EUR (mais temps perdu) | Admin re-upload ZIP manuellement a chaque update |
| **Avec GitHub Free** | 0 EUR | Auto-sync, zero maintenance |
| **Avec GitHub Team** (optionnel) | ~4 EUR/user/mois | Repos prives illimites, controle d'acces avance |

---

## Planning propose

| Semaine | Action | Qui |
|---------|--------|-----|
| S1 | Connecter GitHub a l'orga Claude | Admin |
| S1 | Creer le repo plugins GitHub | DevOps |
| S2 | Deployer le plugin Support | Raphael + DevOps |
| S2 | Deployer le plugin Dev Tools | Raphael |
| S3 | Former l'equipe support | Raphael + support lead |
| S3 | Activer Dispatch pour l'equipe | Admin |

---

## Questions frequentes

**Q : Ca remplace Bitbucket ?**
Non. Bitbucket reste pour le code. GitHub est uniquement pour les plugins/outils Claude.

**Q : C'est securise ?**
Oui. GitHub est utilise par Microsoft, Google, Amazon, et Anthropic eux-memes. Le repo peut etre prive.

**Q : Ca marche si la machine est eteinte ?**
Les triggers cloud oui (ils tournent chez Anthropic). Les plugins se mettent a jour au prochain demarrage de Claude.

**Q : Et si on veut arreter ?**
Deconnecter GitHub dans les settings. Les plugins deja installes continuent de fonctionner, ils ne se mettent juste plus a jour.

---

## Annexe : Architecture cible

```
GitHub (plugins uniquement)              Bitbucket (code)
  neoteem/claude-plugins/                  neot-v2/* (60 repos)
    ├── support-plugin/                    neofront/* (68 repos)
    │   ├── skills/ticket-handler/
    │   ├── skills/knowledge-search/
    │   └── plugin.json
    └── dev-tools-plugin/
        ├── skills/architecture-rules/
        ├── agents/code-reviewer/
        └── plugin.json
           │
           ▼
    Marketplace Cowork (auto-sync)
           │
    ┌──────┴──────┐
    ▼              ▼
  Support        Devs
  (Cowork)     (Claude Code)
  Auto-install   settings.json
```
