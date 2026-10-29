#!/usr/bin/env python3
"""Stamp shared header/footer/chapter navigation into marketing and portfolio pages.

Pages carry marker pairs that this script fills in:

    <!--chrome:header active="tools"--> ... <!--/chrome:header-->
    <!--chrome:footer--> ... <!--/chrome:footer-->

    python3 scripts/build-chrome.py           # rewrite pages in place
    python3 scripts/build-chrome.py --check   # exit 1 if any page is stale
"""
from pathlib import Path
import glob
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PARTIALS = os.path.join(ROOT, "assets", "partials")
MARKER = re.compile(
    r"(?P<indent>[ \t]*)<!--chrome:(?P<kind>header|footer|subnav)(?P<attrs>[^>]*?)-->.*?<!--/chrome:(?P=kind)-->", re.S)


def read(name):
    with open(os.path.join(PARTIALS, name), encoding="utf-8") as fh:
        return fh.read().rstrip("\n")


def render(kind, attrs, path):
    opts = dict(re.findall(r'([\w-]+)="([^"]*)"', attrs))
    prefix = "../" * len(Path(path).relative_to(ROOT).parent.parts)
    if kind == "subnav":
        chapters = [("index.html", "The story"), ("pages/01-mechanism.html", "01 Mechanism"), ("pages/02-networks.html", "02 Networks"), ("pages/03-data.html", "03 Data"), ("pages/04-models.html", "04 Models"), ("pages/05-software.html", "05 Software"), ("pages/06-aidbio.html", "06 AidBio"), ("pages/07-portfolio.html", "Applied work")]
        links = []
        for href, title in chapters:
            active = ' aria-current="page"' if Path(path) == Path(ROOT) / "portfolio" / href else ""
            links.append(f'<a href="{prefix}portfolio/{href}"{active}>{title}</a>')
        return '<nav class="subnav" aria-label="Founder story chapters"><div class="container">' + ''.join(links) + '</div></nav>'
    text = read(f"{kind}.html")
    language = read("language.html") if opts.get("i18n") == "1" else ""
    text = text.replace("{{language}}", language)
    text = re.sub(r"\{\{mark:(\w+)\}\}", lambda m: read("mark.html"), text)
    active = opts.get("active")
    if active:
        text = text.replace(f'data-nav="{active}"', f'data-nav="{active}" aria-current="page"')
    return text.replace("{{root}}", prefix)


def stamp(source, path):
    def sub(m):
        indent, kind, attrs = m.group("indent"), m.group("kind"), m.group("attrs")
        body = "\n".join(indent + line if line else line for line in render(kind, attrs, path).split("\n"))
        return f"{indent}<!--chrome:{kind}{attrs}-->\n{body}\n{indent}<!--/chrome:{kind}-->"
    return MARKER.sub(sub, source)


def main():
    check = "--check" in sys.argv
    stale = []
    for path in sorted(glob.glob(os.path.join(ROOT, "*.html")) + glob.glob(os.path.join(ROOT, "portfolio", "**", "*.html"), recursive=True)):
        with open(path, encoding="utf-8") as fh:
            old = fh.read()
        new = stamp(old, path)
        if new != old:
            stale.append(os.path.relpath(path, ROOT))
            if not check:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(new)
    if check and stale:
        print("stale chrome:", ", ".join(stale))
        sys.exit(1)
    print("chrome is up to date" if check else f"updated: {', '.join(stale) or 'nothing'}")


if __name__ == "__main__":
    main()
