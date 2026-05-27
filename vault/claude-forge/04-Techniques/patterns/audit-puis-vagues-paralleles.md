---
titre: "Méthode audit + vagues d'application parallèles"
resume: "Pattern d'exécution d'un audit massif (15+ tâches) : Phase audit 5-axes parallèles (clusters indépendants) → Phase application en vagues P0/P1/P2/P3 avec vérification empirique entre chaque vague. Validé sur neo_ia 25 mai 2026 (15 tâches, 100% succès, -660 LOC)."
aliases:
  - "audit puis vagues paralleles"
  - "methode vagues paralleles"
  - "5 axes audit + 4 vagues fix"
  - "audit massif execution"
  - "vague parallele fix audit"
derniere-maj: 2026-05-27
auteur: claude
type: technique
sources:
  - "[[feedback_fix_vagues_paralleles]]"
  - "[[feedback_audit_repo_method]]"
  - "Session neo_ia 25 mai 2026"
tags:
  - "#type/technique"
  - "#type/pattern"
  - "#domaine/claude-code"
  - "#sujet/orchestration"
  - "#pattern/audit"
---
# Méthode audit + vagues d'application parallèles

## QUOI

Pattern pour exécuter un **audit massif → fixes massifs** sur un repo en optimisant pour parallélisme + vérification empirique.

```
┌────────────────────────────────────────┐
│  Phase audit (5 sub-agents //)         │
│  - agents / skills / hooks / rules+CM  │
│  - code applicatif                     │
└────────────────────────────────────────┘
                 ↓
         Vérif empirique session principale
                 ↓
         Plan priorisé P0/P1/P2/P3
                 ↓
         Validation user
                 ↓
┌────────────────────────────────────────┐
│  Vague 1 — P0 critiques (N // tasks)   │
└────────────────────────────────────────┘
                 ↓ vérif empirique
┌────────────────────────────────────────┐
│  Vague 2 — P1 important (M //)         │
└────────────────────────────────────────┘
                 ↓ vérif empirique
┌────────────────────────────────────────┐
│  Vague 3 — P2 polish (K //)            │
└────────────────────────────────────────┘
                 ↓ vérif empirique
┌────────────────────────────────────────┐
│  Vague 4 — P3 capitalisation (J //)    │
└────────────────────────────────────────┘
```

## POURQUOI — résout

- **Audit séquentiel** = 5× plus lent, pollue contexte principal
- **Fix séquentiel** = 15× plus lent sur 15 tâches indépendantes
- **Fix sans vérif** = claims non validés s'accumulent (cf [[feedback_audit_claims_after_brief]])
- **Fix une seule grosse vague** = pas de checkpoint, si échec on perd tout
- **Audit + fix mélangés** = sub-agents ré-analysent à chaque fix, gaspillage tokens

## COMMENT — détail des phases

### Phase 1 — Audit 5 axes parallèles

Découper `.claude/` en clusters mutuellement exclusifs :
1. `agents/` (1 sub-agent project-auditor)
2. `skills/` (1 sub-agent project-auditor)
3. `hooks/` + section hooks de settings.json (1 sub-agent project-auditor)
4. `rules/` + CLAUDE.md + sections non-hooks de settings.json (1 sub-agent project-auditor)
5. Code applicatif (1 sub-agent codebase-scanner)

**Tous en parallèle, 1 message multi-Agent.** Chaque sub-agent retourne rapport markdown ~200L.

### Phase 2 — Vérification empirique session principale

CRITIQUE — feedback [[feedback_audit_claims_after_brief]]. Pour chaque claim majeur des sub-agents :
- `Bash grep -c` pour vérifier comptages
- `ls` pour vérifier existence fichiers
- `Read` pour valider contenu cité

Ne jamais relayer un rapport sans vérification.

### Phase 3 — Plan priorisé P0/P1/P2/P3

| Priorité | Critère | Exemples |
|----------|---------|----------|
| **P0** | Sécu / contradictions internes / anti-doctrine critique | secret en clair, workflow hook, contradictions intra-repo |
| **P1** | Déduplication massive / consolidation / SSOT | doublons agents/rules, single source of truth violée |
| **P2** | Polish / cohérence / metadata | descriptions trop longues, metadata.category manquante |
| **P3** | Capitalisation / nouvelles features | skills code-gen, hooks lint sur boundaries observées |

### Phase 3bis — Pas de symétrie artificielle entre axes

Un audit à N axes n'impose PAS un P0/P1 par axe. Prioriser sur l'impact réel, sans complexe : un audit de 5 axes peut légitimement n'avoir **qu'un seul P0** si un seul axe porte un risque réel et présent. Les autres axes vont en P2/P3 capitalisé — différés, pas oubliés (avec leur déclencheur de réactivation).

**Le piège** : distribuer du P0/P1 sur tous les axes pour l'équilibre visuel. C'est de la symétrie artificielle — elle gonfle le travail sur des trous théoriques et dilue l'effort sur le vrai risque.

**Test de discrimination** avant de classer un axe en P0/P1 :
- Le risque est-il **réel et présent**, ou théorique/anticipé ? (théorique → P2/P3 + déclencheur)
- L'impact d'une régression silencieuse est-il maximal (cœur produit) ou cosmétique ?
- Suis-je en train de classer cet axe haut **parce qu'il le mérite**, ou pour ne pas laisser un axe "vide" ?

**Observé 2 fois** :
- Phase 2 (27 mai) : faux ratio 3:1 de tests adverses corrigé en 5.3:1 et 8:1 réels — ne pas padder avec des cas hors-scope pour atteindre un quota.
- Phase 3 (27 mai) : 5 axes audités, advisor a tranché net sur 1 seul P0 (cœur MCP non testé). Le reste P2/P3 avec déclencheurs — voir [[decision-renforcements-differes-phase-3]].

Corollaire : capitaliser franchement les P2/P3 (note ADR avec déclencheurs) vaut mieux qu'un P1 bâclé pour la symétrie. Cf [[bug-caracterise-fix-trivial-vs-couteux]] (trivial = fix now, coûteux = phase dédiée) appliqué à l'échelle d'un axe.

### Phase 4 — Exécution vague par vague

**RÈGLE** : ne pas démarrer vague N+1 avant vérif empirique vague N.

Pour chaque vague :
1. TaskUpdate `in_progress` sur les tâches concernées
2. Dispatch sub-agents en parallèle (1 par tâche)
3. Attendre fin de tous les sub-agents
4. **Bash vérification** : grep résultats attendus, ls fichiers créés, wc -l mesures
5. Si OK → TaskUpdate `completed` + passer à vague suivante
6. Si échec → relancer sub-agent fautif ou escalader

### Phase 5 — Commit final

Après les 4 vagues, **1 seul commit par repo** avec message structuré (Vagues P0/P1/P2/P3 dans le body). Évite spam commits + facilite revert si besoin.

## QUAND L'UTILISER

| Situation | Méthode ? |
|-----------|-----------|
| Audit `.claude/` repo X avec 10+ fixes prévus | OUI |
| Fix 1-2 problèmes ciblés | NON — séquentiel direct |
| Refonte cross-repo (multi-repos en parallèle) | OUI mais 1 quartet par repo |
| Migration majeure (stack switch) | OUI — vagues = phases migration |

## SUB-PATTERN : dispatcher 1 message, attendre tout, vérifier, suivant

```python
# Session principale orchestration
1. dispatch_parallel([sub1, sub2, sub3, sub4, sub5])  # 1 message multi-Agent
2. wait_all_complete()                                  # bloque jusqu'à fin
3. verify_empirically(bash_commands)                   # grep/ls/wc/cat
4. if all_ok: next_wave()
   else: escalate_or_retry()
```

## RÉSULTATS MESURÉS

### neo_ia 25 mai 2026 (commit `7b86ea5`)
- Audit phase : 5 sub-agents en // (1 échec → relancé avec `general-purpose`)
- Vague 1 (P0) : 6 sub-agents en // — 100% succès
- Vague 2 (P1) : 4 sub-agents en // — 100% succès (1 a corrigé sa propre erreur regex)
- Vague 3 (P2) : 3 sub-agents en // — 100% succès (1 a généré `.proposed` pour bypass classifier)
- Vague 4 (P3) : 2 sub-agents en // (skill-creator + hook-creator) — 100% succès avec tests adverses

**Total : 15 tâches, -660 LOC mesurées, 0 régression détectée.**

## ANTI-PATTERNS

- ❌ **Tout dans une vague** = pas de checkpoint, fragile, contexte pollué
- ❌ **Pas de vérif entre vagues** = claims s'accumulent ([[feedback_audit_claims_after_brief]])
- ❌ **Sub-agents séquentiels** = perte 5× temps ([[feedback_audit_repo_method]])
- ❌ **Commit après chaque vague** = spam (préférer 1 commit final structuré)
- ❌ **Dispatcher sans canoniques lus** = biais perception ([[feedback_lire_canoniques_avant_audit]])

## WIKILINKS

- [[methode-analyser-repo]]
- [[quartet-analyse-multi-repo]]
- [[feedback_audit_repo_method]]
- [[feedback_fix_vagues_paralleles]]
- [[feedback_audit_claims_after_brief]]
- [[feedback_lire_canoniques_avant_audit]]
- [[anti-reentrance-sub-agents-pattern-escalade]]
