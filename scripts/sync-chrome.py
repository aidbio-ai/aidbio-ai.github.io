#!/usr/bin/env python3
"""Stamp the shared site chrome (header, local sub-nav, footer) into every page.

Why this exists: the site is plain static HTML with no build step, so the
header/footer markup used to be copy-pasted into each page and drifted apart.
The single source of truth now lives in assets/partials/*.html; this script
copies it into the marked regions of each page. Run it after editing a partial
or adding a page:

    python3 scripts/sync-chrome.py            # rewrite pages in place
    python3 scripts/sync-chrome.py --check    # exit 1 if any page is stale

Marker syntax inside a page (attributes are optional):

    <!--chrome:header active="projects" i18n="1"-->  ...  <!--/chrome:header-->
    <!--chrome:subnav set="portfolio" active="01"-->  ...  <!--/chrome:subnav-->
    <!--chrome:footer note="portfolio" tagline="Custom right-hand text"-->  ...  <!--/chrome:footer-->

  active  marks the current item (aria-current) in the header or sub-nav.
  i18n    include the EN/PT language switcher (only for pages that load
          assets/js/i18n.js and have translated content).
  set     which assets/partials/subnav-<set>.html to use.
  note    optional assets/partials/note-<note>.html shown above the footer bar.
  tagline replaces the default right-hand footer text.

Relative URL prefixes ({{root}}, {{portfolio}}, {{pages}}) are computed from
each page's location, so the same partial works at any folder depth.
"""
import html
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PARTIALS = os.path.join(ROOT, "assets", "partials")
SKIP_DIRS = {".git", "node_modules", "assets", "docs", "scripts"}

MARKER = re.compile(
    r"(?P<indent>[ \t]*)<!--chrome:(?P<kind>header|subnav|footer)(?P<attrs>[^>]*?)-->"
    r".*?"
    r"<!--/chrome:(?P=kind)-->",
    re.S,
)


def read(name):
    with open(os.path.join(PARTIALS, name), encoding="utf-8") as fh:
        return fh.read().rstrip("\n")


def rel(target, start):
    path = os.path.relpath(target, start).replace(os.sep, "/")
    return "" if path == "." else path + "/"


def render(kind, attrs, page_dir):
    opts = dict(re.findall(r'([\w-]+)="([^"]*)"', attrs))
    active = opts.get("active", "")
    tokens = {
        "root": rel(ROOT, page_dir),
        "portfolio": rel(os.path.join(ROOT, "portfolio"), page_dir),
        "pages": rel(os.path.join(ROOT, "portfolio", "pages"), page_dir),
    }

    if kind == "subnav":
        body = read("subnav-%s.html" % opts["set"])
    else:
        body = read("%s.html" % kind)

    if kind == "footer":
        note = read("note-%s.html" % opts["note"]) if opts.get("note") else ""
        if "tagline" in opts:
            tagline = "<span>%s</span>" % html.escape(opts["tagline"], quote=False)
        else:
            tagline = (
                '<span data-i18n="footer.tagline">'
                "Data Science for Life Sciences, Pharma and Agritech</span>"
            )
        body = body.replace("{{note}}\n", (note + "\n") if note else "")
        body = body.replace("{{tagline}}", tagline)

    # {{#i18n}}...{{/i18n}} blocks: keep or drop.
    keep = opts.get("i18n", "") not in ("", "0", "false")
    body = re.sub(
        r"\{\{#i18n\}\}\n(.*?)\{\{/i18n\}\}\n",
        (lambda m: m.group(1)) if keep else (lambda m: ""),
        body,
        flags=re.S,
    )

    body = re.sub(
        r"\{\{cur:([\w-]+)\}\}",
        lambda m: ' aria-current="page"' if m.group(1) == active else "",
        body,
    )
    body = re.sub(
        r"\{\{curtrue:([\w-]+)\}\}",
        lambda m: ' aria-current="true"' if m.group(1) == active else "",
        body,
    )
    for key, value in tokens.items():
        body = body.replace("{{%s}}" % key, value)

    leftover = re.findall(r"\{\{[^}]*\}\}", body)
    if leftover:
        raise SystemExit("unresolved placeholders in %s partial: %s" % (kind, leftover))
    return body


def stamp(text, page_dir):
    def repl(match):
        indent = match.group("indent")
        body = render(match.group("kind"), match.group("attrs"), page_dir)
        body = "\n".join((indent + line) if line.strip() else line for line in body.split("\n"))
        return "%s<!--chrome:%s%s-->\n%s\n%s<!--/chrome:%s-->" % (
            indent,
            match.group("kind"),
            match.group("attrs"),
            body,
            indent,
            match.group("kind"),
        )

    return MARKER.sub(repl, text)


def pages():
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if name.endswith(".html"):
                yield os.path.join(base, name)


def main():
    check = "--check" in sys.argv
    stale = []
    for path in sorted(pages()):
        with open(path, encoding="utf-8") as fh:
            old = fh.read()
        if "<!--chrome:" not in old:
            continue
        new = stamp(old, os.path.dirname(path))
        if new != old:
            stale.append(os.path.relpath(path, ROOT))
            if not check:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(new)
    if check:
        if stale:
            print("stale chrome in: " + ", ".join(stale))
            sys.exit(1)
        print("chrome is up to date")
    else:
        print("updated: " + (", ".join(stale) if stale else "nothing to change"))


if __name__ == "__main__":
    main()
