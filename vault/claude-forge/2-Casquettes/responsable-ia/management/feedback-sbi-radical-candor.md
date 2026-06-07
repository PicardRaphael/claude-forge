---
aliases:
  - feedback SBI
  - SBI feedback
  - Radical Candor
  - feedback canonique
  - feedback dur
  - Ruinous Empathy
resume: Modèle SBI (Situation/Behavior/Impact) + extension SBII (Intent) + matrice Radical Candor de Kim Scott. Ruinous Empathy = piège #1 manager débutant.
derniere-maj: 2026-06-07
tags:
  - "#type/technique"
  - "#casquette/responsable-ia"
  - "#domaine/management"
  - "#pratique/feedback"
---
# Feedback — SBI + Radical Candor

## TL;DR

- **SBI** = Situation / Behavior / Impact. Factuel, observable, pas interprétation.
- **SBII** ajoute Intent inquiry — *"Qu'est-ce qui se passait pour toi ?"*
- **Matrice Radical Candor** : Care personally × Challenge directly. Le piège débutant = **Ruinous Empathy** (on aime, on édulcore, ils repartent sans avoir compris).
- **Aucune surprise en review annuelle** (Fournier). Le feedback est continu.

## Modèle SBI (Center for Creative Leadership)

| Composante | Définition | Exemple OK | Exemple KO |
|---|---|---|---|
| **S**ituation | Quand et où précisément | "Hier dans la revue de PR de NeoChat" | "En général, sur les PR" |
| **B**ehavior | Observable, comportement, pas interprétation | "Tu as merge sans attendre la review d'Alice" | "Tu étais impatient" |
| **I**mpact | Effet sur TOI / l'équipe / l'œuvre | "Alice s'est sentie shortée, et on a poussé un bug en staging" | "C'était mauvais" |

Règle d'or : si quelqu'un peut **filmer** le Behavior, c'est observable. Si c'est une interprétation, retravailler.

## SBII — extension Intent

Après les 3 composantes, **poser une question d'intention** :

> *"J'imagine que ce n'était pas ton intention. Qu'est-ce qui se passait pour toi à ce moment-là ?"*

Pourquoi : sépare le comportement de l'identité. L'IC peut reconnaître l'impact sans s'effondrer sur "je suis mauvais".

## Matrice Radical Candor (Kim Scott)

|  | **Care personally** | **Don't care personally** |
|---|---|---|
| **Challenge directly** | **Radical Candor** ✅ | Obnoxious Aggression (le brutal) |
| **Don't challenge** | **Ruinous Empathy** 🚨 piège #1 | Manipulative Insincerity |

**Ruinous Empathy = piège #1 manager débutant** : tu apprécies l'IC, tu édulcores, il/elle repart sans signal. Plus tard tu dois licencier ou tu portes une frustration accumulée. Le geste empathique de court terme = trahison à long terme.

**Test rapide** : *"Si je ne disais rien et que la situation se reproduisait, est-ce que je m'en voudrais ?"* → Si oui, parler.

## Formule canonique feedback

Pour un feedback simple, un seul template :

```
[Situation] J'ai vu / Hier dans X / Quand Y est arrivé...
[Behavior] ... tu as fait / dit / écrit ...
[Impact]   ... ce qui a eu pour effet ...
[Intent]   J'imagine que ce n'était pas ton intention.
           Qu'est-ce qui se passait pour toi ?
[Future]   Pour la prochaine fois, on peut convenir de ... ?
```

## Continuité vs annuel — règle Fournier

> *« No surprises in performance reviews. »*

Si une info débarque en review annuelle, c'est un échec du manager. Le feedback dur doit avoir été donné **dans la semaine** où l'événement s'est produit, pas 6 mois après.

Cadence Neoteem :
- **Feedback positif** : au moins 1 par 1:1 (Pink — autonomie/maîtrise/sens nourris)
- **Feedback correctif** : sous 1 semaine après observation
- **Feedback dur** : sous 48h, en 1:1 dédié

## Protocole feedback dur — 8 étapes

1. **Préparer SBI écrit** en pré-1:1 notepad
2. **Choisir le canal** : 1:1 dédié, jamais en groupe, jamais Slack
3. **Annoncer** : *"J'ai un feedback à te partager, ça va prendre 15-20 min"*
4. **Donner SBII** : Situation → Behavior → Impact → Intent inquiry
5. **Écouter** sa version complète, ne pas couper
6. **Aligner sur l'écart** : *"On est d'accord que l'impact a été X ?"*
7. **Convenir d'un futur observable** : action + date check-in
8. **Documenter** : 2-3 lignes écrites dans le notepad, partagées avec l'IC

## Recevoir du feedback

Pour modéliser le comportement attendu :
- *« Merci, c'est précieux »* (point — pas de "mais")
- Reformuler pour vérifier la compréhension
- Demander un exemple concret si trop abstrait
- 48h plus tard, revenir avec une action

Si tu ne reçois jamais de feedback dur → c'est que tu n'es pas **safe to challenge**. C'est un signal.

## WWWF follow-up (What Went Well / What didn't / Future)

Pour les sujets récurrents, en fin de 1:1 :
- **W**hat **W**ent **W**ell depuis le dernier feedback ?
- **W**hat didn't go well ?
- **F**uture : qu'est-ce qu'on ajuste ?

## 3 scripts feedback adaptés Neoteem

### Script 1 — Feedback positif à un dev qui a livré NeoChat v2

```
Hier en démo NeoChat v2, j'ai vu que tu as documenté l'archi
hexagonale dans le README et ajouté les eval suites Promptfoo.
L'impact : Camille a pu reprendre la review sans te solliciter,
et la PR a mergé en 2h au lieu de 2 jours.
C'est exactement le niveau de soin qu'on veut. Merci.
```

### Script 2 — Feedback correctif sur qualité code IA

```
Sur la PR #847 NeoDocs (mardi), j'ai vu que le prompt système
est dans le code en string brute, sans versioning ni eval.
L'impact : si on doit rollback ou A/B tester, on n'a pas de
référentiel — et l'équipe IA d'à côté ne peut pas réutiliser.
J'imagine que c'était pour aller vite avant la démo ?
Pour les prochains prompts en prod, on peut convenir de passer
par le pattern versioning prompts du repo (cf [[rag-architecture]]) ?
```

### Script 3 — Feedback dur sur attitude réunion

```
En revue produit jeudi, quand Alice a proposé l'approche RAG,
tu as coupé deux fois et dit "ça marchera jamais en prod" sans
contre-proposition.
L'impact : Alice ne s'est plus exprimée du tout pendant le reste
de la réunion, et la décision a été prise sans son input.
J'imagine que ce n'était pas ton intention. Qu'est-ce qui se
passait pour toi ?
[écouter]
Pour la prochaine fois, est-ce qu'on peut convenir que tu
formules tes objections sous forme de question : "Comment tu
gères X en prod ?" plutôt que verdict ?
```

## Anti-patterns

- ❌ **Sandwich** (positif/négatif/positif) — désormais discrédité, dilue le signal et entraîne la méfiance ("quel est le vrai message ?")
- ❌ **Feedback en public** = humiliation, peu importe l'intention
- ❌ **Différer pour "le bon moment"** → le bon moment c'est maintenant. Sinon contexte perdu.
- ❌ **Ne pas documenter** → mémoire trahit. Pas de trace = pas de progression mesurable.
- ❌ **Ruinous Empathy** = piège mortel. Test : *"Est-ce que je m'en voudrais si ça se reproduit ?"*

## Sources

- [CCL — SBI Feedback Model](https://www.ccl.org/articles/leading-effectively-articles/sbi-feedback-model-a-quick-win-to-improve-talent-conversations-development/)
- [Radical Candor — Our Approach](https://www.radicalcandor.com/our-approach)
- [Kim Scott — Radical Candor TEDx](https://www.youtube.com/watch?v=4xfRizq1Yt0)
- [The Manager's Path — Fournier (No surprises rule)](https://getlighthouse.com/blog/camille-fournier-lessons-managers-path/)

## Liens

- [[index]] — hub management
- [[1-on-1-cadre-canonique]] — où le feedback se donne
- [[manager-seniors-plus-experimentes]] — feedback à un sénior
