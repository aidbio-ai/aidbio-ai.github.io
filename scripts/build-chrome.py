#!/usr/bin/env python3
"""Stamp the shared header and footer (assets/partials/) into every top-level page.

Pages carry marker pairs that this script fills in:

    <!--chrome:header active="tools"--> ... <!--/chrome:header-->
    <!--chrome:footer--> ... <!--/chrome:footer-->

    python3 scripts/build-chrome.py           # rewrite pages in place
    python3 scripts/build-chrome.py --check   # exit 1 if any page is stale
"""
import glob
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PARTIALS = os.path.join(ROOT, "assets", "partials")
MARKER = re.compile(
    r"(?P<indent>[ \t]*)<!--chrome:(?P<kind>header|footer)(?P<attrs>[^>]*?)-->.*?<!--/chrome:(?P=kind)-->", re.S)


def read(name):
    with open(os.path.join(PARTIALS, name), encoding="utf-8") as fh:
        return fh.read().rstrip("\n")


def render(kind, attrs):
    opts = dict(re.findall(r'([\w-]+)="([^"]*)"', attrs))
    text = read(f"{kind}.html")
    text = re.sub(r"\{\{mark:(\w+)\}\}", lambda m: read("mark.svg.html").replace("{{id}}", m.group(1)), text)
    active = opts.get("active")
    if active:
        text = text.replace(f'data-nav="{active}"', f'data-nav="{active}" aria-current="page"')
    return text


def stamp(source):
    def sub(m):
        indent, kind, attrs = m.group("indent"), m.group("kind"), m.group("attrs")
        body = "\n".join(indent + line if line else line for line in render(kind, attrs).split("\n"))
        return f"{indent}<!--chrome:{kind}{attrs}-->\n{body}\n{indent}<!--/chrome:{kind}-->"
    return MARKER.sub(sub, source)


def main():
    check = "--check" in sys.argv
    stale = []
    for path in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
        with open(path, encoding="utf-8") as fh:
            old = fh.read()
        new = stamp(old)
        if new != old:
            stale.append(os.path.basename(path))
            if not check:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(new)
    if check and stale:
        print("stale chrome:", ", ".join(stale))
        sys.exit(1)
    print("chrome is up to date" if check else f"updated: {', '.join(stale) or 'nothing'}")


if __name__ == "__main__":
    main()
