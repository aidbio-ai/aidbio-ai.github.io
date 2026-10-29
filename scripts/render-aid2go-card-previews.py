#!/usr/bin/env python3
"""Make externally loaded Aid2GO SVGs readable without changing their data."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "assets" / "examples"
COLORS = {
    "--text-primary": "#0F172A",
    "--text-secondary": "#475569",
    "--text-muted": "#64748B",
    "--surface-card": "#FFFFFF",
    "--amber-text": "#B45309",
    "--emerald-text": "#047857",
    "--violet-text": "#6D28D9",
}
for stem in ("aid2go-network", "aid2go-ontology", "aid2go-test"):
    source = ROOT / f"{stem}.svg"
    text = source.read_text()
    for token, color in COLORS.items():
        text = text.replace(f"var({token})", color)
    if "var(--" in text:
        raise ValueError(f"Unmapped CSS token in {source}")
    (ROOT / f"{stem}-card.svg").write_text(text)
