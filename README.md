# aidbio-ai.github.io

Public site for AidBio (aidbio.org): data analytics and machine learning for life sciences and agriculture.
Plain static HTML on GitHub Pages, no build step beyond one small script.

- Pages: `index.html`, `solutions.html`, `tools.html`, `aidweather.html`, `work.html`, `404.html`
- Styles: `assets/css/aidbio.css` (AidBio Design System v2.4 tokens, light and dark)
- Scripts: `assets/js/app.js` (theme, menu, tabs, copy buttons), `assets/js/viz.js` (hero charts)
- Fonts: self-hosted Inter and JetBrains Mono in `assets/fonts/`
- `sample-report/`: a real AidWeather Report output, shown as a sample (loads Plotly/MapLibre from CDNs)
- Header and footer live in `assets/partials/`; run `python3 scripts/build-chrome.py` after editing them
  (`--check` verifies). Pages contain `<!--chrome:header-->` / `<!--chrome:footer-->` marker pairs.

Run locally: `python3 -m http.server 8000`. The previous site is kept outside the repo in `aidbio-ai.github.io-backup-2026-10-14/`.
