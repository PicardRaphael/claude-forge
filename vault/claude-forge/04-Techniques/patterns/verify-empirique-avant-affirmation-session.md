---
titre: "Vérification empirique avant affirmation — claims session et sub-agents"
resume: "Tout claim 'X créé/modifié/fixé/fait' — de la session ou d'un sub-agent — doit être vérifié empiriquement (ls/grep/diff) AVANT d'être relayé à l'utilisateur."
aliases:
  - verify-empirique-avant-affirmation
  - claim-verification-session
  - sub-agent-claim-sans-empirie
  - audit-claims-after-brief
  - vérification-claim-post-edit
  - verify empirique session
derniere-maj: "2026-07-07"
tags:
  - patterns
  - agents
  - qualite
  - verification
type: pattern
---

## Principe

Tout claim « X créé / modifié / fixé / fait » doit être vérifié empiriquement **AVANT** d'être relayé comme acquis à l'utilisateur. Ce principe vaut pour :

1. **Les briefs de fin de tâche de la session principale** — une annonce vient de l'intention, pas de l'état réel post-edit.
2. **Les retours de sub-agents éditeurs** (skill-creator, claudemd-optimizer, hook-creator, architect…) — le sub-agent génère son résumé depuis son plan, pas depuis l'état réel ; l'écriture peut échouer silencieusement (surtout en contournant `delegate-guard` via Bash) sans que le sub-agent le sache.

> Coût d'un check empirique : **1 tool call**. Coût d'un claim faux : **confiance + correction publique**.

## Comment appliquer

| Claim reçu | Vérification requise |
|---|---|
| « X créé » | `ls X` ou `Glob X` AVANT de relayer |
| « Y modifié » | `grep <pattern attendu> Y` pour confirmer |
| « fix appliqué » | re-grep le motif fixé pour vérifier qu'il a disparu |
| Calcul numérique (path résolu, nb lignes, version) | recalculer indépendamment avant d'agir |
| « Skill chargée dans la liste » | tester avec un appel concret (≠ fonctionnelle) |

**Cas particulier — fichiers protégés par `delegate-guard`** (CLAUDE.md, agents/\*, SKILL.md) : les sub-agents contournent via Bash ; l'écriture peut foirer silencieusement → toujours `wc -l` + `head -20`.

**Si discordance claim vs réel** → relancer le sub-agent en lui montrant le delta. Ne jamais relayer le claim brut.

## Incidents ayant fondé ce pattern

- **2026-05-20** : annoncé `certs/README.md` créé → DA vérifie `ls certs/` → inexistant. Même session : sub-agent x-read écrit `claude-forge/secrets/` au lieu de `claude-forge/.claude/secrets/` (calcul de path faux).
- **2026-05-24** : claudemd-optimizer annonce « 7 patches appliqués » alors que 3 patterns sur 7 étaient encore présents (L55, L87, L99). Détecté uniquement parce que hook-creator suivant a grep et remonté l'écart.
- **2026-05-27** : skill-creator annonce 296L puis 309L pour un SKILL.md qui en fait 211 puis 219. Vérif PowerShell systématique a corrigé.

## Wikilinks

- [[post-dispatch-verify]] — rule `.claude/rules/` avec checklist par type d'agent (ls, wc, git diff)
- [[verify-exhaustive-claims]] — variante pour les déclarations exhaustives (« zéro / tous / aucun / complet »)
- [[erreur-subagent-bypass-delegate-guard]] — précédent vault sur l'écriture silencieuse contournant le guard
- [[pattern-behavioral-dispatch-test]] — vérification comportementale PASS/FAIL post-setup
- [[anti-reentrance-sub-agents-pattern-escalade]] — pattern escalade + resume pour ne pas re-briefer à vide
