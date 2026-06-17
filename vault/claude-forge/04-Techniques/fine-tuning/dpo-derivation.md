---
titre: "DPO — Dérivation mathématique (de RLHF à la loss)"
resume: "Dérivation complète de la loss DPO depuis l'objectif RLHF KL-régularisé — Bradley-Terry, reward implicite, annulation de Z(x), loss finale en sigmoïde"
aliases:
  - "dérivation DPO"
  - "DPO derivation"
  - "DPO loss"
  - "Your Language Model is Secretly a Reward Model"
  - "reward implicite DPO"
  - "Bradley-Terry DPO"
type: technique
domaine: ia
derniere-maj: 2026-06-17
auteur: claude
sources:
  - "https://arxiv.org/abs/2305.18290"
  - "https://huggingface.co/blog/garg-aayush/derive-dpo-loss"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/fine-tuning"
  - "#domaine/alignment"
---

## Pourquoi cette note

[[fine-tuning-alignment]] donne le comparatif et le « quand utiliser quoi ». Cette note isole la **dérivation mathématique** de DPO — le cœur du titre *« Your Language Model is Secretly a Reward Model »* ([Rafailov et al., Stanford, arXiv 2305.18290](https://arxiv.org/abs/2305.18290)). L'enjeu : comprendre pourquoi DPO optimise **le même objectif** que PPO/RLHF sans jamais entraîner de reward model ni faire de RL.

## Point de départ — l'objectif RLHF KL-régularisé

RLHF maximise la récompense sous une contrainte de divergence KL à une politique de référence (le modèle SFT) :

$$\max_{\pi} \; \mathbb{E}_{x \sim \mathcal{D},\, y \sim \pi(y|x)} \big[ r(x, y) \big] \; - \; \beta\, D_{\text{KL}}\!\big( \pi(y|x) \,\|\, \pi_{\text{ref}}(y|x) \big)$$

- $\pi$ = politique à optimiser, $\pi_{\text{ref}}$ = politique de référence figée (modèle SFT)
- $r(x,y)$ = fonction de récompense, $\beta$ = coefficient de pénalité KL
- La KL empêche la politique de dériver trop loin du SFT (garde-fou de stabilité)

En RLHF classique : on entraîne un reward model via Bradley-Terry, **puis** on optimise $\pi$ par PPO. Lourd, instable, exige du sampling pendant l'entraînement.

## Le modèle de préférence Bradley-Terry

Bradley-Terry convertit des comparaisons par paires en modèle probabiliste : une réponse de récompense plus haute est exponentiellement plus probable d'être préférée.

$$p^*(y_w \succ y_l \mid x) = \sigma\!\big( r^*(x, y_w) - r^*(x, y_l) \big)$$

où $\sigma(t) = \frac{1}{1+e^{-t}}$ est la sigmoïde, $y_w$ la réponse gagnante (winner), $y_l$ la perdante (loser).

## L'astuce centrale — changement de variable

**Étape 1 — politique optimale en forme close.** L'objectif KL-régularisé admet une solution analytique qui relie récompense et politique :

$$r(x,y) = \beta \log \frac{\pi^*(y|x)}{\pi_{\text{ref}}(y|x)} + \beta \log Z(x)$$

où $Z(x)$ est la fonction de partition (ne dépend que de $x$, intractable car somme sur tous les $y$).

**Étape 2 — reward implicite.** On **inverse** la relation : au lieu d'un reward model qui définit la politique, c'est la politique qui définit un reward implicite. La donnée de préférence se modélise alors directement en fonction de $\pi$.

**Étape 3 — annulation de $Z(x)$.** Bradley-Terry ne dépend que de la **différence** de récompenses $r(x,y_w) - r(x,y_l)$. Comme $\beta \log Z(x)$ est identique pour $y_w$ et $y_l$ (même $x$), il **s'annule** :

$$r(x, y_w) - r(x, y_l) = \beta \log \frac{\pi^*(y_w|x)}{\pi_{\text{ref}}(y_w|x)} - \beta \log \frac{\pi^*(y_l|x)}{\pi_{\text{ref}}(y_l|x)}$$

Le terme intractable disparaît — c'est ce qui rend DPO calculable.

## La loss DPO finale

En substituant la différence de récompenses dans l'objectif Bradley-Terry :

$$\mathcal{L}_{\text{DPO}}(\pi_\theta; \pi_{\text{ref}}) = - \mathbb{E}_{(x, y_w, y_l) \sim \mathcal{D}} \left[ \log \sigma\!\left( \beta \log \frac{\pi_\theta(y_w|x)}{\pi_{\text{ref}}(y_w|x)} - \beta \log \frac{\pi_\theta(y_l|x)}{\pi_{\text{ref}}(y_l|x)} \right) \right]$$

Intuition : la mise à jour augmente la log-probabilité **relative** de la réponse préférée vs la rejetée, avec un poids d'importance dynamique par exemple qui empêche la dégénérescence d'un objectif de ratio naïf.

## Ce que « secretly a reward model » veut dire

Le titre ne signifie **pas** que le modèle sort un scalaire de récompense. Il signifie qu'optimiser $\pi$ avec la loss DPO est **mathématiquement équivalent** à : définir implicitement la fonction de récompense qui rationalise les préférences, puis trouver la politique optimale pour cette récompense — le tout en une seule étape supervisée stable, sans boucle RL.

## Conséquences pratiques

- **2 modèles en mémoire** ($\pi_\theta$ + $\pi_{\text{ref}}$ figé) — d'où l'intérêt de [[fine-tuning-alignment|SimPO/ORPO]] qui suppriment $\pi_{\text{ref}}$.
- Le reward implicite $\beta \log \frac{\pi_\theta}{\pi_{\text{ref}}}$ est la base des variantes : R-DPO ajoute un terme de longueur, TDPO descend au niveau token (cf [[fine-tuning-alignment]] § Variantes).
- La pénalité KL via $\pi_{\text{ref}}$ est **cruciale** pour la stabilité — l'ignorer est un pitfall classique (cf [[fine-tuning-datasets]] § Pitfalls DPO).

## Liens

- [[fine-tuning-alignment]] — comparatif et variantes (foyer canonique)
- [[fine-tuning-datasets]] — construction du dataset de préférence + pitfalls
- [[Rafael Rafailov]] — premier auteur du papier DPO
- [[Nathan Lambert]] — expert RLHF, textbook
- [[MOC-Fine-Tuning]] — MOC racine
