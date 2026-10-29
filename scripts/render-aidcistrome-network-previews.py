#!/usr/bin/env python3
"""Render a readable selection from saved PRJNA1172690 GO network tables.

The SVG contains only nodes and edges in the saved AidCistrome outputs. It does
not calculate new enrichment or add inferred links.
"""

import csv
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "assets/examples/aidcistrome-prjna1172690"

TERMS = {
    "GO:0009414": (210, 176, "Water deprivation"),
    "GO:0009737": (745, 176, "Abscisic acid response"),
    "GO:0006412": (205, 400, "Translation"),
    "GO:0003735": (520, 400, "Ribosome structure"),
    "GO:0022626": (855, 400, "Cytosolic ribosome"),
    "GO:0006364": (350, 570, "rRNA processing"),
    "GO:0042254": (720, 570, "Ribosome biogenesis"),
}


def render(label: str, slug: str) -> None:
    with (EXAMPLES / f"term-network-{slug}-nodes.csv").open(newline="") as handle:
        nodes = {row["GO_id"]: row for row in csv.DictReader(handle)}
    with (EXAMPLES / f"term-network-{slug}-edges.csv").open(newline="") as handle:
        edges = list(csv.DictReader(handle))
    chosen = set(TERMS).intersection(nodes)
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1060 670" role="img" '
        'aria-labelledby="title desc">',
        f'<title id="title">{escape(label)}: selected GO leading-edge network</title>',
        f'<desc id="desc">{len(chosen)} saved GO terms and their observed leading-edge Jaccard overlap edges. '
        'Orange means positive NES and blue means negative NES. This is a selected view of the complete network.</desc>',
        '<rect width="1060" height="670" rx="24" fill="#f8fbff"/>',
        f'<text x="46" y="52" fill="#23304b" font-family="sans-serif" font-size="25" font-weight="700">{escape(label)} · selected GO network</text>',
        '<text x="46" y="84" fill="#52627a" font-family="sans-serif" font-size="15">Edges are observed leading-edge Jaccard overlaps; no links were added.</text>',
        '<text x="46" y="130" fill="#a84424" font-family="sans-serif" font-size="16" font-weight="700">Positive enrichment</text>',
        '<text x="46" y="330" fill="#24549e" font-family="sans-serif" font-size="16" font-weight="700">Negative enrichment</text>',
    ]
    for row in edges:
        a, b = row["src"].split(" ", 1)[0], row["tgt"].split(" ", 1)[0]
        if a not in chosen or b not in chosen:
            continue
        x1, y1, _ = TERMS[a]
        x2, y2, _ = TERMS[b]
        weight = float(row["w"])
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#8c9bb2" stroke-width="{1.5 + 5 * weight:.2f}" opacity=".7"/>')
    for term, (x, y, short) in TERMS.items():
        if term not in chosen:
            continue
        row = nodes[term]
        nes = float(row["score"])
        fill = "#ffe8df" if nes > 0 else "#e2efff"
        stroke = "#e25b35" if nes > 0 else "#2660b5"
        parts.extend([
            f'<rect x="{x-130}" y="{y-39}" width="260" height="78" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="2"/>',
            f'<text x="{x}" y="{y-4}" text-anchor="middle" fill="#243044" font-family="sans-serif" font-size="16" font-weight="700">{escape(short)}</text>',
            f'<text x="{x}" y="{y+21}" text-anchor="middle" fill="#52627a" font-family="monospace" font-size="13">{term} · NES {nes:+.2f}</text>',
        ])
    parts.append('<text x="46" y="642" fill="#52627a" font-family="sans-serif" font-size="14">Selected from saved AidCistrome network nodes and edges; open the full network for every term.</text>')
    parts.append('</svg>')
    (EXAMPLES / f"network-{slug}-focus.svg").write_text("\n".join(parts) + "\n")


if __name__ == "__main__":
    render("ABA versus mock", "aba")
    render("iCB versus mock", "icb")
