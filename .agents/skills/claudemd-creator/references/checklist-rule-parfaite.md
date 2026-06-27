# Checklist rule parfaite — 4 dimensions

Source : doctrine forge + dérives réelles observées (session 2026-06-06). Une rule `.claude/rules/*.md` est le composant le PLUS SIMPLE : frontmatter minimal + markdown libre. Pas de skill créatrice dédiée (sur-ingénierie) — cette checklist EST le standard. La consulter avant d'écrire/auditer une rule.

---

## 0. Décision — Est-ce vraiment une rule ? (OBLIGATOIRE)

Une rule = comportement/convention **toujours actif**, chargé automatiquement, qui oriente sans forcer (probabiliste, ~80%).

- [ ] C'est un comportement toujours-vrai à rappeler, PAS un workflow invocable → sinon **skill**
- [ ] Ce n'est PAS un comportement à garantir à 100% → sinon **hook** (déterministe)
- [ ] Ce n'est PAS du contexte projet stable type stack/commandes → sinon **CLAUDE.md**
- [ ] Le sujet n'est pas déjà couvert par une autre rule → sinon **enrichir l'existante**, ne pas créer un doublon

## 1. Frontmatter (liste FERMÉE)

Seuls ces champs existent dans une rule. **Tout autre = ERREUR.**

| Champ | Obligatoire ? | Valeurs |
|-------|---------------|---------|
| `description` | **OUI** | une ligne, ce que fait la rule + quand. SANS elle, la rule ne se charge pas (dérive observée : read-section-preference) |
| `globs` | optionnel | `"*"` (toujours active) ou pattern quoté — guillemets OBLIGATOIRES |
| `paths` | optionnel | pattern quoté si rule conditionnelle à un chemin |

**Champs INTERDITS** (n'existent PAS pour une rule) : `name`, `model`, `effort`, `tools`, `allowed-tools`, `version`, `color`, `memory`, `permissionMode`, `user-invocable`. Si un audit signale l'un d'eux comme « manquant » → l'audit se trompe.

- [ ] `description:` présent (sinon rule non chargée — dérive critique)
- [ ] `description` = UNE ligne, jamais `>-` ni `|`
- [ ] `globs`/`paths` quotés si présents (`"*"`, pas `*` nu)
- [ ] Aucun champ interdit

## 2. Contenu (une règle = une vérité)

- [ ] La rule décrit le comportement RÉEL, pas un comportement périmé (dérive observée : delegate-to-specialists décrivait l'ancien hook → mentait à Claude)
- [ ] Une rule = un seul sujet, au bon mécanisme (pas de workflow déguisé, pas de garantie déguisée)
- [ ] Pas de duplication : si le détail vit dans une canonique vault ou une autre rule → **pointer**, ne pas recopier (dérive : check-before-create pointe vers sequence-canonique)
- [ ] Règles testables + raison (« parce que ») quand c'est un comportement, pas une aspiration vague
- [ ] Tables pour les mappings (dispatch, quand-consulter, repos)
- [ ] Critique en haut (< ligne 25), jamais enfouie en bas

## 3. Cohérence inter-composants

- [ ] Aucune contradiction avec une autre rule, avec CLAUDE.md, ou avec un hook
- [ ] Si la rule décrit le comportement d'un hook → elle dit la VÉRITÉ sur ce hook (vérifier le code du hook, pas supposer — dérive : delegate-to-specialists vs delegate-guard réel)
- [ ] Si la rule est référencée par un script (ex : config-guardian baseline) → le script et la rule sont alignés (dérive : scan.py référençait des rules mortes)
- [ ] Pas de rule « morte » référencée ailleurs sans exister sur disque

## 4. Maintenance

- [ ] La rule a une raison d'exister vérifiable (sinon → supprimer)
- [ ] Datée si elle encode une décision/pivot (la date + la raison musclent la règle)
- [ ] Relue quand le composant qu'elle décrit change (un hook modifié → relire la rule qui le décrit)

---

## Signaux de maladie (audit rapide)

| Signal | Correctif |
|--------|-----------|
| Pas de `description:` | Ajouter — sinon non chargée |
| Décrit un comportement périmé | Réécrire sur le réel (lire le code/hook concerné) |
| Duplique une canonique/autre rule | Pointer au lieu de recopier |
| Champ frontmatter interdit (name, model, version...) | Supprimer — n'existe pas pour une rule |
| Contredit une autre rule / CLAUDE.md | Consolider, une seule source |
| Référencée par un script mais le script attend autre chose | Aligner script ↔ rule |
| Workflow multi-étapes déguisé en rule | → skill |
| Comportement « à garantir » en texte | → hook |
| `globs`/`paths` non quotés | Quoter (`"*"`) |
