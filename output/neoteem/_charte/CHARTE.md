# Charte graphique Neoteem — Guide d'usage

**Version 1.0 — 29 mai 2026** · Pour tous les documents Neoteem (dossiers stratégiques, formations IA, supports CODIR).

## Identité (dérivée du logo officiel)

| Token | Couleur | Usage |
|-------|---------|-------|
| `--neo-bleu` | `#0a3a5c` | Bleu nuit — titres, bandeaux, wordmark |
| `--neo-teal` | `#00a78e` | Vert/teal — secondaire, accents positifs, baseline |
| `--neo-corail` | `#e8455f` | Alertes, points critiques |
| `--neo-magenta` | `#b6306e` | Accent dégradé |

Dégradé signature (pictogramme logo) : teal → corail → magenta.
Baseline officielle : « Créateur d'intelligence au service de votre performance ».
Police : Segoe UI / Helvetica / Arial (système, pas de dépendance).

## Comment créer un nouveau document

1. Créer `mon-document.html` dans `output/neoteem/`
2. Lier la charte : `<link rel="stylesheet" href="_charte/neoteem-charte.css">`
3. Utiliser les composants ci-dessous (classes CSS prêtes)
4. Générer le PDF (voir commande en bas)

## Composants disponibles

| Composant | Classe HTML | Rendu |
|-----------|-------------|-------|
| Page (saut auto) | `<section class="page">` | 1 page A4 |
| Page de garde | `class="cover"` | Fond bleu nuit + logo + dégradé |
| Header/footer | `.doc-header` / `.doc-footer` | Bandeaux répétés |
| Titre section | `<h1 class="section">` + `<span class="section-num">` | Titre bleu + numéro teal |
| Cartes chiffres | `.card-row` > `.kpi` > `.num` (+ `.alert`/`.ok`) | Gros KPI |
| Avis Claude | `.avis` + `<span class="label">` | Encadré jaune italique |
| Alerte | `.alert` | Encadré rouge |
| Note stratégie | `.note-box` | Encadré teal |
| Verdict | `.verdict` + `.vtitle` | Encart bordé teal |
| Citation centrée | `.pullquote` | Phrase forte centrée |
| Badges audit | `.badge.pass` / `.partial` / `.gap` | Pastilles colorées |
| Tableaux | `<table>` | En-tête bleu, lignes alternées |
| Listes | `<ul class="neo">` | Puces teal |

## Générer le PDF (Chrome headless — aucune dépendance à installer)

```powershell
$chrome='C:\Program Files\Google\Chrome\Application\chrome.exe'
$html='file:///C:/Users/raphael.picard_neote/Documents/claude-forge/output/neoteem/mon-document.html'
$out='C:\Users\raphael.picard_neote\Documents\claude-forge\output\neoteem\Mon_Document.pdf'
$tmp=Join-Path $env:TEMP 'chrome-pdf-profile'
& $chrome --headless=new --disable-gpu --user-data-dir="$tmp" --no-pdf-header-footer --print-to-pdf="$out" $html
```

⚠️ **Flag critique** : utiliser `--no-pdf-header-footer` (Chrome 130+). Le flag `--print-to-pdf-no-header` est **ignoré silencieusement** sur Chrome récent → date + URL + pagination parasites apparaissent dans le PDF. Vérifié Chrome 148, 29 mai 2026.

## Gotchas (vérifiés le 29 mai 2026)

- `--headless=new` (pas `--headless` seul) + `--user-data-dir` temporaire : sinon échec silencieux si Chrome tourne déjà.
- `--print-to-pdf-no-header` retire les en-têtes/pieds par défaut de Chrome (date, URL).
- Sauts de page : `page-break-inside: avoid` sur `.avis`/`.alert`/`table` évite de couper un encadré. Peut créer des pages un peu courtes — c'est voulu (lisibilité > compacité).
- Logo en blanc sur fond foncé : `filter: brightness(0) invert(1)` sur `.cover-logo`.
- Pas de rendu PDF visuel en CLI (pdftoppm absent) : ouvrir le PDF manuellement pour valider la mise en page.
