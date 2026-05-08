---
titre: "Plugins neoteem-brain — architecture 5 plugins"
resume: "5 plugins Cowork separes (dev/dev-admin/dev-ia/support/support-admin) + 4 Claude Chat, role-based"
aliases:
  - "neoteem-brain plugins"
  - "brain plugins"
  - "plugins cowork neoteem"
  - "architecture plugins brain"
  - "role-based vault access"
domaine: technique
type: technique
derniere-maj: 2026-04-29
auteur: claude
sources:
  - "[[mcp-obsidian-brain-v2]]"
tags:
  - "#type/technique"
  - "#domaine/neoteem"
  - "#projet/neoteem-brain"
---

## Description

Architecture role-based pour l'acces au vault neoteem-brain. 5 plugins Cowork independants, chacun installable separement via l'orga.

## Plugins Cowork

| Plugin | Acces vault | Pour qui |
|--------|-------------|----------|
| `neoteem-brain-dev` | Lecture seule | Tous les devs |
| `neoteem-brain-dev-admin` | Lecture + ecriture | Leads dev |
| `neoteem-brain-dev-ia` | Lecture + ecriture | Devs IA (cross-ref vault + code) |
| `neoteem-brain-support` | Lecture seule | Tout le support |
| `neoteem-brain-support-admin` | Lecture + ecriture | Leads support |

## Plugins Claude Chat

Meme split (dev, dev-admin, support, support-admin) dans `claude-chat-plugins/`.

## Budget reads

- **Support** : 3-4 reads sur tous les flux (100% reussite)
- **Dev** : 3-4 reads sur tous les flux
- Regle : "Lire TOUTES les notes pertinentes, croiser les informations"

## Ecriture MCP

Les skills admin utilisent `create_note`, `append_note`, `update_property`. Chaque ecriture cree un commit git sur `mcp/<username>`. Raphael merge manuellement.

## Quand utiliser

Reference pour l'installation, la configuration ou l'ajout de plugins brain sur un poste ou profil Neoteem. Aussi pour comprendre le split lecture/ecriture par role.

## Liens

- [[MOC-Techniques]]
- [[mcp-obsidian-brain-v2]]
- [[SQLite FTS5 pour vault]]
