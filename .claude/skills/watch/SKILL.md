---
name: watch
description: Transcribe and analyze YouTube videos — downloads YouTube subtitles via yt-dlp when available, falls back to Whisper ASR on the audio when no captions exist. Use when the user shares a YouTube URL to analyze, summarize, or extract information from a video.
argument-hint: "<youtube-url>"
allowed-tools: Bash, Read, Write
user-invocable: true
---

# Watch — Transcription YouTube

Telecharge les sous-titres auto-generes d'une video YouTube via `python -m yt_dlp`, les nettoie, et retourne la transcription pour analyse. Si la video n'a pas de sous-titres, fallback Whisper ASR sur l'audio.

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
- Si la sortie contient "has no automatic captions" ET "has no subtitles" → passer a l'**etape 3-bis (fallback Whisper)**

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

### 3-bis. Fallback Whisper (si aucun sous-titre disponible)

Quand la video n'a ni sous-titres manuels ni auto-generes.

**a. Telecharger l'audio uniquement :**
```bash
python -m yt_dlp -f "bestaudio" --extract-audio --audio-format wav \
  -o "/tmp/watch_audio.%(ext)s" "$URL" 2>&1
```

Si `--extract-audio` echoue (pas de JS runtime), telecharger la video complete puis extraire avec ffmpeg :
```bash
python -m yt_dlp -o "/tmp/watch_audio_raw.%(ext)s" "$URL" 2>&1
ffmpeg -i /tmp/watch_audio_raw.* -vn -ar 16000 -ac 1 /tmp/watch_audio.wav -y 2>&1
```

**b. Convertir en 16kHz mono si necessaire :**
```bash
ffmpeg -i /tmp/watch_audio.wav -ar 16000 -ac 1 /tmp/watch_audio_16k.wav -y 2>&1
```

**c. Transcrire avec faster-whisper :**

Verifier d'abord que faster-whisper est installe :
```bash
python -c "import faster_whisper; print('faster-whisper OK')" 2>&1
```

Si l'import echoue, indiquer a l'utilisateur : `pip install faster-whisper` (ou relancer `install.bat`).

Ecrire le script de transcription via le **Write tool** vers `/tmp/watch_whisper.py` avec ce contenu :

```python
import sys, json
from faster_whisper import WhisperModel
model = WhisperModel("base", device="cpu", compute_type="int8")
segments, info = model.transcribe(sys.argv[1])
results = [{"start": round(s.start,2), "end": round(s.end,2), "text": s.text.strip()} for s in segments]
with open(sys.argv[2], "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"Transcribed {len(results)} segments, language: {info.language}")
```

Executer ensuite :
```bash
python /tmp/watch_whisper.py /tmp/watch_audio_16k.wav /tmp/watch_whisper_out.json 2>&1
```

Nettoyer apres execution :
```bash
rm -f /tmp/watch_whisper.py /tmp/watch_audio*.wav /tmp/watch_audio_raw.* 2>/dev/null
```

**d. Lire et formater la transcription :**

Lire `/tmp/watch_whisper_out.json` avec le Read tool, puis convertir en texte propre :
- Concatener tous les champs `text` dans l'ordre
- Ajouter des retours a la ligne toutes les ~10-15 phrases pour la lisibilite

### 4. Detecter le fichier cree (cas sous-titres)

Apres le telechargement, chercher le fichier cree :

```bash
ls /tmp/watch_transcript.* 2>/dev/null
```

Le nom reel peut etre `.fr.srt`, `.en.srt`, `.fr.vtt`, `.en.vtt` selon la disponibilite. Utiliser le fichier trouve.

### 5. Nettoyer la transcription (cas sous-titres)

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

**Cas sous-titres YouTube :**
```
Transcription recuperee : [titre de la video]
Langue : FR auto-gen | EN auto-gen | FR manuel
Longueur : ~X mots

---

[transcription propre]

---

Que voulez-vous analyser ?
```

**Cas fallback Whisper ASR :**
```
Transcription via Whisper (pas de sous-titres YouTube disponibles)
Titre : [titre de la video]
Langue detectee : [langue Whisper]
Modele : base / CPU / int8
Longueur : ~X mots

Note : transcription ASR automatique — peut contenir des erreurs (noms propres, termes techniques).

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
- **`faster-whisper` et `ffmpeg` requis pour le fallback** — Installer via `install.bat` du projet ou manuellement : `pip install faster-whisper` + `ffmpeg` dans le PATH. Si absent, signaler a l'utilisateur avec les instructions d'installation.
- **Modele "base" Whisper** — Bon compromis vitesse/qualite (~10 min pour 47 min de video sur CPU). Pour plus de precision : "small" ou "medium" (plus lent). Pour plus de vitesse : "tiny" (qualite moindre).
- **Python alias MS Store sur Windows** — Sur certains PC Windows, `python` renvoie vers le Microsoft Store. Tester `python -c "import faster_whisper"` avant d'executer le script. Si ca echoue malgre pip install, utiliser le chemin absolu Python (ex: `C:/Python313/python.exe`).
- **yt-dlp --extract-audio sans JS runtime** — Si yt-dlp ne peut pas charger le JS runtime, `--extract-audio` peut echouer. Fallback : telecharger la video complete (`-o "/tmp/watch_audio_raw.%(ext)s"`) puis extraire l'audio avec `ffmpeg -i` pour isoler la piste audio en WAV 16kHz mono.
- **Script whisper via Write tool** — Ne pas utiliser un heredoc Bash pour le script Python (les f-strings et guillemets cassent le quoting). Utiliser le Write tool vers `/tmp/watch_whisper.py`, puis `python /tmp/watch_whisper.py ...`.

## Apprentissage

Si une langue de sous-titres est frequemment absente pour un type de video (ex: videos courtes < 2 min, streams live, videos musicales), sauvegarder en memoire projet :

```
memory: "Videos de type [X] n'ont pas de sous-titres FR auto-gen. Utiliser EN directement."
```

Apres plusieurs usages, si un pattern emerge sur les types de videos qui posent probleme, proposer un fallback plus intelligent (ex: detection automatique de la langue par le titre).
