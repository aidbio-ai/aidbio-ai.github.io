#!/usr/bin/env python3
"""Render a verified, privacy-trimmed AidWeather CLI transcript as a looping GIF."""

from html import escape
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "assets/examples"
TRANSCRIPT = (EXAMPLES / "aidweather-cli-transcript.txt").read_text().splitlines()
VISIBLE = TRANSCRIPT[:8]


def svg(lines):
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="490" viewBox="0 0 1000 490">',
             '<rect width="1000" height="490" rx="18" fill="#f8fbff"/>',
             '<rect width="1000" height="44" rx="18" fill="#eaf1fb"/>',
             '<circle cx="28" cy="22" r="7" fill="#f2542d"/><circle cx="50" cy="22" r="7" fill="#f59e0b"/><circle cx="72" cy="22" r="7" fill="#10b981"/>',
             '<text x="500" y="29" text-anchor="middle" fill="#31435f" font-family="DejaVu Sans Mono" font-size="17">AidWeather CLI</text>']
    for i, line in enumerate(lines):
        color = '#0b45fa' if line.startswith('$') else '#27364e'
        if line.startswith('Cache'):
            color = '#16795b'
        parts.append(f'<text x="34" y="{93+i*43}" fill="{color}" font-family="DejaVu Sans Mono" font-size="20">{escape(line)}</text>')
    parts.append('</svg>')
    return ''.join(parts)


with TemporaryDirectory(prefix="aidweather-gif-") as directory:
    tmp = Path(directory)
    pngs = []
    for n in range(1, len(VISIBLE) + 1):
        source = tmp / f"frame-{n:02}.svg"
        output = tmp / f"frame-{n:02}.png"
        source.write_text(svg(VISIBLE[:n]))
        subprocess.run(["magick", str(source), str(output)], check=True)
        pngs.append(output)
    subprocess.run(["magick", str(pngs[-1]), str(EXAMPLES / "aidweather-cli-poster.png")], check=True)
    args = ["magick", "-delay", "70"]
    for frame in pngs:
        args.append(str(frame))
    args += ["-delay", "220", str(pngs[-1]), "-loop", "0", str(EXAMPLES / "aidweather-cli.gif")]
    subprocess.run(args, check=True)
print(EXAMPLES / "aidweather-cli.gif")
