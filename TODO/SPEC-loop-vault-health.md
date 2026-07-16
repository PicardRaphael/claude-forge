---
feature: loop-vault-health
date_spec: 2026-07-16
type: loop-code
statut: valide
---

# SPEC loop — vault-health (check hebdo du cerveau forge-brain)

> Généré par /loop-forge. Conception uniquement — la création des composants est une étape séparée.

## 0. Contexte

**Orga / domaine :** forge perso Raphael (Jarvis) — maintenance du vault forge-brain (560 notes, MCP localhost:8091).
**Objectif business :** garder le cerveau vivant — consensus état de l'art juillet 2026 : « la maintenance doit être PLANIFIÉE, pas espérée » ; un vault seulement écrit stagne. Complète `/forge-review` (stratégique, mensuel) par un check santé hebdo léger. Porte aussi la MESURE de l'extension cross-repo du cerveau (décision 16 juil. 2026, rendez-vous DA J+14).
**Branche :** code (appels MCP + rapport, exécutés par une session Claude Code planifiée)
**Environnement :** repo claude-forge (Windows 11, MCP forge-brain local port 8091)

---

## 1. Job

**Description reformulée :** « Depuis le MCP forge-brain (lint, usage, tool_events) et 0-Inbox, vérifier chaque semaine la santé du vault, appliquer les micro-fixes triviaux, mesurer la consultation (dont hors-forge), jusqu'à production d'un rapport court daté pour Raphael. »

- **Fréquence actuelle (manuelle) :** ad hoc — dernier équivalent : audit complet du 16 juil. 2026 (session dédiée) ; sinon lint/usage consultés irrégulièrement
- **Coût/temps actuel :** ~15-30 min/semaine quand fait à la main ; dérive silencieuse quand pas fait (cf drift doctrine↔réel documenté 8 juin)
- **ROI attendu de l'automatisation :** détection hebdo systématique des dérives (liens brisés, chute de consultation, inbox qui s'accumule) + série de mesure continue de l'adoption cross-repo — au prix d'un run court read-mostly

---

## 2. Type de loop

**Type retenu :** time-loop

- **Justification :** job récurrent sur intervalle fixe (hebdo), autonome, sans condition de convergence (≠ goal-loop) ni déclenchement manuel fréquent (≠ inner-loop)
- **Critère de terminaison nominal (succès) :** rapport écrit avec les 4 sections + triple check PASS
- **Critère de terminaison exceptionnel :** timeout 15 min | MCP injoignable après 1 relance via mcp-autostart | kill-switch = suppression/pause de l'entrée cron

---

## 3. Périmètre

### Périmètre d'écriture (où le loop écrit)

- **Repo d'écriture (unique) :** claude-forge (vault via MCP : rapport + micro-fixes)
- **Repos en lecture croisée :** transcripts `~/.claude/projects/*` (via `search_tool_events`, indexés par le MCP) — lecture seule
- **Pattern multi-repo si applicable :** N/A

### Périmètre de traitement (sur quoi le loop opère)

- **Objets traités :** notes du vault (lint complet), logs usage MCP (`usage_stats(7)`), événements tool_use cross-projets (`search_tool_events`), notes de `0-Inbox/`
- **Même que le repo d'écriture ?** oui pour le vault ; les tool_events proviennent de tous les projets machine mais sont lus via le MCP forge (pas d'accès direct aux autres repos)
- **Filtre / bornage :** lint complet ; usage fenêtre 7 j ; tool_events `project ≠ claude-forge` depuis le run précédent ; inbox signalée si > 3 notes

### Stack / Implémentation _(code)_

- **Langage / runtime :** session Claude Code planifiée (cron natif CC) invoquant la skill `/vault-health` — pas de script Python dédié (toutes les opérations = outils MCP existants)
- **Outils CLI requis :** aucun nouveau (MCP forge-brain 22 outils ; `py` pour mcp-autostart en relance)
- **APIs / services externes :** aucun
- **Path dans le repo :** skill `.claude/skills/vault-health/` (à créer) ; rapports dans `vault/claude-forge/Knowledge/reviews/vault-health-YYYY-MM-DD.md`

### Inputs / Outputs _(code)_

| Direction | Source/Dest | Format | Volume estimé |
|-----------|-------------|--------|---------------|
| Input | `lint_vault(limit=0)` | JSON/markdown | ~2-5k chars |
| Input | `usage_stats(days=7)` | table markdown | ~1k chars |
| Input | `search_tool_events(project≠claude-forge, since=dernier run)` | événements | ~5-15k chars |
| Input | `list_notes("0-Inbox")` | liste | ~0,5k chars |
| Output | note rapport `Knowledge/reviews/vault-health-YYYY-MM-DD.md` | note vault (create_note) | ~60-100 lignes |
| Output | micro-fixes triviaux (liste fermée) | writes MCP ciblés | 0-5 notes/run |

### Gestion d'erreur _(code)_

- **Retry policy :** MCP down → lancer `py .claude/hooks/mcp-autostart.py`, attendre 10 s, 1 seule relance
- **Erreurs fatales (arrêt loop) :** MCP injoignable après relance ; vault illisible → écrire l'échec dans `output/vault-health-FAIL-YYYY-MM-DD.md` (fichier repo, hors MCP) et terminer FAIL
- **Erreurs non-fatales (log + continue) :** une catégorie lint illisible, tool_events vides → section « non mesurée cette semaine » dans le rapport
- **Dead letter / items échoués :** fixes non appliqués → listés dans le rapport, jamais retentés en boucle
- **Verrou concurrence :** NON — run court lundi 09h ; le run s'exécute dans le repo forge (convention single-writer respectée : les update/delete y sont autorisés)

---

## 4. Les 4 briques

| Brique | Description |
|--------|-------------|
| **Déclencheur** | Invocation MANUELLE hebdo par Raphael (`/vault-health`), lundi de préférence — décision 16 juil. 2026 : pas de persistance OS. (Le cron natif CC s'est révélé session-only/7 j max ; la tâche planifiée Windows a été proposée et déclinée.) |
| **Source(s)** | MCP forge-brain : `lint_vault`, `usage_stats(7)`, `search_tool_events`, `list_notes("0-Inbox")` + rapport de la semaine précédente (comparaison tendance) |
| **Critère de jugement** | Triple check structurel (cf §5) |
| **Action** | Micro-fixes triviaux liste fermée + rapport hebdo 4 sections + verdict adoption cross-repo |

### Micro-fixes AUTORISÉS en auto (liste FERMÉE — tout le reste = rapport seulement)

1. Wikilink brisé pointant une non-note (skill, rule, fichier) → réécrire en texte nu/backticks (doctrine mcp-vault-llm-design)
2. Aliases < 4 → compléter (≤ 2 notes/run, jamais sur les notes externes/kepano)

Interdits en auto : suppression de note, move, modification de contenu substantiel, update de frontmatter autre qu'aliases.

### Idempotence & état _(code ET hors-code)_

- **Si même item traité 2× :** safe — lint/stats read-only ; les 2 fixes autorisés sont idempotents (un lien réparé ne matche plus, des aliases complétés ne re-déclenchent plus) ; rapport nommé par date → un 2e run le même jour écrase le rapport du jour (comportement accepté)
- **Si interruption mid-batch :** aucun état intermédiaire critique — relancer le run entier ; l'état inter-runs = le dernier rapport `vault-health-*` (borne temporelle des tool_events + base de comparaison tendance)

---

## 5. Vérification

**Méthode retenue :** triple check structurel (validé Raphael 16 juil. 2026) —

PASS = (a) rapport écrit avec les 4 sections obligatoires (lint / tendance consultation / adoption cross-repo / inbox) **ET** (b) lint post-fixes non dégradé vs pré-fixes (comptes par catégorie ≤ avant) **ET** (c) zéro erreur MCP pendant le run.
Un seul échec → FAIL → fichier d'échec `output/vault-health-FAIL-YYYY-MM-DD.md`.

---

## 6. Infra

**Option retenue :** machine locale (contrainte dure — MCP localhost:8091, vault local)

- **Détails :** Windows 11, invocation manuelle `/vault-health` en session forge ; MCP relançable via mcp-autostart (hook forge + hook SessionStart user installé le 16 juil.)
- **Incompatibilités signalées :** aucune infra installée — la régularité repose sur Raphael. Écart assumé au consensus « maintenance planifiée, pas espérée » (décision 16 juil.) : réévaluer si ≥ 2 lundis consécutifs sont oubliés (re-proposer alors la tâche planifiée Windows).

---

## 7. Garde-fous (obligatoires)

| Garde-fou | Décision |
|-----------|----------|
| Validation humaine | Par batch hebdo : Raphael lit le rapport (note vault seule, pas de push — arbitrage 16 juil.) ; les fixes auto sont bornés à la liste fermée §4 |
| Cap coût / itération | 1 run/semaine, session unique SANS fan-out d'agents, timeout 15 min, ≤ 5 notes modifiées/run |
| Log / trace | Le rapport daté EST le log (`Knowledge/reviews/vault-health-YYYY-MM-DD.md`) ; FAIL → fichier `output/vault-health-FAIL-*.md` |
| Kill-switch | Trivial : ne pas lancer `/vault-health` (aucun déclencheur installé) |

---

## 8. Composants à créer (HORS SCOPE de /loop-forge)

> Créer ces composants depuis la session principale après validation de cette spec.

| Composant | Type | Statut |
|-----------|------|--------|
| `vault-health` | skill (via skill-creator) | **CRÉÉE le 16 juil. 2026** (`.claude/skills/vault-health/SKILL.md`) — routine 5 étapes : lint+fixes liste fermée, usage 7j + tendance, adoption cross-repo (+ verdict J+14 au 1er run ≥ 2026-08-03), inbox, rapport 4 sections + triple check |
| Entrée cron lundi 09:00 | déclencheur auto | **ABANDONNÉE** (décision Raphael 16 juil.) — cron natif CC session-only, tâche Windows déclinée. Invocation manuelle |

Hook kill-switch : NON créé — sans déclencheur installé, il est sans objet.

---

## 9. Critères de done

- [ ] Premier run manuel `/vault-health` complet et validé par Raphael
- [ ] La méthode de vérification est opérationnelle (triple check produit PASS/FAIL réel)
- [ ] Chaque itération produit le livrable attendu (rapport 4 sections daté)
- [ ] Les 4 garde-fous sont opérationnels (validation batch, cap, log, kill-switch)
- [ ] Un premier run complet a été validé par Raphael

---

## Notes / À confirmer

- **Rendez-vous J+14 intégré** : le 1er run ≥ 2026-08-03 rend le verdict de la mesure DA — seuil : ≥ 10 consultations forge-brain (search+read) depuis des sessions hors claude-forge sur 14 j = extension vivante ; en-dessous → proposer retrait du `~/.claude/CLAUDE.md` + note de dette (arbitrage Raphael). **Dépend de la régularité manuelle : penser à lancer `/vault-health` le lundi 2026-08-03.**
- Seuil « inbox qui s'accumule » fixé à > 3 notes — à recalibrer à l'usage.
- Déclencheur manuel = écart assumé au consensus « maintenance planifiée » ; trigger de réouverture : ≥ 2 lundis consécutifs oubliés.
