# Site settings previews

Open `typography-comparison.html` in a browser, or serve the repository with
`python3 -m http.server 8000` and visit `/site-settings/typography-comparison.html`.

The comparison records the local 29 October 2026 typography audit: the original
size declarations, suggested values, selector locations, references, and visual
samples. “Applied” refers to the local shared-CSS update made during that audit;
it does not assert that the production site has been deployed with those sizes.

The samples explicitly set their sizes and use the tracked Inter and JetBrains
Mono fonts. They load the shared stylesheet and `assets/js/theme.js`; the small
inline script only binds the preview selector to that existing theme controller.
The preview does not depend on `assets/js/app.js` or the uncommitted site redesign.

Validation: local links and one-h1 structure checked against an exported HEAD
plus these files; theme controller's six tests and inline JavaScript syntax pass.
