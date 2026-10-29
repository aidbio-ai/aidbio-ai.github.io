# Verification record

## Application card follow-up — 26 October 2026

AidWeather now uses its project logo and a light terminal animation that loops when the card opens. The GIF and install commands no longer show recording notes or Play/Pause controls. Reduced-motion visitors see the still poster in place of the GIF. Command boxes use the page's light or dark surface tokens. The redundant introduction above the cards is gone. AidFarm's content was left as previously reviewed.

Five application cards now lazy-load source-backed Archify data-flow diagrams. English and Brazilian Portuguese candidates, standalone HTML viewers, and validation receipts are kept under [`docs/diagrams/`](diagrams/README.md). Archify `finalize dataflow` passed showcase validation, delivery, strict artifact check, and real-browser check for all ten diagrams. The parent page switches the open card's diagram to the selected language and theme. At desktop width, the taller iframe shows the complete diagrams without clipping their bottom rows; a full-page link remains available.

The AidCistrome card adds saved ABA–mock and iCB–mock GO bubble plots, paired gene views, a selected GO network, and an ABA-up motif figure. The case study adds both contrast-specific saved networks, their self-contained interactive originals, and paired promoter-motif figures and tables. The selected network SVGs redraw only saved GO nodes, NES values, and observed Jaccard edges; no enrichment or network links were recomputed. The public motif TSV copies replace an internal absolute library path with the library filename, preserving result values. New source and published hashes and these display transformations are recorded in [`assets/examples/manifest.json`](../assets/examples/manifest.json). No new SRA download or scientific analysis ran.

### Checks completed

- `python3 scripts/build-chrome.py --check`, `python3 scripts/build-application-cards.py --check`, `python3 scripts/check-site.py` (22 pages), and `python3 scripts/check-examples.py` pass. The site checker now checks lazy report and EN/PT diagram paths as well as ordinary links.
- Six theme tests, JavaScript syntax checks for `theme.js`, `app.js`, and `i18n.js`, and `git diff --check` pass.
- The current homepage, Capabilities, Work, Software, About, AidWeather, 404, and the AidCistrome case study were opened in the in-app browser at 1280px and 320px in Light, Dark, and Auto: 48 observations. Each had one h1, no horizontal document overflow, and no completed broken image. Auto resolved to the browser's dark OS preference. Representative cards and the embedded AidWiki diagram were also visually inspected.
- EN/PT switching changed the open AidWiki diagram to the matching language; theme switching updated the iframe URL and full-page link. All five embedded diagram bodies rendered in the browser. The noindex mock contained the same six cards and five diagram links.
- A homepage deep link opened AidWeather. Enter opened the Weather Report card and loaded its report iframe; Space closed it and removed the iframe source. Only one application card remained open at a time. The full report and methods links remained present.
- In normal motion the GIF was visible and the poster hidden. A separate headless Chrome run with `prefers-reduced-motion: reduce` resolved the GIF to `display:none` and the poster to `display:block`. The generated GIF has nine frames and a continuous loop.

These are browser viewport checks, not a physical-phone test. The live operating-system theme was not changed; the existing theme tests cover Auto changes. No commit, push, or deployment was performed.

## Application cards and marketing alignment — initial implementation, 26 October 2026

Implemented the approved blue/orange mock as the marketing-page style, preserving the homepage navigation, infinity wordmark, hero copy, and scientific plot box. The homepage now has six single-open application cards in the specified order. A shared card partial and `build-application-cards.py` keep the noindex mock synchronized. Baloo 2 and Plus Jakarta Sans are self-hosted with license and source notes in `assets/fonts/`; Inter and JetBrains Mono remain available. CSS and updated homepage scripts use a versioned URL to avoid the stale browser cache observed during review.

The AidWeather GIF was rendered from a successful offline `aidweather params describe T2M` and `aidweather cache info` session, with local path and harmless environment warning omitted from the published excerpt. It starts as a still poster and animates only after an explicit Play action. AidFarm uses its existing 12-row synthetic fixture and labels the raw-value plot as demonstration data, without a treatment claim. The Weather Report iframe has no `src` until its card opens and removes `src` on collapse. The full report and methods remain linked. Aid2GO shows saved network, ontology, and internal held-out evaluation visuals. Their card SVG copies replace unresolved external-image CSS color tokens only; the saved originals, structure, scores, and labels are retained and the derivation is recorded in the manifest.

PRJNA1172690 figures were copied from the saved AidCistrome output without rerunning the analysis. The lead all-group PCA is a PNG rendering of the source blind-VST PDF; its legend overlaps one plotted point, so the page also flags replicate spread and links the original PDF. Separate ABA–mock and iCB–mock PCA views, volcanoes, gene views, GO bubble plots, NES landscape, and PC1 loadings follow. The PCA loadings sit inside a secondary detail. `assets/examples/manifest.json` and the case-study `provenance.json` record source and published hashes, the reviewed design, GEO and paper links, and the absence of a direct ABA–iCB differential-expression contrast. The paper is cited as Mar Bono et al., *Molecular Plant* (2025). The PRJNA968041 study remains an archive.

### Checks completed

- `python3 scripts/build-chrome.py --check` and `python3 scripts/build-application-cards.py --check` pass.
- `python3 scripts/check-site.py` passes for 22 pages, including local links, fragments, image alternatives, h1 counts, and EN/PT keys.
- `python3 scripts/check-examples.py` passes output checksums and the existing weather, Aid2GO, study, and report data checks.
- `node scripts/theme.test.cjs` passes all six tests. JavaScript syntax checks pass for `theme.js`, `app.js`, `i18n.js`, and `home.js`; `git diff --check` passes.
- The local in-app browser visited the ten marketing and case pages at 1280px and 320px in Light, Dark, and Auto: 60 page observations with one h1 each, no horizontal document overflow, and no completed broken image. Auto resolved to the browser's light OS preference. Desktop headers and primary content on Capabilities, Work, Software, About, AidWeather, 404, and the new case page were also visually reviewed.
- On the homepage, EN/PT strings, dark/320px layout, mobile menu and Escape focus return, tab selection, keyboard Enter/Space expansion, one-open-card behavior, deep links, GIF play/reset, report load/unload, and the full-report link were checked. The AidFarm and AidCistrome plot previews loaded. The native `<details>` markup and direct links provide readable content when JavaScript is unavailable; JavaScript-disabled browsing was not separately exercised.

These are viewport emulations, not physical-device tests. The browser's actual reduced-motion OS setting was not changed; the GIF's paused-by-default behavior was verified. No new scientific analysis, upstream application run, commit, push, or deployment was performed.

## Homepage copy — 22 October 2026

Replaced the headline with “Complex data? We translate!” and introduced five conversational service points covering consultancy, machine learning and analysis, whole-experiment context, in-house software and tailored applications. Updated EN/PT copy, titles, descriptions, and the introductions to selected work, process and contact. Scientific example captions and report contents were unchanged.

Checked English and Portuguese at desktop and 320px widths in light and dark themes: the headline wraps, all five points render, metadata switches language, and there is no horizontal page overflow. Shared theme preference was restored to Auto. Static page/translation checks, chrome synchronization, JavaScript syntax and Git whitespace checks pass.

[Updated homepage screenshot](review/humanized-homepage-en.jpg).

## Report replacement — 21 October 2026

Imported the supplied `jaguariuna-maize-2022` report into `sample-report/`, with all 30 required HTML/CSS/image/figure/data files. The report covers 18 February–5 July 2022 (138 daily records). Source files were not modified and no upstream application was run. Unlinked PDFs and the separate verification narrative were not published.

Both embeds and all sample-report links use the new content version. Marketing descriptions, iframe titles and EN/PT strings now identify the maize season; the separate 2024 hero weather charts retain their original data and period. Notes and methods remain linked. Shared theme initialization replaces the report's standalone preference storage, while its own chart-palette mapping and resize handlers are preserved. The print branding title was made a label so the exported page has one h1; scientific text and numbers were preserved.

Browser checks: the report initializes seven Plotly charts; light and dark layouts fit desktop and 320px widths with no missing images after chart resizing settles. Notes inherit the shared dark preference. A long Methods link caused 6px of mobile overflow; the exported copy now wraps it and fits at 320px.

[Screenshot of the replacement embed](review/report-maize-2022-replacement.jpg). Auto mode was restored after browser checks.

`check-site.py` passes for 20 pages, `check-examples.py` verifies the imported 138-day series independently of the 366-day preview and validates export checksums, shared chrome is current, six theme tests pass, JavaScript syntax and Git whitespace checks pass.


## Current revision — 2026-10-15

The follow-up replaces marketing copy, adds twelve source-backed preview views with dissolving transitions, embeds a fresh 2024 weather report, and replaces the cacao example with the Arabidopsis PRJNA968041 study.

### Checks completed

- `build-chrome.py --check`, `check-site.py` (19 pages, including report/print/methods), JavaScript syntax and Git whitespace checks pass.
- Six theme tests pass: Auto resolves either OS scheme and follows changes, explicit choices persist, legacy/invalid storage is handled, blocked storage works, cross-tab updates synchronize, and older media-query listeners work.
- `check-examples.py` verifies every published example checksum; 366 consecutive weather records, units/ranges and the VPD calculation; real held-out predictions, known terms and validation threshold; projection/network identities; six-sample study design and result counts; report source data and exported-file hashes.
- Ten copy-paste Bash blocks in `application-examples.md` parse with `bash -n`. The guide distinguishes executed commands from optional AidFarm/AidWiki recipes.
- Browser: all twelve homepage views in light and dark at 320px and 1440px (48 observations), plus all twelve Portuguese views at 320px (12 observations), without page overflow or missing visible images.
- Browser: all seven full-resolution Arabidopsis views in both themes and both widths (28 observations), without page overflow or missing images.
- Browser: actual 2024 report initializes six Plotly charts in light/dark and mobile/desktop layouts. Dark chart tick labels resolve to the intended light text. No missing report images or horizontal page overflow were observed.
- Keyboard Home/End, arrow navigation, rapid family switching and the full-size mobile figure dialog were exercised. The dialog keeps SVG marker IDs unique, can be closed, and permits internal scrolling without page overflow.
- Browser Auto resolved the actual OS light preference; an explicit dark choice survived reload; a separate open report synchronized to the homepage's dark preference. EN/PT preferences persist.

The browser had a cached copy of the old report. Published report links now use a version query, and the embed opens at the detailed charts after load. The exported report shares the website theme bootstrap. Its print-page chart anchors were corrected. Source application code was not changed.

### Scientific scope

Weather: all daily source records for a public coordinate near Jaguariúna, 2024. VPD in the compact view is derived from daily mean temperature and RH; it is not daily maximum VPD. Soil wetness is modeled saturation fraction, not field sensor data. Rainfall and humidity each have a clearly labeled secondary axis; pressure is in its own aligned strip.

Aid2GO: baseline internal protein-held-out test. Q9NT62 was the application's pre-existing true-positive explanation example. Displaying its top four scores plus all five known annotations shows two matches, two unlisted high-scoring terms and three missed known annotations. This is illustrative, not representative performance. Unlisted terms are not confirmed negatives. The model is in development; t-SNE and embedding-similarity edges are exploratory, not experimental validation.

Arabidopsis: completed AidCistrome outputs copied read-only from `adb1`. Six Col-0 samples, three per group; reviewed `~age` design; four-week inflorescence / two-week shoot-apex contrast. Age and tissue are confounded. Original data authors and publication are attributed. All finite volcano records are included, with explicitly disclosed display caps in the homepage overview and full original figures/tables available.

The fresh report ran successfully with `model: null`: 366 observations, six panels, zero model requests. It used the existing dirty local AidWeather Report tree based on `5963e36`. App source and numerical output were preserved; only the exported presentation/theme/anchors were adapted. Plotly, maps and report fonts require external services. The site is not an offline report application.

### Practical limits

Viewport emulation is not a physical-phone test. Actual OS theme settings were not changed; live OS-change and unavailable-storage cases were exercised by the existing test harness. Reduced-motion behavior is explicit in source; the OS reduced-motion setting was not toggled. This is not an accessibility certification or a new validation of the upstream scientific methods. No commit, push or deployment was performed.

### Review artifacts

- [Homepage, light](review/refresh-home-light.jpg)
- [Homepage, dark](review/refresh-home-dark.jpg)
- [Interactive report embed](review/refresh-work-report-light.jpg)
- [Mobile, dark, Portuguese](review/refresh-mobile-dark-pt.jpg)
- [Full study explorer](review/refresh-arabidopsis-light.jpg)
- [Browser check receipts](review/refresh-browser.json)

Current artifacts use the `refresh-` prefix. Older screenshots and the original redesign evidence below are retained as history.

---

## Original redesign verification (historical)

# Redesign verification — 2026-10-15

## Scope and outcome

The redesigned static marketing site and all eight restored narrative pages were checked locally. No commit, push, deployment, DNS change, source-application reset, RNA-seq run, training, or model generation was performed.

## Automated checks

- `python3 scripts/build-chrome.py --check`: shared chrome synchronized across all 15 pages.
- `python3 scripts/check-site.py`: all 15 pages pass local links/fragments, image alternative attributes, unique IDs, one h1, and EN/PT dictionary completeness.
- `node scripts/theme.test.cjs`: six tests pass, covering fresh Auto in either scheme, simulated OS changes, explicit overrides/return to Auto, legacy/canonical preferences, blocked storage, storage synchronization, and older matchMedia listeners.
- JavaScript syntax checks pass for theme, controls, translation logic, and homepage strings.
- All 13 Bash blocks in the application guide pass `bash -n`. This validates shell syntax; it does not claim application generation succeeded.
- `git diff --check`: passes.

## Browser checks

The Codex in-app browser inspected the 15 pages at widths **320, 390, 768, 1024, and 1440px**, in both explicit light and dark themes: **150 layout observations**. No horizontal page overflow, extra/missing h1, or completed broken-image load was observed. Local asset existence was also checked independently. These are browser viewport checks, not physical-phone testing.

Evidence: [light layouts](review/light-layouts.json), [dark layouts](review/dark-layouts.json), [language checks](review/language-checks.json).

Manual interactions verified:

- Auto resolved to the browser's current light OS preference.
- Changing the theme in a second page synchronized the first page, including its selector; dark persisted after reload.
- Mobile menu opened at 320px and Escape closed it with focus returning to the menu button.
- EN/PT updated content, navigation, controls, image/SVG accessibility labels, document language, and title. Portuguese fit all five widths.
- English-only pages remained English and showed no language selector. Returning to the homepage restored Portuguese.
- The Aid2GO preview opened correctly. ArrowRight selected Methods and moved focus to that tab.
- The self-hosted Inter font loaded. Real data previews, selected work, and the restored narrative were visually inspected.

Actual operating-system settings were not changed. Live OS-change behavior and unavailable-storage behavior were exercised with the theme module's test harness; the real browser verified initial Auto detection. Reduced-motion and no-JavaScript fallback rules were inspected in source, not exercised by changing browser/OS settings. This is not a complete accessibility certification.

## Examples and scientific limits

The collection script read existing outputs only and created compact SVG/JSON extracts plus a preserved cacao plot. Checksums and source limitations are in [the manifest](../assets/examples/manifest.json). The revision recorded for an upstream checkout is its HEAD at collection, not proof of the generating revision.

The restored models chapter now identifies MCC correctly, keeps selected-threshold sensitivity within its paper-specific evaluation scope, and does not equate attention with experimentally established binding. Aid2GO's current-software paragraph was refreshed to ESM-2 and similarity edges. Historical research progression, citations, figure rights, and numerical evidence records remain present.

The preserved legacy weather sample has a solar trace whose label and magnitudes need a separate source-unit audit. Its files were not rewritten. The new preview deliberately uses daily maximum temperature in °C instead. The sample's interactive libraries still load from CDNs.

## Application execution preflight

SSH to `adb1` succeeded with the user's explicit SSH config and host-key verification. Installed AidCistrome and AidFarm `--help` commands exited successfully. AidCistrome's current status and report/path interfaces were inspected read-only. Its PRJNA314774 status included completed design output; other active or review-pending runs were left alone.

The guide targets the current server AidCistrome CLI, uses the server's installed AidFarm environment, and keeps local Aid2GO/AidWiki separate from their different server revisions. Optional generation recipes remain unexecuted, as requested. Existing application worktree changes were preserved.

## Screenshots

- [Desktop, light, English](review/desktop-light-en.jpg)
- [Desktop, dark, English](review/desktop-dark-en.jpg)
- [320px, dark, Portuguese](review/mobile-dark-pt.jpg)
- [Selected work](review/selected-work-light.jpg)
- [Restored narrative](review/narrative-light.jpg)

Homepage copy shortened — 22 October 2026: trimmed the introduction and all five service points in EN/PT; synchronized the English HTML fallback. Site checker, chrome check, i18n JavaScript syntax and diff whitespace checks pass. Visually checked desktop light and 320px mobile dark; no horizontal page overflow. Restored Auto theme. Screenshot: `docs/review/concise-homepage-en.jpg`.

Hero deliverables and AgTech naming — 23 October 2026: replaced the five process bullets with three delivery bullets (AgTech & Climate, gene expression, predictive protein models) plus a one-line note, and renamed Agriculture to AgTech & Climate in the hero kicker and capability title, EN and PT. `build-chrome.py --check`, `check-site.py` (20 pages, EN/PT keys) and JavaScript syntax checks passed. Checked in the browser at 320px in EN and PT: text updated and no horizontal overflow. Not rechecked: dark theme, other widths, screenshots in docs/review.

Blue and orange local design mock — 26 October 2026: visited the live aidbio.org homepage and compared its Plus Jakarta Sans/Baloo 2 typography, blue/orange palette, and large infinity mark with the local homepage. `design-mock.html` is a noindex copy of the current homepage with a separate stylesheet; the existing scientific plot panels, copy, language controls, theme controller, and links remain available. Corrected the third application tab to AidCistrome in `scripts/build-example-panels.py` and regenerated `index.html`. Browser checks: desktop light and dark, AidCistrome and Aid2GO tabs, plot expansion dialog, English and Portuguese, 320px light and dark, mobile menu and Escape focus return, ArrowRight tab focus, no broken images, and no horizontal document overflow. Auto resolved to the browser's light OS setting; restored the prior Dark theme and English language after checking. `build-chrome.py --check`, `check-site.py` (21 pages), `check-examples.py`, six theme tests, JS syntax checks, and `git diff --check` passed. Google Fonts are loaded only by the local mock stylesheet; a production rollout would need local font assets.

Typography enlargement and comparison — 29 October 2026:
- Changed shared type sizes in `assets/css/aidbio.css`: 18px body, 20px lead/hero description, 16px navigation/buttons/supporting copy, 14px compact labels, 32px section headings and 24px card headings (CSS px at a 16px default root). Marketing hero is 48px below 640px and 80px above; page titles are 40/56px. Retained existing font families, copy and example provenance. Portfolio inherits the larger body but retains its local heading/metadata/code overrides; archived reports and figure text retain their independent sizing.
- Added `site-settings/typography-comparison.html` (noindex): before/suggested columns with selector locations, a size-isolated Inter visual comparison, 74 original shared-CSS size declarations including cascade overrides, and links to GOV.UK, USWDS and W3C guidance. Recommendations are design choices, not measured comprehension improvements.
- Browser checks: homepage at desktop and 320px; EN/PT mobile copy and menu; Escape closes menu and restores focus to `menuBtn`; light/dark controls; Auto selected and resolved to light. Comparison inspected at desktop and 320px. Measured no horizontal document overflow on comparison, homepage, solutions, work, tools, about, aidweather, 404 and portfolio/index at 320px; those site pages were checked in light and dark. No completed visible image was broken on the mobile pages checked (lazy/offscreen assets were not exhaustively loaded). Computed body 18px; homepage hero 80px desktop / 48px mobile. Viewport override reset; English and Auto restored. Existing six theme tests cover live OS changes.
- Passed: chrome generation check, site checker (23 pages), six theme tests, syntax checks for theme/app/i18n, and diff whitespace check.
- Limits: no manual browser 200% text-only zoom check, JavaScript-disabled browser run, exhaustive portfolio-page review or embedded report/figure legibility audit. No deployment or commit performed.


Full pending-site commit review — 29 October 2026:
- Reviewed the tracked diff and pending-file inventory for the shared font-size update, existing marketing refresh, EN/PT homepage, restored portfolio, public examples and exported sample report. Included the existing planning/provenance records, generated diagram deliveries and browser-review artifacts. Credential-pattern scan found no matches; no pending file exceeded 5 MB. Python sources parse successfully. Figure licences and narrative evidence records are included under `portfolio/docs/`.
- Extended `scripts/check-site.py` to include `site-settings/*.html`, so the relocated typography comparison remains covered by link and page-structure checks.
- Passing checks: chrome, application-card synchronization, site links/fragments/alt text/one h1/EN-PT keys (23 pages), scientific-example and report-export checksums/data consistency, six theme tests, JavaScript syntax, Python syntax and diff whitespace.
- Browser evidence remains the typography review recorded above and the existing review files; no new browser audit was performed for this commit-only request. The existing marketing font-family override differs from the Inter guidance in AGENTS.md, as disclosed by the comparison; this commit preserves the supplied site edits.
- Scope: commit and push the pending site tree on `new-look`; no DNS changes or application-analysis reruns.

- Full staged-file whitespace check revealed upstream trailing spaces in two font licences and ten hash-pinned generated diagram HTML files. `.gitattributes` exempts only their trailing-space checks, preserving original bytes and provenance receipts. All ten diagram SHA-256 hashes match their delivery receipts. Other paths retain normal Git whitespace checks.
