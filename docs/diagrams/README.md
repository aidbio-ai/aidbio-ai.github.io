# Application flow diagrams

These standalone Archify diagrams are embedded when an application card opens. Each diagram has an English and Brazilian Portuguese version; the full-page viewer supports light and dark themes. The HTML, candidate specification, delivery receipt, and browser-check receipt are kept together in each directory so the diagram remains inspectable on GitHub Pages.

| Application | English | Português | Source repository |
| --- | --- | --- | --- |
| AidWeather | [View](aidweather-en/diagram.html) | [Ver](aidweather-pt/diagram.html) | `~/aidbio/dev/aidweather` |
| AidBio Weather Report | [View](report-en/diagram.html) | [Ver](report-pt/diagram.html) | `~/aidbio/dev/aidweather-report` |
| AidCistrome | [View](aidcistrome-en/diagram.html) | [Ver](aidcistrome-pt/diagram.html) | `~/aidbio/dev/aidcistrome` |
| Aid2GO | [View](aid2go-en/diagram.html) | [Ver](aid2go-pt/diagram.html) | `~/aidbio/dev/aid2go` |
| AidWiki | [View](aidwiki-en/diagram.html) | [Ver](aidwiki-pt/diagram.html) | `~/aidbio/apps/aidwiki` |

`candidate.json` pins each source repository's committed revision and cites README line ranges. The diagrams describe documented application flow, not proof that every step ran for the featured example. AidCistrome's project-specific outputs and their checksums are recorded separately in [`assets/examples/manifest.json`](../../assets/examples/manifest.json). The Portuguese viewer string catalogue is saved in [`pt-viewer.json`](pt-viewer.json); it extends the Archify Portuguese example catalogue with the current viewer keys.

Regenerate candidate specifications with `python3 scripts/build-archify-candidates.py`, then run Archify `finalize dataflow` for each candidate with its pinned application checkout as `--repo-root`. Inspect the resulting receipts before replacing published diagrams. The diagrams are self-contained HTML; no remote scripts or services are needed to view them.
