#!/usr/bin/env python3
"""Render the public synthetic AidFarm fixture as a descriptive raw-value plot."""

import csv
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "assets/examples/aidfarm-synthetic.csv"
TARGET = ROOT / "assets/examples/aidfarm-synthetic.svg"

rows = list(csv.DictReader(SOURCE.open(newline="")))
groups = ["Control", "Treatment A", "Treatment B"]
assert len(rows) == 12 and {row["treatment"] for row in rows} == set(groups)
colors = {"Control": "#0B45FA", "Treatment A": "#F2542D", "Treatment B": "#F59E0B"}
items = []
for tick in range(38, 51, 2):
    y = 410 - (tick - 38) * 25
    items.append(f'<line x1="95" y1="{y}" x2="850" y2="{y}" stroke="#dce5f1"/>')
    items.append(f'<text x="78" y="{y+5}" text-anchor="end" fill="#53647a" font-size="16">{tick}</text>')
for idx, group in enumerate(groups):
    x = 220 + idx * 250
    items.append(f'<text x="{x}" y="458" text-anchor="middle" fill="#24354e" font-size="18" font-weight="700">{escape(group)}</text>')
    values = [row for row in rows if row["treatment"] == group]
    for offset, row in zip([-33, -11, 11, 33], values):
        y = 410 - (float(row["biomass_kg"]) - 38) * 25
        items.append(f'<circle cx="{x+offset}" cy="{y:.1f}" r="10" fill="{colors[group]}" opacity=".82"><title>{escape(row["plot"])}: {escape(row["biomass_kg"])} kg</title></circle>')
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="520" viewBox="0 0 960 520" role="img" aria-labelledby="title desc">
<title id="title">Synthetic AidFarm biomass fixture, raw plot-level values</title>
<desc id="desc">Four synthetic plot values in each of Control, Treatment A, and Treatment B. These are demonstration data, not a real trial or a treatment-effect estimate.</desc>
<rect width="960" height="520" rx="24" fill="#fbfcfe"/>
<text x="70" y="53" fill="#163bb5" font-family="Arial,sans-serif" font-size="27" font-weight="700">Field observations, with every plot visible</text>
<text x="70" y="85" fill="#52627a" font-family="Arial,sans-serif" font-size="17">Synthetic demonstration data · 12 invented plot-level records</text>
<text x="37" y="270" transform="rotate(-90 37 270)" fill="#52627a" font-family="Arial,sans-serif" font-size="17">Harvested biomass (kg per plot)</text>
<g font-family="Arial,sans-serif">{''.join(items)}</g>
<line x1="95" y1="410" x2="850" y2="410" stroke="#71839b" stroke-width="2"/>
<text x="70" y="497" fill="#52627a" font-family="Arial,sans-serif" font-size="15">Illustrates how individual observations remain inspectable. No agronomic conclusion.</text>
</svg>'''
TARGET.write_text(svg + "\n")
print(TARGET)
