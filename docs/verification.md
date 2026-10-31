# Verification record

## Homepage release finishing and animated workflow — 30 October 2026

Removed the hero topic pill and delivery-promise paragraph; moved the bench-to-field sentence below the service cards. The existing decorative logo sits behind and above the headline with empty alternative text. Hero plots now have one concise caption per view, including translated SVG descriptions, with no expansion buttons, raw-data links or window footer. The weather preview links to the AidWeather-Report application card and identifies its use of open-source AidWeather. Updated the report card name and its generated source, including the retained design mock.

Adapted the supplied infinity-loop implementation into local, dependency-free HTML/CSS/JavaScript. It includes animated SVG streams and canvas particles, automatic progression, pause/resume, one-cycle playback, full-loop/spotlight modes, vector and card stage selection, method details and four interactive schematic examples. Viewport visibility suspends the animation. Manual selection stops automatic progression; keyboard navigation is scoped to the workflow. Reduced motion disables automatic playback and keeps manual selection. The template's random power values, biomarker scores and validation/reproducibility guarantees were excluded. See [implementation and source notes](homepage-interactive-workflow.md).

Added an illustrated AidWiki preview after inspecting its current MCP, reference matching and reporting documentation. It shows a report-agent request, retrieval of candidate claims/passages/references, a quotation-location check, and review before citation. It is an illustration, with no live query or invented scientific claim/reference.

Actual checks:

- Chrome and application-card synchronization; site links/fragments/alt text/one h1/EN-PT keys (23 pages); unchanged scientific-asset checksums and example data checks; all six theme tests; syntax checks for theme/app/i18n/home/home-workflow; Python parsing and Git whitespace checks pass. Running the preview generator again produced identical homepage bytes.
- Workflow: EN/PT, Light/Dark, 320/375/768/1440px (16 combinations), selecting all four stages in each. No document overflow or completed visible broken image; exactly one description exposed. All four panels have equal height within each combination. [Measurements](review/homepage-release/layout-checks.json).
- Inspected the desktop hero and full infinity component, and Portuguese mobile in dark theme. All twelve plot views plus AidWiki were checked at 1440px/English/Light and 320px/Portuguese/Dark (26 completed observations): no overflow, expansion controls or completed visible broken images. [Measurements](review/homepage-release/preview-checks.json). The visual checks include the four service cards, decorative logo, wrapped tab bar and concise captions.
- Arrow-key navigation moves selection and focus; Enter selects a vector region; focus outline is 3px. All twelve method buttons change the corresponding description without changing panel height. Block randomization retains C/T1/T2/T3 once in each block; processing toggles its illustrative view; the network action changes the highlighted node; delivery returns selection and focus to Design.
- Full-loop mode illuminates all four quadrants. One-cycle playback progresses through the stages, returns to Design and stops. Canvas sizes to the component. The workflow enters its offscreen-paused state when the hero is in view. AidWiki replay advances through its four steps; EN/PT changes its text and preserves workflow selection. No browser console warnings or errors were observed in the completed checks.
- A temporary deterministic media-change fixture exercised the reduced-motion controller: animation paused, playback controls disabled and manual stage selection still worked. Fixture CSS supplied the corresponding visual media state; the actual OS preference was not changed. A separate script-free copy exposed all four descriptions, hid playback controls and SVG keyboard targets, and had no animation or desktop overflow. Both fixture files were removed.

Screenshots: [hero and AidWiki](review/homepage-release/hero-aidwiki-en.jpg), [complete desktop workflow](review/homepage-release/workflow-desktop-en.jpg), [mobile workflow in Portuguese](review/homepage-release/workflow-mobile-pt-dark.jpg), [mobile AidWiki in Portuguese](review/homepage-release/aidwiki-mobile-pt-dark.jpg).

Limits: browser viewport checks rather than physical touch-device or screen-reader testing; reduced motion was exercised with a deterministic fixture rather than a live OS setting. The script-free check covers script failure, not a browser-wide JavaScript preference change. No upstream scientific application, training or analysis was run. This revision has not been committed, pushed or deployed.

## Homepage services and interactive workflow — 30 October 2026

Replaced the three hero bullets with four service cards: scientific consulting, AI and data science, scientific software and reporting, and training and knowledge transfer. The cards use small inline SVG icons, semantic theme tokens, 16px titles and 15px descriptions; their two-column grid becomes one column below 480px. Hero headline, introductory copy, delivery promise and CTAs are preserved.

Consolidated the former process section into a compact four-stage workflow immediately before Applications, retaining `#process`. Native buttons preview a stage on pointer hover or keyboard focus; click, Enter and Space save the selection. Leaving the controls restores the selected description. `aria-pressed` identifies the saved selection; the visible preview has an accent border and keyboard focus has a 3px outline. All descriptions stay in the DOM and use the existing EN/PT text-only translation mechanism. Their shared grid cell reserves the tallest description, including hidden panels, to keep stage changes stable. No new animation or dependencies were added; the existing reduced-motion rule suppresses border/background transitions.

When scripts fail to load, the workflow controls remain hidden and all four descriptions are readable. Existing translation keys used by the retained design mock remain available. The referenced `../examples/` design files are absent in this checkout; implementation follows the task brief and current shared CSS tokens without changing global fonts or branding.

Checks completed:

- Chrome and application-card generation checks, site checker (23 pages), scientific-example checksums/data checks, all six theme tests, JavaScript syntax checks for theme/app/i18n/home, and `git diff --check` pass.
- In-app browser: EN and PT at 320, 375, 768 and 1440px in Light and Dark (16 combinations). Each has four service cards, no horizontal document overflow and no completed visible broken image. All four workflow stages were selected in every combination. Panel height remained identical across stages at each language/width/theme; [measurements](review/homepage-services-workflow/layout-checks.json) are retained. Final spacing changes affect the introduction only.
- Real mouse pointer movement previewed Discover & Predict without changing the saved Analyze selection; leaving restored Analyze. Tab focus previewed Analyze while Design remained selected. Enter and Space saved selection. Switching EN to PT preserved stage 3 and translated its active title and description. In the accessibility tree, only the visible description is exposed. Mobile menu Escape closes the menu and returns focus to its button. The `#process` link reaches the new component.
- Existing Aid2GO/AidCistrome/AidWeather preview selection, expanded scientific figure opening/closing, and AidWeather card opening/closing with its matching diagram source work. Generated header/footer, application markup and hero scientific examples are byte-identical to the starting commit. Browser console showed no warnings or errors during these checks.
- A temporary copy with all script tags removed showed four readable workflow descriptions, hidden controls, no mobile overflow and the CSS light fallback matching the browser's light OS preference. The temporary file was removed. English and Auto were restored after browser checks; the viewport override was reset. Existing theme tests cover live OS preference changes.

Screenshots: [desktop services](review/homepage-services-workflow/desktop-services-en.jpg), [desktop workflow](review/homepage-services-workflow/desktop-workflow-en.jpg), [Portuguese mobile services in dark theme](review/homepage-services-workflow/mobile-services-pt-dark.jpg), [Portuguese mobile workflow in dark theme](review/homepage-services-workflow/mobile-workflow-pt-dark.jpg).

Limits: viewport emulation and mouse/keyboard checks, not a physical touch-device or screen-reader test. The fallback check removed scripts rather than changing browser JavaScript settings. The live OS theme and reduced-motion preference were not changed. No deployment, DNS changes or scientific analysis runs were performed.

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

Homepage simplification — 31 October 2026:
- Removed the watermark behind the hero headline, the four duplicate stage cards below the infinity animation, and the standalone homepage Capabilities section. Retained the top service descriptions, animation, stage information panels, application examples, and navigation to `solutions.html`.
- Moved keyboard focus destinations from the removed cards to the stage labels beside the animation; removed card progress updates and unused watermark/card CSS. Stage controls identify their corresponding information panels with `aria-controls`.
- Browser checks at 1440px and 320px: EN/PT in light and dark themes; no horizontal document overflow. Confirmed the removed elements are absent, completed images have no loading failures, and the mobile menu exposes the language selector. Visually inspected the workflow in desktop dark and mobile light/dark layouts.
- Passed stage-label clicks, a pointer click on the discovery logo segment, SVG Enter activation, Left/Right arrows, Home/End, visible keyboard focus, and the delivery panel's return-to-design action. English and Auto were restored. No browser console warnings or errors were captured.
- Passed: local HTTP 200; chrome generation check; site checker (23 pages); all six theme tests (including live OS-change behavior); syntax checks for theme/app/i18n/home-workflow; Git whitespace check. The script-failure fallback was inspected in source: all four descriptions remain in HTML and enhanced controls are hidden until initialization. A JavaScript-disabled browser run, physical touch, and live OS-theme switching were not performed.
- Changes remain local and uncommitted; no deployment performed.

Commit preparation — 31 October 2026:
- Reviewed the complete 18-file pending homepage update, including the workflow controller/styles, preview generator, EN/PT strings, generated application cards, implementation notes, and retained 30 October browser evidence. The 31 October simplification checks above describe the final layout; the older screenshots document the preceding revision.
- Re-ran chrome and application-card synchronization, the 23-page site checker, scientific-example checksums/data checks, six theme tests, JavaScript syntax checks, Python parsing, and Git whitespace checks: all passed. Preview regeneration preserved identical homepage and translation bytes. Pending-file size and credential-pattern checks passed.
- Fetched `origin`; local `main` matched `origin/main` before the commit. GitHub Pages configuration confirms publication from `main` at `/`. Browser checks from the preceding edit remain applicable; no additional browser audit was run for this commit request.


## Workflow reference restoration — 31 October 2026

- Compared the source and browser rendering of the supplied `aidbio_interactive_workflow_section.html` (SHA-256 `4f79ef6bfd306b829fbb0b2526a90bfed329bb441b1f0fc5ad2e0c32583a5cd9`) with the homepage. Restored its sixteen capability controls, four workbench layouts/readouts/actions, numbered colored pills, detailed telemetry and stage metadata, ambient/active-quadrant glows, distinct leaf/node motion, selection bursts and full-cycle particle wave. Preserved the previously requested removal of the duplicate selector-card row, hero watermark and standalone Capabilities section. Hero application previews are unchanged.
- Workbenches match the reference structure: 3 × 4 randomized block matrix with clickable treatment cells and titles; six sample boxplots and raw/normalized readouts; actionable hub graph with three driver/score combinations; ranked candidate rows, example release and next-cycle feedback. Prototype values are explicitly labeled synthetic in each workbench; they do not represent measured results, a power calculation, validated candidates or a reproducibility guarantee. Method descriptions retain all sixteen topics without unsupported guarantees.
- Browser layout checks: every stage at 1440px and 320px, EN/PT, light/dark (32 observations). Every observation exposed one panel and four capability controls, with no document overflow and no completed broken images. Inspected desktop light/dark and Portuguese mobile dark screenshots; compared against the original reference in the browser.
- All sixteen capability controls selected the matching description; one note was exposed at a time and the desktop panel height remained 444.28125px. Block randomization retained C/T1/T2/T3 in every block. Normalization switched all six boxplots and both readouts in both directions. Enter and Space on the hub changed the hub/driver/score readout. Delivery returned focus and selection to Design and triggered the wave.
- A pointer drag into the discovery segment previewed its highlight while Design remained selected; a pointer click then selected Discovery and its panel. Right arrow, Home/End and SVG Enter activation passed; keyboard focus remained visible. Full-loop mode set all four quadrant opacities to 1. Auto off preserved running visual streams; enabling Auto advanced Discovery to Deliver after 7.5 seconds. The full-cycle wave was observed independently of stage progression. No console warnings or errors were captured.
- A temporary deterministic reduced-motion fixture disabled Auto/wave controls and all workflow animation, hid canvas particles, and retained manual selection through Deliver. A script-free copy exposed all four panels and sixteen capability notes, hid enhanced controls, disabled block buttons, and had no SVG keyboard targets or document overflow at 1280px. Both fixtures were removed. These checks simulate the media preference and script failure; no OS preference or browser-wide JavaScript setting was changed.
- English and Auto restored. Viewport overrides reset after verification. No physical touch-device or screen-reader audit, scientific application run, commit, push or deployment performed for this restoration.

Commit preparation for reference restoration — 31 October 2026:
- Reviewed the complete six-file restoration. Chrome/application-card synchronization, the 23-page site checker, scientific-example checksums/data checks, six theme tests, JavaScript syntax and Git whitespace checks passed. Preview regeneration preserved identical homepage/translation bytes. Verified the hero/application example blocks are unchanged, all sixteen capabilities and six sample boxplots are present, and the earlier removals remain applied. Pending-file size and credential-pattern checks passed.
- Fetched `origin` and confirmed local `main` matched `origin/main`; Pages publishes `main` at `/`. Browser evidence is the completed restoration audit above; no additional browser audit was run for the commit-only request.
