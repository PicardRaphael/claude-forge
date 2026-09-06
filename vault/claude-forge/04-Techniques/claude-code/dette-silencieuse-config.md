---
titre: "Dette silencieuse de configuration — détecter ce qui existe sans servir"
resume: "Un composant présent mais jamais exécuté ni chargé ne produit aucune erreur ; la détecter demande de comparer des faits sémantiques, pas du texte, et d'adopter la dette existante par ratchet."
aliases:
  - "dette silencieuse"
  - "composant inerte"
  - "test qui ne tourne jamais"
  - "drift entre jumeaux"
  - "detecter config morte"
  - "garde-fou qui crie sur du bruit"
type: technique
auteur: claude
derniere-maj: 2026-09-06
sources: []
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#sujet/qualite"
---
# Dette silencieuse de configuration

Une classe de défaut qui ne produit **aucun signal** : le composant existe sur le
disque, il a l'air correct à la lecture, et il ne sert à rien. Pas d'erreur, pas
de warning — juste du silence, qui se lit comme « tout va bien ».

## Les trois formes observées

Mesurées sur claude-forge en 24 h (5-6 sept. 2026), toutes trois invisibles
jusqu'à ce qu'on les cherche exprès.

| Forme | Instance | Ce qui aurait dû alerter |
|---|---|---|
| **Fichier hors du chemin d'exécution** | deux `test_*.py` à la racine de `.claude/hooks/`, hors du `pytest .claude/hooks/tests` documenté | rien — ils n'ont jamais tourné |
| **Composant que le runtime refuse de charger** | `.codex/agents/repo-inspector.md`, `description: Modes: mode=audit` → ScannerError YAML | rien — l'agent était simplement absent |
| **Correction appliquée d'un seul côté** | libellé du `security-guard` corrigé côté Claude, pas côté Codex ; trois fois en 24 h | rien — les deux surfaces sont légitimement différentes |

Le cas des tests est le plus coûteux : **un test qui ne tourne pas est pire que
pas de test**, il fabrique de la confiance. L'un des deux affirmait que
`git branch -d` était légitime, l'exact inverse du comportement livré. La
contradiction a survécu des mois sans que rien ne la relève.

## Comparer des faits, jamais du texte

C'est le point de conception qui décide si l'outil sera utilisé ou ignoré.

Sur des surfaces **adaptatrices** — la même intention portée par deux plateformes
— la divergence est normale et voulue. Un diff brut y est inexploitable :
`security-guard.py` affichait 24 lignes d'écart entre Claude et Codex alors que
ses trois libellés étaient identiques, l'écart n'étant que du formatage (regex
sur une ligne d'un côté, éclatée de l'autre).

La comparaison doit donc porter sur des **faits sémantiques** :

- **fichiers de code** → les messages (littéraux de longueur moyenne). Exclure
  les regex : le formatage les découpe en morceaux et fabrique des écarts
  fantômes ; un vrai écart de regex se voit dans les suites de tests.
- **fichiers markdown** → les champs de frontmatter à sémantique partagée
  (`model`, `effort`…), et **seulement quand les deux côtés les déclarent**. Un
  champ présent d'un seul côté est une adaptation, pas une dérive.
- **cas dégénéré à reconnaître** : un jumeau qui `exec()` le fichier de l'autre
  n'a qu'une source — aucune dérive n'y est possible, et le comparer produit un
  écart permanent.

## Un garde qui crie sur du bruit se fait ignorer

Le mode de défaillance d'un garde-fou n'est pas le faux négatif, c'est le faux
positif : on apprend à passer outre, et il ne protège plus rien.

Deux mesures de calibrage sur le même outil : un premier critère signalait
34 divergences dont 32 fausses (des sous-projets Python autonomes, chacun
porteur de son `pyproject.toml` et donc de sa propre collecte) ; le critère
corrigé en signale 2, toutes deux réelles. Un garde-fou **étroit et vrai** vaut
mieux qu'un garde large et bruyant — c'est aussi ce qui justifie qu'un outil
documente sa portée volontairement limitée plutôt que de prétendre tout couvrir.

Corollaire : la frontière se décide sur un **critère structurel vérifiable** (ici
« ce dossier porte-t-il son propre marqueur de projet ? »), jamais sur une liste
d'exceptions tenue à la main, qui dérive.

## Adopter l'existant par ratchet

Sur une base qui porte déjà de la dette, un garde binaire est ingérable : rouge
dès le premier run, donc désarmé. Le ratchet — *tightens, never loosens*, cf
[[addy-osmani]] — fige l'état mesuré dans une baseline versionnée et ne signale
que les divergences **nouvelles**.

Deux conditions pour que ce ne soit pas un tapis sous lequel balayer :

1. chaque entrée figée est **lue** avant d'être acceptée, jamais baselinée en
   masse pour obtenir du vert ;
2. accepter une divergence est un **geste explicite** (un flag dédié), jamais un
   silence par défaut.

La baseline porte alors sa propre mise en garde, et le geste d'acceptation est
visible dans le diff.

## Le garde-fou est lui-même un composant

Une vérification qui n'apparaît dans aucune commande ne s'exécute jamais — elle
appartient à sa propre catégorie de défaut. Cas observé : un validateur de
frontmatter existait, sa docstring citait littéralement le bug qui venait de
frapper, et il n'était appelé nulle part **ni ne couvrait la surface concernée**.

D'où deux règles qui se tiennent :

- la liste des commandes de vérification est la **déclaration de ce qui est
  vivant**, pas un pense-bête ; un outil s'y ajoute au moment où il est écrit ;
- un garde-fou mérite ses propres tests, sinon il peut se désarmer en silence —
  exactement le défaut qu'il traque.

## Liens

- [[addy-osmani]] — Ratchet Principle, *tightens never loosens*
- [[Claude-Forge]] — chaîne de vérification locale du framework
- [[methode-analyser-repo]] — analyser le réel avant de prescrire
- [[comment-creer-hook]] — la frontière entre garde déterministe et jugement
