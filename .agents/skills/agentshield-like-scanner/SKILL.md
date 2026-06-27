---
name: agentshield-like-scanner
description: ALWAYS invoke when auditing a Claude Code setup specifically for SECURITY risks (prompt injection, unsafe MCP, dangerous hooks/permissions) — red-team/blue-team pipeline. NOT for general config/quality audit (use repo-inspector mode=audit for that). DO NOT run a security audit manually without invoking first.
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, mcp__forge-brain__read_note, mcp__forge-brain__create_note
model: sonnet
effort: high
---

# AgentShield-like Scanner — audit sécurité pipeline 3-Opus

**Inspiré du pattern ECC AgentShield** (Affaan Mustafa, Grand Prize Anthropic Hacker Marathon 2026). Pipeline `red team → blue team → auditor` transposé à l'audit forge.

La skill DÉCRIT le pipeline que la session principale orchestre. La session lance les 3 sous-agents ; cette skill ne les lance pas elle-même.

---

## Scope d'audit (5 catégories)

| Catégorie | Périmètre |
|-----------|-----------|
| **Secrets / credentials** | `.mcp.json`, settings.json, hooks scripts, CLAUDE.md — aucun secret en clair |
| **Permissions** | `permissionMode` sur tous agents, `disallowedTools` cohérent, `allowed-tools` skill minimal |
| **Hook injection** | Scripts hooks : pas de commandes arbitraires, pas de lecture stdin non filtrée, pas de path traversal |
| **MCP risk** | Servers actifs, wildcard `mcp__server__*`, ports exposés, auto-start non voulu |
| **Agent config** | `memory: project` présent, `effort` approprié, skills: cohérentes avec body, modèle correct |

---

## Pipeline 3 agents Opus (session principale orchestre)

### Agent 1 — Red Team (model: opus)
**Mission** : trouver exploit chains, vecteurs d'attaque, configurations dangereuses.

Brief à passer :
```
Rôle : red team agent — cherche exploit chains dans ce setup Claude Code.
Périmètre : [contenu .claude/ + settings.json + .mcp.json]
Cherche : secrets exposés, permissions trop larges, hooks injectables, MCP dangereux.
Format : liste FINDINGS avec sévérité (CRITICAL/HIGH/MEDIUM/LOW) + vecteur d'attaque exact.
```

### Agent 2 — Blue Team (model: opus)
**Mission** : évaluer les protections existantes, identifier ce qui est déjà mitigé.

Brief à passer :
```
Rôle : blue team agent — évalue les protections du setup.
Périmètre : [contenu .claude/ + settings.json + .mcp.json]
Pour chaque protection trouvée : est-elle suffisante ? Contournable ?
Format : liste MITIGATIONS avec statut (SOLIDE/PARTIEL/ABSENT) par catégorie des 5 scopes.
```

### Agent 3 — Auditor (model: opus)
**Mission** : synthétiser red + blue en prioritized risk assessment.

Brief à passer :
```
Rôle : auditor agent — synthétise les rapports red et blue team.
Red team findings : [insérer rapport Red]
Blue team mitigations : [insérer rapport Blue]
Produit : risk assessment priorisé (CRITICAL first), avec verdict par catégorie et top-3 actions immédiates.
```

---

## Workflow session principale

1. **Préparer le contexte** : lire `.claude/settings.json`, `.mcp.json`, liste agents/skills/hooks via Glob
2. **Lancer Red et Blue en parallèle** (2 appels Task simultanés)
3. **Attendre les 2 rapports**
4. **Lancer Auditor** avec les 2 rapports en contexte
5. **Présenter à Raphael** : risk assessment + top-3 actions immédiates

---

## Gotchas

- **La skill DÉCRIT le pattern, ne l'exécute pas** : la session principale orchestre les 3 agents. Cette skill est une knowledge base, pas un orchestrateur.
- **Red et Blue en PARALLÈLE** (pas séquentiel) : c'est l'avantage du pattern ECC par rapport à un audit linéaire.
- **Auditor reçoit LES DEUX rapports** avant de synthétiser — ne pas lancer Auditor avant d'avoir Red ET Blue complets.
- **Ne PAS confondre avec repo-inspector** : repo-inspector = audit conformité canonique (frontmatter, taille, structure). AgentShield = audit sécurité (exploits, permissions, injection).
- **Vérifier empiriquement les CRITICAL** avant de les relayer : sous-agents Opus peuvent surestimer la sévérité sur des patterns courants (cf `feedback_auditor_false_positives`).
- **`.mcp.json` souvent hors périmètre des audits standards** — l'inclure explicitement dans le brief.
- **Settings.json self-modification** : hook `auto-mode classifier` bloque les édits directs de settings.json. Si un CRITICAL concerne settings.json → signaler pour édition manuelle Raphael.

---

## Output attendu

```
## Risk Assessment — [repo] — [date]

### CRITICAL (0)
### HIGH (N)
  - [vecteur] : [description] | Mitigation : [action]
### MEDIUM (N)
### LOW (N)

### Top-3 actions immédiates
1. ...
2. ...
3. ...
```

---

## Référence

Source vault : `[[ecc-pattern-personal-dev-setup]]` section AgentShield
Pattern original : `github.com/affaan-m/everything-claude-code` — `npx ecc-agentshield scan --opus`
Auteur : [[affaan-mustafa-ecc-hackathon-winner]] — Grand Prize Anthropic Hacker Marathon 2026

---

## Apprentissage

Après chaque scan AgentShield-like complété :
- Catégorie de CRITICAL/HIGH la plus fréquente sur le repo audité
- Taux faux positifs Auditor (findings Red non confirmés par Blue)
- Ajouter patterns nouveaux dans `vault/Knowledge/erreurs/` si exploit chain inédit découvert
- Mettre à jour les 5 catégories scope si une nouvelle classe de risque émerge
