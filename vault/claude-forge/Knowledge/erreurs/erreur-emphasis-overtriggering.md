---
titre: "Emphasis excessive dans un CLAUDE.md = sur-déclenchement (bruit)"
resume: "Anti-pattern CLAUDE.md : une ou deux emphases (gras, majuscules) attirent l'attention sur ce qui compte ; vingt emphases noient le signal et poussent à un comportement sur-prudent généralisé. L'emphase est un budget d'attention rare, pas un style par défaut. La réserver aux une à deux instructions vraiment fragiles."
aliases:
  - "emphasis overtriggering claudemd"
  - "all-caps excessif claude.md"
  - "trop de gras claude.md bruit"
  - "emphase budget rare instructions"
  - "sur-declenchement majuscules prompt"
type: erreur
derniere-maj: 2026-06-07
auteur: claude
tags:
  - "#type/erreur"
  - "#domaine/claude-code"
  - "#domaine/claudemd"
---
# Emphasis excessive = sur-déclenchement

## Le mécanisme

L'emphase (gras, majuscules, « IMPORTANT », « JAMAIS ») fonctionne par contraste : une ou deux marques dans un document signalent « ici, attention particulière ». Quand presque chaque ligne est en gras ou en majuscules, le contraste disparaît — plus rien ne ressort, et le modèle tend à appliquer une prudence généralisée non ciblée (sur-déclenchement). Le signal se noie dans son propre volume.

## La règle

L'emphase est un budget d'attention rare, pas un style par défaut. La réserver aux une à deux instructions réellement fragiles (celles qui, oubliées, cassent quelque chose). Le reste se dit en prose neutre, avec une raison. Une règle bien formulée n'a pas besoin de majuscules pour être suivie ; elle a besoin d'être testable et justifiée.

## Application

Au moment d'un audit CLAUDE.md : compter les emphases. Au-delà de quelques-unes par section, en retirer jusqu'à ce que les rares restantes correspondent aux points vraiment critiques. Cohérent avec la doctrine canonique (« une à deux emphases ok, vingt = bruit »).

## Liens

- [[comment-ecrire-claudemd]] — note canonique qui porte cet anti-pattern (section anti-patterns forge)
- [[erreur-stop-critique-position-gotcha-fin]] — anti-pattern CLAUDE.md voisin (position des instructions critiques)
