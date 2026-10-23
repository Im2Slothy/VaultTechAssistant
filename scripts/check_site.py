"""Check all local page links, assets, anchors, and basic HTML structure."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = []
        self.links = []
        self.counts = Counter()
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        self.counts[tag] += 1
        if values.get('id'):
            self.ids.append(values['id'])
        for key in ('href', 'src'):
            if values.get(key):
                self.links.append(values[key])

def main():
    pages = {p: Page(p.read_text(encoding='utf-8-sig')) for p in ROOT.rglob('*.html') if '.git' not in p.parts}
    errors = []
    links = 0
    for path, page in pages.items():
        for tag in ('h1', 'main', 'title'):
            if page.counts[tag] != 1:
                errors.append(f'{path.relative_to(ROOT)}: expected one {tag}')
        duplicates = [key for key, count in Counter(page.ids).items() if count > 1]
        if duplicates:
            errors.append(f'{path.relative_to(ROOT)}: duplicate IDs {duplicates}')
        for link in page.links:
            parts = urlsplit(link)
            if parts.scheme or parts.netloc:
                continue
            links += 1
            target = (ROOT / unquote(parts.path).lstrip('/')) if parts.path.startswith('/') else (path.parent / unquote(parts.path)) if parts.path else path
            target = target.resolve()
            if target.is_dir():
                target /= 'index.html'
            if not target.is_file():
                errors.append(f'{path.relative_to(ROOT)}: missing {link}')
            elif parts.fragment and target in pages and unquote(parts.fragment) not in pages[target].ids:
                errors.append(f'{path.relative_to(ROOT)}: missing anchor {link}')
    for error in errors:
        print(error)
    print(f'{len(pages)} pages, {links} local links/assets, {len(errors)} errors')
    return bool(errors)

if __name__ == '__main__':
    sys.exit(main())
