---
titre: "Vault health — run du 2026-07-16 (premier run)"
resume: "Premier run vault-health : PASS — lint 11→9 low_aliases (2 fixes), 0 brisé/orphelin/YAML, consultation 7j saine (read 72 / search 25 / create 27), adoption cross-repo 0 (baseline J0 extension user-scope), inbox 1 note"
aliases:
  - "vault health 16 juillet 2026"
  - "premier run vault-health"
  - "rapport sante vault juillet"
  - "vault-health baseline cross-repo"
type: synthese
domaine: vault
derniere-maj: 2026-07-16
auteur: claude
tags:
  - "#type/synthese"
  - "#domaine/vault"
---
**Verdict global : PASS**

Premier run de la routine hebdo (cf [[pattern-vault-llm-karpathy]] pour le failure mode surveillé et [[decision-vault-agent-first]] pour la mesure d'adoption).

## Lint

| Catégorie | Pré | Post |
|---|---|---|
| low_aliases | 11 | 9 |
| no_tags | 0 | 0 |
| orphans | 0 | 0 |
| broken_yaml | 0 | 0 |
| broken_wikilinks | 0 | 0 |

Fixes appliqués (liste fermée (b), 2/2 autorisés) :
1. `critique-plan-modernisation-bdd-claude` — 0 → 4 aliases
2. `delegate-guard-pattern` — 3 → 4 aliases

Fix (a) sans objet : 0 wikilink brisé. Signalements : 9 notes restent à aliases < 4 (toutes à 3, majoritairement des critiques/synthèses datées — candidates aux prochains runs, 2/semaine).

## Consultation (7 j)

Première mesure — pas de rapport précédent.

- `read_note` : 72 calls · `read_section` : 11 · `read_note_by_path` : 9 → **92 lectures**
- `search_brain` : 25 calls
- `create_note` : 27 calls
- Ratio create/search = 1,08× (seuil d'alerte : > 3×) → **pas de signal write-only**. Lecture >> écriture : vault consulté, pas seulement rempli.

Aucune alerte. Ces chiffres deviennent la baseline du prochain run.

## Adoption cross-repo

- Événements `search_brain` + `read_note` depuis 2026-07-09 : **100 % en provenance de claude-forge, 0 hors forge**.
- Attendu : l'extension user-scope (MCP user + `~/.claude/CLAUDE.md`) a été déployée le 2026-07-16 même — la mesure démarre aujourd'hui (J0).
- **Verdict J+14 : non dû** (premier run ≥ 2026-08-03). Seuil à cette échéance : ≥ 10 consultations hors forge sur 14 j, sinon recommander retrait de `~/.claude/CLAUDE.md` + note de dette (arbitrage Raphael).

## Inbox

1 note (`context-actuel`) ≤ seuil 3 → rien à trier.
