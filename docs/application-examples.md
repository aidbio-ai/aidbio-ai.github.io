# Application examples for the AidBio website

This guide explains what to collect, why it belongs on the site, and how to obtain it. The current site uses real outputs described below. Weather retrieval and deterministic report generation were executed; AidCistrome and Aid2GO use saved outputs. AidFarm and AidWiki recipes remain optional.

## Current embedded report — 21 October 2026

The public sample is the supplied **Jaguariúna rainfed-maize report, 18 February–5 July 2022 (138 days)**. Import the prepared files without running an application:

```bash
python3 scripts/import-weather-report.py \
  /home/clever/aidbio/dev/site-assets/weather-reports/jaguariuna-maize-2022
python3 scripts/check-site.py
python3 scripts/check-examples.py
```

The import includes the report, Notes, Methods & references, print page, required assets, daily data and hourly temperatures. The exported copy shares the website's theme preference and versioned links; scientific wording, values and chart behavior are preserved. Unlinked PDFs and the source folder's verification narrative are not copied. The 2024 hero weather plots remain a separate example, with a link explicitly labeled “Maize report (2022).”

The generation recipes below document the original 15 October redesign and optional examples. Their 2024 report is not the currently embedded maize report.

## Hosts, versions, and prerequisites

SSH access and the installed AidCistrome/AidFarm `--help` commands were verified on `adb1`. Use the existing user SSH configuration; the system configuration include produced an ownership error. Host-key verification remains enabled.

| Application | Execution location | Inspected revision | Notes |
|---|---|---|---|
| AidCistrome | `adb1` | `cd7a886` | Current organism-profile CLI; local `4a29cd8` is an older implementation. |
| AidFarm | `adb1` | `8ba38b6` | Installed environment and existing outputs; same source revision locally. |
| AidWeather | Local or `adb1` | `e7da358` | Matching source revisions. |
| AidWeather-Report | Local or `adb1` | `5963e36` | Workspace application, with sibling AidWeather dependency. |
| AidWiki | Local | `19b7aba` | Server `4e09a90` differs. |
| Aid2GO | Local | `3cf41d7` | Server `83a3931` differs; use local gallery and cached artifacts. |

Status refreshed on 2026-10-15: local AidCistrome has 2 changed/untracked paths; local Aid2GO 3; local AidWeather Report 18. Server AidCistrome has 21; all other listed server checkouts are clean. Local AidFarm, AidWeather and AidWiki are clean. The fresh report used the dirty local working tree based on `5963e36`, not a clean release. These are snapshots; preserve all changes, including ongoing work. No pull, reset, commit or environment sync was performed.

The noninteractive SSH PATH does not include every scientific executable or `uv`; the server's `~/.local/bin/uv` exists. Use the installed `.venv/bin/` commands below. For a full RNA-seq run, use AidCistrome's dependency checks and documented environment rather than inferring tool availability from PATH alone.

Start in one local Bash terminal and keep it for the recipes:

```bash
export AIDBIO_DEV="/home/clever/aidbio/dev"
export AIDBIO_WIKI="/home/clever/aidbio/apps/aidwiki"
export AIDBIO_SSH_CONFIG="/home/clever/.ssh/config"
export AIDBIO_EXAMPLES="$(mktemp -d /tmp/aidbio-examples.XXXXXX)"
mkdir -p "$AIDBIO_EXAMPLES"/{aidcistrome,aidfarm,aidweather,aidweather-report,aid2go}
printf 'Collection directory: %s\n' "$AIDBIO_EXAMPLES"
```

`/tmp` is temporary: copy selected deliverables to durable storage after review. Keep the application source revision, source accession or synthetic recipe, command, methods, output checksum, and redistribution basis alongside each example. Run environment setup sequentially within each project; do not run concurrent `uv sync` operations against one environment.

## AidCistrome — public Arabidopsis expression analysis

**What:** Volcano, GSEA, top genes, PCA, heatmap, MA and enrichment curves from **PRJNA968041**. Six Col-0 samples: three two-week shoot apices and three four-week inflorescences. The reviewed design is `~age`; the contrast is four-week / two-week.

**Why:** Shows expression analysis, gene-set interpretation and sample context together. Age and tissue are confounded; these plots do not identify their independent effects or establish causal regulation.

**How:** The analysis was already complete on `adb1`; status was verified and the public tables/figures were copied. No RNA-seq or enrichment rerun was needed. Use the application's path resolver rather than hardcoding its configured data mount.

```bash
ssh -F "$AIDBIO_SSH_CONFIG" -T -o BatchMode=yes -o StrictHostKeyChecking=yes \
  -o UpdateHostKeys=no adb1 'cd ~/aidbio/dev/aidcistrome && .venv/bin/aidcistrome status PRJNA968041 --json'

ssh -F "$AIDBIO_SSH_CONFIG" -T -o BatchMode=yes -o StrictHostKeyChecking=yes \
  -o UpdateHostKeys=no adb1 'cd ~/aidbio/dev/aidcistrome && .venv/bin/python -' \
  > "$AIDBIO_EXAMPLES/aidcistrome/arabidopsis.tar" <<'PYCODE'
import contextlib, io, sys, tarfile
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    from aidcistrome.core.paths import outputs_root
    result = outputs_root() / "PRJNA968041" / "results"
files = ["metadata.json", "deseq2_4_week_vs_2_week.csv",
         "gsea/4_week_vs_2_week/4_week_vs_2_week_prerank_all.csv"]
files += [str(p.relative_to(result)) for p in (result / "plots/4_week_vs_2_week").glob("*.png")]
files += ["gsea/4_week_vs_2_week/" + p for p in
          ["4_week_vs_2_week_prerank_dotplot.png", "running_sum.png"]]
with tarfile.open(fileobj=sys.stdout.buffer, mode="w|") as output:
    for name in files:
        output.add(result / name, arcname=name)
PYCODE

mkdir -p "$AIDBIO_EXAMPLES/aidcistrome/results"
python3 - "$AIDBIO_EXAMPLES/aidcistrome" <<'PYCODE'
import sys, tarfile
from pathlib import Path
stage = Path(sys.argv[1])
with tarfile.open(stage / "arabidopsis.tar") as archive:
    archive.extractall(stage / "results", filter="data")
PYCODE
```

**Attribution:** Tieqiang Hu, Xiaohui Li, Liren Du, Darren Manuela and Mingli Xu (2023), *PNAS* 120(22): e2221181120. [Original publication](https://doi.org/10.1073/pnas.2221181120); [BioProject](https://www.ncbi.nlm.nih.gov/bioproject/968041). Figures here are AidCistrome outputs and AidBio redraws of the public data, not copied paper figures.

The homepage volcano includes all finite genes, with display caps at log₂FC ±20 and −log₁₀(padj) 100. Full original figures and tables are provided. Top-gene ranks use signed Wald statistics. The compact GSEA view selects the four strongest NES values per direction among terms with FDR <0.05; the complete table remains available.

## AidFarm — structured analysis without client data

**What:** A synthetic tidy dataset, exploratory figures/dashboard, and its evidence summaries.

**Why:** Shows a real application workflow while keeping client work private. This recipe begins at tidy data; it does not demonstrate workbook ingestion or schema approval.

**How:** Create an isolated server workspace and use its installed application environment. The fixture contains 72 independent synthetic units, three arbitrary groups, and two count variables with no imposed group effect. Every published figure must say **“Synthetic demonstration data.”**

```bash
export AIDBIO_REMOTE_FARM="/tmp/$(basename "$AIDBIO_EXAMPLES")-aidfarm"
ssh -F "$AIDBIO_SSH_CONFIG" adb1 \
  "AIDBIO_REMOTE_FARM='$AIDBIO_REMOTE_FARM' bash -s" <<'REMOTE'
set -eu
mkdir -p "$AIDBIO_REMOTE_FARM/data/processed/demo"
export AIDBIO_REMOTE_FARM
~/aidbio/dev/aidfarm/.venv/bin/python - <<'PY'
import csv, os, random
from pathlib import Path
rng = random.Random(42)
p = Path(os.environ['AIDBIO_REMOTE_FARM']) / 'data/processed/demo/demo_data.csv'
with p.open('w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['planta', 'tratamento', 'date', 'g1', 'flor'])
    for plant in range(1, 73):
        w.writerow([plant, ['T1', 'T2', 'T3'][(plant-1) % 3],
                    '2024-06-01', rng.randint(5, 25), rng.randint(2, 18)])
PY
cd "$AIDBIO_REMOTE_FARM"
~/aidbio/dev/aidfarm/.venv/bin/aidfarm --project-dir "$PWD" analyze \
  --input "$PWD/data/processed/demo/demo_data.csv"
~/aidbio/dev/aidfarm/.venv/bin/aidfarm --project-dir "$PWD" visualize \
  --input "$PWD/data/processed/demo/demo_data.csv"
printf 'Generated workspace: %s\n' "$PWD"
REMOTE

scp -F "$AIDBIO_SSH_CONFIG" -r \
  "adb1:$AIDBIO_REMOTE_FARM/reports/visualizations" \
  "$AIDBIO_EXAMPLES/aidfarm/"
```

Static export may require the configured Plotly/Kaleido browser runtime. Inspect `data/evidence/` on the server alongside the figures. Synthetic p-values, treatment rankings, PCA, and t-SNE are demonstrations, not agronomic results. Generated prose is optional and is deliberately absent from this baseline recipe.

## AidWeather — source data and provenance

**What:** All 366 daily records for a public coordinate near Jaguariúna, Brazil, in 2024, including mean/min/max temperature, precipitation, humidity, pressure and three soil-wetness depths.

**Why:** Connects atmospheric demand and soil context without hiding incompatible units behind one scale. Rain uses the right axis; humidity uses the right axis in a separate view; pressure has an aligned strip; all wetness series share 0–1.

**How:** This command was executed. Isolated cache/log directories preserve application checkouts; use the installed environment rather than `uv sync`.

```bash
export AIDWEATHER_CACHE_DIR="$AIDBIO_EXAMPLES/aidweather/cache"
export AIDWEATHER_LOG_DIR="$AIDBIO_EXAMPLES/aidweather/logs"
"$AIDBIO_DEV/aidweather/.venv/bin/aidweather" fetch \
  --lat -22.72547 --lon -47.011603 \
  --start 2024-01-01 --end 2024-12-31 \
  --params T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,RH2M,PS,GWETTOP,GWETROOT,GWETPROF \
  --output "$AIDBIO_EXAMPLES/aidweather/weather-2024.csv" --no-preview
```

Units: temperature °C, precipitation mm/day, RH2M %, PS kPa; soil wetness is a modeled fraction of saturation, 0–1. VPD (kPa) is estimated using AidWeather Report's fallback formula from daily mean temperature and humidity: `0.6108 × exp(17.27 × T / (T + 237.3)) × (1 − RH/100)`. This is not daily maximum VPD. No curves are smoothed. The full report additionally estimates daily maximum VPD and explicitly labels that distinction.

Keep [NASA POWER](https://power.larc.nasa.gov/docs/methodology/meteorology/) attribution and grid-resolution caveats. The new report replaces the legacy sample with the solar-unit label problem; its solar units are MJ/m²/day with the kWh equivalent stated.

## AidWeather-Report — an inspectable deliverable

**What:** A dashboard, methods page, and printable assets for the same public location and period.

**Why:** Makes the transition from acquisition to a shareable scientific output visible.

**How:** Executed locally with `model: null`: 366 observations, six chart panels and zero model requests. Use the workspace package, preserving its sibling dependency. The dirty application working tree was read without modifying it.

```bash
cat > "$AIDBIO_EXAMPLES/aidweather-report/config.yaml" <<'YAML'
lat: -22.72547
lon: -47.011603
start_date: "20240101"
end_date: "20241231"
model: null
host: "http://127.0.0.1:11434"
YAML

(
  cd "$AIDBIO_DEV/aidweather-report"
  .venv/bin/aidweather-report weather \
    --config-file "$AIDBIO_EXAMPLES/aidweather-report/config.yaml" \
    --output-dir "$AIDBIO_EXAMPLES/aidweather-report/report"
)

python3 -m http.server 8011 --bind 127.0.0.1 \
  --directory "$AIDBIO_EXAMPLES/aidweather-report/report"
```

Open `http://127.0.0.1:8011/`, inspect `methods.html` and `print.html`, then stop the server with Ctrl+C. Static print export needs the configured Kaleido browser runtime. Keep the report directory and its assets together. Interactive runtime libraries may still require network access. Do not infer crop stages or treatment effects from climate context.

## AidWiki — evidence-bound synthesis

**What:** A registered source, claims with evidence locators, and a cited answer derived from AidWeather's documentation.

**Why:** Demonstrates traceability, source quotation verification, and explicit limits rather than a generic chat interface.

**How:** Use an isolated copy of the current local repository. This recipe requires local Ollama and an already installed model. It downloads no model and does not modify the original wiki.

```bash
git clone --no-hardlinks "$AIDBIO_WIKI" "$AIDBIO_EXAMPLES/aidwiki"
ollama list
export AIDBIO_DEMO_MODEL="gemma4:e2b"
```

If that model is unavailable, change `AIDBIO_DEMO_MODEL` to an installed model before continuing.

```bash
(
  cd "$AIDBIO_EXAMPLES/aidwiki"
  uv run aidwiki --repo "$PWD" config set ollama_base_url http://127.0.0.1:11434
  uv run aidwiki --repo "$PWD" learn "$AIDBIO_DEV/aidweather/README.md" \
    --title "AidWeather documentation demonstration" \
    --kind document --model "$AIDBIO_DEMO_MODEL" --no-commit
  uv run aidwiki --repo "$PWD" index
  uv run aidwiki --repo "$PWD" lint --strict
  uv run aidwiki --repo "$PWD" verify-evidence --strict
  uv run aidwiki --repo "$PWD" insight \
    "What does AidWeather provide, and what limitations does its documentation describe?" \
    --retrieval legacy --model "$AIDBIO_DEMO_MODEL" \
    > "$AIDBIO_EXAMPLES/aidwiki-answer.md"
)
```

Review the actual claim IDs, evidence IDs, locators, and quotations. Select only a short answer excerpt with its supporting record; never invent identifiers or publish the vault/Git history. This demonstrates documentation synthesis, not a literature review. Preserve immutable raw sources and the application's integrity gates.

## Aid2GO — protein function and ontology context

**What:** A real GO subnetwork, held-out test predictions compared with known annotations, saved GO-term t-SNE and a protein similarity network. Every model view states **“Model in development.”**

**Why:** Shows how biological representation and ontology structure become inspectable outputs.

**How:** Reuse the local saved gallery and `reports/experiments/v2_unique_pairs_sample_1000x100_seed42/baseline/heldout_scores.npz` plus `metrics.json`. The NPZ supplies test scores, truth, protein IDs and GO IDs; do not substitute full-graph explorer scores. These commands copy the gallery to staging without training or inference.

```bash
cp "$AIDBIO_DEV/aid2go/reports/visualization-gallery/index.html" \
  "$AIDBIO_EXAMPLES/aid2go/index.html"
cp "$AIDBIO_DEV/aid2go/reports/visualization-gallery/manifest.json" \
  "$AIDBIO_EXAMPLES/aid2go/source-manifest.json"
git -C "$AIDBIO_DEV/aid2go" rev-parse HEAD \
  > "$AIDBIO_EXAMPLES/aid2go/source-revision.txt"
```

Open the staged HTML locally and inspect a real protein. Keep its identifiers, ontology vocabulary, relation types, and evaluation scope in the capture. The site uses the pre-existing true-positive explanation protein Q9NT62: its top four scores plus all five known test annotations. That shows two matches, two unlisted high scores and three missed known terms at the validation-selected 0.55 threshold. Scores are not calibrated probabilities. Unlisted terms are not confirmed negatives. This illustrative example was selected by the application, not as a representative test summary. Similarity edges are not experimental PPI edges.

Optional regeneration from compatible saved artifacts:

```bash
(
  cd "$AIDBIO_DEV/aid2go"
  uv run --no-sync aid2go status
  uv run --no-sync aid2go eda gallery --help
  uv run --no-sync aid2go eda gallery \
    --config configs/default.yaml \
    --output "$AIDBIO_EXAMPLES/aid2go/rebuilt" --seed 42
)
```

Regeneration requires saved graphs, ontology, checkpoint, histories, comparison artifacts, and Graphviz. It can perform inference/projections; missing prerequisites are a stop condition, not permission to launch training. Full-graph exploration is not held-out evaluation or official CAFA certification. Do not ship the approximately 33 MB gallery as a homepage asset.

## Build the exact examples and embed the report

From the website repository, after the retrieval commands above:

```bash
"$AIDBIO_DEV/aid2go/.venv/bin/python" scripts/refresh-site-examples.py \
  --dev-root "$AIDBIO_DEV" \
  --weather-csv "$AIDBIO_EXAMPLES/aidweather/weather-2024.csv" \
  --arabidopsis-root "$AIDBIO_EXAMPLES/aidcistrome/results"
python3 scripts/build-example-panels.py
python3 scripts/import-weather-report.py /home/clever/aidbio/dev/site-assets/weather-reports/jaguariuna-maize-2022
python3 scripts/build-chrome.py --check
python3 scripts/check-site.py
python3 scripts/check-examples.py
node scripts/theme.test.cjs
```

The old `collect-site-examples.py` entry point forwards to the refreshed collector and now requires the same explicit inputs. The collector depends on NumPy already present in Aid2GO's environment; the website itself needs no package installation.

`build-example-panels.py` owns only the homepage's `examples` marker block and figure dialog; it keeps EN/PT captions together. It does not overwrite other copy. Export adaptation shares the site's automatic theme bootstrap and the supplied report's own chart-palette handling. Report wording and numerical values stay unchanged. Report source/export hashes are recorded in `sample-report/provenance.json`; interactive libraries, maps and report fonts still use external services. The current embed opens at the new report's verdict and retains a full-page link.

**Executed for this revision:** public weather fetch; deterministic AidWeather Report; SSH status/public result copy; local saved Aid2GO extraction; site generation. **Not executed:** AidFarm synthetic recipe, AidWiki synthesis, RNA-seq rerun, model training or gallery regeneration. Existing changes in every application remain intact.
