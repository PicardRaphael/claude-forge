---
name: lire-fichier-entier-avant-verdict
description: "JAMAIS de verdict (comparer, auditer, supprimer, juger doublon/subsumé) sur une lecture partielle d'un fichier. Trouvé un fichier à évaluer → le lire EN ENTIER d'abord, poser ensuite."
metadata:
  node_type: memory
  type: feedback
---

Quand je trouve un fichier que je dois ÉVALUER (comparer à un autre, auditer, juger « doublon/subsumé/appauvri », m'apprêter à supprimer ou remplacer), je le lis **EN ENTIER** avant tout verdict. Lire 30 lignes puis conclure « doublon appauvri, safe to delete » = faute.

**Why:** 7 juin 2026, capitalisation Important/. J'ai lu les canoniques vault EN ENTIER mais seulement les 30 premières lignes des 4 docs source (`reference-hooks`, `reference-subagents`, `reference-claude-md`, `Stack IA`) — puis j'ai proposé de les supprimer comme « doublons appauvris ». Vérification asymétrique : prouver que la DESTINATION est riche ne prouve PAS que la SOURCE est subsumée. « Zéro perte » exige l'inverse : que chaque claim substantiel du fichier source EXISTE déjà dans la cible — ce qui demande de lire le source en entier (lignes 31-fin), là où vit le contenu potentiellement neuf. Confirmé après lecture complète : `reference-subagents` lignes 119-204 contenaient les niveaux 1-6 de forçage d'invocation skill + issues #43630/#32910 — du contenu que la suppression sur 30 lignes aurait risqué de perdre. Raphael : « je veux plus jamais ça ».

**How to apply:**
1. **Verdict = lecture complète, sans exception.** Avant d'écrire « doublon / subsumé / safe to delete / identique / appauvri / à supprimer » sur un fichier : `Read` SANS `limit`/`offset` (ou read_note SANS max_lines pour le vault). La barre = avoir le fichier ENTIER en contexte, comme `reference-technique-stack-ia` (276 lignes lues → recréées verbatim → git rm sûr).
2. **Asymétrie interdite** : ne jamais comparer un fichier lu en entier (A) à un fichier lu partiellement (B) puis trancher sur B. Les deux côtés en entier, ou pas de verdict.
3. **`limit:30` = orientation, jamais jugement.** Lire un extrait pour s'orienter est OK ; en TIRER une conclusion de suppression/équivalence ne l'est pas. Si je me surprends à juger sur un extrait → STOP, relire en entier, PUIS reposer.
4. **« Quand je trouve, je repose, puis je lis en entier »** (formulation Raphael) : trouver le fichier ne clôt rien — c'est le déclencheur de la lecture complète.

Renforce la phase A de `.claude/rules/sequence-canonique-modification.md` (« Composant existant EN ENTIER ») par un interdit explicite du verdict-sur-lecture-partielle. Cf [[feedback_lire_canoniques_avant_audit]] (même esprit côté canoniques vault) et [[feedback_stop_over_verifying]] (ne pas SUR-vérifier non plus : lire entier le fichier jugé, pas re-lire 20 fichiers déjà connus).
