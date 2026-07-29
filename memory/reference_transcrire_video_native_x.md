---
name: transcrire-video-native-x
description: Transcrire une vidéo native X/Twitter (pas YouTube) — pipeline x-read JSON → curl MP4 → ffmpeg WAV → faster-whisper
trigger: video, x.com, twitter, transcrire, whisper, ffmpeg
metadata:
  type: reference
---

La skill `/watch` (yt-dlp/Whisper) ne marche QUE sur YouTube. Pour une vidéo **native X** (attachée à un tweet), pipeline validé (5 juin 2026, vidéo Boris 30 min) :

1. `/x-read <url>` (ou `reader.py tweet`) → le JSON contient `extended_entities.media[].video_info.variants` avec les URLs MP4 directes (prendre le bitrate le plus haut = 1920x1080).
2. `curl -sL -o video.mp4 "<url_mp4>"` (~265 Mo pour 30 min 1080p).
3. `ffmpeg -y -i video.mp4 -vn -ac 1 -ar 16000 -c:a pcm_s16le audio.wav` → WAV 16kHz mono (55 Mo, bien plus léger pour Whisper que le MP4).
4. `py -m pip install faster-whisper` puis `WhisperModel("small", device="cpu", compute_type="int8")` + `transcribe(wav, language="en", beam_size=5, vad_filter=True)`. Modèle `small` int8 = bon compromis vitesse/qualité anglais technique clair. Lancer en **background** (run_in_background), ~8-15 min CPU pour 30 min audio.

**Gotchas :**
- ffmpeg présent sur la machine forge (`WinGet/Links/ffmpeg`), Whisper NON installé par défaut → `faster-whisper` (pas openai-whisper, plus léger).
- `import whisper` ≠ `import faster_whisper` (paquets distincts).
- Whisper `small` transcrit "Claude" en **"quad"** (homophone) — corriger au moment de la capitalisation vault.
- Foreground `sleep` bloqué par le harness → utiliser run_in_background et attendre la notification, pas de poll.
- Downloads dans `.claude/skills/x-read/downloads/` (gitignored).

Lié : [[arxiv-url-swap-papers-similaires]] (vérif source primaire), feedback tweet-hype-paraphrase (transcrire la source plutôt que la paraphrase d'un tiers).
