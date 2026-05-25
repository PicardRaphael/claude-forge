---
aliases:
  - post-mortem
  - postmortem
  - blameless post-mortem
  - retex-incident
  - RCA incident
  - 5 whys
resume: Post-mortem incident format Google SRE blameless — RCA via 5 Whys et Ishikawa. Spécificités IA (hallucination, drift, prompt injection). Template complet.
derniere-maj: 2026-05-25
tags:
  - "#type/methode"
  - "#casquette/responsable-ia"
  - "#domaine/sre"
  - "#rituel/post-mortem"
---

# Post-mortem incidents — blameless culture

## TL;DR
- **Blameless absolu** — focus sur conditions systémiques, jamais "qui"
- **5 Whys** pour atteindre cause systémique (pas humaine)
- **Action items SMART** avec owner + deadline
- **Spécifique IA Neoteem** : hallucination, drift modèle, prompt injection = post-mortem obligatoire

## Doctrine Google SRE

Un post-mortem est **blameless** : focus sur *quelles conditions systémiques* ont permis l'incident, jamais *qui* l'a causé. Origine : aviation et santé, domaines où le blâme tue l'apprentissage.

> Si la cause racine identifiée est "John a fait X", alors le système est cassé. Ce n'est jamais une seule personne.

## Template canonique

```markdown
# Incident Postmortem: [Title]

## Summary
- Date / Heure début / Heure fin / Durée
- Sévérité : SEV1 / SEV2 / SEV3
- Services impactés
- Impact business (users affectés, revenu perdu, SLA breaché)

## Timeline (UTC)
| Time | Event |
|------|-------|
| 14:32 | Alerte déclenchée |
| 14:35 | Astreinte engagée |
| ...  | ... |

## Root Cause
Cause technique précise (config, code path, ressource, modèle, prompt, data).

## Detection
- Comment l'incident a été détecté
- Latence de détection
- Alertes étaient-elles suffisantes ?

## Response
- Diagnostic process
- Mitigation immédiate
- Résolution

## Action Items
| Item | Owner | Deadline | Priority |
|------|-------|----------|----------|
| ...  | ...   | ...      | P0/P1/P2 |

## Lessons Learned
- Ce qui a bien marché
- Ce qui a moins bien marché
- Ce qui a été chance
```

**Blameless notice obligatoire** en tête, lue à voix haute en début de réunion review :
> "Cet exercice cherche à comprendre les conditions systémiques qui ont permis l'incident. Aucune personne n'est en cause. L'objectif est d'apprendre pour ne pas répéter."

## Techniques RCA (Root Cause Analysis)

### 5 Whys
Itérer "pourquoi" jusqu'à atteindre une cause systémique (pas humaine).

### Ishikawa (fishbone diagram)
Catégoriser les facteurs contribuants en branches. Branches typiques IA : **Model** / **Prompt Design** / **RAG Pipeline** / **Monitoring** / **Human Review** / **Data Quality**.

### Timeline correlation
Superposer métriques, logs, actions humaines pour identifier le tipping point.

### Fault tree analysis
Décomposer en arbres de défaillance (probabilité combinée).

## Exemple : 5 Whys hallucination LLM (Neoteem)

1. **Pourquoi** le user a reçu une info fausse ? → LLM a halluciné.
2. **Pourquoi** ? → Prompt manquait de grounding context.
3. **Pourquoi** ? → Le retrieval RAG n'a pas trouvé le doc pertinent.
4. **Pourquoi** ? → L'index embedding était stale (7 jours).
5. **Pourquoi** ? → Aucun pipeline de refresh automatique.

→ **Action item** : pipeline refresh quotidien + monitoring fraîcheur index.

## Cas spécifiques Neoteem

| Incident | Déclenche post-mortem ? |
|----------|------------------------|
| **Hallucination grave** (info client fausse) | OUI obligatoire |
| **Drift modèle** (perf dégradée silencieuse) | OUI + revue monitoring |
| **Prompt injection** (fuite contexte) | OUI sécu + audit prompts |
| **Outage RAG / API** > 15 min | OUI |
| **Bug front mineur** | NON, ticket suffit |

## Réunion review post-mortem (30 min)

| Temps | Activité |
|---|---|
| 0-3 min | Blameless notice lue à voix haute |
| 3-10 min | Timeline présentée par l'auteur |
| 10-20 min | RCA (5 Whys collectif) |
| 20-27 min | Action items, owners, dates |
| 27-30 min | Tracking, follow-up scheduled |

## Tracking & follow-up

- **Stocker dans Confluence** : espace dédié `Incidents/YYYY-MM/`
- **Lier ticket Jira** par action item, owner, deadline
- **Revue mensuelle** : taux complétion action items précédents
- **Pattern detection** : tag les root causes pour détecter récurrences

## Métriques globales à tracker

- **MTTD** (Mean Time To Detect) : temps moyen détection
- **MTTR** (Mean Time To Resolve) : temps moyen résolution
- **Recurrence rate** : % incidents avec root cause similaire
- **Action items completion rate** : % AIs faits dans deadline

## Liens

- [[reunions/index]]
- [[../gouvernance/securite-llm-owasp]] (à venir, prompt injection)
- [[../strategie/mlops-monitoring-modeles]] (à venir, drift detection)

## Sources

- [Google SRE – Postmortem Culture](https://sre.google/sre-book/postmortem-culture/)
- [Google SRE – Example Postmortem](https://sre.google/sre-book/example-postmortem/)
- [incident.io – SRE Postmortem Best Practices](https://incident.io/blog/sre-incident-postmortem-best-practices)
