---
aliases:
  - "BLUF"
  - "Bottom Line Up Front"
  - "AR 25-50"
  - "executive summary first"
  - "TL;DR exec"
  - "lead with conclusion"
resume: "BLUF (Bottom Line Up Front) — standard US Army AR 25-50 pour communications exec : conclusion en première ligne, justification en second."
derniere-maj: 2026-05-25
tags:
  - "#type/technique"
  - "#domaine/communication"
  - "#casquette/responsable-ia"
---

## TL;DR

- Première ligne = LA décision attendue ou information critique
- Reste = preuves, contexte, options
- Standardisé US Army AR 25-50, adopté par exécutifs depuis 2000s
- Économise 30-60s de lecture exec par message — multiplié par 50 messages/jour

## Mauvais vs Bon

### Mauvais (lead-up classique)

```
Bonjour Claire,

Suite à nos échanges de la semaine dernière, et après avoir consulté
l'équipe data ainsi que le retour de 3 syndics tests, nous avons
exploré plusieurs pistes. La piste 1 présente des avantages mais
aussi des inconvénients [...] (8 lignes plus tard) ... donc je
recommande de geler la feature Aurore pour 2 semaines.
```

### Bon (BLUF)

```
Décision demandée : geler Aurore 2 semaines pour fixer 3 bugs critiques.

Pourquoi : taux d'hallucination 12% sur cohorte alpha vs cible 3%.
Impact : décalage GA juillet → mi-août. Pas d'impact revenus.
Détails et plan de remédiation en pièce jointe.
```

## Cas où NE PAS utiliser

| Contexte | Pourquoi pas BLUF |
|----------|-------------------|
| Annonce de crise / incident | Empathie d'abord, puis décision |
| Mauvaise nouvelle personnelle (départ, restructuration) | Direct = brutal |
| Sujet politique / change management | Préparer le terrain narratif |
| Première interaction avec un partenaire | Trop frontal sans contexte |
| Pitch commercial à froid | Storytelling > BLUF |

## 5 templates inline

### Template 1 — Email court exec

```
Objet : Décision Comex 12/06 — Aurore go/no-go

Claire, décision demandée 12/06 : go production Aurore.

Raisons : ROI 2.9x sur 12 mois, 3 syndics tests valident, 0 incident sécu.
Risque résiduel : taux d'erreur 1.5% (cible interne 1%).
Plan de mitigation : eval set v2 + review humaine post-validation.

PR-FAQ et business case joints.

Raphael
```

### Template 2 — Slack annonce équipe

```
[ANNONCE] Aurore passe en GA le 1er juillet.

Détails : taux d'erreur stabilisé 1.5%, 40 syndics en alpha satisfaits.
Action équipe : freeze code Aurore à partir du 24/06.
Questions : thread ci-dessous, je réponds avant 17h.
```

### Template 3 — Message décision urgente

```
URGENT — coupure GEMINI prévue 14h-16h aujourd'hui par Google.

Impact : Aurore et NeoChat indisponibles pendant 2h.
Action : email 800 syndics + bandeau Loji + report démos commerciales.
Owner : moi pour com, @design pour bandeau.
Update : dans ce thread toutes les 30 min.
```

### Template 4 — Status update hebdo

```
Statut Aurore — semaine 21

État : ON TRACK pour GA 01/07.
Métriques : 1.7% erreur (cible 1.5%), 92% adoption alpha, 0 incident.
Blocages : aucun.
Décisions attendues Comex : aucune cette semaine.
```

### Template 5 — Escalade

```
ESCALADE — feature Aurore : décision arbitrage Comex requise sous 48h.

Conflit : sales pousse GA 15/06, tech recommande 01/07.
Enjeu : crédibilité commerciale (3 contrats en attente) vs qualité (12% erreur).
Ma recommandation : 01/07 avec annonce sales aux 3 prospects que la
version disponible mi-juin est en alpha contrôlé.
Décision attendue : 27/05 16h.
```

## Règle de la première ligne

Test simple : si le destinataire ne lit QUE la première ligne, sait-il quoi faire ?

| Première ligne | Test |
|---------------|------|
| "Suite à notre échange..." | NON — 0 info |
| "Décision demandée 12/06 : go Aurore" | OUI |
| "Aurore est prête, je voulais te dire que..." | Faible |
| "Aurore GA 01/07, validation Comex requise" | OUI |

## Anti-patterns

- BLUF + politesse en ouverture séparée → diluer la première ligne
- BLUF sur sujet émotionnel → froideur perçue
- BLUF sans backup détaillé → exec demande "et la suite ?"
- 3 BLUF dans un email = pas un BLUF, c'est une liste à hiérarchiser
- Confondre BLUF (conclusion) et TLDR (résumé)

## Sources

- US Army AR 25-50 — *Preparing and Managing Correspondence* https://armypubs.army.mil/epubs/DR_pubs/DR_a/pdf/web/ARN13808_AR25-50_Web_FINAL.pdf
- Kabir Sehgal — *How to write email with military precision* (HBR) https://hbr.org/2016/11/how-to-write-email-with-military-precision
- Animalz blog — *BLUF for technical writers* https://www.animalz.co/blog/bottom-line-up-front/

## Liens

- [[index]]
- [[../index]]
- [[scqa-pyramid-principle-minto]]
- [[../reunions/codir-6-pager-bezos]]
