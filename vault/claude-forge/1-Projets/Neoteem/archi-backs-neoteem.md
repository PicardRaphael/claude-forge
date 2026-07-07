---
titre: "Archi backs Neoteem — qui parle à qui (neo_ia / ia_back / front / webservices Jérôme)"
resume: "Contrats d'exposition front des backs Neoteem : neo_ia exposé front IA uniquement, ia_back jamais exposé front, métier hors scope des deux"
aliases:
  - "archi backs neoteem"
  - "exposition front neoteem"
  - "qui parle a qui neoteem"
  - "contrat backs neoteem"
  - "perimetre neo_ia ia_back"
type: technique
derniere-maj: 2026-05-28
auteur: claude
tags:
  - "#type/technique"
  - "#projet/neoteem"
  - "#domaine/architecture"
---

## Règle d'exposition front

| Back | Exposé au front ? | Scope autorisé |
|------|-------------------|----------------|
| **neo_ia** | Oui | **Uniquement endpoints IA** (génération via agents : comparatif devis, NeoChat, NeoDoc, NeoMail). Pas de métier non-IA. |
| **ia_back** | **Non, jamais** | Parle uniquement à neo_ia (orchestrateur IA interne). Pas exposé front. Pas de métier non-IA. |
| **Webservices Jérôme** | Oui | Toutes les actions métier (mail Correspondance, AG, Drive, persistance). Voir [[webservices-jerome]]. |
| **bdd** | Non | Repo PG/PL-pgSQL, accédé via les backs ci-dessus. |

## Conséquences pour la conception de features

Toute feature impliquant le front doit explicitement décider :

1. **Quelle partie est IA** → endpoint neo_ia exposé au front.
2. **Quelle partie est orchestration IA interne** → ia_back appelé par neo_ia, jamais par le front.
3. **Quelles actions sont métier** (mail, AG, Drive, persistance fichiers) → webservices Jérôme, jamais neo_ia ni ia_back.
4. **Quelle persistance** → BDD JSON (par neo_ia si à la génération) ou Drive client (via webservice Jérôme). Voir [[stockage-fichiers-neoteem]].

## Anti-patterns observés

- ❌ Mettre des actions métier (envoi mail, classement Drive, rattachement AG) dans neo_ia → pollue le scope IA.
- ❌ Exposer ia_back au front → casse le contrat d'orchestrateur IA interne.
- ❌ Réimplémenter Correspondance / AG / Drive ailleurs alors que Jérôme expose des webservices → duplication, dérive.
- ❌ Proposer un livrable cross-stack sans clarifier l'archi en V1 → coût ×4 en itérations (cf [[feedback_archi_clarifier_avant_livrable_cross_stack]]).

## Protocole avant livrable cross-stack

Dès qu'un livrable implique ≥ 2 composants backend Neoteem (neo_ia, ia_back, front, webservices Jérôme, bdd) : **première action = clarifier l'archi**, pas commencer la rédaction.

Question obligatoire en V1 : *« Quel back parle au front pour cette feature ? Qui orchestre quoi ? Quelles actions sont métier vs IA ? »*

S'applique à tout livrable cross-stack : commentaire Jira, `/spec`, BRIEF sub-agent, doc archi, proposition technique. Sans cette clarification → pas de V1. Coût d'un oubli : ×3–4 itérations de correction (cf session 28 mai 2026 : V7→V9→V10 avant archi correcte).
## Origine

Confirmé par Raphael session 28 mai 2026 lors de la rédaction du commentaire ticket comparatif devis (8 itérations V1→V14 pour caler l'archi avant que les sections du commentaire soient justes).

## Liens

- [[neo_ia]] — Monorepo IA (NeoChat/NeoDoc/NeoMail)
- [[ia_back]] — Backend IA FastAPI (orchestrateur interne)
- [[webservices-jerome]] — Webservices métier réutilisables (Correspondance / AG / Drive)
- [[stockage-fichiers-neoteem]] — Pas de S3, persistance BDD JSON ou Drive client
- [[agent-manager-neoteem]] — Gouvernance Claude Code Neoteem
