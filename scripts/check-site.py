#!/usr/bin/env python3
"""Dependency-free checks for local links, fragments, images, and page structure."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import re
import sys

ROOT = Path(__file__).resolve().parent.parent


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.ids, self.links, self.errors, self.h1, self.i18n = set(), [], [], 0, set()
        self.feed(source)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if 'id' in attrs:
            if attrs['id'] in self.ids:
                self.errors.append('duplicate ID: ' + attrs['id'])
            self.ids.add(attrs['id'])
        self.h1 += tag == 'h1'
        for attr in ['href', 'src', 'data-report-src', 'data-diagram-en', 'data-diagram-pt']:
            if attrs.get(attr):
                self.links.append(attrs[attr])
        if tag == 'img' and 'alt' not in attrs:
            self.errors.append('image without alt attribute')
        if attrs.get('data-i18n'):
            self.i18n.add(attrs['data-i18n'])
        for mapping in attrs.get('data-i18n-attr', '').split(';'):
            if ':' in mapping:
                self.i18n.add(mapping.split(':')[1])


def check():
    paths = sorted([*ROOT.glob('*.html'), *(ROOT / 'portfolio').rglob('*.html'), *(ROOT / 'sample-report').glob('*.html'), *(ROOT / 'site-settings').glob('*.html')])
    parsed = {path: Page(path.read_text()) for path in paths}
    errors = []
    for path, page in parsed.items():
        for message in page.errors:
            errors.append(f'{path.relative_to(ROOT)}: {message}')
        if page.h1 != 1:
            errors.append(f'{path.relative_to(ROOT)}: expected one h1, found {page.h1}')
        for link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if url.path.startswith('/'):
                target = ROOT / unquote(url.path).lstrip('/')
            if target.is_dir():
                target /= 'index.html'
            if not target.exists():
                errors.append(f'{path.relative_to(ROOT)}: missing {link}')
                continue
            if url.fragment and target.suffix == '.html':
                other = parsed.get(target) or Page(target.read_text())
                if unquote(url.fragment) not in other.ids:
                    errors.append(f'{path.relative_to(ROOT)}: missing fragment {link}')
    translations = (ROOT / 'assets/i18n/home.js').read_text()
    copy = json.loads(translations.removeprefix('window.AIDBIO_STRINGS = ').rstrip(';\n'))
    for language in ['en', 'pt']:
        missing = parsed[ROOT / 'index.html'].i18n - copy[language].keys()
        if missing:
            errors.append(f'Missing {language} translations: {sorted(missing)}')
    if copy['en'].keys() != copy['pt'].keys():
        errors.append('Language dictionaries do not have matching keys.')
    if errors:
        print('\n'.join(errors))
        return 1
    print(f'{len(paths)} pages: links, fragments, image alternatives, h1, and EN/PT keys pass.')
    return 0


if __name__ == '__main__':
    sys.exit(check())
