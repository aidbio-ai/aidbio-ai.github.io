# AidBio site redesign

Approved direction: retain the original landing-page example's warm technical presentation, use the supplied AidBio Design System v2.4, and recover the scientific foundation from the 2026-10-14 backup.

## Decisions

- Keep static GitHub Pages, existing top-level URLs, the established infinity logo, and self-hosted Inter / JetBrains Mono.
- Homepage: hero → selected work → capabilities → delivery method → scientific foundation → software → contact.
- Hero: “Complex data? We translate!” with a conversational introduction, three delivery points aligned to AgTech & Climate, Omics & Bioinformatics and BioTech R&D, a one-line note on documented pipelines and tailored applications, and two actions: discuss a project / explore the work.
- Capabilities: gene expression and regulation; AgTech & Climate; protein networks and predictive models; scientific software and reporting.
- Restore the full narrative portfolio and its evidence/figure-rights records. Present the founder as the scientific basis for AidBio's work.
- Navigation: Capabilities / Work / Software / About. AidWeather has its own existing page and remains visible in Work and Software.
- English and Brazilian Portuguese on the homepage, including shared navigation, controls, accessibility labels, and metadata. Other pages remain English.
- Auto / Light / Dark: Auto follows the OS live, explicit choices persist, legacy preferences are respected, open tabs synchronize, and storage failure is tolerated.
- Use real public outputs. The follow-up authorizes fetching weather and generating a deterministic weather report; use saved Aid2GO test artifacts and the completed server Arabidopsis analysis without retraining. Preserve all application changes.

## Implementation

Shared chrome is stamped by `python3 scripts/build-chrome.py`, including nested portfolio pages and chapter navigation. Generated reports are excluded. Theme initialization is synchronous before styles, with one shared implementation. Homepage translations replace text and accessibility attributes without injecting HTML.

The follow-up changes replace “reusable software” with “tailored applications,” position AidBio as working with research teams from bench to field trials, and retain the three requested commitments: we are biologists; we keep tabs open; we make it yours. English and Brazilian Portuguese stay aligned.

`refresh-site-examples.py` collects source data; `build-example-panels.py` stamps twelve views:

- AidWeather: daily mean/minimum/maximum temperature with rainfall on the right axis; VPD with humidity on the right axis and pressure in an aligned strip; three soil-wetness depths on one 0–1 scale. All 366 daily records for Jaguariúna in 2024, without smoothing. VPD is derived from daily means.
- Aid2GO: an actual GO subnetwork; real held-out baseline scores against known annotations; saved t-SNE coordinates for all 1,000 GO terms; a saved 35-protein similarity network. “Model in development” remains visible. The selected test example shows matches, unlisted terms and missed annotations; it is not a performance estimate.
- Arabidopsis: volcano, GSEA, top genes, PCA and heatmap from PRJNA968041. Age and tissue differ together. The dedicated page adds full-resolution MA and enrichment-curve plots, source tables, original authors and publication links.

Tab changes cross-dissolve with cancellation for rapid switching and an immediate reduced-motion fallback. Arrow keys, Home and End work at each tab level. An accessible figure dialog permits full-size inspection on small screens.

Selected work embeds the supplied Jaguariúna rainfed-maize report (18 February–5 July 2022, 138 days) instead of a screenshot. The standalone report, notes, methods, printable figures and daily/hourly source CSVs remain available. `import-weather-report.py` applies the shared theme and plain branding only to the exported copy; numerical analysis and application source stay unchanged. The report uses external chart/map/font services.

Source checksums, collection checkout identities, and scientific limits are in `assets/examples/manifest.json`; report source/export hashes are in `sample-report/provenance.json`. A checkout HEAD is not evidence of the revision that generated an old artifact. No checkpoints, full galleries, private datasets or infrastructure addresses are shipped.

## Application execution locations

The SSH preflight established that the local and server checkouts are not interchangeable. Use `adb1` for AidCistrome and AidFarm, local Aid2GO and AidWiki for the currently inspected versions, and either host for the matching weather checkouts. Never pull, reset, or overwrite existing application changes to collect an example. See [application-examples.md](application-examples.md).

## Acceptance

- Verify shared chrome, JavaScript syntax, links and fragments, images, translation completeness, and Git whitespace.
- Inspect all marketing and portfolio pages in both themes at 320, 390, 768, 1024, and 1440px; require no horizontal page overflow.
- Test automatic theme resolution, OS changes, explicit overrides, returning to Auto, legacy preferences, cross-tab updates, and unavailable storage.
- Check mobile navigation, keyboard focus, tabs, language persistence, and reduced motion.
- Verify the refreshed sample report and preserve original-study attribution records. Record actual checks and limitations in [verification.md](verification.md).
- Deliver local changes. No commit, push, DNS change, or deployment is included.
