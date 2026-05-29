---
name: pdf-chrome-headless-charte
description: Générer des PDF pro (docs Neoteem/formation) via Chrome headless + charte CSS, gotchas vérifiés
metadata:
  type: reference
---

Chaîne de génération PDF pour documents pro (dossiers stratégiques, formations IA, supports CODIR), validée 29 mai 2026 sur la machine forge.

**Outils** (déjà installés) : Chrome (`C:\Program Files\Google\Chrome\Application\chrome.exe`) + Poppler (via `scoop install poppler` → `pdftoppm`, `pdfinfo`). PAS besoin de weasyprint/reportlab/puppeteer.

**Commande qui marche** :
```
chrome --headless=new --disable-gpu --user-data-dir="$tmp" --no-pdf-header-footer --print-to-pdf="$out" "file:///...html"
```

**Gotchas vérifiés (coûteux à redécouvrir)** :
- **Flag en-têtes** : `--no-pdf-header-footer` (Chrome 130+). Le flag `--print-to-pdf-no-header` est **ignoré silencieusement** sur Chrome récent → date + URL + pagination parasites DANS le PDF.
- `--headless=new` + `--user-data-dir` temporaire OBLIGATOIRES, sinon échec silencieux si Chrome tourne déjà.
- **Pages blanches** : ne PAS mettre header/footer comme éléments de flux HTML répétés par section (ils débordent → pages orphelines avec juste le footer). Soit Chrome natif, soit pas de footer répété.
- **Tables** : NE PAS mettre `break-inside: avoid` sur `<table>` (un grand tableau saute entier → demi-page vide). Le mettre sur `tr` uniquement + `thead { display: table-header-group }` (en-tête répété si coupe).
- **h1** garde `break-after: avoid` ; **PAS h2** (sinon « titre + grand tableau » sautent ensemble).
- **Vérification visuelle** : `pdftoppm -png -r 55 doc.pdf out\p` puis Read l'image. Une page <12 Ko = potentielle page vide à inspecter. Chrome headless `--screenshot` rend le HTML mais PAS le viewer PDF (page noire).
- **Double `<thead>`** dans un tableau HTML = double en-tête affiché. Vérifier visuellement.

**Charte graphique Neoteem** : `output/neoteem/_charte/neoteem-charte.css` + `CHARTE.md`. Identité réelle (logo.webp) : bleu #0a3a5c, teal #00a78e, dégradé teal→corail→magenta. Page de garde fond clair + logo couleur (PAS de filtre brightness/invert qui casse le WebP). Cf [[dossier-strategique-ia-neoteem]].
