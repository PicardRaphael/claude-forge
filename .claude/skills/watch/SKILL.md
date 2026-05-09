---
name: watch
description: Transcribe and analyze YouTube videos — downloads auto-generated subtitles via yt-dlp, cleans them, and returns the full transcript for analysis. Use when the user shares a YouTube URL to analyze, summarize, or extract information from a video.
argument-hint: "<youtube-url>"
allowed-tools: Bash, Read, Write
user-invokable: true
---

# Watch — Transcription YouTube

Telecharge les sous-titres auto-generes d'une video YouTube via `python -m yt_dlp`, les nettoie, et retourne la transcription pour analyse.

## Etapes

### 1. Valider l'URL

L'URL est fournie via `$ARGUMENTS`. Verifier qu'elle contient `youtube.com` ou `youtu.be`. Si absente ou invalide, demander a l'utilisateur.

### 2. Lister les sous-titres disponibles

```bash
python -m yt_dlp --list-subs "$URL" 2>&1 | head -50
```

Inspecter la sortie pour identifier :
- `fr` (manuel) ou `fr` (auto) — priorite 1
- `en` (manuel) ou `en` (auto) — fallback si FR absent
- Si aucune langue disponible : signaler et s'arreter

### 3. Telecharger les sous-titres

**Cas FR disponible :**
```bash
python -m yt_dlp \
  --write-auto-sub \
  --sub-lang fr \
  --convert-subs srt \
  --skip-download \
  -o "/tmp/watch_transcript" \
  "$URL" 2>&1
```

**Cas FR absent, fallback EN :**
```bash
python -m yt_dlp \
  --write-auto-sub \
  --sub-lang en \
  --convert-subs srt \
  --skip-download \
  -o "/tmp/watch_transcript" \
  "$URL" 2>&1
```

Note : `--convert-subs srt` est obligatoire pour les sous-titres auto-generes (livres en VTT par YouTube, pas en SRT natif).

### 4. Detecter le fichier cree

Apres le telechargement, chercher le fichier cree :

```bash
ls /tmp/watch_transcript.* 2>/dev/null
```

Le nom reel peut etre `.fr.srt`, `.en.srt`, `.fr.vtt`, `.en.vtt` selon la disponibilite. Utiliser le fichier trouve.

### 5. Nettoyer la transcription

Utiliser le script dedie qui supprime les timestamps, tags inline `<c>`, numeros de sequence, et deduplique les lignes repetees (artfact auto-gen) :

```bash
python .claude/skills/watch/scripts/clean_subs.py /tmp/watch_transcript.<lang>.srt
```

Si le fichier est `.vtt` (conversion echouee) : le script gere les deux formats.

### 6. Retourner la transcription

Afficher la transcription propre dans la reponse. Puis proposer a l'utilisateur les analyses possibles :
- Resume
- Points cles
- Citations marquantes
- Extraction de donnees specifiques
- Questions/reponses sur le contenu

## Format de reponse

```
Transcription recuperee : [titre de la video]
Langue : FR auto-gen | EN auto-gen | FR manuel
Longueur : ~X mots

---

[transcription propre]

---

Que voulez-vous analyser ?
```

## Gotchas

- **`--sub-format srt` ne fonctionne PAS pour l'auto-gen** — YouTube livre les auto-subs en VTT. Utiliser `--convert-subs srt` a la place pour forcer la conversion.
- **Tags inline dans la transcription auto-gen** — Le VTT auto-gen contient `<00:00:01.500>`, `<c>`, `</c>`. `sed` simple ne les elimine pas. Utiliser `scripts/clean_subs.py` qui gere les regex correctement.
- **Lignes dupliquees** — L'auto-gen repete souvent la meme ligne sur plusieurs cues successifs. `clean_subs.py` duplique les consecutives identiques.
- **Nom de fichier impredictible** — yt-dlp peut creer `.fr.srt`, `.en.srt` ou `.fr.vtt` selon la langue et la disponibilite. Toujours faire un `ls /tmp/watch_transcript.*` apres telechargement.
- **Warning JS runtime** — yt-dlp peut afficher `WARNING: [youtube] Unable to load JS...` — c'est normal, le telechargement fonctionne quand meme.
- **`python -m yt_dlp` pas de chemin absolu** — yt-dlp est installe via pip, portable cross-PC. Ne jamais hardcoder le chemin de l'executable.
- **`/tmp/` fonctionne dans Bash** — La skill s'execute via le Bash tool (Git Bash sur Windows), pas PowerShell. `/tmp/` est valide. Si besoin de portabilite totale : `python -c "import tempfile; print(tempfile.gettempdir())"`.
- **Transcription auto-gen = erreurs de reconnaissance** — Signaler systematiquement que la transcription est generee automatiquement et peut contenir des erreurs (noms propres, termes techniques).
- **Videos privees ou sans sous-titres** — Signaler clairement si yt-dlp retourne une erreur d'acces ou aucun sous-titre disponible.

## Apprentissage

Si une langue de sous-titres est frequemment absente pour un type de video (ex: videos courtes < 2 min, streams live, videos musicales), sauvegarder en memoire projet :

```
memory: "Videos de type [X] n'ont pas de sous-titres FR auto-gen. Utiliser EN directement."
```

Apres plusieurs usages, si un pattern emerge sur les types de videos qui posent probleme, proposer un fallback plus intelligent (ex: detection automatique de la langue par le titre).
