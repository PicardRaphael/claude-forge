---
aliases:
  - idees-agents-ia-tickets-support
  - nouvelles-idees-agents-neoteem
  - agents-ia-issus-lexique-clients
  - pain-points-clients-loji-agents
resume: Nouvelles idées d'agents IA Neoteem dérivées du lexique de 250 tickets support réels (déc 2025-avr 2026). Pain points clients = opportunités produit, fondées sur données réelles.
derniere-maj: 2026-05-29
tags:
  - "#type/knowledge"
  - "#projet/neoteem"
  - "#casquette/responsable-ia"
  - "#domaine/strategie"
---

# Idées d'agents IA issues des tickets support réels

> Dérivées du [[lexique-expressions-clients]] (250 tickets SC clôturés déc 2025–avr 2026, vault neoteem-brain). Ces idées ne sont PAS inventées : chaque pain point est documenté par des tickets réels (n° SC cités). Complète [[comprendre-neoteem-vue-responsable-ia]] et [[veille-concurrents-ia-syndic]].

## Constat clé du lexique

250 tickets analysés → l'essentiel des demandes support = **diagnostics répétitifs** où la cause est connue et documentée. Beaucoup tournent autour de : cache à vider, dates de facturation erronées, statut ADF « à calculer », exercice non ouvert, paramétrage nature de charges, cumuls/déséquilibres comptables. **Une grande partie est auto-diagnosticable** si on croise le ticket avec le lexique + l'état réel de la base Loji.

## Nouvelles idées d'agents (fondées sur tickets réels)

### Interne (support / qualité)

| Idée | Pain point réel (tickets) | Valeur |
|---|---|---|
| **Agent auto-diagnostic support N1** | Le lexique mappe déjà 250 tickets → diagnostics. Un agent qui lit le ticket entrant + interroge l'état Loji (date facturation, statut ADF, exercice ouvert ?) et propose le diagnostic + la solution. | Désengorge massivement le N1 sur les cas répétitifs (révision loyer, e-paiement, cache, régul). Le support garde les vrais cas complexes. |
| **Agent qualification/triage ticket** | proc-charte-qualification-n2 : règles BLOQUANT/BUG/Intervention BDD à appliquer manuellement. | Pré-qualifie et priorise automatiquement selon la charte. Affecte au bon sprint Jira. |
| **Agent "vérif pré-régularisation"** | Tickets récurrents SC-99352, SC-99375 : régul bloquée par exercice N+2 sans budget, compte 671 non soldé. | Avant que le gestionnaire lance la régul, l'agent vérifie les causes connues de déséquilibre → évite le ticket. |
| **Agent détecteur de cache/MAJ** | Énormément de tickets = simple cache à vider (SC-99208, SC-99247, SC-97598). | Un assistant qui reconnaît les symptômes (« roue de la mort », 404 post-MAJ) et guide le client avant d'ouvrir un ticket. |

### Client (produits)

| Idée | Pain point réel | Valeur |
|---|---|---|
| **Agent "pré-vol comptable" (régul/clôture)** | Déséquilibres récurrents à la validation (erreur 224, compte 471, cumuls doublons). | Détecte les anomalies AVANT la clôture/régul = évite le blocage de convocation AG. Branché sur la compta Loji = inimitable. |
| **Agent "préparation révision loyers"** | SC-99070, SC-99193, SC-93277 : dates de facturation N au lieu de N-1, code INSEE manquant, DPE absent → révision échoue. | Vérifie les prérequis de révision sur tout le portefeuille en 1 clic, signale les contrats à corriger. |
| **Agent "assistant sinistre" (déjà noté)** | Cauchemar admin confirmé marché + API MRI existante. | Voir [[veille-concurrents-ia-syndic]]. |
| **Copilote contextuel dans la fiche** (déjà noté) | « je ne trouve pas le chemin pour… » = catégorie entière de tickets. | Un assistant in-context qui guide DANS Loji (« où extraire les honoraires ? »). |

## Principe directeur (qui distingue ces idées)

Ces agents exploitent **les données Loji vivantes** (état d'un exercice, statut ADF, dates de contrat) — c'est le moat. Un concurrent générique ne peut pas diagnostiquer « votre exercice N+2 a des honoraires sans budget » : il faut être branché sur la base. **Le lexique support EST déjà la base de connaissance d'un agent de diagnostic** — il suffit de le câbler.

⚠️ Toutes ces idées sont des **pistes de cadrage**, pas des engagements. À confronter aux clients (Club Utilisateurs) et à prioriser. Ne pas doubler une fonction Loji existante (leçon NeoChat).
