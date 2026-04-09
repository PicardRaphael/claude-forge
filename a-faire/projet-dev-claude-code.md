# Projet : Dev Tools Neoteem — Claude Code

**Public :** Equipe developpement (technique)
**Outil :** Claude Code (CLI terminal)
**Statut :** Partiellement en place (ia_back, neoteem-brain)

---

## Objectif

Les developpeurs ont un kit Claude Code partage avec :
1. **Agents, skills, rules, hooks** specifiques a chaque repo
2. **Connexion au vault neoteem-brain** = contexte metier partage pour tous
3. **Mise a jour automatique** via plugin Bitbucket (poll 1h)

---

## Principe

Chaque repo a ses propres agents/skills/rules/hooks dans `.claude/` — adaptes a son stack et son metier. Mais **tous les repos partagent la connexion au vault neoteem-brain** via le kit `neo-brain` (skill + wrapper CLI).

```
Bitbucket
  neot-v2/ia_back/.claude/         → agents TS/Bun specifiques ia_back
  neot-v2/bdd/.claude/             → agents PG specifiques bdd
  neot-v2/neo_ia/.claude/          → agents Python specifiques neo_ia
  neot-v2/ws/.claude/              → agents Go specifiques ws
      │
      └── Tous ont : skills/neo-brain/ → connexion vault neoteem-brain
```

**neoteem-brain** est le point commun : tout le monde y cherche le contexte metier avant de coder.

---

## Ce qui existe deja

| Repo | .claude/ | neo-brain | Statut |
|------|----------|-----------|--------|
| ia_back | Complet (11 agents, 16 skills, 4 rules, 4 hooks) | Oui (7 agents connectes) | Pret |
| neoteem-brain | Complet (4 agents Agent Teams, 7 skills, 10 rules) | Natif | Pret |
| neo_ia | Basique (hooks seulement) | Non | A configurer |
| bdd | Rien | Non | A configurer |
| ws | Rien | Non | A configurer |
| ~123 autres repos | Rien | Non | A evaluer |

---

## Comment connecter un nouveau repo au vault

Le kit `neo-brain` est disponible a la racine du vault : `neoteem-brain/neo-brain/`.

Pour connecter un repo :
1. Copier `neo-brain/` dans `.claude/skills/` du repo
2. Ajouter `neo-brain` dans les `skills:` des agents metier
3. C'est tout — Claude cherche dans le vault avant de coder

Documentation complete : `neoteem-brain/neo-brain/README.md`

---

## Plugin partage Bitbucket (optionnel, pour les composants communs)

Si des agents/skills sont identiques entre plusieurs repos, on peut les extraire dans un plugin Bitbucket :

```json
// settings.json de chaque repo
{
  "extraKnownMarketplaces": {
    "neoteem-tools": {
      "source": { "source": "git-url", "url": "https://bitbucket.org/neot-v2/claude-dev-tools.git" }
    }
  },
  "enabledPlugins": { "dev-tools@neoteem-tools": true }
}
```

Claude Code poll le repo au demarrage + toutes les heures. Push sur Bitbucket → les devs recoivent la MAJ automatiquement. **Pas besoin de GitHub pour les devs.**

---

## Prerequis

| Prerequis | Qui | Quand |
|-----------|-----|-------|
| Kit neo-brain deploye dans les repos actifs | Raphael | Progressif |
| `.claude/` configure par repo (agents/skills adaptes au stack) | Raphael | Par repo |
| Plugin Bitbucket si composants communs | Raphael + DevOps | Si besoin |
| Former les devs (30 min) | Raphael | Par equipe |

---

## KPIs attendus

| Metrique | Avant | Apres (estime) |
|----------|-------|----------------|
| Devs avec contexte metier (neo-brain) | 2 | Tous |
| Temps de comprehension d'un domaine metier | 1h+ (lire Confluence, demander) | 5 min (vault) |
| Qualite du code premier jet | Variable | +40% (contexte metier des le depart) |
