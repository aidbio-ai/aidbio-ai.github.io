#!/usr/bin/env python3
"""Keep the homepage and local design mock's application stack in sync."""

import argparse
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
PARTIAL = (ROOT / "assets/partials/applications.html").read_text().strip()
BEGIN = "<!--applications:begin-->"
END = "<!--applications:end-->"

parser = argparse.ArgumentParser()
parser.add_argument("--check", action="store_true")
args = parser.parse_args()

for name in ("index.html", "design-mock.html"):
    path = ROOT / name
    source = path.read_text()
    pattern = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.S)
    assert len(pattern.findall(source)) == 1, f"Missing or duplicate application markers in {name}"
    expected = f"{BEGIN}\n{PARTIAL}\n{END}"
    updated = pattern.sub(lambda _: expected, source)
    if args.check:
        assert source == updated, f"Run scripts/build-application-cards.py for {name}"
    else:
        path.write_text(updated)
print("Application cards synchronized." if not args.check else "Application cards current.")
