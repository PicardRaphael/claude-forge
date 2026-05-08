---
titre: "Amanda Askell — Prompt Engineering & Custom Instructions"
resume: "15 techniques de prompt engineering par Amanda Askell (Anthropic) : TDD prompts, anti-filler, disposition vs regles, debug avec le modele"
aliases:
  - "amanda askell"
  - "askell prompt engineering"
  - "TDD system prompts"
domaine: technique
type: technique
derniere-maj: 2026-04-23
auteur: claude
sources:
  - "https://x.com/AmandaAskell/status/1866207266761760812"
  - "https://www.anthropic.com/research/claude-character"
  - "https://www.bigtechnology.com/p/how-anthropic-builds-claudes-personality"
tags:
  - "#type/technique"
  - "#domaine/prompt-engineering"
  - "#domaine/anthropic"
---

## Description

Amanda Askell est la philosophe d'Anthropic qui dirige l'equipe "personality alignment" et a ecrit le "soul document" de Claude (~30 000 mots). Time 100 AI 2024.

## 1. Test-Driven Development pour System Prompts

Sa technique la plus citee et la plus actionnable.

> "The boring yet crucial secret behind good system prompts is test-driven development. You don't write down a system prompt and find ways to test it. You write down tests and find a system prompt that passes them."
> — [Tweet, 10 dec 2024](https://x.com/AmandaAskell/status/1866207266761760812)

Processus :
1. Ecrire un jeu de tests (messages ou le modele echoue par defaut)
2. Trouver un system prompt qui fait passer ces tests
3. Identifier les cas ou le SP est mal applique, corriger
4. Elargir le jeu de tests, repeter

## 2. La metaphore du "voyageur apprecie"

> "A template here that I like is the idea of a well-liked traveler who can adjust to local customs and the person they're talking to without pandering to them. They're often very open and thoughtful."
> — [Big Technology](https://www.bigtechnology.com/p/how-anthropic-builds-claudes-personality)

Claude s'adapte au contexte sans perdre son caractere propre. Ni cameleon, ni miroir — une personne.

## 3. Contre "You are a..." (role prompting)

> "Whenever I see a system prompt that starts with 'You are a'."
> — [Tweet, 18 juin 2025](https://x.com/AmandaAskell/status/1935410853903483328)

Elle ne l'utilise jamais. Prefere l'honnetete : nommer la tache directement, decrire le contexte reel.

## 4. Contre les filler phrases

Directement dans le system prompt de Claude qu'elle a ecrit :
> "Claude responds directly to all human messages without unnecessary affirmations or filler phrases like 'Certainly!', 'Of course!', 'Absolutely!', 'Great!', 'Sure!', etc."

Plus tard ajoute :
> "Claude never starts its response by saying a question or idea or observation was good, great, fascinating, profound, excellent, or any other positive adjective."

## 5. Clarte = comprendre ce qu'on veut

> "Clear prompting is often just me understanding what I want."

Approche philosophique : definir tous les termes, anticiper les objections, eliminer l'ambiguite. Si on demande au modele d'identifier des reponses "polies" ou "grossieres", definir ces termes explicitement.

## 6. Ne jamais faire confiance au modele

> "I don't trust the model ever. I just hammer on it to see if it can perform the task consistently."

Quelques centaines de prompts bien craftes > des milliers de prompts bacles.

## 7. Eviter la paresse

> "There's a laziness that overtakes me if I'm talking to Claude where I hope Claude just figures it out."

Investir du temps dans des instructions detaillees.

## 8. Utiliser le modele pour debugger les prompts

3 questions cles quand un prompt echoue :
1. **"Why did you do that?"** — comprendre le raisonnement du modele
2. **"What could I have said that would make you not make that error? Write that out as an instruction."** — utiliser le modele pour ameliorer son propre prompt
3. **"What other details can I provide to help you answer better?"**

## 9. Exemples qui generalisent, pas qui memorisent

Utiliser des exemples de **domaines non lies** pour transmettre la structure sans biaiser la sortie. Ex : exemples de contes pour enfants pour une tache d'extraction factuelle.

> Pas fan de "beaucoup d'exemples, ou un ou deux exemples. Trop peu, le modele s'accroche a ceux-la."

## 10. Etre direct, pas theatral

Ne pas utiliser "I am a teacher trying to write a quiz." Dire directement : "I want you to construct questions that evaluate a language model."

## 11. Disposition > regles (design de caractere)

Principes du [blog post Claude Character](https://www.anthropic.com/research/claude-character) :
- Definir **qui** est l'IA en tant que personne, pas juste ce qu'elle peut/ne peut pas faire
- Construire une **disposition**, pas des regles — approche ethique de la vertu (Aristote)
- Modeliser un **humain ideal** : "Que ferait un humain ideal dans la situation de Claude ?"
- Donner les **raisons** des comportements, pas juste les comportements

> "Instead of just saying, 'here's a bunch of behaviors that we want,' we're hoping that if you give models the reasons why you want these behaviors, it's going to generalize more effectively in new contexts."

## 12. Contre l'engagement-bait

> "If we think about people who are just trying to engage us, I don't think we often think of those people as good people. We think our friends are good because they tell us what we need to hear."

## 13. Externaliser son cerveau

Le coeur du bon prompting = "externalize your brain" dans le modele. Relire ses prompts comme si on les decouvrait pour la premiere fois.

## 14. Edge cases

- Toujours tester : inputs vides, donnees manquantes, inputs completement inattendus
- Donner un fallback explicite : "If something weird happens... just output 'unsure.'"

## 15. Pourquoi les system prompts

> "Why do we use system prompts at all? First, they let us give the model 'live' information like the date. Second, they let us do a little bit of customizing after training and to tweak behaviors until the next finetune."
> — [Thread Claude 3, mars 2024](https://x.com/AmandaAskell/status/1765207842993434880)

## Quand utiliser

A chaque creation de system prompt, skill, agent description, ou instructions personnalisees. Reference fondamentale pour le prompt engineering chez Anthropic.

## Sources cles

- [Thread TDD system prompts (dec 2024)](https://x.com/AmandaAskell/status/1866207266761760812)
- [Thread Claude 3 system prompt (mars 2024)](https://x.com/AmandaAskell/status/1765207842993434880)
- [Blog Anthropic — Claude Character (juin 2024)](https://www.anthropic.com/research/claude-character)
- [Constitution de Claude](https://www.anthropic.com/constitution)
- [Deep Dive video YouTube](https://www.youtube.com/watch?v=T9aRN5JkmL8)
- [Philosopher Q&A (dec 2025)](https://www.youtube.com/watch?v=I9aGC6Ui3eE)
- [Big Technology interview](https://www.bigtechnology.com/p/how-anthropic-builds-claudes-personality)
- [Startup Spells synthese](https://startupspells.com/p/amanda-askell-prompt-engineering-secrets)
- [Simon Willison tag](https://simonwillison.net/tags/amanda-askell/)
- [Tweet "You are a" (juin 2025)](https://x.com/AmandaAskell/status/1935410853903483328)
- [Tweet soul document (dec 2025)](https://x.com/AmandaAskell/status/1995610567923695633)

## Liens

- [[MOC-Techniques]]
- [[forge-prompt-machine]]
- [[claude-desktop-preferences]]
- [[Context Engineering]]
