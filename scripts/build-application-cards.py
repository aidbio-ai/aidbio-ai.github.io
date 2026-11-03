#!/usr/bin/env python3
"""Keep the approved application explorer and local previews in sync."""

import argparse
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
PARTIAL = (ROOT / "assets/partials/applications.html").read_text().strip()
PARTIAL = PARTIAL.replace("{{aidwiki-preview}}", (ROOT / "assets/partials/aidwiki-preview.html").read_text().strip())
BEGIN = "<!--applications:begin-->"
END = "<!--applications:end-->"

parser = argparse.ArgumentParser()
parser.add_argument("--check", action="store_true")
args = parser.parse_args()

for name in ("index.html", "design-mock.html", "applications-mock.html"):
    path = ROOT / name
    source = path.read_text()
    pattern = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.S)
    assert len(pattern.findall(source)) == 1, f"Missing or duplicate application markers in {name}"
    partial = PARTIAL
    if name == "applications-mock.html":
        partial = re.sub(r'<h2\b([^>]*data-i18n="apps.title"[^>]*)>(.*?)</h2>', r'<h1\1>\2</h1>', partial, count=1, flags=re.S)
        partial = partial.replace('<h3 class="h2">', '<h2 class="h2">').replace('</h3>', '</h2>')
    expected = f"{BEGIN}\n{partial}\n{END}"
    updated = pattern.sub(lambda _: expected, source)
    if args.check:
        assert source == updated, f"Run scripts/build-application-cards.py for {name}"
    else:
        path.write_text(updated)
print("Application cards synchronized." if not args.check else "Application cards current.")
