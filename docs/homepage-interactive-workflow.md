# Homepage workflow and evidence preview

The production homepage adapts the user-supplied `aidbio_interactive_workflow_section.html`, SHA-256 `4f79ef6bfd306b829fbb0b2526a90bfed329bb441b1f0fc5ad2e0c32583a5cd9`.

The infinity ribbon, leaf, nodes, masks and gradients retain the supplied vector geometry, with namespaced IDs. The standalone template's Tailwind CDN, Google Fonts, page chrome, global keyboard handler, generated HTML and canvas engine were replaced with the site's own CSS tokens, fonts, translation system and homepage-only controller. No external runtime is added.

## Implementation

- `index.html`: semantic controls, inline vector and four stage panels at the retained `#process` anchor. Each panel includes three method descriptions and one schematic example. All stage and method descriptions remain in the DOM for localization and a script-failure fallback.
- `assets/css/home-workflow.css`: homepage preview adjustments, light/dark surfaces, stage labels around the vector, shared-grid sizing for stable descriptions, vector animation and reduced-motion rules.
- `assets/js/home-workflow.js`: scoped keyboard/focus/pointer selection, playback modes, method selection, illustrative interactions and AidWiki replay. It updates text with `textContent`, never translated HTML. The old simple workflow controller was removed from `app.js`.
- The particle stream samples the supplied SVG paths with `getPointAtLength`, rather than approximating the ribbon with a different curve. Canvas pixel density is capped at 2. Intersection and page visibility stop frame scheduling when the section is not being viewed; reduced-motion changes stop playback and retain manual controls.
- `scripts/build-example-panels.py`: owns the four hero tabs and twelve plot captions. The source images and saved SVG assets remain unchanged; inline SVG descriptions use the concise EN/PT captions. AidWiki markup comes from `assets/partials/aidwiki-preview.html`.
- `assets/partials/applications.html`: owns the AidWeather-Report card name and product introduction; the application-card generator also synchronizes the retained design mock.

The workbench is illustrative: block allocation, before/after distributions, a small network and a delivery checklist explain the stages. They do not estimate statistical power, evaluate a model, infer a biological regulator or certify a deliverable. No values or claims of that kind from the supplied prototype were imported.

## AidWiki implementation evidence

Read-only inspection of the local AidWiki workspace informed the preview:

- `scripts/aidwiki_mcp.py`, functions `wiki_context`, `wiki_match_references` and `wiki_cite`: context packs include claims, evidence quotations, locators, verification, conflicts and formatted references. Reference matching returns candidates, not semantic judgements.
- `scripts/report_refs.py`, `_is_citable`, `match` and `_candidate`: evidence verification status, active claims, source identities and open conflicts remain distinct. Missing evidence is represented explicitly.
- `docs/guides/references-for-reports.md`: the report agent requests evidence for draft statements, reviews candidates and presents a citation proposal. The user confirms the selection before citations are locked and recorded. Report builds use the confirmed lock file.

The graphic illustrates a successful retrieval-and-review path, not a live execution. Its check mark means a source passage was located and checked; the final review step remains necessary to decide whether that evidence supports the report statement at the appropriate scope. It contains no client material, actual research claim, fabricated quotation or invented bibliography.

See [verification](verification.md) for actual browser checks and their limitations.

## Homepage simplification — 31 October 2026

The decorative hero watermark, duplicated stage-card row, and standalone Capabilities section were removed. The infinity regions and their adjacent stage labels select the existing information panel. Arrow keys, Home/End, and the delivery panel’s next-cycle action focus those labels. All four descriptions remain readable when scripts fail. The Capabilities navigation still opens the dedicated solutions page.
