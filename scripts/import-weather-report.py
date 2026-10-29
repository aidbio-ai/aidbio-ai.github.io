#!/usr/bin/env python3
"""Import a supplied public report, preserving its data, copy and chart behavior.

The exported copy shares the site's theme preference and uses versioned links.
Source applications and the supplied report directory are never modified.
"""
import argparse
import csv
import hashlib
import json
import re
import shutil
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
PAGES = {'index.html', 'methods.html', 'print.html', 'notes.html'}
BOOTSTRAP = '<meta name="theme-color" content="#F8FAFC"><script src="../assets/js/theme.js"></script>'
THEME_CLICK = """document.getElementById('theme-toggle').addEventListener('click', function () {
            window.__aidbioTheme.setPreference(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark');
        });"""
THEME_SYNC = """<script>
    document.addEventListener('aidbio:theme', function () {
        if (window.abApplyChartTheme) window.abApplyChartTheme();
    });
    </script>"""


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        self.links += [v for k, v in attrs if k in ['src', 'href'] and v]


def required_files(source):
    queue = [source/name for name in sorted(PAGES) if (source/name).is_file()]
    queue += [source/name for name in ['weather_data.csv', 'hourly_temperature.csv'] if (source/name).is_file()]
    seen = set()
    while queue:
        path = queue.pop().resolve()
        if path in seen:
            continue
        if not path.is_relative_to(source) or not path.is_file():
            raise ValueError(f'Missing or out-of-directory report dependency: {path.name}')
        seen.add(path)
        if path.suffix == '.html':
            parser = Links()
            parser.feed(path.read_text())
            references = parser.links
        elif path.suffix == '.css':
            references = re.findall(r'url\([\'\"]?([^\)\'\"]+)', path.read_text())
        else:
            references = []
        for reference in references:
            url = urlsplit(reference)
            if url.scheme or url.netloc or not url.path:
                continue
            queue.append(path.parent/unquote(url.path))
    return seen


def adapt_page(content, version):
    # Replace the report's own preference bootstrap with the shared controller.
    content = re.sub(
        r'<script>\s*\(function \(\) \{\s*var stored = localStorage.getItem\(\'ab-theme\'\);.*?</script>',
        BOOTSTRAP, content, count=1, flags=re.S)
    if 'src="../assets/js/theme.js"' not in content:
        content = content.replace('</title>', '</title>'+BOOTSTRAP, 1)
    # Preserve the supplied report's chart palette mapping and other event handlers.
    content = re.sub(
        r"document\.getElementById\('theme-toggle'\)\.addEventListener\('click', function \(\) \{.*?\n\s*\}\);",
        lambda _: THEME_CLICK, content, count=1, flags=re.S)
    if 'window.abApplyChartTheme' in content:
        content = content.replace('</body>', THEME_SYNC+'\n</body>', 1)
    content = re.sub(
        r'href="((?:index|methods|print|notes)\.html)(#[^"]*)?"',
        lambda m: f'href="{m[1]}?v={version}{m[2] or ""}"', content)
    return '\n'.join(row.rstrip() for row in content.splitlines())+'\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    args = parser.parse_args()
    source = args.source.resolve()
    for name in ['index.html', 'methods.html', 'print.html', 'weather_data.csv']:
        if not (source/name).is_file():
            parser.error(f'Required report file is missing: {name}')
    files = required_files(source)
    source_hashes = {str(p.relative_to(source)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
    version = hashlib.sha256((json.dumps(source_hashes, sort_keys=True)+Path(__file__).read_text()).encode()).hexdigest()[:12]
    rows = list(csv.DictReader((source/'weather_data.csv').open()))
    if not rows:
        parser.error('Weather data is empty')
    dest = ROOT/'sample-report'
    dest.mkdir(exist_ok=True)
    for path in sorted(files):
        target = dest/path.relative_to(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix == '.html':
            content = adapt_page(path.read_text(), version)
            if path.name == 'print.html':
                # The report verdict is the document heading; its brand title is a label.
                content = content.replace('<h1>Weather report</h1>', '<p class="print-report-title" style="margin:.15rem 0 .2rem;color:#1b2230;font-size:1.55rem;line-height:1.1;font-weight:700">Weather report</p>', 1)
            if path.name == 'methods.html':
                content = content.replace('</head>', '<style>main a { overflow-wrap:anywhere; }</style>\n</head>', 1)
            target.write_text(content)
        else:
            shutil.copy2(path, target)
    # Keep the public URLs stable while invalidating the previous sample's cache.
    for page in ROOT.glob('*.html'):
        content = page.read_text()
        updated = re.sub(
            r'href="(sample-report/(?:index|methods|print|notes)\.html)(?:\?[^"#]*)?(#[^"]*)?"',
            lambda m: f'href="{m[1]}?v={version}{m[2] or ""}"', content)
        updated = re.sub(r'src="sample-report/index\.html[^\"]*"', f'src="sample-report/index.html?v={version}"', updated)
        if updated != content:
            page.write_text(updated)
    exported = {str(p.relative_to(source)):hashlib.sha256((dest/p.relative_to(source)).read_bytes()).hexdigest() for p in sorted(files)}
    record = {
        'source_name':source.name,
        'generator':'Pre-generated AidWeather Report supplied by the user; no application execution during import.',
        'period':rows[0]['date']+'/'+rows[-1]['date'],
        'observations':len(rows), 'version':version,
        'adaptations':'Export only: shared AidBio theme bootstrap and preference toggle; supplied chart palette synchronization; versioned report links; print brand title made a label to retain one h1; long Methods links wrap on mobile. Report wording, charts and numerical analysis preserved.',
        'external_dependencies':['Plotly CDN','Google Fonts'],
        'source_sha256':source_hashes, 'export_sha256':exported,
    }
    (dest/'provenance.json').write_text(json.dumps(record,indent=2)+'\n')
    print(f'Imported {len(files)} files from {source.name}: {len(rows)} records, {record["period"]}.')


if __name__ == '__main__':
    main()
