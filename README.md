# AidBio website

Public site for AidBio at [aidbio.org](https://aidbio.org). Static HTML on GitHub Pages, with self-hosted fonts and shared CSS/JavaScript. No framework or package install is required.

## Preview

```bash
python3 -m http.server 8000
```

Open `http://127.0.0.1:8000/`. The homepage is available in English and Brazilian Portuguese. Other marketing pages and the restored scientific narrative remain English.

## Structure

- `index.html`: Complex data? We translate!; the preserved scientific plot demo, six expandable application cards, capabilities, delivery method, Why AidBio exists, and contact.
- `solutions.html`, `work.html`, `tools.html`, `about.html`, `aidweather.html`: focused marketing and context pages.
- `portfolio/`: eight restored narrative pages, original figures/diagrams, citations, evidence map, and figure-rights record.
- `assets/css/aidbio.css`: shared marketing-page blue/orange styling with restrained scientific accents and self-hosted Baloo 2 / Plus Jakarta Sans; Inter and JetBrains Mono remain available for other pages.
- `assets/js/theme.js`: blocking Auto / Light / Dark bootstrap, preference persistence, legacy migration behavior, live OS and cross-tab updates.
- `assets/i18n/home.js`: EN/PT strings; text-only translation implementation in `assets/js/i18n.js`.
- `assets/partials/`: shared header, footer, logo mark, and homepage application cards. `scripts/build-chrome.py` and `scripts/build-application-cards.py` stamp generated marker contents; edit the partials instead of those marker contents.
- `assets/examples/`: real weather, Aid2GO and Arabidopsis previews, full study figures, source tables and provenance.
- `aidcistrome-aba-icb.html`: PRJNA1172690 / GSE279431 case study with saved AidCistrome figures, source records, and explicit contrast limits. `arabidopsis.html` retains the earlier PRJNA968041 case study.
- `sample-report/`: Jaguariúna maize report (18 February–5 July 2022), notes, methods, print page, figures and daily/hourly source CSVs. Interactive libraries and maps use external services.

The source design references are in `../examples/`; the previous site remains in `../aidbio-ai.github.io-backup-2026-10-14/`.

## Checks

```bash
python3 scripts/build-chrome.py --check
python3 scripts/build-application-cards.py --check
python3 scripts/check-site.py
python3 scripts/check-examples.py
node scripts/theme.test.cjs
node --check assets/js/theme.js
node --check assets/js/app.js
node --check assets/js/i18n.js
node --check assets/i18n/home.js
git diff --check
```

Also inspect light/dark themes, English/Portuguese, keyboard navigation, and mobile width 320px. Generated sample reports are excluded from shared-chrome stamping.

## Working documents

- [Redesign plan](docs/site-redesign-plan.md)
- [Application examples: what, why, and copy-paste commands](docs/application-examples.md)
- [Verification record](docs/verification.md)

The example guide distinguishes `adb1` applications from local checkouts. The current application cards use saved public-data outputs, a synthetic AidFarm fixture, and an offline AidWeather CLI excerpt. The PRJNA1172690 figures were copied from completed AidCistrome outputs; no RNA-seq rerun or model retraining was performed for the site. The embedded report remains the existing exported sample.
