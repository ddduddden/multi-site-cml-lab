"""Check repository Markdown links and heading anchors using only Python's standard library.

Run from any directory: python scripts/check_links.py
External websites are outside this check; it verifies links within this repository.
"""
from pathlib import Path
import html
import posixpath
import re
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]


def without_fences(text):
    lines = []
    fence = None
    for line in text.splitlines():
        match = re.match(r'^\s{0,3}(`{3,}|~{3,})', line)
        if match:
            mark = match[1]
            if fence is None:
                fence = mark
            elif mark[0] == fence[0] and len(mark) >= len(fence):
                fence = None
            lines.append('')
        else:
            lines.append('' if fence else line)
    return re.sub(r'<!--.*?-->', '', '\n'.join(lines), flags=re.S)


def slug(text):
    text = re.sub(r'!?\[([^\]]*)\]\([^)]*\)', r'\1', text)
    text = html.unescape(re.sub(r'<[^>]+>', '', text))
    text = text.replace('`', '').replace('*', '').lower()
    return re.sub(r'[^\w\- ]', '', text).replace(' ', '-')


def anchors(text):
    text = without_fences(text)
    found = set(re.findall(r'\b(?:id|name)=["\x27]([^"\x27]+)', text))
    counts = {}
    lines = text.splitlines()
    for i, line in enumerate(lines):
        match = re.match(r'^\s{0,3}#{1,6}\s+(.+?)(?:\s+#+)?\s*$', line)
        title = match[1] if match else None
        if not title and i and re.match(r'^\s{0,3}(?:=+|-+)\s*$', line):
            previous = lines[i - 1].strip()
            if previous and not previous.startswith(('#', '|', '-', '*', '>')):
                title = previous
        if title:
            key = slug(title)
            count = counts.get(key, 0)
            found.add(key + (f'-{count}' if count else ''))
            counts[key] = count + 1
    return found


def links(text):
    text = without_fences(text)
    # Protect literal inline code, but retain HTML hrefs in GitHub navigation tables.
    text = re.sub(r'(`+).*?\1', '', text)
    refs = {key.lower(): target for key, target in
            re.findall(r'^\s{0,3}\[([^\]]+)\]:\s*<?(\S+?)>?(?:\s+["\x27].*)?$', text, re.M)}
    for match in re.finditer(r'!?\[[^\]\n]*\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+["\x27][^\n]*?["\x27])?\s*\)', text):
        yield match[1].strip('<>')
    for target in re.findall(r'\b(?:href|src)=["\x27]([^"\x27]+)', text):
        yield html.unescape(target)
    for label, key in re.findall(r'!?\[([^\]\n]+)\]\[([^\]\n]*)\]', text):
        key = (key or label).lower()
        yield refs.get(key, '__missing_reference__/' + key)
    for target in refs.values():
        yield target


def check(root=ROOT):
    paths = {p.relative_to(root).as_posix(): p for p in root.rglob('*')
             if '.git' not in p.relative_to(root).parts}
    errors = []
    count = 0
    cache = {}
    for name, source in sorted(paths.items()):
        if not source.is_file() or source.suffix.lower() != '.md':
            continue
        for target in links(source.read_text(encoding='utf-8')):
            parts = urlsplit(target)
            if parts.scheme or parts.netloc:
                continue
            count += 1
            file = unquote(parts.path)
            dest = (root / file.lstrip('/')) if file.startswith('/') else (source.parent / file)
            if not file:
                dest = source
            # Keep the supplied spelling: Windows resolve() can silently correct case.
            relative = posixpath.normpath(file.lstrip('/') if file.startswith('/') else
                                         posixpath.join(posixpath.dirname(name), file)) if file else name
            try:
                dest.resolve().relative_to(root.resolve())
            except ValueError:
                errors.append(f'{name}: target leaves repository: {target}')
                continue
            if relative not in paths:
                errors.append(f'{name}: missing path or wrong filename case: {target}')
                continue
            if dest.is_dir() and parts.fragment:
                dest = dest / 'README.md'
            if parts.fragment and dest.suffix.lower() == '.md':
                if not dest.is_file():
                    errors.append(f'{name}: no README for anchor: {target}')
                    continue
                if dest not in cache:
                    cache[dest] = anchors(dest.read_text(encoding='utf-8'))
                if unquote(parts.fragment) not in cache[dest]:
                    errors.append(f'{name}: missing heading anchor: {target}')
    return count, errors


if __name__ == '__main__':
    checked, errors = check()
    for error in errors:
        print(error)
    print(f'Checked {checked} internal links; {len(errors)} error(s).')
    sys.exit(bool(errors))
