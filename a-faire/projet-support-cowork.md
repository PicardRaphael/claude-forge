# Projet : Support Neoteem — Claude Cowork

**Public :** Equipe support (non-technique)
**Outil :** Claude Cowork (Claude Desktop)
**Statut :** A valider

---

## Objectif

Les supports utilisent Claude Cowork pour :
1. **Trier** les tickets automatiquement (priorite, categorie, assignation)
2. **Chercher** dans la base de connaissances avant de repondre
3. **Capitaliser** — chaque resolution enrichit la base pour les prochains
4. **Escalader** intelligemment quand c'est hors scope

---

## Architecture

```
Support ouvre Claude Desktop (Cowork)
  │
  ├── Plugin "Support Neoteem" (auto-installe)
  │   ├── Skill : ticket-triage (analyse + classification)
  │   ├── Skill : knowledge-search (cherche dans la base)
  │   └── Skill : escalation (qui contacter pour quoi)
  │
  └── Dossier reseau partage \\serveur\support-brain\
      ├── FAQ/                    (questions frequentes)
      ├── Process/                (procedures par type de ticket)
      ├── Solutions/              (tickets resolus capitalises)
      ├── Escalade/               (matrice d'escalade)
      └── CLAUDE.md               (regles et contexte)
```

---

## Comment ca marche pour le support

### Scenario : nouveau ticket

```
1. Le support recoit un ticket : "Mon loyer n'est pas debite"
2. Il ouvre Claude Desktop → ecrit le ticket
3. Claude cherche dans le dossier partage :
   - FAQ/ → "Non-prelevement loyer"
   - Solutions/ → 3 tickets similaires deja resolus
   - Process/ → Procedure verification prelevement
4. Claude propose une reponse structuree
5. Le support valide ou modifie
6. Claude capitalise la resolution dans Solutions/
7. Le prochain support qui a le meme probleme → Claude trouve directement
```

### Scenario : escalade

```
1. Le support recoit un ticket technique complexe
2. Claude analyse → detecte que c'est hors scope support
3. Claude consulte Escalade/matrice.md
4. Propose : "Ce ticket concerne le calcul des charges.
   Escalader a Jerome (equipe dev backend)."
```

---

## Ce dont les supports ont besoin

| Element | Fourni par |
|---------|-----------|
| Claude Desktop installe | DevOps (1 fois par poste) |
| Plugin "Support Neoteem" | Auto-installe via marketplace (GitHub sync) |
| Dossier reseau `support-brain` | DevOps (1 fois, dossier partage) |
| Formation initiale (1h) | Raphael |

**Les supports n'ont PAS besoin de :**
- Git / terminal / ligne de commande
- Compte GitHub
- Connaissances techniques

---

## Memoire partagee — comment ca fonctionne

```
Support A resout un ticket lundi
  → Claude ecrit dans \\serveur\support-brain\Solutions\prelevement-loyer.md
  → Git push automatique (script DevOps en background)

Support B recoit un ticket similaire mardi
  → Claude cherche dans le dossier → trouve la solution de Support A
  → Propose la meme resolution adaptee
```

Le dossier reseau EST la memoire partagee. Pas besoin d'outil complique.

---

## Structure du dossier support-brain

```
support-brain/
├── CLAUDE.md                 # Regles et contexte pour Claude
├── FAQ/
│   ├── prelevement-loyer.md
│   ├── quittance-manquante.md
│   ├── relance-impaye.md
│   └── ...
├── Process/
│   ├── verification-prelevement.md
│   ├── creation-bail.md
│   ├── cloture-compte.md
│   └── ...
├── Solutions/
│   ├── 2026-04/
│   │   ├── sol-prelevement-rejete.md
│   │   ├── sol-erreur-calcul-charges.md
│   │   └── ...
│   └── ...
├── Escalade/
│   ├── matrice.md             # Qui contacter pour quoi
│   └── contacts.md            # Liste des referents par domaine
└── Templates/
    ├── reponse-standard.md
    ├── escalade.md
    └── ...
```

---

## Plugin "Support Neoteem"

### Skills incluses

| Skill | Description | Trigger |
|-------|-------------|---------|
| `ticket-triage` | Analyse le ticket, classifie (priorite, categorie, domaine) | Quand le support colle un ticket |
| `knowledge-search` | Cherche dans FAQ/, Process/, Solutions/ | Automatique avant toute reponse |
| `escalation` | Consulte la matrice d'escalade et propose le bon referent | Quand le ticket est hors scope |
| `capitalize` | Ecrit la resolution dans Solutions/ pour les prochains | Apres validation de la reponse |

### Mise a jour automatique

Le plugin est sur GitHub. Quand on l'ameliore (nouvelle skill, correction) :
1. Push sur GitHub
2. Marketplace Cowork detecte le changement
3. Tous les postes support recoivent la MAJ en 30 min
4. Zero action du support

---

## Prerequis

| Prerequis | Qui | Quand |
|-----------|-----|-------|
| Abonnement Claude Team actif | Deja fait | - |
| Admin connecte GitHub a l'orga | Admin | Semaine 1 |
| Dossier reseau `support-brain` cree | DevOps | Semaine 1 |
| Claude Desktop installe sur les postes support | DevOps | Semaine 1 |
| Plugin cree et publie sur GitHub | Raphael | Semaine 2 |
| Formation support (1h) | Raphael | Semaine 3 |

---

## KPIs attendus

| Metrique | Avant | Apres (estime) |
|----------|-------|----------------|
| Temps moyen resolution ticket | ? min | -40% |
| Tickets escalades a tort | ? /semaine | -60% |
| Temps de formation nouveau support | ? jours | -50% |
| Base de connaissances enrichie | 0 | +10 solutions/semaine |
