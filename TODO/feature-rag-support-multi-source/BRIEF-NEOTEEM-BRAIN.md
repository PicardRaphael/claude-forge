# BRIEF — neoteem-brain : skill « Jira → brain »

> Contrat pour `neoteem-brain`. À copier dans `neoteem-brain/.claude/skills/` (ou TODO du repo brain). Voir `SPEC.md` §3.
> Rôle : alimenter le vault curé depuis les tickets Jira fermés. Le vault est ensuite traduit en Confluence (skill ② côté neo_ia), seule source embeddée.

## Contexte
Vault neoteem-brain déjà curé : `07-Support/{faq,procedures,problemes-connus}`, `06-Regles-Metier`, MOC-Support, templates, frontmatter v2. Écriture via plugins `neoteem-brain-admin`. Gabarit : skill existante `ticket-analyzer`.

## À faire — V5 (indépendante, parallélisable)
**CREER** `neoteem-brain/.claude/skills/jira-to-brain/SKILL.md` :

1. **Déclenchement** : tâche planifiée Claude Code desktop, fin de semaine, batch tickets fermés.
2. **Lecture Jira** : API REST `POST /rest/api/3/search` (le MCP Jira est admin-only, pas de JQL ; acli absent). Credentials Atlassian = table `parametrage` type=`documentation_lojii` (même domaine neoteem.atlassian.net) — à récupérer (ou variables d'env si la skill n'a pas accès à la DB neo_ia ; **à confirmer**).
3. **JQL incrémental** : `project IN (<projets à confirmer>) AND statusCategory = Done AND resolutiondate >= "<dernier_traité>" ORDER BY resolutiondate ASC`.
4. **Mémoire du déjà-traité** : sidecar `neoteem-brain/.claude/skills/jira-to-brain/state/processed.json` (`{last_resolutiondate, processed_keys[]}`). Ne pas tout refaire ; ignorer les tickets déjà dans `processed_keys`.
5. **Classification par domaine** (par Claude, PAS que support) : bug/contournement → `07-Support/problemes-connus/pb-*.md` · question récurrente → `07-Support/faq/faq-*.md` · procédure → `07-Support/procedures/proc-*.md` · règle métier révélée → `06-Regles-Metier/*.md` · autres branches selon contenu.
6. **Format note** : templates brain existants (`Templates/support-*.md`, `regle-metier.md`), frontmatter v2 (aliases ≥3, tags `#domaine/X`, `#statut/draft` à la création), corps = paire problème/solution, source = réf ticket Jira.
7. **Dédup** : `search_brain` (MCP obsidian-brain) AVANT création → si une note couvre déjà le sujet, **enrichir** (`append_note`/`insert_section`) au lieu de dupliquer ; skill `deduplicate-brain` en appui.
8. **Écriture** : via plugin `neoteem-brain-admin:neo-brain-support-admin` (07-Support) ou `neo-brain-dev-admin` (06/Knowledge). **Gate humaine obligatoire** (aucune écriture sans OK explicite).

## Critères de done
- [ ] La skill lit les tickets fermés via REST Jira (pas le MCP admin).
- [ ] Incrémental : un 2e run ne retraite pas les tickets déjà dans `processed.json`.
- [ ] Un ticket est rangé dans la BONNE branche (support OU règle métier OU autre) selon son contenu.
- [ ] Note produite conforme aux templates brain (frontmatter v2, `#statut/draft`).
- [ ] Sujet déjà couvert → note existante enrichie, pas de doublon.
- [ ] Aucune écriture sans gate humaine.

## Implementation Notes
Maintenir des notes d'implémentation dans le repo brain (convention locale).

## Acceptance Tests
- Run sur un batch de tickets fermés → notes créées dans les bonnes branches, `processed.json` mis à jour.
- 2e run immédiat → 0 nouvelle note (tout déjà traité).
- Ticket dont le sujet existe déjà en note → enrichissement, pas de doublon.

## Bloquants PO (SPEC §7)
Périmètre projets Jira (`project IN ...`) · accès credentials Jira depuis le repo brain (parametrage DB neo_ia vs env) · stockage état sidecar validé.
