---
titre: Context Actuel
resume: Working memory dynamique — mis à jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, memoire de travail, etat actuel]
type: context
status: active
derniere-maj: 2026-05-27
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---

## Phase actuelle
SELF_PORTRAIT régénéré (630L) — reflète l'état post Mémoire Portable + DA compounding rétroactif + Audit transverse + Investigation veille. Métriques unifiées sur source unique (`vault_stats`) : 302 commits, 244 tests (101 hooks + 143 MCP), 22 outils MCP, 430 notes vault, 193 feedbacks memory. Nouvelle section 8bis "Système de veille" avec 3 chantiers (A pont veille→doctrine P-haute, B checklist vendredi P-basse, C sync leaders P-moyenne). Hermes déplacé en annexe B condensée. **Pas de commit lancé** (Raphael décide du découpage). Suivant = **Chantier A — pont veille→doctrine** (proposition Jarvis).

## Dernière session (2026-05-27)
### Décisions prises
- **Régénération SELF_PORTRAIT en update chirurgical** (pas rewrite) : ancien portrait du même jour structurellement sain, brief = "reprendre structure, actualiser contenu". Delta par section présenté à l'étape D, validé.
- **Unification des métriques** : l'ancien portrait affichait 3 valeurs de notes divergentes (412/412/417) — symptôme de patches multiples. Source unique retenue = `vault_stats` du jour = 430.
- **Section Hermes → annexe B condensée** (choix Raphael) : le corps décrit forge en lui-même, pas son positionnement vs concurrent. Verdict actuel (A1+A3 livrés, A1×A3 tué) + pointeur [[phase-4-comparaison-hermes-roadmap]].
- **Section 8bis veille créée** : cc-news (Tier 0 + 11 agents / 6 spécialités) + 80 fiches leaders + 2 gaps majeurs (Chantier A pont veille→doctrine, Chantier C sync leaders) + Chantier B checklist vendredi manuel.
- **Dette double-source mémoire tracée** (section 12) : auto-memory native tronquée coexiste avec @import, pas la single source visée, désactivation différée (clé settings global, hard-block classifier).
- **Annexe A "non vérifié"** : README périmé (412 notes/21 outils, hors scope), line refs agents non revérifiées, double-source mémoire, tests = compte de collecte pas relance verte intégrale.

### En cours
Rien. SELF_PORTRAIT + context-actuel prêts. CHANGELOG vault à ajouter si Raphael valide.

### Prochaines étapes
- Commits du SELF_PORTRAIT (1 fichier racine + context-actuel + CHANGELOG/log éventuels). Raphael décide du découpage.
- **Chantier A — pont veille→doctrine** (proposition Jarvis suivante) : détection contradiction doctrinale à cc-news + gate humaine, équivalent /done-propose appliqué à la veille.
- Chantier C — sync 2 listes leaders (vault source unique → dériver les queries domain-*.md).
- TODO P0 : rotation password PostgreSQL prod (secret redacté mais pas tourné).
- Valider empiriquement le pivot `/recall-uncaptured` si l'intuition se présente.

## Fils ouverts
- **Double-source mémoire transitoire** : auto-memory native encore injectée en parallèle de l'@import. Dette tracée, désactivation différée. Cf [[import-ajoute-pas-remplace-automemory]].
- **A1×A3 tué** : ne pas réouvrir le scan rétroactif systématique sans nouvelle donnée infirmant le 0/12. Cf [[idee-compounding-retroactif]] (TUÉE).
- **README périmé** : 21 outils / 412 notes — à corriger en session dédiée (hors scope SELF_PORTRAIT).
- Détection contradictions vault (extension lint_vault, gap léger Hermes) — non priorisé.

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
[[resolution-path-3-contextes]]
[[critique-2026-05-27-compounding-retroactif]]
[[phase-4-comparaison-hermes-roadmap]]
