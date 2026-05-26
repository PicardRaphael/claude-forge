# ia-lead-neoteem

Boite a outils du Responsable IA chez Neoteem (Loji). Six skills independants couvrent les principaux contextes du poste :

| Skill | Pour quoi |
|---|---|
| `reunion-direction` | Reunion direction sur strategie IA (objectifs, budget, ROI, gouvernance) |
| `reunion-metier-interne` | Reunion avec un metier interne (dev, design, devops, support, QA, commercial, redaction) pour capter les besoins puis suggerer des cas d'usage IA |
| `reunion-produit-loji` | Cadrage d'une feature IA dans Loji (NeoChat, NeoDocs, GEMINI, nouvelle brique) |
| `reunion-client-projet` | Reunion avec un client B2B sur son projet IA d'entreprise |
| `management-equipe` | 1-1, rituels equipe, OKR, feedback, recrutement, conduite du changement IA |
| `formation-ia` | Conception et animation de formations IA pour les collaborateurs Neoteem |
| `ticket-claude-code` | Redaction de tickets Jira exploitables par humains OU par Claude Code en autonomie |

## Deux formats d'usage

### 1. Comme plugin Claude Code

Installer depuis un repo Git :

```
/plugin marketplace add <path/to/this/repo>
/plugin install ia-lead-neoteem
```

Ou en local sur ton poste, via `~/.claude/plugins/` :

```bash
git clone <repo> ~/.claude/plugins/ia-lead-neoteem
```

Les 6 skills se chargent automatiquement quand Claude Code detecte un declencheur dans ta demande.

### 2. Comme skills Claude.ai

Chaque dossier dans `skills/` contient un `SKILL.md` autonome. Tu peux :

- les copier dans la fonctionnalite "Skills" de claude.ai si tu y as acces
- ou simplement coller le contenu du SKILL.md pertinent en debut de conversation comme contexte

## Contexte ancre

Tous les skills supposent ce contexte :

- **Neoteem** edite **Loji**, ERP AI-native pour syndics et gerance locative (Meylan / Grenoble)
- **Stack** : back2.0 (Bun / Hono / Drizzle / PostgreSQL / GCP Cloud Run), architecture hexagonale, OpenAPI
- **Outillage IA interne** : Claude Code, Cowork, MCP Atlassian, **neoteem-brain** (Obsidian vault)
- **Briques IA existantes Loji** : NeoChat, NeoDocs, integration GEMINI
- **Concurrents** : Genius Immo, Reemia AI
- **Equipe Raphael** : dev, design, devops, redaction

## Reglages communs a tous les skills

- Reponses en francais
- Pas d'emojis
- Format copy-paste-ready
- Rappel RGPD / risques systematique mais court
- Pour les metiers internes : on capte d'abord les besoins, on suggere ensuite
- Reunions cibles : 1h-1h30
- Sortie type : ordre du jour, questions a poser, points d'attention, livrables

## Versionning

v1.0.0 - mai 2026 - sortie initiale 6 skills.
